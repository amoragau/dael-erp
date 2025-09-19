from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date

from database import get_db
from models import DespachosObra
from schemas import (
    DespachosObraCreate,
    DespachosObraUpdate,
    DespachosObraResponse,
    DespachosObraWithRelations
)
from crud import despachos_obra_crud

router = APIRouter(
    prefix="/despachos-obra",
    tags=["Despachos de Obra"]
)

@router.post("/", response_model=DespachosObraResponse)
def crear_despacho(
    despacho: DespachosObraCreate,
    db: Session = Depends(get_db)
):
    db_despacho = despachos_obra_crud.get_despacho_by_numero(db, despacho.numero_despacho)
    if db_despacho:
        raise HTTPException(status_code=400, detail="El número de despacho ya existe")

    return despachos_obra_crud.create_despacho(db, despacho)

@router.get("/", response_model=List[DespachosObraResponse])
def listar_despachos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return despachos_obra_crud.get_despachos(db, skip=skip, limit=limit)

@router.get("/con-relaciones", response_model=List[DespachosObraWithRelations])
def listar_despachos_con_relaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return (db.query(DespachosObra)
            .options(joinedload(DespachosObra.obra))
            .offset(skip)
            .limit(limit)
            .all())

@router.get("/{id_despacho}", response_model=DespachosObraWithRelations)
def obtener_despacho(
    id_despacho: int,
    db: Session = Depends(get_db)
):
    despacho = (db.query(DespachosObra)
                .options(joinedload(DespachosObra.obra))
                .filter(DespachosObra.id_despacho == id_despacho)
                .first())
    if not despacho:
        raise HTTPException(status_code=404, detail="Despacho no encontrado")
    return despacho

@router.put("/{id_despacho}", response_model=DespachosObraResponse)
def actualizar_despacho(
    id_despacho: int,
    despacho: DespachosObraUpdate,
    db: Session = Depends(get_db)
):
    db_despacho = despachos_obra_crud.get_despacho(db, id_despacho)
    if not db_despacho:
        raise HTTPException(status_code=404, detail="Despacho no encontrado")

    if despacho.numero_despacho:
        existing = despachos_obra_crud.get_despacho_by_numero(db, despacho.numero_despacho)
        if existing and existing.id_despacho != id_despacho:
            raise HTTPException(status_code=400, detail="El número de despacho ya existe")

    return despachos_obra_crud.update_despacho(db, id_despacho, despacho)

@router.delete("/{id_despacho}")
def eliminar_despacho(
    id_despacho: int,
    db: Session = Depends(get_db)
):
    success = despachos_obra_crud.delete_despacho(db, id_despacho)
    if not success:
        raise HTTPException(status_code=404, detail="Despacho no encontrado")

    return {"message": "Despacho eliminado correctamente"}

@router.get("/numero/{numero_despacho}", response_model=DespachosObraWithRelations)
def obtener_despacho_por_numero(
    numero_despacho: str,
    db: Session = Depends(get_db)
):
    despacho = (db.query(DespachosObra)
                .options(joinedload(DespachosObra.obra))
                .filter(DespachosObra.numero_despacho == numero_despacho)
                .first())
    if not despacho:
        raise HTTPException(status_code=404, detail="Despacho no encontrado")
    return despacho

@router.get("/obra/{id_obra}", response_model=List[DespachosObraResponse])
def listar_despachos_por_obra(
    id_obra: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return despachos_obra_crud.get_despachos_by_obra(db, id_obra=id_obra, skip=skip, limit=limit)

@router.get("/estado/{estado}", response_model=List[DespachosObraResponse])
def listar_despachos_por_estado(
    estado: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    estados_validos = ["PREPARADO", "EN_TRANSITO", "ENTREGADO", "DEVOLUCION_PARCIAL", "DEVOLUCION_COMPLETA", "CERRADO"]
    if estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Estados válidos: {estados_validos}")

    return despachos_obra_crud.get_despachos_by_estado(db, estado=estado, skip=skip, limit=limit)

@router.get("/pendientes/devolucion", response_model=List[DespachosObraWithRelations])
def listar_despachos_pendientes_devolucion(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    despachos = (db.query(DespachosObra)
                .options(joinedload(DespachosObra.obra))
                .filter(
                    DespachosObra.requiere_devolucion == True,
                    DespachosObra.estado.in_(["ENTREGADO", "DEVOLUCION_PARCIAL"]),
                    DespachosObra.fecha_limite_devolucion.isnot(None)
                )
                .offset(skip)
                .limit(limit)
                .all())
    return despachos

@router.get("/vencidos/devolucion", response_model=List[DespachosObraWithRelations])
def listar_despachos_vencidos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    despachos = (db.query(DespachosObra)
                .options(joinedload(DespachosObra.obra))
                .filter(
                    DespachosObra.requiere_devolucion == True,
                    DespachosObra.estado.in_(["ENTREGADO", "DEVOLUCION_PARCIAL"]),
                    DespachosObra.fecha_limite_devolucion < date.today()
                )
                .offset(skip)
                .limit(limit)
                .all())
    return despachos

@router.get("/buscar/{termino}", response_model=List[DespachosObraWithRelations])
def buscar_despachos(
    termino: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    despachos = (db.query(DespachosObra)
                .options(joinedload(DespachosObra.obra))
                .filter(
                    db.or_(
                        DespachosObra.numero_despacho.contains(termino),
                        DespachosObra.transportista.contains(termino),
                        DespachosObra.vehiculo.contains(termino),
                        DespachosObra.chofer.contains(termino),
                        DespachosObra.recibido_por.contains(termino),
                        DespachosObra.motivo_despacho.contains(termino)
                    )
                )
                .offset(skip)
                .limit(limit)
                .all())
    return despachos

@router.patch("/{id_despacho}/estado", response_model=DespachosObraResponse)
def cambiar_estado_despacho(
    id_despacho: int,
    nuevo_estado: str,
    observaciones: Optional[str] = None,
    db: Session = Depends(get_db)
):
    estados_validos = ["PREPARADO", "EN_TRANSITO", "ENTREGADO", "DEVOLUCION_PARCIAL", "DEVOLUCION_COMPLETA", "CERRADO"]
    if nuevo_estado not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Estados válidos: {estados_validos}")

    despacho = despachos_obra_crud.cambiar_estado_despacho(db, id_despacho, nuevo_estado, observaciones)
    if not despacho:
        raise HTTPException(status_code=404, detail="Despacho no encontrado")

    return despacho

@router.get("/estadisticas/general")
def obtener_estadisticas_despachos(db: Session = Depends(get_db)):
    return despachos_obra_crud.get_estadisticas_despachos(db)