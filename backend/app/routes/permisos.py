from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import Permisos, Roles
from schemas import PermisoCreate, PermisoUpdate, PermisoResponse, PermisoWithRol
from crud import permiso_crud, roles_crud

# Configuración del router
router = APIRouter(
    prefix="/permisos",
    tags=["Permisos"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[PermisoResponse])
def listar_permisos(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    rol_id: Optional[int] = Query(None, description="Filtrar por rol"),
    modulo: Optional[str] = Query(None, description="Filtrar por módulo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de permisos con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **rol_id**: Filtrar permisos de un rol específico
    - **modulo**: Filtrar permisos de un módulo específico
    """
    if rol_id:
        return permiso_crud.get_permisos_by_rol(db, rol_id=rol_id, modulo=modulo)

    return permiso_crud.get_permisos(db, skip=skip, limit=limit, modulo=modulo)

@router.get("/{permiso_id}", response_model=PermisoWithRol)
def obtener_permiso(
    permiso_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un permiso por su ID con información del rol"""
    permiso = db.query(Permisos).filter(Permisos.id_permiso == permiso_id).first()
    if permiso is None:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return permiso

@router.get("/rol/{rol_id}/permisos", response_model=List[PermisoResponse])
def obtener_permisos_por_rol(
    rol_id: int,
    modulo: Optional[str] = Query(None, description="Filtrar por módulo"),
    db: Session = Depends(get_db)
):
    """Obtener todos los permisos de un rol específico"""
    # Verificar que el rol existe
    rol = roles_crud.get_rol(db, rol_id)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    return permiso_crud.get_permisos_by_rol(db, rol_id=rol_id, modulo=modulo)

@router.post("/", response_model=PermisoResponse, status_code=201)
def crear_permiso(
    permiso: PermisoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo permiso
    - Requiere que el rol exista
    - La combinación rol-módulo debe ser única
    """
    # Verificar que el rol existe
    rol = roles_crud.get_rol(db, permiso.id_rol)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    # Verificar que no existe un permiso con el mismo rol y módulo
    existing_permiso = db.query(Permisos).filter(
        Permisos.id_rol == permiso.id_rol,
        Permisos.modulo == permiso.modulo.upper()
    ).first()

    if existing_permiso:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un permiso para el módulo {permiso.modulo} en este rol"
        )

    return permiso_crud.create_permiso(db=db, permiso=permiso)

@router.put("/{permiso_id}", response_model=PermisoResponse)
def actualizar_permiso(
    permiso_id: int,
    permiso_update: PermisoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar permiso existente
    - Solo se actualizan los campos proporcionados
    - Si se cambia el rol, debe existir
    - Si se cambia el módulo, la combinación rol-módulo debe ser única
    """
    # Verificar que el permiso existe
    db_permiso = permiso_crud.get_permiso(db, permiso_id)
    if not db_permiso:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")

    # Si se está actualizando el rol, verificar que existe
    if permiso_update.id_rol and permiso_update.id_rol != db_permiso.id_rol:
        rol = roles_crud.get_rol(db, permiso_update.id_rol)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

    # Si se está actualizando el módulo, verificar unicidad
    if permiso_update.modulo:
        rol_id = permiso_update.id_rol or db_permiso.id_rol
        modulo = permiso_update.modulo.upper()

        # Solo verificar si es diferente al actual
        if modulo != db_permiso.modulo or rol_id != db_permiso.id_rol:
            existing_permiso = db.query(Permisos).filter(
                Permisos.id_rol == rol_id,
                Permisos.modulo == modulo,
                Permisos.id_permiso != permiso_id
            ).first()

            if existing_permiso:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe un permiso para el módulo {modulo} en este rol"
                )

    updated_permiso = permiso_crud.update_permiso(db=db, permiso_id=permiso_id, permiso_update=permiso_update)
    if not updated_permiso:
        raise HTTPException(status_code=404, detail="Error al actualizar el permiso")

    return updated_permiso

@router.delete("/{permiso_id}")
def eliminar_permiso(
    permiso_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar permiso
    - Elimina físicamente el registro
    """
    success = permiso_crud.delete_permiso(db=db, permiso_id=permiso_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")

    return {"message": "Permiso eliminado correctamente"}

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_permisos(
    rol_id: Optional[int] = Query(None, description="Filtrar por rol"),
    modulo: Optional[str] = Query(None, description="Filtrar por módulo"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de permisos"""
    query = db.query(Permisos)

    if rol_id is not None:
        query = query.filter(Permisos.id_rol == rol_id)

    if modulo is not None:
        query = query.filter(Permisos.modulo == modulo.upper())

    total = query.count()
    return {"total_permisos": total}

@router.get("/stats/por-rol")
def estadisticas_por_rol(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de permisos por rol"""
    from sqlalchemy import func

    stats = db.query(
        Roles.nombre_rol,
        func.count(Permisos.id_permiso).label('total_permisos'),
        func.sum(func.cast(Permisos.crear, db.Integer)).label('permisos_crear'),
        func.sum(func.cast(Permisos.leer, db.Integer)).label('permisos_leer'),
        func.sum(func.cast(Permisos.actualizar, db.Integer)).label('permisos_actualizar'),
        func.sum(func.cast(Permisos.eliminar, db.Integer)).label('permisos_eliminar'),
        func.sum(func.cast(Permisos.autorizar, db.Integer)).label('permisos_autorizar')
    ).outerjoin(Permisos).group_by(
        Roles.id_rol, Roles.nombre_rol
    ).filter(Roles.activo == True).all()

    return [
        {
            "nombre_rol": stat.nombre_rol,
            "total_permisos": stat.total_permisos or 0,
            "permisos_crear": stat.permisos_crear or 0,
            "permisos_leer": stat.permisos_leer or 0,
            "permisos_actualizar": stat.permisos_actualizar or 0,
            "permisos_eliminar": stat.permisos_eliminar or 0,
            "permisos_autorizar": stat.permisos_autorizar or 0
        }
        for stat in stats
    ]