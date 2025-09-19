from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import Bodega
from schemas import BodegaCreate, BodegaUpdate, BodegaResponse
from crud import bodega_crud

# Configuración del router
router = APIRouter(
    prefix="/bodegas",
    tags=["Bodegas"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[BodegaResponse])
def listar_bodegas(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de bodegas con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo bodegas activas (true) o inactivas (false)
    """
    return bodega_crud.get_bodegas(db, skip=skip, limit=limit, activo=activo)

@router.get("/{bodega_id}", response_model=BodegaResponse)
def obtener_bodega(
    bodega_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una bodega por su ID"""
    bodega = bodega_crud.get_bodega(db, bodega_id)
    if bodega is None:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    return bodega

@router.get("/codigo/{codigo_bodega}", response_model=BodegaResponse)
def obtener_bodega_por_codigo(
    codigo_bodega: str,
    db: Session = Depends(get_db)
):
    """Obtener una bodega por su código"""
    bodega = bodega_crud.get_bodega_by_codigo(db, codigo_bodega)
    if bodega is None:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")
    return bodega

@router.post("/", response_model=BodegaResponse, status_code=201)
def crear_bodega(
    bodega: BodegaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nueva bodega
    - Requiere código único (A-I)
    - Valida rango de temperaturas si se especifican
    """
    # Verificar si ya existe una bodega con el mismo código
    db_bodega = bodega_crud.get_bodega_by_codigo(db, bodega.codigo_bodega)
    if db_bodega:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una bodega con ese código"
        )

    # Validar rango de temperaturas
    if (bodega.temperatura_min is not None and
        bodega.temperatura_max is not None and
        bodega.temperatura_min > bodega.temperatura_max):
        raise HTTPException(
            status_code=400,
            detail="La temperatura mínima no puede ser mayor que la máxima"
        )

    return bodega_crud.create_bodega(db=db, bodega=bodega)

@router.put("/{bodega_id}", response_model=BodegaResponse)
def actualizar_bodega(
    bodega_id: int,
    bodega_update: BodegaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar bodega existente
    - Solo se actualizan los campos proporcionados
    - Si se cambia el código, debe ser único
    - Valida rango de temperaturas
    """
    # Verificar que la bodega existe
    db_bodega = bodega_crud.get_bodega(db, bodega_id)
    if not db_bodega:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")

    # Si se está actualizando el código, verificar que sea único
    if bodega_update.codigo_bodega and bodega_update.codigo_bodega != db_bodega.codigo_bodega:
        existing_bodega = bodega_crud.get_bodega_by_codigo(db, bodega_update.codigo_bodega)
        if existing_bodega:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una bodega con ese código"
            )

    # Validar rango de temperaturas
    temp_min = bodega_update.temperatura_min if bodega_update.temperatura_min is not None else db_bodega.temperatura_min
    temp_max = bodega_update.temperatura_max if bodega_update.temperatura_max is not None else db_bodega.temperatura_max

    if temp_min is not None and temp_max is not None and temp_min > temp_max:
        raise HTTPException(
            status_code=400,
            detail="La temperatura mínima no puede ser mayor que la máxima"
        )

    updated_bodega = bodega_crud.update_bodega(db=db, bodega_id=bodega_id, bodega_update=bodega_update)
    if not updated_bodega:
        raise HTTPException(status_code=404, detail="Error al actualizar la bodega")

    return updated_bodega

@router.delete("/{bodega_id}")
def eliminar_bodega(
    bodega_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar bodega (soft delete)
    - Marca la bodega como inactiva en lugar de eliminarla físicamente
    """
    success = bodega_crud.delete_bodega(db=db, bodega_id=bodega_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")

    return {"message": "Bodega eliminada correctamente"}

@router.patch("/{bodega_id}/toggle", response_model=BodegaResponse)
def toggle_estado_bodega(
    bodega_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de una bodega
    """
    db_bodega = bodega_crud.get_bodega(db, bodega_id)
    if not db_bodega:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")

    # Cambiar el estado
    bodega_update = BodegaUpdate(activo=not db_bodega.activo)
    updated_bodega = bodega_crud.update_bodega(db=db, bodega_id=bodega_id, bodega_update=bodega_update)

    return updated_bodega

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_bodegas(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de bodegas"""
    query = db.query(Bodega)
    if activo is not None:
        query = query.filter(Bodega.activo == activo)

    total = query.count()
    return {"total_bodegas": total}

@router.get("/stats/condiciones")
def estadisticas_condiciones(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de condiciones ambientales"""
    from sqlalchemy import func

    stats = db.query(
        func.count(Bodega.id_bodega).label('total'),
        func.count(Bodega.temperatura_min).label('con_temp_min'),
        func.count(Bodega.temperatura_max).label('con_temp_max'),
        func.count(Bodega.humedad_max).label('con_humedad'),
        func.sum(func.cast(Bodega.requiere_certificacion, db.Integer)).label('requieren_certificacion'),
        func.avg(Bodega.temperatura_min).label('temp_min_promedio'),
        func.avg(Bodega.temperatura_max).label('temp_max_promedio'),
        func.avg(Bodega.humedad_max).label('humedad_promedio')
    ).filter(Bodega.activo == True).first()

    return {
        "total_bodegas_activas": stats.total or 0,
        "bodegas_con_temperatura_min": stats.con_temp_min or 0,
        "bodegas_con_temperatura_max": stats.con_temp_max or 0,
        "bodegas_con_humedad_max": stats.con_humedad or 0,
        "bodegas_requieren_certificacion": stats.requieren_certificacion or 0,
        "temperatura_min_promedio": float(stats.temp_min_promedio or 0),
        "temperatura_max_promedio": float(stats.temp_max_promedio or 0),
        "humedad_max_promedio": float(stats.humedad_promedio or 0)
    }