"""
API routes for Empresas
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas import EmpresaCreate, EmpresaUpdate, EmpresaResponse
from crud import empresas_crud

router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)


@router.get("", response_model=List[EmpresaResponse])
def listar_empresas(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Listar todas las empresas con paginación opcional
    """
    empresas = empresas_crud.get_all(db, skip=skip, limit=limit, activo=activo)
    return empresas


@router.get("/activos", response_model=List[EmpresaResponse])
def listar_empresas_activas(db: Session = Depends(get_db)):
    """
    Listar todas las empresas activas
    """
    empresas = empresas_crud.get_activos(db)
    return empresas


@router.get("/buscar", response_model=List[EmpresaResponse])
def buscar_empresas(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Buscar empresas por RUT o razón social
    """
    empresas = empresas_crud.search(db, search_term=q, activo=activo)
    return empresas


@router.get("/{id_empresa}", response_model=EmpresaResponse)
def obtener_empresa(
    id_empresa: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una empresa por su ID
    """
    empresa = empresas_crud.get_by_id(db, id_empresa)

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail=f"Empresa con ID {id_empresa} no encontrada"
        )

    return empresa


@router.post("", response_model=EmpresaResponse, status_code=201)
def crear_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva empresa
    """
    # Verificar si el RUT ya existe
    existing_empresa = empresas_crud.get_by_rut(db, empresa.rut_empresa)
    if existing_empresa:
        raise HTTPException(
            status_code=400,
            detail=f"El RUT '{empresa.rut_empresa}' ya existe"
        )

    # TODO: Obtener usuario_id de la sesión/token
    usuario_id = None

    new_empresa = empresas_crud.create(db, empresa, usuario_id)
    return new_empresa


@router.put("/{id_empresa}", response_model=EmpresaResponse)
def actualizar_empresa(
    id_empresa: int,
    empresa: EmpresaUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una empresa existente
    """
    # Si se está actualizando el RUT, verificar que no exista
    if empresa.rut_empresa:
        existing_empresa = empresas_crud.get_by_rut(db, empresa.rut_empresa)
        if existing_empresa and existing_empresa.id_empresa != id_empresa:
            raise HTTPException(
                status_code=400,
                detail=f"El RUT '{empresa.rut_empresa}' ya existe"
            )

    # TODO: Obtener usuario_id de la sesión/token
    usuario_id = None

    updated_empresa = empresas_crud.update(db, id_empresa, empresa, usuario_id)

    if not updated_empresa:
        raise HTTPException(
            status_code=404,
            detail=f"Empresa con ID {id_empresa} no encontrada"
        )

    return updated_empresa


@router.delete("/{id_empresa}", response_model=EmpresaResponse)
def eliminar_empresa(
    id_empresa: int,
    db: Session = Depends(get_db)
):
    """
    Desactivar una empresa (soft delete)
    """
    # TODO: Obtener usuario_id de la sesión/token
    usuario_id = None

    deleted_empresa = empresas_crud.delete(db, id_empresa, usuario_id)

    if not deleted_empresa:
        raise HTTPException(
            status_code=404,
            detail=f"Empresa con ID {id_empresa} no encontrada"
        )

    return deleted_empresa
