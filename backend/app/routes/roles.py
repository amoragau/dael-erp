from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Roles
from schemas import (
    RolesCreate,
    RolesUpdate,
    RolesResponse
)
from crud import roles_crud

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

@router.post("/", response_model=RolesResponse)
def crear_rol(
    rol: RolesCreate,
    db: Session = Depends(get_db)
):
    try:
        return roles_crud.create_rol(db, rol)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[RolesResponse])
def listar_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return roles_crud.get_roles(db, skip=skip, limit=limit)

@router.get("/{id_rol}", response_model=RolesResponse)
def obtener_rol(
    id_rol: int,
    db: Session = Depends(get_db)
):
    rol = roles_crud.get_rol(db, id_rol)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.put("/{id_rol}", response_model=RolesResponse)
def actualizar_rol(
    id_rol: int,
    rol: RolesUpdate,
    db: Session = Depends(get_db)
):
    try:
        db_rol = roles_crud.update_rol(db, id_rol, rol)
        if not db_rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return db_rol
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_rol}")
def eliminar_rol(
    id_rol: int,
    db: Session = Depends(get_db)
):
    success = roles_crud.delete_rol(db, id_rol)
    if not success:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"message": "Rol eliminado correctamente"}

@router.get("/nombre/{nombre_rol}", response_model=RolesResponse)
def obtener_rol_por_nombre(
    nombre_rol: str,
    db: Session = Depends(get_db)
):
    rol = roles_crud.get_rol_by_nombre(db, nombre_rol)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.get("/activos/listar", response_model=List[RolesResponse])
def listar_roles_activos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return roles_crud.get_roles_activos(db, skip=skip, limit=limit)

@router.patch("/{id_rol}/activar", response_model=RolesResponse)
def activar_rol(
    id_rol: int,
    db: Session = Depends(get_db)
):
    rol = roles_crud.activar_rol(db, id_rol)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.patch("/{id_rol}/desactivar", response_model=RolesResponse)
def desactivar_rol(
    id_rol: int,
    db: Session = Depends(get_db)
):
    rol = roles_crud.desactivar_rol(db, id_rol)
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.get("/buscar/texto", response_model=List[RolesResponse])
def buscar_roles(
    q: str = Query(..., min_length=2, description="Texto a buscar en nombre o descripción"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return roles_crud.buscar_roles(db, q, skip=skip, limit=limit)

@router.get("/ordenados/listar", response_model=List[RolesResponse])
def listar_roles_ordenados(
    campo_orden: str = Query("nombre_rol", description="Campo por el que ordenar: nombre_rol, activo, id_rol"),
    ascendente: bool = Query(True, description="True para orden ascendente, False para descendente"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return roles_crud.get_roles_ordenados(db, campo_orden, ascendente, skip=skip, limit=limit)

@router.post("/{id_rol}/duplicar", response_model=RolesResponse)
def duplicar_rol(
    id_rol: int,
    nuevo_nombre: str = Query(..., description="Nombre para el nuevo rol"),
    db: Session = Depends(get_db)
):
    try:
        nuevo_rol = roles_crud.duplicar_rol(db, id_rol, nuevo_nombre)
        if not nuevo_rol:
            raise HTTPException(status_code=404, detail="Rol original no encontrado")
        return nuevo_rol
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/validar/nombre-unico")
def validar_nombre_unico(
    nombre_rol: str = Query(..., description="Nombre del rol a validar"),
    excluir_id: Optional[int] = Query(None, description="ID del rol a excluir de la validación"),
    db: Session = Depends(get_db)
):
    es_unico = roles_crud.validar_nombre_unico(db, nombre_rol, excluir_id)
    return {
        "nombre_rol": nombre_rol,
        "es_unico": es_unico,
        "mensaje": "Nombre disponible" if es_unico else "Nombre ya está en uso"
    }

@router.get("/estadisticas/general")
def obtener_estadisticas_roles(db: Session = Depends(get_db)):
    return roles_crud.get_estadisticas_roles(db)

@router.get("/resumen/configuracion")
def obtener_resumen_configuracion(db: Session = Depends(get_db)):
    """Obtener resumen de la configuración de roles"""
    estadisticas = roles_crud.get_estadisticas_roles(db)
    roles_activos = roles_crud.get_roles_activos(db, limit=1000)

    # Roles más comunes (esto podría extenderse con relaciones a usuarios)
    return {
        **estadisticas,
        "roles_disponibles": [{"id": rol.id_rol, "nombre": rol.nombre_rol} for rol in roles_activos],
        "total_roles_disponibles": len(roles_activos)
    }