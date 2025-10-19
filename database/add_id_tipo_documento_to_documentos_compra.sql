-- Agregar columna id_tipo_documento a la tabla documentos_compra
-- Esta columna relaciona el documento con la tabla tipos_documentos_compra

USE `erp-dael`;

-- Verificar si la columna ya existe antes de agregarla
SET @column_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'erp-dael'
    AND TABLE_NAME = 'documentos_compra'
    AND COLUMN_NAME = 'id_tipo_documento'
);

-- Agregar la columna si no existe
SET @sql = IF(
    @column_exists = 0,
    'ALTER TABLE documentos_compra ADD COLUMN id_tipo_documento INT NULL AFTER id_orden_compra, ADD INDEX idx_id_tipo_documento (id_tipo_documento)',
    'SELECT "La columna id_tipo_documento ya existe" AS mensaje'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Agregar la foreign key si no existe
SET @fk_exists = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS
    WHERE TABLE_SCHEMA = 'erp-dael'
    AND TABLE_NAME = 'documentos_compra'
    AND CONSTRAINT_NAME = 'fk_documentos_compra_tipo_documento'
);

SET @sql_fk = IF(
    @fk_exists = 0 AND @column_exists = 0,
    'ALTER TABLE documentos_compra ADD CONSTRAINT fk_documentos_compra_tipo_documento FOREIGN KEY (id_tipo_documento) REFERENCES tipos_documentos_compra(id_tipo_documento)',
    'SELECT "La foreign key ya existe o la columna no se agregó" AS mensaje'
);

PREPARE stmt_fk FROM @sql_fk;
EXECUTE stmt_fk;
DEALLOCATE PREPARE stmt_fk;

-- Hacer la columna tipo_documento nullable (en caso de que sea NOT NULL)
ALTER TABLE documentos_compra MODIFY COLUMN tipo_documento ENUM('FACTURA', 'FACTURA_EXENTA', 'BOLETA', 'NOTA_CREDITO', 'NOTA_DEBITO', 'GUIA_DESPACHO', 'OTRO') NULL;

SELECT 'Migración completada exitosamente' AS resultado;
