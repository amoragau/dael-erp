-- ========================================
-- ESTRUCTURA DE TABLAS PARA ÓRDENES DE COMPRA
-- Sistema ERP DAEL
-- ========================================

-- Tabla para estados de órdenes de compra
CREATE TABLE estados_orden_compra (
    id_estado INT AUTO_INCREMENT PRIMARY KEY,
    codigo_estado VARCHAR(20) NOT NULL UNIQUE,
    nombre_estado VARCHAR(50) NOT NULL,
    descripcion VARCHAR(200),
    es_estado_inicial BOOLEAN DEFAULT FALSE,
    es_estado_final BOOLEAN DEFAULT FALSE,
    permite_edicion BOOLEAN DEFAULT TRUE,
    permite_cancelacion BOOLEAN DEFAULT TRUE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_codigo_estado (codigo_estado),
    INDEX idx_activo (activo)
);

-- Tabla principal de órdenes de compra
CREATE TABLE ordenes_compra (
    id_orden_compra INT AUTO_INCREMENT PRIMARY KEY,
    numero_orden VARCHAR(50) NOT NULL UNIQUE,

    -- Referencias
    id_proveedor INT NOT NULL,
    id_usuario_solicitante INT NOT NULL,
    id_usuario_aprobador INT NULL,
    id_estado INT NOT NULL,

    -- Fechas
    fecha_orden DATE NOT NULL,
    fecha_requerida DATE NOT NULL,
    fecha_esperada_entrega DATE NULL,
    fecha_entrega_real DATE NULL,

    -- Totales
    subtotal DECIMAL(15,4) NOT NULL DEFAULT 0,
    impuestos DECIMAL(15,4) NOT NULL DEFAULT 0,
    descuentos DECIMAL(15,4) NOT NULL DEFAULT 0,
    total DECIMAL(15,4) NOT NULL DEFAULT 0,

    -- Información adicional
    observaciones TEXT NULL,
    terminos_pago VARCHAR(100) NULL,
    moneda VARCHAR(3) DEFAULT 'MXN',
    tipo_cambio DECIMAL(10,4) DEFAULT 1.0000,

    -- Dirección de entrega
    direccion_entrega TEXT NULL,
    contacto_entrega VARCHAR(100) NULL,
    telefono_contacto VARCHAR(20) NULL,

    -- Control
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    fecha_aprobacion TIMESTAMP NULL,
    fecha_cancelacion TIMESTAMP NULL,
    motivo_cancelacion VARCHAR(200) NULL,

    -- Índices
    INDEX idx_numero_orden (numero_orden),
    INDEX idx_proveedor (id_proveedor),
    INDEX idx_usuario_solicitante (id_usuario_solicitante),
    INDEX idx_estado (id_estado),
    INDEX idx_fecha_orden (fecha_orden),
    INDEX idx_fecha_requerida (fecha_requerida),
    INDEX idx_activo (activo),

    -- Claves foráneas
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor),
    FOREIGN KEY (id_usuario_solicitante) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_usuario_aprobador) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_estado) REFERENCES estados_orden_compra(id_estado)
);

-- Tabla de detalle de órdenes de compra
CREATE TABLE ordenes_compra_detalle (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_orden_compra INT NOT NULL,
    id_producto INT NOT NULL,

    -- Cantidades
    cantidad_solicitada DECIMAL(12,4) NOT NULL,
    cantidad_recibida DECIMAL(12,4) NOT NULL DEFAULT 0,
    cantidad_pendiente DECIMAL(12,4) NOT NULL DEFAULT 0,

    -- Precios
    precio_unitario DECIMAL(15,4) NOT NULL,
    descuento_porcentaje DECIMAL(5,2) NOT NULL DEFAULT 0,
    descuento_importe DECIMAL(15,4) NOT NULL DEFAULT 0,
    precio_neto DECIMAL(15,4) NOT NULL,
    importe_total DECIMAL(15,4) NOT NULL,

    -- Información adicional
    observaciones TEXT NULL,
    numero_linea INT NOT NULL,
    codigo_producto_proveedor VARCHAR(100) NULL,

    -- Fechas esperadas
    fecha_entrega_esperada DATE NULL,
    fecha_entrega_real DATE NULL,

    -- Control
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Índices
    INDEX idx_orden_compra (id_orden_compra),
    INDEX idx_producto (id_producto),
    INDEX idx_numero_linea (numero_linea),
    INDEX idx_activo (activo),

    -- Claves foráneas
    FOREIGN KEY (id_orden_compra) REFERENCES ordenes_compra(id_orden_compra) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla para recepciones de mercancía
CREATE TABLE recepciones_mercancia (
    id_recepcion INT AUTO_INCREMENT PRIMARY KEY,
    numero_recepcion VARCHAR(50) NOT NULL UNIQUE,
    id_orden_compra INT NOT NULL,
    id_usuario_receptor INT NOT NULL,

    -- Información de recepción
    fecha_recepcion DATE NOT NULL,
    numero_factura_proveedor VARCHAR(100) NULL,
    numero_remision VARCHAR(100) NULL,
    numero_guia VARCHAR(100) NULL,
    transportista VARCHAR(200) NULL,

    -- Estado de la recepción
    recepcion_completa BOOLEAN DEFAULT FALSE,
    observaciones TEXT NULL,

    -- Control
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Índices
    INDEX idx_numero_recepcion (numero_recepcion),
    INDEX idx_orden_compra (id_orden_compra),
    INDEX idx_usuario_receptor (id_usuario_receptor),
    INDEX idx_fecha_recepcion (fecha_recepcion),
    INDEX idx_activo (activo),

    -- Claves foráneas
    FOREIGN KEY (id_orden_compra) REFERENCES ordenes_compra(id_orden_compra),
    FOREIGN KEY (id_usuario_receptor) REFERENCES usuarios(id_usuario)
);

-- Tabla de detalle de recepciones de mercancía
CREATE TABLE recepciones_mercancia_detalle (
    id_detalle_recepcion INT AUTO_INCREMENT PRIMARY KEY,
    id_recepcion INT NOT NULL,
    id_detalle_orden INT NOT NULL,

    -- Cantidades
    cantidad_recibida DECIMAL(12,4) NOT NULL,
    cantidad_aceptada DECIMAL(12,4) NOT NULL,
    cantidad_rechazada DECIMAL(12,4) NOT NULL DEFAULT 0,

    -- Información de calidad
    observaciones_calidad TEXT NULL,
    motivo_rechazo VARCHAR(200) NULL,
    lote_proveedor VARCHAR(100) NULL,
    fecha_vencimiento DATE NULL,

    -- Ubicación en almacén
    ubicacion_almacen VARCHAR(100) NULL,

    -- Control
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Índices
    INDEX idx_recepcion (id_recepcion),
    INDEX idx_detalle_orden (id_detalle_orden),
    INDEX idx_lote_proveedor (lote_proveedor),
    INDEX idx_fecha_vencimiento (fecha_vencimiento),

    -- Claves foráneas
    FOREIGN KEY (id_recepcion) REFERENCES recepciones_mercancia(id_recepcion) ON DELETE CASCADE,
    FOREIGN KEY (id_detalle_orden) REFERENCES ordenes_compra_detalle(id_detalle)
);

-- ========================================
-- DATOS INICIALES PARA ESTADOS
-- ========================================

INSERT INTO estados_orden_compra (codigo_estado, nombre_estado, descripcion, es_estado_inicial, es_estado_final, permite_edicion, permite_cancelacion) VALUES
('BORRADOR', 'Borrador', 'Orden en proceso de creación', TRUE, FALSE, TRUE, TRUE),
('PENDIENTE', 'Pendiente Aprobación', 'Orden esperando aprobación', FALSE, FALSE, FALSE, TRUE),
('APROBADA', 'Aprobada', 'Orden aprobada y lista para enviar', FALSE, FALSE, FALSE, TRUE),
('ENVIADA', 'Enviada', 'Orden enviada al proveedor', FALSE, FALSE, FALSE, TRUE),
('PARCIAL', 'Recepción Parcial', 'Orden con entregas parciales', FALSE, FALSE, FALSE, FALSE),
('COMPLETADA', 'Completada', 'Orden totalmente recibida', FALSE, TRUE, FALSE, FALSE),
('CANCELADA', 'Cancelada', 'Orden cancelada', FALSE, TRUE, FALSE, FALSE);

-- ========================================
-- TRIGGERS PARA ACTUALIZACIÓN AUTOMÁTICA
-- ========================================

-- Trigger para actualizar cantidad pendiente en detalle de orden
DELIMITER //
CREATE TRIGGER tr_actualizar_cantidad_pendiente
    AFTER UPDATE ON ordenes_compra_detalle
    FOR EACH ROW
BEGIN
    UPDATE ordenes_compra_detalle
    SET cantidad_pendiente = cantidad_solicitada - cantidad_recibida
    WHERE id_detalle = NEW.id_detalle;
END//
DELIMITER ;

-- Trigger para actualizar totales de orden al modificar detalle
DELIMITER //
CREATE TRIGGER tr_actualizar_totales_orden
    AFTER INSERT ON ordenes_compra_detalle
    FOR EACH ROW
BEGIN
    UPDATE ordenes_compra
    SET subtotal = (
        SELECT COALESCE(SUM(importe_total), 0)
        FROM ordenes_compra_detalle
        WHERE id_orden_compra = NEW.id_orden_compra AND activo = TRUE
    ),
    total = subtotal + impuestos - descuentos
    WHERE id_orden_compra = NEW.id_orden_compra;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER tr_actualizar_totales_orden_update
    AFTER UPDATE ON ordenes_compra_detalle
    FOR EACH ROW
BEGIN
    UPDATE ordenes_compra
    SET subtotal = (
        SELECT COALESCE(SUM(importe_total), 0)
        FROM ordenes_compra_detalle
        WHERE id_orden_compra = NEW.id_orden_compra AND activo = TRUE
    ),
    total = subtotal + impuestos - descuentos
    WHERE id_orden_compra = NEW.id_orden_compra;
END//
DELIMITER ;

-- ========================================
-- VISTAS ÚTILES
-- ========================================

-- Vista resumen de órdenes de compra
CREATE VIEW vista_ordenes_compra_resumen AS
SELECT
    oc.id_orden_compra,
    oc.numero_orden,
    p.nombre_proveedor,
    p.codigo_proveedor,
    us.nombre_completo as solicitante,
    ua.nombre_completo as aprobador,
    eoc.nombre_estado,
    oc.fecha_orden,
    oc.fecha_requerida,
    oc.total,
    oc.moneda,
    COUNT(ocd.id_detalle) as total_lineas,
    SUM(CASE WHEN ocd.cantidad_pendiente > 0 THEN 1 ELSE 0 END) as lineas_pendientes,
    CASE
        WHEN SUM(ocd.cantidad_pendiente) = 0 THEN 'COMPLETA'
        WHEN SUM(ocd.cantidad_recibida) = 0 THEN 'PENDIENTE'
        ELSE 'PARCIAL'
    END as estado_recepcion
FROM ordenes_compra oc
INNER JOIN proveedores p ON oc.id_proveedor = p.id_proveedor
INNER JOIN usuarios us ON oc.id_usuario_solicitante = us.id_usuario
LEFT JOIN usuarios ua ON oc.id_usuario_aprobador = ua.id_usuario
INNER JOIN estados_orden_compra eoc ON oc.id_estado = eoc.id_estado
LEFT JOIN ordenes_compra_detalle ocd ON oc.id_orden_compra = ocd.id_orden_compra AND ocd.activo = TRUE
WHERE oc.activo = TRUE
GROUP BY oc.id_orden_compra;

-- Vista detalle de órdenes con información del producto
CREATE VIEW vista_ordenes_detalle_completo AS
SELECT
    ocd.id_detalle,
    oc.numero_orden,
    ocd.numero_linea,
    pr.sku,
    pr.nombre_producto as producto_nombre,
    pr.descripcion_corta as producto_descripcion,
    um.nombre_unidad,
    ocd.cantidad_solicitada,
    ocd.cantidad_recibida,
    ocd.cantidad_pendiente,
    ocd.precio_unitario,
    ocd.descuento_porcentaje,
    ocd.precio_neto,
    ocd.importe_total,
    ocd.fecha_entrega_esperada,
    ocd.codigo_producto_proveedor,
    p.nombre_proveedor
FROM ordenes_compra_detalle ocd
INNER JOIN ordenes_compra oc ON ocd.id_orden_compra = oc.id_orden_compra
INNER JOIN productos pr ON ocd.id_producto = pr.id_producto
INNER JOIN unidades_medida um ON pr.id_unidad_medida = um.id_unidad
INNER JOIN proveedores p ON oc.id_proveedor = p.id_proveedor
WHERE ocd.activo = TRUE AND oc.activo = TRUE;