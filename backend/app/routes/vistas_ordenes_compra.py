from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
import schemas, crud

router = APIRouter()

# ========================================
# ENDPOINTS PARA VISTA RESUMEN DE ÓRDENES
# ========================================

@router.get("/resumen/", response_model=List[schemas.VistaOrdenesCompraResumenRead])
def get_vista_ordenes_resumen(
    skip: int = 0,
    limit: int = 100,
    numero_orden: Optional[str] = Query(None),
    nombre_proveedor: Optional[str] = Query(None),
    codigo_proveedor: Optional[str] = Query(None),
    solicitante: Optional[str] = Query(None),
    nombre_estado: Optional[str] = Query(None),
    fecha_desde: Optional[str] = Query(None),
    fecha_hasta: Optional[str] = Query(None),
    total_minimo: Optional[float] = Query(None),
    total_maximo: Optional[float] = Query(None),
    estado_recepcion: Optional[str] = Query(None),
    moneda: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Obtener vista resumen de órdenes de compra con filtros"""
    filtros = schemas.VistaOrdenesCompraResumenFilters(
        numero_orden=numero_orden,
        nombre_proveedor=nombre_proveedor,
        codigo_proveedor=codigo_proveedor,
        solicitante=solicitante,
        nombre_estado=nombre_estado,
        fecha_desde=fecha_desde,
        fecha_hasta=fecha_hasta,
        total_minimo=total_minimo,
        total_maximo=total_maximo,
        estado_recepcion=estado_recepcion,
        moneda=moneda
    )
    ordenes = crud.vista_ordenes_compra_resumen_crud.get_multi_filtered(db, skip=skip, limit=limit, filtro=filtros)
    return ordenes

@router.get("/resumen/{orden_id}", response_model=schemas.VistaOrdenesCompraResumenRead)
def get_vista_orden_resumen_by_id(
    orden_id: int,
    db: Session = Depends(get_db)
):
    """Obtener resumen de orden por ID"""
    orden = crud.vista_ordenes_compra_resumen_crud.get_by_id(db, orden_id)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return orden

@router.get("/resumen/count/", response_model=int)
def count_vista_ordenes_resumen(
    numero_orden: Optional[str] = Query(None),
    nombre_proveedor: Optional[str] = Query(None),
    estado_recepcion: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Contar órdenes en vista resumen con filtros"""
    filtros = schemas.VistaOrdenesCompraResumenFilters(
        numero_orden=numero_orden,
        nombre_proveedor=nombre_proveedor,
        estado_recepcion=estado_recepcion
    )
    return crud.vista_ordenes_compra_resumen_crud.contar_con_filtros(db, filtros)

@router.get("/resumen/estadisticas/")
def get_estadisticas_ordenes(db: Session = Depends(get_db)):
    """Obtener estadísticas generales de órdenes de compra"""
    return crud.vista_ordenes_compra_resumen_crud.get_estadisticas_resumen(db)

# ========================================
# ENDPOINTS PARA VISTA DETALLE COMPLETO
# ========================================

@router.get("/detalle-completo/", response_model=List[schemas.VistaOrdenesDetalleCompletoRead])
def get_vista_ordenes_detalle_completo(
    skip: int = 0,
    limit: int = 100,
    numero_orden: Optional[str] = Query(None),
    sku: Optional[str] = Query(None),
    producto_nombre: Optional[str] = Query(None),
    nombre_proveedor: Optional[str] = Query(None),
    fecha_entrega_desde: Optional[str] = Query(None),
    fecha_entrega_hasta: Optional[str] = Query(None),
    cantidad_pendiente_mayor_que: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    """Obtener vista detalle completo de órdenes de compra con filtros"""
    filtros = schemas.VistaOrdenesDetalleCompletoFilters(
        numero_orden=numero_orden,
        sku=sku,
        producto_nombre=producto_nombre,
        nombre_proveedor=nombre_proveedor,
        fecha_entrega_desde=fecha_entrega_desde,
        fecha_entrega_hasta=fecha_entrega_hasta,
        cantidad_pendiente_mayor_que=cantidad_pendiente_mayor_que
    )
    detalles = crud.vista_ordenes_detalle_completo_crud.get_multi_filtered(db, skip=skip, limit=limit, filtro=filtros)
    return detalles

@router.get("/detalle-completo/{detalle_id}", response_model=schemas.VistaOrdenesDetalleCompletoRead)
def get_vista_detalle_completo_by_id(
    detalle_id: int,
    db: Session = Depends(get_db)
):
    """Obtener detalle completo por ID"""
    detalle = crud.vista_ordenes_detalle_completo_crud.get_by_id(db, detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

@router.get("/detalle-completo/orden/{numero_orden}", response_model=List[schemas.VistaOrdenesDetalleCompletoRead])
def get_vista_detalles_by_orden(
    numero_orden: str,
    db: Session = Depends(get_db)
):
    """Obtener detalles completos por número de orden"""
    detalles = crud.vista_ordenes_detalle_completo_crud.get_by_orden(db, numero_orden)
    return detalles

@router.get("/detalle-completo/pendientes/", response_model=List[schemas.VistaOrdenesDetalleCompletoRead])
def get_productos_pendientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener productos con cantidades pendientes de recibir"""
    productos = crud.vista_ordenes_detalle_completo_crud.get_productos_pendientes(db, skip=skip, limit=limit)
    return productos

@router.get("/detalle-completo/count/", response_model=int)
def count_vista_detalle_completo(
    numero_orden: Optional[str] = Query(None),
    sku: Optional[str] = Query(None),
    cantidad_pendiente_mayor_que: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    """Contar detalles en vista completa con filtros"""
    filtros = schemas.VistaOrdenesDetalleCompletoFilters(
        numero_orden=numero_orden,
        sku=sku,
        cantidad_pendiente_mayor_que=cantidad_pendiente_mayor_que
    )
    return crud.vista_ordenes_detalle_completo_crud.contar_con_filtros(db, filtros)

# ========================================
# ENDPOINTS ADICIONALES PARA REPORTES
# ========================================

@router.get("/reportes/ordenes-por-estado/")
def get_ordenes_por_estado(db: Session = Depends(get_db)):
    """Obtener cantidad de órdenes agrupadas por estado de recepción"""
    resultado = db.query(
        crud.vista_ordenes_compra_resumen_crud.model.estado_recepcion,
        func.count(crud.vista_ordenes_compra_resumen_crud.model.id_orden_compra).label('cantidad'),
        func.sum(crud.vista_ordenes_compra_resumen_crud.model.total).label('valor_total')
    ).group_by(crud.vista_ordenes_compra_resumen_crud.model.estado_recepcion).all()

    return [
        {
            "estado_recepcion": row.estado_recepcion,
            "cantidad_ordenes": row.cantidad,
            "valor_total": float(row.valor_total or 0)
        }
        for row in resultado
    ]

@router.get("/reportes/ordenes-por-proveedor/")
def get_ordenes_por_proveedor(
    limite: int = Query(10, description="Número de proveedores a mostrar"),
    db: Session = Depends(get_db)
):
    """Obtener top proveedores por cantidad de órdenes"""
    resultado = db.query(
        crud.vista_ordenes_compra_resumen_crud.model.nombre_proveedor,
        crud.vista_ordenes_compra_resumen_crud.model.codigo_proveedor,
        func.count(crud.vista_ordenes_compra_resumen_crud.model.id_orden_compra).label('cantidad_ordenes'),
        func.sum(crud.vista_ordenes_compra_resumen_crud.model.total).label('valor_total')
    ).group_by(
        crud.vista_ordenes_compra_resumen_crud.model.nombre_proveedor,
        crud.vista_ordenes_compra_resumen_crud.model.codigo_proveedor
    ).order_by(func.count(crud.vista_ordenes_compra_resumen_crud.model.id_orden_compra).desc()).limit(limite).all()

    return [
        {
            "nombre_proveedor": row.nombre_proveedor,
            "codigo_proveedor": row.codigo_proveedor,
            "cantidad_ordenes": row.cantidad_ordenes,
            "valor_total": float(row.valor_total or 0)
        }
        for row in resultado
    ]

@router.get("/reportes/productos-mas-solicitados/")
def get_productos_mas_solicitados(
    limite: int = Query(10, description="Número de productos a mostrar"),
    db: Session = Depends(get_db)
):
    """Obtener productos más solicitados en órdenes de compra"""
    resultado = db.query(
        crud.vista_ordenes_detalle_completo_crud.model.sku,
        crud.vista_ordenes_detalle_completo_crud.model.producto_nombre,
        func.count(crud.vista_ordenes_detalle_completo_crud.model.id_detalle).label('veces_solicitado'),
        func.sum(crud.vista_ordenes_detalle_completo_crud.model.cantidad_solicitada).label('cantidad_total'),
        func.sum(crud.vista_ordenes_detalle_completo_crud.model.importe_total).label('valor_total')
    ).group_by(
        crud.vista_ordenes_detalle_completo_crud.model.sku,
        crud.vista_ordenes_detalle_completo_crud.model.producto_nombre
    ).order_by(func.count(crud.vista_ordenes_detalle_completo_crud.model.id_detalle).desc()).limit(limite).all()

    return [
        {
            "sku": row.sku,
            "producto_nombre": row.producto_nombre,
            "veces_solicitado": row.veces_solicitado,
            "cantidad_total": float(row.cantidad_total or 0),
            "valor_total": float(row.valor_total or 0)
        }
        for row in resultado
    ]