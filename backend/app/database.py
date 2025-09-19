from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# URL de conexión a MySQL
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://amoragau:dosenuno@localhost:3306/erp-dael")

# Crear engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Para ver las queries SQL en desarrollo
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_recycle=3600  # Renovar conexiones cada hora
)

# Crear SessionLocal para transacciones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependency para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para probar conexión
def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print("✅ Conexión a MySQL exitosa")
            return True
    except Exception as e:
        print(f"❌ Error conectando a MySQL: {e}")
        return False