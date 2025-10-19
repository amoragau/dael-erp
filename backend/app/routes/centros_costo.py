"""
API routes for Centros de Costo
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas import CentroCostoCreate, CentroCostoUpdate, CentroCostoResponse
from crud import centros_costo_crud

router = APIRouter(
    prefix="/centros-costo",
    tags=["Centros de Costo"]
)


@router.get("", response_model=List[CentroCostoResponse])
def listar_centros_costo(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Listar todos los centros de costo con paginación opcional
    """
    centros = centros_costo_crud.get_all(db, skip=skip, limit=limit, activo=activo)
    return centros


@router.get("/activos", response_model=List[CentroCostoResponse])
def listar_centros_costo_activos(db: Session = Depends(get_db)):
    """
    Listar todos los centros de costo activos
    """
    centros = centros_costo_crud.get_activos(db)
    return centros


@router.get("/buscar", response_model=List[CentroCostoResponse])
def buscar_centros_costo(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Buscar centros de costo por código o nombre
    """
    centros = centros_costo_crud.search(db, search_term=q, activo=activo)
    return centros


@router.get("/{id_centro_costo}", response_model=CentroCostoResponse)
def obtener_centro_costo(
    id_centro_costo: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un centro de costo por su ID
    """
    centro = centros_costo_crud.get_by_id(db, id_centro_costo)

    if not centro:
        raise HTTPException(
            status_code=404,
            detail=f"Centro de costo con ID {id_centro_costo} no encontrado"
        )

    return centro


@router.post("", response_model=CentroCostoResponse, status_code=201)
def crear_centro_costo(
    centro_costo: CentroCostoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo centro de costo
    """
    # Verificar si el código ya existe
    existing_centro = centros_costo_crud.get_by_codigo(db, centro_costo.codigo_centro_costo)
    if existing_centro:
        raise HTTPException(
            status_code=400,
            detail=f"El código de centro de costo '{centro_costo.codigo_centro_costo}' ya existe"
        )

    # TODO: Obtener usuario_id de la sesión/token
    usuario_id = None

    new_centro = centros_costo_crud.create(db, centro_costo, usuario_id)
    return new_centro


@router.put("/{id_centro_costo}", response_model=CentroCostoResponse)
def actualizar_centro_costo(
    id_centro_costo: int,
    centro_costo: CentroCostoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un centro de costo existente
    """
    # Si se está actualizando el código, verificar que no exista
    if centro_costo.codigo_centro_costo:
        existing_centro = centros_costo_crud.get_by_codigo(db, centro_costo.codigo_centro_costo)
        if existing_centro and existing_centro.id_centro_costo != id_centro_costo:
            raise HTTPException(
                status_code=400,
                detail=f"El código de centro de costo '{centro_costo.codigo_centro_costo}' ya existe"
            )

    # TODO: Obtener usuario_id de la sesión/token
    usuario_id = None

    updated_centro = centros_costo_crud.update(db, id_centro_costo, centro_costo, usuario_id)

    if not updated_centro:
        raise HTTPException(
            status_code=404,
            detail=f"Centro de costo con ID {id_centro_costo} no encontrado"
        )

    return updated_centro


@router.delete("/{id_centro_costo}", response_model=CentroCostoResponse)
def eliminar_centro_costo(
    id_centro_costo: int,
    db: Session = Depends(get_db)
):
    """
    Desactivar un centro de costo (soft delete)
    """
    # TODO: Obtener usuario_id de la sesión/token
    usuario_id = None

    deleted_centro = centros_costo_crud.delete(db, id_centro_costo, usuario_id)

    if not deleted_centro:
        raise HTTPException(
            status_code=404,
            detail=f"Centro de costo con ID {id_centro_costo} no encontrado"
        )

    return deleted_centro
