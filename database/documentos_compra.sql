-- ========================================
-- SISTEMA DE DOCUMENTOS DE COMPRA
-- Sistema ERP DAEL - Script de documentos independientes
-- ========================================

USE `erp-dael`;

-- ========================================
-- 1. LIMPIAR TABLAS EXISTENTES INCORRECTAS
-- ========================================

-- Eliminar tablas del workflow anterior
DROP TABLE IF EXISTS conciliacion_oc_facturas;
DROP TABLE IF EXISTS pagos_ordenes_compra;
DROP TABLE IF EXISTS movimientos_inventario_oc;
DROP TABLE IF EXISTS documentos_orden_compra;

-- Remover columnas XML de ordenes_compra (estas no pertenecen ahí)
ALTER TABLE ordenes_compra
  DROP COLUMN IF EXISTS xml_original,
  DROP COLUMN IF EXISTS xml_procesado,
  DROP COLUMN IF EXISTS numero_documento_externo,
  DROP COLUMN IF EXISTS firma_digital,
  DROP COLUMN IF EXISTS uuid_fiscal,
  DROP COLUMN IF EXISTS serie_documento,
  DROP COLUMN IF EXISTS folio_documento;

-- ========================================
-- 2. TABLA DE DOCUMENTOS DE COMPRA (INDEPENDIENTE)
-- ========================================

CREATE TABLE IF NOT EXISTS documentos_compra (
    id_documento INT AUTO_INCREMENT PRIMARY KEY,

    -- Proveedor (OBLIGATORIO)
    id_proveedor INT NOT NULL COMMENT 'Proveedor emisor del documento',

    -- Relación opcional con orden de compra
    id_orden_compra INT NULL COMMENT 'Orden de compra asociada (opcional)',

    -- Información básica del documento (OBLIGATORIOS)
    tipo_documento ENUM('FACTURA', 'FACTURA_EXENTA', 'BOLETA', 'NOTA_CREDITO', 'NOTA_DEBITO', 'GUIA_DESPACHO', 'OTRO') NOT NULL,
    numero_documento VARCHAR(100) NOT NULL,
    fecha_documento DATE NOT NULL,

    -- Información fiscal chilena
    serie VARCHAR(20) NULL COMMENT 'Serie del documento',
    folio VARCHAR(50) NOT NULL COMMENT 'Folio del documento (OBLIGATORIO)',
    uuid_fiscal VARCHAR(100) NULL COMMENT 'Timbre electrónico único',
    rut_emisor VARCHAR(12) NULL COMMENT 'RUT del emisor',
    rut_receptor VARCHAR(12) NULL COMMENT 'RUT del receptor',

    -- Montos
    subtotal DECIMAL(15,2) NOT NULL DEFAULT 0,
    impuestos DECIMAL(15,2) NOT NULL DEFAULT 0,
    descuentos DECIMAL(15,2) NOT NULL DEFAULT 0,
    total DECIMAL(15,2) NOT NULL DEFAULT 0,
    moneda VARCHAR(3) DEFAULT 'CLP',
    tipo_cambio DECIMAL(10,4) DEFAULT 1.0000,

    -- XML (para documentos electrónicos)
    contenido_xml LONGTEXT NULL COMMENT 'Contenido XML del DTE',

    -- Estado y control
    estado ENUM('PENDIENTE', 'VALIDADO', 'DISPONIBLE_BODEGA', 'INGRESADO_BODEGA', 'ANULADO') DEFAULT 'PENDIENTE',
    disponible_bodega BOOLEAN DEFAULT FALSE COMMENT 'Si está disponible para ingreso a bodega',
    fecha_ingreso_bodega DATETIME NULL COMMENT 'Fecha de ingreso a bodega',
    usuario_ingreso_bodega INT NULL COMMENT 'Usuario que ingresó a bodega',

    -- Observaciones y errores
    observaciones TEXT NULL,
    errores_procesamiento TEXT NULL,

    -- Control de auditoría
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modificacion INT NULL,

    -- Índices
    INDEX idx_proveedor (id_proveedor),
    INDEX idx_orden_compra (id_orden_compra),
    INDEX idx_tipo_documento (tipo_documento),
    INDEX idx_numero_documento (numero_documento),
    INDEX idx_uuid_fiscal (uuid_fiscal),
    INDEX idx_estado (estado),
    INDEX idx_fecha_documento (fecha_documento),
    INDEX idx_disponible_bodega (disponible_bodega),
    INDEX idx_rut_emisor (rut_emisor),

    -- Claves foráneas
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE RESTRICT,
    FOREIGN KEY (id_orden_compra) REFERENCES ordenes_compra(id_orden_compra) ON DELETE SET NULL,
    FOREIGN KEY (usuario_creacion) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (usuario_modificacion) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (usuario_ingreso_bodega) REFERENCES usuarios(id_usuario),

    -- Constraints únicos
    UNIQUE KEY unique_numero_rut_emisor (numero_documento, rut_emisor),
    UNIQUE KEY unique_uuid_fiscal (uuid_fiscal)
) COMMENT 'Documentos de compra independientes (facturas, boletas, etc.)';

-- ========================================
-- 3. TABLA DE DETALLE DE DOCUMENTOS DE COMPRA
-- ========================================

CREATE TABLE IF NOT EXISTS documentos_compra_detalle (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_documento INT NOT NULL,

    -- Información del producto/servicio
    id_producto INT NULL COMMENT 'Producto del catálogo (opcional)',
    codigo_producto VARCHAR(100) NULL COMMENT 'Código del producto en el documento',
    descripcion TEXT NOT NULL COMMENT 'Descripción del item',

    -- Cantidades y medidas
    cantidad DECIMAL(15,4) NOT NULL,
    id_unidad_medida INT NULL,

    -- Precios
    precio_unitario DECIMAL(15,4) NOT NULL,
    descuento_linea DECIMAL(15,4) DEFAULT 0,
    subtotal_linea DECIMAL(15,4) NOT NULL,
    impuesto_linea DECIMAL(15,4) DEFAULT 0,
    total_linea DECIMAL(15,4) NOT NULL,

    -- Control de bodega
    cantidad_recibida DECIMAL(15,4) NULL COMMENT 'Cantidad realmente recibida en bodega',
    diferencia_cantidad DECIMAL(15,4) NULL COMMENT 'Diferencia entre facturado y recibido',
    motivo_diferencia TEXT NULL COMMENT 'Motivo de la diferencia',

    -- Orden en el documento
    numero_linea INT NOT NULL DEFAULT 1,

    -- Control
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Índices
    INDEX idx_documento (id_documento),
    INDEX idx_producto (id_producto),
    INDEX idx_codigo_producto (codigo_producto),
    INDEX idx_numero_linea (numero_linea),

    -- Claves foráneas
    FOREIGN KEY (id_documento) REFERENCES documentos_compra(id_documento) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto) ON DELETE SET NULL,
    FOREIGN KEY (id_unidad_medida) REFERENCES unidades_medida(id_unidad_medida),

    -- Constraints
    UNIQUE KEY unique_documento_linea (id_documento, numero_linea)
) COMMENT 'Detalle de documentos de compra';

-- ========================================
-- 4. TABLA DE ARCHIVOS ADJUNTOS
-- ========================================

CREATE TABLE IF NOT EXISTS documentos_compra_archivos (
    id_archivo INT AUTO_INCREMENT PRIMARY KEY,
    id_documento INT NOT NULL,

    -- Información del archivo
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_archivo VARCHAR(500) NOT NULL,
    tipo_archivo ENUM('XML', 'PDF', 'IMAGEN', 'OTRO') NOT NULL,
    tamaño_archivo BIGINT NULL COMMENT 'Tamaño en bytes',
    mime_type VARCHAR(100) NULL,
    hash_archivo VARCHAR(64) NULL COMMENT 'Hash MD5 del archivo',

    -- Control
    activo BOOLEAN DEFAULT TRUE,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_subida INT NULL,

    -- Índices
    INDEX idx_documento (id_documento),
    INDEX idx_tipo_archivo (tipo_archivo),
    INDEX idx_hash_archivo (hash_archivo),

    -- Claves foráneas
    FOREIGN KEY (id_documento) REFERENCES documentos_compra(id_documento) ON DELETE CASCADE,
    FOREIGN KEY (usuario_subida) REFERENCES usuarios(id_usuario)
) COMMENT 'Archivos adjuntos a documentos de compra';

-- ========================================
-- 5. VISTAS ÚTILES
-- ========================================

-- Vista de documentos con información de OC
CREATE OR REPLACE VIEW vista_documentos_compra AS
SELECT
    d.*,
    p.razon_social as proveedor,
    p.rut as rut_proveedor,
    oc.numero_orden,
    oc.estado as estado_oc,
    (SELECT COUNT(*) FROM documentos_compra_detalle dd WHERE dd.id_documento = d.id_documento AND dd.activo = TRUE) as total_lineas,
    (SELECT COUNT(*) FROM documentos_compra_archivos da WHERE da.id_documento = d.id_documento AND da.activo = TRUE) as total_archivos
FROM documentos_compra d
INNER JOIN proveedores p ON d.id_proveedor = p.id_proveedor
LEFT JOIN ordenes_compra oc ON d.id_orden_compra = oc.id_orden_compra
WHERE d.activo = TRUE;

-- Vista de detalle completo
CREATE OR REPLACE VIEW vista_documentos_detalle_completo AS
SELECT
    d.id_documento,
    d.numero_documento,
    d.fecha_documento,
    d.total,
    dd.*,
    pr.codigo as codigo_producto_catalogo,
    pr.nombre as nombre_producto_catalogo,
    um.nombre as unidad_medida
FROM documentos_compra d
INNER JOIN documentos_compra_detalle dd ON d.id_documento = dd.id_documento
LEFT JOIN productos pr ON dd.id_producto = pr.id_producto
LEFT JOIN unidades_medida um ON dd.id_unidad_medida = um.id_unidad_medida
WHERE d.activo = TRUE AND dd.activo = TRUE;