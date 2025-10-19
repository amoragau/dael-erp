-- =============================================
-- Tabla: centros_costo
-- Descripción: Tabla para gestionar los centros de costo
-- Fecha: 2025-10-13
-- =============================================

CREATE TABLE IF NOT EXISTS centros_costo (
    id_centro_costo INT AUTO_INCREMENT PRIMARY KEY,
    codigo_centro_costo VARCHAR(20) NOT NULL UNIQUE COMMENT 'Código único del centro de costo',
    nombre_centro_costo VARCHAR(100) NOT NULL COMMENT 'Nombre del centro de costo',
    descripcion TEXT COMMENT 'Descripción detallada del centro de costo',
    id_responsable INT COMMENT 'ID del usuario responsable del centro de costo',
    presupuesto_anual DECIMAL(15,2) DEFAULT 0 COMMENT 'Presupuesto anual asignado',
    activo BOOLEAN DEFAULT TRUE COMMENT 'Indica si el centro de costo está activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación del registro',
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de última modificación',
    usuario_creacion INT COMMENT 'ID del usuario que creó el registro',
    usuario_modificacion INT COMMENT 'ID del usuario que modificó el registro',

    INDEX idx_codigo_centro (codigo_centro_costo),
    INDEX idx_nombre_centro (nombre_centro_costo),
    INDEX idx_activo (activo),
    INDEX idx_responsable (id_responsable),

    CONSTRAINT fk_centro_costo_responsable FOREIGN KEY (id_responsable)
        REFERENCES usuarios(id_usuario) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_centro_costo_usuario_creacion FOREIGN KEY (usuario_creacion)
        REFERENCES usuarios(id_usuario) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_centro_costo_usuario_modificacion FOREIGN KEY (usuario_modificacion)
        REFERENCES usuarios(id_usuario) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Catálogo de centros de costo para asignación de gastos';

-- =============================================
-- Agregar columna id_centro_costo a ordenes_compra
-- =============================================

ALTER TABLE ordenes_compra
ADD COLUMN id_centro_costo INT NOT NULL COMMENT 'Centro de costo asociado a la orden'
AFTER id_usuario_solicitante;

ALTER TABLE ordenes_compra
ADD INDEX idx_centro_costo (id_centro_costo);

ALTER TABLE ordenes_compra
ADD CONSTRAINT fk_orden_compra_centro_costo
    FOREIGN KEY (id_centro_costo)
    REFERENCES centros_costo(id_centro_costo)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- =============================================
-- Datos iniciales (opcional)
-- =============================================

INSERT INTO centros_costo (codigo_centro_costo, nombre_centro_costo, descripcion, activo) VALUES
('CC-001', 'Administración', 'Centro de costo para gastos administrativos generales', TRUE),
('CC-002', 'Ventas', 'Centro de costo para el departamento de ventas', TRUE),
('CC-003', 'Producción', 'Centro de costo para el área de producción', TRUE),
('CC-004', 'Logística', 'Centro de costo para operaciones logísticas', TRUE),
('CC-005', 'TI', 'Centro de costo para tecnología de la información', TRUE);
