"""
Rutas para el manejo de vista de obras inventario
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, date

from database import get_db
from crud import ObrasInventarioCRUD
from schemas import (
    VistaObrasInventarioRead,
    VistaObrasInventarioFilter,
    EstadoObra,
    TipoObra,
    UrgenciaObra,
    AlertaObra,
    MetricaObra
)

router = APIRouter(
    prefix="/obras-inventario",
    tags=["Obras Inventario"]
)

@router.get("/", response_model=List[VistaObrasInventarioRead])
def listar_obras_inventario(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros a retornar"),
    obra_id: Optional[int] = Query(None, description="Filtrar por ID de obra"),
    cliente_id: Optional[int] = Query(None, description="Filtrar por ID de cliente"),
    bodega_id: Optional[int] = Query(None, description="Filtrar por ID de bodega"),
    producto_id: Optional[int] = Query(None, description="Filtrar por ID de producto"),
    estado_obra: Optional[EstadoObra] = Query(None, description="Filtrar por estado de obra"),
    tipo_obra: Optional[TipoObra] = Query(None, description="Filtrar por tipo de obra"),
    urgencia_obra: Optional[UrgenciaObra] = Query(None, description="Filtrar por urgencia de obra"),
    fecha_inicio_desde: Optional[date] = Query(None, description="Fecha de inicio desde"),
    fecha_inicio_hasta: Optional[date] = Query(None, description="Fecha de inicio hasta"),
    fecha_fin_desde: Optional[date] = Query(None, description="Fecha de fin desde"),
    fecha_fin_hasta: Optional[date] = Query(None, description="Fecha de fin hasta"),
    tiene_stock_critico: Optional[bool] = Query(None, description="Filtrar por stock crítico"),
    tiene_sobrecosto: Optional[bool] = Query(None, description="Filtrar por sobrecosto"),
    db: Session = Depends(get_db)
):
    """Obtener lista de obras inventario con filtros opcionales"""
    filtro = VistaObrasInventarioFilter(
        obra_id=obra_id,
        cliente_id=cliente_id,
        bodega_id=bodega_id,
        producto_id=producto_id,
        estado_obra=estado_obra,
        tipo_obra=tipo_obra,
        urgencia_obra=urgencia_obra,
        fecha_inicio_desde=fecha_inicio_desde,
        fecha_inicio_hasta=fecha_inicio_hasta,
        fecha_fin_desde=fecha_fin_desde,
        fecha_fin_hasta=fecha_fin_hasta,
        tiene_stock_critico=tiene_stock_critico,
        tiene_sobrecosto=tiene_sobrecosto
    )

    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_multi_filtered(filtro=filtro, skip=skip, limit=limit)

@router.get("/{obra_id}", response_model=VistaObrasInventarioRead)
def obtener_obra_inventario(obra_id: int, db: Session = Depends(get_db)):
    """Obtener una obra inventario específica por ID"""
    crud_obras = ObrasInventarioCRUD(db)
    obra = crud_obras.get(obra_id)
    if not obra:
        raise HTTPException(status_code=404, detail="Obra inventario no encontrada")
    return obra

@router.get("/activas/listar", response_model=List[VistaObrasInventarioRead])
def obtener_obras_activas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener obras activas"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_obras_activas(skip=skip, limit=limit)

@router.get("/retrasadas/listar", response_model=List[VistaObrasInventarioRead])
def obtener_obras_retrasadas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener obras retrasadas"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_obras_retrasadas(skip=skip, limit=limit)

@router.get("/urgentes/listar", response_model=List[VistaObrasInventarioRead])
def obtener_obras_urgentes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener obras urgentes"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_obras_urgentes(skip=skip, limit=limit)

@router.get("/alto-valor/listar", response_model=List[VistaObrasInventarioRead])
def obtener_obras_alto_valor(
    valor_minimo: float = Query(100000.0, description="Valor mínimo para considerar alto valor"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener obras de alto valor"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_obras_alto_valor(valor_minimo=valor_minimo, skip=skip, limit=limit)

@router.get("/estadisticas/generales", response_model=Dict[str, Any])
def obtener_estadisticas_generales(db: Session = Depends(get_db)):
    """Obtener estadísticas generales de obras inventario"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_estadisticas_generales()

@router.get("/estadisticas/por-estado", response_model=Dict[str, Any])
def obtener_estadisticas_por_estado(db: Session = Depends(get_db)):
    """Obtener estadísticas por estado de obra"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_estadisticas_por_estado()

@router.get("/estadisticas/por-tipo", response_model=Dict[str, Any])
def obtener_estadisticas_por_tipo(db: Session = Depends(get_db)):
    """Obtener estadísticas por tipo de obra"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_estadisticas_por_tipo()

@router.get("/estadisticas/por-cliente", response_model=Dict[str, Any])
def obtener_estadisticas_por_cliente(
    top_clientes: int = Query(10, ge=1, le=50, description="Número de top clientes"),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas por cliente"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_estadisticas_por_cliente(top_clientes=top_clientes)

@router.get("/estadisticas/financieras", response_model=Dict[str, Any])
def obtener_estadisticas_financieras(db: Session = Depends(get_db)):
    """Obtener estadísticas financieras de obras"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_estadisticas_financieras()

@router.get("/alertas/listar", response_model=List[Dict[str, Any]])
def obtener_alertas_obras(
    tipo_alerta: Optional[AlertaObra] = Query(None, description="Filtrar por tipo de alerta"),
    db: Session = Depends(get_db)
):
    """Obtener alertas de obras inventario"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_alertas(tipo_alerta=tipo_alerta)

@router.get("/alertas/resumen", response_model=Dict[str, Any])
def obtener_resumen_alertas(db: Session = Depends(get_db)):
    """Obtener resumen de alertas de obras"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_resumen_alertas()

@router.get("/recomendaciones/optimizacion", response_model=List[Dict[str, Any]])
def obtener_recomendaciones_optimizacion(
    limite_recomendaciones: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Obtener recomendaciones para optimización de obras"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_recomendaciones_optimizacion(limite=limite_recomendaciones)

@router.get("/recomendaciones/resumen", response_model=Dict[str, Any])
def obtener_resumen_recomendaciones(db: Session = Depends(get_db)):
    """Obtener resumen de recomendaciones"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_resumen_recomendaciones()

@router.get("/ranking/eficiencia", response_model=List[Dict[str, Any]])
def obtener_ranking_eficiencia(
    top_obras: int = Query(10, ge=1, le=100, description="Número de obras en el ranking"),
    db: Session = Depends(get_db)
):
    """Obtener ranking de obras por eficiencia"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_ranking_eficiencia(top=top_obras)

@router.get("/ranking/rentabilidad", response_model=List[Dict[str, Any]])
def obtener_ranking_rentabilidad(
    top_obras: int = Query(10, ge=1, le=100, description="Número de obras en el ranking"),
    db: Session = Depends(get_db)
):
    """Obtener ranking de obras por rentabilidad"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_ranking_rentabilidad(top=top_obras)

@router.get("/dashboard/kpis", response_model=Dict[str, Any])
def obtener_dashboard_kpis(db: Session = Depends(get_db)):
    """Obtener KPIs principales para dashboard de obras"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_dashboard_kpis()

@router.get("/dashboard/metricas/{obra_id}", response_model=Dict[str, Any])
def obtener_metricas_obra(obra_id: int, db: Session = Depends(get_db)):
    """Obtener métricas detalladas de una obra específica"""
    crud_obras = ObrasInventarioCRUD(db)
    obra = crud_obras.get(obra_id)
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    return crud_obras.get_metricas_obra(obra_id)

@router.get("/analisis/tendencias", response_model=Dict[str, Any])
def obtener_analisis_tendencias(
    meses_analisis: int = Query(12, ge=1, le=60, description="Número de meses para análisis"),
    db: Session = Depends(get_db)
):
    """Obtener análisis de tendencias de obras"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_analisis_tendencias(meses=meses_analisis)

@router.get("/exportar/excel", response_model=Dict[str, Any])
def exportar_obras_excel(
    filtro: Optional[VistaObrasInventarioFilter] = None,
    db: Session = Depends(get_db)
):
    """Exportar obras inventario a Excel"""
    crud_obras = ObrasInventarioCRUD(db)
    # En un entorno real, aquí se generaría el archivo Excel
    obras = crud_obras.get_multi_filtered(filtro=filtro, skip=0, limit=10000)
    return {
        "mensaje": "Exportación iniciada",
        "total_registros": len(obras),
        "archivo": "obras_inventario_export.xlsx",
        "fecha_generacion": datetime.now().isoformat()
    }

@router.get("/reportes/ejecutivo", response_model=Dict[str, Any])
def obtener_reporte_ejecutivo(
    periodo_meses: int = Query(3, ge=1, le=24, description="Período en meses para el reporte"),
    db: Session = Depends(get_db)
):
    """Obtener reporte ejecutivo de obras inventario"""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.get_reporte_ejecutivo(periodo_meses=periodo_meses)

@router.get("/buscar/texto", response_model=List[VistaObrasInventarioRead])
def buscar_obras_texto(
    q: str = Query(..., min_length=3, description="Texto a buscar"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Buscar obras por texto en nombre, descripción, cliente, etc."""
    crud_obras = ObrasInventarioCRUD(db)
    return crud_obras.buscar_por_texto(texto=q, skip=skip, limit=limit)

@router.get("/contar/total", response_model=Dict[str, int])
def contar_total_obras(
    filtro: Optional[VistaObrasInventarioFilter] = None,
    db: Session = Depends(get_db)
):
    """Contar total de obras inventario con filtros opcionales"""
    crud_obras = ObrasInventarioCRUD(db)
    total = crud_obras.contar_con_filtros(filtro=filtro)
    return {"total": total}