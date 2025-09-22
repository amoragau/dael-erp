from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from datetime import datetime, date
from database import get_db
from models import (
    PagosOrdenesCompra, OrdenCompra, EstadoOrdenCompra,
    ConciliacionOcFacturas, Proveedor, Usuarios
)
from schemas import (
    PagosOrdenesCompraCreate,
    PagosOrdenesCompraUpdate,
    PagosOrdenesCompraResponse,
    MetodoPago,
    EstadoPago
)

router = APIRouter()

# ========================================
# CRUD BÁSICO PARA PAGOS
# ========================================

@router.post("/", response_model=PagosOrdenesCompraResponse)
def create_pago(
    pago: PagosOrdenesCompraCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo pago de orden de compra"""

    # Verificar que la orden de compra existe
    orden = db.query(OrdenCompra).filter(OrdenCompra.id_orden_compra == pago.id_orden_compra).first()
    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden de compra no encontrada"
        )

    # Verificar que la orden está en estado que permite pagos (CONCILIADA)
    estado_orden = db.query(EstadoOrdenCompra).filter(
        EstadoOrdenCompra.id_estado == orden.id_estado
    ).first()

    if estado_orden and estado_orden.codigo_estado not in ["CONCILIADA", "FACTURADA"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede crear pago. La orden está en estado: {estado_orden.nombre_estado}"
        )

    # Verificar que no existe un número de pago duplicado
    existing_pago = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.numero_pago == pago.numero_pago,
        PagosOrdenesCompra.activo == True
    ).first()

    if existing_pago:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un pago con este número"
        )

    # Validar que el monto del pago no exceda el total de la orden
    pagos_anteriores = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.id_orden_compra == pago.id_orden_compra,
        PagosOrdenesCompra.estado != EstadoPago.CANCELADO,
        PagosOrdenesCompra.activo == True
    ).all()

    monto_pagado = sum(p.monto_pago for p in pagos_anteriores)
    if monto_pagado + pago.monto_pago > orden.total:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El monto del pago excede el saldo pendiente. Saldo disponible: {orden.total - monto_pagado}"
        )

    db_pago = PagosOrdenesCompra(**pago.dict())
    db.add(db_pago)
    db.commit()
    db.refresh(db_pago)

    return db_pago

@router.get("/{pago_id}", response_model=PagosOrdenesCompraResponse)
def get_pago(pago_id: int, db: Session = Depends(get_db)):
    """Obtener un pago por ID"""
    pago = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.id_pago == pago_id,
        PagosOrdenesCompra.activo == True
    ).first()

    if not pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado"
        )

    return pago

@router.get("/", response_model=List[PagosOrdenesCompraResponse])
def get_pagos(
    id_orden_compra: Optional[int] = None,
    estado: Optional[EstadoPago] = None,
    metodo_pago: Optional[MetodoPago] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener lista de pagos con filtros opcionales"""
    query = db.query(PagosOrdenesCompra).filter(PagosOrdenesCompra.activo == True)

    if id_orden_compra:
        query = query.filter(PagosOrdenesCompra.id_orden_compra == id_orden_compra)

    if estado:
        query = query.filter(PagosOrdenesCompra.estado == estado)

    if metodo_pago:
        query = query.filter(PagosOrdenesCompra.metodo_pago == metodo_pago)

    if fecha_desde:
        query = query.filter(PagosOrdenesCompra.fecha_pago >= fecha_desde)

    if fecha_hasta:
        query = query.filter(PagosOrdenesCompra.fecha_pago <= fecha_hasta)

    pagos = query.offset(skip).limit(limit).all()
    return pagos

@router.put("/{pago_id}", response_model=PagosOrdenesCompraResponse)
def update_pago(
    pago_id: int,
    pago: PagosOrdenesCompraUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un pago"""
    db_pago = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.id_pago == pago_id,
        PagosOrdenesCompra.activo == True
    ).first()

    if not db_pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado"
        )

    # No permitir modificar pagos confirmados
    if db_pago.estado == EstadoPago.CONFIRMADO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede modificar un pago confirmado"
        )

    update_data = pago.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_pago, field, value)

    db.commit()
    db.refresh(db_pago)

    return db_pago

@router.delete("/{pago_id}")
def delete_pago(pago_id: int, db: Session = Depends(get_db)):
    """Cancelar un pago"""
    db_pago = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.id_pago == pago_id,
        PagosOrdenesCompra.activo == True
    ).first()

    if not db_pago:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado"
        )

    # No permitir cancelar pagos confirmados
    if db_pago.estado == EstadoPago.CONFIRMADO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede cancelar un pago confirmado"
        )

    db_pago.estado = EstadoPago.CANCELADO
    db.commit()

    return {"message": "Pago cancelado exitosamente"}

# ========================================
# WORKFLOW DE PAGOS
# ========================================

@router.post("/{pago_id}/procesar")
def procesar_pago(
    pago_id: int,
    id_usuario_procesa: int,
    db: Session = Depends(get_db)
):
    """Procesar un pago pendiente"""
    pago = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.id_pago == pago_id,
        PagosOrdenesCompra.activo == True
    ).first()

    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    if pago.estado != EstadoPago.PENDIENTE:
        raise HTTPException(
            status_code=400,
            detail=f"El pago no está en estado pendiente. Estado actual: {pago.estado}"
        )

    # Cambiar estado a procesado
    pago.estado = EstadoPago.PROCESADO
    db.commit()

    return {
        "mensaje": "Pago procesado exitosamente",
        "id_pago": pago_id,
        "estado": pago.estado
    }

@router.post("/{pago_id}/confirmar")
def confirmar_pago(
    pago_id: int,
    id_usuario_confirma: int,
    referencia_confirmacion: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Confirmar un pago procesado"""
    pago = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.id_pago == pago_id,
        PagosOrdenesCompra.activo == True
    ).first()

    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    if pago.estado != EstadoPago.PROCESADO:
        raise HTTPException(
            status_code=400,
            detail=f"El pago debe estar en estado procesado. Estado actual: {pago.estado}"
        )

    try:
        # Confirmar pago
        pago.estado = EstadoPago.CONFIRMADO
        if referencia_confirmacion:
            pago.referencia_pago = referencia_confirmacion

        # Verificar si este es el pago final de la orden
        orden = db.query(OrdenCompra).filter(
            OrdenCompra.id_orden_compra == pago.id_orden_compra
        ).first()

        if orden:
            # Calcular total pagado incluyendo este pago
            pagos_confirmados = db.query(PagosOrdenesCompra).filter(
                PagosOrdenesCompra.id_orden_compra == pago.id_orden_compra,
                PagosOrdenesCompra.estado == EstadoPago.CONFIRMADO,
                PagosOrdenesCompra.activo == True
            ).all()

            total_pagado = sum(p.monto_pago for p in pagos_confirmados)

            # Si se pagó el total, cambiar estado de la orden a PAGADA
            if total_pagado >= orden.total:
                estado_pagada = db.query(EstadoOrdenCompra).filter(
                    EstadoOrdenCompra.codigo_estado == "PAGADA"
                ).first()

                if estado_pagada:
                    orden.id_estado = estado_pagada.id_estado

        db.commit()

        return {
            "mensaje": "Pago confirmado exitosamente",
            "id_pago": pago_id,
            "estado": pago.estado,
            "orden_pagada_completamente": total_pagado >= orden.total if orden else False
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error confirmando pago: {str(e)}"
        )

# ========================================
# GENERACIÓN AUTOMÁTICA DE PAGOS
# ========================================

@router.post("/generar-desde-conciliacion/{id_conciliacion}")
def generar_pago_desde_conciliacion(
    id_conciliacion: int,
    metodo_pago: MetodoPago,
    fecha_pago: date,
    id_usuario_autoriza: int,
    observaciones: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Generar pago automáticamente desde una conciliación aprobada"""

    # Verificar que la conciliación existe y está aprobada
    conciliacion = db.query(ConciliacionOcFacturas).filter(
        ConciliacionOcFacturas.id_conciliacion == id_conciliacion,
        ConciliacionOcFacturas.activo == True
    ).first()

    if not conciliacion:
        raise HTTPException(status_code=404, detail="Conciliación no encontrada")

    if conciliacion.estado != "CONCILIADA":
        raise HTTPException(
            status_code=400,
            detail="La conciliación debe estar aprobada para generar pago"
        )

    # Obtener la orden de compra
    orden = db.query(OrdenCompra).filter(
        OrdenCompra.id_orden_compra == conciliacion.id_orden_compra
    ).first()

    if not orden:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")

    # Verificar si ya existe un pago para esta orden
    pago_existente = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.id_orden_compra == orden.id_orden_compra,
        PagosOrdenesCompra.activo == True
    ).first()

    if pago_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un pago para esta orden de compra"
        )

    try:
        # Generar número de pago automático
        from datetime import datetime
        numero_pago = f"PAG-{fecha_pago.year}-{orden.id_orden_compra:06d}"

        # Crear pago
        pago_data = {
            "id_orden_compra": orden.id_orden_compra,
            "numero_pago": numero_pago,
            "fecha_pago": fecha_pago,
            "monto_pago": orden.total,  # Pagar el total de la orden
            "moneda": orden.moneda,
            "tipo_cambio": orden.tipo_cambio,
            "metodo_pago": metodo_pago,
            "estado": EstadoPago.PENDIENTE,
            "autorizado_por": id_usuario_autoriza,
            "fecha_autorizacion": datetime.now(),
            "observaciones": observaciones or f"Pago generado automáticamente desde conciliación {id_conciliacion}"
        }

        db_pago = PagosOrdenesCompra(**pago_data)
        db.add(db_pago)
        db.commit()
        db.refresh(db_pago)

        return {
            "mensaje": "Pago generado exitosamente desde conciliación",
            "id_pago": db_pago.id_pago,
            "numero_pago": db_pago.numero_pago,
            "monto": float(db_pago.monto_pago),
            "id_conciliacion": id_conciliacion
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando pago: {str(e)}"
        )

# ========================================
# CONSULTAS ESPECÍFICAS
# ========================================

@router.get("/orden/{id_orden_compra}", response_model=List[PagosOrdenesCompraResponse])
def get_pagos_por_orden(
    id_orden_compra: int,
    db: Session = Depends(get_db)
):
    """Obtener todos los pagos de una orden de compra específica"""

    # Verificar que la orden existe
    orden = db.query(OrdenCompra).filter(OrdenCompra.id_orden_compra == id_orden_compra).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")

    pagos = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.id_orden_compra == id_orden_compra,
        PagosOrdenesCompra.activo == True
    ).all()

    return pagos

@router.get("/resumen-pagos/{id_orden_compra}")
def get_resumen_pagos_orden(
    id_orden_compra: int,
    db: Session = Depends(get_db)
):
    """Obtener resumen de pagos para una orden de compra"""

    orden = db.query(OrdenCompra).filter(OrdenCompra.id_orden_compra == id_orden_compra).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")

    pagos = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.id_orden_compra == id_orden_compra,
        PagosOrdenesCompra.activo == True
    ).all()

    # Calcular totales por estado
    monto_pendiente = sum(p.monto_pago for p in pagos if p.estado == EstadoPago.PENDIENTE)
    monto_procesado = sum(p.monto_pago for p in pagos if p.estado == EstadoPago.PROCESADO)
    monto_confirmado = sum(p.monto_pago for p in pagos if p.estado == EstadoPago.CONFIRMADO)
    monto_cancelado = sum(p.monto_pago for p in pagos if p.estado == EstadoPago.CANCELADO)

    total_pagado = monto_confirmado
    saldo_pendiente = orden.total - total_pagado

    return {
        "orden_id": id_orden_compra,
        "monto_orden": float(orden.total),
        "total_pagos": len(pagos),
        "montos": {
            "pendiente": float(monto_pendiente),
            "procesado": float(monto_procesado),
            "confirmado": float(monto_confirmado),
            "cancelado": float(monto_cancelado)
        },
        "total_pagado": float(total_pagado),
        "saldo_pendiente": float(saldo_pendiente),
        "orden_pagada_completamente": saldo_pendiente <= 0,
        "pagos": pagos
    }

@router.get("/pendientes-confirmacion")
def get_pagos_pendientes_confirmacion(db: Session = Depends(get_db)):
    """Obtener pagos pendientes de confirmación"""

    pagos = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.estado == EstadoPago.PROCESADO,
        PagosOrdenesCompra.activo == True
    ).all()

    return {
        "total": len(pagos),
        "pagos": pagos
    }

@router.get("/reportes/por-metodo-pago")
def reporte_pagos_por_metodo(
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Reporte de pagos agrupados por método de pago"""

    query = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.estado == EstadoPago.CONFIRMADO,
        PagosOrdenesCompra.activo == True
    )

    if fecha_desde:
        query = query.filter(PagosOrdenesCompra.fecha_pago >= fecha_desde)

    if fecha_hasta:
        query = query.filter(PagosOrdenesCompra.fecha_pago <= fecha_hasta)

    pagos = query.all()

    # Agrupar por método de pago
    resumen = {}
    for pago in pagos:
        metodo = pago.metodo_pago
        if metodo not in resumen:
            resumen[metodo] = {
                "cantidad_pagos": 0,
                "monto_total": 0
            }

        resumen[metodo]["cantidad_pagos"] += 1
        resumen[metodo]["monto_total"] += float(pago.monto_pago)

    return {
        "periodo": {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta
        },
        "total_pagos": len(pagos),
        "monto_total_general": sum(float(p.monto_pago) for p in pagos),
        "resumen_por_metodo": resumen
    }

# ========================================
# VALIDACIONES Y UTILIDADES
# ========================================

@router.post("/validar-pago")
def validar_datos_pago(
    id_orden_compra: int,
    monto_pago: Decimal,
    metodo_pago: MetodoPago,
    db: Session = Depends(get_db)
):
    """Validar datos antes de crear un pago"""

    # Verificar orden
    orden = db.query(OrdenCompra).filter(OrdenCompra.id_orden_compra == id_orden_compra).first()
    if not orden:
        return {"valido": False, "error": "Orden de compra no encontrada"}

    # Verificar estado de la orden
    estado_orden = db.query(EstadoOrdenCompra).filter(
        EstadoOrdenCompra.id_estado == orden.id_estado
    ).first()

    if estado_orden and estado_orden.codigo_estado not in ["CONCILIADA", "FACTURADA"]:
        return {
            "valido": False,
            "error": f"La orden está en estado {estado_orden.nombre_estado}, no permite pagos"
        }

    # Calcular saldo disponible
    pagos_anteriores = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.id_orden_compra == id_orden_compra,
        PagosOrdenesCompra.estado != EstadoPago.CANCELADO,
        PagosOrdenesCompra.activo == True
    ).all()

    monto_pagado = sum(p.monto_pago for p in pagos_anteriores)
    saldo_disponible = orden.total - monto_pagado

    if monto_pago > saldo_disponible:
        return {
            "valido": False,
            "error": f"Monto excede saldo disponible. Saldo: {saldo_disponible}"
        }

    return {
        "valido": True,
        "orden": {
            "numero": orden.numero_orden,
            "total": float(orden.total),
            "moneda": orden.moneda
        },
        "saldo_disponible": float(saldo_disponible),
        "monto_a_pagar": float(monto_pago),
        "saldo_restante": float(saldo_disponible - monto_pago)
    }