-- Agregar campos ACTECO a la tabla proveedores
-- Los códigos de Actividad Económica (ACTECO) del SII Chile

USE `erp-dael`;

-- Agregar columnas ACTECO si no existen
SET @column_exists_1 = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'erp-dael'
    AND TABLE_NAME = 'proveedores'
    AND COLUMN_NAME = 'acteco_1'
);

SET @sql_1 = IF(
    @column_exists_1 = 0,
    'ALTER TABLE proveedores ADD COLUMN acteco_1 VARCHAR(10) NULL COMMENT "Código ACTECO principal" AFTER giro_comercial',
    'SELECT "La columna acteco_1 ya existe" AS mensaje'
);

PREPARE stmt_1 FROM @sql_1;
EXECUTE stmt_1;
DEALLOCATE PREPARE stmt_1;

-- ACTECO 2
SET @column_exists_2 = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'erp-dael'
    AND TABLE_NAME = 'proveedores'
    AND COLUMN_NAME = 'acteco_2'
);

SET @sql_2 = IF(
    @column_exists_2 = 0,
    'ALTER TABLE proveedores ADD COLUMN acteco_2 VARCHAR(10) NULL COMMENT "Código ACTECO secundario" AFTER acteco_1',
    'SELECT "La columna acteco_2 ya existe" AS mensaje'
);

PREPARE stmt_2 FROM @sql_2;
EXECUTE stmt_2;
DEALLOCATE PREPARE stmt_2;

-- ACTECO 3
SET @column_exists_3 = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'erp-dael'
    AND TABLE_NAME = 'proveedores'
    AND COLUMN_NAME = 'acteco_3'
);

SET @sql_3 = IF(
    @column_exists_3 = 0,
    'ALTER TABLE proveedores ADD COLUMN acteco_3 VARCHAR(10) NULL COMMENT "Código ACTECO terciario" AFTER acteco_2',
    'SELECT "La columna acteco_3 ya existe" AS mensaje'
);

PREPARE stmt_3 FROM @sql_3;
EXECUTE stmt_3;
DEALLOCATE PREPARE stmt_3;

-- ACTECO 4
SET @column_exists_4 = (
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'erp-dael'
    AND TABLE_NAME = 'proveedores'
    AND COLUMN_NAME = 'acteco_4'
);

SET @sql_4 = IF(
    @column_exists_4 = 0,
    'ALTER TABLE proveedores ADD COLUMN acteco_4 VARCHAR(10) NULL COMMENT "Código ACTECO cuaternario" AFTER acteco_3',
    'SELECT "La columna acteco_4 ya existe" AS mensaje'
);

PREPARE stmt_4 FROM @sql_4;
EXECUTE stmt_4;
DEALLOCATE PREPARE stmt_4;

SELECT 'Migración ACTECO completada exitosamente' AS resultado;
