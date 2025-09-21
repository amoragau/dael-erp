from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import ProductoUbicacion, Producto, Estante
from schemas import ProductoUbicacionCreate, ProductoUbicacionUpdate, ProductoUbicacionResponse, ProductoUbicacionWithRelations
from crud import producto_ubicacion_crud, producto_crud, estante_crud

# Configuración del router
router = APIRouter(
    prefix="/producto-ubicaciones",
    tags=["Producto-Ubicaciones"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[ProductoUbicacionResponse])
def listar_ubicaciones(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    producto_id: Optional[int] = Query(None, description="Filtrar por producto"),
    estante_id: Optional[int] = Query(None, description="Filtrar por estante"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de ubicaciones de productos con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo ubicaciones activas (true) o inactivas (false)
    - **producto_id**: Filtrar ubicaciones de un producto específico
    - **estante_id**: Filtrar ubicaciones en un estante específico
    """
    if producto_id:
        return producto_ubicacion_crud.get_ubicaciones_by_producto(db, producto_id=producto_id, activo=activo)

    if estante_id:
        return producto_ubicacion_crud.get_ubicaciones_by_estante(db, estante_id=estante_id, activo=activo)

    return producto_ubicacion_crud.get_ubicaciones(db, skip=skip, limit=limit, activo=activo)

@router.get("/{ubicacion_id}", response_model=ProductoUbicacionWithRelations)
def obtener_ubicacion(
    ubicacion_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una ubicación por su ID con información completa"""
    ubicacion = db.query(ProductoUbicacion).filter(ProductoUbicacion.id_ubicacion == ubicacion_id).first()
    if ubicacion is None:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return ubicacion

@router.get("/producto/{producto_id}/ubicaciones", response_model=List[ProductoUbicacionWithRelations])
def obtener_ubicaciones_por_producto(
    producto_id: int,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener todas las ubicaciones de un producto específico"""
    # Verificar que el producto existe
    producto = producto_crud.get_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Obtener con relaciones completas
    query = db.query(ProductoUbicacion).filter(ProductoUbicacion.id_producto == producto_id)

    if activo is not None:
        query = query.filter(ProductoUbicacion.activo == activo)

    return query.all()

@router.get("/estante/{estante_id}/ubicaciones", response_model=List[ProductoUbicacionWithRelations])
def obtener_ubicaciones_por_estante(
    estante_id: int,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener todas las ubicaciones en un estante específico"""
    # Verificar que el estante existe
    estante = estante_crud.get_estante(db, estante_id)
    if not estante:
        raise HTTPException(status_code=404, detail="Estante no encontrado")

    # Obtener con relaciones completas
    query = db.query(ProductoUbicacion).filter(ProductoUbicacion.id_estante == estante_id)

    if activo is not None:
        query = query.filter(ProductoUbicacion.activo == activo)

    return query.all()

@router.post("/", response_model=ProductoUbicacionResponse, status_code=201)
def crear_ubicacion(
    ubicacion: ProductoUbicacionCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nueva ubicación de producto
    - Requiere que existan el producto y el estante
    - Valida que la cantidad reservada no sea mayor que la cantidad total
    """
    # Verificar que el producto existe
    producto = producto_crud.get_producto(db, ubicacion.id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar que el estante existe
    estante = estante_crud.get_estante(db, ubicacion.id_estante)
    if not estante:
        raise HTTPException(status_code=404, detail="Estante no encontrado")

    # Validar que la cantidad reservada no sea mayor que la cantidad total
    if ubicacion.cantidad_reservada > ubicacion.cantidad:
        raise HTTPException(
            status_code=400,
            detail="La cantidad reservada no puede ser mayor que la cantidad total"
        )

    # Verificar si ya existe una ubicación para este producto en este estante
    existing_ubicacion = db.query(ProductoUbicacion).filter(
        ProductoUbicacion.id_producto == ubicacion.id_producto,
        ProductoUbicacion.id_estante == ubicacion.id_estante,
        ProductoUbicacion.activo == True
    ).first()

    if existing_ubicacion:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una ubicación activa para este producto en este estante"
        )

    return producto_ubicacion_crud.create_ubicacion(db=db, ubicacion=ubicacion)

@router.put("/{ubicacion_id}", response_model=ProductoUbicacionResponse)
def actualizar_ubicacion(
    ubicacion_id: int,
    ubicacion_update: ProductoUbicacionUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar ubicación existente
    - Solo se actualizan los campos proporcionados
    - Valida relaciones y restricciones
    """
    # Verificar que la ubicación existe
    db_ubicacion = producto_ubicacion_crud.get_ubicacion(db, ubicacion_id)
    if not db_ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    # Verificar relaciones si se actualizan
    if ubicacion_update.id_producto:
        producto = producto_crud.get_producto(db, ubicacion_update.id_producto)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

    if ubicacion_update.id_estante:
        estante = estante_crud.get_estante(db, ubicacion_update.id_estante)
        if not estante:
            raise HTTPException(status_code=404, detail="Estante no encontrado")

    # Validar cantidades
    cantidad_total = ubicacion_update.cantidad if ubicacion_update.cantidad is not None else db_ubicacion.cantidad
    cantidad_reservada = ubicacion_update.cantidad_reservada if ubicacion_update.cantidad_reservada is not None else db_ubicacion.cantidad_reservada

    if cantidad_reservada > cantidad_total:
        raise HTTPException(
            status_code=400,
            detail="La cantidad reservada no puede ser mayor que la cantidad total"
        )

    updated_ubicacion = producto_ubicacion_crud.update_ubicacion(db=db, ubicacion_id=ubicacion_id, ubicacion_update=ubicacion_update)
    if not updated_ubicacion:
        raise HTTPException(status_code=404, detail="Error al actualizar la ubicación")

    return updated_ubicacion

@router.delete("/{ubicacion_id}")
def eliminar_ubicacion(
    ubicacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar ubicación (soft delete)
    - Marca la ubicación como inactiva en lugar de eliminarla físicamente
    """
    success = producto_ubicacion_crud.delete_ubicacion(db=db, ubicacion_id=ubicacion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    return {"message": "Ubicación eliminada correctamente"}

@router.patch("/{ubicacion_id}/toggle", response_model=ProductoUbicacionResponse)
def toggle_estado_ubicacion(
    ubicacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de una ubicación
    """
    db_ubicacion = producto_ubicacion_crud.get_ubicacion(db, ubicacion_id)
    if not db_ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    # Cambiar el estado
    ubicacion_update = ProductoUbicacionUpdate(activo=not db_ubicacion.activo)
    updated_ubicacion = producto_ubicacion_crud.update_ubicacion(db=db, ubicacion_id=ubicacion_id, ubicacion_update=ubicacion_update)

    return updated_ubicacion

@router.patch("/{ubicacion_id}/cantidad", response_model=ProductoUbicacionResponse)
def actualizar_cantidad(
    ubicacion_id: int,
    nueva_cantidad: int = Query(..., ge=0, description="Nueva cantidad en la ubicación"),
    db: Session = Depends(get_db)
):
    """
    Actualizar cantidad en una ubicación específica
    """
    # Verificar que la nueva cantidad sea mayor o igual a la cantidad reservada
    db_ubicacion = producto_ubicacion_crud.get_ubicacion(db, ubicacion_id)
    if not db_ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    if nueva_cantidad < db_ubicacion.cantidad_reservada:
        raise HTTPException(
            status_code=400,
            detail=f"La nueva cantidad ({nueva_cantidad}) no puede ser menor que la cantidad reservada ({db_ubicacion.cantidad_reservada})"
        )

    updated_ubicacion = producto_ubicacion_crud.update_cantidad(db=db, ubicacion_id=ubicacion_id, nueva_cantidad=nueva_cantidad)
    if not updated_ubicacion:
        raise HTTPException(status_code=404, detail="Error al actualizar la cantidad")

    return updated_ubicacion

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_ubicaciones(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de ubicaciones"""
    query = db.query(ProductoUbicacion)
    if activo is not None:
        query = query.filter(ProductoUbicacion.activo == activo)

    total = query.count()
    return {"total_ubicaciones": total}

@router.get("/stats/ocupacion")
def estadisticas_ocupacion(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de ocupación de ubicaciones"""
    from sqlalchemy import func

    stats = db.query(
        func.count(ProductoUbicacion.id_ubicacion).label('total_ubicaciones'),
        func.sum(ProductoUbicacion.cantidad).label('cantidad_total'),
        func.sum(ProductoUbicacion.cantidad_reservada).label('cantidad_reservada_total'),
        func.count(func.nullif(ProductoUbicacion.cantidad, 0)).label('ubicaciones_con_stock'),
        func.count(func.nullif(ProductoUbicacion.cantidad_reservada, 0)).label('ubicaciones_con_reservas')
    ).filter(ProductoUbicacion.activo == True).first()

    # Ubicaciones vacías
    ubicaciones_vacias = db.query(func.count(ProductoUbicacion.id_ubicacion)).filter(
        ProductoUbicacion.activo == True,
        ProductoUbicacion.cantidad == 0
    ).scalar()

    return {
        "total_ubicaciones_activas": stats.total_ubicaciones or 0,
        "cantidad_total_almacenada": int(stats.cantidad_total or 0),
        "cantidad_total_reservada": int(stats.cantidad_reservada_total or 0),
        "ubicaciones_con_stock": stats.ubicaciones_con_stock or 0,
        "ubicaciones_con_reservas": stats.ubicaciones_con_reservas or 0,
        "ubicaciones_vacias": ubicaciones_vacias or 0,
        "cantidad_disponible": int((stats.cantidad_total or 0) - (stats.cantidad_reservada_total or 0))
    }

@router.get("/stats/por-bodega")
def estadisticas_por_bodega(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de ubicaciones por bodega"""
    from sqlalchemy import func
    from models import Bodega, Pasillo, Estante

    stats = db.query(
        Bodega.codigo_bodega,
        Bodega.nombre_bodega,
        func.count(ProductoUbicacion.id_ubicacion).label('total_ubicaciones'),
        func.sum(ProductoUbicacion.cantidad).label('cantidad_total'),
        func.count(func.nullif(ProductoUbicacion.cantidad, 0)).label('ubicaciones_ocupadas')
    ).select_from(Bodega).join(Pasillo).join(Estante).join(Estante).outerjoin(ProductoUbicacion).group_by(
        Bodega.id_bodega, Bodega.codigo_bodega, Bodega.nombre_bodega
    ).filter(
        Bodega.activo == True,
        ProductoUbicacion.activo == True
    ).all()

    return [
        {
            "codigo_bodega": stat.codigo_bodega,
            "nombre_bodega": stat.nombre_bodega,
            "total_ubicaciones": stat.total_ubicaciones or 0,
            "cantidad_total": int(stat.cantidad_total or 0),
            "ubicaciones_ocupadas": stat.ubicaciones_ocupadas or 0,
            "porcentaje_ocupacion": round((stat.ubicaciones_ocupadas / stat.total_ubicaciones * 100) if stat.total_ubicaciones > 0 else 0, 2)
        }
        for stat in stats
    ]

@router.get("/stats/productos-sin-ubicacion")
def productos_sin_ubicacion(
    db: Session = Depends(get_db)
):
    """Obtener productos que no tienen ubicaciones activas"""
    productos_sin_ubicacion = db.query(Producto).outerjoin(
        ProductoUbicacion,
        (Producto.id_producto == ProductoUbicacion.id_producto) &
        (ProductoUbicacion.activo == True)
    ).filter(
        Producto.activo == True,
        ProductoUbicacion.id_ubicacion.is_(None)
    ).all()

    return {
        "total_productos_sin_ubicacion": len(productos_sin_ubicacion),
        "productos": [
            {
                "id_producto": p.id_producto,
                "sku": p.sku,
                "nombre_producto": p.nombre_producto,
                "stock_actual": p.stock_actual
            }
            for p in productos_sin_ubicacion
        ]
    }