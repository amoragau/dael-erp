from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas, crud

router = APIRouter()

@router.get("/", response_model=List[schemas.EstadoOrdenCompraResponse])
def get_estados_orden_compra(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los estados de orden de compra"""
    estados = crud.estado_orden_compra_crud.get_estados(db, skip=skip, limit=limit)
    return estados

@router.get("/{estado_id}", response_model=schemas.EstadoOrdenCompraResponse)
def get_estado_orden_compra(
    estado_id: int,
    db: Session = Depends(get_db)
):
    """Obtener estado de orden de compra por ID"""
    estado = crud.estado_orden_compra_crud.get_estado(db, estado_id)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return estado

@router.get("/codigo/{codigo_estado}", response_model=schemas.EstadoOrdenCompraResponse)
def get_estado_by_codigo(
    codigo_estado: str,
    db: Session = Depends(get_db)
):
    """Obtener estado de orden de compra por código"""
    estado = crud.estado_orden_compra_crud.get_estado_by_codigo(db, codigo_estado)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return estado

@router.get("/inicial/", response_model=schemas.EstadoOrdenCompraResponse)
def get_estado_inicial(db: Session = Depends(get_db)):
    """Obtener estado inicial de orden de compra"""
    estado = crud.estado_orden_compra_crud.get_estado_inicial(db)
    if not estado:
        raise HTTPException(status_code=404, detail="No hay estado inicial configurado")
    return estado

@router.get("/finales/", response_model=List[schemas.EstadoOrdenCompraResponse])
def get_estados_finales(db: Session = Depends(get_db)):
    """Obtener estados finales de orden de compra"""
    estados = crud.estado_orden_compra_crud.get_estados_finales(db)
    return estados

@router.post("/", response_model=schemas.EstadoOrdenCompraResponse)
def create_estado_orden_compra(
    estado: schemas.EstadoOrdenCompraCreate,
    db: Session = Depends(get_db)
):
    """Crear nuevo estado de orden de compra"""
    try:
        db_estado = crud.estado_orden_compra_crud.create_estado(db, estado)
        return db_estado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{estado_id}", response_model=schemas.EstadoOrdenCompraResponse)
def update_estado_orden_compra(
    estado_id: int,
    estado: schemas.EstadoOrdenCompraUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar estado de orden de compra"""
    try:
        db_estado = crud.estado_orden_compra_crud.update_estado(db, estado_id, estado)
        if not db_estado:
            raise HTTPException(status_code=404, detail="Estado no encontrado")
        return db_estado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{estado_id}")
def delete_estado_orden_compra(
    estado_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar estado de orden de compra"""
    success = crud.estado_orden_compra_crud.delete_estado(db, estado_id)
    if not success:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return {"message": "Estado eliminado correctamente"}

@router.get("/count/", response_model=int)
def count_estados_orden_compra(db: Session = Depends(get_db)):
    """Contar estados de orden de compra activos"""
    return crud.estado_orden_compra_crud.count_estados(db)

@router.post("/validar-transicion/")
def validar_transicion_estado(
    estado_origen_id: int,
    estado_destino_id: int,
    db: Session = Depends(get_db)
):
    """Validar si es posible la transición entre estados"""
    es_valida = crud.estado_orden_compra_crud.validate_transicion(db, estado_origen_id, estado_destino_id)
    return {
        "transicion_valida": es_valida,
        "estado_origen_id": estado_origen_id,
        "estado_destino_id": estado_destino_id
    }