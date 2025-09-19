from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import Estante, Pasillo
from schemas import EstanteCreate, EstanteUpdate, EstanteResponse, EstanteWithPasillo
from crud import estante_crud, pasillo_crud

# Configuración del router
router = APIRouter(
    prefix="/estantes",
    tags=["Estantes"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[EstanteResponse])
def listar_estantes(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    pasillo_id: Optional[int] = Query(None, description="Filtrar por pasillo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de estantes con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo estantes activos (true) o inactivos (false)
    - **pasillo_id**: Filtrar estantes de un pasillo específico
    """
    if pasillo_id:
        return estante_crud.get_estantes_by_pasillo(db, pasillo_id=pasillo_id, activo=activo)

    return estante_crud.get_estantes(db, skip=skip, limit=limit, activo=activo)

@router.get("/{estante_id}", response_model=EstanteWithPasillo)
def obtener_estante(
    estante_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un estante por su ID con información del pasillo y bodega"""
    estante = db.query(Estante).filter(Estante.id_estante == estante_id).first()
    if estante is None:
        raise HTTPException(status_code=404, detail="Estante no encontrado")
    return estante

@router.get("/pasillo/{pasillo_id}/estantes", response_model=List[EstanteResponse])
def obtener_estantes_por_pasillo(
    pasillo_id: int,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener todos los estantes de un pasillo específico"""
    # Verificar que el pasillo existe
    pasillo = pasillo_crud.get_pasillo(db, pasillo_id)
    if not pasillo:
        raise HTTPException(status_code=404, detail="Pasillo no encontrado")

    return estante_crud.get_estantes_by_pasillo(db, pasillo_id=pasillo_id, activo=activo)

@router.post("/", response_model=EstanteResponse, status_code=201)
def crear_estante(
    estante: EstanteCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo estante
    - Requiere que el pasillo exista
    - El código de estante debe ser único dentro del pasillo
    """
    # Verificar que el pasillo existe
    pasillo = pasillo_crud.get_pasillo(db, estante.id_pasillo)
    if not pasillo:
        raise HTTPException(status_code=404, detail="Pasillo no encontrado")

    # Verificar que no existe un estante con el mismo código en el pasillo
    existing_estante = db.query(Estante).filter(
        Estante.id_pasillo == estante.id_pasillo,
        Estante.codigo_estante == estante.codigo_estante
    ).first()

    if existing_estante:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un estante con código '{estante.codigo_estante}' en este pasillo"
        )

    return estante_crud.create_estante(db=db, estante=estante)

@router.put("/{estante_id}", response_model=EstanteResponse)
def actualizar_estante(
    estante_id: int,
    estante_update: EstanteUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar estante existente
    - Solo se actualizan los campos proporcionados
    - Si se cambia el pasillo, debe existir
    - Si se cambia el código, debe ser único en el pasillo
    """
    # Verificar que el estante existe
    db_estante = estante_crud.get_estante(db, estante_id)
    if not db_estante:
        raise HTTPException(status_code=404, detail="Estante no encontrado")

    # Si se está actualizando el pasillo, verificar que existe
    if estante_update.id_pasillo and estante_update.id_pasillo != db_estante.id_pasillo:
        pasillo = pasillo_crud.get_pasillo(db, estante_update.id_pasillo)
        if not pasillo:
            raise HTTPException(status_code=404, detail="Pasillo no encontrado")

    # Si se está actualizando el código de estante, verificar unicidad
    if estante_update.codigo_estante:
        pasillo_id = estante_update.id_pasillo or db_estante.id_pasillo
        codigo_estante = estante_update.codigo_estante

        # Solo verificar si es diferente al actual
        if codigo_estante != db_estante.codigo_estante or pasillo_id != db_estante.id_pasillo:
            existing_estante = db.query(Estante).filter(
                Estante.id_pasillo == pasillo_id,
                Estante.codigo_estante == codigo_estante,
                Estante.id_estante != estante_id
            ).first()

            if existing_estante:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe un estante con código '{codigo_estante}' en este pasillo"
                )

    updated_estante = estante_crud.update_estante(db=db, estante_id=estante_id, estante_update=estante_update)
    if not updated_estante:
        raise HTTPException(status_code=404, detail="Error al actualizar el estante")

    return updated_estante

@router.delete("/{estante_id}")
def eliminar_estante(
    estante_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar estante (soft delete)
    - Marca el estante como inactivo en lugar de eliminarlo físicamente
    """
    success = estante_crud.delete_estante(db=db, estante_id=estante_id)
    if not success:
        raise HTTPException(status_code=404, detail="Estante no encontrado")

    return {"message": "Estante eliminado correctamente"}

@router.patch("/{estante_id}/toggle", response_model=EstanteResponse)
def toggle_estado_estante(
    estante_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de un estante
    """
    db_estante = estante_crud.get_estante(db, estante_id)
    if not db_estante:
        raise HTTPException(status_code=404, detail="Estante no encontrado")

    # Cambiar el estado
    estante_update = EstanteUpdate(activo=not db_estante.activo)
    updated_estante = estante_crud.update_estante(db=db, estante_id=estante_id, estante_update=estante_update)

    return updated_estante

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_estantes(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    pasillo_id: Optional[int] = Query(None, description="Filtrar por pasillo"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de estantes"""
    query = db.query(Estante)

    if activo is not None:
        query = query.filter(Estante.activo == activo)

    if pasillo_id is not None:
        query = query.filter(Estante.id_pasillo == pasillo_id)

    total = query.count()
    return {"total_estantes": total}

@router.get("/stats/por-pasillo")
def estadisticas_por_pasillo(
    bodega_id: Optional[int] = Query(None, description="Filtrar por bodega"),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de estantes por pasillo"""
    from sqlalchemy import func
    from models import Bodega

    query = db.query(
        Bodega.codigo_bodega,
        Pasillo.numero_pasillo,
        Pasillo.nombre_pasillo,
        func.count(Estante.id_estante).label('total_estantes'),
        func.sum(func.cast(Estante.activo, db.Integer)).label('estantes_activos'),
        func.avg(Estante.altura_metros).label('altura_promedio'),
        func.sum(Estante.capacidad_peso_kg).label('capacidad_total')
    ).select_from(Bodega).join(Pasillo).outerjoin(Estante).group_by(
        Bodega.id_bodega, Bodega.codigo_bodega, Pasillo.id_pasillo,
        Pasillo.numero_pasillo, Pasillo.nombre_pasillo
    ).filter(
        Bodega.activo == True,
        Pasillo.activo == True
    )

    if bodega_id:
        query = query.filter(Bodega.id_bodega == bodega_id)

    stats = query.all()

    return [
        {
            "codigo_bodega": stat.codigo_bodega,
            "numero_pasillo": stat.numero_pasillo,
            "nombre_pasillo": stat.nombre_pasillo,
            "total_estantes": stat.total_estantes or 0,
            "estantes_activos": stat.estantes_activos or 0,
            "altura_promedio": float(stat.altura_promedio or 0),
            "capacidad_total_kg": float(stat.capacidad_total or 0)
        }
        for stat in stats
    ]

@router.get("/stats/capacidad")
def estadisticas_capacidad(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de capacidad de estantes"""
    from sqlalchemy import func

    stats = db.query(
        func.count(Estante.id_estante).label('total'),
        func.sum(Estante.capacidad_peso_kg).label('capacidad_total'),
        func.avg(Estante.capacidad_peso_kg).label('capacidad_promedio'),
        func.avg(Estante.altura_metros).label('altura_promedio'),
        func.max(Estante.capacidad_peso_kg).label('capacidad_maxima'),
        func.min(Estante.capacidad_peso_kg).label('capacidad_minima')
    ).filter(Estante.activo == True).first()

    return {
        "total_estantes_activos": stats.total or 0,
        "capacidad_total_kg": float(stats.capacidad_total or 0),
        "capacidad_promedio_kg": float(stats.capacidad_promedio or 0),
        "altura_promedio_metros": float(stats.altura_promedio or 0),
        "capacidad_maxima_kg": float(stats.capacidad_maxima or 0),
        "capacidad_minima_kg": float(stats.capacidad_minima or 0)
    }