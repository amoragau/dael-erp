"""
Script para asegurar que hay un estado inicial configurado correctamente
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
        # Ver todos los estados actuales
        cursor.execute("SELECT id_estado, codigo_estado, nombre_estado, es_estado_inicial, activo FROM estados_orden_compra")
        estados = cursor.fetchall()

        print("Estados actuales:")
        for estado in estados:
            print(f"  ID: {estado[0]}, Código: {estado[1]}, Nombre: {estado[2]}, Es Inicial: {estado[3]}, Activo: {estado[4]}")

        # Verificar si hay un estado inicial activo
        cursor.execute("SELECT COUNT(*) FROM estados_orden_compra WHERE es_estado_inicial = 1 AND activo = 1")
        count = cursor.fetchone()[0]

        print(f"\nEstados iniciales activos encontrados: {count}")

        if count == 0:
            print("\n⚠ No hay estado inicial activo. Actualizando...")

            # Primero, asegurarse de que todos tengan es_estado_inicial = 0
            cursor.execute("UPDATE estados_orden_compra SET es_estado_inicial = 0")

            # Luego, marcar CREADA como estado inicial
            cursor.execute("UPDATE estados_orden_compra SET es_estado_inicial = 1, activo = 1 WHERE codigo_estado = 'CREADA'")

            connection.commit()

            # Verificar de nuevo
            cursor.execute("SELECT id_estado, codigo_estado, nombre_estado, es_estado_inicial, activo FROM estados_orden_compra WHERE es_estado_inicial = 1")
            estado_inicial = cursor.fetchone()

            if estado_inicial:
                print(f"✓ Estado inicial configurado: ID={estado_inicial[0]}, Código={estado_inicial[1]}, Nombre={estado_inicial[2]}")
            else:
                print("✗ No se pudo configurar el estado inicial")
        else:
            cursor.execute("SELECT id_estado, codigo_estado, nombre_estado FROM estados_orden_compra WHERE es_estado_inicial = 1 AND activo = 1")
            estado_inicial = cursor.fetchone()
            print(f"✓ Estado inicial ya configurado: ID={estado_inicial[0]}, Código={estado_inicial[1]}, Nombre={estado_inicial[2]}")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    connection.close()
