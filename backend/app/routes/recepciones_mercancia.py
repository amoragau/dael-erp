from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import schemas, crud

router = APIRouter()

# ========================================
# ENDPOINTS PARA RECEPCIONES DE MERCANCÍA
# ========================================

@router.get("/", response_model=List[schemas.RecepcionMercanciaResponse])
def get_recepciones_mercancia(
    skip: int = 0,
    limit: int = 100,
    id_orden_compra: Optional[int] = Query(None),
    id_usuario_receptor: Optional[int] = Query(None),
    fecha_desde: Optional[str] = Query(None),
    fecha_hasta: Optional[str] = Query(None),
    numero_recepcion: Optional[str] = Query(None),
    numero_factura_proveedor: Optional[str] = Query(None),
    recepcion_completa: Optional[bool] = Query(None),
    activo: Optional[bool] = Query(True),
    db: Session = Depends(get_db)
):
    """Obtener todas las recepciones de mercancía con filtros"""
    filtros = schemas.RecepcionMercanciaFilters(
        id_orden_compra=id_orden_compra,
        id_usuario_receptor=id_usuario_receptor,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        numero_recepcion=numero_recepcion,
        numero_factura_proveedor=numero_factura_proveedor,
        recepcion_completa=recepcion_completa,
        activo=activo
    )
    recepciones = crud.recepcion_mercancia_crud.get_recepciones(db, skip=skip, limit=limit, filtros=filtros)
    return recepciones

@router.get("/{recepcion_id}", response_model=schemas.RecepcionMercanciaCompletaResponse)
def get_recepcion_mercancia(
    recepcion_id: int,
    db: Session = Depends(get_db)
):
    """Obtener recepción de mercancía por ID con detalles"""
    recepcion = crud.recepcion_mercancia_crud.get_recepcion(db, recepcion_id)
    if not recepcion:
        raise HTTPException(status_code=404, detail="Recepción no encontrada")

    # Cargar detalles
    detalles = crud.recepcion_mercancia_detalle_crud.get_detalles_by_recepcion(db, recepcion_id)

    # Crear respuesta completa
    recepcion_response = schemas.RecepcionMercanciaCompletaResponse.model_validate(recepcion)
    recepcion_response.detalles = [schemas.RecepcionMercanciaDetalleResponse.model_validate(detalle) for detalle in detalles]

    return recepcion_response

@router.get("/numero/{numero_recepcion}", response_model=schemas.RecepcionMercanciaResponse)
def get_recepcion_by_numero(
    numero_recepcion: str,
    db: Session = Depends(get_db)
):
    """Obtener recepción de mercancía por número"""
    recepcion = crud.recepcion_mercancia_crud.get_recepcion_by_numero(db, numero_recepcion)
    if not recepcion:
        raise HTTPException(status_code=404, detail="Recepción no encontrada")
    return recepcion

@router.get("/orden/{orden_id}", response_model=List[schemas.RecepcionMercanciaResponse])
def get_recepciones_by_orden(
    orden_id: int,
    db: Session = Depends(get_db)
):
    """Obtener recepciones de mercancía por orden de compra"""
    recepciones = crud.recepcion_mercancia_crud.get_recepciones_by_orden(db, orden_id)
    return recepciones

@router.post("/", response_model=schemas.RecepcionMercanciaResponse)
def create_recepcion_mercancia(
    recepcion: schemas.RecepcionMercanciaCreate,
    db: Session = Depends(get_db)
):
    """Crear nueva recepción de mercancía"""
    try:
        db_recepcion = crud.recepcion_mercancia_crud.create_recepcion(db, recepcion)
        return db_recepcion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/completa/", response_model=schemas.RecepcionMercanciaCompletaResponse)
def create_recepcion_completa(
    recepcion_completa: schemas.RecepcionMercanciaCompleta,
    db: Session = Depends(get_db)
):
    """Crear recepción de mercancía completa con detalles"""
    try:
        # Crear la recepción principal
        db_recepcion = crud.recepcion_mercancia_crud.create_recepcion(db, recepcion_completa.recepcion)

        # Crear los detalles
        detalles_response = []
        for detalle in recepcion_completa.detalles:
            db_detalle = crud.recepcion_mercancia_detalle_crud.create_detalle(db, detalle, db_recepcion.id_recepcion)
            detalles_response.append(schemas.RecepcionMercanciaDetalleResponse.model_validate(db_detalle))

        # Crear respuesta completa
        recepcion_response = schemas.RecepcionMercanciaCompletaResponse.model_validate(db_recepcion)
        recepcion_response.detalles = detalles_response

        return recepcion_response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{recepcion_id}", response_model=schemas.RecepcionMercanciaResponse)
def update_recepcion_mercancia(
    recepcion_id: int,
    recepcion: schemas.RecepcionMercanciaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar recepción de mercancía"""
    try:
        db_recepcion = crud.recepcion_mercancia_crud.update_recepcion(db, recepcion_id, recepcion)
        if not db_recepcion:
            raise HTTPException(status_code=404, detail="Recepción no encontrada")
        return db_recepcion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{recepcion_id}")
def delete_recepcion_mercancia(
    recepcion_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar recepción de mercancía"""
    success = crud.recepcion_mercancia_crud.delete_recepcion(db, recepcion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recepción no encontrada")
    return {"message": "Recepción eliminada correctamente"}

@router.get("/count/", response_model=int)
def count_recepciones_mercancia(
    id_orden_compra: Optional[int] = Query(None),
    id_usuario_receptor: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Contar recepciones de mercancía con filtros"""
    filtros = schemas.RecepcionMercanciaFilters(
        id_orden_compra=id_orden_compra,
        id_usuario_receptor=id_usuario_receptor
    )
    return crud.recepcion_mercancia_crud.count_recepciones(db, filtros)

@router.post("/{recepcion_id}/marcar-completa/", response_model=schemas.RecepcionMercanciaResponse)
def marcar_recepcion_completa(
    recepcion_id: int,
    db: Session = Depends(get_db)
):
    """Marcar recepción como completa"""
    try:
        db_recepcion = crud.recepcion_mercancia_crud.marcar_como_completa(db, recepcion_id)
        if not db_recepcion:
            raise HTTPException(status_code=404, detail="Recepción no encontrada")
        return db_recepcion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========================================
# ENDPOINTS PARA DETALLES DE RECEPCIÓN
# ========================================

@router.get("/{recepcion_id}/detalles/", response_model=List[schemas.RecepcionMercanciaDetalleResponse])
def get_detalles_recepcion(
    recepcion_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalles de una recepción de mercancía"""
    # Verificar que la recepción existe
    recepcion = crud.recepcion_mercancia_crud.get_recepcion(db, recepcion_id)
    if not recepcion:
        raise HTTPException(status_code=404, detail="Recepción no encontrada")

    detalles = crud.recepcion_mercancia_detalle_crud.get_detalles_by_recepcion(db, recepcion_id)
    return detalles

@router.post("/{recepcion_id}/detalles/", response_model=schemas.RecepcionMercanciaDetalleResponse)
def create_detalle_recepcion(
    recepcion_id: int,
    detalle: schemas.RecepcionMercanciaDetalleCreate,
    db: Session = Depends(get_db)
):
    """Crear detalle de recepción de mercancía"""
    try:
        db_detalle = crud.recepcion_mercancia_detalle_crud.create_detalle(db, detalle, recepcion_id)
        return db_detalle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/detalles/{detalle_id}", response_model=schemas.RecepcionMercanciaDetalleResponse)
def get_detalle_recepcion(
    detalle_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalle de recepción por ID"""
    detalle = crud.recepcion_mercancia_detalle_crud.get_detalle(db, detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

@router.put("/detalles/{detalle_id}", response_model=schemas.RecepcionMercanciaDetalleResponse)
def update_detalle_recepcion(
    detalle_id: int,
    detalle: schemas.RecepcionMercanciaDetalleUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar detalle de recepción de mercancía"""
    try:
        db_detalle = crud.recepcion_mercancia_detalle_crud.update_detalle(db, detalle_id, detalle)
        if not db_detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        return db_detalle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/detalles/{detalle_id}")
def delete_detalle_recepcion(
    detalle_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar detalle de recepción de mercancía"""
    success = crud.recepcion_mercancia_detalle_crud.delete_detalle(db, detalle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return {"message": "Detalle eliminado correctamente"}