from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import ProductoProveedor, Producto, Proveedor
from schemas import ProductoProveedorCreate, ProductoProveedorUpdate, ProductoProveedorResponse, ProductoProveedorWithRelations
from crud import producto_proveedor_crud, producto_crud, proveedor_crud

# Configuración del router
router = APIRouter(
    prefix="/producto-proveedores",
    tags=["Producto-Proveedores"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[ProductoProveedorResponse])
def listar_producto_proveedores(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    producto_id: Optional[int] = Query(None, description="Filtrar por producto"),
    proveedor_id: Optional[int] = Query(None, description="Filtrar por proveedor"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de relaciones producto-proveedor con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo relaciones activas (true) o inactivas (false)
    - **producto_id**: Filtrar relaciones de un producto específico
    - **proveedor_id**: Filtrar relaciones de un proveedor específico
    """
    if producto_id:
        return producto_proveedor_crud.get_proveedores_by_producto(db, producto_id=producto_id, activo=activo)

    if proveedor_id:
        return producto_proveedor_crud.get_productos_by_proveedor(db, proveedor_id=proveedor_id, activo=activo)

    return producto_proveedor_crud.get_producto_proveedores(db, skip=skip, limit=limit, activo=activo)

@router.get("/{producto_proveedor_id}", response_model=ProductoProveedorWithRelations)
def obtener_producto_proveedor(
    producto_proveedor_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una relación producto-proveedor por su ID con información completa"""
    producto_proveedor = db.query(ProductoProveedor).filter(
        ProductoProveedor.id_producto_proveedor == producto_proveedor_id
    ).first()
    if producto_proveedor is None:
        raise HTTPException(status_code=404, detail="Relación producto-proveedor no encontrada")
    return producto_proveedor

@router.get("/producto/{producto_id}/proveedores", response_model=List[ProductoProveedorWithRelations])
def obtener_proveedores_por_producto(
    producto_id: int,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener todos los proveedores de un producto específico"""
    # Verificar que el producto existe
    producto = producto_crud.get_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Obtener con relaciones completas
    query = db.query(ProductoProveedor).filter(ProductoProveedor.id_producto == producto_id)

    if activo is not None:
        query = query.filter(ProductoProveedor.activo == activo)

    return query.all()

@router.get("/proveedor/{proveedor_id}/productos", response_model=List[ProductoProveedorWithRelations])
def obtener_productos_por_proveedor(
    proveedor_id: int,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener todos los productos de un proveedor específico"""
    # Verificar que el proveedor existe
    proveedor = proveedor_crud.get_proveedor(db, proveedor_id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    # Obtener con relaciones completas
    query = db.query(ProductoProveedor).filter(ProductoProveedor.id_proveedor == proveedor_id)

    if activo is not None:
        query = query.filter(ProductoProveedor.activo == activo)

    return query.all()

@router.get("/producto/{producto_id}/proveedor-principal", response_model=ProductoProveedorWithRelations)
def obtener_proveedor_principal(
    producto_id: int,
    db: Session = Depends(get_db)
):
    """Obtener el proveedor principal de un producto"""
    # Verificar que el producto existe
    producto = producto_crud.get_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    proveedor_principal = producto_proveedor_crud.get_proveedor_principal(db, producto_id)
    if not proveedor_principal:
        raise HTTPException(status_code=404, detail="No hay proveedor principal definido para este producto")

    return proveedor_principal

@router.post("/", response_model=ProductoProveedorResponse, status_code=201)
def crear_producto_proveedor(
    producto_proveedor: ProductoProveedorCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nueva relación producto-proveedor
    - Requiere que existan el producto y el proveedor
    - Si se marca como principal, desmarca otros proveedores principales del mismo producto
    - Valida que no exista la relación duplicada
    """
    # Verificar que el producto existe
    producto = producto_crud.get_producto(db, producto_proveedor.id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar que el proveedor existe
    proveedor = proveedor_crud.get_proveedor(db, producto_proveedor.id_proveedor)
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    # Verificar que no existe la relación duplicada
    existing_relation = db.query(ProductoProveedor).filter(
        ProductoProveedor.id_producto == producto_proveedor.id_producto,
        ProductoProveedor.id_proveedor == producto_proveedor.id_proveedor
    ).first()

    if existing_relation:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una relación entre este producto y proveedor"
        )

    # Validar fechas de vigencia
    if (producto_proveedor.fecha_vigencia_desde and
        producto_proveedor.fecha_vigencia_hasta and
        producto_proveedor.fecha_vigencia_desde > producto_proveedor.fecha_vigencia_hasta):
        raise HTTPException(
            status_code=400,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin"
        )

    return producto_proveedor_crud.create_producto_proveedor(db=db, producto_proveedor=producto_proveedor)

@router.put("/{producto_proveedor_id}", response_model=ProductoProveedorResponse)
def actualizar_producto_proveedor(
    producto_proveedor_id: int,
    producto_proveedor_update: ProductoProveedorUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar relación producto-proveedor existente
    - Solo se actualizan los campos proporcionados
    - Si se marca como principal, desmarca otros proveedores principales
    - Valida relaciones y fechas
    """
    # Verificar que la relación existe
    db_producto_proveedor = producto_proveedor_crud.get_producto_proveedor(db, producto_proveedor_id)
    if not db_producto_proveedor:
        raise HTTPException(status_code=404, detail="Relación producto-proveedor no encontrada")

    # Verificar relaciones si se actualizan
    if producto_proveedor_update.id_producto:
        producto = producto_crud.get_producto(db, producto_proveedor_update.id_producto)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

    if producto_proveedor_update.id_proveedor:
        proveedor = proveedor_crud.get_proveedor(db, producto_proveedor_update.id_proveedor)
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    # Validar fechas de vigencia
    fecha_desde = producto_proveedor_update.fecha_vigencia_desde or db_producto_proveedor.fecha_vigencia_desde
    fecha_hasta = producto_proveedor_update.fecha_vigencia_hasta or db_producto_proveedor.fecha_vigencia_hasta

    if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
        raise HTTPException(
            status_code=400,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin"
        )

    updated_producto_proveedor = producto_proveedor_crud.update_producto_proveedor(
        db=db, producto_proveedor_id=producto_proveedor_id, producto_proveedor_update=producto_proveedor_update
    )
    if not updated_producto_proveedor:
        raise HTTPException(status_code=404, detail="Error al actualizar la relación")

    return updated_producto_proveedor

@router.delete("/{producto_proveedor_id}")
def eliminar_producto_proveedor(
    producto_proveedor_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar relación producto-proveedor (soft delete)
    - Marca la relación como inactiva en lugar de eliminarla físicamente
    """
    success = producto_proveedor_crud.delete_producto_proveedor(db=db, producto_proveedor_id=producto_proveedor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Relación producto-proveedor no encontrada")

    return {"message": "Relación producto-proveedor eliminada correctamente"}

@router.patch("/{producto_proveedor_id}/toggle", response_model=ProductoProveedorResponse)
def toggle_estado_producto_proveedor(
    producto_proveedor_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de una relación producto-proveedor
    """
    db_producto_proveedor = producto_proveedor_crud.get_producto_proveedor(db, producto_proveedor_id)
    if not db_producto_proveedor:
        raise HTTPException(status_code=404, detail="Relación producto-proveedor no encontrada")

    # Cambiar el estado
    producto_proveedor_update = ProductoProveedorUpdate(activo=not db_producto_proveedor.activo)
    updated_producto_proveedor = producto_proveedor_crud.update_producto_proveedor(
        db=db, producto_proveedor_id=producto_proveedor_id, producto_proveedor_update=producto_proveedor_update
    )

    return updated_producto_proveedor

@router.patch("/{producto_proveedor_id}/principal")
def marcar_como_principal(
    producto_proveedor_id: int,
    db: Session = Depends(get_db)
):
    """
    Marcar una relación producto-proveedor como principal
    - Desmarca automáticamente otros proveedores principales del mismo producto
    """
    db_producto_proveedor = producto_proveedor_crud.get_producto_proveedor(db, producto_proveedor_id)
    if not db_producto_proveedor:
        raise HTTPException(status_code=404, detail="Relación producto-proveedor no encontrada")

    # Marcar como principal
    producto_proveedor_update = ProductoProveedorUpdate(es_principal=True)
    updated_producto_proveedor = producto_proveedor_crud.update_producto_proveedor(
        db=db, producto_proveedor_id=producto_proveedor_id, producto_proveedor_update=producto_proveedor_update
    )

    return {"message": "Proveedor marcado como principal", "proveedor_principal": updated_producto_proveedor}

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_producto_proveedores(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de relaciones producto-proveedor"""
    query = db.query(ProductoProveedor)
    if activo is not None:
        query = query.filter(ProductoProveedor.activo == activo)

    total = query.count()
    return {"total_relaciones": total}

@router.get("/stats/productos-sin-proveedor")
def productos_sin_proveedor(
    db: Session = Depends(get_db)
):
    """Obtener productos que no tienen proveedores activos"""
    from sqlalchemy import func

    # Productos sin ningún proveedor activo
    productos_sin_proveedor = db.query(Producto).outerjoin(
        ProductoProveedor,
        (Producto.id_producto == ProductoProveedor.id_producto) &
        (ProductoProveedor.activo == True)
    ).filter(
        Producto.activo == True,
        ProductoProveedor.id_producto_proveedor.is_(None)
    ).all()

    return {
        "total_productos_sin_proveedor": len(productos_sin_proveedor),
        "productos": [
            {
                "id_producto": p.id_producto,
                "sku": p.sku,
                "nombre_producto": p.nombre_producto
            }
            for p in productos_sin_proveedor
        ]
    }

@router.get("/stats/costos-promedio")
def estadisticas_costos(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de costos por proveedor"""
    from sqlalchemy import func

    stats = db.query(
        Proveedor.nombre_proveedor,
        func.count(ProductoProveedor.id_producto_proveedor).label('total_productos'),
        func.avg(ProductoProveedor.costo_actual).label('costo_promedio'),
        func.avg(ProductoProveedor.descuento_producto).label('descuento_promedio'),
        func.avg(ProductoProveedor.tiempo_entrega_dias).label('tiempo_entrega_promedio')
    ).join(ProductoProveedor).group_by(
        Proveedor.id_proveedor, Proveedor.nombre_proveedor
    ).filter(
        Proveedor.activo == True,
        ProductoProveedor.activo == True
    ).all()

    return [
        {
            "proveedor": stat.nombre_proveedor,
            "total_productos": stat.total_productos or 0,
            "costo_promedio": float(stat.costo_promedio or 0),
            "descuento_promedio": float(stat.descuento_promedio or 0),
            "tiempo_entrega_promedio": float(stat.tiempo_entrega_promedio or 0)
        }
        for stat in stats
    ]