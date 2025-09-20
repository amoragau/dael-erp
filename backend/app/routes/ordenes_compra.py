from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import schemas, crud

router = APIRouter()

# ========================================
# ENDPOINTS PARA ÓRDENES DE COMPRA
# ========================================

@router.get("/", response_model=List[schemas.OrdenCompraResponse])
def get_ordenes_compra(
    skip: int = 0,
    limit: int = 100,
    id_proveedor: Optional[int] = Query(None),
    id_estado: Optional[int] = Query(None),
    fecha_desde: Optional[str] = Query(None),
    fecha_hasta: Optional[str] = Query(None),
    numero_orden: Optional[str] = Query(None),
    total_minimo: Optional[float] = Query(None),
    total_maximo: Optional[float] = Query(None),
    activo: Optional[bool] = Query(True),
    db: Session = Depends(get_db)
):
    """Obtener todas las órdenes de compra con filtros"""
    filtros = schemas.OrdenCompraFilters(
        id_proveedor=id_proveedor,
        id_estado=id_estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        numero_orden=numero_orden,
        total_minimo=total_minimo,
        total_maximo=total_maximo,
        activo=activo
    )
    ordenes = crud.orden_compra_crud.get_ordenes(db, skip=skip, limit=limit, filtros=filtros)
    return ordenes

@router.get("/{orden_id}", response_model=schemas.OrdenCompraCompletaResponse)
def get_orden_compra(
    orden_id: int,
    db: Session = Depends(get_db)
):
    """Obtener orden de compra por ID con detalles"""
    orden = crud.orden_compra_crud.get_orden(db, orden_id)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    # Cargar detalles
    detalles = crud.orden_compra_detalle_crud.get_detalles_by_orden(db, orden_id)

    # Crear respuesta completa
    orden_response = schemas.OrdenCompraCompletaResponse.model_validate(orden)
    orden_response.detalles = [schemas.OrdenCompraDetalleResponse.model_validate(detalle) for detalle in detalles]

    return orden_response

@router.get("/numero/{numero_orden}", response_model=schemas.OrdenCompraResponse)
def get_orden_by_numero(
    numero_orden: str,
    db: Session = Depends(get_db)
):
    """Obtener orden de compra por número"""
    orden = crud.orden_compra_crud.get_orden_by_numero(db, numero_orden)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return orden

@router.post("/", response_model=schemas.OrdenCompraResponse)
def create_orden_compra(
    orden: schemas.OrdenCompraCreate,
    db: Session = Depends(get_db)
):
    """Crear nueva orden de compra"""
    try:
        db_orden = crud.orden_compra_crud.create_orden(db, orden)
        return db_orden
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/completa/", response_model=schemas.OrdenCompraCompletaResponse)
def create_orden_completa(
    orden_completa: schemas.OrdenCompraCompleta,
    db: Session = Depends(get_db)
):
    """Crear orden de compra completa con detalles"""
    try:
        # Crear la orden principal
        db_orden = crud.orden_compra_crud.create_orden(db, orden_completa.orden)

        # Crear los detalles
        detalles_response = []
        for detalle in orden_completa.detalles:
            db_detalle = crud.orden_compra_detalle_crud.create_detalle(db, detalle, db_orden.id_orden_compra)
            detalles_response.append(schemas.OrdenCompraDetalleResponse.model_validate(db_detalle))

        # Crear respuesta completa
        orden_response = schemas.OrdenCompraCompletaResponse.model_validate(db_orden)
        orden_response.detalles = detalles_response

        return orden_response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{orden_id}", response_model=schemas.OrdenCompraResponse)
def update_orden_compra(
    orden_id: int,
    orden: schemas.OrdenCompraUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar orden de compra"""
    try:
        db_orden = crud.orden_compra_crud.update_orden(db, orden_id, orden)
        if not db_orden:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        return db_orden
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{orden_id}")
def delete_orden_compra(
    orden_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar orden de compra"""
    success = crud.orden_compra_crud.delete_orden(db, orden_id)
    if not success:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return {"message": "Orden eliminada correctamente"}

@router.get("/count/", response_model=int)
def count_ordenes_compra(
    id_proveedor: Optional[int] = Query(None),
    id_estado: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Contar órdenes de compra con filtros"""
    filtros = schemas.OrdenCompraFilters(
        id_proveedor=id_proveedor,
        id_estado=id_estado
    )
    return crud.orden_compra_crud.count_ordenes(db, filtros)

@router.post("/{orden_id}/aprobar/", response_model=schemas.OrdenCompraResponse)
def aprobar_orden(
    orden_id: int,
    usuario_aprobador_id: int,
    db: Session = Depends(get_db)
):
    """Aprobar orden de compra"""
    try:
        db_orden = crud.orden_compra_crud.aprobar_orden(db, orden_id, usuario_aprobador_id)
        if not db_orden:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        return db_orden
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{orden_id}/cancelar/", response_model=schemas.OrdenCompraResponse)
def cancelar_orden(
    orden_id: int,
    motivo: str,
    db: Session = Depends(get_db)
):
    """Cancelar orden de compra"""
    try:
        db_orden = crud.orden_compra_crud.cancelar_orden(db, orden_id, motivo)
        if not db_orden:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        return db_orden
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ========================================
# ENDPOINTS PARA DETALLES DE ORDEN
# ========================================

@router.get("/{orden_id}/detalles/", response_model=List[schemas.OrdenCompraDetalleResponse])
def get_detalles_orden(
    orden_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalles de una orden de compra"""
    # Verificar que la orden existe
    orden = crud.orden_compra_crud.get_orden(db, orden_id)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    detalles = crud.orden_compra_detalle_crud.get_detalles_by_orden(db, orden_id)
    return detalles

@router.post("/{orden_id}/detalles/", response_model=schemas.OrdenCompraDetalleResponse)
def create_detalle_orden(
    orden_id: int,
    detalle: schemas.OrdenCompraDetalleCreate,
    db: Session = Depends(get_db)
):
    """Crear detalle de orden de compra"""
    try:
        db_detalle = crud.orden_compra_detalle_crud.create_detalle(db, detalle, orden_id)
        return db_detalle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/detalles/{detalle_id}", response_model=schemas.OrdenCompraDetalleResponse)
def get_detalle_orden(
    detalle_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalle de orden por ID"""
    detalle = crud.orden_compra_detalle_crud.get_detalle(db, detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

@router.put("/detalles/{detalle_id}", response_model=schemas.OrdenCompraDetalleResponse)
def update_detalle_orden(
    detalle_id: int,
    detalle: schemas.OrdenCompraDetalleUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar detalle de orden de compra"""
    try:
        db_detalle = crud.orden_compra_detalle_crud.update_detalle(db, detalle_id, detalle)
        if not db_detalle:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        return db_detalle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/detalles/{detalle_id}")
def delete_detalle_orden(
    detalle_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar detalle de orden de compra"""
    success = crud.orden_compra_detalle_crud.delete_detalle(db, detalle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return {"message": "Detalle eliminado correctamente"}