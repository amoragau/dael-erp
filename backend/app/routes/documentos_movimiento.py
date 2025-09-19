from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

# Imports locales
from database import get_db
from models import DocumentoMovimiento, Proveedor
from schemas import DocumentoMovimientoCreate, DocumentoMovimientoUpdate, DocumentoMovimientoResponse, DocumentoMovimientoWithRelations
from crud import documento_movimiento_crud, proveedor_crud

# Configuración del router
router = APIRouter(
    prefix="/documentos-movimiento",
    tags=["Documentos de Movimiento"],
    responses={404: {"description": "No encontrado"}}
)


# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[DocumentoMovimientoResponse])
def listar_documentos(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    tipo_documento: Optional[str] = Query(None, description="Filtrar por tipo de documento"),
    proveedor_id: Optional[int] = Query(None, description="Filtrar por proveedor"),
    fecha_desde: Optional[date] = Query(None, description="Fecha inicial"),
    fecha_hasta: Optional[date] = Query(None, description="Fecha final"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de documentos de movimiento con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **tipo_documento**: Filtrar por tipo (FACTURA, REMISION, ORDEN, etc.)
    - **proveedor_id**: Filtrar documentos de un proveedor específico
    - **fecha_desde/fecha_hasta**: Rango de fechas
    """
    if proveedor_id:
        return documento_movimiento_crud.get_documentos_by_proveedor(db, proveedor_id=proveedor_id)

    # Aplicar filtros adicionales
    query = db.query(DocumentoMovimiento)

    if tipo_documento:
        query = query.filter(DocumentoMovimiento.tipo_documento == tipo_documento)

    if fecha_desde:
        query = query.filter(DocumentoMovimiento.fecha_documento >= fecha_desde)

    if fecha_hasta:
        query = query.filter(DocumentoMovimiento.fecha_documento <= fecha_hasta)

    return query.order_by(DocumentoMovimiento.fecha_documento.desc()).offset(skip).limit(limit).all()

@router.get("/{documento_id}", response_model=DocumentoMovimientoWithRelations)
def obtener_documento(
    documento_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un documento por su ID con información del proveedor"""
    documento = db.query(DocumentoMovimiento).filter(DocumentoMovimiento.id_documento == documento_id).first()
    if documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return documento

@router.get("/tipo/{tipo_documento}/numero/{numero_documento}", response_model=DocumentoMovimientoWithRelations)
def obtener_documento_por_tipo_numero(
    tipo_documento: str,
    numero_documento: str,
    db: Session = Depends(get_db)
):
    """Obtener un documento por tipo y número"""
    documento = documento_movimiento_crud.get_documento_by_tipo_numero(db, tipo_documento, numero_documento)
    if documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return documento

@router.get("/proveedor/{proveedor_id}/documentos", response_model=List[DocumentoMovimientoWithRelations])
def obtener_documentos_por_proveedor(
    proveedor_id: int,
    db: Session = Depends(get_db)
):
    """Obtener todos los documentos de un proveedor específico"""
    # Verificar que el proveedor existe
    proveedor = proveedor_crud.get_proveedor(db, proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    return documento_movimiento_crud.get_documentos_by_proveedor(db, proveedor_id=proveedor_id)

@router.post("/", response_model=DocumentoMovimientoResponse, status_code=201)
def crear_documento(
    documento: DocumentoMovimientoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo documento de movimiento
    - Requiere tipo y número únicos
    - Si se especifica proveedor, debe existir
    """
    # Verificar que no existe un documento con el mismo tipo y número
    existing_documento = documento_movimiento_crud.get_documento_by_tipo_numero(
        db, documento.tipo_documento, documento.numero_documento
    )
    if existing_documento:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un documento {documento.tipo_documento} con número {documento.numero_documento}"
        )

    # Verificar que el proveedor existe (si se especifica)
    if documento.id_proveedor:
        proveedor = proveedor_crud.get_proveedor(db, documento.id_proveedor)
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    return documento_movimiento_crud.create_documento(db=db, documento=documento)

@router.put("/{documento_id}", response_model=DocumentoMovimientoResponse)
def actualizar_documento(
    documento_id: int,
    documento_update: DocumentoMovimientoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar documento existente
    - Solo se actualizan los campos proporcionados
    - Si se cambia tipo/número, debe ser único
    - Valida relaciones
    """
    # Verificar que el documento existe
    db_documento = documento_movimiento_crud.get_documento(db, documento_id)
    if not db_documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    # Si se está actualizando tipo/número, verificar unicidad
    if ((documento_update.tipo_documento and documento_update.tipo_documento != db_documento.tipo_documento) or
        (documento_update.numero_documento and documento_update.numero_documento != db_documento.numero_documento)):

        tipo = documento_update.tipo_documento or db_documento.tipo_documento
        numero = documento_update.numero_documento or db_documento.numero_documento

        existing_documento = documento_movimiento_crud.get_documento_by_tipo_numero(db, tipo, numero)
        if existing_documento and existing_documento.id_documento != documento_id:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un documento {tipo} con número {numero}"
            )

    # Verificar que el proveedor existe (si se actualiza)
    if documento_update.id_proveedor:
        proveedor = proveedor_crud.get_proveedor(db, documento_update.id_proveedor)
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    updated_documento = documento_movimiento_crud.update_documento(
        db=db, documento_id=documento_id, documento_update=documento_update
    )
    if not updated_documento:
        raise HTTPException(status_code=404, detail="Error al actualizar el documento")

    return updated_documento

@router.delete("/{documento_id}")
def eliminar_documento(
    documento_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar documento
    - Verifica que no tenga movimientos asociados
    """
    # Verificar que el documento existe
    db_documento = documento_movimiento_crud.get_documento(db, documento_id)
    if not db_documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    # Verificar que no tenga movimientos asociados
    if db_documento.movimientos:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el documento porque tiene movimientos asociados"
        )

    db.delete(db_documento)
    db.commit()

    return {"message": "Documento eliminado correctamente"}

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_documentos(
    tipo_documento: Optional[str] = Query(None, description="Filtrar por tipo"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de documentos"""
    query = db.query(DocumentoMovimiento)
    if tipo_documento:
        query = query.filter(DocumentoMovimiento.tipo_documento == tipo_documento)

    total = query.count()
    return {"total_documentos": total}

@router.get("/stats/por-tipo")
def estadisticas_por_tipo(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de documentos por tipo"""
    from sqlalchemy import func

    stats = db.query(
        DocumentoMovimiento.tipo_documento,
        func.count(DocumentoMovimiento.id_documento).label('total_documentos'),
        func.sum(DocumentoMovimiento.total_documento).label('total_valor'),
        func.avg(DocumentoMovimiento.total_documento).label('valor_promedio')
    ).group_by(
        DocumentoMovimiento.tipo_documento
    ).all()

    return [
        {
            "tipo_documento": stat.tipo_documento,
            "total_documentos": stat.total_documentos or 0,
            "total_valor": float(stat.total_valor or 0),
            "valor_promedio": float(stat.valor_promedio or 0)
        }
        for stat in stats
    ]

@router.get("/stats/por-proveedor")
def estadisticas_por_proveedor(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de documentos por proveedor"""
    from sqlalchemy import func

    stats = db.query(
        Proveedor.nombre_proveedor,
        func.count(DocumentoMovimiento.id_documento).label('total_documentos'),
        func.sum(DocumentoMovimiento.total_documento).label('total_valor')
    ).join(DocumentoMovimiento).group_by(
        Proveedor.id_proveedor, Proveedor.nombre_proveedor
    ).filter(Proveedor.activo == True).all()

    return [
        {
            "proveedor": stat.nombre_proveedor,
            "total_documentos": stat.total_documentos or 0,
            "total_valor": float(stat.total_valor or 0)
        }
        for stat in stats
    ]

@router.get("/stats/por-periodo")
def estadisticas_por_periodo(
    fecha_desde: Optional[date] = Query(None, description="Fecha inicial"),
    fecha_hasta: Optional[date] = Query(None, description="Fecha final"),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de documentos por período"""
    from sqlalchemy import func

    query = db.query(
        func.count(DocumentoMovimiento.id_documento).label('total_documentos'),
        func.sum(DocumentoMovimiento.total_documento).label('total_valor'),
        func.avg(DocumentoMovimiento.total_documento).label('valor_promedio')
    )

    if fecha_desde:
        query = query.filter(DocumentoMovimiento.fecha_documento >= fecha_desde)

    if fecha_hasta:
        query = query.filter(DocumentoMovimiento.fecha_documento <= fecha_hasta)

    stats = query.first()

    return {
        "periodo": {
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta
        },
        "total_documentos": stats.total_documentos or 0,
        "total_valor": float(stats.total_valor or 0),
        "valor_promedio": float(stats.valor_promedio or 0)
    }