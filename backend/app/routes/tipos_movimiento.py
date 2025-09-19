# ========================================
# backend/app/routes/unidades_medida.py - VERSIÓN CORREGIDA
# ========================================

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import TipoMovimiento
from schemas import TipoMovimientoCreate, TipoMovimientoUpdate, TipoMovimientoResponse

# Configuración del router
router = APIRouter(
    prefix="/tipos-movimiento",
    tags=["Tipo de Movimiento"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[TipoMovimientoResponse])
def listar_tipos_movimiento(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de tipo de movimiento con paginación
    
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo movimientos activos (true) o inactivas (false)
    """
    query = db.query(TipoMovimiento)
    
    if activo is not None:
        query = query.filter(TipoMovimiento.activo == activo)
        
    movimientos = query.offset(skip).limit(limit).all()
    return movimientos

@router.get("/{movimiento_id}", response_model=TipoMovimientoResponse)
def obtener_tipo_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una tipo de movimiento específico por ID"""
    movimiento = db.query(TipoMovimiento).filter(
        TipoMovimiento.id_tipo_movimiento == movimiento_id
    ).first()
    
    if movimiento is None:
        raise HTTPException(status_code=404, detail="Tipo de movimiento no encontrado")
    return movimiento

@router.get("/codigo/{codigo}", response_model=TipoMovimientoResponse)
def obtener_movimiento_por_codigo(
    codigo: str,
    db: Session = Depends(get_db)
):
    """Obtener una tipo de movimiento por su código"""
    movimiento = db.query(TipoMovimiento).filter(
        TipoMovimiento.codigo_tipo == codigo
    ).first()
    
    if movimiento is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Movimiento con código '{codigo}' no encontrado"
        )
    return movimiento

@router.post("/", response_model=TipoMovimientoResponse, status_code=201)
def crear_tipo_movimiento(
    movimiento: TipoMovimientoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo tipo de movimiento
    
    - **codigo_tipo**: Código único (ej: PZA, KG, MT)
    - **nombre_tipo**: Nombre descriptivo
    - **afecta_stock**: Descripción opcional
    - **requiere_autorizacion**: Descripción opcional
    - **activo**: Estado activo/inactivo
    """
    # Verificar que el código no exista
    existing_movimiento = db.query(TipoMovimiento).filter(
        TipoMovimiento.codigo_tipo == movimiento.codigo_tipo
    ).first()
    
    if existing_movimiento:
        raise HTTPException(
            status_code=400, 
            detail=f"Ya existe un tipo de movimiento con código '{movimiento.codigo_tipo}'"
        )
    
    # Crear nueva unidad
    db_movimiento = TipoMovimiento(**movimiento.dict())
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    return db_movimiento

@router.put("/{movimiento_id}", response_model=TipoMovimientoResponse)
def actualizar_tipo_movimiento(
    movimiento_id: int,
    movimiento_update: TipoMovimientoUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un tipo de movimiento existente"""
    # Verificar que existe
    db_movimiento = db.query(TipoMovimiento).filter(
        TipoMovimiento.id_tipo_movimiento == movimiento_id
    ).first()
    
    if not db_movimiento:
        raise HTTPException(status_code=404, detail="Tipo de movimiento no encontrado")
    
    # Si se está actualizando el código, verificar que no exista
    if movimiento_update.codigo_:
        codigo_exists = db.query(TipoMovimiento).filter(
            TipoMovimiento.codigo_tipo == movimiento_update.codigo_tipo,
            TipoMovimiento.id_tipo_movimiento != movimiento_id
        ).first()
        
        if codigo_exists:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un tipo de movimiento con código '{movimiento_update.codigo_tipo}'"
            )
    
    # Actualizar campos
    update_data = movimiento_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_movimiento, field, value)
    
    db.commit()
    db.refresh(db_movimiento)
    return db_movimiento

@router.delete("/{movimiento_id}")
def eliminar_tipo_movimiento(
    movimiento_id: int,
    permanente: bool = Query(
        False, 
        description="Eliminación permanente (true) o soft delete (false)"
    ),
    db: Session = Depends(get_db)
):
    """
    Eliminar un Tipo de Movimiento
    
    - **permanente**: Si es true, elimina permanentemente. Si es false, solo marca como inactivo.
    """
    db_movimiento = db.query(TipoMovimiento).filter(
        TipoMovimiento.id_tipo_movimiento == movimiento_id
    ).first()
    
    if not db_movimiento:
        raise HTTPException(status_code=404, detail="Tipo de movimiento no encontrado")
    
    if permanente:
        db.delete(db_movimiento)
        message = "Tipo de movimiento eliminado permanentemente"
    else:
        db_movimiento.activo = False
        message = "Tipo de movimiento desactivado"
    
    db.commit()
    return {"message": message}

@router.patch("/{movimiento_id}/activar")
def activar_tipo_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db)
):
    """Activar un Tipo de movimiento (cambiar activo = true)"""
    db_movimiento = db.query(TipoMovimiento).filter(
        TipoMovimiento.id_tipo_movimiento == movimiento_id
    ).first()
    
    if not db_movimiento:
        raise HTTPException(status_code=404, detail="Tipo de movimiento no encontrado")
    
    db_movimiento.activo = True
    db.commit()
    db.refresh(db_movimiento)
    
    return {"message": "Tipo de movimiento activado", "movimiento": db_movimiento}

# ========================================
# ENDPOINTS ADICIONALES
# ========================================

@router.get("/estadisticas/resumen")
def obtener_estadisticas_movimientos(db: Session = Depends(get_db)):
    """Obtener estadísticas generales de Tipos de movimiento"""
    total = db.query(TipoMovimiento).count()
    activas = db.query(TipoMovimiento).filter(TipoMovimiento.activo == True).count()
    inactivas = total - activas
    
    return {
        "total": total,
        "activas": activas,
        "inactivas": inactivas,
        "porcentaje_activas": round((activas / total * 100) if total > 0 else 0, 2)
    }

@router.post("/bulk", response_model=List[TipoMovimientoResponse])
def crear_movimientos_masivo(
    movimientos: List[TipoMovimientoCreate],
    db: Session = Depends(get_db)
):
    """Crear múltiples Tipo de movimiento de una vez"""
    if len(movimientos) > 50:
        raise HTTPException(
            status_code=400, 
            detail="Máximo 50 tipos de movimiento por operación masiva"
        )
    
    # Verificar códigos duplicados en la lista
    codigos = [u.codigo_tipo for u in movimientos]
    if len(codigos) != len(set(codigos)):
        raise HTTPException(
            status_code=400,
            detail="Hay códigos duplicados en la lista"
        )
    
    # Verificar códigos existentes en BD
    existing_codes = db.query(TipoMovimiento.codigo_tipo).filter(
        TipoMovimiento.codigo_tipo.in_(codigos)
    ).all()
    
    if existing_codes:
        codes_str = ", ".join([code[0] for code in existing_codes])
        raise HTTPException(
            status_code=400,
            detail=f"Los siguientes códigos ya existen: {codes_str}"
        )
    
    # Crear todas las unidades
    db_movimientos = []
    for movimiento_data in movimientos:
        db_movimiento = TipoMovimiento(**movimiento_data.dict())
        db.add(db_movimiento)
        db_movimiento.append(db_movimiento)
    
    db.commit()
    
    # Refresh todas las unidades
    for db_movimiento in db_movimientos:
        db.refresh(db_movimiento)
    
    return db_movimientos