from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import Subcategoria, Categoria  # Asegúrate de que estén definidos en models.py
from schemas import (
    SubcategoriaCreate,
    SubcategoriaUpdate,
    SubcategoriaResponse,
    SubcategoriaWithCategoria
)

# Configuración del router
router = APIRouter(
    prefix="/subcategorias",
    tags=["Subcategorías"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[SubcategoriaResponse])
def listar_subcategorias(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de subcategorías con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo subcategorías activas (true) o inactivas (false)
    """
    query = db.query(Subcategoria)
    if activo is not None:
        query = query.filter(Subcategoria.activo == activo)
    return query.offset(skip).limit(limit).all()

@router.get("/{subcategoria_id}", response_model=SubcategoriaWithCategoria)
def obtener_subcategoria(
    subcategoria_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una subcategoría por su ID"""
    subcategoria = db.query(Subcategoria).filter(Subcategoria.id_subcategoria == subcategoria_id).first()
    if subcategoria is None:
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")
    
    # Incluir detalles de la categoría relacionada
    categoria = db.query(Categoria).filter(Categoria.id_categoria == subcategoria.id_categoria).first()
    subcategoria.categoria = categoria
    
    return subcategoria

@router.get("/codigo/{codigo}", response_model=SubcategoriaWithCategoria)
def obtener_subcategoria_por_codigo(
    codigo: str,
    db: Session = Depends(get_db)
):
    """Obtener una subcategoría por su código"""
    subcategoria = db.query(Subcategoria).filter(Subcategoria.codigo_subcategoria == codigo).first()
    if subcategoria is None:
        raise HTTPException(status_code=404, detail=f"Subcategoría con código '{codigo}' no encontrada")
    
    # Incluir detalles de la categoría relacionada
    categoria = db.query(Categoria).filter(Categoria.id_categoria == subcategoria.id_categoria).first()
    subcategoria.categoria = categoria
    
    return subcategoria

@router.post("/", response_model=SubcategoriaResponse, status_code=201)
def crear_subcategoria(
    subcategoria: SubcategoriaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva subcategoría
    - **id_categoria**: ID de la categoría padre
    - **codigo_subcategoria**: Código único de la subcategoría
    - **nombre_subcategoria**: Nombre de la subcategoría
    - **descripcion**: Descripción opcional
    - **activo**: Estado activo/inactivo
    """
    # Verificar que el código no exista para la misma categoría
    existing_subcategoria = db.query(Subcategoria).filter(
        Subcategoria.id_categoria == subcategoria.id_categoria,
        Subcategoria.codigo_subcategoria == subcategoria.codigo_subcategoria
    ).first()
    if existing_subcategoria:
        raise HTTPException(status_code=400, detail=f"Ya existe una subcategoría con código '{subcategoria.codigo_subcategoria}' en la categoría")
    
    # Crear nueva subcategoría
    db_subcategoria = Subcategoria(**subcategoria.dict())
    db.add(db_subcategoria)
    db.commit()
    db.refresh(db_subcategoria)
    return db_subcategoria

@router.put("/{subcategoria_id}", response_model=SubcategoriaResponse)
def actualizar_subcategoria(
    subcategoria_id: int,
    subcategoria_update: SubcategoriaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una subcategoría existente"""
    # Verificar que existe
    db_subcategoria = db.query(Subcategoria).filter(
        Subcategoria.id_subcategoria == subcategoria_id
    ).first()
    if not db_subcategoria:
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")
    
    # Si se está actualizando el código, verificar que no exista para la misma categoría
    if subcategoria_update.codigo_subcategoria:
        codigo_exists = db.query(Subcategoria).filter(
            Subcategoria.id_categoria == db_subcategoria.id_categoria,
            Subcategoria.codigo_subcategoria == subcategoria_update.codigo_subcategoria,
            Subcategoria.id_subcategoria != subcategoria_id
        ).first()
        if codigo_exists:
            raise HTTPException(status_code=400, detail=f"Ya existe una subcategoría con código '{subcategoria_update.codigo_subcategoria}' en la categoría")
    
    # Actualizar campos
    update_data = subcategoria_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_subcategoria, field, value)
    db.commit()
    db.refresh(db_subcategoria)
    return db_subcategoria

@router.delete("/{subcategoria_id}")
def eliminar_subcategoria(
    subcategoria_id: int,
    permanente: bool = Query(False, description="Eliminación permanente (true) o soft delete (false)"),
    db: Session = Depends(get_db)
):
    """
    Eliminar una subcategoría
    - **permanente**: Si es true, elimina permanentemente. Si es false, solo marca como inactivo.
    """
    db_subcategoria = db.query(Subcategoria).filter(
        Subcategoria.id_subcategoria == subcategoria_id
    ).first()
    if not db_subcategoria:
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")
    
    if permanente:
        db.delete(db_subcategoria)
        message = "Subcategoría eliminada permanentemente"
    else:
        db_subcategoria.activo = False
        message = "Subcategoría desactivada"
    db.commit()
    return {"message": message}

@router.patch("/{subcategoria_id}/activar")
def activar_subcategoria(
    subcategoria_id: int,
    db: Session = Depends(get_db)
):
    """Activar una subcategoría (cambiar activo = true)"""
    db_subcategoria = db.query(Subcategoria).filter(
        Subcategoria.id_subcategoria == subcategoria_id
    ).first()
    if not db_subcategoria:
        raise HTTPException(status_code=404, detail="Subcategoría no encontrada")
    
    db_subcategoria.activo = True
    db.commit()
    db.refresh(db_subcategoria)
    return {"message": "Subcategoría activada", "subcategoria": db_subcategoria}

# ========================================
# ENDPOINTS ADICIONALES
# ========================================

@router.get("/estadisticas/resumen")
def obtener_estadisticas_subcategorias(db: Session = Depends(get_db)):
    """Obtener estadísticas generales de subcategorías"""
    total = db.query(Subcategoria).count()
    activas = db.query(Subcategoria).filter(Subcategoria.activo == True).count()
    inactivas = total - activas
    return {"total": total, "activas": activas, "inactivas": inactivas}

@router.get("/por-categoria/{id_categoria}", response_model=List[SubcategoriaResponse])
def listar_subcategorias_por_categoria(
    id_categoria: int,
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de subcategorías por categoría
    - **id_categoria**: ID de la categoría
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo subcategorías activas (true) o inactivas (false)
    """
    query = db.query(Subcategoria).filter(Subcategoria.id_categoria == id_categoria)
    if activo is not None:
        query = query.filter(Subcategoria.activo == activo)
    return query.offset(skip).limit(limit).all()

@router.post("/bulk", response_model=List[SubcategoriaResponse], status_code=201)
def crear_subcategorias_masivas(
    subcategorias: List[SubcategoriaCreate],
    db: Session = Depends(get_db)
):
    """
    Crear múltiples subcategorías de una vez
    - **subcategorias**: Lista de datos para las subcategorías a crear
    """
    created_subcategorias = []
    for subcategoria_data in subcategorias:
        # Verificar que el código no exista para la misma categoría
        existing_subcategoria = db.query(Subcategoria).filter(
            Subcategoria.id_categoria == subcategoria_data.id_categoria,
            Subcategoria.codigo_subcategoria == subcategoria_data.codigo_subcategoria
        ).first()
        if existing_subcategoria:
            raise HTTPException(status_code=400, detail=f"Ya existe una subcategoría con código '{subcategoria_data.codigo_subcategoria}' en la categoría")
        
        # Crear nueva subcategoría
        db_subcategoria = Subcategoria(**subcategoria_data.dict())
        db.add(db_subcategoria)
        created_subcategorias.append(db_subcategoria)
    
    db.commit()
    for subcategoria in created_subcategorias:
        db.refresh(subcategoria)
    
    return created_subcategorias

# Asegúrate de que los esquemas estén definidos correctamente