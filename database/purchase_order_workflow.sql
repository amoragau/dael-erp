-- ========================================
-- SISTEMA DE ORDENES DE COMPRA - FLUJO COMPLETO DE 5 PASOS
-- Sistema ERP DAEL - Script de actualización
-- ========================================

USE `erp-dael`;

-- ========================================
-- 1. MODIFICACIONES A TABLAS EXISTENTES
-- ========================================

-- Agregar campos adicionales a ordenes_compra para soporte XML y workflow
ALTER TABLE ordenes_compra ADD COLUMN IF NOT EXISTS `xml_original` LONGTEXT NULL COMMENT 'XML original del documento';
ALTER TABLE ordenes_compra ADD COLUMN IF NOT EXISTS `xml_procesado` BOOLEAN DEFAULT FALSE COMMENT 'Indica si el XML fue procesado';
ALTER TABLE ordenes_compra ADD COLUMN IF NOT EXISTS `numero_documento_externo` VARCHAR(100) NULL COMMENT 'Número de documento del proveedor';
ALTER TABLE ordenes_compra ADD COLUMN IF NOT EXISTS `firma_digital` TEXT NULL COMMENT 'Firma digital del documento';
ALTER TABLE ordenes_compra ADD COLUMN IF NOT EXISTS `uuid_fiscal` VARCHAR(36) NULL COMMENT 'UUID fiscal del documento';
ALTER TABLE ordenes_compra ADD COLUMN IF NOT EXISTS `serie_documento` VARCHAR(20) NULL COMMENT 'Serie del documento fiscal';
ALTER TABLE ordenes_compra ADD COLUMN IF NOT EXISTS `folio_documento` VARCHAR(50) NULL COMMENT 'Folio del documento fiscal';

-- ========================================
-- 2. TABLA PARA DOCUMENTOS ASOCIADOS A OC
-- ========================================

CREATE TABLE IF NOT EXISTS documentos_orden_compra (
    id_documento_oc INT AUTO_INCREMENT PRIMARY KEY,
    id_orden_compra INT NOT NULL,
    tipo_documento ENUM('ORDEN_COMPRA', 'FACTURA', 'REMISION', 'RECIBO', 'CONTRATO', 'COTIZACION', 'XML_FACTURA', 'PDF_FACTURA') NOT NULL,
    numero_documento VARCHAR(100) NOT NULL,
    fecha_documento DATE NOT NULL,

    -- Datos fiscales
    serie VARCHAR(20) NULL,
    folio VARCHAR(50) NULL,
    uuid_fiscal VARCHAR(36) NULL,
    rfc_emisor VARCHAR(20) NULL,
    rfc_receptor VARCHAR(20) NULL,

    -- Montos
    subtotal DECIMAL(15,4) DEFAULT 0,
    impuestos DECIMAL(15,4) DEFAULT 0,
    descuentos DECIMAL(15,4) DEFAULT 0,
    total DECIMAL(15,4) DEFAULT 0,
    moneda VARCHAR(3) DEFAULT 'MXN',
    tipo_cambio DECIMAL(10,4) DEFAULT 1.0000,

    -- Archivos
    ruta_archivo_original VARCHAR(500) NULL COMMENT 'Ruta del archivo original',
    ruta_archivo_xml VARCHAR(500) NULL COMMENT 'Ruta del archivo XML',
    ruta_archivo_pdf VARCHAR(500) NULL COMMENT 'Ruta del archivo PDF',
    contenido_xml LONGTEXT NULL COMMENT 'Contenido del XML',

    -- Estado y procesamiento
    estado ENUM('PENDIENTE', 'PROCESADO', 'ERROR', 'VALIDADO', 'CONCILIADO') DEFAULT 'PENDIENTE',
    fecha_procesamiento DATETIME NULL,
    errores_procesamiento TEXT NULL,
    observaciones TEXT NULL,

    -- Control
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modificacion INT NULL,

    -- Índices
    INDEX idx_orden_compra (id_orden_compra),
    INDEX idx_tipo_documento (tipo_documento),
    INDEX idx_numero_documento (numero_documento),
    INDEX idx_uuid_fiscal (uuid_fiscal),
    INDEX idx_estado (estado),
    INDEX idx_fecha_documento (fecha_documento),

    -- Claves foráneas
    FOREIGN KEY (id_orden_compra) REFERENCES ordenes_compra(id_orden_compra),
    FOREIGN KEY (usuario_creacion) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (usuario_modificacion) REFERENCES usuarios(id_usuario),

    -- Constraints únicos
    UNIQUE KEY unique_orden_tipo_numero (id_orden_compra, tipo_documento, numero_documento),
    UNIQUE KEY unique_uuid_fiscal (uuid_fiscal)
);

-- ========================================
-- 3. TABLA DE CONCILIACIÓN OC-FACTURAS
-- ========================================

CREATE TABLE IF NOT EXISTS conciliacion_oc_facturas (
    id_conciliacion INT AUTO_INCREMENT PRIMARY KEY,
    id_orden_compra INT NOT NULL,
    id_documento_factura INT NOT NULL,

    -- Información de conciliación
    tipo_conciliacion ENUM('AUTOMATICA', 'MANUAL', 'PARCIAL') NOT NULL,
    fecha_conciliacion DATETIME NOT NULL,
    id_usuario_concilia INT NOT NULL,

    -- Resultados de conciliación
    productos_conciliados INT DEFAULT 0,
    productos_con_diferencias INT DEFAULT 0,
    diferencia_total DECIMAL(15,4) DEFAULT 0,
    porcentaje_coincidencia DECIMAL(5,2) DEFAULT 0,

    -- Estado
    estado ENUM('PENDIENTE', 'CONCILIADA', 'CON_DIFERENCIAS', 'RECHAZADA') DEFAULT 'PENDIENTE',
    observaciones TEXT NULL,
    aprobado_por INT NULL,
    fecha_aprobacion DATETIME NULL,

    -- Control
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Índices
    INDEX idx_orden_compra (id_orden_compra),
    INDEX idx_documento_factura (id_documento_factura),
    INDEX idx_estado (estado),
    INDEX idx_fecha_conciliacion (fecha_conciliacion),

    -- Claves foráneas
    FOREIGN KEY (id_orden_compra) REFERENCES ordenes_compra(id_orden_compra),
    FOREIGN KEY (id_documento_factura) REFERENCES documentos_orden_compra(id_documento_oc),
    FOREIGN KEY (id_usuario_concilia) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (aprobado_por) REFERENCES usuarios(id_usuario)
);

-- ========================================
-- 4. DETALLE DE CONCILIACIÓN POR PRODUCTO
-- ========================================

CREATE TABLE IF NOT EXISTS conciliacion_detalle (
    id_detalle_conciliacion INT AUTO_INCREMENT PRIMARY KEY,
    id_conciliacion INT NOT NULL,
    id_producto INT NOT NULL,

    -- Datos de la orden de compra
    cantidad_oc DECIMAL(12,4) NOT NULL,
    precio_unitario_oc DECIMAL(15,4) NOT NULL,
    importe_oc DECIMAL(15,4) NOT NULL,

    -- Datos de la factura
    cantidad_factura DECIMAL(12,4) NOT NULL,
    precio_unitario_factura DECIMAL(15,4) NOT NULL,
    importe_factura DECIMAL(15,4) NOT NULL,
    descripcion_factura TEXT NULL,

    -- Diferencias
    diferencia_cantidad DECIMAL(12,4) GENERATED ALWAYS AS (cantidad_factura - cantidad_oc) STORED,
    diferencia_precio DECIMAL(15,4) GENERATED ALWAYS AS (precio_unitario_factura - precio_unitario_oc) STORED,
    diferencia_importe DECIMAL(15,4) GENERATED ALWAYS AS (importe_factura - importe_oc) STORED,

    -- Estado de conciliación del producto
    estado_producto ENUM('COINCIDE', 'DIFERENCIA_CANTIDAD', 'DIFERENCIA_PRECIO', 'DIFERENCIA_TOTAL', 'NO_ENCONTRADO') NOT NULL,
    observaciones TEXT NULL,
    accion_tomada ENUM('ACEPTAR', 'RECHAZAR', 'AJUSTAR', 'PENDIENTE') DEFAULT 'PENDIENTE',

    -- Control
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Índices
    INDEX idx_conciliacion (id_conciliacion),
    INDEX idx_producto (id_producto),
    INDEX idx_estado_producto (estado_producto),

    -- Claves foráneas
    FOREIGN KEY (id_conciliacion) REFERENCES conciliacion_oc_facturas(id_conciliacion),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- ========================================
-- 5. TABLA DE AJUSTES DE INVENTARIO POR CONCILIACIÓN
-- ========================================

CREATE TABLE IF NOT EXISTS ajustes_conciliacion (
    id_ajuste INT AUTO_INCREMENT PRIMARY KEY,
    id_conciliacion INT NOT NULL,
    id_producto INT NOT NULL,

    -- Tipo de ajuste
    tipo_ajuste ENUM('CANTIDAD', 'PRECIO', 'NUEVO_PRODUCTO', 'ELIMINACION') NOT NULL,

    -- Valores antes del ajuste
    cantidad_anterior DECIMAL(12,4) DEFAULT 0,
    precio_anterior DECIMAL(15,4) DEFAULT 0,

    -- Valores después del ajuste
    cantidad_nueva DECIMAL(12,4) DEFAULT 0,
    precio_nuevo DECIMAL(15,4) DEFAULT 0,

    -- Justificación
    motivo_ajuste TEXT NOT NULL,
    autorizado_por INT NOT NULL,
    fecha_autorizacion DATETIME NOT NULL,

    -- Control
    procesado BOOLEAN DEFAULT FALSE,
    fecha_procesamiento DATETIME NULL,
    id_movimiento_inventario INT NULL,

    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Índices
    INDEX idx_conciliacion (id_conciliacion),
    INDEX idx_producto (id_producto),
    INDEX idx_tipo_ajuste (tipo_ajuste),
    INDEX idx_procesado (procesado),

    -- Claves foráneas
    FOREIGN KEY (id_conciliacion) REFERENCES conciliacion_oc_facturas(id_conciliacion),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (autorizado_por) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_movimiento_inventario) REFERENCES movimientos_inventario(id_movimiento)
);

-- ========================================
-- 6. NUEVOS ESTADOS PARA ÓRDENES DE COMPRA
-- ========================================

-- Actualizar estados existentes y agregar nuevos para el workflow de 5 pasos
INSERT INTO estados_orden_compra (codigo_estado, nombre_estado, descripcion, es_estado_inicial, es_estado_final, permite_edicion, permite_cancelacion) VALUES
('RECIBIDA', 'Mercancía Recibida', 'Mercancía recibida físicamente', FALSE, FALSE, FALSE, FALSE),
('FACTURADA', 'Facturada', 'Factura recibida y procesada', FALSE, FALSE, FALSE, FALSE),
('CONCILIADA', 'Conciliada', 'Orden conciliada con factura', FALSE, FALSE, FALSE, FALSE),
('PAGADA', 'Pagada', 'Orden pagada al proveedor', FALSE, TRUE, FALSE, FALSE),
('CERRADA', 'Cerrada', 'Orden cerrada y archivada', FALSE, TRUE, FALSE, FALSE)
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);

-- ========================================
-- 7. TABLA PARA HISTORIAL DE ESTADOS
-- ========================================

CREATE TABLE IF NOT EXISTS historial_estados_oc (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_orden_compra INT NOT NULL,
    id_estado_anterior INT NULL,
    id_estado_nuevo INT NOT NULL,
    fecha_cambio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_usuario INT NOT NULL,
    observaciones TEXT NULL,

    -- Índices
    INDEX idx_orden_compra (id_orden_compra),
    INDEX idx_fecha_cambio (fecha_cambio),
    INDEX idx_usuario (id_usuario),

    -- Claves foráneas
    FOREIGN KEY (id_orden_compra) REFERENCES ordenes_compra(id_orden_compra),
    FOREIGN KEY (id_estado_anterior) REFERENCES estados_orden_compra(id_estado),
    FOREIGN KEY (id_estado_nuevo) REFERENCES estados_orden_compra(id_estado),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- ========================================
-- 8. TABLA PARA PAGOS A PROVEEDORES
-- ========================================

CREATE TABLE IF NOT EXISTS pagos_ordenes_compra (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_orden_compra INT NOT NULL,
    numero_pago VARCHAR(50) NOT NULL UNIQUE,

    -- Información del pago
    fecha_pago DATE NOT NULL,
    monto_pago DECIMAL(15,4) NOT NULL,
    moneda VARCHAR(3) DEFAULT 'MXN',
    tipo_cambio DECIMAL(10,4) DEFAULT 1.0000,

    -- Método de pago
    metodo_pago ENUM('TRANSFERENCIA', 'CHEQUE', 'EFECTIVO', 'TARJETA', 'OTRO') NOT NULL,
    referencia_pago VARCHAR(100) NULL,
    numero_cheque VARCHAR(50) NULL,
    banco VARCHAR(100) NULL,
    cuenta_origen VARCHAR(50) NULL,
    cuenta_destino VARCHAR(50) NULL,

    -- Descuentos y retenciones
    descuentos DECIMAL(15,4) DEFAULT 0,
    retenciones DECIMAL(15,4) DEFAULT 0,
    iva_retenido DECIMAL(15,4) DEFAULT 0,
    isr_retenido DECIMAL(15,4) DEFAULT 0,

    -- Control
    estado ENUM('PENDIENTE', 'PROCESADO', 'CONFIRMADO', 'CANCELADO') DEFAULT 'PENDIENTE',
    autorizado_por INT NOT NULL,
    fecha_autorizacion DATETIME NOT NULL,
    observaciones TEXT NULL,

    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Índices
    INDEX idx_orden_compra (id_orden_compra),
    INDEX idx_numero_pago (numero_pago),
    INDEX idx_fecha_pago (fecha_pago),
    INDEX idx_estado (estado),
    INDEX idx_metodo_pago (metodo_pago),

    -- Claves foráneas
    FOREIGN KEY (id_orden_compra) REFERENCES ordenes_compra(id_orden_compra),
    FOREIGN KEY (autorizado_por) REFERENCES usuarios(id_usuario)
);

-- ========================================
-- 9. CONFIGURACIÓN PARA XML Y DOCUMENTOS
-- ========================================

-- Agregar configuraciones específicas para el manejo de documentos
INSERT INTO configuracion_sistema (parametro, valor, tipo_dato, descripcion, modificable) VALUES
('RUTA_ALMACEN_XML', '/var/erp/documentos/xml/', 'STRING', 'Ruta donde se almacenan los archivos XML', TRUE),
('RUTA_ALMACEN_PDF', '/var/erp/documentos/pdf/', 'STRING', 'Ruta donde se almacenan los archivos PDF', TRUE),
('VALIDAR_XML_SAT', 'TRUE', 'BOOLEAN', 'Validar XMLs contra el SAT', TRUE),
('AUTO_CONCILIAR_OC', 'TRUE', 'BOOLEAN', 'Conciliar automáticamente OC con facturas', TRUE),
('TOLERANCIA_PRECIO_CONCILIACION', '5.00', 'DECIMAL', 'Porcentaje de tolerancia en precios para conciliación automática', TRUE),
('TOLERANCIA_CANTIDAD_CONCILIACION', '2.00', 'DECIMAL', 'Porcentaje de tolerancia en cantidades para conciliación automática', TRUE),
('REQUIERE_APROBACION_AJUSTES', 'TRUE', 'BOOLEAN', 'Los ajustes por conciliación requieren aprobación', TRUE),
('DIAS_LIMITE_CONCILIACION', '30', 'INTEGER', 'Días límite para conciliar OC con facturas', TRUE),
('GENERAR_MOVIMIENTO_AUTO_RECEPCION', 'TRUE', 'BOOLEAN', 'Generar movimiento de inventario automático al recibir mercancía', TRUE)
ON DUPLICATE KEY UPDATE valor = VALUES(valor);

-- ========================================
-- 10. VISTAS PARA EL WORKFLOW DE 5 PASOS
-- ========================================

-- Vista resumen del workflow de órdenes de compra
CREATE OR REPLACE VIEW vista_workflow_ordenes_compra AS
SELECT
    oc.id_orden_compra,
    oc.numero_orden,
    p.nombre_proveedor,
    eoc.nombre_estado,
    eoc.codigo_estado,

    -- Paso 1: Orden de Compra
    oc.fecha_orden,
    oc.total as monto_orden,

    -- Paso 2: Recepción de Mercancía
    rm.fecha_recepcion,
    rm.recepcion_completa,

    -- Paso 3: Recepción de Factura
    doc_fact.fecha_documento as fecha_factura,
    doc_fact.total as monto_factura,
    doc_fact.estado as estado_factura,

    -- Paso 4: Conciliación
    conc.fecha_conciliacion,
    conc.estado as estado_conciliacion,
    conc.porcentaje_coincidencia,

    -- Paso 5: Pago
    pago.fecha_pago,
    pago.monto_pago,
    pago.estado as estado_pago,

    -- Indicadores de progreso
    CASE
        WHEN oc.id_estado IN (SELECT id_estado FROM estados_orden_compra WHERE codigo_estado IN ('BORRADOR', 'PENDIENTE', 'APROBADA', 'ENVIADA')) THEN 1
        ELSE 0
    END as paso_1_completado,

    CASE
        WHEN rm.id_recepcion IS NOT NULL AND rm.recepcion_completa = TRUE THEN 1
        ELSE 0
    END as paso_2_completado,

    CASE
        WHEN doc_fact.id_documento_oc IS NOT NULL AND doc_fact.estado = 'PROCESADO' THEN 1
        ELSE 0
    END as paso_3_completado,

    CASE
        WHEN conc.id_conciliacion IS NOT NULL AND conc.estado = 'CONCILIADA' THEN 1
        ELSE 0
    END as paso_4_completado,

    CASE
        WHEN pago.id_pago IS NOT NULL AND pago.estado = 'CONFIRMADO' THEN 1
        ELSE 0
    END as paso_5_completado

FROM ordenes_compra oc
INNER JOIN proveedores p ON oc.id_proveedor = p.id_proveedor
INNER JOIN estados_orden_compra eoc ON oc.id_estado = eoc.id_estado
LEFT JOIN recepciones_mercancia rm ON oc.id_orden_compra = rm.id_orden_compra
LEFT JOIN documentos_orden_compra doc_fact ON oc.id_orden_compra = doc_fact.id_orden_compra
    AND doc_fact.tipo_documento = 'FACTURA' AND doc_fact.activo = TRUE
LEFT JOIN conciliacion_oc_facturas conc ON oc.id_orden_compra = conc.id_orden_compra AND conc.activo = TRUE
LEFT JOIN pagos_ordenes_compra pago ON oc.id_orden_compra = pago.id_orden_compra AND pago.activo = TRUE
WHERE oc.activo = TRUE;

-- Vista de órdenes pendientes por paso
CREATE OR REPLACE VIEW vista_ordenes_pendientes_por_paso AS
SELECT
    'Paso 1: Orden de Compra' as paso,
    COUNT(*) as cantidad_pendiente,
    'BORRADOR,PENDIENTE' as estados_incluidos
FROM ordenes_compra oc
INNER JOIN estados_orden_compra eoc ON oc.id_estado = eoc.id_estado
WHERE oc.activo = TRUE AND eoc.codigo_estado IN ('BORRADOR', 'PENDIENTE')

UNION ALL

SELECT
    'Paso 2: Recepción de Mercancía' as paso,
    COUNT(*) as cantidad_pendiente,
    'APROBADA,ENVIADA' as estados_incluidos
FROM ordenes_compra oc
INNER JOIN estados_orden_compra eoc ON oc.id_estado = eoc.id_estado
LEFT JOIN recepciones_mercancia rm ON oc.id_orden_compra = rm.id_orden_compra
WHERE oc.activo = TRUE
    AND eoc.codigo_estado IN ('APROBADA', 'ENVIADA')
    AND (rm.id_recepcion IS NULL OR rm.recepcion_completa = FALSE)

UNION ALL

SELECT
    'Paso 3: Recepción de Factura' as paso,
    COUNT(*) as cantidad_pendiente,
    'RECIBIDA' as estados_incluidos
FROM ordenes_compra oc
INNER JOIN estados_orden_compra eoc ON oc.id_estado = eoc.id_estado
LEFT JOIN documentos_orden_compra doc ON oc.id_orden_compra = doc.id_orden_compra
    AND doc.tipo_documento = 'FACTURA' AND doc.activo = TRUE
WHERE oc.activo = TRUE
    AND eoc.codigo_estado = 'RECIBIDA'
    AND doc.id_documento_oc IS NULL

UNION ALL

SELECT
    'Paso 4: Conciliación' as paso,
    COUNT(*) as cantidad_pendiente,
    'FACTURADA' as estados_incluidos
FROM ordenes_compra oc
INNER JOIN estados_orden_compra eoc ON oc.id_estado = eoc.id_estado
LEFT JOIN conciliacion_oc_facturas conc ON oc.id_orden_compra = conc.id_orden_compra AND conc.activo = TRUE
WHERE oc.activo = TRUE
    AND eoc.codigo_estado = 'FACTURADA'
    AND (conc.id_conciliacion IS NULL OR conc.estado != 'CONCILIADA')

UNION ALL

SELECT
    'Paso 5: Pago' as paso,
    COUNT(*) as cantidad_pendiente,
    'CONCILIADA' as estados_incluidos
FROM ordenes_compra oc
INNER JOIN estados_orden_compra eoc ON oc.id_estado = eoc.id_estado
LEFT JOIN pagos_ordenes_compra pago ON oc.id_orden_compra = pago.id_orden_compra AND pago.activo = TRUE
WHERE oc.activo = TRUE
    AND eoc.codigo_estado = 'CONCILIADA'
    AND (pago.id_pago IS NULL OR pago.estado != 'CONFIRMADO');

-- ========================================
-- 11. TRIGGERS PARA AUTOMATIZACIÓN DEL WORKFLOW
-- ========================================

-- Trigger para registrar cambios de estado en el historial
DELIMITER //
CREATE TRIGGER IF NOT EXISTS tr_historial_estado_oc
    AFTER UPDATE ON ordenes_compra
    FOR EACH ROW
BEGIN
    IF OLD.id_estado != NEW.id_estado THEN
        INSERT INTO historial_estados_oc (
            id_orden_compra,
            id_estado_anterior,
            id_estado_nuevo,
            fecha_cambio,
            id_usuario,
            observaciones
        ) VALUES (
            NEW.id_orden_compra,
            OLD.id_estado,
            NEW.id_estado,
            NOW(),
            COALESCE(@usuario_id, NEW.id_usuario_solicitante),
            CONCAT('Cambio automático de estado de ',
                   (SELECT nombre_estado FROM estados_orden_compra WHERE id_estado = OLD.id_estado),
                   ' a ',
                   (SELECT nombre_estado FROM estados_orden_compra WHERE id_estado = NEW.id_estado))
        );
    END IF;
END//
DELIMITER ;

-- Trigger para actualizar estado después de recepción completa
DELIMITER //
CREATE TRIGGER IF NOT EXISTS tr_estado_despues_recepcion
    AFTER UPDATE ON recepciones_mercancia
    FOR EACH ROW
BEGIN
    IF NEW.recepcion_completa = TRUE AND OLD.recepcion_completa = FALSE THEN
        UPDATE ordenes_compra
        SET id_estado = (SELECT id_estado FROM estados_orden_compra WHERE codigo_estado = 'RECIBIDA')
        WHERE id_orden_compra = NEW.id_orden_compra;
    END IF;
END//
DELIMITER ;

-- Trigger para actualizar estado después de procesar factura
DELIMITER //
CREATE TRIGGER IF NOT EXISTS tr_estado_despues_factura
    AFTER UPDATE ON documentos_orden_compra
    FOR EACH ROW
BEGIN
    IF NEW.tipo_documento = 'FACTURA'
       AND NEW.estado = 'PROCESADO'
       AND OLD.estado != 'PROCESADO' THEN
        UPDATE ordenes_compra
        SET id_estado = (SELECT id_estado FROM estados_orden_compra WHERE codigo_estado = 'FACTURADA')
        WHERE id_orden_compra = NEW.id_orden_compra;
    END IF;
END//
DELIMITER ;

-- Trigger para actualizar estado después de conciliación
DELIMITER //
CREATE TRIGGER IF NOT EXISTS tr_estado_despues_conciliacion
    AFTER UPDATE ON conciliacion_oc_facturas
    FOR EACH ROW
BEGIN
    IF NEW.estado = 'CONCILIADA' AND OLD.estado != 'CONCILIADA' THEN
        UPDATE ordenes_compra
        SET id_estado = (SELECT id_estado FROM estados_orden_compra WHERE codigo_estado = 'CONCILIADA')
        WHERE id_orden_compra = NEW.id_orden_compra;
    END IF;
END//
DELIMITER ;

-- Trigger para actualizar estado después de pago
DELIMITER //
CREATE TRIGGER IF NOT EXISTS tr_estado_despues_pago
    AFTER UPDATE ON pagos_ordenes_compra
    FOR EACH ROW
BEGIN
    IF NEW.estado = 'CONFIRMADO' AND OLD.estado != 'CONFIRMADO' THEN
        UPDATE ordenes_compra
        SET id_estado = (SELECT id_estado FROM estados_orden_compra WHERE codigo_estado = 'PAGADA')
        WHERE id_orden_compra = NEW.id_orden_compra;
    END IF;
END//
DELIMITER ;

-- ========================================
-- 12. PROCEDIMIENTOS ALMACENADOS PARA WORKFLOW
-- ========================================

-- Procedimiento para conciliación automática
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS sp_conciliar_oc_automatica(
    IN p_id_orden_compra INT,
    IN p_id_documento_factura INT,
    IN p_id_usuario INT,
    OUT p_resultado VARCHAR(100)
)
BEGIN
    DECLARE v_id_conciliacion INT;
    DECLARE v_tolerancia_precio DECIMAL(5,2);
    DECLARE v_tolerancia_cantidad DECIMAL(5,2);
    DECLARE v_productos_coincidentes INT DEFAULT 0;
    DECLARE v_productos_total INT DEFAULT 0;
    DECLARE v_porcentaje_coincidencia DECIMAL(5,2);

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_resultado = 'ERROR: No se pudo realizar la conciliación automática';
    END;

    START TRANSACTION;

    -- Obtener tolerancias del sistema
    SELECT CAST(valor AS DECIMAL(5,2)) INTO v_tolerancia_precio
    FROM configuracion_sistema
    WHERE parametro = 'TOLERANCIA_PRECIO_CONCILIACION';

    SELECT CAST(valor AS DECIMAL(5,2)) INTO v_tolerancia_cantidad
    FROM configuracion_sistema
    WHERE parametro = 'TOLERANCIA_CANTIDAD_CONCILIACION';

    -- Crear registro de conciliación
    INSERT INTO conciliacion_oc_facturas (
        id_orden_compra, id_documento_factura, tipo_conciliacion,
        fecha_conciliacion, id_usuario_concilia
    ) VALUES (
        p_id_orden_compra, p_id_documento_factura, 'AUTOMATICA',
        NOW(), p_id_usuario
    );

    SET v_id_conciliacion = LAST_INSERT_ID();

    -- Conciliar productos
    INSERT INTO conciliacion_detalle (
        id_conciliacion, id_producto, cantidad_oc, precio_unitario_oc, importe_oc,
        cantidad_factura, precio_unitario_factura, importe_factura, estado_producto
    )
    SELECT
        v_id_conciliacion,
        ocd.id_producto,
        ocd.cantidad_solicitada,
        ocd.precio_unitario,
        ocd.importe_total,
        0, 0, 0, -- Estos valores se actualizarían con los datos de la factura
        'PENDIENTE'
    FROM ordenes_compra_detalle ocd
    WHERE ocd.id_orden_compra = p_id_orden_compra AND ocd.activo = TRUE;

    -- Calcular porcentaje de coincidencia (simplificado)
    SELECT COUNT(*) INTO v_productos_total
    FROM conciliacion_detalle
    WHERE id_conciliacion = v_id_conciliacion;

    SET v_porcentaje_coincidencia = (v_productos_coincidentes * 100.0) / v_productos_total;

    -- Actualizar conciliación
    UPDATE conciliacion_oc_facturas
    SET productos_conciliados = v_productos_coincidentes,
        productos_con_diferencias = v_productos_total - v_productos_coincidentes,
        porcentaje_coincidencia = v_porcentaje_coincidencia,
        estado = CASE WHEN v_porcentaje_coincidencia >= 95 THEN 'CONCILIADA' ELSE 'CON_DIFERENCIAS' END
    WHERE id_conciliacion = v_id_conciliacion;

    COMMIT;
    SET p_resultado = 'CONCILIACION_AUTOMATICA_EXITOSA';

END//
DELIMITER ;

-- ========================================
-- 13. ALERTAS ESPECÍFICAS PARA EL WORKFLOW
-- ========================================

INSERT INTO configuracion_alertas (nombre_alerta, tipo_alerta, dias_anticipacion, frecuencia_revision_horas) VALUES
('OC pendientes de recepción', 'OC_PENDIENTE_RECEPCION', 7, 24),
('Facturas pendientes de procesar', 'FACTURA_PENDIENTE_PROCESO', 3, 12),
('OC pendientes de conciliación', 'OC_PENDIENTE_CONCILIACION', 15, 24),
('Pagos pendientes', 'PAGO_PENDIENTE', 5, 12),
('XML con errores de procesamiento', 'XML_ERROR_PROCESO', 1, 6)
ON DUPLICATE KEY UPDATE descripcion = VALUES(nombre_alerta);

-- ========================================
-- FIN DEL SCRIPT DE WORKFLOW DE OC
-- ========================================