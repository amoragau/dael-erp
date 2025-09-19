"""
Rutas para el manejo de análisis ABC de productos
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal

from database import get_db
from crud import ProductosABCCRUD
from schemas import (
    VistaProductosABCRead,
    VistaProductosABCFilter,
    ClasificacionABC,
    CategoriaValorInventario,
    CategoriaRotacion,
    CriticidadProducto,
    AccionRecomendada,
    ImpactoFinanciero
)

router = APIRouter(
    prefix="/productos-abc",
    tags=["Productos ABC"]
)

@router.get("/", response_model=List[VistaProductosABCRead])
def listar_productos_abc(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros a retornar"),
    id_producto: Optional[int] = Query(None, description="Filtrar por ID de producto"),
    sku: Optional[str] = Query(None, description="Filtrar por SKU"),
    nombre_producto: Optional[str] = Query(None, description="Filtrar por nombre de producto"),
    clasificacion_abc: Optional[ClasificacionABC] = Query(None, description="Filtrar por clasificación ABC"),
    categoria_valor: Optional[CategoriaValorInventario] = Query(None, description="Filtrar por categoría de valor"),
    categoria_rotacion: Optional[CategoriaRotacion] = Query(None, description="Filtrar por categoría de rotación"),
    criticidad: Optional[CriticidadProducto] = Query(None, description="Filtrar por criticidad"),
    stock_actual_min: Optional[float] = Query(None, description="Stock actual mínimo"),
    stock_actual_max: Optional[float] = Query(None, description="Stock actual máximo"),
    valor_inventario_min: Optional[Decimal] = Query(None, description="Valor de inventario mínimo"),
    valor_inventario_max: Optional[Decimal] = Query(None, description="Valor de inventario máximo"),
    solo_requieren_atencion: Optional[bool] = Query(None, description="Solo productos que requieren atención"),
    solo_sin_stock: Optional[bool] = Query(None, description="Solo productos sin stock"),
    solo_sin_movimiento: Optional[bool] = Query(None, description="Solo productos sin movimiento"),
    db: Session = Depends(get_db)
):
    """Obtener lista de productos ABC con filtros opcionales"""
    filtro = VistaProductosABCFilter(
        id_producto=id_producto,
        sku=sku,
        nombre_producto=nombre_producto,
        clasificacion_abc=clasificacion_abc,
        categoria_valor=categoria_valor,
        categoria_rotacion=categoria_rotacion,
        criticidad=criticidad,
        stock_actual_min=stock_actual_min,
        stock_actual_max=stock_actual_max,
        valor_inventario_min=valor_inventario_min,
        valor_inventario_max=valor_inventario_max,
        solo_requieren_atencion=solo_requieren_atencion,
        solo_sin_stock=solo_sin_stock,
        solo_sin_movimiento=solo_sin_movimiento
    )

    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_multi_filtered(filtro=filtro, skip=skip, limit=limit)

@router.get("/{id_producto}", response_model=VistaProductosABCRead)
def obtener_producto_abc(id_producto: int, db: Session = Depends(get_db)):
    """Obtener un producto ABC específico por ID"""
    crud_productos = ProductosABCCRUD(db)
    producto = crud_productos.get(id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto ABC no encontrado")
    return producto

@router.get("/clase-a/listar", response_model=List[VistaProductosABCRead])
def obtener_productos_clase_a(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener productos clasificados como A"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_productos_clase_a(skip=skip, limit=limit)

@router.get("/clase-b/listar", response_model=List[VistaProductosABCRead])
def obtener_productos_clase_b(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener productos clasificados como B"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_productos_clase_b(skip=skip, limit=limit)

@router.get("/clase-c/listar", response_model=List[VistaProductosABCRead])
def obtener_productos_clase_c(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener productos clasificados como C"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_productos_clase_c(skip=skip, limit=limit)

@router.get("/sin-movimiento/listar", response_model=List[VistaProductosABCRead])
def obtener_productos_sin_movimiento(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener productos sin movimiento en el último año"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_productos_sin_movimiento(skip=skip, limit=limit)

@router.get("/requieren-atencion/listar", response_model=List[VistaProductosABCRead])
def obtener_productos_requieren_atencion(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener productos que requieren atención especial"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_productos_requieren_atencion(skip=skip, limit=limit)

@router.get("/obsolescencia-alta/listar", response_model=List[VistaProductosABCRead])
def obtener_productos_obsolescencia_alta(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener productos con alta obsolescencia"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_productos_obsolescencia_alta(skip=skip, limit=limit)

@router.get("/estadisticas/generales", response_model=Dict[str, Any])
def obtener_estadisticas_generales(db: Session = Depends(get_db)):
    """Obtener estadísticas generales del análisis ABC"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_estadisticas_generales()

@router.get("/ranking/por-valor", response_model=List[Dict[str, Any]])
def obtener_ranking_por_valor(
    top_productos: int = Query(20, ge=1, le=100, description="Número de productos en el ranking"),
    db: Session = Depends(get_db)
):
    """Obtener ranking de productos por valor de inventario"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_ranking_por_valor(top=top_productos)

@router.get("/analisis/obsolescencia", response_model=List[Dict[str, Any]])
def obtener_analisis_obsolescencia(
    limite_productos: int = Query(50, ge=1, le=200, description="Límite de productos a analizar"),
    db: Session = Depends(get_db)
):
    """Obtener análisis de obsolescencia de productos"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_analisis_obsolescencia(limite=limite_productos)

@router.get("/alertas/listar", response_model=List[Dict[str, Any]])
def obtener_alertas_productos(
    nivel_criticidad: Optional[CriticidadProducto] = Query(None, description="Filtrar por nivel de criticidad"),
    db: Session = Depends(get_db)
):
    """Obtener alertas de productos ABC"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_alertas(nivel_criticidad=nivel_criticidad.value if nivel_criticidad else None)

@router.get("/recomendaciones/listar", response_model=List[Dict[str, Any]])
def obtener_recomendaciones_productos(
    limite_recomendaciones: int = Query(20, ge=1, le=100, description="Límite de recomendaciones"),
    db: Session = Depends(get_db)
):
    """Obtener recomendaciones para productos ABC"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_recomendaciones(limite=limite_recomendaciones)

@router.get("/dashboard/kpis", response_model=Dict[str, Any])
def obtener_dashboard_kpis(db: Session = Depends(get_db)):
    """Obtener KPIs principales para dashboard ABC"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_dashboard_kpis()

@router.get("/optimizacion/inventario", response_model=List[Dict[str, Any]])
def obtener_optimizacion_inventario(
    limite_optimizaciones: int = Query(50, ge=1, le=200, description="Límite de optimizaciones"),
    db: Session = Depends(get_db)
):
    """Obtener recomendaciones de optimización de inventario"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.get_optimizacion_inventario(limite=limite_optimizaciones)

@router.get("/buscar/texto", response_model=List[VistaProductosABCRead])
def buscar_productos_texto(
    q: str = Query(..., min_length=2, description="Texto a buscar"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Buscar productos por texto en SKU o nombre"""
    crud_productos = ProductosABCCRUD(db)
    return crud_productos.buscar_por_texto(texto=q, skip=skip, limit=limit)

@router.get("/contar/total", response_model=Dict[str, int])
def contar_total_productos(
    filtro: Optional[VistaProductosABCFilter] = None,
    db: Session = Depends(get_db)
):
    """Contar total de productos ABC con filtros opcionales"""
    crud_productos = ProductosABCCRUD(db)
    total = crud_productos.contar_con_filtros(filtro=filtro)
    return {"total": total}

@router.get("/exportar/excel", response_model=Dict[str, Any])
def exportar_productos_excel(
    filtro: Optional[VistaProductosABCFilter] = None,
    db: Session = Depends(get_db)
):
    """Exportar productos ABC a Excel"""
    crud_productos = ProductosABCCRUD(db)
    # En un entorno real, aquí se generaría el archivo Excel
    productos = crud_productos.get_multi_filtered(filtro=filtro, skip=0, limit=10000)
    return {
        "mensaje": "Exportación iniciada",
        "total_registros": len(productos),
        "archivo": "productos_abc_export.xlsx",
        "fecha_generacion": datetime.now().isoformat()
    }

@router.get("/reportes/ejecutivo", response_model=Dict[str, Any])
def obtener_reporte_ejecutivo(
    incluir_obsolescencia: bool = Query(True, description="Incluir análisis de obsolescencia"),
    incluir_optimizacion: bool = Query(True, description="Incluir recomendaciones de optimización"),
    db: Session = Depends(get_db)
):
    """Obtener reporte ejecutivo del análisis ABC"""
    crud_productos = ProductosABCCRUD(db)

    stats_generales = crud_productos.get_estadisticas_generales()
    ranking_valor = crud_productos.get_ranking_por_valor(top=10)
    alertas_activas = crud_productos.get_alertas()
    recomendaciones = crud_productos.get_recomendaciones(limite=10)

    reporte = {
        "fecha_generacion": datetime.now().isoformat(),
        "resumen_ejecutivo": {
            "total_productos": stats_generales["total_productos"],
            "valor_total_inventario": stats_generales["total_valor_inventario"],
            "distribucion_abc": {
                "clase_a": {
                    "productos": stats_generales["productos_clase_a"],
                    "valor": stats_generales["valor_clase_a"],
                    "porcentaje_valor": stats_generales["porcentaje_valor_a"]
                },
                "clase_b": {
                    "productos": stats_generales["productos_clase_b"],
                    "valor": stats_generales["valor_clase_b"],
                    "porcentaje_valor": stats_generales["porcentaje_valor_b"]
                },
                "clase_c": {
                    "productos": stats_generales["productos_clase_c"],
                    "valor": stats_generales["valor_clase_c"],
                    "porcentaje_valor": stats_generales["porcentaje_valor_c"]
                },
                "sin_movimiento": {
                    "productos": stats_generales["productos_sin_movimiento"],
                    "valor": stats_generales["valor_sin_movimiento"],
                    "porcentaje_valor": stats_generales["porcentaje_sin_movimiento"]
                }
            },
            "eficiencia_inventario": crud_productos._calcular_eficiencia_inventario(),
            "productos_requieren_atencion": stats_generales["productos_requieren_atencion"],
            "productos_obsolescencia_alta": stats_generales["productos_obsolescencia_alta"]
        },
        "top_productos_valor": ranking_valor,
        "alertas_criticas": len([a for a in alertas_activas if a["nivel_criticidad"] in ["CRITICA", "ALTA"]]),
        "recomendaciones_prioritarias": len([r for r in recomendaciones if r["prioridad"] in ["CRITICA", "ALTA"]])
    }

    if incluir_obsolescencia:
        reporte["analisis_obsolescencia"] = crud_productos.get_analisis_obsolescencia(limite=20)

    if incluir_optimizacion:
        reporte["oportunidades_optimizacion"] = crud_productos.get_optimizacion_inventario(limite=20)

    # Conclusiones y recomendaciones estratégicas
    reporte["conclusiones_estrategicas"] = [
        f"El {stats_generales['porcentaje_valor_a']:.1f}% del valor está en productos clase A",
        f"Se identificaron {stats_generales['productos_sin_movimiento']} productos sin movimiento",
        f"La eficiencia del inventario es del {crud_productos._calcular_eficiencia_inventario()}%",
        f"Hay {stats_generales['productos_requieren_atencion']} productos que requieren atención inmediata"
    ]

    return reporte

@router.get("/metricas/rotacion", response_model=Dict[str, Any])
def obtener_metricas_rotacion(db: Session = Depends(get_db)):
    """Obtener métricas de rotación de inventario"""
    crud_productos = ProductosABCCRUD(db)
    productos = crud_productos.get_multi_filtered(skip=0, limit=10000)

    if not productos:
        return {
            "promedio_rotacion": 0,
            "mediana_rotacion": 0,
            "productos_alta_rotacion": 0,
            "productos_baja_rotacion": 0,
            "productos_sin_rotacion": 0
        }

    rotaciones = [p.rotacion_inventario for p in productos]
    promedio = sum(rotaciones) / len(rotaciones)
    mediana = sorted(rotaciones)[len(rotaciones)//2]

    alta_rotacion = len([r for r in rotaciones if r >= 6])
    baja_rotacion = len([r for r in rotaciones if 0 < r < 1])
    sin_rotacion = len([r for r in rotaciones if r == 0])

    return {
        "promedio_rotacion": round(promedio, 2),
        "mediana_rotacion": round(mediana, 2),
        "productos_alta_rotacion": alta_rotacion,
        "productos_baja_rotacion": baja_rotacion,
        "productos_sin_rotacion": sin_rotacion,
        "total_evaluado": len(productos),
        "distribucion_rotacion": {
            "muy_alta": len([r for r in rotaciones if r >= 12]),
            "alta": len([r for r in rotaciones if 6 <= r < 12]),
            "media": len([r for r in rotaciones if 3 <= r < 6]),
            "baja": len([r for r in rotaciones if 1 <= r < 3]),
            "sin_rotacion": sin_rotacion
        }
    }

@router.get("/analisis/pareto", response_model=Dict[str, Any])
def obtener_analisis_pareto(db: Session = Depends(get_db)):
    """Obtener análisis de Pareto (80/20) de productos"""
    crud_productos = ProductosABCCRUD(db)
    productos = crud_productos.get_multi_filtered(skip=0, limit=10000)

    if not productos:
        return {
            "principio_80_20": "Sin datos suficientes",
            "productos_top_20": 0,
            "valor_top_20": 0,
            "porcentaje_valor_top_20": 0
        }

    # Ordenar por valor de inventario
    productos_ordenados = sorted(productos, key=lambda p: float(p.valor_inventario), reverse=True)
    total_productos = len(productos_ordenados)
    total_valor = sum([float(p.valor_inventario) for p in productos_ordenados])

    # Calcular top 20% de productos
    top_20_count = max(1, int(total_productos * 0.2))
    productos_top_20 = productos_ordenados[:top_20_count]
    valor_top_20 = sum([float(p.valor_inventario) for p in productos_top_20])
    porcentaje_valor_top_20 = (valor_top_20 / total_valor) * 100 if total_valor > 0 else 0

    # Determinar si se cumple el principio 80/20
    cumple_pareto = porcentaje_valor_top_20 >= 80

    return {
        "principio_80_20": "Se cumple" if cumple_pareto else "No se cumple completamente",
        "total_productos": total_productos,
        "productos_top_20_pct": top_20_count,
        "valor_total_inventario": total_valor,
        "valor_top_20_pct": valor_top_20,
        "porcentaje_valor_top_20": round(porcentaje_valor_top_20, 2),
        "productos_representan_80_pct": productos_top_20[:min(len(productos_top_20), 10)],
        "recomendacion": "Enfocar gestión en productos top 20%" if cumple_pareto else "Revisar distribución de inventario"
    }

@router.get("/simulacion/punto-reorden", response_model=Dict[str, Any])
def simular_puntos_reorden(
    factor_ajuste: float = Query(1.0, ge=0.5, le=2.0, description="Factor de ajuste para puntos de reorden"),
    db: Session = Depends(get_db)
):
    """Simular impacto de ajustar puntos de reorden"""
    crud_productos = ProductosABCCRUD(db)
    productos = crud_productos.get_multi_filtered(skip=0, limit=1000)

    if not productos:
        return {"mensaje": "Sin productos para simular"}

    simulacion = []
    impacto_total = 0

    for producto in productos:
        punto_actual = producto.stock_actual
        punto_sugerido = producto.punto_reorden_sugerido
        punto_simulado = punto_sugerido * factor_ajuste

        diferencia = punto_simulado - punto_actual
        impacto_monetario = diferencia * float(producto.costo_promedio)
        impacto_total += impacto_monetario

        if abs(diferencia) > 1:  # Solo incluir cambios significativos
            simulacion.append({
                "id_producto": producto.id_producto,
                "sku": producto.sku,
                "nombre_producto": producto.nombre_producto,
                "stock_actual": punto_actual,
                "punto_reorden_actual": punto_sugerido,
                "punto_reorden_simulado": round(punto_simulado, 1),
                "diferencia_unidades": round(diferencia, 1),
                "impacto_monetario": round(impacto_monetario, 2),
                "clasificacion_abc": producto.clasificacion_abc_calculada
            })

    # Ordenar por impacto monetario
    simulacion_sorted = sorted(simulacion, key=lambda x: abs(x["impacto_monetario"]), reverse=True)

    return {
        "factor_ajuste_aplicado": factor_ajuste,
        "productos_afectados": len(simulacion_sorted),
        "impacto_monetario_total": round(impacto_total, 2),
        "simulacion_detallada": simulacion_sorted[:50],  # Top 50 impactos
        "resumen_por_clase": {
            "clase_a": len([s for s in simulacion if s["clasificacion_abc"] == "A"]),
            "clase_b": len([s for s in simulacion if s["clasificacion_abc"] == "B"]),
            "clase_c": len([s for s in simulacion if s["clasificacion_abc"] == "C"])
        },
        "recomendacion": "Ajuste favorable" if -50000 <= impacto_total <= 100000 else "Revisar ajuste propuesto"
    }