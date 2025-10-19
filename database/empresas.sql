-- =============================================
-- Tabla: empresas
-- Descripción: Tabla para gestionar las empresas emisoras
-- Fecha: 2025-10-13
-- =============================================

CREATE TABLE IF NOT EXISTS empresas (
    id_empresa INT AUTO_INCREMENT PRIMARY KEY,
    rut_empresa VARCHAR(20) NOT NULL UNIQUE COMMENT 'RUT de la empresa',
    razon_social VARCHAR(200) NOT NULL COMMENT 'Razón social de la empresa',
    nombre_fantasia VARCHAR(200) COMMENT 'Nombre de fantasía',
    giro VARCHAR(200) COMMENT 'Giro o actividad económica',
    direccion VARCHAR(255) COMMENT 'Dirección fiscal',
    comuna VARCHAR(100) COMMENT 'Comuna',
    ciudad VARCHAR(100) COMMENT 'Ciudad',
    region VARCHAR(100) COMMENT 'Región',
    telefono VARCHAR(20) COMMENT 'Teléfono de contacto',
    email VARCHAR(100) COMMENT 'Email de contacto',
    sitio_web VARCHAR(200) COMMENT 'Sitio web',
    logo_url VARCHAR(500) COMMENT 'URL del logo de la empresa',
    activo BOOLEAN DEFAULT TRUE COMMENT 'Indica si la empresa está activa',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación del registro',
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de última modificación',
    usuario_creacion INT COMMENT 'ID del usuario que creó el registro',
    usuario_modificacion INT COMMENT 'ID del usuario que modificó el registro',

    INDEX idx_rut_empresa (rut_empresa),
    INDEX idx_razon_social (razon_social),
    INDEX idx_activo (activo),

    CONSTRAINT fk_empresa_usuario_creacion FOREIGN KEY (usuario_creacion)
        REFERENCES usuarios(id_usuario) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_empresa_usuario_modificacion FOREIGN KEY (usuario_modificacion)
        REFERENCES usuarios(id_usuario) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Catálogo de empresas emisoras para documentos';

-- =============================================
-- Agregar columna id_empresa a ordenes_compra
-- =============================================

ALTER TABLE ordenes_compra
ADD COLUMN id_empresa INT COMMENT 'Empresa emisora de la orden'
AFTER id_centro_costo;

ALTER TABLE ordenes_compra
ADD INDEX idx_empresa (id_empresa);

ALTER TABLE ordenes_compra
ADD CONSTRAINT fk_orden_compra_empresa
    FOREIGN KEY (id_empresa)
    REFERENCES empresas(id_empresa)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- =============================================
-- Datos iniciales (opcional)
-- =============================================

INSERT INTO empresas (rut_empresa, razon_social, nombre_fantasia, giro, direccion, comuna, ciudad, region, telefono, email, activo) VALUES
('76.123.456-7', 'Constructora DAEL S.A.', 'DAEL', 'Construcción y obras civiles', 'Av. Principal 1234', 'Santiago', 'Santiago', 'Región Metropolitana', '+56912345678', 'contacto@dael.cl', TRUE),
('77.234.567-8', 'Inversiones y Construcciones del Sur Ltda.', 'IC SUR', 'Construcción e inversiones', 'Calle Los Robles 456', 'Concepción', 'Concepción', 'Región del Biobío', '+56987654321', 'contacto@icsur.cl', TRUE);
