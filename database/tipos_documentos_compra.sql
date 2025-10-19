-- Tabla: tipos_documentos_compra
-- Descripción: Almacena los tipos de documentos de compra con soporte para DTE (Chile)

CREATE TABLE IF NOT EXISTS tipos_documentos_compra (
    id_tipo_documento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo_dte VARCHAR(10) NULL COMMENT 'Código DTE según normativa chilena (ej: 33, 34, 46, etc.)',
    descripcion TEXT NULL,
    requiere_folio BOOLEAN DEFAULT FALSE COMMENT 'Indica si el documento requiere folio',
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_nombre (nombre),
    UNIQUE KEY unique_codigo_dte (codigo_dte)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar tipos de documentos DTE más comunes en Chile
INSERT INTO tipos_documentos_compra (nombre, codigo_dte, descripcion, requiere_folio, activo) VALUES
('Factura Electrónica', '33', 'Factura electrónica de compra según normativa chilena', TRUE, TRUE),
('Factura Exenta Electrónica', '34', 'Factura electrónica exenta de IVA', TRUE, TRUE),
('Factura de Compra Electrónica', '46', 'Factura de compra electrónica', TRUE, TRUE),
('Guía de Despacho Electrónica', '52', 'Guía de despacho electrónica', TRUE, TRUE),
('Nota de Débito Electrónica', '56', 'Nota de débito electrónica', TRUE, TRUE),
('Nota de Crédito Electrónica', '61', 'Nota de crédito electrónica', TRUE, TRUE),
('Factura Electrónica de Exportación', '110', 'Factura electrónica de exportación', TRUE, TRUE),
('Nota de Débito de Exportación Electrónica', '111', 'Nota de débito de exportación electrónica', TRUE, TRUE),
('Nota de Crédito de Exportación Electrónica', '112', 'Nota de crédito de exportación electrónica', TRUE, TRUE);
