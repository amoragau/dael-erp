from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import Categoria
from schemas import CategoriaCreate, CategoriaUpdate, CategoriaResponse

# Configuración del router
router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de categorías con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo categorías activas (true) o inactivas (false)
    """
    query = db.query(Categoria)
    if activo is not None:
        query = query.filter(Categoria.activo == activo)
    return query.offset(skip).limit(limit).all()

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una categoría por su ID"""
    categoria = db.query(Categoria).filter(Categoria.id_categoria == categoria_id).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.get("/codigo/{codigo}", response_model=CategoriaResponse)
def obtener_categoria_por_codigo(
    codigo: str,
    db: Session = Depends(get_db)
):
    """Obtener una categoría por su código"""
    categoria = db.query(Categoria).filter(Categoria.codigo == codigo).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail=f"Categoría con código '{codigo}' no encontrada")
    return categoria

@router.post("/", response_model=CategoriaResponse, status_code=201)
def crear_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva categoría
    - **nombre**: Nombre de la categoría
    - **descripcion**: Descripción opcional
    - **activo**: Estado activo/inactivo
    """
    # Verificar que el código no exista
    existing_categoria = db.query(Categoria).filter(
        Categoria.codigo == categoria.codigo
    ).first()
    if existing_categoria:
        raise HTTPException(status_code=400, detail=f"Ya existe una categoría con código '{categoria.codigo}'")
    
    # Crear nueva categoría
    db_categoria = Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.put("/{categoria_id}", response_model=CategoriaResponse)
def actualizar_categoria(
    categoria_id: int,
    categoria_update: CategoriaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una categoría existente"""
    # Verificar que existe
    db_categoria = db.query(Categoria).filter(
        Categoria.id_categoria == categoria_id
    ).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Si se está actualizando el código, verificar que no exista
    if categoria_update.codigo:
        codigo_exists = db.query(Categoria).filter(
            Categoria.codigo == categoria_update.codigo,
            Categoria.id_categoria != categoria_id
        ).first()
        if codigo_exists:
            raise HTTPException(status_code=400, detail=f"Ya existe una categoría con código '{categoria_update.codigo}'")
    
    # Actualizar campos
    update_data = categoria_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_categoria, field, value)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int,
    permanente: bool = Query(False, description="Eliminación permanente (true) o soft delete (false)"),
    db: Session = Depends(get_db)
):
    """
    Eliminar una categoría
    - **permanente**: Si es true, elimina permanentemente. Si es false, solo marca como inactivo.
    """
    db_categoria = db.query(Categoria).filter(
        Categoria.id_categoria == categoria_id
    ).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    if permanente:
        db.delete(db_categoria)
        message = "Categoría eliminada permanentemente"
    else:
        db_categoria.activo = False
        message = "Categoría desactivada"
    db.commit()
    return {"message": message}

@router.patch("/{categoria_id}/activar")
def activar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db)
):
    """Activar una categoría (cambiar activo = true)"""
    db_categoria = db.query(Categoria).filter(
        Categoria.id_categoria == categoria_id
    ).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    db_categoria.activo = True
    db.commit()
    db.refresh(db_categoria)
    return {"message": "Categoría activada", "categoria": db_categoria}

# ========================================
# ENDPOINTS ADICIONALES
# ========================================

@router.get("/estadisticas/resumen")
def obtener_estadisticas_categorias(db: Session = Depends(get_db)):
    """Obtener estadísticas generales de categorías"""
    total = db.query(Categoria).count()
    activas = db.query(Categoria).filter(Categoria.activo == True).count()
    inactivas = total - activas
    return {
        "total": total,
        "activas": activas,
        "inactivas": inactivas,
        "porcentaje_activas": round((activas / total * 100) if total > 0 else 0, 2)
    }

@router.post("/bulk", response_model=List[CategoriaResponse])
def crear_categorias_masivo(
    categorias: List[CategoriaCreate],
    db: Session = Depends(get_db)
):
    """Crear múltiples categorías de una vez"""
    if len(categorias) > 50:
        raise HTTPException(status_code=400, detail="Máximo 50 categorías por operación masiva")
    
    # Verificar códigos duplicados en la lista
    codigos = [c.codigo for c in categorias]
    if len(codigos) != len(set(codigos)):
        raise HTTPException(status_code=400, detail="Hay códigos duplicados en la lista")
    
    # Verificar códigos existentes en BD
    existing_codes = db.query(Categoria.codigo).filter(
        Categoria.codigo.in_(codigos)
    ).all()
    if existing_codes:
        codes_str = ", ".join([code[0] for code in existing_codes])
        raise HTTPException(status_code=400, detail=f"Los siguientes códigos ya existen: {codes_str}")
    
    # Crear todas las categorías
    db_categorias = []
    for categoria_data in categorias:
        db_categoria = Categoria(**categoria_data.dict())
        db.add(db_categoria)
        db_categorias.append(db_categoria)
    db.commit()
    
    # Refresh todas las categorías
    for db_categoria in db_categorias:
        db.refresh(db_categoria)
    
    return db_categorias