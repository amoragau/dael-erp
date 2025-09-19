-- ========================================
-- SISTEMA DE INVENTARIO - ESTRUCTURA DE BASE DE DATOS
-- Para Sistemas Contra Incendios y Construcción
-- ========================================


-- Crea la base de datos si no existe
CREATE DATABASE IF NOT EXISTS erp-dael;

-- Usa la base de datos recién creada
USE erp-dael;

-- ========================================
-- 1. TABLAS MAESTRAS Y CATALOGOS
-- ========================================

-- Categorías principales de productos
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    codigo_categoria VARCHAR(10) NOT NULL UNIQUE, -- DET, EXT, FIT, CON
    nombre_categoria VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Subcategorías de productos
CREATE TABLE IF NOT EXISTS subcategorias (
    id_subcategoria INT PRIMARY KEY AUTO_INCREMENT,
    id_categoria INT NOT NULL,
    codigo_subcategoria VARCHAR(10) NOT NULL, -- SEN, CEN, SPK, TUB, etc.
    nombre_subcategoria VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    UNIQUE KEY unique_sub_cat (id_categoria, codigo_subcategoria)
);

-- Tipos de productos dentro de subcategorías
CREATE TABLE IF NOT EXISTS tipos_producto (
    id_tipo_producto INT PRIMARY KEY AUTO_INCREMENT,
    id_subcategoria INT NOT NULL,
    codigo_tipo VARCHAR(10) NOT NULL, -- HUM, ION, UPR, ACE, etc.
    nombre_tipo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_subcategoria) REFERENCES subcategorias(id_subcategoria),
    UNIQUE KEY unique_tipo_prod (id_subcategoria, codigo_tipo)
);

-- Marcas/Fabricantes
CREATE TABLE IF NOT EXISTS marcas (
    id_marca INT PRIMARY KEY AUTO_INCREMENT,
    nombre_marca VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    pais_origen VARCHAR(50),
    sitio_web VARCHAR(200),
    contacto_tecnico VARCHAR(200),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT PRIMARY KEY AUTO_INCREMENT,
    codigo_proveedor VARCHAR(20) NOT NULL UNIQUE,
    nombre_proveedor VARCHAR(200) NOT NULL,
    razon_social VARCHAR(200),
    rfc VARCHAR(20),
    direccion TEXT,
    ciudad VARCHAR(100),
    estado VARCHAR(50),
    codigo_postal VARCHAR(10),
    pais VARCHAR(50) DEFAULT 'México',
    telefono VARCHAR(20),
    email VARCHAR(100),
    contacto_principal VARCHAR(100),
    dias_credito INT DEFAULT 0,
    limite_credito DECIMAL(15,2) DEFAULT 0,
    descuento_general DECIMAL(5,2) DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Unidades de medida
CREATE TABLE IF NOT EXISTS unidades_medida (
    id_unidad INT PRIMARY KEY AUTO_INCREMENT,
    codigo_unidad VARCHAR(10) NOT NULL UNIQUE, -- PZA, MT, LT, KG, etc.
    nombre_unidad VARCHAR(50) NOT NULL,
    descripcion VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE
);

-- ========================================
-- 2. ESTRUCTURA DEL ALMACÉN (ACTUALIZADO A BODEGAS)
-- ========================================

-- Bodegas del almacén
CREATE TABLE IF NOT EXISTS bodegas (
    id_bodega INT PRIMARY KEY AUTO_INCREMENT,
    codigo_bodega CHAR(1) NOT NULL UNIQUE, -- A, B, C, D, E, F, G, H, I
    nombre_bodega VARCHAR(100) NOT NULL,
    descripcion TEXT,
    temperatura_min DECIMAL(5,2),
    temperatura_max DECIMAL(5,2),
    humedad_max DECIMAL(5,2),
    requiere_certificacion BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE
);

-- Pasillos dentro de cada bodega
CREATE TABLE IF NOT EXISTS pasillos (
    id_pasillo INT PRIMARY KEY AUTO_INCREMENT,
    id_bodega INT NOT NULL,
    numero_pasillo INT NOT NULL,
    nombre_pasillo VARCHAR(50),
    longitud_metros DECIMAL(6,2),
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_bodega) REFERENCES bodegas(id_bodega),
    UNIQUE KEY unique_pasillo_bodega (id_bodega, numero_pasillo)
);

-- Estantes dentro de cada pasillo
CREATE TABLE IF NOT EXISTS estantes (
    id_estante INT PRIMARY KEY AUTO_INCREMENT,
    id_pasillo INT NOT NULL,
    codigo_estante VARCHAR(5) NOT NULL, -- A, B, C, etc.
    altura_metros DECIMAL(4,2),
    capacidad_peso_kg DECIMAL(8,2),
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_pasillo) REFERENCES pasillos(id_pasillo),
    UNIQUE KEY unique_estante_pasillo (id_pasillo, codigo_estante)
);

-- Niveles dentro de cada estante
CREATE TABLE IF NOT EXISTS niveles (
    id_nivel INT PRIMARY KEY AUTO_INCREMENT,
    id_estante INT NOT NULL,
    numero_nivel INT NOT NULL, -- 1, 2, 3, etc.
    altura_cm DECIMAL(6,2),
    capacidad_peso_kg DECIMAL(8,2),
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_estante) REFERENCES estantes(id_estante),
    UNIQUE KEY unique_nivel_estante (id_estante, numero_nivel)
);

-- ========================================
-- 3. PRODUCTOS
-- ========================================

-- Tabla principal de productos
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    sku VARCHAR(50) NOT NULL UNIQUE,
    nombre_producto VARCHAR(200) NOT NULL,
    descripcion_corta VARCHAR(500),
    descripcion_detallada TEXT,
    id_marca INT,
    modelo VARCHAR(100),
    numero_parte VARCHAR(100),
    id_tipo_producto INT NOT NULL,
    id_unidad_medida INT NOT NULL,
    
    -- Especificaciones técnicas generales
    peso_kg DECIMAL(8,3),
    dimensiones_largo_cm DECIMAL(8,2),
    dimensiones_ancho_cm DECIMAL(8,2),
    dimensiones_alto_cm DECIMAL(8,2),
    material_principal VARCHAR(100),
    color VARCHAR(50),
    
    -- Información para sistemas contra incendios
    presion_trabajo_bar DECIMAL(6,2),
    presion_maxima_bar DECIMAL(6,2),
    temperatura_min_celsius DECIMAL(6,2),
    temperatura_max_celsius DECIMAL(6,2),
    temperatura_activacion_celsius DECIMAL(6,2),
    factor_k DECIMAL(6,3), -- Para rociadores
    conexion_entrada VARCHAR(50),
    conexion_salida VARCHAR(50),
    
    -- Certificaciones y normativas
    certificacion_ul VARCHAR(50),
    certificacion_fm VARCHAR(50),
    certificacion_nfpa VARCHAR(100),
    otras_certificaciones TEXT,
    
    -- Control de inventario
    stock_actual INT DEFAULT 0,
    stock_minimo INT DEFAULT 0,
    stock_maximo INT DEFAULT 0,
    punto_reorden INT DEFAULT 0,
    lead_time_dias INT DEFAULT 0,
    
    -- Información comercial
    costo_promedio DECIMAL(15,4) DEFAULT 0,
    precio_venta DECIMAL(15,2) DEFAULT 0,
    margen_ganancia DECIMAL(5,2) DEFAULT 0,
    
    -- Control de calidad y almacenamiento
    requiere_refrigeracion BOOLEAN DEFAULT FALSE,
    vida_util_meses INT,
    condiciones_almacenamiento TEXT,
    manejo_especial TEXT,
    
    -- Control del sistema
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT,
    usuario_modificacion INT,
    
    FOREIGN KEY (id_marca) REFERENCES marcas(id_marca),
    FOREIGN KEY (id_tipo_producto) REFERENCES tipos_producto(id_tipo_producto),
    FOREIGN KEY (id_unidad_medida) REFERENCES unidades_medida(id_unidad),
    
    INDEX idx_sku (sku),
    INDEX idx_nombre (nombre_producto),
    INDEX idx_marca (id_marca),
    INDEX idx_tipo (id_tipo_producto)
);

-- Proveedores por producto
CREATE TABLE IF NOT EXISTS producto_proveedores (
    id_producto_proveedor INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT NOT NULL,
    id_proveedor INT NOT NULL,
    es_principal BOOLEAN DEFAULT FALSE,
    codigo_proveedor_producto VARCHAR(100),
    costo_actual DECIMAL(15,4),
    descuento_producto DECIMAL(5,2) DEFAULT 0,
    tiempo_entrega_dias INT DEFAULT 0,
    cantidad_minima_orden INT DEFAULT 1,
    activo BOOLEAN DEFAULT TRUE,
    fecha_vigencia_desde DATE,
    fecha_vigencia_hasta DATE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    UNIQUE KEY unique_prod_prov (id_producto, id_proveedor)
);

-- ========================================
-- 4. UBICACIONES DE PRODUCTOS
-- ========================================

-- Ubicaciones específicas de productos
CREATE TABLE IF NOT EXISTS producto_ubicaciones (
    id_ubicacion INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT NOT NULL,
    id_nivel INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 0,
    cantidad_reservada INT DEFAULT 0,
    posicion_especifica VARCHAR(20), -- Para ubicación más detallada
    fecha_ultima_conteo DATE,
    observaciones TEXT,
    activo BOOLEAN DEFAULT TRUE,
    
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_nivel) REFERENCES niveles(id_nivel),
    
    INDEX idx_producto_ubicacion (id_producto),
    INDEX idx_nivel_ubicacion (id_nivel)
);

-- ========================================
-- 5. MOVIMIENTOS DE INVENTARIO (SIMPLIFICADO)
-- ========================================

-- Tipos de movimientos
CREATE TABLE IF NOT EXISTS tipos_movimiento (
    id_tipo_movimiento INT PRIMARY KEY AUTO_INCREMENT,
    codigo_tipo VARCHAR(10) NOT NULL UNIQUE, -- ENT, SAL, AJU, TRA, DEV
    nombre_tipo VARCHAR(50) NOT NULL,
    afecta_stock ENUM('AUMENTA', 'DISMINUYE', 'NO_AFECTA') NOT NULL,
    requiere_autorizacion BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE
);

-- Documentos que respaldan movimientos
CREATE TABLE IF NOT EXISTS documentos_movimiento (
    id_documento INT PRIMARY KEY AUTO_INCREMENT,
    tipo_documento VARCHAR(20) NOT NULL, -- FACTURA, REMISION, ORDEN, etc.
    numero_documento VARCHAR(50) NOT NULL,
    fecha_documento DATE NOT NULL,
    id_proveedor INT,
    total_documento DECIMAL(15,2),
    observaciones TEXT,
    ruta_archivo VARCHAR(500),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    UNIQUE KEY unique_tipo_numero_doc (tipo_documento, numero_documento)
);

-- Movimientos de inventario (cabecera)
CREATE TABLE IF NOT EXISTS movimientos_inventario (
    id_movimiento INT PRIMARY KEY AUTO_INCREMENT,
    id_tipo_movimiento INT NOT NULL,
    numero_movimiento VARCHAR(50) NOT NULL,
    fecha_movimiento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_documento INT,
    id_usuario INT NOT NULL,
    motivo TEXT,
    observaciones TEXT,
    autorizado_por INT,
    fecha_autorizacion DATETIME,
    estado ENUM('PENDIENTE', 'AUTORIZADO', 'PROCESADO', 'CANCELADO') DEFAULT 'PENDIENTE',
    
    FOREIGN KEY (id_tipo_movimiento) REFERENCES tipos_movimiento(id_tipo_movimiento),
    FOREIGN KEY (id_documento) REFERENCES documentos_movimiento(id_documento),
    
    INDEX idx_fecha_movimiento (fecha_movimiento),
    INDEX idx_numero_movimiento (numero_movimiento),
    INDEX idx_estado (estado)
);

-- Detalle de movimientos de inventario (sin lotes ni series)
CREATE TABLE IF NOT EXISTS movimientos_detalle (
    id_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_movimiento INT NOT NULL,
    id_producto INT NOT NULL,
    id_ubicacion_origen INT,
    id_ubicacion_destino INT,
    cantidad INT NOT NULL,
    costo_unitario DECIMAL(15,4) DEFAULT 0,
    costo_total DECIMAL(15,2) DEFAULT 0,
    observaciones TEXT,
    
    FOREIGN KEY (id_movimiento) REFERENCES movimientos_inventario(id_movimiento),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_ubicacion_origen) REFERENCES producto_ubicaciones(id_ubicacion),
    FOREIGN KEY (id_ubicacion_destino) REFERENCES producto_ubicaciones(id_ubicacion)
);

-- ========================================
-- 6. CONTROL DE LOTES Y SERIES
-- ========================================

-- Lotes de productos
CREATE TABLE IF NOT EXISTS lotes (
    id_lote INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT NOT NULL,
    numero_lote VARCHAR(50) NOT NULL,
    fecha_fabricacion DATE,
    fecha_vencimiento DATE,
    id_proveedor INT,
    cantidad_inicial INT NOT NULL,
    cantidad_actual INT NOT NULL,
    costo_promedio DECIMAL(15,4),
    certificado_calidad VARCHAR(500), -- Ruta del archivo
    observaciones TEXT,
    estado ENUM('ACTIVO', 'VENCIDO', 'CUARENTENA', 'AGOTADO') DEFAULT 'ACTIVO',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    UNIQUE KEY unique_producto_lote (id_producto, numero_lote)
);

-- Control de números de serie (para productos individuales)
CREATE TABLE IF NOT EXISTS numeros_serie (
    id_serie INT PRIMARY KEY AUTO_INCREMENT,
    id_producto INT NOT NULL,
    numero_serie VARCHAR(100) NOT NULL,
    id_lote INT,
    fecha_ingreso DATE NOT NULL,
    id_ubicacion INT,
    estado ENUM('DISPONIBLE', 'RESERVADO', 'VENDIDO', 'DEFECTUOSO', 'EN_REPARACION') DEFAULT 'DISPONIBLE',
    cliente_asignado VARCHAR(200),
    fecha_venta DATE,
    observaciones TEXT,
    
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_lote) REFERENCES lotes(id_lote),
    FOREIGN KEY (id_ubicacion) REFERENCES producto_ubicaciones(id_ubicacion),
    UNIQUE KEY unique_producto_serie (id_producto, numero_serie)
);

-- ========================================
-- 7. GESTIÓN DE OBRAS Y PROYECTOS
-- ========================================

-- Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    codigo_cliente VARCHAR(20) NOT NULL UNIQUE,
    nombre_cliente VARCHAR(200) NOT NULL,
    razon_social VARCHAR(200),
    rfc VARCHAR(20),
    direccion TEXT,
    ciudad VARCHAR(100),
    estado VARCHAR(50),
    codigo_postal VARCHAR(10),
    pais VARCHAR(50) DEFAULT 'México',
    telefono VARCHAR(20),
    email VARCHAR(100),
    contacto_principal VARCHAR(100),
    tipo_cliente ENUM('GOBIERNO', 'PRIVADO', 'CONSTRUCTORA', 'DISTRIBUIDOR') NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Obras/Proyectos
CREATE TABLE IF NOT EXISTS obras (
    id_obra INT PRIMARY KEY AUTO_INCREMENT,
    codigo_obra VARCHAR(50) NOT NULL UNIQUE,
    nombre_obra VARCHAR(200) NOT NULL,
    descripcion TEXT,
    id_cliente INT NOT NULL,
    direccion_obra TEXT,
    ciudad VARCHAR(100),
    codigo_postal VARCHAR(10),
    
    -- Responsables
    supervisor_obra VARCHAR(100),
    contacto_obra VARCHAR(100),
    telefono_obra VARCHAR(20),
    
    -- Fechas del proyecto
    fecha_inicio_programada DATE,
    fecha_fin_programada DATE,
    fecha_inicio_real DATE,
    fecha_fin_real DATE,
    
    -- Control financiero
    valor_contrato DECIMAL(15,2),
    moneda VARCHAR(10) DEFAULT 'MXN',
    
    -- Control de inventario
    requiere_devolucion_sobrantes BOOLEAN DEFAULT TRUE,
    dias_limite_devolucion INT DEFAULT 30,
    porcentaje_merma_permitida DECIMAL(5,2) DEFAULT 5.00,
    
    -- Estado y control
    estado ENUM('PLANIFICACION', 'EN_EJECUCION', 'SUSPENDIDA', 'FINALIZADA', 'CANCELADA') DEFAULT 'PLANIFICACION',
    prioridad ENUM('BAJA', 'MEDIA', 'ALTA', 'CRITICA') DEFAULT 'MEDIA',
    observaciones TEXT,
    activo BOOLEAN DEFAULT TRUE,
    
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT,
    usuario_modificacion INT,
    
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    
    INDEX idx_cliente_obra (id_cliente),
    INDEX idx_estado_obra (estado),
    INDEX idx_codigo_obra (codigo_obra)
);

-- Almacén único por obra
CREATE TABLE IF NOT EXISTS almacen_obra (
    id_almacen_obra INT PRIMARY KEY AUTO_INCREMENT,
    id_obra INT NOT NULL UNIQUE,
    nombre_almacen VARCHAR(100) NOT NULL,
    descripcion TEXT,
    direccion TEXT,
    responsable VARCHAR(100),
    telefono VARCHAR(20),
    
    -- Condiciones del almacén
    tiene_seguridad BOOLEAN DEFAULT FALSE,
    tiene_techo BOOLEAN DEFAULT TRUE,
    capacidad_m3 DECIMAL(10,2),
    observaciones TEXT,
    
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_obra) REFERENCES obras(id_obra),
    
    INDEX idx_obra_almacen (id_obra)
);

-- ========================================
-- 8. DESPACHOS DIRECTOS A OBRA
-- ========================================

-- Despachos a obras (sin solicitud previa)
CREATE TABLE IF NOT EXISTS despachos_obra (
    id_despacho INT PRIMARY KEY AUTO_INCREMENT,
    numero_despacho VARCHAR(50) NOT NULL UNIQUE,
    id_obra INT NOT NULL,
    fecha_despacho DATE NOT NULL,
    
    -- Transporte
    transportista VARCHAR(100),
    vehiculo VARCHAR(50),
    chofer VARCHAR(100),
    
    -- Entrega
    id_usuario_despacha INT NOT NULL,
    recibido_por VARCHAR(100),
    fecha_entrega DATE,
    hora_entrega TIME,
    
    -- Control
    requiere_devolucion BOOLEAN DEFAULT TRUE,
    fecha_limite_devolucion DATE,
    motivo_despacho TEXT, -- Razón del envío de material
    observaciones TEXT,
    
    estado ENUM('PREPARADO', 'EN_TRANSITO', 'ENTREGADO', 'DEVOLUCION_PARCIAL', 'DEVOLUCION_COMPLETA', 'CERRADO') DEFAULT 'PREPARADO',
    
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_obra) REFERENCES obras(id_obra),
    
    INDEX idx_obra_despacho (id_obra),
    INDEX idx_estado_despacho (estado),
    INDEX idx_fecha_limite_devolucion (fecha_limite_devolucion)
);

-- Detalle de despachos a obras
CREATE TABLE IF NOT EXISTS despachos_obra_detalle (
    id_despacho_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_despacho INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad_despachada INT NOT NULL,
    cantidad_utilizada INT DEFAULT 0,
    cantidad_devuelta INT DEFAULT 0,
    cantidad_perdida INT DEFAULT 0, -- Por daños, robos, etc.
    
    -- Trazabilidad
    id_lote INT,
    numeros_serie TEXT, -- Para productos con serie, separados por comas
    
    -- Costos
    costo_unitario DECIMAL(15,4),
    costo_total DECIMAL(15,2),
    
    -- Para herramientas y equipos
    es_herramienta BOOLEAN DEFAULT FALSE,
    requiere_devolucion_obligatoria BOOLEAN DEFAULT FALSE, -- Para herramientas costosas
    
    observaciones TEXT,
    
    FOREIGN KEY (id_despacho) REFERENCES despachos_obra(id_despacho),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_lote) REFERENCES lotes(id_lote),
    
    INDEX idx_despacho_producto (id_despacho, id_producto),
    INDEX idx_herramientas (es_herramienta, requiere_devolucion_obligatoria)
);

-- Devoluciones desde obras (igual que antes)
CREATE TABLE IF NOT EXISTS devoluciones_obra (
    id_devolucion INT PRIMARY KEY AUTO_INCREMENT,
    numero_devolucion VARCHAR(50) NOT NULL UNIQUE,
    id_obra INT NOT NULL,
    id_despacho INT NOT NULL,
    fecha_devolucion DATE NOT NULL,
    
    -- Transporte de devolución
    transportista VARCHAR(100),
    vehiculo VARCHAR(50),
    chofer VARCHAR(100),
    
    -- Recepción
    id_usuario_recibe INT NOT NULL,
    entregado_por VARCHAR(100),
    fecha_recepcion DATE,
    hora_recepcion TIME,
    
    -- Motivos de devolución
    motivo_devolucion ENUM('FIN_OBRA', 'SOBRANTE', 'CAMBIO_ESPECIFICACION', 'DEFECTUOSO', 'NO_UTILIZADO', 'DEVOLUCION_HERRAMIENTAS') NOT NULL,
    observaciones TEXT,
    
    estado ENUM('EN_TRANSITO', 'RECIBIDA', 'EN_REVISION', 'PROCESADA', 'RECHAZADA') DEFAULT 'EN_TRANSITO',
    
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_obra) REFERENCES obras(id_obra),
    FOREIGN KEY (id_despacho) REFERENCES despachos_obra(id_despacho),
    
    INDEX idx_obra_devolucion (id_obra),
    INDEX idx_despacho_devolucion (id_despacho),
    INDEX idx_estado_devolucion (estado)
);

-- Detalle de devoluciones desde obras (actualizado para herramientas)
CREATE TABLE IF NOT EXISTS devoluciones_obra_detalle (
    id_devolucion_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_devolucion INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad_devuelta INT NOT NULL,
    
    -- Estado del producto devuelto
    estado_producto ENUM('NUEVO', 'USADO_BUENO', 'USADO_REGULAR', 'DEFECTUOSO', 'NO_REUTILIZABLE') NOT NULL,
    requiere_limpieza BOOLEAN DEFAULT FALSE,
    requiere_reparacion BOOLEAN DEFAULT FALSE,
    requiere_calibracion BOOLEAN DEFAULT FALSE, -- Para herramientas de precisión
    
    -- Trazabilidad
    id_lote INT,
    numeros_serie TEXT,
    
    -- Ubicación de recepción
    id_ubicacion_recepcion INT,
    
    observaciones TEXT,
    
    FOREIGN KEY (id_devolucion) REFERENCES devoluciones_obra(id_devolucion),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_lote) REFERENCES lotes(id_lote),
    FOREIGN KEY (id_ubicacion_recepcion) REFERENCES producto_ubicaciones(id_ubicacion),
    
    INDEX idx_devolucion_producto (id_devolucion, id_producto)
);

-- ========================================
-- 9. INVENTARIO EN OBRA (SIMPLIFICADO)
-- ========================================

-- Inventario actual en cada obra (sin lotes)
CREATE TABLE IF NOT EXISTS inventario_obra (
    id_inventario_obra INT PRIMARY KEY AUTO_INCREMENT,
    id_obra INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad_actual INT NOT NULL DEFAULT 0,
    cantidad_utilizada_acumulada INT DEFAULT 0,
    cantidad_devuelta_acumulada INT DEFAULT 0,
    
    -- Control de costos
    costo_promedio DECIMAL(15,4),
    valor_inventario DECIMAL(15,2) GENERATED ALWAYS AS (cantidad_actual * costo_promedio) STORED,
    
    -- Trazabilidad
    fecha_ultimo_movimiento DATETIME,
    
    -- Para herramientas
    es_herramienta BOOLEAN DEFAULT FALSE,
    ubicacion_especifica VARCHAR(100), -- Ubicación dentro de la obra
    responsable_herramienta VARCHAR(100), -- Quién tiene la herramienta asignada
    
    observaciones TEXT,
    
    FOREIGN KEY (id_obra) REFERENCES obras(id_obra),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    
    UNIQUE KEY unique_obra_producto (id_obra, id_producto),
    INDEX idx_obra_producto (id_obra, id_producto),
    INDEX idx_herramientas_obra (id_obra, es_herramienta)
);

-- ========================================
-- 10. RESERVAS Y APARTADOS (ACTUALIZADO)
-- ========================================

-- Reservas de productos (actualizado para incluir obras)
CREATE TABLE IF NOT EXISTS reservas (
    id_reserva INT PRIMARY KEY AUTO_INCREMENT,
    numero_reserva VARCHAR(50) NOT NULL UNIQUE,
    id_producto INT NOT NULL,
    cantidad_reservada INT NOT NULL,
    id_ubicacion INT NOT NULL,
    
    -- Puede ser para cliente/obra específica o genérica
    id_cliente INT,
    id_obra INT,
    cliente_externo VARCHAR(200), -- Para clientes no registrados
    proyecto_externo VARCHAR(200), -- Para proyectos externos
    
    fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_vencimiento_reserva DATETIME,
    motivo_reserva TEXT,
    id_usuario INT NOT NULL,
    
    estado ENUM('ACTIVA', 'UTILIZADA', 'VENCIDA', 'CANCELADA') DEFAULT 'ACTIVA',
    observaciones TEXT,
    
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_ubicacion) REFERENCES producto_ubicaciones(id_ubicacion),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_obra) REFERENCES obras(id_obra),
    
    INDEX idx_fecha_vencimiento (fecha_vencimiento_reserva),
    INDEX idx_estado_reserva (estado),
    INDEX idx_obra_reserva (id_obra)
);

-- ========================================
-- 6. CONTEOS FÍSICOS Y AUDITORÍAS (ACTUALIZADO)
-- ========================================

-- Programación de conteos físicos
CREATE TABLE IF NOT EXISTS programacion_conteos (
    id_programacion INT PRIMARY KEY AUTO_INCREMENT,
    nombre_conteo VARCHAR(100) NOT NULL,
    fecha_programada DATE NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    
    -- Tipo y alcance del conteo
    tipo_conteo ENUM('COMPLETO', 'CICLICO', 'CATEGORIA', 'BODEGA', 'OBRA', 'ALMACEN_OBRA') NOT NULL,
    id_bodega INT,
    id_categoria INT,
    id_obra INT, -- Para conteos en obra
    
    id_usuario_responsable INT NOT NULL,
    estado ENUM('PROGRAMADO', 'EN_PROCESO', 'COMPLETADO', 'CANCELADO') DEFAULT 'PROGRAMADO',
    observaciones TEXT,
    
    FOREIGN KEY (id_bodega) REFERENCES bodegas(id_bodega),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_obra) REFERENCES obras(id_obra)
);

-- Conteos físicos realizados (actualizado para bodegas y sin lotes)
CREATE TABLE IF NOT EXISTS conteos_fisicos (
    id_conteo INT PRIMARY KEY AUTO_INCREMENT,
    id_programacion INT NOT NULL,
    id_producto INT NOT NULL,
    
    -- Ubicación: puede ser en almacén principal o en obra
    id_ubicacion INT, -- Para almacén principal
    id_obra INT, -- Para inventario en obra
    
    cantidad_sistema INT NOT NULL,
    cantidad_fisica INT NOT NULL,
    diferencia INT GENERATED ALWAYS AS (cantidad_fisica - cantidad_sistema) STORED,
    
    id_usuario_contador INT NOT NULL,
    fecha_conteo DATETIME DEFAULT CURRENT_TIMESTAMP,
    observaciones TEXT,
    
    ajuste_procesado BOOLEAN DEFAULT FALSE,
    id_movimiento_ajuste INT,
    
    FOREIGN KEY (id_programacion) REFERENCES programacion_conteos(id_programacion),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_ubicacion) REFERENCES producto_ubicaciones(id_ubicacion),
    FOREIGN KEY (id_obra) REFERENCES obras(id_obra),
    FOREIGN KEY (id_movimiento_ajuste) REFERENCES movimientos_inventario(id_movimiento)
);

-- ========================================
-- 9. ALERTAS Y NOTIFICACIONES (ACTUALIZADO)
-- ========================================

-- Configuración de alertas
CREATE TABLE IF NOT EXISTS configuracion_alertas (
    id_alerta INT PRIMARY KEY AUTO_INCREMENT,
    nombre_alerta VARCHAR(100) NOT NULL,
    tipo_alerta ENUM(
        'STOCK_MINIMO', 
        'VENCIMIENTO', 
        'SIN_MOVIMIENTO', 
        'CERTIFICACION_VENCIDA',
        'DEVOLUCION_PENDIENTE',
        'OBRA_SIN_ACTIVIDAD',
        'MATERIAL_VENCIDO_EN_OBRA',
        'DESPACHO_NO_ENTREGADO'
    ) NOT NULL,
    activa BOOLEAN DEFAULT TRUE,
    dias_anticipacion INT DEFAULT 0,
    usuarios_notificar TEXT, -- IDs separados por comas
    email_notificar TEXT, -- Emails separados por comas
    frecuencia_revision_horas INT DEFAULT 24,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Log de alertas generadas (actualizado para obras)
CREATE TABLE IF NOT EXISTS log_alertas (
    id_log_alerta INT PRIMARY KEY AUTO_INCREMENT,
    id_alerta INT NOT NULL,
    id_producto INT,
    id_obra INT, -- Para alertas relacionadas con obras
    id_despacho INT, -- Para alertas de despachos
    
    mensaje TEXT NOT NULL,
    nivel_prioridad ENUM('BAJA', 'MEDIA', 'ALTA', 'CRITICA') DEFAULT 'MEDIA',
    
    fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_visualizacion DATETIME,
    fecha_resolucion DATETIME,
    estado ENUM('PENDIENTE', 'VISTA', 'RESUELTA', 'IGNORADA') DEFAULT 'PENDIENTE',
    
    usuario_resolucion INT,
    observaciones_resolucion TEXT,
    
    FOREIGN KEY (id_alerta) REFERENCES configuracion_alertas(id_alerta),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    FOREIGN KEY (id_obra) REFERENCES obras(id_obra),
    FOREIGN KEY (id_despacho) REFERENCES despachos_obra(id_despacho)
);

-- ========================================
-- 10. USUARIOS Y PERMISOS
-- ========================================

-- Roles de usuario
CREATE TABLE IF NOT EXISTS roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

-- Usuarios del sistema
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    nombre_completo VARCHAR(200) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    ultimo_acceso DATETIME,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- Permisos por módulo
CREATE TABLE IF NOT EXISTS permisos (
    id_permiso INT PRIMARY KEY AUTO_INCREMENT,
    id_rol INT NOT NULL,
    modulo VARCHAR(50) NOT NULL, -- INVENTARIO, MOVIMIENTOS, REPORTES, etc.
    crear BOOLEAN DEFAULT FALSE,
    leer BOOLEAN DEFAULT FALSE,
    actualizar BOOLEAN DEFAULT FALSE,
    eliminar BOOLEAN DEFAULT FALSE,
    autorizar BOOLEAN DEFAULT FALSE,
    
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol),
    UNIQUE KEY unique_rol_modulo (id_rol, modulo)
);

-- ========================================
-- 11. CONFIGURACIÓN DEL SISTEMA
-- ========================================

-- Parámetros generales del sistema
CREATE TABLE IF NOT EXISTS configuracion_sistema (
    id_config INT PRIMARY KEY AUTO_INCREMENT,
    parametro VARCHAR(100) NOT NULL UNIQUE,
    valor TEXT,
    tipo_dato ENUM('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'DATE') DEFAULT 'STRING',
    descripcion TEXT,
    modificable BOOLEAN DEFAULT TRUE,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_modificacion INT
);

-- ========================================
-- ÍNDICES ADICIONALES PARA RENDIMIENTO (ACTUALIZADO)
-- ========================================

-- Índices para optimizar consultas frecuentes
CREATE INDEX idx_productos_stock ON productos(stock_actual, stock_minimo);
CREATE INDEX idx_movimientos_fecha_producto ON movimientos_detalle(id_producto, id_movimiento);
CREATE INDEX idx_ubicaciones_producto_cantidad ON producto_ubicaciones(id_producto, cantidad);
CREATE INDEX idx_alertas_pendientes ON log_alertas(estado, nivel_prioridad, fecha_generacion);

-- Índices específicos para gestión de obras (actualizados)
CREATE INDEX idx_obras_estado_fecha ON obras(estado, fecha_fin_programada);
CREATE INDEX idx_despachos_obra_pendientes ON despachos_obra(estado, fecha_limite_devolucion);
CREATE INDEX idx_devoluciones_obra_estado ON devoluciones_obra(estado, fecha_devolucion);
CREATE INDEX idx_inventario_obra_producto ON inventario_obra(id_obra, id_producto);
CREATE INDEX idx_despachos_detalle_producto ON despachos_obra_detalle(id_producto, cantidad_despachada);

-- Índices compuestos para reportes
CREATE INDEX idx_obra_despacho_fecha ON despachos_obra(id_obra, fecha_despacho);
CREATE INDEX idx_obra_producto_inventario ON inventario_obra(id_obra, id_producto, cantidad_actual);
CREATE INDEX idx_devolucion_fecha_estado ON devoluciones_obra(fecha_devolucion, estado);

-- Índices para bodegas (actualizados)
CREATE INDEX idx_bodega_pasillo ON pasillos(id_bodega, numero_pasillo);
CREATE INDEX idx_pasillo_estante ON estantes(id_pasillo, codigo_estante);
CREATE INDEX idx_estante_nivel ON niveles(id_estante, numero_nivel);

-- ========================================
-- DATOS INICIALES SIMPLIFICADOS
-- ========================================

-- Insertar tipos de movimiento básicos (actualizados para obras)
INSERT INTO tipos_movimiento (codigo_tipo, nombre_tipo, afecta_stock, requiere_autorizacion) VALUES
('ENT', 'Entrada por Compra', 'AUMENTA', FALSE),
('SAL', 'Salida por Venta', 'DISMINUYE', FALSE),
('AJU', 'Ajuste de Inventario', 'NO_AFECTA', TRUE),
('TRA', 'Transferencia', 'NO_AFECTA', FALSE),
('DEV', 'Devolución', 'AUMENTA', FALSE),
('MER', 'Merma', 'DISMINUYE', TRUE),
('DAÑ', 'Producto Dañado', 'DISMINUYE', TRUE),
('DSO', 'Despacho a Obra', 'DISMINUYE', FALSE),
('DVO', 'Devolución de Obra', 'AUMENTA', FALSE),
('USO', 'Utilizado en Obra', 'NO_AFECTA', FALSE),
('PER', 'Pérdida en Obra', 'DISMINUYE', TRUE);

-- Insertar unidades de medida básicas
INSERT INTO unidades_medida (codigo_unidad, nombre_unidad, descripcion) VALUES
('UN', 'Unidad', 'Unidad individual'),
('LT', 'Litro', 'Medida de volumen'),
('MT', 'Metro', 'Medida de longitud'),
('KG', 'Kilogramo', 'Medida de peso'),
('M2', 'Metro Cuadrado', 'Medida de superficie'),
('JGO', 'Juego', 'Conjunto de piezas'),
('PAR', 'Par', 'Conjunto de dos piezas'),
('CAJ', 'Caja', 'Embalaje múltiple'),
('ROL', 'Rollo', 'Producto enrollado');

-- Insertar categorías principales (actualizado para herramientas)
INSERT INTO categorias (codigo_categoria, nombre_categoria, descripcion) VALUES
('DET', 'Sistemas de Detección', 'Equipos para detección de incendios y alarmas'),
('EXT', 'Sistemas de Extinción', 'Equipos para extinción de incendios'),
('FIT', 'Fitting y Accesorios', 'Tuberías, válvulas y accesorios hidráulicos'),
('CON', 'Elementos de Construcción', 'Materiales eléctricos y elementos de construcción'),
('HER', 'Herramientas y Equipos', 'Herramientas de trabajo, equipos de seguridad y apoyo');

-- Insertar subcategorías para herramientas
INSERT INTO subcategorias (id_categoria, codigo_subcategoria, nombre_subcategoria, descripcion) VALUES
-- Para categoría HER (Herramientas y Equipos)
(5, 'ESC', 'Escaleras', 'Escaleras de diferentes tipos y tamaños'),
(5, 'CON', 'Conos y Señalización', 'Conos de tráfico, señalamientos y barreras'),
(5, 'PIZ', 'Pizarras y Comunicación', 'Pizarras, rotuladores y material de comunicación'),
(5, 'SEG', 'Equipo de Seguridad', 'Cascos, arneses, chalecos y equipo de protección'),
(5, 'MAN', 'Herramientas Manuales', 'Llaves, destornilladores, martillos, etc.'),
(5, 'ELE', 'Herramientas Eléctricas', 'Taladros, sierras, pulidoras, etc.'),
(5, 'MED', 'Instrumentos de Medición', 'Flexómetros, niveles, multímetros, etc.'),
(5, 'LIM', 'Equipo de Limpieza', 'Aspiradoras, traperos, productos de limpieza'),
(5, 'TRA', 'Equipo de Transporte', 'Carretillas, diablos, montacargas manuales'),
(5, 'ILU', 'Iluminación Temporal', 'Reflectores, lámparas portátiles, extensiones');

-- Insertar bodegas básicas del almacén (actualizado para herramientas)
INSERT INTO bodegas (codigo_bodega, nombre_bodega, descripcion) VALUES
('A', 'Sistemas de Detección', 'Bodega para equipos de detección de incendios'),
('B', 'Sistemas de Extinción', 'Bodega para equipos de extinción'),
('C', 'Fitting y Accesorios', 'Bodega para tuberías y accesorios'),
('D', 'Material Eléctrico', 'Bodega para elementos eléctricos'),
('E', 'Construcción General', 'Bodega para elementos de construcción'),
('F', 'Productos Especiales', 'Bodega para productos certificados especiales'),
('G', 'Control de Calidad', 'Bodega de cuarentena y control'),
('H', 'Devoluciones', 'Bodega para productos defectuosos y devoluciones'),
('I', 'Herramientas y Equipos', 'Bodega para herramientas de trabajo y equipos de apoyo');

-- Insertar roles básicos (actualizado para obras)
INSERT INTO roles (nombre_rol, descripcion) VALUES
('ADMINISTRADOR', 'Acceso completo al sistema'),
('JEFE_ALMACEN', 'Gestión completa de inventario'),
('OPERADOR_ALMACEN', 'Operaciones básicas de almacén'),
('SUPERVISOR_OBRA', 'Gestión de inventario en obras'),
('AUXILIAR_OBRA', 'Operaciones básicas en obra'),
('VENTAS', 'Consulta de inventario y reservas'),
('COMPRAS', 'Gestión de proveedores y compras'),
('AUDITOR', 'Solo lectura para auditorías');

-- Insertar configuraciones específicas para obras (simplificadas)
INSERT INTO configuracion_sistema (parametro, valor, tipo_dato, descripcion) VALUES
('DIAS_LIMITE_DEVOLUCION_DEFAULT', '30', 'INTEGER', 'Días límite por defecto para devolución de materiales de obra'),
('PORCENTAJE_MERMA_PERMITIDA_DEFAULT', '5.00', 'DECIMAL', 'Porcentaje de merma permitida por defecto en obras'),
('REQUIERE_AUTORIZACION_DESPACHO', 'FALSE', 'BOOLEAN', 'Indica si los despachos a obra requieren autorización'),
('ALERTA_DIAS_ANTES_LIMITE_DEVOLUCION', '7', 'INTEGER', 'Días antes del límite para alertar sobre devoluciones pendientes'),
('GENERAR_MOVIMIENTO_AUTO_DESPACHO', 'TRUE', 'BOOLEAN', 'Generar automáticamente movimiento de inventario al despachar'),
('PERMITIR_DEVOLUCION_PARCIAL', 'TRUE', 'BOOLEAN', 'Permitir devoluciones parciales de materiales'),
('CONTROL_HERRAMIENTAS_EN_OBRA', 'TRUE', 'BOOLEAN', 'Controlar herramientas asignadas en obra');

-- Insertar alertas específicas para obras (simplificadas)
INSERT INTO configuracion_alertas (nombre_alerta, tipo_alerta, dias_anticipacion, frecuencia_revision_horas) VALUES
('Devoluciones próximas a vencer', 'DEVOLUCION_PENDIENTE', 7, 24),
('Obras sin actividad', 'OBRA_SIN_ACTIVIDAD', 15, 48),
('Material vencido en obra', 'MATERIAL_VENCIDO_EN_OBRA', 0, 24),
('Despacho no entregado', 'DESPACHO_NO_ENTREGADO', 3, 12);

-- ========================================
-- FIN DE LA ESTRUCTURA SIMPLIFICADA
-- ========================================lotes_vencimiento ON lotes(fecha_vencimiento, estado);

-- ========================================
-- 13. VISTAS PARA REPORTES Y CONSULTAS FRECUENTES
-- ========================================

-- Vista consolidada de inventario total (almacén + obras) - sin lotes
CREATE VIEW vista_inventario_consolidado AS
SELECT 
    p.id_producto,
    p.sku,
    p.nombre_producto,
    p.stock_actual as stock_almacen,
    COALESCE(SUM(io.cantidad_actual), 0) as stock_obras,
    (p.stock_actual + COALESCE(SUM(io.cantidad_actual), 0)) as stock_total,
    p.stock_minimo,
    p.stock_maximo,
    p.costo_promedio,
    (p.stock_actual + COALESCE(SUM(io.cantidad_actual), 0)) * p.costo_promedio as valor_total
FROM productos p
LEFT JOIN inventario_obra io ON p.id_producto = io.id_producto
WHERE p.activo = TRUE
GROUP BY p.id_producto, p.sku, p.nombre_producto, p.stock_actual, p.stock_minimo, p.stock_maximo, p.costo_promedio;

-- Vista de obras activas con resumen de inventario - simplificada
CREATE VIEW vista_obras_inventario AS
SELECT 
    o.id_obra,
    o.codigo_obra,
    o.nombre_obra,
    o.estado,
    c.nombre_cliente,
    COUNT(DISTINCT io.id_producto) as productos_diferentes,
    SUM(io.cantidad_actual) as cantidad_total_productos,
    SUM(io.valor_inventario) as valor_total_inventario,
    o.fecha_inicio_real,
    o.fecha_fin_programada
FROM obras o
INNER JOIN clientes c ON o.id_cliente = c.id_cliente
LEFT JOIN inventario_obra io ON o.id_obra = io.id_obra
WHERE o.activo = TRUE
GROUP BY o.id_obra, o.codigo_obra, o.nombre_obra, o.estado, c.nombre_cliente, o.fecha_inicio_real, o.fecha_fin_programada;

-- Vista de devoluciones pendientes - simplificada
CREATE VIEW vista_devoluciones_pendientes AS
SELECT 
    d.id_despacho,
    d.numero_despacho,
    o.codigo_obra,
    o.nombre_obra,
    d.fecha_despacho,
    d.fecha_limite_devolucion,
    DATEDIFF(d.fecha_limite_devolucion, CURDATE()) as dias_para_limite,
    COUNT(dd.id_despacho_detalle) as productos_diferentes,
    SUM(dd.cantidad_despachada - dd.cantidad_devuelta) as cantidad_pendiente_devolucion,
    SUM((dd.cantidad_despachada - dd.cantidad_devuelta) * dd.costo_unitario) as valor_pendiente
FROM despachos_obra d
INNER JOIN obras o ON d.id_obra = o.id_obra
INNER JOIN despachos_obra_detalle dd ON d.id_despacho = dd.id_despacho
WHERE d.requiere_devolucion = TRUE 
  AND d.estado NOT IN ('DEVOLUCION_COMPLETA', 'CERRADO')
  AND (dd.cantidad_despachada - dd.cantidad_devuelta) > 0
GROUP BY d.id_despacho, d.numero_despacho, o.codigo_obra, o.nombre_obra, d.fecha_despacho, d.fecha_limite_devolucion;

-- Vista de productos con rotación ABC - simplificada
CREATE VIEW vista_productos_abc AS
SELECT 
    p.id_producto,
    p.sku,
    p.nombre_producto,
    p.stock_actual,
    p.costo_promedio,
    (p.stock_actual * p.costo_promedio) as valor_inventario,
    COALESCE(SUM(md.cantidad), 0) as movimientos_anuales,
    CASE 
        WHEN COALESCE(SUM(md.cantidad), 0) = 0 THEN 'SIN_MOVIMIENTO'
        ELSE 'POR_CLASIFICAR'
    END as clasificacion_abc
FROM productos p
LEFT JOIN movimientos_detalle md ON p.id_producto = md.id_producto
LEFT JOIN movimientos_inventario mi ON md.id_movimiento = mi.id_movimiento
LEFT JOIN tipos_movimiento tm ON mi.id_tipo_movimiento = tm.id_tipo_movimiento
WHERE p.activo = TRUE
  AND (mi.fecha_movimiento >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH) OR mi.fecha_movimiento IS NULL)
  AND (tm.codigo_tipo IN ('SAL', 'DSO') OR tm.codigo_tipo IS NULL)
GROUP BY p.id_producto, p.sku, p.nombre_producto, p.stock_actual, p.costo_promedio;

-- ========================================
-- 14. PROCEDIMIENTOS ALMACENADOS PRINCIPALES
-- ========================================

-- Procedimiento para despachar material a obra
DELIMITER //
CREATE PROCEDURE sp_despachar_material_obra(
    IN p_id_obra INT,
    IN p_id_almacen_obra INT,
    IN p_id_solicitud INT,
    IN p_fecha_despacho DATE,
    IN p_id_usuario_despacha INT,
    IN p_observaciones TEXT,
    OUT p_numero_despacho VARCHAR(50),
    OUT p_resultado VARCHAR(100)
)
BEGIN
    DECLARE v_id_despacho INT;
    DECLARE v_contador INT DEFAULT 1;
    
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_resultado = 'ERROR: No se pudo procesar el despacho';
        SET p_numero_despacho = NULL;
    END;
    
    START TRANSACTION;
    
    -- Generar número de despacho
    SELECT CONCAT('DSP-', YEAR(p_fecha_despacho), '-', LPAD(COUNT(*) + 1, 6, '0'))
    INTO p_numero_despacho
    FROM despachos_obra 
    WHERE YEAR(fecha_despacho) = YEAR(p_fecha_despacho);
    
    -- Crear el despacho
    INSERT INTO despachos_obra (
        numero_despacho, id_obra, id_almacen_obra, id_solicitud,
        fecha_despacho, id_usuario_despacha, observaciones, estado
    ) VALUES (
        p_numero_despacho, p_id_obra, p_id_almacen_obra, p_id_solicitud,
        p_fecha_despacho, p_id_usuario_despacha, p_observaciones, 'PREPARADO'
    );
    
    SET v_id_despacho = LAST_INSERT_ID();
    
    -- Si hay solicitud, copiar el detalle autorizado
    IF p_id_solicitud IS NOT NULL THEN
        INSERT INTO despachos_obra_detalle (
            id_despacho, id_producto, cantidad_despachada, costo_unitario, costo_total
        )
        SELECT 
            v_id_despacho,
            sod.id_producto,
            sod.cantidad_autorizada,
            p.costo_promedio,
            sod.cantidad_autorizada * p.costo_promedio
        FROM solicitudes_obra_detalle sod
        INNER JOIN productos p ON sod.id_producto = p.id_producto
        WHERE sod.id_solicitud = p_id_solicitud 
          AND sod.cantidad_autorizada > 0;
    END IF;
    
    COMMIT;
    SET p_resultado = 'DESPACHO_CREADO_EXITOSAMENTE';
    
END //
DELIMITER ;

-- Procedimiento para recibir devolución de obra
DELIMITER //
CREATE PROCEDURE sp_recibir_devolucion_obra(
    IN p_id_devolucion INT,
    IN p_fecha_recepcion DATE,
    IN p_id_usuario_recibe INT,
    OUT p_resultado VARCHAR(100)
)
BEGIN
    DECLARE v_id_producto INT;
    DECLARE v_cantidad_devuelta INT;
    DECLARE v_estado_producto VARCHAR(20);
    DECLARE v_id_ubicacion INT;
    DECLARE v_done INT DEFAULT FALSE;
    
    -- Cursor para procesar el detalle de la devolución
    DECLARE cur_devolucion CURSOR FOR 
        SELECT id_producto, cantidad_devuelta, estado_producto, id_ubicacion_recepcion
        FROM devoluciones_obra_detalle 
        WHERE id_devolucion = p_id_devolucion;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SET p_resultado = 'ERROR: No se pudo procesar la devolución';
    END;
    
    START TRANSACTION;
    
    -- Actualizar el estado de la devolución
    UPDATE devoluciones_obra 
    SET estado = 'PROCESADA', 
        fecha_recepcion = p_fecha_recepcion,
        id_usuario_recibe = p_id_usuario_recibe
    WHERE id_devolucion = p_id_devolucion;
    
    -- Procesar cada producto devuelto
    OPEN cur_devolucion;
    
    read_loop: LOOP
        FETCH cur_devolucion INTO v_id_producto, v_cantidad_devuelta, v_estado_producto, v_id_ubicacion;
        
        IF v_done THEN
            LEAVE read_loop;
        END IF;
        
        -- Si el producto está en buen estado, regresarlo al inventario
        IF v_estado_producto IN ('NUEVO', 'USADO_BUENO') THEN
            
            -- Actualizar stock en ubicación
            UPDATE producto_ubicaciones 
            SET cantidad = cantidad + v_cantidad_devuelta
            WHERE id_ubicacion = v_id_ubicacion;
            
            -- Actualizar stock general del producto
            UPDATE productos 
            SET stock_actual = stock_actual + v_cantidad_devuelta
            WHERE id_producto = v_id_producto;
            
        END IF;
        
    END LOOP;
    
    CLOSE cur_devolucion;
    
    COMMIT;
    SET p_resultado = 'DEVOLUCION_PROCESADA_EXITOSAMENTE';
    
END //
DELIMITER ;

-- ========================================
-- 15. TRIGGERS PARA MANTENER INTEGRIDAD
-- ========================================

-- Trigger para actualizar inventario en obra después de despacho
DELIMITER //
CREATE TRIGGER tr_after_despacho_detail_insert
AFTER INSERT ON despachos_obra_detalle
FOR EACH ROW
BEGIN
    -- Obtener el id_obra del despacho
    SET @v_id_obra = (SELECT id_obra FROM despachos_obra WHERE id_despacho = NEW.id_despacho);
    SET @v_id_almacen_obra = (SELECT id_almacen_obra FROM despachos_obra WHERE id_despacho = NEW.id_despacho);
    
    -- Actualizar o insertar en inventario_obra
    INSERT INTO inventario_obra (
        id_obra, id_almacen_obra, id_producto, cantidad_actual, 
        costo_promedio, fecha_ultimo_movimiento
    ) VALUES (
        @v_id_obra, @v_id_almacen_obra, NEW.id_producto, NEW.cantidad_despachada,
        NEW.costo_unitario, NOW()
    )
    ON DUPLICATE KEY UPDATE
        cantidad_actual = cantidad_actual + NEW.cantidad_despachada,
        costo_promedio = ((cantidad_actual * costo_promedio) + (NEW.cantidad_despachada * NEW.costo_unitario)) / (cantidad_actual + NEW.cantidad_despachada),
        fecha_ultimo_movimiento = NOW();
        
    -- Actualizar stock en almacén principal
    UPDATE productos 
    SET stock_actual = stock_actual - NEW.cantidad_despachada
    WHERE id_producto = NEW.id_producto;
    
END //
DELIMITER ;

-- Trigger para controlar stock negativo
DELIMITER //
CREATE TRIGGER tr_before_producto_update_stock
BEFORE UPDATE ON productos
FOR EACH ROW
BEGIN
    IF NEW.stock_actual < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El stock no puede ser negativo';
    END IF;
END //
DELIMITER ;

-- ========================================
-- 16. FUNCIONES ÚTILES
-- ========================================

-- Función para calcular días en obra de un material
DELIMITER //
CREATE FUNCTION fn_dias_material_en_obra(p_id_despacho INT, p_id_producto INT)
RETURNS INT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_fecha_despacho DATE;
    DECLARE v_fecha_devolucion DATE;
    DECLARE v_dias INT DEFAULT 0;
    
    -- Obtener fecha de despacho
    SELECT fecha_despacho INTO v_fecha_despacho
    FROM despachos_obra 
    WHERE id_despacho = p_id_despacho;
    
    -- Buscar fecha de devolución más reciente
    SELECT MAX(do.fecha_devolucion) INTO v_fecha_devolucion
    FROM devoluciones_obra do
    INNER JOIN devoluciones_obra_detalle dod ON do.id_devolucion = dod.id_devolucion
    WHERE do.id_despacho = p_id_despacho 
      AND dod.id_producto = p_id_producto;
    
    -- Calcular días
    IF v_fecha_devolucion IS NOT NULL THEN
        SET v_dias = DATEDIFF(v_fecha_devolucion, v_fecha_despacho);
    ELSE
        SET v_dias = DATEDIFF(CURDATE(), v_fecha_despacho);
    END IF;
    
    RETURN v_dias;
END //
DELIMITER ;

-- Función para obtener el estado consolidado de una obra
DELIMITER //
CREATE FUNCTION fn_estado_inventario_obra(p_id_obra INT)
RETURNS VARCHAR(50)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_total_despachado DECIMAL(15,2) DEFAULT 0;
    DECLARE v_total_devuelto DECIMAL(15,2) DEFAULT 0;
    DECLARE v_total_pendiente DECIMAL(15,2) DEFAULT 0;
    DECLARE v_estado VARCHAR(50);
    
    -- Calcular totales
    SELECT 
        COALESCE(SUM(dod.cantidad_despachada * dod.costo_unitario), 0),
        COALESCE(SUM(dod.cantidad_devuelta * dod.costo_unitario), 0)
    INTO v_total_despachado, v_total_devuelto
    FROM despachos_obra do
    INNER JOIN despachos_obra_detalle dod ON do.id_despacho = dod.id_despacho
    WHERE do.id_obra = p_id_obra;
    
    SET v_total_pendiente = v_total_despachado - v_total_devuelto;
    
    -- Determinar estado
    IF v_total_despachado = 0 THEN
        SET v_estado = 'SIN_MATERIAL';
    ELSEIF v_total_pendiente = 0 THEN
        SET v_estado = 'MATERIAL_DEVUELTO';
    ELSEIF v_total_pendiente > 0 THEN
        SET v_estado = 'MATERIAL_PENDIENTE';
    ELSE
        SET v_estado = 'INCONSISTENCIA';
    END IF;
    
    RETURN v_estado;
END //
DELIMITER ;

-- ========================================
-- FIN DE LA ESTRUCTURA
-- ========================================