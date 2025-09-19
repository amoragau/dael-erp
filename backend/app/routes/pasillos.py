from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import Pasillo, Bodega
from schemas import PasilloCreate, PasilloUpdate, PasilloResponse, PasilloWithBodega
from crud import pasillo_crud, bodega_crud

# Configuración del router
router = APIRouter(
    prefix="/pasillos",
    tags=["Pasillos"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[PasilloResponse])
def listar_pasillos(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    bodega_id: Optional[int] = Query(None, description="Filtrar por bodega"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de pasillos con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo pasillos activos (true) o inactivos (false)
    - **bodega_id**: Filtrar pasillos de una bodega específica
    """
    if bodega_id:
        return pasillo_crud.get_pasillos_by_bodega(db, bodega_id=bodega_id, activo=activo)

    return pasillo_crud.get_pasillos(db, skip=skip, limit=limit, activo=activo)

@router.get("/{pasillo_id}", response_model=PasilloWithBodega)
def obtener_pasillo(
    pasillo_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un pasillo por su ID con información de la bodega"""
    pasillo = db.query(Pasillo).filter(Pasillo.id_pasillo == pasillo_id).first()
    if pasillo is None:
        raise HTTPException(status_code=404, detail="Pasillo no encontrado")
    return pasillo

@router.get("/bodega/{bodega_id}/pasillos", response_model=List[PasilloResponse])
def obtener_pasillos_por_bodega(
    bodega_id: int,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener todos los pasillos de una bodega específica"""
    # Verificar que la bodega existe
    bodega = bodega_crud.get_bodega(db, bodega_id)
    if not bodega:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")

    return pasillo_crud.get_pasillos_by_bodega(db, bodega_id=bodega_id, activo=activo)

@router.post("/", response_model=PasilloResponse, status_code=201)
def crear_pasillo(
    pasillo: PasilloCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo pasillo
    - Requiere que la bodega exista
    - El número de pasillo debe ser único dentro de la bodega
    """
    # Verificar que la bodega existe
    bodega = bodega_crud.get_bodega(db, pasillo.id_bodega)
    if not bodega:
        raise HTTPException(status_code=404, detail="Bodega no encontrada")

    # Verificar que no existe un pasillo con el mismo número en la bodega
    existing_pasillo = db.query(Pasillo).filter(
        Pasillo.id_bodega == pasillo.id_bodega,
        Pasillo.numero_pasillo == pasillo.numero_pasillo
    ).first()

    if existing_pasillo:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe el pasillo número {pasillo.numero_pasillo} en esta bodega"
        )

    return pasillo_crud.create_pasillo(db=db, pasillo=pasillo)

@router.put("/{pasillo_id}", response_model=PasilloResponse)
def actualizar_pasillo(
    pasillo_id: int,
    pasillo_update: PasilloUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar pasillo existente
    - Solo se actualizan los campos proporcionados
    - Si se cambia la bodega, debe existir
    - Si se cambia el número, debe ser único en la bodega
    """
    # Verificar que el pasillo existe
    db_pasillo = pasillo_crud.get_pasillo(db, pasillo_id)
    if not db_pasillo:
        raise HTTPException(status_code=404, detail="Pasillo no encontrado")

    # Si se está actualizando la bodega, verificar que existe
    if pasillo_update.id_bodega and pasillo_update.id_bodega != db_pasillo.id_bodega:
        bodega = bodega_crud.get_bodega(db, pasillo_update.id_bodega)
        if not bodega:
            raise HTTPException(status_code=404, detail="Bodega no encontrada")

    # Si se está actualizando el número de pasillo, verificar unicidad
    if pasillo_update.numero_pasillo:
        bodega_id = pasillo_update.id_bodega or db_pasillo.id_bodega
        numero_pasillo = pasillo_update.numero_pasillo

        # Solo verificar si es diferente al actual
        if numero_pasillo != db_pasillo.numero_pasillo or bodega_id != db_pasillo.id_bodega:
            existing_pasillo = db.query(Pasillo).filter(
                Pasillo.id_bodega == bodega_id,
                Pasillo.numero_pasillo == numero_pasillo,
                Pasillo.id_pasillo != pasillo_id
            ).first()

            if existing_pasillo:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe el pasillo número {numero_pasillo} en esta bodega"
                )

    updated_pasillo = pasillo_crud.update_pasillo(db=db, pasillo_id=pasillo_id, pasillo_update=pasillo_update)
    if not updated_pasillo:
        raise HTTPException(status_code=404, detail="Error al actualizar el pasillo")

    return updated_pasillo

@router.delete("/{pasillo_id}")
def eliminar_pasillo(
    pasillo_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar pasillo (soft delete)
    - Marca el pasillo como inactivo en lugar de eliminarlo físicamente
    """
    success = pasillo_crud.delete_pasillo(db=db, pasillo_id=pasillo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pasillo no encontrado")

    return {"message": "Pasillo eliminado correctamente"}

@router.patch("/{pasillo_id}/toggle", response_model=PasilloResponse)
def toggle_estado_pasillo(
    pasillo_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de un pasillo
    """
    db_pasillo = pasillo_crud.get_pasillo(db, pasillo_id)
    if not db_pasillo:
        raise HTTPException(status_code=404, detail="Pasillo no encontrado")

    # Cambiar el estado
    pasillo_update = PasilloUpdate(activo=not db_pasillo.activo)
    updated_pasillo = pasillo_crud.update_pasillo(db=db, pasillo_id=pasillo_id, pasillo_update=pasillo_update)

    return updated_pasillo

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_pasillos(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    bodega_id: Optional[int] = Query(None, description="Filtrar por bodega"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de pasillos"""
    query = db.query(Pasillo)

    if activo is not None:
        query = query.filter(Pasillo.activo == activo)

    if bodega_id is not None:
        query = query.filter(Pasillo.id_bodega == bodega_id)

    total = query.count()
    return {"total_pasillos": total}

@router.get("/stats/por-bodega")
def estadisticas_por_bodega(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de pasillos por bodega"""
    from sqlalchemy import func

    stats = db.query(
        Bodega.codigo_bodega,
        Bodega.nombre_bodega,
        func.count(Pasillo.id_pasillo).label('total_pasillos'),
        func.sum(func.cast(Pasillo.activo, db.Integer)).label('pasillos_activos'),
        func.avg(Pasillo.longitud_metros).label('longitud_promedio')
    ).outerjoin(Pasillo).group_by(
        Bodega.id_bodega, Bodega.codigo_bodega, Bodega.nombre_bodega
    ).filter(Bodega.activo == True).all()

    return [
        {
            "codigo_bodega": stat.codigo_bodega,
            "nombre_bodega": stat.nombre_bodega,
            "total_pasillos": stat.total_pasillos or 0,
            "pasillos_activos": stat.pasillos_activos or 0,
            "longitud_promedio": float(stat.longitud_promedio or 0)
        }
        for stat in stats
    ]