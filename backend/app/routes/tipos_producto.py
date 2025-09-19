from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import TipoProducto, Subcategoria
from schemas import (
    TipoProductoCreate,
    TipoProductoUpdate,
    TipoProductoResponse,
    TipoProductoWithSubcategoria
)
from crud import tipo_producto_crud

router = APIRouter(
    prefix="/tipos-producto",
    tags=["Tipos de Producto"],
    responses={404: {"description": "No encontrado"}}
)

@router.get("/", response_model=List[TipoProductoResponse])
def listar_tipos_producto(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de tipos de producto con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo tipos activos (true) o inactivos (false)
    """
    return tipo_producto_crud.get_tipos_productos(db, skip=skip, limit=limit, activo=activo)

@router.get("/{tipo_producto_id}", response_model=TipoProductoWithSubcategoria)
def obtener_tipo_producto(
    tipo_producto_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un tipo de producto por su ID"""
    tipo_producto = tipo_producto_crud.get_tipo_producto(db, tipo_producto_id)
    if tipo_producto is None:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    
    subcategoria = db.query(Subcategoria).filter(Subcategoria.id_subcategoria == tipo_producto.id_subcategoria).first()
    tipo_producto.subcategoria = subcategoria
    
    return tipo_producto

@router.get("/codigo/{codigo}", response_model=TipoProductoWithSubcategoria)
def obtener_tipo_producto_por_codigo(
    codigo: str,
    db: Session = Depends(get_db)
):
    """Obtener un tipo de producto por su código"""
    tipo_producto = tipo_producto_crud.get_tipo_producto_by_codigo(db, codigo)
    if tipo_producto is None:
        raise HTTPException(status_code=404, detail=f"Tipo de producto con código '{codigo}' no encontrado")
    
    subcategoria = db.query(Subcategoria).filter(Subcategoria.id_subcategoria == tipo_producto.id_subcategoria).first()
    tipo_producto.subcategoria = subcategoria
    
    return tipo_producto

@router.post("/", response_model=TipoProductoResponse, status_code=201)
def crear_tipo_producto(
    tipo_producto: TipoProductoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo tipo de producto
    - **id_subcategoria**: ID de la subcategoría
    - **codigo_tipo**: Código único del tipo de producto
    - **nombre_tipo**: Nombre del tipo de producto
    - **descripcion**: Descripción opcional
    - **activo**: Estado activo/inactivo
    """
    # Verificar que la subcategoría existe
    subcategoria = db.query(Subcategoria).filter(Subcategoria.id_subcategoria == tipo_producto.id_subcategoria).first()
    if not subcategoria:
        raise HTTPException(status_code=400, detail="La subcategoría especificada no existe")
    
    # Verificar que el código no exista para la misma subcategoría
    existing_tipo = db.query(TipoProducto).filter(
        TipoProducto.id_subcategoria == tipo_producto.id_subcategoria,
        TipoProducto.codigo_tipo == tipo_producto.codigo_tipo
    ).first()
    if existing_tipo:
        raise HTTPException(status_code=400, detail=f"Ya existe un tipo de producto con código '{tipo_producto.codigo_tipo}' en la subcategoría")
    
    return tipo_producto_crud.create_tipo_producto(db, tipo_producto)

@router.put("/{tipo_producto_id}", response_model=TipoProductoResponse)
def actualizar_tipo_producto(
    tipo_producto_id: int,
    tipo_producto_update: TipoProductoUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un tipo de producto existente"""
    # Verificar que existe
    db_tipo_producto = tipo_producto_crud.get_tipo_producto(db, tipo_producto_id)
    if not db_tipo_producto:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    
    # Si se está actualizando la subcategoría, verificar que existe
    if tipo_producto_update.id_subcategoria:
        subcategoria = db.query(Subcategoria).filter(Subcategoria.id_subcategoria == tipo_producto_update.id_subcategoria).first()
        if not subcategoria:
            raise HTTPException(status_code=400, detail="La subcategoría especificada no existe")
    
    # Si se está actualizando el código, verificar que no exista para la misma subcategoría
    if tipo_producto_update.codigo_tipo:
        subcategoria_id = tipo_producto_update.id_subcategoria or db_tipo_producto.id_subcategoria
        codigo_exists = db.query(TipoProducto).filter(
            TipoProducto.id_subcategoria == subcategoria_id,
            TipoProducto.codigo_tipo == tipo_producto_update.codigo_tipo,
            TipoProducto.id_tipo_producto != tipo_producto_id
        ).first()
        if codigo_exists:
            raise HTTPException(status_code=400, detail=f"Ya existe un tipo de producto con código '{tipo_producto_update.codigo_tipo}' en la subcategoría")
    
    result = tipo_producto_crud.update_tipo_producto(db, tipo_producto_id, tipo_producto_update)
    if not result:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    return result

@router.delete("/{tipo_producto_id}")
def eliminar_tipo_producto(
    tipo_producto_id: int,
    permanente: bool = Query(False, description="Eliminación permanente (true) o soft delete (false)"),
    db: Session = Depends(get_db)
):
    """
    Eliminar un tipo de producto
    - **permanente**: Si es true, elimina permanentemente. Si es false, solo marca como inactivo.
    """
    db_tipo_producto = tipo_producto_crud.get_tipo_producto(db, tipo_producto_id)
    if not db_tipo_producto:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    
    if permanente:
        db.delete(db_tipo_producto)
        message = "Tipo de producto eliminado permanentemente"
    else:
        success = tipo_producto_crud.delete_tipo_producto(db, tipo_producto_id)
        if not success:
            raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
        message = "Tipo de producto desactivado"
    
    db.commit()
    return {"message": message}

@router.patch("/{tipo_producto_id}/activar")
def activar_tipo_producto(
    tipo_producto_id: int,
    db: Session = Depends(get_db)
):
    """Activar un tipo de producto (cambiar activo = true)"""
    db_tipo_producto = tipo_producto_crud.get_tipo_producto(db, tipo_producto_id)
    if not db_tipo_producto:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")
    
    db_tipo_producto.activo = True
    db.commit()
    db.refresh(db_tipo_producto)
    return {"message": "Tipo de producto activado", "tipo_producto": db_tipo_producto}

@router.get("/estadisticas/resumen")
def obtener_estadisticas_tipos_producto(db: Session = Depends(get_db)):
    """Obtener estadísticas generales de tipos de producto"""
    total = db.query(TipoProducto).count()
    activos = db.query(TipoProducto).filter(TipoProducto.activo == True).count()
    inactivos = total - activos
    return {"total": total, "activos": activos, "inactivos": inactivos}

@router.get("/por-subcategoria/{id_subcategoria}", response_model=List[TipoProductoResponse])
def listar_tipos_producto_por_subcategoria(
    id_subcategoria: int,
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de tipos de producto por subcategoría
    - **id_subcategoria**: ID de la subcategoría
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo tipos activos (true) o inactivos (false)
    """
    query = db.query(TipoProducto).filter(TipoProducto.id_subcategoria == id_subcategoria)
    if activo is not None:
        query = query.filter(TipoProducto.activo == activo)
    return query.offset(skip).limit(limit).all()

@router.post("/bulk", response_model=List[TipoProductoResponse], status_code=201)
def crear_tipos_producto_masivos(
    tipos_producto: List[TipoProductoCreate],
    db: Session = Depends(get_db)
):
    """
    Crear múltiples tipos de producto de una vez
    - **tipos_producto**: Lista de datos para los tipos de producto a crear
    """
    created_tipos = []
    for tipo_data in tipos_producto:
        # Verificar que la subcategoría existe
        subcategoria = db.query(Subcategoria).filter(Subcategoria.id_subcategoria == tipo_data.id_subcategoria).first()
        if not subcategoria:
            raise HTTPException(status_code=400, detail=f"La subcategoría {tipo_data.id_subcategoria} no existe")
        
        # Verificar que el código no exista para la misma subcategoría
        existing_tipo = db.query(TipoProducto).filter(
            TipoProducto.id_subcategoria == tipo_data.id_subcategoria,
            TipoProducto.codigo_tipo == tipo_data.codigo_tipo
        ).first()
        if existing_tipo:
            raise HTTPException(status_code=400, detail=f"Ya existe un tipo de producto con código '{tipo_data.codigo_tipo}' en la subcategoría")
        
        # Crear nuevo tipo de producto
        db_tipo = TipoProducto(**tipo_data.dict())
        db.add(db_tipo)
        created_tipos.append(db_tipo)
    
    db.commit()
    for tipo in created_tipos:
        db.refresh(tipo)
    
    return created_tipos