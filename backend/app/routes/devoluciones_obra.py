from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date, time

from database import get_db
from models import DevolucionesObra
from schemas import (
    DevolucionesObraCreate,
    DevolucionesObraUpdate,
    DevolucionesObraResponse,
    DevolucionesObraWithRelations
)
from crud import devoluciones_obra_crud

router = APIRouter(
    prefix="/devoluciones-obra",
    tags=["Devoluciones de Obra"]
)

@router.post("/", response_model=DevolucionesObraResponse)
def crear_devolucion(
    devolucion: DevolucionesObraCreate,
    db: Session = Depends(get_db)
):
    db_devolucion = devoluciones_obra_crud.get_devolucion_by_numero(db, devolucion.numero_devolucion)
    if db_devolucion:
        raise HTTPException(status_code=400, detail="El número de devolución ya existe")

    return devoluciones_obra_crud.create_devolucion(db, devolucion)

@router.get("/", response_model=List[DevolucionesObraResponse])
def listar_devoluciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return devoluciones_obra_crud.get_devoluciones(db, skip=skip, limit=limit)

@router.get("/con-relaciones", response_model=List[DevolucionesObraWithRelations])
def listar_devoluciones_con_relaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return (db.query(DevolucionesObra)
            .options(
                joinedload(DevolucionesObra.obra),
                joinedload(DevolucionesObra.despacho),
                joinedload(DevolucionesObra.detalles)
            )
            .offset(skip)
            .limit(limit)
            .all())

@router.get("/{id_devolucion}", response_model=DevolucionesObraWithRelations)
def obtener_devolucion(
    id_devolucion: int,
    db: Session = Depends(get_db)
):
    devolucion = (db.query(DevolucionesObra)
                  .options(
                      joinedload(DevolucionesObra.obra),
                      joinedload(DevolucionesObra.despacho),
                      joinedload(DevolucionesObra.detalles)
                  )
                  .filter(DevolucionesObra.id_devolucion == id_devolucion)
                  .first())
    if not devolucion:
        raise HTTPException(status_code=404, detail="Devolución no encontrada")
    return devolucion

@router.put("/{id_devolucion}", response_model=DevolucionesObraResponse)
def actualizar_devolucion(
    id_devolucion: int,
    devolucion: DevolucionesObraUpdate,
    db: Session = Depends(get_db)
):
    db_devolucion = devoluciones_obra_crud.get_devolucion(db, id_devolucion)
    if not db_devolucion:
        raise HTTPException(status_code=404, detail="Devolución no encontrada")

    if devolucion.numero_devolucion:
        existing = devoluciones_obra_crud.get_devolucion_by_numero(db, devolucion.numero_devolucion)
        if existing and existing.id_devolucion != id_devolucion:
            raise HTTPException(status_code=400, detail="El número de devolución ya existe")

    return devoluciones_obra_crud.update_devolucion(db, id_devolucion, devolucion)

@router.delete("/{id_devolucion}")
def eliminar_devolucion(
    id_devolucion: int,
    db: Session = Depends(get_db)
):
    success = devoluciones_obra_crud.delete_devolucion(db, id_devolucion)
    if not success:
        raise HTTPException(status_code=404, detail="Devolución no encontrada")
    return {"message": "Devolución eliminada correctamente"}

@router.get("/numero/{numero_devolucion}", response_model=DevolucionesObraWithRelations)
def obtener_devolucion_por_numero(
    numero_devolucion: str,
    db: Session = Depends(get_db)
):
    devolucion = (db.query(DevolucionesObra)
                  .options(
                      joinedload(DevolucionesObra.obra),
                      joinedload(DevolucionesObra.despacho),
                      joinedload(DevolucionesObra.detalles)
                  )
                  .filter(DevolucionesObra.numero_devolucion == numero_devolucion)
                  .first())
    if not devolucion:
        raise HTTPException(status_code=404, detail="Devolución no encontrada")
    return devolucion

@router.get("/obra/{id_obra}", response_model=List[DevolucionesObraResponse])
def listar_devoluciones_por_obra(
    id_obra: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return devoluciones_obra_crud.get_devoluciones_by_obra(db, id_obra=id_obra, skip=skip, limit=limit)

@router.get("/despacho/{id_despacho}", response_model=List[DevolucionesObraResponse])
def listar_devoluciones_por_despacho(
    id_despacho: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return devoluciones_obra_crud.get_devoluciones_by_despacho(db, id_despacho=id_despacho, skip=skip, limit=limit)

@router.get("/estado/{estado}", response_model=List[DevolucionesObraResponse])
def listar_devoluciones_por_estado(
    estado: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    estados_validos = ["EN_TRANSITO", "RECIBIDA", "EN_REVISION", "PROCESADA", "RECHAZADA"]
    if estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Estados válidos: {estados_validos}")

    return devoluciones_obra_crud.get_devoluciones_by_estado(db, estado=estado, skip=skip, limit=limit)

@router.get("/motivo/{motivo}", response_model=List[DevolucionesObraResponse])
def listar_devoluciones_por_motivo(
    motivo: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    motivos_validos = ["FIN_OBRA", "SOBRANTE", "CAMBIO_ESPECIFICACION", "DEFECTUOSO", "NO_UTILIZADO", "DEVOLUCION_HERRAMIENTAS"]
    if motivo not in motivos_validos:
        raise HTTPException(status_code=400, detail=f"Motivo inválido. Motivos válidos: {motivos_validos}")

    return devoluciones_obra_crud.get_devoluciones_by_motivo(db, motivo=motivo, skip=skip, limit=limit)

@router.get("/pendientes/recepcion", response_model=List[DevolucionesObraWithRelations])
def listar_devoluciones_pendientes_recepcion(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    devoluciones = (db.query(DevolucionesObra)
                    .options(
                        joinedload(DevolucionesObra.obra),
                        joinedload(DevolucionesObra.despacho),
                        joinedload(DevolucionesObra.detalles)
                    )
                    .filter(DevolucionesObra.estado.in_(["EN_TRANSITO", "RECIBIDA"]))
                    .offset(skip)
                    .limit(limit)
                    .all())
    return devoluciones

@router.get("/buscar/{termino}", response_model=List[DevolucionesObraWithRelations])
def buscar_devoluciones(
    termino: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    devoluciones = (db.query(DevolucionesObra)
                    .options(
                        joinedload(DevolucionesObra.obra),
                        joinedload(DevolucionesObra.despacho),
                        joinedload(DevolucionesObra.detalles)
                    )
                    .filter(
                        db.or_(
                            DevolucionesObra.numero_devolucion.contains(termino),
                            DevolucionesObra.transportista.contains(termino),
                            DevolucionesObra.vehiculo.contains(termino),
                            DevolucionesObra.chofer.contains(termino),
                            DevolucionesObra.entregado_por.contains(termino),
                            DevolucionesObra.observaciones.contains(termino)
                        )
                    )
                    .offset(skip)
                    .limit(limit)
                    .all())
    return devoluciones

@router.patch("/{id_devolucion}/estado", response_model=DevolucionesObraResponse)
def cambiar_estado_devolucion(
    id_devolucion: int,
    nuevo_estado: str,
    observaciones: Optional[str] = None,
    db: Session = Depends(get_db)
):
    estados_validos = ["EN_TRANSITO", "RECIBIDA", "EN_REVISION", "PROCESADA", "RECHAZADA"]
    if nuevo_estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Estados válidos: {estados_validos}")

    devolucion = devoluciones_obra_crud.cambiar_estado_devolucion(db, id_devolucion, nuevo_estado, observaciones)
    if not devolucion:
        raise HTTPException(status_code=404, detail="Devolución no encontrada")

    return devolucion

@router.patch("/{id_devolucion}/recibir", response_model=DevolucionesObraResponse)
def marcar_devolucion_como_recibida(
    id_devolucion: int,
    fecha_recepcion: Optional[date] = Query(None, description="Fecha de recepción (opcional, por defecto hoy)"),
    hora_recepcion: Optional[time] = Query(None, description="Hora de recepción (opcional, por defecto ahora)"),
    db: Session = Depends(get_db)
):
    devolucion = devoluciones_obra_crud.marcar_como_recibida(db, id_devolucion, fecha_recepcion, hora_recepcion)
    if not devolucion:
        raise HTTPException(status_code=404, detail="Devolución no encontrada")

    return devolucion

@router.get("/estadisticas/general")
def obtener_estadisticas_devoluciones(db: Session = Depends(get_db)):
    return devoluciones_obra_crud.get_estadisticas_devoluciones(db)