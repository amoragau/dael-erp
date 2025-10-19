"""
Script para verificar los estados de orden de compra
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
        cursor.execute("SELECT * FROM estados_orden_compra")
        estados = cursor.fetchall()

        if estados:
            print(f"Se encontraron {len(estados)} estados:")
            for estado in estados:
                print(estado)
        else:
            print("No se encontraron estados")

except Exception as e:
    print(f"Error: {e}")
finally:
    connection.close()
