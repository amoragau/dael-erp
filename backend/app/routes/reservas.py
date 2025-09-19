from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date

from database import get_db
from models import Reservas
from schemas import (
    ReservasCreate,
    ReservasUpdate,
    ReservasResponse,
    ReservasWithRelations
)
from crud import reservas_crud

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)

@router.post("/", response_model=ReservasResponse)
def crear_reserva(
    reserva: ReservasCreate,
    db: Session = Depends(get_db)
):
    return reservas_crud.create_reserva(db, reserva)

@router.get("/", response_model=List[ReservasResponse])
def listar_reservas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return reservas_crud.get_reservas(db, skip=skip, limit=limit)

@router.get("/con-relaciones", response_model=List[ReservasWithRelations])
def listar_reservas_con_relaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return (db.query(Reservas)
            .options(
                joinedload(Reservas.cliente),
                joinedload(Reservas.obra),
                joinedload(Reservas.producto)
            )
            .offset(skip)
            .limit(limit)
            .all())

@router.get("/{id_reserva}", response_model=ReservasWithRelations)
def obtener_reserva(
    id_reserva: int,
    db: Session = Depends(get_db)
):
    reserva = (db.query(Reservas)
               .options(
                   joinedload(Reservas.cliente),
                   joinedload(Reservas.obra),
                   joinedload(Reservas.producto)
               )
               .filter(Reservas.id_reserva == id_reserva)
               .first())
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@router.put("/{id_reserva}", response_model=ReservasResponse)
def actualizar_reserva(
    id_reserva: int,
    reserva: ReservasUpdate,
    db: Session = Depends(get_db)
):
    db_reserva = reservas_crud.update_reserva(db, id_reserva, reserva)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return db_reserva

@router.delete("/{id_reserva}")
def eliminar_reserva(
    id_reserva: int,
    db: Session = Depends(get_db)
):
    success = reservas_crud.delete_reserva(db, id_reserva)
    if not success:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {"message": "Reserva eliminada correctamente"}

@router.get("/cliente/{id_cliente}", response_model=List[ReservasWithRelations])
def listar_reservas_por_cliente(
    id_cliente: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    activas_solo: bool = Query(False, description="Solo reservas activas"),
    db: Session = Depends(get_db)
):
    query = (db.query(Reservas)
             .options(
                 joinedload(Reservas.obra),
                 joinedload(Reservas.producto)
             )
             .filter(Reservas.id_cliente == id_cliente))

    if activas_solo:
        query = query.filter(Reservas.estado == "ACTIVA")

    return query.offset(skip).limit(limit).all()

@router.get("/obra/{id_obra}", response_model=List[ReservasWithRelations])
def listar_reservas_por_obra(
    id_obra: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    activas_solo: bool = Query(False, description="Solo reservas activas"),
    db: Session = Depends(get_db)
):
    query = (db.query(Reservas)
             .options(
                 joinedload(Reservas.cliente),
                 joinedload(Reservas.producto)
             )
             .filter(Reservas.id_obra == id_obra))

    if activas_solo:
        query = query.filter(Reservas.estado == "ACTIVA")

    return query.offset(skip).limit(limit).all()

@router.get("/producto/{id_producto}", response_model=List[ReservasWithRelations])
def listar_reservas_por_producto(
    id_producto: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    activas_solo: bool = Query(False, description="Solo reservas activas"),
    db: Session = Depends(get_db)
):
    query = (db.query(Reservas)
             .options(
                 joinedload(Reservas.cliente),
                 joinedload(Reservas.obra)
             )
             .filter(Reservas.id_producto == id_producto))

    if activas_solo:
        query = query.filter(Reservas.estado == "ACTIVA")

    return query.offset(skip).limit(limit).all()

@router.get("/estado/{estado}", response_model=List[ReservasWithRelations])
def listar_reservas_por_estado(
    estado: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    reservas = (db.query(Reservas)
                .options(
                    joinedload(Reservas.cliente),
                    joinedload(Reservas.obra),
                    joinedload(Reservas.producto)
                )
                .filter(Reservas.estado == estado)
                .offset(skip)
                .limit(limit)
                .all())
    return reservas

@router.get("/vencidas/listar", response_model=List[ReservasWithRelations])
def listar_reservas_vencidas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return reservas_crud.get_reservas_vencidas(db, skip=skip, limit=limit)

@router.patch("/vencidas/marcar")
def marcar_reservas_vencidas(db: Session = Depends(get_db)):
    count = reservas_crud.marcar_vencidas(db)
    return {"message": f"{count} reservas marcadas como vencidas"}

@router.get("/producto/{id_producto}/cantidad-reservada")
def obtener_cantidad_reservada_producto(
    id_producto: int,
    db: Session = Depends(get_db)
):
    cantidad = reservas_crud.get_cantidad_reservada_producto(db, id_producto)
    return {"id_producto": id_producto, "cantidad_reservada": cantidad}

@router.patch("/{id_reserva}/utilizar", response_model=ReservasResponse)
def marcar_reserva_utilizada(
    id_reserva: int,
    cantidad_utilizada: int = Query(..., ge=1, description="Cantidad utilizada de la reserva"),
    observaciones: Optional[str] = Query(None, description="Observaciones del uso"),
    db: Session = Depends(get_db)
):
    reserva = reservas_crud.utilizar_reserva(db, id_reserva, cantidad_utilizada, observaciones)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada o no puede ser utilizada")
    return reserva

@router.patch("/{id_reserva}/cancelar", response_model=ReservasResponse)
def cancelar_reserva(
    id_reserva: int,
    motivo: Optional[str] = Query(None, description="Motivo de la cancelación"),
    db: Session = Depends(get_db)
):
    reserva = reservas_crud.cancelar_reserva(db, id_reserva, motivo)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada o no puede ser cancelada")
    return reserva

@router.get("/externas/listar", response_model=List[ReservasWithRelations])
def listar_reservas_externas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    reservas = (db.query(Reservas)
                .options(joinedload(Reservas.producto))
                .filter(Reservas.cliente_externo.isnot(None))
                .offset(skip)
                .limit(limit)
                .all())
    return reservas

@router.get("/rango-fechas", response_model=List[ReservasWithRelations])
def listar_reservas_por_rango_fechas(
    fecha_inicio: date = Query(..., description="Fecha de inicio del rango"),
    fecha_fin: date = Query(..., description="Fecha de fin del rango"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    reservas = (db.query(Reservas)
                .options(
                    joinedload(Reservas.cliente),
                    joinedload(Reservas.obra),
                    joinedload(Reservas.producto)
                )
                .filter(
                    Reservas.fecha_reserva >= fecha_inicio,
                    Reservas.fecha_reserva <= fecha_fin
                )
                .offset(skip)
                .limit(limit)
                .all())
    return reservas

@router.get("/resumen/general")
def obtener_resumen_reservas(db: Session = Depends(get_db)):
    return reservas_crud.get_resumen_general(db)

@router.get("/estadisticas/por-estado")
def obtener_estadisticas_por_estado(db: Session = Depends(get_db)):
    return reservas_crud.get_estadisticas_por_estado(db)

@router.get("/estadisticas/por-producto")
def obtener_estadisticas_por_producto(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return reservas_crud.get_estadisticas_por_producto(db, skip=skip, limit=limit)