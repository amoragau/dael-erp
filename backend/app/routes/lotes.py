from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date

# Imports locales
from database import get_db
from models import Lote, Producto, Proveedor
from schemas import LoteCreate, LoteUpdate, LoteResponse, LoteWithRelations, EstadoLoteEnum
from crud import lote_crud, producto_crud, proveedor_crud

# Configuración del router
router = APIRouter(
    prefix="/lotes",
    tags=["Lotes"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[LoteWithRelations])
def listar_lotes(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    estado: Optional[EstadoLoteEnum] = Query(None, description="Filtrar por estado"),
    producto_id: Optional[int] = Query(None, description="Filtrar por producto"),
    proveedor_id: Optional[int] = Query(None, description="Filtrar por proveedor"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de lotes con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **estado**: Filtrar por estado del lote
    - **producto_id**: Filtrar lotes de un producto específico
    - **proveedor_id**: Filtrar lotes de un proveedor específico
    """
    if producto_id:
        query = db.query(Lote).options(
            joinedload(Lote.producto),
            joinedload(Lote.proveedor),
            joinedload(Lote.numeros_serie)
        ).filter(Lote.id_producto == producto_id)
    elif proveedor_id:
        query = db.query(Lote).options(
            joinedload(Lote.producto),
            joinedload(Lote.proveedor),
            joinedload(Lote.numeros_serie)
        ).filter(Lote.id_proveedor == proveedor_id)
    else:
        query = db.query(Lote).options(
            joinedload(Lote.producto),
            joinedload(Lote.proveedor),
            joinedload(Lote.numeros_serie)
        )

    if estado:
        query = query.filter(Lote.estado == estado.value)

    return query.order_by(Lote.fecha_creacion.desc()).offset(skip).limit(limit).all()

@router.get("/{lote_id}", response_model=LoteWithRelations)
def obtener_lote(
    lote_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un lote por su ID con información completa"""
    lote = db.query(Lote).options(
        joinedload(Lote.producto),
        joinedload(Lote.proveedor),
        joinedload(Lote.numeros_serie)
    ).filter(Lote.id_lote == lote_id).first()

    if lote is None:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return lote

@router.get("/producto/{producto_id}/numero/{numero_lote}", response_model=LoteWithRelations)
def obtener_lote_por_numero(
    producto_id: int,
    numero_lote: str,
    db: Session = Depends(get_db)
):
    """Obtener un lote por producto y número"""
    lote = db.query(Lote).options(
        joinedload(Lote.producto),
        joinedload(Lote.proveedor),
        joinedload(Lote.numeros_serie)
    ).filter(
        Lote.id_producto == producto_id,
        Lote.numero_lote == numero_lote
    ).first()

    if lote is None:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return lote

@router.get("/producto/{producto_id}/lotes", response_model=List[LoteWithRelations])
def obtener_lotes_por_producto(
    producto_id: int,
    estado: Optional[EstadoLoteEnum] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """Obtener todos los lotes de un producto específico"""
    # Verificar que el producto existe
    producto = producto_crud.get_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    query = db.query(Lote).options(
        joinedload(Lote.producto),
        joinedload(Lote.proveedor),
        joinedload(Lote.numeros_serie)
    ).filter(Lote.id_producto == producto_id)

    if estado:
        query = query.filter(Lote.estado == estado.value)

    return query.order_by(Lote.fecha_vencimiento.asc()).all()

@router.get("/proveedor/{proveedor_id}/lotes", response_model=List[LoteWithRelations])
def obtener_lotes_por_proveedor(
    proveedor_id: int,
    estado: Optional[EstadoLoteEnum] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """Obtener todos los lotes de un proveedor específico"""
    # Verificar que el proveedor existe
    proveedor = proveedor_crud.get_proveedor(db, proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    query = db.query(Lote).options(
        joinedload(Lote.producto),
        joinedload(Lote.proveedor),
        joinedload(Lote.numeros_serie)
    ).filter(Lote.id_proveedor == proveedor_id)

    if estado:
        query = query.filter(Lote.estado == estado.value)

    return query.order_by(Lote.fecha_creacion.desc()).all()

@router.post("/", response_model=LoteWithRelations, status_code=201)
def crear_lote(
    lote: LoteCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo lote
    - Requiere número único por producto
    - Valida que existan el producto y proveedor (opcional)
    """
    # Verificar que el producto existe
    producto = producto_crud.get_producto(db, lote.id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar que no existe un lote con el mismo número para este producto
    existing_lote = lote_crud.get_lote_by_numero(db, lote.id_producto, lote.numero_lote)
    if existing_lote:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un lote con número {lote.numero_lote} para este producto"
        )

    # Verificar que el proveedor existe (si se especifica)
    if lote.id_proveedor:
        proveedor = proveedor_crud.get_proveedor(db, lote.id_proveedor)
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    # Validar fechas lógicas
    if lote.fecha_fabricacion and lote.fecha_vencimiento:
        if lote.fecha_fabricacion > lote.fecha_vencimiento:
            raise HTTPException(
                status_code=400,
                detail="La fecha de fabricación no puede ser posterior a la fecha de vencimiento"
            )

    nuevo_lote = lote_crud.create_lote(db=db, lote=lote)

    # Cargar el lote con todas las relaciones
    return db.query(Lote).options(
        joinedload(Lote.producto),
        joinedload(Lote.proveedor),
        joinedload(Lote.numeros_serie)
    ).filter(Lote.id_lote == nuevo_lote.id_lote).first()

@router.put("/{lote_id}", response_model=LoteWithRelations)
def actualizar_lote(
    lote_id: int,
    lote_update: LoteUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar lote existente
    - Solo se actualizan los campos proporcionados
    - Valida relaciones y restricciones
    """
    # Verificar que el lote existe
    db_lote = lote_crud.get_lote(db, lote_id)
    if not db_lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

    # Si se actualiza el número, verificar unicidad
    if lote_update.numero_lote and lote_update.numero_lote != db_lote.numero_lote:
        existing_lote = lote_crud.get_lote_by_numero(db, db_lote.id_producto, lote_update.numero_lote)
        if existing_lote:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un lote con número {lote_update.numero_lote} para este producto"
            )

    # Verificar que el proveedor existe (si se actualiza)
    if lote_update.id_proveedor:
        proveedor = proveedor_crud.get_proveedor(db, lote_update.id_proveedor)
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    # Validar fechas lógicas
    fecha_fabricacion = lote_update.fecha_fabricacion if lote_update.fecha_fabricacion is not None else db_lote.fecha_fabricacion
    fecha_vencimiento = lote_update.fecha_vencimiento if lote_update.fecha_vencimiento is not None else db_lote.fecha_vencimiento

    if fecha_fabricacion and fecha_vencimiento:
        if fecha_fabricacion > fecha_vencimiento:
            raise HTTPException(
                status_code=400,
                detail="La fecha de fabricación no puede ser posterior a la fecha de vencimiento"
            )

    updated_lote = lote_crud.update_lote(db=db, lote_id=lote_id, lote_update=lote_update)
    if not updated_lote:
        raise HTTPException(status_code=404, detail="Error al actualizar el lote")

    # Cargar el lote con todas las relaciones
    return db.query(Lote).options(
        joinedload(Lote.producto),
        joinedload(Lote.proveedor),
        joinedload(Lote.numeros_serie)
    ).filter(Lote.id_lote == lote_id).first()

@router.delete("/{lote_id}")
def eliminar_lote(
    lote_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar lote
    - Verifica que no tenga números de serie asociados
    """
    # Verificar que el lote existe
    db_lote = lote_crud.get_lote(db, lote_id)
    if not db_lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

    # Intentar eliminar (el CRUD verifica las restricciones)
    success = lote_crud.delete_lote(db=db, lote_id=lote_id)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el lote porque tiene números de serie asociados"
        )

    return {"message": "Lote eliminado correctamente"}

@router.patch("/{lote_id}/cantidad", response_model=LoteWithRelations)
def actualizar_cantidad_lote(
    lote_id: int,
    nueva_cantidad: int = Query(..., ge=0, description="Nueva cantidad actual del lote"),
    db: Session = Depends(get_db)
):
    """
    Actualizar cantidad actual de un lote
    - Cambia automáticamente el estado a AGOTADO si la cantidad es 0
    """
    updated_lote = lote_crud.update_cantidad_lote(db=db, lote_id=lote_id, nueva_cantidad=nueva_cantidad)
    if not updated_lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

    # Cargar el lote con todas las relaciones
    return db.query(Lote).options(
        joinedload(Lote.producto),
        joinedload(Lote.proveedor),
        joinedload(Lote.numeros_serie)
    ).filter(Lote.id_lote == lote_id).first()

# ========================================
# ENDPOINTS ESPECIALES
# ========================================

@router.get("/especiales/vencidos", response_model=List[LoteWithRelations])
def obtener_lotes_vencidos(
    db: Session = Depends(get_db)
):
    """Obtener lotes vencidos que aún no están marcados como vencidos"""
    lotes_vencidos = lote_crud.get_lotes_vencidos(db)

    # Cargar con relaciones
    lotes_ids = [lote.id_lote for lote in lotes_vencidos]
    if not lotes_ids:
        return []

    return db.query(Lote).options(
        joinedload(Lote.producto),
        joinedload(Lote.proveedor),
        joinedload(Lote.numeros_serie)
    ).filter(Lote.id_lote.in_(lotes_ids)).all()

@router.get("/especiales/por-vencer", response_model=List[LoteWithRelations])
def obtener_lotes_por_vencer(
    dias: int = Query(30, ge=1, le=365, description="Días de anticipación"),
    db: Session = Depends(get_db)
):
    """Obtener lotes que vencen en los próximos X días"""
    lotes_por_vencer = lote_crud.get_lotes_por_vencer(db, dias)

    # Cargar con relaciones
    lotes_ids = [lote.id_lote for lote in lotes_por_vencer]
    if not lotes_ids:
        return []

    return db.query(Lote).options(
        joinedload(Lote.producto),
        joinedload(Lote.proveedor),
        joinedload(Lote.numeros_serie)
    ).filter(Lote.id_lote.in_(lotes_ids)).order_by(Lote.fecha_vencimiento.asc()).all()

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_lotes(
    estado: Optional[EstadoLoteEnum] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de lotes"""
    query = db.query(Lote)
    if estado:
        query = query.filter(Lote.estado == estado.value)

    total = query.count()
    return {"total_lotes": total}

@router.get("/stats/por-estado")
def estadisticas_por_estado(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de lotes por estado"""
    from sqlalchemy import func

    stats = db.query(
        Lote.estado,
        func.count(Lote.id_lote).label('total_lotes'),
        func.sum(Lote.cantidad_actual).label('cantidad_total'),
        func.avg(Lote.cantidad_actual).label('cantidad_promedio')
    ).group_by(Lote.estado).all()

    return [
        {
            "estado": stat.estado,
            "total_lotes": stat.total_lotes or 0,
            "cantidad_total": int(stat.cantidad_total or 0),
            "cantidad_promedio": float(stat.cantidad_promedio or 0)
        }
        for stat in stats
    ]

@router.get("/stats/por-producto")
def estadisticas_por_producto(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de lotes por producto"""
    from sqlalchemy import func

    stats = db.query(
        Producto.sku,
        Producto.nombre_producto,
        func.count(Lote.id_lote).label('total_lotes'),
        func.sum(Lote.cantidad_actual).label('cantidad_total'),
        func.sum(func.case(
            [(Lote.estado == 'ACTIVO', Lote.cantidad_actual)],
            else_=0
        )).label('cantidad_activa')
    ).join(Lote).group_by(
        Producto.id_producto, Producto.sku, Producto.nombre_producto
    ).all()

    return [
        {
            "sku": stat.sku,
            "nombre_producto": stat.nombre_producto,
            "total_lotes": stat.total_lotes or 0,
            "cantidad_total": int(stat.cantidad_total or 0),
            "cantidad_activa": int(stat.cantidad_activa or 0)
        }
        for stat in stats
    ]

@router.get("/stats/vencimientos")
def estadisticas_vencimientos(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de vencimientos"""
    from sqlalchemy import func
    from datetime import date, timedelta

    hoy = date.today()
    en_30_dias = hoy + timedelta(days=30)
    en_90_dias = hoy + timedelta(days=90)

    stats = db.query(
        func.count(func.case(
            [(Lote.fecha_vencimiento < hoy, 1)]
        )).label('vencidos'),
        func.count(func.case(
            [(Lote.fecha_vencimiento.between(hoy, en_30_dias), 1)]
        )).label('vencen_30_dias'),
        func.count(func.case(
            [(Lote.fecha_vencimiento.between(en_30_dias + timedelta(days=1), en_90_dias), 1)]
        )).label('vencen_90_dias'),
        func.count(func.case(
            [(Lote.fecha_vencimiento > en_90_dias, 1)]
        )).label('vencen_mas_90_dias')
    ).filter(Lote.fecha_vencimiento.isnot(None)).first()

    return {
        "vencidos": stats.vencidos or 0,
        "vencen_en_30_dias": stats.vencen_30_dias or 0,
        "vencen_en_90_dias": stats.vencen_90_dias or 0,
        "vencen_en_mas_90_dias": stats.vencen_mas_90_dias or 0
    }