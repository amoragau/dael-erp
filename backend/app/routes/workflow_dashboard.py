from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, case, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from database import get_db
from models import (
    OrdenCompra, EstadoOrdenCompra, RecepcionMercancia, DocumentoOrdenCompra,
    ConciliacionOcFacturas, PagosOrdenesCompra, Proveedor, Usuarios,
    HistorialEstadosOc
)
from schemas import (
    WorkflowOrdenCompraResponse, OrdenPendientePorPasoResponse,
    EstadoDocumento, EstadoConciliacion, EstadoPago
)

router = APIRouter()

# ========================================
# DASHBOARD PRINCIPAL DEL WORKFLOW
# ========================================

@router.get("/resumen-general")
def get_resumen_general_workflow(db: Session = Depends(get_db)):
    """Obtener resumen general del workflow de órdenes de compra"""

    # Contar órdenes por estado
    estados_query = db.query(
        EstadoOrdenCompra.codigo_estado,
        EstadoOrdenCompra.nombre_estado,
        func.count(OrdenCompra.id_orden_compra).label('cantidad')
    ).join(
        OrdenCompra, OrdenCompra.id_estado == EstadoOrdenCompra.id_estado
    ).filter(
        OrdenCompra.activo == True
    ).group_by(
        EstadoOrdenCompra.codigo_estado,
        EstadoOrdenCompra.nombre_estado
    ).all()

    estados_resumen = {estado.codigo_estado: {"nombre": estado.nombre_estado, "cantidad": estado.cantidad} for estado in estados_query}

    # Calcular KPIs del workflow
    total_ordenes = sum(estado["cantidad"] for estado in estados_resumen.values())

    # Órdenes en cada paso del workflow
    paso_1 = estados_resumen.get("BORRADOR", {"cantidad": 0})["cantidad"] + estados_resumen.get("PENDIENTE", {"cantidad": 0})["cantidad"]
    paso_2 = estados_resumen.get("APROBADA", {"cantidad": 0})["cantidad"] + estados_resumen.get("ENVIADA", {"cantidad": 0})["cantidad"]
    paso_3 = estados_resumen.get("RECIBIDA", {"cantidad": 0})["cantidad"]
    paso_4 = estados_resumen.get("FACTURADA", {"cantidad": 0})["cantidad"]
    paso_5 = estados_resumen.get("CONCILIADA", {"cantidad": 0})["cantidad"]
    completadas = estados_resumen.get("PAGADA", {"cantidad": 0})["cantidad"]

    # Documentos pendientes de procesar
    docs_pendientes = db.query(func.count(DocumentoOrdenCompra.id_documento_oc)).filter(
        DocumentoOrdenCompra.estado == EstadoDocumento.PENDIENTE,
        DocumentoOrdenCompra.activo == True
    ).scalar()

    # Conciliaciones pendientes
    conciliaciones_pendientes = db.query(func.count(ConciliacionOcFacturas.id_conciliacion)).filter(
        ConciliacionOcFacturas.estado.in_([EstadoConciliacion.PENDIENTE, EstadoConciliacion.CON_DIFERENCIAS]),
        ConciliacionOcFacturas.activo == True
    ).scalar()

    # Pagos pendientes
    pagos_pendientes = db.query(func.count(PagosOrdenesCompra.id_pago)).filter(
        PagosOrdenesCompra.estado == EstadoPago.PROCESADO,
        PagosOrdenesCompra.activo == True
    ).scalar()

    return {
        "resumen_general": {
            "total_ordenes": total_ordenes,
            "ordenes_completadas": completadas,
            "porcentaje_completado": round((completadas / total_ordenes * 100) if total_ordenes > 0 else 0, 2)
        },
        "progreso_workflow": {
            "paso_1_orden_compra": paso_1,
            "paso_2_recepcion": paso_2,
            "paso_3_facturacion": paso_3,
            "paso_4_conciliacion": paso_4,
            "paso_5_pago": paso_5,
            "completadas": completadas
        },
        "pendientes_atencion": {
            "documentos_por_procesar": docs_pendientes,
            "conciliaciones_pendientes": conciliaciones_pendientes,
            "pagos_por_confirmar": pagos_pendientes
        },
        "estados_detallados": estados_resumen
    }

@router.get("/ordenes-workflow", response_model=List[WorkflowOrdenCompraResponse])
def get_ordenes_workflow(
    estado: Optional[str] = None,
    proveedor_id: Optional[int] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener órdenes con información completa del workflow"""

    # Query base usando las vistas creadas en la base de datos
    query = db.query(
        OrdenCompra.id_orden_compra,
        OrdenCompra.numero_orden,
        Proveedor.nombre_proveedor,
        EstadoOrdenCompra.nombre_estado,
        EstadoOrdenCompra.codigo_estado,
        OrdenCompra.fecha_orden,
        OrdenCompra.total.label('monto_orden'),
        RecepcionMercancia.fecha_recepcion,
        RecepcionMercancia.recepcion_completa,
        DocumentoOrdenCompra.fecha_documento.label('fecha_factura'),
        DocumentoOrdenCompra.total.label('monto_factura'),
        DocumentoOrdenCompra.estado.label('estado_factura'),
        ConciliacionOcFacturas.fecha_conciliacion,
        ConciliacionOcFacturas.estado.label('estado_conciliacion'),
        ConciliacionOcFacturas.porcentaje_coincidencia,
        PagosOrdenesCompra.fecha_pago,
        PagosOrdenesCompra.monto_pago,
        PagosOrdenesCompra.estado.label('estado_pago')
    ).select_from(OrdenCompra).join(
        Proveedor, OrdenCompra.id_proveedor == Proveedor.id_proveedor
    ).join(
        EstadoOrdenCompra, OrdenCompra.id_estado == EstadoOrdenCompra.id_estado
    ).outerjoin(
        RecepcionMercancia, OrdenCompra.id_orden_compra == RecepcionMercancia.id_orden_compra
    ).outerjoin(
        DocumentoOrdenCompra, and_(
            OrdenCompra.id_orden_compra == DocumentoOrdenCompra.id_orden_compra,
            DocumentoOrdenCompra.tipo_documento == 'FACTURA',
            DocumentoOrdenCompra.activo == True
        )
    ).outerjoin(
        ConciliacionOcFacturas, and_(
            OrdenCompra.id_orden_compra == ConciliacionOcFacturas.id_orden_compra,
            ConciliacionOcFacturas.activo == True
        )
    ).outerjoin(
        PagosOrdenesCompra, and_(
            OrdenCompra.id_orden_compra == PagosOrdenesCompra.id_orden_compra,
            PagosOrdenesCompra.activo == True
        )
    ).filter(OrdenCompra.activo == True)

    # Aplicar filtros
    if estado:
        query = query.filter(EstadoOrdenCompra.codigo_estado == estado)

    if proveedor_id:
        query = query.filter(OrdenCompra.id_proveedor == proveedor_id)

    if fecha_desde:
        query = query.filter(OrdenCompra.fecha_orden >= fecha_desde)

    if fecha_hasta:
        query = query.filter(OrdenCompra.fecha_orden <= fecha_hasta)

    # Ejecutar query con paginación
    resultados = query.offset(skip).limit(limit).all()

    # Convertir a formato de respuesta
    ordenes_workflow = []
    for resultado in resultados:
        # Calcular indicadores de progreso
        paso_1_completado = 1 if resultado.codigo_estado not in ['BORRADOR', 'PENDIENTE'] else 0
        paso_2_completado = 1 if resultado.fecha_recepcion and resultado.recepcion_completa else 0
        paso_3_completado = 1 if resultado.fecha_factura and resultado.estado_factura == 'PROCESADO' else 0
        paso_4_completado = 1 if resultado.fecha_conciliacion and resultado.estado_conciliacion == 'CONCILIADA' else 0
        paso_5_completado = 1 if resultado.fecha_pago and resultado.estado_pago == 'CONFIRMADO' else 0

        orden_workflow = {
            "id_orden_compra": resultado.id_orden_compra,
            "numero_orden": resultado.numero_orden,
            "nombre_proveedor": resultado.nombre_proveedor,
            "nombre_estado": resultado.nombre_estado,
            "codigo_estado": resultado.codigo_estado,
            "fecha_orden": resultado.fecha_orden,
            "monto_orden": resultado.monto_orden,
            "fecha_recepcion": resultado.fecha_recepcion,
            "recepcion_completa": resultado.recepcion_completa,
            "fecha_factura": resultado.fecha_factura,
            "monto_factura": resultado.monto_factura,
            "estado_factura": resultado.estado_factura,
            "fecha_conciliacion": resultado.fecha_conciliacion,
            "estado_conciliacion": resultado.estado_conciliacion,
            "porcentaje_coincidencia": resultado.porcentaje_coincidencia,
            "fecha_pago": resultado.fecha_pago,
            "monto_pago": resultado.monto_pago,
            "estado_pago": resultado.estado_pago,
            "paso_1_completado": paso_1_completado,
            "paso_2_completado": paso_2_completado,
            "paso_3_completado": paso_3_completado,
            "paso_4_completado": paso_4_completado,
            "paso_5_completado": paso_5_completado
        }

        ordenes_workflow.append(orden_workflow)

    return ordenes_workflow

@router.get("/pendientes-por-paso", response_model=List[OrdenPendientePorPasoResponse])
def get_ordenes_pendientes_por_paso(db: Session = Depends(get_db)):
    """Obtener órdenes pendientes agrupadas por paso del workflow"""

    # Paso 1: Órdenes pendientes de aprobación
    paso_1 = db.query(func.count(OrdenCompra.id_orden_compra)).join(
        EstadoOrdenCompra, OrdenCompra.id_estado == EstadoOrdenCompra.id_estado
    ).filter(
        OrdenCompra.activo == True,
        EstadoOrdenCompra.codigo_estado.in_(['BORRADOR', 'PENDIENTE'])
    ).scalar()

    # Paso 2: Órdenes pendientes de recepción
    paso_2 = db.query(func.count(OrdenCompra.id_orden_compra)).join(
        EstadoOrdenCompra, OrdenCompra.id_estado == EstadoOrdenCompra.id_estado
    ).outerjoin(
        RecepcionMercancia, OrdenCompra.id_orden_compra == RecepcionMercancia.id_orden_compra
    ).filter(
        OrdenCompra.activo == True,
        EstadoOrdenCompra.codigo_estado.in_(['APROBADA', 'ENVIADA']),
        or_(
            RecepcionMercancia.id_recepcion.is_(None),
            RecepcionMercancia.recepcion_completa == False
        )
    ).scalar()

    # Paso 3: Órdenes pendientes de facturación
    paso_3 = db.query(func.count(OrdenCompra.id_orden_compra)).join(
        EstadoOrdenCompra, OrdenCompra.id_estado == EstadoOrdenCompra.id_estado
    ).outerjoin(
        DocumentoOrdenCompra, and_(
            OrdenCompra.id_orden_compra == DocumentoOrdenCompra.id_orden_compra,
            DocumentoOrdenCompra.tipo_documento == 'FACTURA',
            DocumentoOrdenCompra.activo == True
        )
    ).filter(
        OrdenCompra.activo == True,
        EstadoOrdenCompra.codigo_estado == 'RECIBIDA',
        DocumentoOrdenCompra.id_documento_oc.is_(None)
    ).scalar()

    # Paso 4: Órdenes pendientes de conciliación
    paso_4 = db.query(func.count(OrdenCompra.id_orden_compra)).join(
        EstadoOrdenCompra, OrdenCompra.id_estado == EstadoOrdenCompra.id_estado
    ).outerjoin(
        ConciliacionOcFacturas, and_(
            OrdenCompra.id_orden_compra == ConciliacionOcFacturas.id_orden_compra,
            ConciliacionOcFacturas.activo == True
        )
    ).filter(
        OrdenCompra.activo == True,
        EstadoOrdenCompra.codigo_estado == 'FACTURADA',
        or_(
            ConciliacionOcFacturas.id_conciliacion.is_(None),
            ConciliacionOcFacturas.estado != 'CONCILIADA'
        )
    ).scalar()

    # Paso 5: Órdenes pendientes de pago
    paso_5 = db.query(func.count(OrdenCompra.id_orden_compra)).join(
        EstadoOrdenCompra, OrdenCompra.id_estado == EstadoOrdenCompra.id_estado
    ).outerjoin(
        PagosOrdenesCompra, and_(
            OrdenCompra.id_orden_compra == PagosOrdenesCompra.id_orden_compra,
            PagosOrdenesCompra.activo == True
        )
    ).filter(
        OrdenCompra.activo == True,
        EstadoOrdenCompra.codigo_estado == 'CONCILIADA',
        or_(
            PagosOrdenesCompra.id_pago.is_(None),
            PagosOrdenesCompra.estado != 'CONFIRMADO'
        )
    ).scalar()

    return [
        {
            "paso": "Paso 1: Orden de Compra",
            "cantidad_pendiente": paso_1,
            "estados_incluidos": "BORRADOR,PENDIENTE"
        },
        {
            "paso": "Paso 2: Recepción de Mercancía",
            "cantidad_pendiente": paso_2,
            "estados_incluidos": "APROBADA,ENVIADA"
        },
        {
            "paso": "Paso 3: Recepción de Factura",
            "cantidad_pendiente": paso_3,
            "estados_incluidos": "RECIBIDA"
        },
        {
            "paso": "Paso 4: Conciliación",
            "cantidad_pendiente": paso_4,
            "estados_incluidos": "FACTURADA"
        },
        {
            "paso": "Paso 5: Pago",
            "cantidad_pendiente": paso_5,
            "estados_incluidos": "CONCILIADA"
        }
    ]

# ========================================
# MÉTRICAS Y ANALÍTICAS
# ========================================

@router.get("/metricas-tiempo-promedio")
def get_metricas_tiempo_promedio(
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Obtener métricas de tiempo promedio por paso del workflow"""

    # Si no se proporcionan fechas, usar los últimos 3 meses
    if not fecha_hasta:
        fecha_hasta = date.today()
    if not fecha_desde:
        fecha_desde = fecha_hasta - timedelta(days=90)

    # Query base para órdenes en el período
    ordenes_periodo = db.query(OrdenCompra).filter(
        OrdenCompra.fecha_orden >= fecha_desde,
        OrdenCompra.fecha_orden <= fecha_hasta,
        OrdenCompra.activo == True
    ).subquery()

    # Calcular tiempo promedio entre estados usando el historial
    # TODO: Implementar cálculo preciso usando historial_estados_oc
    # Por ahora retornamos valores simulados

    return {
        "periodo": {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta
        },
        "tiempos_promedio_dias": {
            "orden_a_aprobacion": 2.5,
            "aprobacion_a_recepcion": 7.2,
            "recepcion_a_facturacion": 3.1,
            "facturacion_a_conciliacion": 4.8,
            "conciliacion_a_pago": 5.5,
            "total_workflow": 23.1
        },
        "ordenes_analizadas": db.query(func.count()).select_from(ordenes_periodo).scalar()
    }

@router.get("/eficiencia-workflow")
def get_eficiencia_workflow(
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Calcular métricas de eficiencia del workflow"""

    if not fecha_hasta:
        fecha_hasta = date.today()
    if not fecha_desde:
        fecha_desde = fecha_hasta - timedelta(days=30)

    # Órdenes iniciadas en el período
    ordenes_iniciadas = db.query(func.count(OrdenCompra.id_orden_compra)).filter(
        OrdenCompra.fecha_orden >= fecha_desde,
        OrdenCompra.fecha_orden <= fecha_hasta,
        OrdenCompra.activo == True
    ).scalar()

    # Órdenes completadas en el período
    ordenes_completadas = db.query(func.count(OrdenCompra.id_orden_compra)).join(
        EstadoOrdenCompra, OrdenCompra.id_estado == EstadoOrdenCompra.id_estado
    ).filter(
        OrdenCompra.fecha_orden >= fecha_desde,
        OrdenCompra.fecha_orden <= fecha_hasta,
        OrdenCompra.activo == True,
        EstadoOrdenCompra.codigo_estado == 'PAGADA'
    ).scalar()

    # Órdenes con problemas (conciliaciones con diferencias)
    ordenes_con_problemas = db.query(func.count(ConciliacionOcFacturas.id_conciliacion)).join(
        OrdenCompra, ConciliacionOcFacturas.id_orden_compra == OrdenCompra.id_orden_compra
    ).filter(
        OrdenCompra.fecha_orden >= fecha_desde,
        OrdenCompra.fecha_orden <= fecha_hasta,
        ConciliacionOcFacturas.estado == 'CON_DIFERENCIAS',
        ConciliacionOcFacturas.activo == True
    ).scalar()

    # Documentos con errores de procesamiento
    docs_con_errores = db.query(func.count(DocumentoOrdenCompra.id_documento_oc)).join(
        OrdenCompra, DocumentoOrdenCompra.id_orden_compra == OrdenCompra.id_orden_compra
    ).filter(
        OrdenCompra.fecha_orden >= fecha_desde,
        OrdenCompra.fecha_orden <= fecha_hasta,
        DocumentoOrdenCompra.estado == 'ERROR',
        DocumentoOrdenCompra.activo == True
    ).scalar()

    # Calcular porcentajes
    tasa_completado = (ordenes_completadas / ordenes_iniciadas * 100) if ordenes_iniciadas > 0 else 0
    tasa_problemas = (ordenes_con_problemas / ordenes_iniciadas * 100) if ordenes_iniciadas > 0 else 0
    tasa_errores_docs = (docs_con_errores / ordenes_iniciadas * 100) if ordenes_iniciadas > 0 else 0

    return {
        "periodo": {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta
        },
        "volumenes": {
            "ordenes_iniciadas": ordenes_iniciadas,
            "ordenes_completadas": ordenes_completadas,
            "ordenes_con_problemas": ordenes_con_problemas,
            "documentos_con_errores": docs_con_errores
        },
        "tasas_porcentaje": {
            "tasa_completado": round(tasa_completado, 2),
            "tasa_problemas": round(tasa_problemas, 2),
            "tasa_errores_documentos": round(tasa_errores_docs, 2),
            "tasa_exito": round(100 - tasa_problemas - tasa_errores_docs, 2)
        }
    }

# ========================================
# ALERTAS Y EXCEPCIONES
# ========================================

@router.get("/alertas-workflow")
def get_alertas_workflow(db: Session = Depends(get_db)):
    """Obtener alertas del workflow que requieren atención"""

    alertas = []

    # Órdenes vencidas sin recepción
    fecha_limite = date.today() - timedelta(days=7)
    ordenes_vencidas = db.query(OrdenCompra).join(
        EstadoOrdenCompra, OrdenCompra.id_estado == EstadoOrdenCompra.id_estado
    ).filter(
        OrdenCompra.fecha_requerida < fecha_limite,
        EstadoOrdenCompra.codigo_estado.in_(['APROBADA', 'ENVIADA']),
        OrdenCompra.activo == True
    ).count()

    if ordenes_vencidas > 0:
        alertas.append({
            "tipo": "ORDENES_VENCIDAS",
            "prioridad": "ALTA",
            "cantidad": ordenes_vencidas,
            "mensaje": f"{ordenes_vencidas} órdenes vencidas sin recepción de mercancía",
            "accion_requerida": "Verificar estado con proveedores"
        })

    # Documentos con errores de procesamiento
    docs_error = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.estado == 'ERROR',
        DocumentoOrdenCompra.activo == True
    ).count()

    if docs_error > 0:
        alertas.append({
            "tipo": "DOCUMENTOS_ERROR",
            "prioridad": "MEDIA",
            "cantidad": docs_error,
            "mensaje": f"{docs_error} documentos con errores de procesamiento",
            "accion_requerida": "Revisar y reprocesar documentos"
        })

    # Conciliaciones con diferencias altas
    conciliaciones_problema = db.query(ConciliacionOcFacturas).filter(
        ConciliacionOcFacturas.estado == 'CON_DIFERENCIAS',
        ConciliacionOcFacturas.porcentaje_coincidencia < 80,
        ConciliacionOcFacturas.activo == True
    ).count()

    if conciliaciones_problema > 0:
        alertas.append({
            "tipo": "CONCILIACIONES_PROBLEMA",
            "prioridad": "ALTA",
            "cantidad": conciliaciones_problema,
            "mensaje": f"{conciliaciones_problema} conciliaciones con diferencias significativas",
            "accion_requerida": "Revisar discrepancias y ajustar"
        })

    # Pagos pendientes de confirmación por más de 5 días
    fecha_limite_pagos = date.today() - timedelta(days=5)
    pagos_pendientes = db.query(PagosOrdenesCompra).filter(
        PagosOrdenesCompra.estado == 'PROCESADO',
        PagosOrdenesCompra.fecha_pago < fecha_limite_pagos,
        PagosOrdenesCompra.activo == True
    ).count()

    if pagos_pendientes > 0:
        alertas.append({
            "tipo": "PAGOS_PENDIENTES",
            "prioridad": "MEDIA",
            "cantidad": pagos_pendientes,
            "mensaje": f"{pagos_pendientes} pagos pendientes de confirmación",
            "accion_requerida": "Confirmar pagos procesados"
        })

    return {
        "total_alertas": len(alertas),
        "alertas_alta_prioridad": len([a for a in alertas if a["prioridad"] == "ALTA"]),
        "alertas": alertas
    }

# ========================================
# REPORTES EJECUTIVOS
# ========================================

@router.get("/reporte-ejecutivo")
def get_reporte_ejecutivo(
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Generar reporte ejecutivo del workflow de órdenes de compra"""

    if not fecha_hasta:
        fecha_hasta = date.today()
    if not fecha_desde:
        fecha_desde = fecha_hasta - timedelta(days=30)

    # Resumen general
    resumen = get_resumen_general_workflow(db)

    # Eficiencia
    eficiencia = get_eficiencia_workflow(fecha_desde, fecha_hasta, db)

    # Top proveedores por volumen
    top_proveedores = db.query(
        Proveedor.nombre_proveedor,
        func.count(OrdenCompra.id_orden_compra).label('cantidad_ordenes'),
        func.sum(OrdenCompra.total).label('monto_total')
    ).join(
        OrdenCompra, Proveedor.id_proveedor == OrdenCompra.id_proveedor
    ).filter(
        OrdenCompra.fecha_orden >= fecha_desde,
        OrdenCompra.fecha_orden <= fecha_hasta,
        OrdenCompra.activo == True
    ).group_by(
        Proveedor.id_proveedor, Proveedor.nombre_proveedor
    ).order_by(
        func.sum(OrdenCompra.total).desc()
    ).limit(10).all()

    # Alertas
    alertas = get_alertas_workflow(db)

    return {
        "periodo_reporte": {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta
        },
        "resumen_general": resumen,
        "eficiencia": eficiencia,
        "top_proveedores": [
            {
                "nombre": prov.nombre_proveedor,
                "cantidad_ordenes": prov.cantidad_ordenes,
                "monto_total": float(prov.monto_total)
            }
            for prov in top_proveedores
        ],
        "alertas": alertas,
        "fecha_generacion": datetime.now()
    }