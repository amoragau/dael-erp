# debug.py
# Coloca este archivo en backend/app/ junto a main.py y database.py
# Ejecuta: python debug.py

import os
import sys

print("🔍 DIAGNÓSTICO DETALLADO")
print("=" * 50)

# 1. Verificar carpeta actual
current_dir = os.getcwd()
print(f"📁 Carpeta actual: {current_dir}")
print()

# 2. Verificar carpeta del script
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"📁 Carpeta del script: {script_dir}")
print()

# 3. Listar archivos en la carpeta actual
print("📂 Archivos en la carpeta actual:")
files = os.listdir('.')
for file in sorted(files):
    if os.path.isfile(file):
        size = os.path.getsize(file)
        print(f"   📄 {file} ({size} bytes)")
    else:
        print(f"   📁 {file}/")
print()

# 4. Verificar específicamente database.py
database_file = "database.py"
if os.path.exists(database_file):
    size = os.path.getsize(database_file)
    print(f"✅ {database_file} EXISTE ({size} bytes)")
    
    # Intentar leer las primeras líneas
    try:
        with open(database_file, 'r', encoding='utf-8') as f:
            first_lines = [f.readline().strip() for _ in range(3)]
        print(f"📖 Primeras líneas de {database_file}:")
        for i, line in enumerate(first_lines, 1):
            if line:
                print(f"   {i}: {line}")
    except Exception as e:
        print(f"❌ Error leyendo {database_file}: {e}")
else:
    print(f"❌ {database_file} NO EXISTE")
print()

# 5. Intentar import
print("🔬 PRUEBA DE IMPORT:")
try:
    import database
    print("✅ 'import database' EXITOSO")
    
    # Verificar qué tiene el módulo
    attributes = [attr for attr in dir(database) if not attr.startswith('_')]
    print(f"📋 Atributos en database: {attributes}")
    
    # Verificar elementos específicos
    required_items = ['engine', 'test_connection', 'Base']
    for item in required_items:
        if hasattr(database, item):
            print(f"   ✅ {item} disponible")
        else:
            print(f"   ❌ {item} NO disponible")
            
except ImportError as e:
    print(f"❌ 'import database' FALLÓ: {e}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")
print()

# 6. Verificar Python path
print("🐍 Python sys.path:")
for i, path in enumerate(sys.path[:5]):  # Solo primeros 5
    print(f"   {i}: {path}")
if len(sys.path) > 5:
    print(f"   ... y {len(sys.path) - 5} más")
print()

# 7. Verificar versión de Python
print(f"🐍 Versión de Python: {sys.version}")
print(f"💻 Plataforma: {sys.platform}")