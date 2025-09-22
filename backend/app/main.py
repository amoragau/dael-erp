"""
FastAPI para ERP DAEL - Optimizado para uvicorn
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# IMPORTS ABSOLUTOS - No relativos
from database import engine, test_connection, Base
from routes import unidades_medida
from routes import tipos_movimiento
from routes import categorias
from routes import subcategorias
from routes import tipos_producto
from routes import marcas
from routes import proveedores
from routes import sucursales_proveedor
from routes import bodegas
from routes import pasillos
from routes import estantes
from routes import productos
from routes import producto_proveedores
from routes import producto_ubicaciones
from routes import documentos_movimiento
from routes import movimientos_inventario
from routes import movimientos_detalle
from routes import lotes
from routes import numeros_serie
from routes import clientes
from routes import obras
from routes import almacen_obra
from routes import despachos_obra
from routes import despachos_obra_detalle
from routes import devoluciones_obra
from routes import devoluciones_obra_detalle
from routes import inventario_obra
from routes import reservas
from routes import programacion_conteos
from routes import conteos_fisicos
from routes import configuracion_alertas
from routes import log_alertas
from routes import roles
from routes import usuarios
from routes import permisos
from routes import configuracion_sistema
from routes import inventario_consolidado
from routes import obras_inventario
from routes import devoluciones_pendientes
from routes import productos_abc
from routes import estados_orden_compra
from routes import ordenes_compra
from routes import recepciones_mercancia
from routes import vistas_ordenes_compra
from routes import documentos_compra

# Cargar variables de entorno
load_dotenv()

# Crear las tablas en la base de datos
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas de base de datos verificadas/creadas")
except Exception as e:
    print(f"⚠️ Error con base de datos: {e}")

# Crear aplicación FastAPI
app = FastAPI(
    title="ERP DAEL API",
    description="Sistema de inventario para equipos contra incendios",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas de la API
app.include_router(unidades_medida.router, prefix="/api/v1")
app.include_router(tipos_movimiento.router, prefix="/api/v1")
app.include_router(categorias.router, prefix="/api/v1")
app.include_router(subcategorias.router, prefix="/api/v1")
app.include_router(tipos_producto.router, prefix="/api/v1")
app.include_router(marcas.router, prefix="/api/v1")
app.include_router(proveedores.router, prefix="/api/v1")
app.include_router(sucursales_proveedor.router, prefix="/api/v1")
app.include_router(bodegas.router, prefix="/api/v1")
app.include_router(pasillos.router, prefix="/api/v1")
app.include_router(estantes.router, prefix="/api/v1")
app.include_router(productos.router, prefix="/api/v1")
app.include_router(producto_proveedores.router, prefix="/api/v1")
app.include_router(producto_ubicaciones.router, prefix="/api/v1")
app.include_router(documentos_movimiento.router, prefix="/api/v1")
app.include_router(movimientos_inventario.router, prefix="/api/v1")
app.include_router(movimientos_detalle.router, prefix="/api/v1")
app.include_router(lotes.router, prefix="/api/v1")
app.include_router(numeros_serie.router, prefix="/api/v1")
app.include_router(clientes.router, prefix="/api/v1")
app.include_router(obras.router, prefix="/api/v1")
app.include_router(almacen_obra.router, prefix="/api/v1")
app.include_router(despachos_obra.router, prefix="/api/v1")
app.include_router(despachos_obra_detalle.router, prefix="/api/v1")
app.include_router(devoluciones_obra.router, prefix="/api/v1")
app.include_router(devoluciones_obra_detalle.router, prefix="/api/v1")
app.include_router(inventario_obra.router, prefix="/api/v1")
app.include_router(reservas.router, prefix="/api/v1")
app.include_router(programacion_conteos.router, prefix="/api/v1")
app.include_router(conteos_fisicos.router, prefix="/api/v1")
app.include_router(configuracion_alertas.router, prefix="/api/v1")
app.include_router(log_alertas.router, prefix="/api/v1")
app.include_router(roles.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")
app.include_router(permisos.router, prefix="/api/v1")
app.include_router(configuracion_sistema.router, prefix="/api/v1")
app.include_router(inventario_consolidado.router, prefix="/api/v1")
app.include_router(obras_inventario.router, prefix="/api/v1")
app.include_router(devoluciones_pendientes.router, prefix="/api/v1")
app.include_router(productos_abc.router, prefix="/api/v1")
app.include_router(estados_orden_compra.router, prefix="/api/v1/estados-orden-compra", tags=["Estados Orden Compra"])
app.include_router(ordenes_compra.router, prefix="/api/v1/ordenes-compra", tags=["Órdenes de Compra"])
app.include_router(recepciones_mercancia.router, prefix="/api/v1/recepciones-mercancia", tags=["Recepciones de Mercancía"])
app.include_router(vistas_ordenes_compra.router, prefix="/api/v1/vistas-ordenes-compra", tags=["Vistas Órdenes de Compra"])

# Nuevas rutas de documentos de compra
app.include_router(documentos_compra.router, prefix="/api/v1", tags=["Documentos de Compra"])

@app.get("/")
def root():
    return {
        "message": "ERP DAEL API - Sistema de Inventario",
        "version": "1.0.0",
        "python": "3.13",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "unidades_medida": "/api/v1/unidades-medida",
            "tipos_movimiento": "/api/v1/tipos-movimiento",
            "categorias": "/api/v1/categorias",
            "subcategorias": "/api/v1/subcategorias",
            "tipos_producto": "/api/v1/tipos-producto",
            "marcas": "/api/v1/marcas",
            "proveedores": "/api/v1/proveedores",
            "bodegas": "/api/v1/bodegas",
            "pasillos": "/api/v1/pasillos",
            "estantes": "/api/v1/estantes",
            "productos": "/api/v1/productos",
            "producto_proveedores": "/api/v1/producto-proveedores",
            "producto_ubicaciones": "/api/v1/producto-ubicaciones",
            "documentos_movimiento": "/api/v1/documentos-movimiento",
            "movimientos_inventario": "/api/v1/movimientos-inventario",
            "movimientos_detalle": "/api/v1/movimientos-detalle",
            "lotes": "/api/v1/lotes",
            "numeros_serie": "/api/v1/numeros-serie",
            "clientes": "/api/v1/clientes",
            "obras": "/api/v1/obras",
            "almacen_obra": "/api/v1/almacen-obra",
            "despachos_obra": "/api/v1/despachos-obra",
            "despachos_obra_detalle": "/api/v1/despachos-obra-detalle",
            "devoluciones_obra": "/api/v1/devoluciones-obra",
            "devoluciones_obra_detalle": "/api/v1/devoluciones-obra-detalle",
            "inventario_obra": "/api/v1/inventario-obra",
            "reservas": "/api/v1/reservas",
            "programacion_conteos": "/api/v1/programacion-conteos",
            "conteos_fisicos": "/api/v1/conteos-fisicos",
            "configuracion_alertas": "/api/v1/configuracion-alertas",
            "log_alertas": "/api/v1/log-alertas",
            "roles": "/api/v1/roles",
            "usuarios": "/api/v1/usuarios",
            "permisos": "/api/v1/permisos",
            "configuracion_sistema": "/api/v1/configuracion-sistema",
            "inventario_consolidado": "/api/v1/inventario-consolidado",
            "obras_inventario": "/api/v1/obras-inventario",
            "devoluciones_pendientes": "/api/v1/devoluciones-pendientes",
            "productos_abc": "/api/v1/productos-abc",
            "documentos_orden_compra": "/api/v1/documentos-orden-compra",
            "conciliacion_oc_facturas": "/api/v1/conciliacion-oc-facturas",
            "pagos_ordenes_compra": "/api/v1/pagos-ordenes-compra",
            "workflow_dashboard": "/api/v1/workflow-dashboard",
            "xml_processor": "/api/v1/xml-processor"
        }
    }

@app.get("/health")
def health_check():
    db_status = test_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected",
        "mysql_url": "mysql://localhost:3306",
        "message": "API funcionando correctamente"
    }
