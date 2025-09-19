from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date

from database import get_db
from models import ProgramacionConteos
from schemas import (
    ProgramacionConteosCreate,
    ProgramacionConteosUpdate,
    ProgramacionConteosResponse,
    ProgramacionConteosWithRelations
)
from crud import programacion_conteos_crud

router = APIRouter(
    prefix="/programacion-conteos",
    tags=["Programación de Conteos"]
)

@router.post("/", response_model=ProgramacionConteosResponse)
def crear_programacion(
    programacion: ProgramacionConteosCreate,
    db: Session = Depends(get_db)
):
    return programacion_conteos_crud.create_programacion(db, programacion)

@router.get("/", response_model=List[ProgramacionConteosResponse])
def listar_programaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return programacion_conteos_crud.get_programaciones(db, skip=skip, limit=limit)

@router.get("/con-relaciones", response_model=List[ProgramacionConteosWithRelations])
def listar_programaciones_con_relaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return (db.query(ProgramacionConteos)
            .options(
                joinedload(ProgramacionConteos.bodega),
                joinedload(ProgramacionConteos.categoria),
                joinedload(ProgramacionConteos.obra)
            )
            .offset(skip)
            .limit(limit)
            .all())

@router.get("/{id_programacion}", response_model=ProgramacionConteosWithRelations)
def obtener_programacion(
    id_programacion: int,
    db: Session = Depends(get_db)
):
    programacion = (db.query(ProgramacionConteos)
                    .options(
                        joinedload(ProgramacionConteos.bodega),
                        joinedload(ProgramacionConteos.categoria),
                        joinedload(ProgramacionConteos.obra)
                    )
                    .filter(ProgramacionConteos.id_programacion == id_programacion)
                    .first())
    if not programacion:
        raise HTTPException(status_code=404, detail="Programación no encontrada")
    return programacion

@router.put("/{id_programacion}", response_model=ProgramacionConteosResponse)
def actualizar_programacion(
    id_programacion: int,
    programacion: ProgramacionConteosUpdate,
    db: Session = Depends(get_db)
):
    db_programacion = programacion_conteos_crud.update_programacion(db, id_programacion, programacion)
    if not db_programacion:
        raise HTTPException(status_code=404, detail="Programación no encontrada")
    return db_programacion

@router.delete("/{id_programacion}")
def eliminar_programacion(
    id_programacion: int,
    db: Session = Depends(get_db)
):
    success = programacion_conteos_crud.delete_programacion(db, id_programacion)
    if not success:
        raise HTTPException(status_code=404, detail="Programación no encontrada")
    return {"message": "Programación eliminada correctamente"}

@router.get("/estado/{estado}", response_model=List[ProgramacionConteosWithRelations])
def listar_programaciones_por_estado(
    estado: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    programaciones = (db.query(ProgramacionConteos)
                      .options(
                          joinedload(ProgramacionConteos.bodega),
                          joinedload(ProgramacionConteos.categoria),
                          joinedload(ProgramacionConteos.obra)
                      )
                      .filter(ProgramacionConteos.estado == estado)
                      .offset(skip)
                      .limit(limit)
                      .all())
    return programaciones

@router.get("/tipo/{tipo}", response_model=List[ProgramacionConteosWithRelations])
def listar_programaciones_por_tipo(
    tipo: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    programaciones = (db.query(ProgramacionConteos)
                      .options(
                          joinedload(ProgramacionConteos.bodega),
                          joinedload(ProgramacionConteos.categoria),
                          joinedload(ProgramacionConteos.obra)
                      )
                      .filter(ProgramacionConteos.tipo_conteo == tipo)
                      .offset(skip)
                      .limit(limit)
                      .all())
    return programaciones

@router.get("/bodega/{id_bodega}", response_model=List[ProgramacionConteosWithRelations])
def listar_programaciones_por_bodega(
    id_bodega: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    programaciones = (db.query(ProgramacionConteos)
                      .options(
                          joinedload(ProgramacionConteos.categoria),
                          joinedload(ProgramacionConteos.obra)
                      )
                      .filter(ProgramacionConteos.id_bodega == id_bodega)
                      .offset(skip)
                      .limit(limit)
                      .all())
    return programaciones

@router.get("/categoria/{id_categoria}", response_model=List[ProgramacionConteosWithRelations])
def listar_programaciones_por_categoria(
    id_categoria: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    programaciones = (db.query(ProgramacionConteos)
                      .options(
                          joinedload(ProgramacionConteos.bodega),
                          joinedload(ProgramacionConteos.obra)
                      )
                      .filter(ProgramacionConteos.id_categoria == id_categoria)
                      .offset(skip)
                      .limit(limit)
                      .all())
    return programaciones

@router.get("/obra/{id_obra}", response_model=List[ProgramacionConteosWithRelations])
def listar_programaciones_por_obra(
    id_obra: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    programaciones = (db.query(ProgramacionConteos)
                      .options(
                          joinedload(ProgramacionConteos.bodega),
                          joinedload(ProgramacionConteos.categoria)
                      )
                      .filter(ProgramacionConteos.id_obra == id_obra)
                      .offset(skip)
                      .limit(limit)
                      .all())
    return programaciones

@router.get("/responsable/{id_usuario}", response_model=List[ProgramacionConteosWithRelations])
def listar_programaciones_por_responsable(
    id_usuario: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    programaciones = (db.query(ProgramacionConteos)
                      .options(
                          joinedload(ProgramacionConteos.bodega),
                          joinedload(ProgramacionConteos.categoria),
                          joinedload(ProgramacionConteos.obra)
                      )
                      .filter(ProgramacionConteos.id_usuario_responsable == id_usuario)
                      .offset(skip)
                      .limit(limit)
                      .all())
    return programaciones

@router.get("/rango-fechas", response_model=List[ProgramacionConteosWithRelations])
def listar_programaciones_por_rango_fechas(
    fecha_inicio: date = Query(..., description="Fecha de inicio del rango"),
    fecha_fin: date = Query(..., description="Fecha de fin del rango"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    programaciones = (db.query(ProgramacionConteos)
                      .options(
                          joinedload(ProgramacionConteos.bodega),
                          joinedload(ProgramacionConteos.categoria),
                          joinedload(ProgramacionConteos.obra)
                      )
                      .filter(
                          ProgramacionConteos.fecha_programada >= fecha_inicio,
                          ProgramacionConteos.fecha_programada <= fecha_fin
                      )
                      .offset(skip)
                      .limit(limit)
                      .all())
    return programaciones

@router.patch("/{id_programacion}/iniciar", response_model=ProgramacionConteosResponse)
def iniciar_conteo(
    id_programacion: int,
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio del conteo"),
    db: Session = Depends(get_db)
):
    programacion = programacion_conteos_crud.iniciar_conteo(db, id_programacion, fecha_inicio)
    if not programacion:
        raise HTTPException(status_code=400, detail="No se puede iniciar el conteo. Verifica el estado de la programación")
    return programacion

@router.patch("/{id_programacion}/completar", response_model=ProgramacionConteosResponse)
def completar_conteo(
    id_programacion: int,
    fecha_fin: Optional[date] = Query(None, description="Fecha de finalización del conteo"),
    observaciones: Optional[str] = Query(None, description="Observaciones del conteo completado"),
    db: Session = Depends(get_db)
):
    programacion = programacion_conteos_crud.completar_conteo(db, id_programacion, fecha_fin, observaciones)
    if not programacion:
        raise HTTPException(status_code=400, detail="No se puede completar el conteo. Verifica el estado de la programación")
    return programacion

@router.patch("/{id_programacion}/cancelar", response_model=ProgramacionConteosResponse)
def cancelar_conteo(
    id_programacion: int,
    motivo: Optional[str] = Query(None, description="Motivo de la cancelación"),
    db: Session = Depends(get_db)
):
    programacion = programacion_conteos_crud.cancelar_conteo(db, id_programacion, motivo)
    if not programacion:
        raise HTTPException(status_code=400, detail="No se puede cancelar el conteo. Verifica el estado de la programación")
    return programacion

@router.get("/pendientes/listar", response_model=List[ProgramacionConteosWithRelations])
def listar_programaciones_pendientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    programaciones = (db.query(ProgramacionConteos)
                      .options(
                          joinedload(ProgramacionConteos.bodega),
                          joinedload(ProgramacionConteos.categoria),
                          joinedload(ProgramacionConteos.obra)
                      )
                      .filter(ProgramacionConteos.estado.in_(["PROGRAMADO", "EN_PROCESO"]))
                      .offset(skip)
                      .limit(limit)
                      .all())
    return programaciones

@router.get("/vencidas/listar", response_model=List[ProgramacionConteosWithRelations])
def listar_programaciones_vencidas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    from datetime import date
    fecha_hoy = date.today()

    programaciones = (db.query(ProgramacionConteos)
                      .options(
                          joinedload(ProgramacionConteos.bodega),
                          joinedload(ProgramacionConteos.categoria),
                          joinedload(ProgramacionConteos.obra)
                      )
                      .filter(
                          ProgramacionConteos.fecha_programada < fecha_hoy,
                          ProgramacionConteos.estado == "PROGRAMADO"
                      )
                      .offset(skip)
                      .limit(limit)
                      .all())
    return programaciones

@router.get("/estadisticas/generales")
def obtener_estadisticas_generales(db: Session = Depends(get_db)):
    return programacion_conteos_crud.get_estadisticas_generales(db)

@router.get("/estadisticas/por-tipo")
def obtener_estadisticas_por_tipo(db: Session = Depends(get_db)):
    return programacion_conteos_crud.get_estadisticas_por_tipo(db)

@router.get("/resumen/pendientes")
def obtener_resumen_pendientes(db: Session = Depends(get_db)):
    pendientes = programacion_conteos_crud.get_programaciones_pendientes(db, limit=1000)
    vencidas = programacion_conteos_crud.get_programaciones_vencidas(db, limit=1000)

    return {
        "total_pendientes": len(pendientes),
        "total_vencidas": len(vencidas),
        "programados": len([p for p in pendientes if p.estado == "PROGRAMADO"]),
        "en_proceso": len([p for p in pendientes if p.estado == "EN_PROCESO"])
    }