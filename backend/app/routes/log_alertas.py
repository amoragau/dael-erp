from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import LogAlertas
from schemas import (
    LogAlertasCreate,
    LogAlertasUpdate,
    LogAlertasResponse,
    LogAlertasWithRelations,
    MarcarVistaRequest,
    ResolverAlertaRequest,
    IgnorarAlertaRequest
)
from crud import log_alertas_crud

router = APIRouter(
    prefix="/log-alertas",
    tags=["Log de Alertas"]
)

@router.post("/", response_model=LogAlertasResponse)
def crear_log_alerta(
    log_alerta: LogAlertasCreate,
    db: Session = Depends(get_db)
):
    return log_alertas_crud.create_log_alerta(db, log_alerta)

@router.get("/", response_model=List[LogAlertasResponse])
def listar_logs_alertas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return log_alertas_crud.get_logs_alertas(db, skip=skip, limit=limit)

@router.get("/con-relaciones", response_model=List[LogAlertasWithRelations])
def listar_logs_con_relaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return (db.query(LogAlertas)
            .options(
                joinedload(LogAlertas.configuracion_alerta),
                joinedload(LogAlertas.producto),
                joinedload(LogAlertas.obra),
                joinedload(LogAlertas.despacho)
            )
            .order_by(LogAlertas.fecha_generacion.desc())
            .offset(skip)
            .limit(limit)
            .all())

@router.get("/{id_log_alerta}", response_model=LogAlertasWithRelations)
def obtener_log_alerta(
    id_log_alerta: int,
    db: Session = Depends(get_db)
):
    log_alerta = (db.query(LogAlertas)
                  .options(
                      joinedload(LogAlertas.configuracion_alerta),
                      joinedload(LogAlertas.producto),
                      joinedload(LogAlertas.obra),
                      joinedload(LogAlertas.despacho)
                  )
                  .filter(LogAlertas.id_log_alerta == id_log_alerta)
                  .first())
    if not log_alerta:
        raise HTTPException(status_code=404, detail="Log de alerta no encontrado")
    return log_alerta

@router.put("/{id_log_alerta}", response_model=LogAlertasResponse)
def actualizar_log_alerta(
    id_log_alerta: int,
    log_alerta: LogAlertasUpdate,
    db: Session = Depends(get_db)
):
    db_log = log_alertas_crud.update_log_alerta(db, id_log_alerta, log_alerta)
    if not db_log:
        raise HTTPException(status_code=404, detail="Log de alerta no encontrado")
    return db_log

@router.delete("/{id_log_alerta}")
def eliminar_log_alerta(
    id_log_alerta: int,
    db: Session = Depends(get_db)
):
    success = log_alertas_crud.delete_log_alerta(db, id_log_alerta)
    if not success:
        raise HTTPException(status_code=404, detail="Log de alerta no encontrado")
    return {"message": "Log de alerta eliminado correctamente"}

@router.get("/configuracion/{id_alerta}", response_model=List[LogAlertasWithRelations])
def listar_logs_por_configuracion(
    id_alerta: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    logs = (db.query(LogAlertas)
            .options(
                joinedload(LogAlertas.producto),
                joinedload(LogAlertas.obra),
                joinedload(LogAlertas.despacho)
            )
            .filter(LogAlertas.id_alerta == id_alerta)
            .order_by(LogAlertas.fecha_generacion.desc())
            .offset(skip)
            .limit(limit)
            .all())
    return logs

@router.get("/estado/{estado}", response_model=List[LogAlertasWithRelations])
def listar_logs_por_estado(
    estado: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    logs = (db.query(LogAlertas)
            .options(
                joinedload(LogAlertas.configuracion_alerta),
                joinedload(LogAlertas.producto),
                joinedload(LogAlertas.obra),
                joinedload(LogAlertas.despacho)
            )
            .filter(LogAlertas.estado == estado)
            .order_by(LogAlertas.fecha_generacion.desc())
            .offset(skip)
            .limit(limit)
            .all())
    return logs

@router.get("/prioridad/{prioridad}", response_model=List[LogAlertasWithRelations])
def listar_logs_por_prioridad(
    prioridad: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    logs = (db.query(LogAlertas)
            .options(
                joinedload(LogAlertas.configuracion_alerta),
                joinedload(LogAlertas.producto),
                joinedload(LogAlertas.obra),
                joinedload(LogAlertas.despacho)
            )
            .filter(LogAlertas.nivel_prioridad == prioridad)
            .order_by(LogAlertas.fecha_generacion.desc())
            .offset(skip)
            .limit(limit)
            .all())
    return logs

@router.get("/producto/{id_producto}", response_model=List[LogAlertasWithRelations])
def listar_logs_por_producto(
    id_producto: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    logs = (db.query(LogAlertas)
            .options(
                joinedload(LogAlertas.configuracion_alerta),
                joinedload(LogAlertas.obra),
                joinedload(LogAlertas.despacho)
            )
            .filter(LogAlertas.id_producto == id_producto)
            .order_by(LogAlertas.fecha_generacion.desc())
            .offset(skip)
            .limit(limit)
            .all())
    return logs

@router.get("/obra/{id_obra}", response_model=List[LogAlertasWithRelations])
def listar_logs_por_obra(
    id_obra: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    logs = (db.query(LogAlertas)
            .options(
                joinedload(LogAlertas.configuracion_alerta),
                joinedload(LogAlertas.producto),
                joinedload(LogAlertas.despacho)
            )
            .filter(LogAlertas.id_obra == id_obra)
            .order_by(LogAlertas.fecha_generacion.desc())
            .offset(skip)
            .limit(limit)
            .all())
    return logs

@router.get("/despacho/{id_despacho}", response_model=List[LogAlertasWithRelations])
def listar_logs_por_despacho(
    id_despacho: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    logs = (db.query(LogAlertas)
            .options(
                joinedload(LogAlertas.configuracion_alerta),
                joinedload(LogAlertas.producto),
                joinedload(LogAlertas.obra)
            )
            .filter(LogAlertas.id_despacho == id_despacho)
            .order_by(LogAlertas.fecha_generacion.desc())
            .offset(skip)
            .limit(limit)
            .all())
    return logs

@router.get("/usuario/{id_usuario}", response_model=List[LogAlertasWithRelations])
def listar_logs_por_usuario_resolucion(
    id_usuario: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    logs = (db.query(LogAlertas)
            .options(
                joinedload(LogAlertas.configuracion_alerta),
                joinedload(LogAlertas.producto),
                joinedload(LogAlertas.obra),
                joinedload(LogAlertas.despacho)
            )
            .filter(LogAlertas.usuario_resolucion == id_usuario)
            .order_by(LogAlertas.fecha_generacion.desc())
            .offset(skip)
            .limit(limit)
            .all())
    return logs

@router.get("/pendientes/listar", response_model=List[LogAlertasWithRelations])
def listar_logs_pendientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    logs = (db.query(LogAlertas)
            .options(
                joinedload(LogAlertas.configuracion_alerta),
                joinedload(LogAlertas.producto),
                joinedload(LogAlertas.obra),
                joinedload(LogAlertas.despacho)
            )
            .filter(LogAlertas.estado == 'PENDIENTE')
            .order_by(LogAlertas.fecha_generacion.desc())
            .offset(skip)
            .limit(limit)
            .all())
    return logs

@router.get("/criticas/listar", response_model=List[LogAlertasWithRelations])
def listar_logs_criticos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    logs = (db.query(LogAlertas)
            .options(
                joinedload(LogAlertas.configuracion_alerta),
                joinedload(LogAlertas.producto),
                joinedload(LogAlertas.obra),
                joinedload(LogAlertas.despacho)
            )
            .filter(LogAlertas.nivel_prioridad == 'CRITICA')
            .order_by(LogAlertas.fecha_generacion.desc())
            .offset(skip)
            .limit(limit)
            .all())
    return logs

@router.get("/sin-resolver/listar", response_model=List[LogAlertasWithRelations])
def listar_logs_sin_resolver(
    horas_limite: int = Query(24, ge=1, description="Horas sin resolver"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    logs = log_alertas_crud.get_logs_sin_resolver(db, horas_limite, skip=skip, limit=limit)
    # Cargar relaciones manualmente
    for log in logs:
        db.refresh(log)
    return logs

@router.get("/rango-fechas", response_model=List[LogAlertasWithRelations])
def listar_logs_por_rango_fechas(
    fecha_inicio: datetime = Query(..., description="Fecha y hora de inicio del rango"),
    fecha_fin: datetime = Query(..., description="Fecha y hora de fin del rango"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    logs = (db.query(LogAlertas)
            .options(
                joinedload(LogAlertas.configuracion_alerta),
                joinedload(LogAlertas.producto),
                joinedload(LogAlertas.obra),
                joinedload(LogAlertas.despacho)
            )
            .filter(
                LogAlertas.fecha_generacion >= fecha_inicio,
                LogAlertas.fecha_generacion <= fecha_fin
            )
            .order_by(LogAlertas.fecha_generacion.desc())
            .offset(skip)
            .limit(limit)
            .all())
    return logs

@router.patch("/{id_log_alerta}/marcar-vista", response_model=LogAlertasResponse)
def marcar_como_vista(
    id_log_alerta: int,
    request: MarcarVistaRequest = Body(default_factory=MarcarVistaRequest),
    db: Session = Depends(get_db)
):
    log_alerta = log_alertas_crud.marcar_como_vista(db, id_log_alerta, request.fecha_visualizacion)
    if not log_alerta:
        raise HTTPException(status_code=404, detail="Log de alerta no encontrado")
    return log_alerta

@router.patch("/{id_log_alerta}/resolver", response_model=LogAlertasResponse)
def resolver_alerta(
    id_log_alerta: int,
    request: ResolverAlertaRequest,
    db: Session = Depends(get_db)
):
    log_alerta = log_alertas_crud.resolver_alerta(
        db,
        id_log_alerta,
        request.usuario_resolucion,
        request.observaciones_resolucion,
        request.fecha_resolucion
    )
    if not log_alerta:
        raise HTTPException(status_code=404, detail="Log de alerta no encontrado")
    return log_alerta

@router.patch("/{id_log_alerta}/ignorar", response_model=LogAlertasResponse)
def ignorar_alerta(
    id_log_alerta: int,
    request: IgnorarAlertaRequest,
    db: Session = Depends(get_db)
):
    log_alerta = log_alertas_crud.ignorar_alerta(
        db,
        id_log_alerta,
        request.usuario_resolucion,
        request.motivo
    )
    if not log_alerta:
        raise HTTPException(status_code=404, detail="Log de alerta no encontrado")
    return log_alerta

@router.patch("/multiples/marcar-vistas")
def marcar_multiples_como_vistas(
    log_ids: List[int] = Body(..., description="Lista de IDs de logs a marcar como vistos"),
    db: Session = Depends(get_db)
):
    count = log_alertas_crud.marcar_multiples_como_vistas(db, log_ids)
    return {"message": f"{count} logs marcados como vistos", "count": count}

@router.patch("/multiples/resolver")
def resolver_multiples_alertas(
    log_ids: List[int] = Body(..., description="Lista de IDs de logs a resolver"),
    usuario_resolucion: int = Body(..., description="ID del usuario que resuelve"),
    observaciones_resolucion: Optional[str] = Body(None, description="Observaciones de resolución"),
    db: Session = Depends(get_db)
):
    count = log_alertas_crud.resolver_multiples_alertas(db, log_ids, usuario_resolucion, observaciones_resolucion)
    return {"message": f"{count} alertas resueltas", "count": count}

@router.get("/buscar/mensaje", response_model=List[LogAlertasWithRelations])
def buscar_logs_por_mensaje(
    q: str = Query(..., min_length=2, description="Texto a buscar en el mensaje"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    logs = log_alertas_crud.buscar_logs(db, q, skip=skip, limit=limit)
    # Cargar relaciones manualmente
    for log in logs:
        db.refresh(log)
    return logs

@router.get("/estadisticas/generales")
def obtener_estadisticas_logs(db: Session = Depends(get_db)):
    return log_alertas_crud.get_estadisticas_logs(db)

@router.get("/estadisticas/configuracion/{id_alerta}")
def obtener_resumen_por_configuracion(
    id_alerta: int,
    db: Session = Depends(get_db)
):
    return log_alertas_crud.get_resumen_por_configuracion(db, id_alerta)

@router.delete("/limpiar/antiguos")
def limpiar_logs_antiguos(
    dias_antiguedad: int = Query(90, ge=1, description="Días de antigüedad para limpiar logs resueltos/ignorados"),
    db: Session = Depends(get_db)
):
    count = log_alertas_crud.limpiar_logs_antiguos(db, dias_antiguedad)
    return {"message": f"{count} logs antiguos eliminados", "count": count}

@router.get("/dashboard/resumen")
def obtener_resumen_dashboard(db: Session = Depends(get_db)):
    """Obtener resumen para dashboard de alertas"""
    estadisticas = log_alertas_crud.get_estadisticas_logs(db)
    logs_criticos_pendientes = log_alertas_crud.get_logs_criticos(db, limit=5)
    logs_sin_resolver = log_alertas_crud.get_logs_sin_resolver(db, 24, limit=10)

    return {
        "estadisticas": estadisticas,
        "alertas_criticas_pendientes": len([log for log in logs_criticos_pendientes if log.estado == 'PENDIENTE']),
        "alertas_sin_resolver_24h": len(logs_sin_resolver),
        "ultimas_criticas": logs_criticos_pendientes[:3],
        "mas_antiguas_sin_resolver": logs_sin_resolver[:5]
    }

@router.get("/analisis/tendencias")
def analizar_tendencias_alertas(
    dias_analisis: int = Query(30, ge=7, le=365, description="Días hacia atrás para analizar"),
    db: Session = Depends(get_db)
):
    """Analizar tendencias de alertas en los últimos días"""
    from datetime import datetime, timedelta
    fecha_inicio = datetime.now() - timedelta(days=dias_analisis)
    fecha_fin = datetime.now()

    logs_periodo = log_alertas_crud.get_logs_by_fecha_range(db, fecha_inicio, fecha_fin, limit=10000)

    # Agrupar por día
    alertas_por_dia = {}
    for log in logs_periodo:
        fecha_str = log.fecha_generacion.date().isoformat()
        if fecha_str not in alertas_por_dia:
            alertas_por_dia[fecha_str] = {"total": 0, "criticas": 0, "resueltas": 0}

        alertas_por_dia[fecha_str]["total"] += 1
        if log.nivel_prioridad == 'CRITICA':
            alertas_por_dia[fecha_str]["criticas"] += 1
        if log.estado == 'RESUELTA':
            alertas_por_dia[fecha_str]["resueltas"] += 1

    return {
        "periodo_analisis": f"{dias_analisis} días",
        "fecha_inicio": fecha_inicio.date(),
        "fecha_fin": fecha_fin.date(),
        "total_alertas": len(logs_periodo),
        "alertas_por_dia": alertas_por_dia,
        "promedio_diario": len(logs_periodo) / dias_analisis if dias_analisis > 0 else 0
    }