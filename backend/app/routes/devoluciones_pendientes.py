"""
Rutas para el manejo de vista de devoluciones pendientes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, date

from database import get_db
from crud import DevolucionesPendientesCRUD
from schemas import (
    VistaDevolucionesPendientesRead,
    VistaDevolucionesPendientesFilter,
    EstadoDevolucion,
    CriticidadDevolucion,
    CategoriaValorDevolucion,
    TipoAlertaDevolucion
)

router = APIRouter(
    prefix="/devoluciones-pendientes",
    tags=["Devoluciones Pendientes"]
)

@router.get("/", response_model=List[VistaDevolucionesPendientesRead])
def listar_devoluciones_pendientes(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros a retornar"),
    id_despacho: Optional[int] = Query(None, description="Filtrar por ID de despacho"),
    numero_despacho: Optional[str] = Query(None, description="Filtrar por número de despacho"),
    codigo_obra: Optional[str] = Query(None, description="Filtrar por código de obra"),
    fecha_despacho_desde: Optional[date] = Query(None, description="Fecha de despacho desde"),
    fecha_despacho_hasta: Optional[date] = Query(None, description="Fecha de despacho hasta"),
    fecha_limite_desde: Optional[date] = Query(None, description="Fecha límite desde"),
    fecha_limite_hasta: Optional[date] = Query(None, description="Fecha límite hasta"),
    dias_para_limite_min: Optional[int] = Query(None, description="Días para límite mínimo"),
    dias_para_limite_max: Optional[int] = Query(None, description="Días para límite máximo"),
    estado_devolucion: Optional[EstadoDevolucion] = Query(None, description="Estado de devolución"),
    criticidad: Optional[CriticidadDevolucion] = Query(None, description="Nivel de criticidad"),
    categoria_valor: Optional[CategoriaValorDevolucion] = Query(None, description="Categoría de valor"),
    solo_vencidas: Optional[bool] = Query(None, description="Solo devoluciones vencidas"),
    solo_urgentes: Optional[bool] = Query(None, description="Solo devoluciones urgentes"),
    solo_atencion_inmediata: Optional[bool] = Query(None, description="Solo que requieren atención inmediata"),
    db: Session = Depends(get_db)
):
    """Obtener lista de devoluciones pendientes con filtros opcionales"""
    filtro = VistaDevolucionesPendientesFilter(
        id_despacho=id_despacho,
        numero_despacho=numero_despacho,
        codigo_obra=codigo_obra,
        fecha_despacho_desde=fecha_despacho_desde,
        fecha_despacho_hasta=fecha_despacho_hasta,
        fecha_limite_desde=fecha_limite_desde,
        fecha_limite_hasta=fecha_limite_hasta,
        dias_para_limite_min=dias_para_limite_min,
        dias_para_limite_max=dias_para_limite_max,
        estado_devolucion=estado_devolucion,
        criticidad=criticidad,
        categoria_valor=categoria_valor,
        solo_vencidas=solo_vencidas,
        solo_urgentes=solo_urgentes,
        solo_atencion_inmediata=solo_atencion_inmediata
    )

    crud_devoluciones = DevolucionesPendientesCRUD(db)
    return crud_devoluciones.get_multi_filtered(filtro=filtro, skip=skip, limit=limit)

@router.get("/{id_despacho}", response_model=VistaDevolucionesPendientesRead)
def obtener_devolucion_pendiente(id_despacho: int, db: Session = Depends(get_db)):
    """Obtener una devolución pendiente específica por ID de despacho"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    devolucion = crud_devoluciones.get(id_despacho)
    if not devolucion:
        raise HTTPException(status_code=404, detail="Devolución pendiente no encontrada")
    return devolucion

@router.get("/vencidas/listar", response_model=List[VistaDevolucionesPendientesRead])
def obtener_devoluciones_vencidas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener devoluciones vencidas"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    return crud_devoluciones.get_devoluciones_vencidas(skip=skip, limit=limit)

@router.get("/urgentes/listar", response_model=List[VistaDevolucionesPendientesRead])
def obtener_devoluciones_urgentes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener devoluciones urgentes (vencen en 7 días o menos)"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    return crud_devoluciones.get_devoluciones_urgentes(skip=skip, limit=limit)

@router.get("/alto-valor/listar", response_model=List[VistaDevolucionesPendientesRead])
def obtener_devoluciones_alto_valor(
    valor_minimo: float = Query(50000.0, description="Valor mínimo para considerar alto valor"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener devoluciones de alto valor"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    return crud_devoluciones.get_devoluciones_alto_valor(valor_minimo=valor_minimo, skip=skip, limit=limit)

@router.get("/atencion-inmediata/listar", response_model=List[VistaDevolucionesPendientesRead])
def obtener_devoluciones_atencion_inmediata(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obtener devoluciones que requieren atención inmediata"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    return crud_devoluciones.get_devoluciones_atencion_inmediata(skip=skip, limit=limit)

@router.get("/estadisticas/generales", response_model=Dict[str, Any])
def obtener_estadisticas_generales(db: Session = Depends(get_db)):
    """Obtener estadísticas generales de devoluciones pendientes"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    return crud_devoluciones.get_estadisticas_generales()

@router.get("/estadisticas/por-estado", response_model=Dict[str, Any])
def obtener_estadisticas_por_estado(db: Session = Depends(get_db)):
    """Obtener estadísticas agrupadas por estado de devolución"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    return crud_devoluciones.get_estadisticas_por_estado()

@router.get("/ranking/por-valor", response_model=List[Dict[str, Any]])
def obtener_ranking_por_valor(
    top_devoluciones: int = Query(10, ge=1, le=50, description="Número de devoluciones en el ranking"),
    db: Session = Depends(get_db)
):
    """Obtener ranking de devoluciones por valor pendiente"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    return crud_devoluciones.get_ranking_por_valor(top=top_devoluciones)

@router.get("/alertas/listar", response_model=List[Dict[str, Any]])
def obtener_alertas_devoluciones(
    tipo_alerta: Optional[TipoAlertaDevolucion] = Query(None, description="Filtrar por tipo de alerta"),
    db: Session = Depends(get_db)
):
    """Obtener alertas de devoluciones pendientes"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    return crud_devoluciones.get_alertas(tipo_alerta=tipo_alerta.value if tipo_alerta else None)

@router.get("/recomendaciones/listar", response_model=List[Dict[str, Any]])
def obtener_recomendaciones_devoluciones(
    limite_recomendaciones: int = Query(10, ge=1, le=50, description="Límite de recomendaciones"),
    db: Session = Depends(get_db)
):
    """Obtener recomendaciones para devoluciones pendientes"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    return crud_devoluciones.get_recomendaciones(limite=limite_recomendaciones)

@router.get("/dashboard/kpis", response_model=Dict[str, Any])
def obtener_dashboard_kpis(db: Session = Depends(get_db)):
    """Obtener KPIs principales para dashboard de devoluciones"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    return crud_devoluciones.get_dashboard_kpis()

@router.get("/buscar/texto", response_model=List[VistaDevolucionesPendientesRead])
def buscar_devoluciones_texto(
    q: str = Query(..., min_length=3, description="Texto a buscar"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Buscar devoluciones por texto en número de despacho, código de obra, etc."""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    return crud_devoluciones.buscar_por_texto(texto=q, skip=skip, limit=limit)

@router.get("/contar/total", response_model=Dict[str, int])
def contar_total_devoluciones(
    filtro: Optional[VistaDevolucionesPendientesFilter] = None,
    db: Session = Depends(get_db)
):
    """Contar total de devoluciones pendientes con filtros opcionales"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    total = crud_devoluciones.contar_con_filtros(filtro=filtro)
    return {"total": total}

@router.get("/exportar/excel", response_model=Dict[str, Any])
def exportar_devoluciones_excel(
    filtro: Optional[VistaDevolucionesPendientesFilter] = None,
    db: Session = Depends(get_db)
):
    """Exportar devoluciones pendientes a Excel"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)
    # En un entorno real, aquí se generaría el archivo Excel
    devoluciones = crud_devoluciones.get_multi_filtered(filtro=filtro, skip=0, limit=10000)
    return {
        "mensaje": "Exportación iniciada",
        "total_registros": len(devoluciones),
        "archivo": "devoluciones_pendientes_export.xlsx",
        "fecha_generacion": datetime.now().isoformat()
    }

@router.get("/reportes/ejecutivo", response_model=Dict[str, Any])
def obtener_reporte_ejecutivo(
    periodo_dias: int = Query(30, ge=1, le=365, description="Período en días para el reporte"),
    db: Session = Depends(get_db)
):
    """Obtener reporte ejecutivo de devoluciones pendientes"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)

    stats_generales = crud_devoluciones.get_estadisticas_generales()
    stats_por_estado = crud_devoluciones.get_estadisticas_por_estado()
    ranking_valor = crud_devoluciones.get_ranking_por_valor(top=5)
    alertas_activas = crud_devoluciones.get_alertas()
    recomendaciones = crud_devoluciones.get_recomendaciones(limite=5)

    return {
        "periodo_analisis": f"{periodo_dias} días",
        "fecha_generacion": datetime.now().isoformat(),
        "resumen_ejecutivo": {
            "total_devoluciones": stats_generales["total_devoluciones"],
            "valor_total_pendiente": stats_generales["total_valor_pendiente"],
            "devoluciones_criticas": stats_generales["devoluciones_vencidas"] + stats_generales["devoluciones_urgentes"],
            "riesgo_financiero": stats_por_estado["vencidas"]["valor_total"] + stats_por_estado["urgentes"]["valor_total"]
        },
        "estadisticas_detalladas": {
            "generales": stats_generales,
            "por_estado": stats_por_estado
        },
        "top_devoluciones_riesgo": ranking_valor,
        "alertas_activas": len([a for a in alertas_activas if a["tipo_alerta"] in ["DEVOLUCION_VENCIDA", "DEVOLUCION_URGENTE"]]),
        "acciones_recomendadas": len(recomendaciones),
        "conclusiones": [
            f"Se identificaron {stats_generales['devoluciones_vencidas']} devoluciones vencidas",
            f"Valor total en riesgo: ${stats_generales['total_valor_pendiente']:,.2f}",
            f"Requieren atención inmediata: {len(recomendaciones)} casos"
        ]
    }

@router.get("/metricas/tiempo-respuesta", response_model=Dict[str, Any])
def obtener_metricas_tiempo_respuesta(db: Session = Depends(get_db)):
    """Obtener métricas de tiempo de respuesta para devoluciones"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)

    todas_devoluciones = crud_devoluciones.get_multi_filtered(skip=0, limit=10000)

    if not todas_devoluciones:
        return {
            "promedio_dias_vencimiento": 0,
            "mediana_dias_vencimiento": 0,
            "devoluciones_en_tiempo": 0,
            "devoluciones_retrasadas": 0,
            "eficiencia_general": 0
        }

    dias_limites = [d.dias_para_limite for d in todas_devoluciones if d.dias_para_limite is not None]
    vencidas = len([d for d in todas_devoluciones if d.esta_vencida])
    en_tiempo = len(todas_devoluciones) - vencidas

    promedio = sum(dias_limites) / len(dias_limites) if dias_limites else 0
    mediana = sorted(dias_limites)[len(dias_limites)//2] if dias_limites else 0
    eficiencia = (en_tiempo / len(todas_devoluciones)) * 100 if todas_devoluciones else 0

    return {
        "promedio_dias_vencimiento": round(promedio, 2),
        "mediana_dias_vencimiento": mediana,
        "devoluciones_en_tiempo": en_tiempo,
        "devoluciones_retrasadas": vencidas,
        "total_evaluado": len(todas_devoluciones),
        "eficiencia_general": round(eficiencia, 2)
    }

@router.get("/analisis/tendencias", response_model=Dict[str, Any])
def obtener_analisis_tendencias(
    dias_analisis: int = Query(90, ge=30, le=365, description="Días para análisis de tendencias"),
    db: Session = Depends(get_db)
):
    """Obtener análisis de tendencias de devoluciones pendientes"""
    crud_devoluciones = DevolucionesPendientesCRUD(db)

    from datetime import date, timedelta
    fecha_inicio = date.today() - timedelta(days=dias_analisis)

    # Filtrar por rango de fechas
    filtro = VistaDevolucionesPendientesFilter(
        fecha_despacho_desde=fecha_inicio,
        fecha_despacho_hasta=date.today()
    )

    devoluciones_periodo = crud_devoluciones.get_multi_filtered(filtro=filtro, skip=0, limit=10000)

    if not devoluciones_periodo:
        return {
            "periodo_analisis": f"{dias_analisis} días",
            "tendencia_general": "Sin datos suficientes",
            "indicadores": {},
            "recomendaciones": ["Ampliar período de análisis"]
        }

    # Análisis de tendencias
    total_valor = sum([float(d.valor_pendiente) for d in devoluciones_periodo])
    promedio_valor = total_valor / len(devoluciones_periodo)
    vencidas_porcentaje = len([d for d in devoluciones_periodo if d.esta_vencida]) / len(devoluciones_periodo) * 100

    # Determinar tendencia
    if vencidas_porcentaje > 30:
        tendencia = "CRITICA"
    elif vencidas_porcentaje > 15:
        tendencia = "PREOCUPANTE"
    else:
        tendencia = "ESTABLE"

    return {
        "periodo_analisis": f"{dias_analisis} días",
        "fecha_inicio_analisis": fecha_inicio.isoformat(),
        "fecha_fin_analisis": date.today().isoformat(),
        "tendencia_general": tendencia,
        "indicadores": {
            "total_devoluciones_periodo": len(devoluciones_periodo),
            "valor_total_pendiente": total_valor,
            "valor_promedio_devolucion": round(promedio_valor, 2),
            "porcentaje_vencidas": round(vencidas_porcentaje, 2),
            "devoluciones_alto_riesgo": len([d for d in devoluciones_periodo if float(d.valor_pendiente) > 50000])
        },
        "recomendaciones": [
            "Implementar seguimiento proactivo" if vencidas_porcentaje > 20 else "Mantener proceso actual",
            "Revisar políticas de devolución" if promedio_valor > 30000 else "Proceso eficiente",
            "Escalar casos críticos" if tendencia == "CRITICA" else "Seguimiento normal"
        ]
    }