from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime, date

# Imports locales
from database import get_db
from models import MovimientoInventario, MovimientoDetalle, TipoMovimiento, DocumentoMovimiento
from schemas import (
    MovimientoInventarioCreate, MovimientoInventarioUpdate, MovimientoInventarioResponse,
    MovimientoInventarioWithRelations, MovimientoInventarioCompleto,
    MovimientoDetalleCreate, MovimientoDetalleUpdate, MovimientoDetalleResponse,
    MovimientoDetalleWithRelations, EstadoMovimientoEnum
)
from crud import (
    movimiento_inventario_crud, movimiento_detalle_crud, tipo_movimiento_crud,
    documento_movimiento_crud, producto_crud, producto_ubicacion_crud
)

# Configuración del router
router = APIRouter(
    prefix="/movimientos-inventario",
    tags=["Movimientos de Inventario"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD - MOVIMIENTOS
# ========================================

@router.get("/", response_model=List[MovimientoInventarioWithRelations])
def listar_movimientos(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    estado: Optional[EstadoMovimientoEnum] = Query(None, description="Filtrar por estado"),
    tipo_movimiento_id: Optional[int] = Query(None, description="Filtrar por tipo de movimiento"),
    usuario_id: Optional[int] = Query(None, description="Filtrar por usuario"),
    fecha_desde: Optional[date] = Query(None, description="Fecha inicial"),
    fecha_hasta: Optional[date] = Query(None, description="Fecha final"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de movimientos de inventario con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **estado**: Filtrar por estado del movimiento
    - **tipo_movimiento_id**: Filtrar por tipo de movimiento
    - **usuario_id**: Filtrar movimientos de un usuario específico
    - **fecha_desde/fecha_hasta**: Rango de fechas
    """
    if usuario_id:
        return movimiento_inventario_crud.get_movimientos_by_usuario(db, usuario_id=usuario_id)

    # Aplicar filtros adicionales con carga de relaciones
    query = db.query(MovimientoInventario).options(
        joinedload(MovimientoInventario.tipo_movimiento),
        joinedload(MovimientoInventario.documento),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.producto),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_origen),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_destino)
    )

    if estado:
        query = query.filter(MovimientoInventario.estado == estado.value)

    if tipo_movimiento_id:
        query = query.filter(MovimientoInventario.id_tipo_movimiento == tipo_movimiento_id)

    if fecha_desde:
        query = query.filter(MovimientoInventario.fecha_movimiento >= fecha_desde)

    if fecha_hasta:
        query = query.filter(MovimientoInventario.fecha_movimiento <= fecha_hasta)

    return query.order_by(MovimientoInventario.fecha_movimiento.desc()).offset(skip).limit(limit).all()

@router.get("/{movimiento_id}", response_model=MovimientoInventarioWithRelations)
def obtener_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un movimiento por su ID con información completa incluyendo detalles"""
    movimiento = db.query(MovimientoInventario).options(
        joinedload(MovimientoInventario.tipo_movimiento),
        joinedload(MovimientoInventario.documento),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.producto),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_origen),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_destino)
    ).filter(MovimientoInventario.id_movimiento == movimiento_id).first()
    if movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return movimiento

@router.get("/numero/{numero_movimiento}", response_model=MovimientoInventarioWithRelations)
def obtener_movimiento_por_numero(
    numero_movimiento: str,
    db: Session = Depends(get_db)
):
    """Obtener un movimiento por su número"""
    movimiento = db.query(MovimientoInventario).options(
        joinedload(MovimientoInventario.tipo_movimiento),
        joinedload(MovimientoInventario.documento),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.producto),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_origen),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_destino)
    ).filter(MovimientoInventario.numero_movimiento == numero_movimiento).first()
    if movimiento is None:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return movimiento

@router.post("/", response_model=MovimientoInventarioWithRelations, status_code=201)
def crear_movimiento(
    movimiento: MovimientoInventarioCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo movimiento de inventario
    - Requiere número único
    - Valida que existan tipo de movimiento y documento (opcional)
    """
    # Verificar que no existe un movimiento con el mismo número
    existing_movimiento = movimiento_inventario_crud.get_movimiento_by_numero(db, movimiento.numero_movimiento)
    if existing_movimiento:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un movimiento con número {movimiento.numero_movimiento}"
        )

    # Verificar que el tipo de movimiento existe
    tipo_movimiento = tipo_movimiento_crud.get_movimiento(db, movimiento.id_tipo_movimiento)
    if not tipo_movimiento:
        raise HTTPException(status_code=404, detail="Tipo de movimiento no encontrado")

    # Verificar que el documento existe (si se especifica)
    if movimiento.id_documento:
        documento = documento_movimiento_crud.get_documento(db, movimiento.id_documento)
        if not documento:
            raise HTTPException(status_code=404, detail="Documento no encontrado")

    nuevo_movimiento = movimiento_inventario_crud.create_movimiento(db=db, movimiento=movimiento)

    # Cargar el movimiento con todas las relaciones
    return db.query(MovimientoInventario).options(
        joinedload(MovimientoInventario.tipo_movimiento),
        joinedload(MovimientoInventario.documento),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.producto),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_origen),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_destino)
    ).filter(MovimientoInventario.id_movimiento == nuevo_movimiento.id_movimiento).first()

@router.post("/completo", response_model=MovimientoInventarioWithRelations, status_code=201)
def crear_movimiento_completo(
    movimiento_completo: MovimientoInventarioCompleto,
    db: Session = Depends(get_db)
):
    """
    Crear movimiento completo con detalles en una sola operación
    - Valida todas las relaciones
    - Crea movimiento y detalles automáticamente
    """
    # Validaciones del movimiento principal (reutilizar lógica)
    existing_movimiento = movimiento_inventario_crud.get_movimiento_by_numero(
        db, movimiento_completo.movimiento.numero_movimiento
    )
    if existing_movimiento:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un movimiento con número {movimiento_completo.movimiento.numero_movimiento}"
        )

    # Verificar tipo de movimiento
    tipo_movimiento = tipo_movimiento_crud.get_movimiento(db, movimiento_completo.movimiento.id_tipo_movimiento)
    if not tipo_movimiento:
        raise HTTPException(status_code=404, detail="Tipo de movimiento no encontrado")

    # Crear el movimiento principal
    db_movimiento = movimiento_inventario_crud.create_movimiento(db=db, movimiento=movimiento_completo.movimiento)

    # Crear los detalles
    for detalle_data in movimiento_completo.detalles:
        # Validar producto
        producto = producto_crud.get_producto(db, detalle_data.id_producto)
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {detalle_data.id_producto} no encontrado")

        # Validar ubicaciones si se especifican
        if detalle_data.id_ubicacion_origen:
            ubicacion_origen = producto_ubicacion_crud.get_ubicacion(db, detalle_data.id_ubicacion_origen)
            if not ubicacion_origen:
                raise HTTPException(status_code=404, detail=f"Ubicación origen {detalle_data.id_ubicacion_origen} no encontrada")

        if detalle_data.id_ubicacion_destino:
            ubicacion_destino = producto_ubicacion_crud.get_ubicacion(db, detalle_data.id_ubicacion_destino)
            if not ubicacion_destino:
                raise HTTPException(status_code=404, detail=f"Ubicación destino {detalle_data.id_ubicacion_destino} no encontrada")

        # Asignar el ID del movimiento creado
        detalle_data.id_movimiento = db_movimiento.id_movimiento

        # Crear el detalle
        movimiento_detalle_crud.create_detalle(db=db, detalle=detalle_data)

    # Obtener el movimiento completo con relaciones
    return db.query(MovimientoInventario).filter(MovimientoInventario.id_movimiento == db_movimiento.id_movimiento).first()

@router.put("/{movimiento_id}", response_model=MovimientoInventarioWithRelations)
def actualizar_movimiento(
    movimiento_id: int,
    movimiento_update: MovimientoInventarioUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar movimiento existente
    - Solo se actualizan los campos proporcionados
    - No se puede modificar si está PROCESADO
    """
    # Verificar que el movimiento existe
    db_movimiento = movimiento_inventario_crud.get_movimiento(db, movimiento_id)
    if not db_movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    # No permitir modificaciones si está procesado
    if db_movimiento.estado == 'PROCESADO':
        raise HTTPException(
            status_code=400,
            detail="No se puede modificar un movimiento que ya ha sido procesado"
        )

    # Validar número único si se cambia
    if movimiento_update.numero_movimiento and movimiento_update.numero_movimiento != db_movimiento.numero_movimiento:
        existing_movimiento = movimiento_inventario_crud.get_movimiento_by_numero(db, movimiento_update.numero_movimiento)
        if existing_movimiento:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un movimiento con número {movimiento_update.numero_movimiento}"
            )

    # Validar relaciones si se actualizan
    if movimiento_update.id_tipo_movimiento:
        tipo_movimiento = tipo_movimiento_crud.get_movimiento(db, movimiento_update.id_tipo_movimiento)
        if not tipo_movimiento:
            raise HTTPException(status_code=404, detail="Tipo de movimiento no encontrado")

    if movimiento_update.id_documento:
        documento = documento_movimiento_crud.get_documento(db, movimiento_update.id_documento)
        if not documento:
            raise HTTPException(status_code=404, detail="Documento no encontrado")

    updated_movimiento = movimiento_inventario_crud.update_movimiento(
        db=db, movimiento_id=movimiento_id, movimiento_update=movimiento_update
    )
    if not updated_movimiento:
        raise HTTPException(status_code=404, detail="Error al actualizar el movimiento")

    # Cargar el movimiento con todas las relaciones
    return db.query(MovimientoInventario).options(
        joinedload(MovimientoInventario.tipo_movimiento),
        joinedload(MovimientoInventario.documento),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.producto),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_origen),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_destino)
    ).filter(MovimientoInventario.id_movimiento == movimiento_id).first()

@router.patch("/{movimiento_id}/autorizar", response_model=MovimientoInventarioWithRelations)
def autorizar_movimiento(
    movimiento_id: int,
    autorizado_por: int = Query(..., description="ID del usuario que autoriza"),
    db: Session = Depends(get_db)
):
    """
    Autorizar un movimiento
    - Solo se pueden autorizar movimientos PENDIENTES
    - Requiere ID de usuario autorizador
    """
    db_movimiento = movimiento_inventario_crud.get_movimiento(db, movimiento_id)
    if not db_movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    if db_movimiento.estado != 'PENDIENTE':
        raise HTTPException(
            status_code=400,
            detail=f"Solo se pueden autorizar movimientos PENDIENTES. Estado actual: {db_movimiento.estado}"
        )

    # Validar que el tipo de movimiento requiere autorización
    if not db_movimiento.tipo_movimiento.requiere_autorizacion:
        raise HTTPException(
            status_code=400,
            detail="Este tipo de movimiento no requiere autorización"
        )

    updated_movimiento = movimiento_inventario_crud.autorizar_movimiento(
        db=db, movimiento_id=movimiento_id, autorizado_por=autorizado_por
    )

    # Cargar el movimiento con todas las relaciones
    return db.query(MovimientoInventario).options(
        joinedload(MovimientoInventario.tipo_movimiento),
        joinedload(MovimientoInventario.documento),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.producto),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_origen),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_destino)
    ).filter(MovimientoInventario.id_movimiento == movimiento_id).first()

@router.patch("/{movimiento_id}/procesar", response_model=MovimientoInventarioWithRelations)
def procesar_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db)
):
    """
    Procesar un movimiento (actualizar stocks)
    - Solo se pueden procesar movimientos AUTORIZADOS
    - Actualiza automáticamente las cantidades en ubicaciones
    """
    db_movimiento = movimiento_inventario_crud.get_movimiento(db, movimiento_id)
    if not db_movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    if db_movimiento.estado not in ['AUTORIZADO', 'PENDIENTE']:
        raise HTTPException(
            status_code=400,
            detail=f"Solo se pueden procesar movimientos AUTORIZADOS o PENDIENTES. Estado actual: {db_movimiento.estado}"
        )

    # Si requiere autorización y está pendiente, no se puede procesar
    if db_movimiento.tipo_movimiento.requiere_autorizacion and db_movimiento.estado == 'PENDIENTE':
        raise HTTPException(
            status_code=400,
            detail="Este movimiento requiere autorización antes de ser procesado"
        )

    updated_movimiento = movimiento_inventario_crud.procesar_movimiento(db=db, movimiento_id=movimiento_id)
    if not updated_movimiento:
        raise HTTPException(status_code=400, detail="Error al procesar el movimiento")

    # Cargar el movimiento con todas las relaciones
    return db.query(MovimientoInventario).options(
        joinedload(MovimientoInventario.tipo_movimiento),
        joinedload(MovimientoInventario.documento),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.producto),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_origen),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_destino)
    ).filter(MovimientoInventario.id_movimiento == movimiento_id).first()

@router.patch("/{movimiento_id}/cancelar", response_model=MovimientoInventarioWithRelations)
def cancelar_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db)
):
    """
    Cancelar un movimiento
    - Solo se pueden cancelar movimientos PENDIENTES o AUTORIZADOS
    """
    db_movimiento = movimiento_inventario_crud.get_movimiento(db, movimiento_id)
    if not db_movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    if db_movimiento.estado not in ['PENDIENTE', 'AUTORIZADO']:
        raise HTTPException(
            status_code=400,
            detail=f"Solo se pueden cancelar movimientos PENDIENTES o AUTORIZADOS. Estado actual: {db_movimiento.estado}"
        )

    movimiento_update = MovimientoInventarioUpdate(estado=EstadoMovimientoEnum.CANCELADO)
    updated_movimiento = movimiento_inventario_crud.update_movimiento(
        db=db, movimiento_id=movimiento_id, movimiento_update=movimiento_update
    )

    # Cargar el movimiento con todas las relaciones
    return db.query(MovimientoInventario).options(
        joinedload(MovimientoInventario.tipo_movimiento),
        joinedload(MovimientoInventario.documento),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.producto),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_origen),
        joinedload(MovimientoInventario.detalles).joinedload(MovimientoDetalle.ubicacion_destino)
    ).filter(MovimientoInventario.id_movimiento == movimiento_id).first()

# ========================================
# ENDPOINTS CRUD - DETALLES
# ========================================

@router.get("/{movimiento_id}/detalles", response_model=List[MovimientoDetalleWithRelations])
def obtener_detalles_movimiento(
    movimiento_id: int,
    db: Session = Depends(get_db)
):
    """Obtener todos los detalles de un movimiento"""
    # Verificar que el movimiento existe
    movimiento = movimiento_inventario_crud.get_movimiento(db, movimiento_id)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    return db.query(MovimientoDetalle).filter(MovimientoDetalle.id_movimiento == movimiento_id).all()

@router.post("/{movimiento_id}/detalles", response_model=MovimientoDetalleResponse, status_code=201)
def crear_detalle_movimiento(
    movimiento_id: int,
    detalle: MovimientoDetalleCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo detalle para un movimiento
    - El movimiento no debe estar PROCESADO
    """
    # Verificar que el movimiento existe y no está procesado
    movimiento = movimiento_inventario_crud.get_movimiento(db, movimiento_id)
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")

    if movimiento.estado == 'PROCESADO':
        raise HTTPException(
            status_code=400,
            detail="No se pueden agregar detalles a un movimiento procesado"
        )

    # Validar producto
    producto = producto_crud.get_producto(db, detalle.id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Asignar el ID del movimiento
    detalle.id_movimiento = movimiento_id

    return movimiento_detalle_crud.create_detalle(db=db, detalle=detalle)

@router.put("/detalles/{detalle_id}", response_model=MovimientoDetalleResponse)
def actualizar_detalle_movimiento(
    detalle_id: int,
    detalle_update: MovimientoDetalleUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar detalle de movimiento
    - El movimiento no debe estar PROCESADO
    """
    # Verificar que el detalle existe
    db_detalle = movimiento_detalle_crud.get_detalle(db, detalle_id)
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    # Verificar que el movimiento no está procesado
    if db_detalle.movimiento.estado == 'PROCESADO':
        raise HTTPException(
            status_code=400,
            detail="No se pueden modificar detalles de un movimiento procesado"
        )

    updated_detalle = movimiento_detalle_crud.update_detalle(
        db=db, detalle_id=detalle_id, detalle_update=detalle_update
    )
    if not updated_detalle:
        raise HTTPException(status_code=404, detail="Error al actualizar el detalle")

    return updated_detalle

@router.delete("/detalles/{detalle_id}")
def eliminar_detalle_movimiento(
    detalle_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar detalle de movimiento
    - El movimiento no debe estar PROCESADO
    """
    # Verificar que el detalle existe
    db_detalle = movimiento_detalle_crud.get_detalle(db, detalle_id)
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    # Verificar que el movimiento no está procesado
    if db_detalle.movimiento.estado == 'PROCESADO':
        raise HTTPException(
            status_code=400,
            detail="No se pueden eliminar detalles de un movimiento procesado"
        )

    success = movimiento_detalle_crud.delete_detalle(db=db, detalle_id=detalle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Error al eliminar el detalle")

    return {"message": "Detalle eliminado correctamente"}

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_movimientos(
    estado: Optional[EstadoMovimientoEnum] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de movimientos"""
    query = db.query(MovimientoInventario)
    if estado:
        query = query.filter(MovimientoInventario.estado == estado.value)

    total = query.count()
    return {"total_movimientos": total}

@router.get("/stats/por-estado")
def estadisticas_por_estado(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de movimientos por estado"""
    from sqlalchemy import func

    stats = db.query(
        MovimientoInventario.estado,
        func.count(MovimientoInventario.id_movimiento).label('total_movimientos')
    ).group_by(MovimientoInventario.estado).all()

    return [
        {
            "estado": stat.estado,
            "total_movimientos": stat.total_movimientos or 0
        }
        for stat in stats
    ]

@router.get("/stats/por-tipo")
def estadisticas_por_tipo(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de movimientos por tipo"""
    from sqlalchemy import func

    stats = db.query(
        TipoMovimiento.nombre_tipo,
        TipoMovimiento.afecta_stock,
        func.count(MovimientoInventario.id_movimiento).label('total_movimientos')
    ).join(MovimientoInventario).group_by(
        TipoMovimiento.id_tipo_movimiento, TipoMovimiento.nombre_tipo, TipoMovimiento.afecta_stock
    ).filter(TipoMovimiento.activo == True).all()

    return [
        {
            "tipo_movimiento": stat.nombre_tipo,
            "afecta_stock": stat.afecta_stock,
            "total_movimientos": stat.total_movimientos or 0
        }
        for stat in stats
    ]

@router.get("/stats/por-usuario")
def estadisticas_por_usuario(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de movimientos por usuario"""
    from sqlalchemy import func

    stats = db.query(
        MovimientoInventario.id_usuario,
        func.count(MovimientoInventario.id_movimiento).label('total_movimientos'),
        func.count(func.nullif(MovimientoInventario.estado != 'PENDIENTE', False)).label('movimientos_procesados')
    ).group_by(MovimientoInventario.id_usuario).all()

    return [
        {
            "id_usuario": stat.id_usuario,
            "total_movimientos": stat.total_movimientos or 0,
            "movimientos_procesados": stat.movimientos_procesados or 0
        }
        for stat in stats
    ]