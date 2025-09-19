from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

# Imports locales
from database import get_db
from models import VistaInventarioConsolidado
from schemas import (
    InventarioConsolidadoResponse,
    InventarioConsolidadoCompleto,
    InventarioConsolidadoFilters,
    EstadisticasInventario,
    AlertaInventario,
    RecomendacionReposicion,
    AnalisisRotacion,
    NivelStock
)
from crud import inventario_consolidado_crud

# Configuración del router
router = APIRouter(
    prefix="/inventario-consolidado",
    tags=["Inventario Consolidado"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS PRINCIPALES
# ========================================

@router.get("/", response_model=List[InventarioConsolidadoResponse])
def listar_inventario_consolidado(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    nivel_stock: Optional[NivelStock] = Query(None, description="Filtrar por nivel de stock"),
    necesita_reposicion: Optional[bool] = Query(None, description="Filtrar productos que necesitan reposición"),
    exceso_stock: Optional[bool] = Query(None, description="Filtrar productos con exceso de stock"),
    es_alto_valor: Optional[bool] = Query(None, description="Filtrar productos de alto valor"),
    buscar_sku: Optional[str] = Query(None, description="Buscar por SKU"),
    buscar_nombre: Optional[str] = Query(None, description="Buscar por nombre"),
    db: Session = Depends(get_db)
):
    """
    Obtener inventario consolidado con filtros avanzados
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **nivel_stock**: Filtrar por nivel específico (AGOTADO, CRITICO, BAJO, NORMAL, EXCESO)
    - **necesita_reposicion**: Productos que requieren reposición
    - **exceso_stock**: Productos con exceso de inventario
    """
    filtros = InventarioConsolidadoFilters(
        nivel_stock=nivel_stock,
        necesita_reposicion=necesita_reposicion,
        exceso_stock=exceso_stock,
        es_alto_valor=es_alto_valor,
        buscar_sku=buscar_sku,
        buscar_nombre=buscar_nombre
    )

    productos = inventario_consolidado_crud.get_inventario_consolidado(db, skip=skip, limit=limit, filtros=filtros)

    # Convertir a response añadiendo propiedades calculadas
    response_productos = []
    for producto in productos:
        response_productos.append(InventarioConsolidadoResponse(
            **producto.__dict__,
            nivel_stock=producto.nivel_stock,
            necesita_reposicion=producto.necesita_reposicion,
            exceso_stock=producto.exceso_stock,
            porcentaje_stock_minimo=producto.porcentaje_stock_minimo,
            porcentaje_stock_maximo=producto.porcentaje_stock_maximo,
            es_producto_alto_valor=producto.es_producto_alto_valor
        ))

    return response_productos

@router.get("/{producto_id}", response_model=InventarioConsolidadoCompleto)
def obtener_producto_consolidado(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """Obtener información consolidada completa de un producto específico"""
    producto = db.query(VistaInventarioConsolidado).filter(VistaInventarioConsolidado.id_producto == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return InventarioConsolidadoCompleto(
        **producto.__dict__,
        nivel_stock=producto.nivel_stock,
        necesita_reposicion=producto.necesita_reposicion,
        exceso_stock=producto.exceso_stock,
        porcentaje_stock_minimo=producto.porcentaje_stock_minimo,
        porcentaje_stock_maximo=producto.porcentaje_stock_maximo,
        es_producto_alto_valor=producto.es_producto_alto_valor,
        distribucion_stock=producto.distribucion_stock,
        valor_promedio_unitario=producto.valor_promedio_unitario,
        dias_stock_estimados=producto.dias_stock_estimados
    )

@router.get("/sku/{sku}", response_model=InventarioConsolidadoCompleto)
def obtener_producto_por_sku(
    sku: str,
    db: Session = Depends(get_db)
):
    """Obtener información consolidada de un producto por SKU"""
    producto = inventario_consolidado_crud.get_producto_by_sku(db, sku)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return InventarioConsolidadoCompleto(
        **producto.__dict__,
        nivel_stock=producto.nivel_stock,
        necesita_reposicion=producto.necesita_reposicion,
        exceso_stock=producto.exceso_stock,
        porcentaje_stock_minimo=producto.porcentaje_stock_minimo,
        porcentaje_stock_maximo=producto.porcentaje_stock_maximo,
        es_producto_alto_valor=producto.es_producto_alto_valor,
        distribucion_stock=producto.distribucion_stock,
        valor_promedio_unitario=producto.valor_promedio_unitario,
        dias_stock_estimados=producto.dias_stock_estimados
    )

# ========================================
# ENDPOINTS DE ALERTAS Y MONITOREO
# ========================================

@router.get("/alertas/criticos", response_model=List[InventarioConsolidadoResponse])
def obtener_productos_criticos(
    limit: int = Query(50, ge=1, le=500, description="Máximo productos a retornar"),
    db: Session = Depends(get_db)
):
    """Obtener productos con stock crítico (por debajo del mínimo)"""
    productos = inventario_consolidado_crud.get_productos_criticos(db, limit=limit)

    response_productos = []
    for producto in productos:
        response_productos.append(InventarioConsolidadoResponse(
            **producto.__dict__,
            nivel_stock=producto.nivel_stock,
            necesita_reposicion=producto.necesita_reposicion,
            exceso_stock=producto.exceso_stock,
            porcentaje_stock_minimo=producto.porcentaje_stock_minimo,
            porcentaje_stock_maximo=producto.porcentaje_stock_maximo,
            es_producto_alto_valor=producto.es_producto_alto_valor
        ))

    return response_productos

@router.get("/alertas/agotados", response_model=List[InventarioConsolidadoResponse])
def obtener_productos_agotados(
    limit: int = Query(50, ge=1, le=500, description="Máximo productos a retornar"),
    db: Session = Depends(get_db)
):
    """Obtener productos completamente agotados"""
    productos = inventario_consolidado_crud.get_productos_agotados(db, limit=limit)

    response_productos = []
    for producto in productos:
        response_productos.append(InventarioConsolidadoResponse(
            **producto.__dict__,
            nivel_stock=producto.nivel_stock,
            necesita_reposicion=producto.necesita_reposicion,
            exceso_stock=producto.exceso_stock,
            porcentaje_stock_minimo=producto.porcentaje_stock_minimo,
            porcentaje_stock_maximo=producto.porcentaje_stock_maximo,
            es_producto_alto_valor=producto.es_producto_alto_valor
        ))

    return response_productos

@router.get("/alertas/exceso", response_model=List[InventarioConsolidadoResponse])
def obtener_productos_exceso(
    limit: int = Query(50, ge=1, le=500, description="Máximo productos a retornar"),
    db: Session = Depends(get_db)
):
    """Obtener productos con exceso de stock (por encima del máximo)"""
    productos = inventario_consolidado_crud.get_productos_exceso(db, limit=limit)

    response_productos = []
    for producto in productos:
        response_productos.append(InventarioConsolidadoResponse(
            **producto.__dict__,
            nivel_stock=producto.nivel_stock,
            necesita_reposicion=producto.necesita_reposicion,
            exceso_stock=producto.exceso_stock,
            porcentaje_stock_minimo=producto.porcentaje_stock_minimo,
            porcentaje_stock_maximo=producto.porcentaje_stock_maximo,
            es_producto_alto_valor=producto.es_producto_alto_valor
        ))

    return response_productos

@router.get("/alertas/alto-valor", response_model=List[InventarioConsolidadoResponse])
def obtener_productos_alto_valor(
    valor_minimo: float = Query(10000.0, ge=0, description="Valor mínimo para considerar alto valor"),
    limit: int = Query(50, ge=1, le=500, description="Máximo productos a retornar"),
    db: Session = Depends(get_db)
):
    """Obtener productos de alto valor que requieren atención especial"""
    productos = inventario_consolidado_crud.get_productos_alto_valor(db, valor_minimo=valor_minimo, limit=limit)

    response_productos = []
    for producto in productos:
        response_productos.append(InventarioConsolidadoResponse(
            **producto.__dict__,
            nivel_stock=producto.nivel_stock,
            necesita_reposicion=producto.necesita_reposicion,
            exceso_stock=producto.exceso_stock,
            porcentaje_stock_minimo=producto.porcentaje_stock_minimo,
            porcentaje_stock_maximo=producto.porcentaje_stock_maximo,
            es_producto_alto_valor=producto.es_producto_alto_valor
        ))

    return response_productos

@router.get("/alertas/sistema", response_model=List[AlertaInventario])
def obtener_alertas_sistema(
    db: Session = Depends(get_db)
):
    """Obtener todas las alertas activas del sistema de inventario"""
    alertas_data = inventario_consolidado_crud.get_alertas_inventario(db)

    alertas = []
    for alerta_data in alertas_data:
        alertas.append(AlertaInventario(**alerta_data))

    return alertas

# ========================================
# ENDPOINTS DE RECOMENDACIONES
# ========================================

@router.get("/recomendaciones/reposicion", response_model=List[RecomendacionReposicion])
def obtener_recomendaciones_reposicion(
    db: Session = Depends(get_db)
):
    """Obtener recomendaciones de reposición de inventario"""
    recomendaciones_data = inventario_consolidado_crud.get_recomendaciones_reposicion(db)

    recomendaciones = []
    for rec_data in recomendaciones_data:
        recomendaciones.append(RecomendacionReposicion(**rec_data))

    return recomendaciones

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/resumen", response_model=EstadisticasInventario)
def obtener_resumen_inventario(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas consolidadas del inventario"""
    stats_data = inventario_consolidado_crud.get_estadisticas_inventario(db)

    return EstadisticasInventario(**stats_data)

@router.get("/stats/count")
def contar_productos_inventario(
    nivel_stock: Optional[NivelStock] = Query(None, description="Filtrar por nivel de stock"),
    necesita_reposicion: Optional[bool] = Query(None, description="Filtrar por necesidad de reposición"),
    es_alto_valor: Optional[bool] = Query(None, description="Filtrar por alto valor"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de productos con filtros específicos"""
    filtros = InventarioConsolidadoFilters(
        nivel_stock=nivel_stock,
        necesita_reposicion=necesita_reposicion,
        es_alto_valor=es_alto_valor
    )

    productos = inventario_consolidado_crud.get_inventario_consolidado(db, skip=0, limit=10000, filtros=filtros)
    total = len(productos)

    return {"total_productos": total}

@router.get("/stats/por-nivel")
def estadisticas_por_nivel_stock(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de productos por nivel de stock"""
    from sqlalchemy import func

    # Obtener todos los productos
    productos = db.query(VistaInventarioConsolidado).all()

    # Contar por nivel (usando las properties del modelo)
    conteos = {
        'AGOTADO': 0,
        'CRITICO': 0,
        'BAJO': 0,
        'NORMAL': 0,
        'EXCESO': 0,
        'SIN_DATOS': 0
    }

    valor_por_nivel = {
        'AGOTADO': 0.0,
        'CRITICO': 0.0,
        'BAJO': 0.0,
        'NORMAL': 0.0,
        'EXCESO': 0.0,
        'SIN_DATOS': 0.0
    }

    for producto in productos:
        nivel = producto.nivel_stock
        conteos[nivel] += 1
        valor_por_nivel[nivel] += float(producto.valor_total) if producto.valor_total else 0.0

    return {
        "conteos_por_nivel": conteos,
        "valor_por_nivel": valor_por_nivel,
        "total_productos": len(productos),
        "valor_total_inventario": sum(valor_por_nivel.values())
    }

# ========================================
# ENDPOINTS DE BÚSQUEDA Y FILTROS
# ========================================

@router.get("/buscar/termino")
def buscar_productos_inventario(
    q: str = Query(..., min_length=2, description="Término de búsqueda (SKU o nombre)"),
    limit: int = Query(50, ge=1, le=200, description="Máximo productos a retornar"),
    db: Session = Depends(get_db)
):
    """Buscar productos en el inventario por SKU o nombre"""
    productos = inventario_consolidado_crud.buscar_productos(db, q, limit=limit)

    response_productos = []
    for producto in productos:
        response_productos.append(InventarioConsolidadoResponse(
            **producto.__dict__,
            nivel_stock=producto.nivel_stock,
            necesita_reposicion=producto.necesita_reposicion,
            exceso_stock=producto.exceso_stock,
            porcentaje_stock_minimo=producto.porcentaje_stock_minimo,
            porcentaje_stock_maximo=producto.porcentaje_stock_maximo,
            es_producto_alto_valor=producto.es_producto_alto_valor
        ))

    return response_productos

@router.get("/filtrar/rango-valor")
def filtrar_por_rango_valor(
    valor_min: float = Query(..., ge=0, description="Valor mínimo"),
    valor_max: float = Query(..., ge=0, description="Valor máximo"),
    db: Session = Depends(get_db)
):
    """Filtrar productos por rango de valor total"""
    if valor_min > valor_max:
        raise HTTPException(status_code=400, detail="El valor mínimo no puede ser mayor al máximo")

    productos = inventario_consolidado_crud.get_inventario_por_rango_valor(db, valor_min, valor_max)

    response_productos = []
    for producto in productos:
        response_productos.append(InventarioConsolidadoResponse(
            **producto.__dict__,
            nivel_stock=producto.nivel_stock,
            necesita_reposicion=producto.necesita_reposicion,
            exceso_stock=producto.exceso_stock,
            porcentaje_stock_minimo=producto.porcentaje_stock_minimo,
            porcentaje_stock_maximo=producto.porcentaje_stock_maximo,
            es_producto_alto_valor=producto.es_producto_alto_valor
        ))

    return response_productos

# ========================================
# ENDPOINTS DE EXPORTACIÓN
# ========================================

@router.get("/export/excel")
def exportar_inventario_excel(
    incluir_solo_criticos: bool = Query(False, description="Exportar solo productos críticos"),
    incluir_solo_alto_valor: bool = Query(False, description="Exportar solo productos de alto valor"),
    db: Session = Depends(get_db)
):
    """Exportar inventario consolidado a formato Excel"""
    from datetime import datetime

    if incluir_solo_criticos:
        productos = inventario_consolidado_crud.get_productos_criticos(db, limit=1000)
        filtros_aplicados = "Solo productos críticos"
    elif incluir_solo_alto_valor:
        productos = inventario_consolidado_crud.get_productos_alto_valor(db, limit=1000)
        filtros_aplicados = "Solo productos de alto valor"
    else:
        productos = inventario_consolidado_crud.get_inventario_consolidado(db, skip=0, limit=10000)
        filtros_aplicados = "Todos los productos"

    # Convertir a formato de exportación
    productos_export = []
    for producto in productos:
        productos_export.append({
            'ID': producto.id_producto,
            'SKU': producto.sku,
            'Nombre': producto.nombre_producto,
            'Stock Almacén': producto.stock_almacen,
            'Stock Obras': producto.stock_obras,
            'Stock Total': producto.stock_total,
            'Stock Mínimo': producto.stock_minimo,
            'Stock Máximo': producto.stock_maximo,
            'Nivel Stock': producto.nivel_stock,
            'Costo Promedio': float(producto.costo_promedio) if producto.costo_promedio else 0,
            'Valor Total': float(producto.valor_total) if producto.valor_total else 0,
            'Necesita Reposición': 'Sí' if producto.necesita_reposicion else 'No',
            'Exceso Stock': 'Sí' if producto.exceso_stock else 'No',
            '% Stock Mínimo': producto.porcentaje_stock_minimo,
            'Alto Valor': 'Sí' if producto.es_producto_alto_valor else 'No'
        })

    estadisticas = inventario_consolidado_crud.get_estadisticas_inventario(db)

    return {
        "metadata": {
            "fecha_exportacion": datetime.now().isoformat(),
            "total_registros": len(productos_export),
            "filtros_aplicados": filtros_aplicados,
            "generado_por": "Sistema ERP DAEL"
        },
        "estadisticas_resumen": estadisticas,
        "productos": productos_export
    }

@router.get("/dashboard/data")
def obtener_datos_dashboard(
    db: Session = Depends(get_db)
):
    """Obtener datos consolidados para dashboard de inventario"""
    estadisticas = inventario_consolidado_crud.get_estadisticas_inventario(db)
    alertas = inventario_consolidado_crud.get_alertas_inventario(db)
    productos_criticos = inventario_consolidado_crud.get_productos_criticos(db, limit=10)
    productos_alto_valor = inventario_consolidado_crud.get_productos_alto_valor(db, limit=10)

    return {
        "estadisticas_generales": estadisticas,
        "total_alertas": len(alertas),
        "alertas_recientes": alertas[:5],  # Solo las 5 más importantes
        "productos_criticos_top": [
            {
                "id_producto": p.id_producto,
                "sku": p.sku,
                "nombre_producto": p.nombre_producto,
                "stock_total": p.stock_total,
                "stock_minimo": p.stock_minimo,
                "nivel_stock": p.nivel_stock
            }
            for p in productos_criticos
        ],
        "productos_alto_valor_top": [
            {
                "id_producto": p.id_producto,
                "sku": p.sku,
                "nombre_producto": p.nombre_producto,
                "stock_total": p.stock_total,
                "valor_total": float(p.valor_total) if p.valor_total else 0
            }
            for p in productos_alto_valor
        ]
    }