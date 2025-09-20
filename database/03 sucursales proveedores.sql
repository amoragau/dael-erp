-- Agregado para el sistema de gestión de sucursales de proveedores

  CREATE TABLE sucursales_proveedor (
      id_sucursal INT AUTO_INCREMENT PRIMARY KEY,
      id_proveedor INT NOT NULL,
      codigo_sucursal VARCHAR(20) NOT NULL,
      nombre_sucursal VARCHAR(200) NOT NULL,
      direccion TEXT,
      ciudad VARCHAR(100),
      estado VARCHAR(50),
      codigo_postal VARCHAR(10),
      pais VARCHAR(50) DEFAULT 'Chile',
      telefono VARCHAR(20),
      email VARCHAR(100),
      contacto VARCHAR(100),
      telefono_contacto VARCHAR(20),
      email_contacto VARCHAR(100),
      es_sucursal_principal BOOLEAN DEFAULT FALSE,
      activo BOOLEAN DEFAULT TRUE,
      fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

      -- Clave foránea hacia la tabla proveedores
      CONSTRAINT fk_sucursal_proveedor FOREIGN KEY (id_proveedor)
          REFERENCES proveedores(id_proveedor) ON DELETE CASCADE,

      -- Índice único para asegurar que el código de sucursal sea único por proveedor
      CONSTRAINT uq_proveedor_codigo_sucursal UNIQUE (id_proveedor, codigo_sucursal),

      -- Índices para optimizar consultas
      INDEX idx_sucursal_proveedor (id_proveedor),
      INDEX idx_sucursal_activo (activo),
      INDEX idx_sucursal_principal (es_sucursal_principal)
  );

  -- Comentarios de documentación
  COMMENT ON TABLE sucursales_proveedor IS 'Tabla de sucursales de proveedores';
  COMMENT ON COLUMN sucursales_proveedor.id_sucursal IS 'ID único de la sucursal';
  COMMENT ON COLUMN sucursales_proveedor.id_proveedor IS 'ID del proveedor al que pertenece la sucursal';
  COMMENT ON COLUMN sucursales_proveedor.codigo_sucursal IS 'Código único de la sucursal dentro del proveedor';
  COMMENT ON COLUMN sucursales_proveedor.es_sucursal_principal IS 'Indica si es la sucursal principal del proveedor';
  COMMENT ON COLUMN sucursales_proveedor.activo IS 'Estado activo/inactivo de la sucursal';