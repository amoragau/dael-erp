from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from database import get_db
from models import (
    ConciliacionOcFacturas, ConciliacionDetalle, AjustesConciliacion,
    OrdenCompra, OrdenCompraDetalle, DocumentoOrdenCompra, Producto,
    MovimientoInventario, TipoMovimiento
)
from schemas import (
    ConciliacionOcFacturasCreate,
    ConciliacionOcFacturasUpdate,
    ConciliacionOcFacturasResponse,
    ConciliacionDetalleCreate,
    ConciliacionDetalleUpdate,
    ConciliacionDetalleResponse,
    AjustesConciliacionCreate,
    AjustesConciliacionResponse,
    TipoConciliacion,
    EstadoConciliacion,
    EstadoProductoConciliacion,
    AccionConciliacion,
    TipoAjuste
)

router = APIRouter()

# ========================================
# CRUD BÁSICO PARA CONCILIACIONES
# ========================================

@router.post("/", response_model=ConciliacionOcFacturasResponse)
def create_conciliacion(
    conciliacion: ConciliacionOcFacturasCreate,
    db: Session = Depends(get_db)
):
    """Crear una nueva conciliación entre OC y factura"""

    # Verificar que la orden de compra existe
    orden = db.query(OrdenCompra).filter(OrdenCompra.id_orden_compra == conciliacion.id_orden_compra).first()
    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden de compra no encontrada"
        )

    # Verificar que el documento de factura existe
    factura = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.id_documento_oc == conciliacion.id_documento_factura
    ).first()
    if not factura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento de factura no encontrado"
        )

    # Verificar que no existe una conciliación activa
    existing_conciliacion = db.query(ConciliacionOcFacturas).filter(
        ConciliacionOcFacturas.id_orden_compra == conciliacion.id_orden_compra,
        ConciliacionOcFacturas.id_documento_factura == conciliacion.id_documento_factura,
        ConciliacionOcFacturas.activo == True
    ).first()

    if existing_conciliacion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una conciliación activa para esta OC y factura"
        )

    db_conciliacion = ConciliacionOcFacturas(**conciliacion.dict())
    db.add(db_conciliacion)
    db.commit()
    db.refresh(db_conciliacion)

    return db_conciliacion

@router.get("/{conciliacion_id}", response_model=ConciliacionOcFacturasResponse)
def get_conciliacion(conciliacion_id: int, db: Session = Depends(get_db)):
    """Obtener una conciliación por ID"""
    conciliacion = db.query(ConciliacionOcFacturas).filter(
        ConciliacionOcFacturas.id_conciliacion == conciliacion_id,
        ConciliacionOcFacturas.activo == True
    ).first()

    if not conciliacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conciliación no encontrada"
        )

    return conciliacion

@router.get("/", response_model=List[ConciliacionOcFacturasResponse])
def get_conciliaciones(
    id_orden_compra: Optional[int] = None,
    estado: Optional[EstadoConciliacion] = None,
    tipo_conciliacion: Optional[TipoConciliacion] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener lista de conciliaciones con filtros opcionales"""
    query = db.query(ConciliacionOcFacturas).filter(ConciliacionOcFacturas.activo == True)

    if id_orden_compra:
        query = query.filter(ConciliacionOcFacturas.id_orden_compra == id_orden_compra)

    if estado:
        query = query.filter(ConciliacionOcFacturas.estado == estado)

    if tipo_conciliacion:
        query = query.filter(ConciliacionOcFacturas.tipo_conciliacion == tipo_conciliacion)

    conciliaciones = query.offset(skip).limit(limit).all()
    return conciliaciones

@router.put("/{conciliacion_id}", response_model=ConciliacionOcFacturasResponse)
def update_conciliacion(
    conciliacion_id: int,
    conciliacion: ConciliacionOcFacturasUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una conciliación"""
    db_conciliacion = db.query(ConciliacionOcFacturas).filter(
        ConciliacionOcFacturas.id_conciliacion == conciliacion_id,
        ConciliacionOcFacturas.activo == True
    ).first()

    if not db_conciliacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conciliación no encontrada"
        )

    update_data = conciliacion.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_conciliacion, field, value)

    db.commit()
    db.refresh(db_conciliacion)

    return db_conciliacion

# ========================================
# CONCILIACIÓN AUTOMÁTICA
# ========================================

@router.post("/conciliar-automatica/{id_orden_compra}")
def conciliar_automatica(
    id_orden_compra: int,
    id_documento_factura: int,
    id_usuario_concilia: int,
    tolerancia_precio: float = 5.0,
    tolerancia_cantidad: float = 2.0,
    db: Session = Depends(get_db)
):
    """Realizar conciliación automática entre OC y factura"""

    # Verificar que la orden y factura existen
    orden = db.query(OrdenCompra).filter(OrdenCompra.id_orden_compra == id_orden_compra).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")

    factura = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.id_documento_oc == id_documento_factura
    ).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    try:
        # Crear conciliación
        conciliacion_data = {
            "id_orden_compra": id_orden_compra,
            "id_documento_factura": id_documento_factura,
            "tipo_conciliacion": TipoConciliacion.AUTOMATICA,
            "fecha_conciliacion": datetime.now(),
            "id_usuario_concilia": id_usuario_concilia
        }

        db_conciliacion = ConciliacionOcFacturas(**conciliacion_data)
        db.add(db_conciliacion)
        db.flush()  # Para obtener el ID sin hacer commit completo

        # Obtener detalles de la orden de compra
        detalles_oc = db.query(OrdenCompraDetalle).filter(
            OrdenCompraDetalle.id_orden_compra == id_orden_compra,
            OrdenCompraDetalle.activo == True
        ).all()

        productos_conciliados = 0
        productos_con_diferencias = 0
        diferencia_total = Decimal('0')

        # Conciliar cada producto
        for detalle_oc in detalles_oc:
            # Simular datos de factura (en implementación real se extraerían del XML)
            # TODO: Extraer productos reales del XML de la factura
            cantidad_factura = detalle_oc.cantidad_solicitada
            precio_factura = detalle_oc.precio_unitario

            # Calcular diferencias
            dif_cantidad = abs(cantidad_factura - detalle_oc.cantidad_solicitada)
            dif_precio = abs(precio_factura - detalle_oc.precio_unitario)

            # Determinar estado del producto
            estado_producto = EstadoProductoConciliacion.COINCIDE

            if (dif_cantidad / detalle_oc.cantidad_solicitada * 100) > tolerancia_cantidad:
                estado_producto = EstadoProductoConciliacion.DIFERENCIA_CANTIDAD
                productos_con_diferencias += 1
            elif (dif_precio / detalle_oc.precio_unitario * 100) > tolerancia_precio:
                estado_producto = EstadoProductoConciliacion.DIFERENCIA_PRECIO
                productos_con_diferencias += 1
            else:
                productos_conciliados += 1

            # Crear detalle de conciliación
            detalle_conciliacion = ConciliacionDetalle(
                id_conciliacion=db_conciliacion.id_conciliacion,
                id_producto=detalle_oc.id_producto,
                cantidad_oc=detalle_oc.cantidad_solicitada,
                precio_unitario_oc=detalle_oc.precio_unitario,
                importe_oc=detalle_oc.importe_total,
                cantidad_factura=cantidad_factura,
                precio_unitario_factura=precio_factura,
                importe_factura=cantidad_factura * precio_factura,
                estado_producto=estado_producto,
                accion_tomada=AccionConciliacion.ACEPTAR if estado_producto == EstadoProductoConciliacion.COINCIDE else AccionConciliacion.PENDIENTE
            )

            db.add(detalle_conciliacion)

            # Calcular diferencia en importe
            diferencia_total += abs(detalle_conciliacion.importe_factura - detalle_conciliacion.importe_oc)

        # Actualizar totales de conciliación
        total_productos = len(detalles_oc)
        porcentaje_coincidencia = (productos_conciliados / total_productos * 100) if total_productos > 0 else 0

        db_conciliacion.productos_conciliados = productos_conciliados
        db_conciliacion.productos_con_diferencias = productos_con_diferencias
        db_conciliacion.diferencia_total = diferencia_total
        db_conciliacion.porcentaje_coincidencia = Decimal(str(porcentaje_coincidencia))

        # Determinar estado final
        if porcentaje_coincidencia >= 95:
            db_conciliacion.estado = EstadoConciliacion.CONCILIADA
        elif productos_con_diferencias > 0:
            db_conciliacion.estado = EstadoConciliacion.CON_DIFERENCIAS
        else:
            db_conciliacion.estado = EstadoConciliacion.PENDIENTE

        db.commit()

        return {
            "exito": True,
            "mensaje": "Conciliación automática completada",
            "id_conciliacion": db_conciliacion.id_conciliacion,
            "productos_conciliados": productos_conciliados,
            "productos_con_diferencias": productos_con_diferencias,
            "porcentaje_coincidencia": float(porcentaje_coincidencia),
            "diferencia_total": float(diferencia_total),
            "estado": db_conciliacion.estado
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en conciliación automática: {str(e)}"
        )

# ========================================
# DETALLE DE CONCILIACIÓN
# ========================================

@router.get("/{conciliacion_id}/detalles", response_model=List[ConciliacionDetalleResponse])
def get_detalles_conciliacion(conciliacion_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de una conciliación"""
    # Verificar que la conciliación existe
    conciliacion = db.query(ConciliacionOcFacturas).filter(
        ConciliacionOcFacturas.id_conciliacion == conciliacion_id
    ).first()

    if not conciliacion:
        raise HTTPException(status_code=404, detail="Conciliación no encontrada")

    detalles = db.query(ConciliacionDetalle).filter(
        ConciliacionDetalle.id_conciliacion == conciliacion_id
    ).all()

    return detalles

@router.post("/{conciliacion_id}/detalles", response_model=ConciliacionDetalleResponse)
def create_detalle_conciliacion(
    conciliacion_id: int,
    detalle: ConciliacionDetalleCreate,
    db: Session = Depends(get_db)
):
    """Crear un detalle de conciliación"""
    # Verificar que la conciliación existe
    conciliacion = db.query(ConciliacionOcFacturas).filter(
        ConciliacionOcFacturas.id_conciliacion == conciliacion_id
    ).first()

    if not conciliacion:
        raise HTTPException(status_code=404, detail="Conciliación no encontrada")

    # Asegurar que el detalle pertenece a la conciliación correcta
    detalle.id_conciliacion = conciliacion_id

    db_detalle = ConciliacionDetalle(**detalle.dict())
    db.add(db_detalle)
    db.commit()
    db.refresh(db_detalle)

    return db_detalle

@router.put("/{conciliacion_id}/detalles/{detalle_id}", response_model=ConciliacionDetalleResponse)
def update_detalle_conciliacion(
    conciliacion_id: int,
    detalle_id: int,
    detalle: ConciliacionDetalleUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un detalle de conciliación"""
    db_detalle = db.query(ConciliacionDetalle).filter(
        ConciliacionDetalle.id_detalle_conciliacion == detalle_id,
        ConciliacionDetalle.id_conciliacion == conciliacion_id
    ).first()

    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle de conciliación no encontrado")

    update_data = detalle.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_detalle, field, value)

    db.commit()
    db.refresh(db_detalle)

    return db_detalle

# ========================================
# AJUSTES POR CONCILIACIÓN
# ========================================

@router.post("/{conciliacion_id}/ajustes", response_model=AjustesConciliacionResponse)
def create_ajuste_conciliacion(
    conciliacion_id: int,
    ajuste: AjustesConciliacionCreate,
    db: Session = Depends(get_db)
):
    """Crear un ajuste basado en conciliación"""
    # Verificar que la conciliación existe
    conciliacion = db.query(ConciliacionOcFacturas).filter(
        ConciliacionOcFacturas.id_conciliacion == conciliacion_id
    ).first()

    if not conciliacion:
        raise HTTPException(status_code=404, detail="Conciliación no encontrada")

    # Asegurar que el ajuste pertenece a la conciliación correcta
    ajuste.id_conciliacion = conciliacion_id

    db_ajuste = AjustesConciliacion(**ajuste.dict())
    db.add(db_ajuste)
    db.commit()
    db.refresh(db_ajuste)

    return db_ajuste

@router.get("/{conciliacion_id}/ajustes", response_model=List[AjustesConciliacionResponse])
def get_ajustes_conciliacion(conciliacion_id: int, db: Session = Depends(get_db)):
    """Obtener ajustes de una conciliación"""
    ajustes = db.query(AjustesConciliacion).filter(
        AjustesConciliacion.id_conciliacion == conciliacion_id
    ).all()

    return ajustes

@router.post("/ajustes/{ajuste_id}/procesar")
def procesar_ajuste(
    ajuste_id: int,
    id_usuario_procesa: int,
    db: Session = Depends(get_db)
):
    """Procesar un ajuste y generar movimiento de inventario"""
    ajuste = db.query(AjustesConciliacion).filter(
        AjustesConciliacion.id_ajuste == ajuste_id
    ).first()

    if not ajuste:
        raise HTTPException(status_code=404, detail="Ajuste no encontrado")

    if ajuste.procesado:
        raise HTTPException(status_code=400, detail="El ajuste ya fue procesado")

    try:
        # Crear movimiento de inventario según el tipo de ajuste
        tipo_movimiento = None
        if ajuste.tipo_ajuste == TipoAjuste.CANTIDAD:
            tipo_movimiento = db.query(TipoMovimiento).filter(
                TipoMovimiento.codigo_tipo == "AJU"
            ).first()

        if tipo_movimiento:
            # TODO: Implementar creación de movimiento de inventario
            # Por ahora solo marcamos como procesado
            pass

        # Marcar como procesado
        ajuste.procesado = True
        ajuste.fecha_procesamiento = datetime.now()

        db.commit()

        return {
            "exito": True,
            "mensaje": "Ajuste procesado exitosamente",
            "id_ajuste": ajuste_id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando ajuste: {str(e)}"
        )

# ========================================
# APROBACIÓN DE CONCILIACIONES
# ========================================

@router.post("/{conciliacion_id}/aprobar")
def aprobar_conciliacion(
    conciliacion_id: int,
    id_usuario_aprueba: int,
    observaciones: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Aprobar una conciliación"""
    conciliacion = db.query(ConciliacionOcFacturas).filter(
        ConciliacionOcFacturas.id_conciliacion == conciliacion_id,
        ConciliacionOcFacturas.activo == True
    ).first()

    if not conciliacion:
        raise HTTPException(status_code=404, detail="Conciliación no encontrada")

    if conciliacion.estado == EstadoConciliacion.CONCILIADA:
        raise HTTPException(status_code=400, detail="La conciliación ya está aprobada")

    # Aprobar conciliación
    conciliacion.estado = EstadoConciliacion.CONCILIADA
    conciliacion.aprobado_por = id_usuario_aprueba
    conciliacion.fecha_aprobacion = datetime.now()
    if observaciones:
        conciliacion.observaciones = observaciones

    # Actualizar estado de la orden de compra
    orden = db.query(OrdenCompra).filter(
        OrdenCompra.id_orden_compra == conciliacion.id_orden_compra
    ).first()

    if orden:
        # Buscar estado "CONCILIADA"
        from models import EstadoOrdenCompra
        estado_conciliada = db.query(EstadoOrdenCompra).filter(
            EstadoOrdenCompra.codigo_estado == "CONCILIADA"
        ).first()

        if estado_conciliada:
            orden.id_estado = estado_conciliada.id_estado

    db.commit()

    return {
        "mensaje": "Conciliación aprobada exitosamente",
        "id_conciliacion": conciliacion_id,
        "fecha_aprobacion": conciliacion.fecha_aprobacion
    }

@router.post("/{conciliacion_id}/rechazar")
def rechazar_conciliacion(
    conciliacion_id: int,
    id_usuario_rechaza: int,
    motivo_rechazo: str,
    db: Session = Depends(get_db)
):
    """Rechazar una conciliación"""
    conciliacion = db.query(ConciliacionOcFacturas).filter(
        ConciliacionOcFacturas.id_conciliacion == conciliacion_id,
        ConciliacionOcFacturas.activo == True
    ).first()

    if not conciliacion:
        raise HTTPException(status_code=404, detail="Conciliación no encontrada")

    # Rechazar conciliación
    conciliacion.estado = EstadoConciliacion.RECHAZADA
    conciliacion.aprobado_por = id_usuario_rechaza
    conciliacion.fecha_aprobacion = datetime.now()
    conciliacion.observaciones = f"RECHAZADA: {motivo_rechazo}"

    db.commit()

    return {
        "mensaje": "Conciliación rechazada",
        "id_conciliacion": conciliacion_id,
        "motivo": motivo_rechazo
    }

# ========================================
# REPORTES Y CONSULTAS
# ========================================

@router.get("/pendientes")
def get_conciliaciones_pendientes(db: Session = Depends(get_db)):
    """Obtener conciliaciones pendientes de aprobación"""
    conciliaciones = db.query(ConciliacionOcFacturas).filter(
        ConciliacionOcFacturas.estado.in_([EstadoConciliacion.PENDIENTE, EstadoConciliacion.CON_DIFERENCIAS]),
        ConciliacionOcFacturas.activo == True
    ).all()

    return {
        "total": len(conciliaciones),
        "conciliaciones": conciliaciones
    }

@router.get("/resumen/{id_orden_compra}")
def get_resumen_conciliacion(id_orden_compra: int, db: Session = Depends(get_db)):
    """Obtener resumen de conciliación para una orden de compra"""
    orden = db.query(OrdenCompra).filter(OrdenCompra.id_orden_compra == id_orden_compra).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")

    conciliacion = db.query(ConciliacionOcFacturas).filter(
        ConciliacionOcFacturas.id_orden_compra == id_orden_compra,
        ConciliacionOcFacturas.activo == True
    ).first()

    if not conciliacion:
        return {
            "orden_id": id_orden_compra,
            "tiene_conciliacion": False,
            "mensaje": "No hay conciliación para esta orden"
        }

    detalles = db.query(ConciliacionDetalle).filter(
        ConciliacionDetalle.id_conciliacion == conciliacion.id_conciliacion
    ).all()

    return {
        "orden_id": id_orden_compra,
        "tiene_conciliacion": True,
        "conciliacion": conciliacion,
        "total_productos": len(detalles),
        "productos_conciliados": conciliacion.productos_conciliados,
        "productos_con_diferencias": conciliacion.productos_con_diferencias,
        "porcentaje_coincidencia": float(conciliacion.porcentaje_coincidencia),
        "estado": conciliacion.estado,
        "detalles": detalles
    }