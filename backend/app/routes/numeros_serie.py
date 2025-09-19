from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date

# Imports locales
from database import get_db
from models import NumeroSerie, Producto, Lote, ProductoUbicacion
from schemas import NumeroSerieCreate, NumeroSerieUpdate, NumeroSerieResponse, NumeroSerieWithRelations, EstadoSerieEnum
from crud import numero_serie_crud, producto_crud, lote_crud, producto_ubicacion_crud

# Configuración del router
router = APIRouter(
    prefix="/numeros-serie",
    tags=["Números de Serie"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[NumeroSerieWithRelations])
def listar_numeros_serie(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    estado: Optional[EstadoSerieEnum] = Query(None, description="Filtrar por estado"),
    producto_id: Optional[int] = Query(None, description="Filtrar por producto"),
    lote_id: Optional[int] = Query(None, description="Filtrar por lote"),
    ubicacion_id: Optional[int] = Query(None, description="Filtrar por ubicación"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de números de serie con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **estado**: Filtrar por estado del número de serie
    - **producto_id**: Filtrar números de serie de un producto específico
    - **lote_id**: Filtrar números de serie de un lote específico
    - **ubicacion_id**: Filtrar números de serie en una ubicación específica
    """
    query = db.query(NumeroSerie).options(
        joinedload(NumeroSerie.producto),
        joinedload(NumeroSerie.lote),
        joinedload(NumeroSerie.ubicacion)
    )

    if producto_id:
        query = query.filter(NumeroSerie.id_producto == producto_id)

    if lote_id:
        query = query.filter(NumeroSerie.id_lote == lote_id)

    if ubicacion_id:
        query = query.filter(NumeroSerie.id_ubicacion == ubicacion_id)

    if estado:
        query = query.filter(NumeroSerie.estado == estado.value)

    return query.order_by(NumeroSerie.fecha_ingreso.desc()).offset(skip).limit(limit).all()

@router.get("/{serie_id}", response_model=NumeroSerieWithRelations)
def obtener_numero_serie(
    serie_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un número de serie por su ID con información completa"""
    numero_serie = db.query(NumeroSerie).options(
        joinedload(NumeroSerie.producto),
        joinedload(NumeroSerie.lote),
        joinedload(NumeroSerie.ubicacion)
    ).filter(NumeroSerie.id_serie == serie_id).first()

    if numero_serie is None:
        raise HTTPException(status_code=404, detail="Número de serie no encontrado")
    return numero_serie

@router.get("/producto/{producto_id}/numero/{numero_serie}", response_model=NumeroSerieWithRelations)
def obtener_numero_serie_por_numero(
    producto_id: int,
    numero_serie: str,
    db: Session = Depends(get_db)
):
    """Obtener un número de serie por producto y número"""
    serie = db.query(NumeroSerie).options(
        joinedload(NumeroSerie.producto),
        joinedload(NumeroSerie.lote),
        joinedload(NumeroSerie.ubicacion)
    ).filter(
        NumeroSerie.id_producto == producto_id,
        NumeroSerie.numero_serie == numero_serie
    ).first()

    if serie is None:
        raise HTTPException(status_code=404, detail="Número de serie no encontrado")
    return serie

@router.get("/producto/{producto_id}/series", response_model=List[NumeroSerieWithRelations])
def obtener_series_por_producto(
    producto_id: int,
    estado: Optional[EstadoSerieEnum] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """Obtener todos los números de serie de un producto específico"""
    # Verificar que el producto existe
    producto = producto_crud.get_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    query = db.query(NumeroSerie).options(
        joinedload(NumeroSerie.producto),
        joinedload(NumeroSerie.lote),
        joinedload(NumeroSerie.ubicacion)
    ).filter(NumeroSerie.id_producto == producto_id)

    if estado:
        query = query.filter(NumeroSerie.estado == estado.value)

    return query.order_by(NumeroSerie.fecha_ingreso.desc()).all()

@router.get("/lote/{lote_id}/series", response_model=List[NumeroSerieWithRelations])
def obtener_series_por_lote(
    lote_id: int,
    estado: Optional[EstadoSerieEnum] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """Obtener todos los números de serie de un lote específico"""
    # Verificar que el lote existe
    lote = lote_crud.get_lote(db, lote_id)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

    query = db.query(NumeroSerie).options(
        joinedload(NumeroSerie.producto),
        joinedload(NumeroSerie.lote),
        joinedload(NumeroSerie.ubicacion)
    ).filter(NumeroSerie.id_lote == lote_id)

    if estado:
        query = query.filter(NumeroSerie.estado == estado.value)

    return query.order_by(NumeroSerie.numero_serie.asc()).all()

@router.get("/ubicacion/{ubicacion_id}/series", response_model=List[NumeroSerieWithRelations])
def obtener_series_por_ubicacion(
    ubicacion_id: int,
    estado: Optional[EstadoSerieEnum] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """Obtener todos los números de serie en una ubicación específica"""
    # Verificar que la ubicación existe
    ubicacion = producto_ubicacion_crud.get_ubicacion(db, ubicacion_id)
    if not ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    query = db.query(NumeroSerie).options(
        joinedload(NumeroSerie.producto),
        joinedload(NumeroSerie.lote),
        joinedload(NumeroSerie.ubicacion)
    ).filter(NumeroSerie.id_ubicacion == ubicacion_id)

    if estado:
        query = query.filter(NumeroSerie.estado == estado.value)

    return query.order_by(NumeroSerie.numero_serie.asc()).all()

@router.post("/", response_model=NumeroSerieWithRelations, status_code=201)
def crear_numero_serie(
    numero_serie: NumeroSerieCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo número de serie
    - Requiere número único por producto
    - Valida que existan el producto, lote (opcional) y ubicación (opcional)
    """
    # Verificar que el producto existe
    producto = producto_crud.get_producto(db, numero_serie.id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar que no existe un número de serie con el mismo número para este producto
    existing_serie = numero_serie_crud.get_numero_serie_by_numero(
        db, numero_serie.id_producto, numero_serie.numero_serie
    )
    if existing_serie:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un número de serie {numero_serie.numero_serie} para este producto"
        )

    # Verificar que el lote existe (si se especifica)
    if numero_serie.id_lote:
        lote = lote_crud.get_lote(db, numero_serie.id_lote)
        if not lote:
            raise HTTPException(status_code=404, detail="Lote no encontrado")

        # Verificar que el lote pertenece al mismo producto
        if lote.id_producto != numero_serie.id_producto:
            raise HTTPException(
                status_code=400,
                detail="El lote especificado no pertenece al producto indicado"
            )

    # Verificar que la ubicación existe (si se especifica)
    if numero_serie.id_ubicacion:
        ubicacion = producto_ubicacion_crud.get_ubicacion(db, numero_serie.id_ubicacion)
        if not ubicacion:
            raise HTTPException(status_code=404, detail="Ubicación no encontrada")

        # Verificar que la ubicación es del mismo producto
        if ubicacion.id_producto != numero_serie.id_producto:
            raise HTTPException(
                status_code=400,
                detail="La ubicación especificada no pertenece al producto indicado"
            )

    nuevo_numero_serie = numero_serie_crud.create_numero_serie(db=db, numero_serie=numero_serie)

    # Cargar el número de serie con todas las relaciones
    return db.query(NumeroSerie).options(
        joinedload(NumeroSerie.producto),
        joinedload(NumeroSerie.lote),
        joinedload(NumeroSerie.ubicacion)
    ).filter(NumeroSerie.id_serie == nuevo_numero_serie.id_serie).first()

@router.put("/{serie_id}", response_model=NumeroSerieWithRelations)
def actualizar_numero_serie(
    serie_id: int,
    numero_serie_update: NumeroSerieUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar número de serie existente
    - Solo se actualizan los campos proporcionados
    - Valida relaciones y restricciones
    """
    # Verificar que el número de serie existe
    db_numero_serie = numero_serie_crud.get_numero_serie(db, serie_id)
    if not db_numero_serie:
        raise HTTPException(status_code=404, detail="Número de serie no encontrado")

    # Si se actualiza el número, verificar unicidad
    if numero_serie_update.numero_serie and numero_serie_update.numero_serie != db_numero_serie.numero_serie:
        existing_serie = numero_serie_crud.get_numero_serie_by_numero(
            db, db_numero_serie.id_producto, numero_serie_update.numero_serie
        )
        if existing_serie:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un número de serie {numero_serie_update.numero_serie} para este producto"
            )

    # Verificar relaciones si se actualizan
    if numero_serie_update.id_lote:
        lote = lote_crud.get_lote(db, numero_serie_update.id_lote)
        if not lote:
            raise HTTPException(status_code=404, detail="Lote no encontrado")

        if lote.id_producto != db_numero_serie.id_producto:
            raise HTTPException(
                status_code=400,
                detail="El lote especificado no pertenece al producto del número de serie"
            )

    if numero_serie_update.id_ubicacion:
        ubicacion = producto_ubicacion_crud.get_ubicacion(db, numero_serie_update.id_ubicacion)
        if not ubicacion:
            raise HTTPException(status_code=404, detail="Ubicación no encontrada")

        if ubicacion.id_producto != db_numero_serie.id_producto:
            raise HTTPException(
                status_code=400,
                detail="La ubicación especificada no pertenece al producto del número de serie"
            )

    updated_numero_serie = numero_serie_crud.update_numero_serie(
        db=db, serie_id=serie_id, numero_serie_update=numero_serie_update
    )
    if not updated_numero_serie:
        raise HTTPException(status_code=404, detail="Error al actualizar el número de serie")

    # Cargar el número de serie con todas las relaciones
    return db.query(NumeroSerie).options(
        joinedload(NumeroSerie.producto),
        joinedload(NumeroSerie.lote),
        joinedload(NumeroSerie.ubicacion)
    ).filter(NumeroSerie.id_serie == serie_id).first()

@router.delete("/{serie_id}")
def eliminar_numero_serie(
    serie_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar número de serie
    - Solo se permite si no está vendido
    """
    # Verificar que el número de serie existe
    db_numero_serie = numero_serie_crud.get_numero_serie(db, serie_id)
    if not db_numero_serie:
        raise HTTPException(status_code=404, detail="Número de serie no encontrado")

    # Verificar que no esté vendido
    if db_numero_serie.estado == 'VENDIDO':
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar un número de serie que ya fue vendido"
        )

    success = numero_serie_crud.delete_numero_serie(db=db, serie_id=serie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Error al eliminar el número de serie")

    return {"message": "Número de serie eliminado correctamente"}

# ========================================
# ENDPOINTS ESPECIALES DE OPERACIONES
# ========================================

@router.patch("/{serie_id}/reservar", response_model=NumeroSerieWithRelations)
def reservar_numero_serie(
    serie_id: int,
    cliente: str = Query(..., description="Nombre del cliente"),
    db: Session = Depends(get_db)
):
    """
    Reservar número de serie para un cliente
    - Solo se pueden reservar números de serie DISPONIBLES
    """
    updated_numero_serie = numero_serie_crud.reservar_numero_serie(db=db, serie_id=serie_id, cliente=cliente)
    if not updated_numero_serie:
        raise HTTPException(
            status_code=400,
            detail="No se puede reservar este número de serie. Debe estar DISPONIBLE"
        )

    # Cargar el número de serie con todas las relaciones
    return db.query(NumeroSerie).options(
        joinedload(NumeroSerie.producto),
        joinedload(NumeroSerie.lote),
        joinedload(NumeroSerie.ubicacion)
    ).filter(NumeroSerie.id_serie == serie_id).first()

@router.patch("/{serie_id}/vender", response_model=NumeroSerieWithRelations)
def vender_numero_serie(
    serie_id: int,
    cliente: str = Query(..., description="Nombre del cliente"),
    fecha_venta: Optional[date] = Query(None, description="Fecha de venta (hoy si no se especifica)"),
    db: Session = Depends(get_db)
):
    """
    Marcar número de serie como vendido
    - Se pueden vender números de serie DISPONIBLES o RESERVADOS
    """
    updated_numero_serie = numero_serie_crud.vender_numero_serie(
        db=db, serie_id=serie_id, cliente=cliente, fecha_venta=fecha_venta
    )
    if not updated_numero_serie:
        raise HTTPException(
            status_code=400,
            detail="No se puede vender este número de serie. Debe estar DISPONIBLE o RESERVADO"
        )

    # Cargar el número de serie con todas las relaciones
    return db.query(NumeroSerie).options(
        joinedload(NumeroSerie.producto),
        joinedload(NumeroSerie.lote),
        joinedload(NumeroSerie.ubicacion)
    ).filter(NumeroSerie.id_serie == serie_id).first()

@router.patch("/{serie_id}/liberar", response_model=NumeroSerieWithRelations)
def liberar_numero_serie(
    serie_id: int,
    db: Session = Depends(get_db)
):
    """
    Liberar número de serie (volver a disponible)
    - Quita reservas y limpia información de venta
    """
    updated_numero_serie = numero_serie_crud.liberar_numero_serie(db=db, serie_id=serie_id)
    if not updated_numero_serie:
        raise HTTPException(status_code=404, detail="Número de serie no encontrado")

    # Cargar el número de serie con todas las relaciones
    return db.query(NumeroSerie).options(
        joinedload(NumeroSerie.producto),
        joinedload(NumeroSerie.lote),
        joinedload(NumeroSerie.ubicacion)
    ).filter(NumeroSerie.id_serie == serie_id).first()

# ========================================
# ENDPOINTS ESPECIALES DE CONSULTA
# ========================================

@router.get("/especiales/disponibles", response_model=List[NumeroSerieWithRelations])
def obtener_series_disponibles(
    producto_id: Optional[int] = Query(None, description="Filtrar por producto"),
    db: Session = Depends(get_db)
):
    """Obtener números de serie disponibles"""
    series_disponibles = numero_serie_crud.get_numeros_serie_disponibles(db, producto_id)

    # Cargar con relaciones
    series_ids = [serie.id_serie for serie in series_disponibles]
    if not series_ids:
        return []

    return db.query(NumeroSerie).options(
        joinedload(NumeroSerie.producto),
        joinedload(NumeroSerie.lote),
        joinedload(NumeroSerie.ubicacion)
    ).filter(NumeroSerie.id_serie.in_(series_ids)).all()

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_numeros_serie(
    estado: Optional[EstadoSerieEnum] = Query(None, description="Filtrar por estado"),
    producto_id: Optional[int] = Query(None, description="Filtrar por producto"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de números de serie"""
    query = db.query(NumeroSerie)

    if estado:
        query = query.filter(NumeroSerie.estado == estado.value)

    if producto_id:
        query = query.filter(NumeroSerie.id_producto == producto_id)

    total = query.count()
    return {"total_numeros_serie": total}

@router.get("/stats/por-estado")
def estadisticas_por_estado(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de números de serie por estado"""
    from sqlalchemy import func

    stats = db.query(
        NumeroSerie.estado,
        func.count(NumeroSerie.id_serie).label('total_series')
    ).group_by(NumeroSerie.estado).all()

    return [
        {
            "estado": stat.estado,
            "total_series": stat.total_series or 0
        }
        for stat in stats
    ]

@router.get("/stats/por-producto")
def estadisticas_por_producto(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de números de serie por producto"""
    from sqlalchemy import func

    stats = db.query(
        Producto.sku,
        Producto.nombre_producto,
        func.count(NumeroSerie.id_serie).label('total_series'),
        func.count(func.case(
            [(NumeroSerie.estado == 'DISPONIBLE', 1)]
        )).label('disponibles'),
        func.count(func.case(
            [(NumeroSerie.estado == 'VENDIDO', 1)]
        )).label('vendidos'),
        func.count(func.case(
            [(NumeroSerie.estado == 'RESERVADO', 1)]
        )).label('reservados')
    ).join(NumeroSerie).group_by(
        Producto.id_producto, Producto.sku, Producto.nombre_producto
    ).all()

    return [
        {
            "sku": stat.sku,
            "nombre_producto": stat.nombre_producto,
            "total_series": stat.total_series or 0,
            "disponibles": stat.disponibles or 0,
            "vendidos": stat.vendidos or 0,
            "reservados": stat.reservados or 0
        }
        for stat in stats
    ]

@router.get("/stats/por-lote")
def estadisticas_por_lote(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de números de serie por lote"""
    from sqlalchemy import func

    stats = db.query(
        Lote.numero_lote,
        Producto.sku,
        func.count(NumeroSerie.id_serie).label('total_series'),
        func.count(func.case(
            [(NumeroSerie.estado == 'DISPONIBLE', 1)]
        )).label('disponibles'),
        func.count(func.case(
            [(NumeroSerie.estado == 'VENDIDO', 1)]
        )).label('vendidos')
    ).join(NumeroSerie).join(Producto).group_by(
        Lote.id_lote, Lote.numero_lote, Producto.sku
    ).all()

    return [
        {
            "numero_lote": stat.numero_lote,
            "sku_producto": stat.sku,
            "total_series": stat.total_series or 0,
            "disponibles": stat.disponibles or 0,
            "vendidos": stat.vendidos or 0
        }
        for stat in stats
    ]