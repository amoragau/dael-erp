from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import Marca
from schemas import MarcaCreate, MarcaUpdate, MarcaResponse
from crud import marca_crud

# Configuración del router
router = APIRouter(
    prefix="/marcas",
    tags=["Marcas"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[MarcaResponse])
def listar_marcas(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de marcas con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo marcas activas (true) o inactivas (false)
    """
    return marca_crud.get_marcas(db, skip=skip, limit=limit, activo=activo)

@router.get("/{marca_id}", response_model=MarcaResponse)
def obtener_marca(
    marca_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una marca por su ID"""
    marca = marca_crud.get_marca(db, marca_id)
    if marca is None:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return marca

@router.get("/nombre/{nombre_marca}", response_model=MarcaResponse)
def obtener_marca_por_nombre(
    nombre_marca: str,
    db: Session = Depends(get_db)
):
    """Obtener una marca por su nombre"""
    marca = marca_crud.get_marca_by_nombre(db, nombre_marca)
    if marca is None:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return marca

@router.post("/", response_model=MarcaResponse, status_code=201)
def crear_marca(
    marca: MarcaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nueva marca
    - Requiere nombre único
    - Todos los campos son opcionales excepto nombre_marca
    """
    # Verificar si ya existe una marca con el mismo nombre
    db_marca = marca_crud.get_marca_by_nombre(db, marca.nombre_marca)
    if db_marca:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una marca con ese nombre"
        )

    return marca_crud.create_marca(db=db, marca=marca)

@router.put("/{marca_id}", response_model=MarcaResponse)
def actualizar_marca(
    marca_id: int,
    marca_update: MarcaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar marca existente
    - Solo se actualizan los campos proporcionados
    - Si se cambia el nombre, debe ser único
    """
    # Verificar que la marca existe
    db_marca = marca_crud.get_marca(db, marca_id)
    if not db_marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    # Si se está actualizando el nombre, verificar que sea único
    if marca_update.nombre_marca and marca_update.nombre_marca != db_marca.nombre_marca:
        existing_marca = marca_crud.get_marca_by_nombre(db, marca_update.nombre_marca)
        if existing_marca:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una marca con ese nombre"
            )

    updated_marca = marca_crud.update_marca(db=db, marca_id=marca_id, marca_update=marca_update)
    if not updated_marca:
        raise HTTPException(status_code=404, detail="Error al actualizar la marca")

    return updated_marca

@router.delete("/{marca_id}")
def eliminar_marca(
    marca_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar marca (soft delete)
    - Marca la marca como inactiva en lugar de eliminarla físicamente
    """
    success = marca_crud.delete_marca(db=db, marca_id=marca_id)
    if not success:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    return {"message": "Marca eliminada correctamente"}

@router.patch("/{marca_id}/toggle", response_model=MarcaResponse)
def toggle_estado_marca(
    marca_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de una marca
    """
    db_marca = marca_crud.get_marca(db, marca_id)
    if not db_marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")

    # Cambiar el estado
    marca_update = MarcaUpdate(activo=not db_marca.activo)
    updated_marca = marca_crud.update_marca(db=db, marca_id=marca_id, marca_update=marca_update)

    return updated_marca

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_marcas(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de marcas"""
    query = db.query(Marca)
    if activo is not None:
        query = query.filter(Marca.activo == activo)

    total = query.count()
    return {"total_marcas": total}