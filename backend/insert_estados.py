"""
Script para insertar los estados iniciales de orden de compra
Ejecutar con: python insert_estados.py
"""

import pymysql

# Conectar a la base de datos
connection = pymysql.connect(
    host='localhost',
    user='amoragau',
    password='dosenuno',
    database='erp-dael'
)

try:
    with connection.cursor() as cursor:
        # Verificar si ya existen estados
        cursor.execute("SELECT COUNT(*) FROM estados_orden_compra WHERE es_estado_inicial = 1")
        count = cursor.fetchone()[0]

        if count == 0:
            print("Insertando estados de orden de compra...")

            # Insertar estados
            sql = """
            INSERT INTO estados_orden_compra (codigo_estado, nombre_estado, descripcion, es_estado_inicial, es_estado_final, permite_edicion, permite_cancelacion, activo)
            VALUES
                ('CREADA', 'Creada', 'Orden de compra creada', 1, 0, 1, 1, 1),
                ('APROBADA', 'Aprobada', 'Orden de compra aprobada', 0, 0, 0, 1, 1),
                ('ENVIADA', 'Enviada', 'Orden de compra enviada al proveedor', 0, 0, 0, 1, 1),
                ('RECIBIDA', 'Recibida', 'Orden de compra recibida', 0, 0, 0, 0, 1),
                ('CERRADA', 'Cerrada', 'Orden de compra cerrada', 0, 1, 0, 0, 1),
                ('CANCELADA', 'Cancelada', 'Orden de compra cancelada', 0, 1, 0, 0, 1)
            """
            cursor.execute(sql)
            connection.commit()
            print("✓ Estados de orden de compra creados exitosamente")
        else:
            print("✓ Ya existe un estado inicial configurado")

except Exception as e:
    print(f"✗ Error: {e}")
    connection.rollback()
finally:
    connection.close()
