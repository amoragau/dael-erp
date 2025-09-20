from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import SucursalProveedor, Proveedor
from schemas import (
    SucursalProveedorCreate,
    SucursalProveedorUpdate,
    SucursalProveedorResponse,
    SucursalProveedorWithProveedor
)

# Configuración del router
router = APIRouter(
    prefix="/sucursales-proveedor",
    tags=["Sucursales de Proveedores"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[SucursalProveedorResponse])
def listar_sucursales(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de sucursales con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo sucursales activas (true) o inactivas (false)
    """
    query = db.query(SucursalProveedor)
    if activo is not None:
        query = query.filter(SucursalProveedor.activo == activo)
    return query.offset(skip).limit(limit).all()

@router.get("/{sucursal_id}", response_model=SucursalProveedorWithProveedor)
def obtener_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una sucursal por su ID"""
    sucursal = db.query(SucursalProveedor).filter(SucursalProveedor.id_sucursal == sucursal_id).first()
    if sucursal is None:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")

    # Incluir detalles del proveedor relacionado
    proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == sucursal.id_proveedor).first()
    sucursal.proveedor = proveedor

    return sucursal

@router.get("/proveedor/{proveedor_id}", response_model=List[SucursalProveedorResponse])
def listar_sucursales_por_proveedor(
    proveedor_id: int,
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de sucursales por proveedor
    - **proveedor_id**: ID del proveedor
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo sucursales activas (true) o inactivas (false)
    """
    # Verificar que el proveedor existe
    proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == proveedor_id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    query = db.query(SucursalProveedor).filter(SucursalProveedor.id_proveedor == proveedor_id)
    if activo is not None:
        query = query.filter(SucursalProveedor.activo == activo)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=SucursalProveedorResponse, status_code=201)
def crear_sucursal(
    sucursal: SucursalProveedorCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva sucursal
    - **id_proveedor**: ID del proveedor padre
    - **codigo_sucursal**: Código único de la sucursal para el proveedor
    - **nombre_sucursal**: Nombre de la sucursal
    - **direccion**: Dirección opcional
    - **activo**: Estado activo/inactivo
    """
    # Verificar que el proveedor existe
    proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == sucursal.id_proveedor).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    # Verificar que el código no exista para el mismo proveedor
    existing_sucursal = db.query(SucursalProveedor).filter(
        SucursalProveedor.id_proveedor == sucursal.id_proveedor,
        SucursalProveedor.codigo_sucursal == sucursal.codigo_sucursal
    ).first()
    if existing_sucursal:
        raise HTTPException(status_code=400, detail=f"Ya existe una sucursal con código '{sucursal.codigo_sucursal}' para este proveedor")

    # Crear nueva sucursal
    db_sucursal = SucursalProveedor(**sucursal.dict())
    db.add(db_sucursal)
    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal

@router.put("/{sucursal_id}", response_model=SucursalProveedorResponse)
def actualizar_sucursal(
    sucursal_id: int,
    sucursal_update: SucursalProveedorUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una sucursal existente"""
    # Verificar que existe
    db_sucursal = db.query(SucursalProveedor).filter(
        SucursalProveedor.id_sucursal == sucursal_id
    ).first()
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")

    # Si se está actualizando el código, verificar que no exista para el mismo proveedor
    if sucursal_update.codigo_sucursal:
        codigo_exists = db.query(SucursalProveedor).filter(
            SucursalProveedor.id_proveedor == db_sucursal.id_proveedor,
            SucursalProveedor.codigo_sucursal == sucursal_update.codigo_sucursal,
            SucursalProveedor.id_sucursal != sucursal_id
        ).first()
        if codigo_exists:
            raise HTTPException(status_code=400, detail=f"Ya existe una sucursal con código '{sucursal_update.codigo_sucursal}' para este proveedor")

    # Actualizar campos
    update_data = sucursal_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sucursal, field, value)
    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal

@router.delete("/{sucursal_id}")
def eliminar_sucursal(
    sucursal_id: int,
    permanente: bool = Query(False, description="Eliminación permanente (true) o soft delete (false)"),
    db: Session = Depends(get_db)
):
    """
    Eliminar una sucursal
    - **permanente**: Si es true, elimina permanentemente. Si es false, solo marca como inactivo.
    """
    db_sucursal = db.query(SucursalProveedor).filter(
        SucursalProveedor.id_sucursal == sucursal_id
    ).first()
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")

    if permanente:
        db.delete(db_sucursal)
        message = "Sucursal eliminada permanentemente"
    else:
        db_sucursal.activo = False
        message = "Sucursal desactivada"
    db.commit()
    return {"message": message}

@router.patch("/{sucursal_id}/activar")
def activar_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db)
):
    """Activar una sucursal (cambiar activo = true)"""
    db_sucursal = db.query(SucursalProveedor).filter(
        SucursalProveedor.id_sucursal == sucursal_id
    ).first()
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")

    db_sucursal.activo = True
    db.commit()
    db.refresh(db_sucursal)
    return {"message": "Sucursal activada", "sucursal": db_sucursal}

@router.patch("/{sucursal_id}/principal")
def establecer_sucursal_principal(
    sucursal_id: int,
    db: Session = Depends(get_db)
):
    """Establecer una sucursal como principal (solo una por proveedor)"""
    db_sucursal = db.query(SucursalProveedor).filter(
        SucursalProveedor.id_sucursal == sucursal_id
    ).first()
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")

    # Quitar el estado principal de otras sucursales del mismo proveedor
    db.query(SucursalProveedor).filter(
        SucursalProveedor.id_proveedor == db_sucursal.id_proveedor,
        SucursalProveedor.id_sucursal != sucursal_id
    ).update({"es_sucursal_principal": False})

    # Establecer esta sucursal como principal
    db_sucursal.es_sucursal_principal = True
    db.commit()
    db.refresh(db_sucursal)
    return {"message": "Sucursal establecida como principal", "sucursal": db_sucursal}

# ========================================
# ENDPOINTS ADICIONALES
# ========================================

@router.get("/estadisticas/resumen")
def obtener_estadisticas_sucursales(db: Session = Depends(get_db)):
    """Obtener estadísticas generales de sucursales"""
    total = db.query(SucursalProveedor).count()
    activas = db.query(SucursalProveedor).filter(SucursalProveedor.activo == True).count()
    inactivas = total - activas
    principales = db.query(SucursalProveedor).filter(SucursalProveedor.es_sucursal_principal == True).count()
    return {
        "total": total,
        "activas": activas,
        "inactivas": inactivas,
        "principales": principales,
        "porcentaje_activas": round((activas / total * 100) if total > 0 else 0, 2)
    }