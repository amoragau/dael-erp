from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import MovimientoDetalle, MovimientoInventario, Producto, ProductoUbicacion
from schemas import MovimientoDetalleCreate, MovimientoDetalleUpdate, MovimientoDetalleResponse, MovimientoDetalleWithRelations
from crud import movimiento_detalle_crud, movimiento_inventario_crud, producto_crud, producto_ubicacion_crud

# Configuración del router
router = APIRouter(
    prefix="/movimientos-detalle",
    tags=["Movimientos Detalle"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[MovimientoDetalleResponse])
def listar_detalles(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    movimiento_id: Optional[int] = Query(None, description="Filtrar por movimiento"),
    producto_id: Optional[int] = Query(None, description="Filtrar por producto"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de detalles de movimientos con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **movimiento_id**: Filtrar detalles de un movimiento específico
    - **producto_id**: Filtrar detalles de un producto específico
    """
    if movimiento_id:
        return movimiento_detalle_crud.get_detalles_by_movimiento(db, movimiento_id=movimiento_id)

    if producto_id:
        return movimiento_detalle_crud.get_detalles_by_producto(db, producto_id=producto_id)

    return movimiento_detalle_crud.get_detalles(db, skip=skip, limit=limit)

@router.get("/{detalle_id}", response_model=MovimientoDetalleWithRelations)
def obtener_detalle(
    detalle_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un detalle por su ID con información completa"""
    detalle = db.query(MovimientoDetalle).filter(MovimientoDetalle.id_detalle == detalle_id).first()
    if detalle is None:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

@router.get("/movimiento/{movimiento_id}/detalles", response_model=List[MovimientoDetalleWithRelations])
def obtener_detalles_por_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db)
):
    """Obtener todos los detalles de un movimiento específico"""
    # Verificar que el movimiento existe
    movimiento = movimiento_inventario_crud.get_movimiento(db, movimiento_id)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    # Obtener con relaciones completas
    query = db.query(MovimientoDetalle).filter(MovimientoDetalle.id_movimiento == movimiento_id)
    return query.all()

@router.get("/producto/{producto_id}/detalles", response_model=List[MovimientoDetalleWithRelations])
def obtener_detalles_por_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """Obtener todos los detalles de movimientos de un producto específico"""
    # Verificar que el producto existe
    producto = producto_crud.get_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Obtener con relaciones completas
    query = db.query(MovimientoDetalle).filter(MovimientoDetalle.id_producto == producto_id)
    return query.all()

@router.post("/", response_model=MovimientoDetalleResponse, status_code=201)
def crear_detalle(
    detalle: MovimientoDetalleCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo detalle de movimiento
    - Requiere que existan el movimiento, producto y ubicaciones
    - Valida disponibilidad de stock en ubicación origen (para salidas)
    """
    # Verificar que el movimiento existe
    movimiento = movimiento_inventario_crud.get_movimiento(db, detalle.id_movimiento)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    # Verificar que el producto existe
    producto = producto_crud.get_producto(db, detalle.id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar ubicación origen si se especifica
    if detalle.id_ubicacion_origen:
        ubicacion_origen = producto_ubicacion_crud.get_ubicacion(db, detalle.id_ubicacion_origen)
        if not ubicacion_origen:
            raise HTTPException(status_code=404, detail="Ubicación origen no encontrada")

        # Validar que hay suficiente stock disponible
        stock_disponible = ubicacion_origen.cantidad - ubicacion_origen.cantidad_reservada
        if detalle.cantidad > stock_disponible:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente. Disponible: {stock_disponible}, Solicitado: {detalle.cantidad}"
            )

    # Verificar ubicación destino si se especifica
    if detalle.id_ubicacion_destino:
        ubicacion_destino = producto_ubicacion_crud.get_ubicacion(db, detalle.id_ubicacion_destino)
        if not ubicacion_destino:
            raise HTTPException(status_code=404, detail="Ubicación destino no encontrada")

    return movimiento_detalle_crud.create_detalle(db=db, detalle=detalle)

@router.put("/{detalle_id}", response_model=MovimientoDetalleResponse)
def actualizar_detalle(
    detalle_id: int,
    detalle_update: MovimientoDetalleUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar detalle existente
    - Solo se actualizan los campos proporcionados
    - Valida relaciones y disponibilidad de stock
    """
    # Verificar que el detalle existe
    db_detalle = movimiento_detalle_crud.get_detalle(db, detalle_id)
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    # Verificar que el movimiento no esté ya procesado
    if db_detalle.movimiento.estado_movimiento == "PROCESADO":
        raise HTTPException(
            status_code=400,
            detail="No se puede modificar el detalle de un movimiento ya procesado"
        )

    # Verificar relaciones si se actualizan
    if detalle_update.id_producto:
        producto = producto_crud.get_producto(db, detalle_update.id_producto)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

    if detalle_update.id_ubicacion_origen:
        ubicacion_origen = producto_ubicacion_crud.get_ubicacion(db, detalle_update.id_ubicacion_origen)
        if not ubicacion_origen:
            raise HTTPException(status_code=404, detail="Ubicación origen no encontrada")

    if detalle_update.id_ubicacion_destino:
        ubicacion_destino = producto_ubicacion_crud.get_ubicacion(db, detalle_update.id_ubicacion_destino)
        if not ubicacion_destino:
            raise HTTPException(status_code=404, detail="Ubicación destino no encontrada")

    # Validar stock si se actualiza la cantidad o ubicación origen
    if (detalle_update.cantidad is not None or detalle_update.id_ubicacion_origen is not None):
        ubicacion_origen_id = detalle_update.id_ubicacion_origen or db_detalle.id_ubicacion_origen
        cantidad = detalle_update.cantidad or db_detalle.cantidad

        if ubicacion_origen_id:
            ubicacion_origen = producto_ubicacion_crud.get_ubicacion(db, ubicacion_origen_id)
            stock_disponible = ubicacion_origen.cantidad - ubicacion_origen.cantidad_reservada

            # Si estamos aumentando la cantidad, validar disponibilidad adicional
            if detalle_update.cantidad and detalle_update.cantidad > db_detalle.cantidad:
                cantidad_adicional = detalle_update.cantidad - db_detalle.cantidad
                if cantidad_adicional > stock_disponible:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Stock insuficiente para el incremento. Disponible: {stock_disponible}, Adicional requerido: {cantidad_adicional}"
                    )

    updated_detalle = movimiento_detalle_crud.update_detalle(db=db, detalle_id=detalle_id, detalle_update=detalle_update)
    if not updated_detalle:
        raise HTTPException(status_code=404, detail="Error al actualizar el detalle")

    return updated_detalle

@router.delete("/{detalle_id}")
def eliminar_detalle(
    detalle_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar detalle
    - Solo se permite si el movimiento no está procesado
    """
    # Verificar que el detalle existe
    db_detalle = movimiento_detalle_crud.get_detalle(db, detalle_id)
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    # Verificar que el movimiento no esté procesado
    if db_detalle.movimiento.estado_movimiento == "PROCESADO":
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el detalle de un movimiento ya procesado"
        )

    success = movimiento_detalle_crud.delete_detalle(db=db, detalle_id=detalle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Error al eliminar el detalle")

    return {"message": "Detalle eliminado correctamente"}

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_detalles(
    movimiento_id: Optional[int] = Query(None, description="Filtrar por movimiento"),
    producto_id: Optional[int] = Query(None, description="Filtrar por producto"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de detalles"""
    query = db.query(MovimientoDetalle)

    if movimiento_id:
        query = query.filter(MovimientoDetalle.id_movimiento == movimiento_id)

    if producto_id:
        query = query.filter(MovimientoDetalle.id_producto == producto_id)

    total = query.count()
    return {"total_detalles": total}

@router.get("/stats/por-producto")
def estadisticas_por_producto(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de movimientos por producto"""
    from sqlalchemy import func

    stats = db.query(
        Producto.sku,
        Producto.nombre_producto,
        func.count(MovimientoDetalle.id_detalle).label('total_movimientos'),
        func.sum(MovimientoDetalle.cantidad).label('cantidad_total_movida'),
        func.avg(MovimientoDetalle.cantidad).label('cantidad_promedio'),
        func.sum(MovimientoDetalle.valor_unitario * MovimientoDetalle.cantidad).label('valor_total')
    ).join(MovimientoDetalle).group_by(
        Producto.id_producto, Producto.sku, Producto.nombre_producto
    ).all()

    return [
        {
            "sku": stat.sku,
            "nombre_producto": stat.nombre_producto,
            "total_movimientos": stat.total_movimientos or 0,
            "cantidad_total_movida": float(stat.cantidad_total_movida or 0),
            "cantidad_promedio": float(stat.cantidad_promedio or 0),
            "valor_total": float(stat.valor_total or 0)
        }
        for stat in stats
    ]

@router.get("/stats/resumen-movimiento/{movimiento_id}")
def resumen_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db)
):
    """Obtener resumen de un movimiento específico"""
    from sqlalchemy import func

    # Verificar que el movimiento existe
    movimiento = movimiento_inventario_crud.get_movimiento(db, movimiento_id)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    stats = db.query(
        func.count(MovimientoDetalle.id_detalle).label('total_lineas'),
        func.sum(MovimientoDetalle.cantidad).label('cantidad_total'),
        func.sum(MovimientoDetalle.valor_unitario * MovimientoDetalle.cantidad).label('valor_total'),
        func.count(func.distinct(MovimientoDetalle.id_producto)).label('productos_distintos')
    ).filter(MovimientoDetalle.id_movimiento == movimiento_id).first()

    return {
        "id_movimiento": movimiento_id,
        "numero_movimiento": movimiento.numero_movimiento,
        "tipo_movimiento": movimiento.tipo_movimiento.nombre_tipo if movimiento.tipo_movimiento else None,
        "estado_movimiento": movimiento.estado_movimiento,
        "total_lineas": stats.total_lineas or 0,
        "cantidad_total": float(stats.cantidad_total or 0),
        "valor_total": float(stats.valor_total or 0),
        "productos_distintos": stats.productos_distintos or 0
    }

@router.get("/stats/valores")
def estadisticas_valores(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de valores de movimientos"""
    from sqlalchemy import func

    stats = db.query(
        func.sum(MovimientoDetalle.valor_unitario * MovimientoDetalle.cantidad).label('valor_total'),
        func.avg(MovimientoDetalle.valor_unitario * MovimientoDetalle.cantidad).label('valor_promedio'),
        func.max(MovimientoDetalle.valor_unitario * MovimientoDetalle.cantidad).label('valor_maximo'),
        func.min(MovimientoDetalle.valor_unitario * MovimientoDetalle.cantidad).label('valor_minimo'),
        func.count(MovimientoDetalle.id_detalle).label('total_detalles')
    ).first()

    return {
        "valor_total": float(stats.valor_total or 0),
        "valor_promedio": float(stats.valor_promedio or 0),
        "valor_maximo": float(stats.valor_maximo or 0),
        "valor_minimo": float(stats.valor_minimo or 0),
        "total_detalles": stats.total_detalles or 0
    }