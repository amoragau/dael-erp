# ========================================
# backend/app/routes/unidades_medida.py - VERSIÓN CORREGIDA
# ========================================

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import UnidadMedida
from schemas import UnidadMedidaCreate, UnidadMedidaUpdate, UnidadMedidaResponse

# Configuración del router
router = APIRouter(
    prefix="/unidades-medida",
    tags=["Unidades de Medida"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[UnidadMedidaResponse])
def listar_unidades_medida(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de unidades de medida con paginación
    
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo unidades activas (true) o inactivas (false)
    """
    query = db.query(UnidadMedida)
    
    if activo is not None:
        query = query.filter(UnidadMedida.activo == activo)
        
    unidades = query.offset(skip).limit(limit).all()
    return unidades

@router.get("/{unidad_id}", response_model=UnidadMedidaResponse)
def obtener_unidad_medida(
    unidad_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una unidad de medida específica por ID"""
    unidad = db.query(UnidadMedida).filter(
        UnidadMedida.id_unidad == unidad_id
    ).first()
    
    if unidad is None:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    return unidad

@router.get("/codigo/{codigo}", response_model=UnidadMedidaResponse)
def obtener_unidad_por_codigo(
    codigo: str,
    db: Session = Depends(get_db)
):
    """Obtener una unidad de medida por su código"""
    unidad = db.query(UnidadMedida).filter(
        UnidadMedida.codigo_unidad == codigo
    ).first()
    
    if unidad is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Unidad con código '{codigo}' no encontrada"
        )
    return unidad

@router.post("/", response_model=UnidadMedidaResponse, status_code=201)
def crear_unidad_medida(
    unidad: UnidadMedidaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva unidad de medida
    
    - **codigo_unidad**: Código único (ej: PZA, KG, MT)
    - **nombre_unidad**: Nombre descriptivo
    - **descripcion**: Descripción opcional
    - **activo**: Estado activo/inactivo
    """
    # Verificar que el código no exista
    existing_unidad = db.query(UnidadMedida).filter(
        UnidadMedida.codigo_unidad == unidad.codigo_unidad
    ).first()
    
    if existing_unidad:
        raise HTTPException(
            status_code=400, 
            detail=f"Ya existe una unidad de medida con código '{unidad.codigo_unidad}'"
        )
    
    # Crear nueva unidad
    db_unidad = UnidadMedida(**unidad.dict())
    db.add(db_unidad)
    db.commit()
    db.refresh(db_unidad)
    return db_unidad

@router.put("/{unidad_id}", response_model=UnidadMedidaResponse)
def actualizar_unidad_medida(
    unidad_id: int,
    unidad_update: UnidadMedidaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una unidad de medida existente"""
    # Verificar que existe
    db_unidad = db.query(UnidadMedida).filter(
        UnidadMedida.id_unidad == unidad_id
    ).first()
    
    if not db_unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    
    # Si se está actualizando el código, verificar que no exista
    if unidad_update.codigo_unidad:
        codigo_exists = db.query(UnidadMedida).filter(
            UnidadMedida.codigo_unidad == unidad_update.codigo_unidad,
            UnidadMedida.id_unidad != unidad_id
        ).first()
        
        if codigo_exists:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe una unidad de medida con código '{unidad_update.codigo_unidad}'"
            )
    
    # Actualizar campos
    update_data = unidad_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_unidad, field, value)
    
    db.commit()
    db.refresh(db_unidad)
    return db_unidad

@router.delete("/{unidad_id}")
def eliminar_unidad_medida(
    unidad_id: int,
    permanente: bool = Query(
        False, 
        description="Eliminación permanente (true) o soft delete (false)"
    ),
    db: Session = Depends(get_db)
):
    """
    Eliminar una unidad de medida
    
    - **permanente**: Si es true, elimina permanentemente. Si es false, solo marca como inactivo.
    """
    db_unidad = db.query(UnidadMedida).filter(
        UnidadMedida.id_unidad == unidad_id
    ).first()
    
    if not db_unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    
    if permanente:
        db.delete(db_unidad)
        message = "Unidad de medida eliminada permanentemente"
    else:
        db_unidad.activo = False
        message = "Unidad de medida desactivada"
    
    db.commit()
    return {"message": message}

@router.patch("/{unidad_id}/activar")
def activar_unidad_medida(
    unidad_id: int,
    db: Session = Depends(get_db)
):
    """Activar una unidad de medida (cambiar activo = true)"""
    db_unidad = db.query(UnidadMedida).filter(
        UnidadMedida.id_unidad == unidad_id
    ).first()
    
    if not db_unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    
    db_unidad.activo = True
    db.commit()
    db.refresh(db_unidad)
    
    return {"message": "Unidad de medida activada", "unidad": db_unidad}

# ========================================
# ENDPOINTS ADICIONALES
# ========================================

@router.get("/estadisticas/resumen")
def obtener_estadisticas_unidades(db: Session = Depends(get_db)):
    """Obtener estadísticas generales de unidades de medida"""
    total = db.query(UnidadMedida).count()
    activas = db.query(UnidadMedida).filter(UnidadMedida.activo == True).count()
    inactivas = total - activas
    
    return {
        "total": total,
        "activas": activas,
        "inactivas": inactivas,
        "porcentaje_activas": round((activas / total * 100) if total > 0 else 0, 2)
    }

@router.post("/bulk", response_model=List[UnidadMedidaResponse])
def crear_unidades_masivo(
    unidades: List[UnidadMedidaCreate],
    db: Session = Depends(get_db)
):
    """Crear múltiples unidades de medida de una vez"""
    if len(unidades) > 50:
        raise HTTPException(
            status_code=400, 
            detail="Máximo 50 unidades por operación masiva"
        )
    
    # Verificar códigos duplicados en la lista
    codigos = [u.codigo_unidad for u in unidades]
    if len(codigos) != len(set(codigos)):
        raise HTTPException(
            status_code=400,
            detail="Hay códigos duplicados en la lista"
        )
    
    # Verificar códigos existentes en BD
    existing_codes = db.query(UnidadMedida.codigo_unidad).filter(
        UnidadMedida.codigo_unidad.in_(codigos)
    ).all()
    
    if existing_codes:
        codes_str = ", ".join([code[0] for code in existing_codes])
        raise HTTPException(
            status_code=400,
            detail=f"Los siguientes códigos ya existen: {codes_str}"
        )
    
    # Crear todas las unidades
    db_unidades = []
    for unidad_data in unidades:
        db_unidad = UnidadMedida(**unidad_data.dict())
        db.add(db_unidad)
        db_unidades.append(db_unidad)
    
    db.commit()
    
    # Refresh todas las unidades
    for db_unidad in db_unidades:
        db.refresh(db_unidad)
    
    return db_unidades