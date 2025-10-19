-- Tabla: direcciones_proveedor
-- Descripción: Almacena las diferentes direcciones de los proveedores

CREATE TABLE IF NOT EXISTS direcciones_proveedor (
    id_direccion INT AUTO_INCREMENT PRIMARY KEY,
    id_proveedor INT NOT NULL,
    tipo_direccion ENUM('FISCAL', 'COMERCIAL', 'ENTREGA', 'FACTURACION', 'OTRO') DEFAULT 'COMERCIAL',
    direccion TEXT NOT NULL,
    comuna VARCHAR(100) NULL,
    ciudad VARCHAR(100) NULL,
    region VARCHAR(100) NULL,
    codigo_postal VARCHAR(20) NULL,
    pais VARCHAR(100) DEFAULT 'Chile',
    es_principal BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE CASCADE,
    INDEX idx_proveedor (id_proveedor),
    INDEX idx_tipo_direccion (tipo_direccion),
    INDEX idx_es_principal (es_principal)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
