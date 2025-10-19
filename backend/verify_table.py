"""
Script para verificar si la tabla estados_orden_compra existe
"""

import pymysql

connection = pymysql.connect(
    host='localhost',
    user='amoragau',
    password='dosenuno',
    database='erp-dael'
)

try:
    with connection.cursor() as cursor:
        # Verificar si la tabla existe
        cursor.execute("SHOW TABLES LIKE 'estados_orden_compra'")
        result = cursor.fetchone()

        if result:
            print("✓ La tabla estados_orden_compra existe")

            # Ver la estructura
            cursor.execute("DESCRIBE estados_orden_compra")
            columns = cursor.fetchall()
            print("\nEstructura de la tabla:")
            for col in columns:
                print(f"  {col}")

            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM estados_orden_compra")
            count = cursor.fetchone()[0]
            print(f"\n✓ Total de registros: {count}")

            # Ver estados con es_estado_inicial = 1
            cursor.execute("SELECT * FROM estados_orden_compra WHERE es_estado_inicial = 1")
            inicial = cursor.fetchall()
            print(f"\n✓ Estados iniciales encontrados: {len(inicial)}")
            for estado in inicial:
                print(f"  {estado}")

        else:
            print("✗ La tabla estados_orden_compra NO existe")
            print("\nCreando tabla...")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estados_orden_compra (
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
                    INDEX idx_codigo (codigo_estado),
                    INDEX idx_activo (activo)
                )
            """)
            connection.commit()
            print("✓ Tabla creada")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    connection.close()
