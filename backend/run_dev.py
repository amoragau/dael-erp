#!/usr/bin/env python3
"""
Script para iniciar FastAPI en desarrollo local
Conecta a MySQL en Docker
"""

import uvicorn
import os
from pathlib import Path

# Configurar variables de entorno para desarrollo
os.environ.setdefault("DATABASE_URL", "mysql+aiomysql://amoragau:dosenuno@localhost:3306/erp-dael")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("ENVIRONMENT", "development")

if __name__ == "__main__":
    print("🏢 Iniciando FastAPI - ERP DAEL")
    print("🐍 Python 3.13 - Desarrollo Local")
    print("🗄️ MySQL: localhost:3306")
    print("🌐 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )