from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import Proveedor
from schemas import ProveedorCreate, ProveedorUpdate, ProveedorResponse
from crud import proveedor_crud

# Configuración del router
router = APIRouter(
    prefix="/proveedores",
    tags=["Proveedores"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[ProveedorResponse])
def listar_proveedores(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de proveedores con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo proveedores activos (true) o inactivos (false)
    """
    return proveedor_crud.get_proveedores(db, skip=skip, limit=limit, activo=activo)

@router.get("/search", response_model=List[ProveedorResponse])
def buscar_proveedores(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    db: Session = Depends(get_db)
):
    """
    Buscar proveedores por nombre, código o razón social
    - **q**: Término de búsqueda (busca en nombre, código y razón social)
    """
    return proveedor_crud.search_proveedores(db, search_term=q, skip=skip, limit=limit)

@router.get("/{proveedor_id}", response_model=ProveedorResponse)
def obtener_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un proveedor por su ID"""
    proveedor = proveedor_crud.get_proveedor(db, proveedor_id)
    if proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@router.get("/codigo/{codigo_proveedor}", response_model=ProveedorResponse)
def obtener_proveedor_por_codigo(
    codigo_proveedor: str,
    db: Session = Depends(get_db)
):
    """Obtener un proveedor por su código"""
    proveedor = proveedor_crud.get_proveedor_by_codigo(db, codigo_proveedor)
    if proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@router.get("/rfc/{rfc}", response_model=ProveedorResponse)
def obtener_proveedor_por_rfc(
    rfc: str,
    db: Session = Depends(get_db)
):
    """Obtener un proveedor por su RFC"""
    proveedor = proveedor_crud.get_proveedor_by_rfc(db, rfc)
    if proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

@router.post("/", response_model=ProveedorResponse, status_code=201)
def crear_proveedor(
    proveedor: ProveedorCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo proveedor
    - Requiere código único
    - El RFC debe ser único si se proporciona
    """
    # Verificar si ya existe un proveedor con el mismo código
    db_proveedor = proveedor_crud.get_proveedor_by_codigo(db, proveedor.codigo_proveedor)
    if db_proveedor:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un proveedor con ese código"
        )

    # Verificar RFC único si se proporciona
    if proveedor.rfc:
        db_proveedor_rfc = proveedor_crud.get_proveedor_by_rfc(db, proveedor.rfc)
        if db_proveedor_rfc:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un proveedor con ese RFC"
            )

    return proveedor_crud.create_proveedor(db=db, proveedor=proveedor)

@router.put("/{proveedor_id}", response_model=ProveedorResponse)
def actualizar_proveedor(
    proveedor_id: int,
    proveedor_update: ProveedorUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar proveedor existente
    - Solo se actualizan los campos proporcionados
    - Si se cambia el código, debe ser único
    - Si se cambia el RFC, debe ser único
    """
    # Verificar que el proveedor existe
    db_proveedor = proveedor_crud.get_proveedor(db, proveedor_id)
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    # Si se está actualizando el código, verificar que sea único
    if proveedor_update.codigo_proveedor and proveedor_update.codigo_proveedor != db_proveedor.codigo_proveedor:
        existing_proveedor = proveedor_crud.get_proveedor_by_codigo(db, proveedor_update.codigo_proveedor)
        if existing_proveedor:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un proveedor con ese código"
            )

    # Si se está actualizando el RFC, verificar que sea único
    if proveedor_update.rfc and proveedor_update.rfc != db_proveedor.rfc:
        existing_proveedor_rfc = proveedor_crud.get_proveedor_by_rfc(db, proveedor_update.rfc)
        if existing_proveedor_rfc:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un proveedor con ese RFC"
            )

    updated_proveedor = proveedor_crud.update_proveedor(db=db, proveedor_id=proveedor_id, proveedor_update=proveedor_update)
    if not updated_proveedor:
        raise HTTPException(status_code=404, detail="Error al actualizar el proveedor")

    return updated_proveedor

@router.delete("/{proveedor_id}")
def eliminar_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar proveedor (soft delete)
    - Marca el proveedor como inactivo en lugar de eliminarlo físicamente
    """
    success = proveedor_crud.delete_proveedor(db=db, proveedor_id=proveedor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    return {"message": "Proveedor eliminado correctamente"}

@router.patch("/{proveedor_id}/toggle", response_model=ProveedorResponse)
def toggle_estado_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de un proveedor
    """
    db_proveedor = proveedor_crud.get_proveedor(db, proveedor_id)
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    # Cambiar el estado
    proveedor_update = ProveedorUpdate(activo=not db_proveedor.activo)
    updated_proveedor = proveedor_crud.update_proveedor(db=db, proveedor_id=proveedor_id, proveedor_update=proveedor_update)

    return updated_proveedor

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_proveedores(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de proveedores"""
    query = db.query(Proveedor)
    if activo is not None:
        query = query.filter(Proveedor.activo == activo)

    total = query.count()
    return {"total_proveedores": total}

@router.get("/stats/credito")
def estadisticas_credito(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de crédito de proveedores"""
    from sqlalchemy import func

    # Obtener estadísticas básicas
    stats = db.query(
        func.count(Proveedor.id_proveedor).label('total'),
        func.sum(Proveedor.limite_credito).label('limite_total'),
        func.avg(Proveedor.limite_credito).label('limite_promedio'),
        func.avg(Proveedor.dias_credito).label('dias_promedio'),
        func.avg(Proveedor.descuento_general).label('descuento_promedio')
    ).filter(Proveedor.activo == True).first()

    # Proveedores con crédito
    con_credito = db.query(func.count(Proveedor.id_proveedor)).filter(
        Proveedor.activo == True,
        Proveedor.limite_credito > 0
    ).scalar()

    return {
        "total_proveedores_activos": stats.total or 0,
        "proveedores_con_credito": con_credito or 0,
        "limite_credito_total": float(stats.limite_total or 0),
        "limite_credito_promedio": float(stats.limite_promedio or 0),
        "dias_credito_promedio": float(stats.dias_promedio or 0),
        "descuento_promedio": float(stats.descuento_promedio or 0)
    }