"""
Script para corregir los valores booleanos del estado inicial
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
        # Ver el estado actual
        print("Estado actual del campo es_estado_inicial y activo:")
        cursor.execute("SELECT id_estado, codigo_estado, nombre_estado, es_estado_inicial, activo FROM estados_orden_compra")
        estados = cursor.fetchall()
        for estado in estados:
            print(f"  ID: {estado[0]}, Código: {estado[1]}, Es Inicial: {estado[3]} (tipo: {type(estado[3])}), Activo: {estado[4]} (tipo: {type(estado[4])})")

        # Verificar la consulta que hace el backend
        print("\nBuscando con la consulta del backend (es_estado_inicial = 1 AND activo = 1):")
        cursor.execute("SELECT id_estado, codigo_estado, nombre_estado FROM estados_orden_compra WHERE es_estado_inicial = 1 AND activo = 1")
        resultado = cursor.fetchone()

        if resultado:
            print(f"✓ Encontrado: ID={resultado[0]}, Código={resultado[1]}, Nombre={resultado[2]}")
        else:
            print("✗ No se encontró ningún estado inicial activo")
            print("\nCorrigiendo...")

            # Asegurar que todos los valores sean correctos
            cursor.execute("""
                UPDATE estados_orden_compra
                SET es_estado_inicial = 1, activo = 1
                WHERE codigo_estado = 'Borrador' OR codigo_estado = 'BORRADOR' OR nombre_estado = 'Borrador'
            """)

            # Asegurar que otros estados no sean iniciales
            cursor.execute("""
                UPDATE estados_orden_compra
                SET es_estado_inicial = 0
                WHERE codigo_estado != 'Borrador' AND codigo_estado != 'BORRADOR' AND nombre_estado != 'Borrador'
            """)

            connection.commit()

            # Verificar de nuevo
            cursor.execute("SELECT id_estado, codigo_estado, nombre_estado FROM estados_orden_compra WHERE es_estado_inicial = 1 AND activo = 1")
            resultado = cursor.fetchone()

            if resultado:
                print(f"✓ Corregido: ID={resultado[0]}, Código={resultado[1]}, Nombre={resultado[2]}")
            else:
                print("✗ Aún no se encuentra el estado inicial")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    connection.close()
