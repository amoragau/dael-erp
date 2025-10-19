-- Tabla: referencias_documento
-- Descripción: Almacena las referencias de los documentos tributarios (DTE Chile)
-- Las referencias permiten relacionar un documento con otros (ej: Nota de Crédito que referencia una Factura)

CREATE TABLE IF NOT EXISTS referencias_documento (
    id_referencia INT AUTO_INCREMENT PRIMARY KEY,
    id_documento INT NOT NULL,

    -- Información de la referencia
    numero_linea_ref INT NOT NULL COMMENT 'Número de línea de la referencia (1, 2, 3...)',
    tipo_documento_ref VARCHAR(10) NULL COMMENT 'Código del tipo de documento referenciado (33, 34, 52, etc.)',
    folio_ref VARCHAR(50) NULL COMMENT 'Folio del documento referenciado',
    fecha_ref DATE NULL COMMENT 'Fecha del documento referenciado',

    -- Códigos de referencia según normativa SII
    codigo_ref ENUM('1', '2', '3') NULL COMMENT '1=Anula, 2=Corrige texto, 3=Corrige montos',
    razon_ref TEXT NULL COMMENT 'Razón de la referencia',

    -- Campos adicionales
    indicador_global BOOLEAN DEFAULT FALSE COMMENT 'Indica si es una referencia global',
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (id_documento) REFERENCES documentos_compra(id_documento) ON DELETE CASCADE,
    INDEX idx_documento (id_documento),
    INDEX idx_folio_ref (folio_ref),
    INDEX idx_tipo_documento_ref (tipo_documento_ref),
    UNIQUE KEY unique_referencia (id_documento, numero_linea_ref)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
