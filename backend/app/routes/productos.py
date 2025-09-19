from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import Producto, Marca, TipoProducto, UnidadMedida
from schemas import ProductoCreate, ProductoUpdate, ProductoResponse, ProductoWithRelations
from crud import producto_crud, marca_crud, tipo_producto_crud, unidad_medida_crud

# Configuración del router
router = APIRouter(
    prefix="/productos",
    tags=["Productos"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[ProductoResponse])
def listar_productos(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    marca_id: Optional[int] = Query(None, description="Filtrar por marca"),
    tipo_id: Optional[int] = Query(None, description="Filtrar por tipo de producto"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de productos con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo productos activos (true) o inactivos (false)
    - **marca_id**: Filtrar productos de una marca específica
    - **tipo_id**: Filtrar productos de un tipo específico
    """
    if marca_id:
        return producto_crud.get_productos_by_marca(db, marca_id=marca_id, activo=activo)

    if tipo_id:
        return producto_crud.get_productos_by_tipo(db, tipo_id=tipo_id, activo=activo)

    return producto_crud.get_productos(db, skip=skip, limit=limit, activo=activo)

@router.get("/search", response_model=List[ProductoResponse])
def buscar_productos(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    db: Session = Depends(get_db)
):
    """
    Buscar productos por SKU, nombre o descripción
    - **q**: Término de búsqueda (busca en SKU, nombre y descripción)
    """
    return producto_crud.search_productos(db, search_term=q, skip=skip, limit=limit)

@router.get("/bajo-stock", response_model=List[ProductoResponse])
def productos_bajo_stock(
    db: Session = Depends(get_db)
):
    """Obtener productos con stock bajo el punto de reorden"""
    return producto_crud.get_productos_bajo_stock(db)

@router.get("/{producto_id}", response_model=ProductoWithRelations)
def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un producto por su ID con información de marca, tipo y unidad"""
    producto = db.query(Producto).filter(Producto.id_producto == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.get("/sku/{sku}", response_model=ProductoWithRelations)
def obtener_producto_por_sku(
    sku: str,
    db: Session = Depends(get_db)
):
    """Obtener un producto por su SKU"""
    producto = db.query(Producto).filter(Producto.sku == sku).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/", response_model=ProductoResponse, status_code=201)
def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo producto
    - Requiere SKU único
    - Valida que existan marca (opcional), tipo de producto y unidad de medida
    """
    # Verificar si ya existe un producto con el mismo SKU
    db_producto = producto_crud.get_producto_by_sku(db, producto.sku)
    if db_producto:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un producto con ese SKU"
        )

    # Verificar que el tipo de producto existe
    tipo_producto = tipo_producto_crud.get_tipo_producto(db, producto.id_tipo_producto)
    if not tipo_producto:
        raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")

    # Verificar que la unidad de medida existe
    unidad_medida = unidad_medida_crud.get_unidad(db, producto.id_unidad_medida)
    if not unidad_medida:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")

    # Verificar que la marca existe (si se especifica)
    if producto.id_marca:
        marca = marca_crud.get_marca(db, producto.id_marca)
        if not marca:
            raise HTTPException(status_code=404, detail="Marca no encontrada")

    # Validar rangos de temperatura si se especifican
    if (producto.temperatura_min_celsius is not None and
        producto.temperatura_max_celsius is not None and
        producto.temperatura_min_celsius > producto.temperatura_max_celsius):
        raise HTTPException(
            status_code=400,
            detail="La temperatura mínima no puede ser mayor que la máxima"
        )

    # Validar rangos de presión si se especifican
    if (producto.presion_trabajo_bar is not None and
        producto.presion_maxima_bar is not None and
        producto.presion_trabajo_bar > producto.presion_maxima_bar):
        raise HTTPException(
            status_code=400,
            detail="La presión de trabajo no puede ser mayor que la máxima"
        )

    return producto_crud.create_producto(db=db, producto=producto)

@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int,
    producto_update: ProductoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar producto existente
    - Solo se actualizan los campos proporcionados
    - Si se cambia el SKU, debe ser único
    - Valida relaciones con otras tablas
    """
    # Verificar que el producto existe
    db_producto = producto_crud.get_producto(db, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Si se está actualizando el SKU, verificar que sea único
    if producto_update.sku and producto_update.sku != db_producto.sku:
        existing_producto = producto_crud.get_producto_by_sku(db, producto_update.sku)
        if existing_producto:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un producto con ese SKU"
            )

    # Verificar relaciones si se actualizan
    if producto_update.id_tipo_producto:
        tipo_producto = tipo_producto_crud.get_tipo_producto(db, producto_update.id_tipo_producto)
        if not tipo_producto:
            raise HTTPException(status_code=404, detail="Tipo de producto no encontrado")

    if producto_update.id_unidad_medida:
        unidad_medida = unidad_medida_crud.get_unidad(db, producto_update.id_unidad_medida)
        if not unidad_medida:
            raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")

    if producto_update.id_marca:
        marca = marca_crud.get_marca(db, producto_update.id_marca)
        if not marca:
            raise HTTPException(status_code=404, detail="Marca no encontrada")

    # Validar rangos de temperatura
    temp_min = producto_update.temperatura_min_celsius if producto_update.temperatura_min_celsius is not None else db_producto.temperatura_min_celsius
    temp_max = producto_update.temperatura_max_celsius if producto_update.temperatura_max_celsius is not None else db_producto.temperatura_max_celsius

    if temp_min is not None and temp_max is not None and temp_min > temp_max:
        raise HTTPException(
            status_code=400,
            detail="La temperatura mínima no puede ser mayor que la máxima"
        )

    # Validar rangos de presión
    presion_trabajo = producto_update.presion_trabajo_bar if producto_update.presion_trabajo_bar is not None else db_producto.presion_trabajo_bar
    presion_maxima = producto_update.presion_maxima_bar if producto_update.presion_maxima_bar is not None else db_producto.presion_maxima_bar

    if presion_trabajo is not None and presion_maxima is not None and presion_trabajo > presion_maxima:
        raise HTTPException(
            status_code=400,
            detail="La presión de trabajo no puede ser mayor que la máxima"
        )

    updated_producto = producto_crud.update_producto(db=db, producto_id=producto_id, producto_update=producto_update)
    if not updated_producto:
        raise HTTPException(status_code=404, detail="Error al actualizar el producto")

    return updated_producto

@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar producto (soft delete)
    - Marca el producto como inactivo en lugar de eliminarlo físicamente
    """
    success = producto_crud.delete_producto(db=db, producto_id=producto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"message": "Producto eliminado correctamente"}

@router.patch("/{producto_id}/toggle", response_model=ProductoResponse)
def toggle_estado_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de un producto
    """
    db_producto = producto_crud.get_producto(db, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Cambiar el estado
    producto_update = ProductoUpdate(activo=not db_producto.activo)
    updated_producto = producto_crud.update_producto(db=db, producto_id=producto_id, producto_update=producto_update)

    return updated_producto

@router.patch("/{producto_id}/stock", response_model=ProductoResponse)
def actualizar_stock(
    producto_id: int,
    nuevo_stock: int = Query(..., ge=0, description="Nuevo stock del producto"),
    db: Session = Depends(get_db)
):
    """
    Actualizar stock de un producto
    """
    updated_producto = producto_crud.update_stock(db=db, producto_id=producto_id, nuevo_stock=nuevo_stock)
    if not updated_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return updated_producto

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_productos(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de productos"""
    query = db.query(Producto)
    if activo is not None:
        query = query.filter(Producto.activo == activo)

    total = query.count()
    return {"total_productos": total}

@router.get("/stats/inventario")
def estadisticas_inventario(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de inventario"""
    from sqlalchemy import func

    # Estadísticas básicas
    stats = db.query(
        func.count(Producto.id_producto).label('total'),
        func.sum(Producto.stock_actual).label('stock_total'),
        func.avg(Producto.stock_actual).label('stock_promedio'),
        func.sum(Producto.costo_promedio * Producto.stock_actual).label('valor_inventario'),
        func.count(func.nullif(Producto.stock_actual <= Producto.punto_reorden, False)).label('productos_bajo_stock')
    ).filter(Producto.activo == True).first()

    # Productos sin stock
    sin_stock = db.query(func.count(Producto.id_producto)).filter(
        Producto.activo == True,
        Producto.stock_actual == 0
    ).scalar()

    return {
        "total_productos_activos": stats.total or 0,
        "stock_total_unidades": int(stats.stock_total or 0),
        "stock_promedio": float(stats.stock_promedio or 0),
        "valor_total_inventario": float(stats.valor_inventario or 0),
        "productos_bajo_stock": stats.productos_bajo_stock or 0,
        "productos_sin_stock": sin_stock or 0
    }

@router.get("/stats/por-marca")
def estadisticas_por_marca(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de productos por marca"""
    from sqlalchemy import func

    stats = db.query(
        Marca.nombre_marca,
        func.count(Producto.id_producto).label('total_productos'),
        func.sum(Producto.stock_actual).label('stock_total'),
        func.avg(Producto.precio_venta).label('precio_promedio')
    ).outerjoin(Producto).group_by(
        Marca.id_marca, Marca.nombre_marca
    ).filter(
        Marca.activo == True,
        Producto.activo == True
    ).all()

    return [
        {
            "marca": stat.nombre_marca,
            "total_productos": stat.total_productos or 0,
            "stock_total": int(stat.stock_total or 0),
            "precio_promedio": float(stat.precio_promedio or 0)
        }
        for stat in stats
    ]

@router.get("/stats/por-tipo")
def estadisticas_por_tipo(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de productos por tipo"""
    from sqlalchemy import func

    stats = db.query(
        TipoProducto.nombre_tipo,
        func.count(Producto.id_producto).label('total_productos'),
        func.sum(Producto.stock_actual).label('stock_total'),
        func.avg(Producto.costo_promedio).label('costo_promedio')
    ).join(Producto).group_by(
        TipoProducto.id_tipo_producto, TipoProducto.nombre_tipo
    ).filter(
        TipoProducto.activo == True,
        Producto.activo == True
    ).all()

    return [
        {
            "tipo_producto": stat.nombre_tipo,
            "total_productos": stat.total_productos or 0,
            "stock_total": int(stat.stock_total or 0),
            "costo_promedio": float(stat.costo_promedio or 0)
        }
        for stat in stats
    ]