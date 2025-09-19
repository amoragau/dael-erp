from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import Cliente
from schemas import ClienteCreate, ClienteUpdate, ClienteResponse, TipoClienteEnum
from crud import cliente_crud

# Configuración del router
router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    tipo_cliente: Optional[TipoClienteEnum] = Query(None, description="Filtrar por tipo de cliente"),
    ciudad: Optional[str] = Query(None, description="Filtrar por ciudad"),
    estado: Optional[str] = Query(None, description="Filtrar por estado/provincia"),
    search: Optional[str] = Query(None, description="Buscar por nombre, código o razón social"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de clientes con paginación y filtros
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo clientes activos (true) o inactivos (false)
    - **tipo_cliente**: Filtrar por tipo de cliente
    - **ciudad**: Filtrar por ciudad
    - **estado**: Filtrar por estado/provincia
    - **search**: Buscar en nombre, código o razón social
    """
    # Si hay búsqueda, usar el método de búsqueda
    if search:
        return cliente_crud.search_clientes(db, search, activo)

    # Si hay filtro por tipo, usar método específico
    if tipo_cliente:
        return cliente_crud.get_clientes_by_tipo(db, tipo_cliente.value, activo)

    # Si hay filtro por ciudad, usar método específico
    if ciudad:
        return cliente_crud.get_clientes_by_ciudad(db, ciudad, activo)

    # Si hay filtro por estado, usar método específico
    if estado:
        return cliente_crud.get_clientes_by_estado(db, estado, activo)

    # Lista general con paginación
    return cliente_crud.get_clientes(db, skip=skip, limit=limit, activo=activo)

@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un cliente por su ID"""
    cliente = cliente_crud.get_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.get("/codigo/{codigo_cliente}", response_model=ClienteResponse)
def obtener_cliente_por_codigo(
    codigo_cliente: str,
    db: Session = Depends(get_db)
):
    """Obtener un cliente por su código"""
    cliente = cliente_crud.get_cliente_by_codigo(db, codigo_cliente)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/", response_model=ClienteResponse, status_code=201)
def crear_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo cliente
    - Requiere código único
    - Valida formato de email si se proporciona
    """
    # Verificar que no existe un cliente con el mismo código
    existing_cliente = cliente_crud.get_cliente_by_codigo(db, cliente.codigo_cliente)
    if existing_cliente:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un cliente con código {cliente.codigo_cliente}"
        )

    return cliente_crud.create_cliente(db=db, cliente=cliente)

@router.put("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar cliente existente
    - Solo se actualizan los campos proporcionados
    - Valida unicidad del código si se cambia
    """
    # Verificar que el cliente existe
    db_cliente = cliente_crud.get_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Si se actualiza el código, verificar unicidad
    if cliente_update.codigo_cliente and cliente_update.codigo_cliente != db_cliente.codigo_cliente:
        existing_cliente = cliente_crud.get_cliente_by_codigo(db, cliente_update.codigo_cliente)
        if existing_cliente:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un cliente con código {cliente_update.codigo_cliente}"
            )

    updated_cliente = cliente_crud.update_cliente(db=db, cliente_id=cliente_id, cliente_update=cliente_update)
    if not updated_cliente:
        raise HTTPException(status_code=404, detail="Error al actualizar el cliente")

    return updated_cliente

@router.delete("/{cliente_id}")
def eliminar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar cliente (soft delete)
    - Marca el cliente como inactivo en lugar de eliminarlo físicamente
    """
    success = cliente_crud.delete_cliente(db=db, cliente_id=cliente_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return {"message": "Cliente eliminado correctamente"}

@router.patch("/{cliente_id}/toggle", response_model=ClienteResponse)
def toggle_estado_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de un cliente
    """
    cliente = cliente_crud.toggle_cliente_activo(db=db, cliente_id=cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    return cliente

# ========================================
# ENDPOINTS DE CONSULTA ESPECÍFICA
# ========================================

@router.get("/tipo/{tipo_cliente}/clientes", response_model=List[ClienteResponse])
def obtener_clientes_por_tipo(
    tipo_cliente: TipoClienteEnum,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener todos los clientes de un tipo específico"""
    return cliente_crud.get_clientes_by_tipo(db, tipo_cliente.value, activo)

@router.get("/ubicacion/ciudad/{ciudad}", response_model=List[ClienteResponse])
def obtener_clientes_por_ciudad(
    ciudad: str,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener clientes de una ciudad específica"""
    clientes = cliente_crud.get_clientes_by_ciudad(db, ciudad, activo)
    if not clientes:
        raise HTTPException(status_code=404, detail=f"No se encontraron clientes en {ciudad}")
    return clientes

@router.get("/ubicacion/estado/{estado}", response_model=List[ClienteResponse])
def obtener_clientes_por_estado(
    estado: str,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener clientes de un estado/provincia específico"""
    clientes = cliente_crud.get_clientes_by_estado(db, estado, activo)
    if not clientes:
        raise HTTPException(status_code=404, detail=f"No se encontraron clientes en {estado}")
    return clientes

@router.get("/buscar/{search_term}", response_model=List[ClienteResponse])
def buscar_clientes(
    search_term: str,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Buscar clientes por nombre, código o razón social
    - Búsqueda insensible a mayúsculas/minúsculas
    - Busca coincidencias parciales
    """
    clientes = cliente_crud.search_clientes(db, search_term, activo)
    if not clientes:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron clientes con el término de búsqueda: {search_term}"
        )
    return clientes

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_clientes(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    tipo_cliente: Optional[TipoClienteEnum] = Query(None, description="Filtrar por tipo"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de clientes"""
    if tipo_cliente:
        clientes = cliente_crud.get_clientes_by_tipo(db, tipo_cliente.value, activo)
        total = len(clientes)
    else:
        from sqlalchemy import func
        query = db.query(func.count(Cliente.id_cliente))
        if activo is not None:
            query = query.filter(Cliente.activo == activo)
        total = query.scalar()

    return {"total_clientes": total}

@router.get("/stats/resumen")
def estadisticas_resumen(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas generales de clientes"""
    return cliente_crud.get_estadisticas_clientes(db)

@router.get("/stats/por-tipo")
def estadisticas_por_tipo(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de clientes por tipo"""
    from sqlalchemy import func

    stats = db.query(
        Cliente.tipo_cliente,
        func.count(Cliente.id_cliente).label('total_clientes'),
        func.count(func.case(
            [(Cliente.activo == True, 1)]
        )).label('clientes_activos'),
        func.count(func.case(
            [(Cliente.activo == False, 1)]
        )).label('clientes_inactivos')
    ).group_by(Cliente.tipo_cliente).all()

    return [
        {
            "tipo_cliente": stat.tipo_cliente,
            "total_clientes": stat.total_clientes or 0,
            "clientes_activos": stat.clientes_activos or 0,
            "clientes_inactivos": stat.clientes_inactivos or 0
        }
        for stat in stats
    ]

@router.get("/stats/por-ubicacion")
def estadisticas_por_ubicacion(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de clientes por ubicación geográfica"""
    from sqlalchemy import func

    # Por estado
    stats_estado = db.query(
        Cliente.estado,
        func.count(Cliente.id_cliente).label('total_clientes')
    ).filter(
        Cliente.estado.isnot(None),
        Cliente.activo == True
    ).group_by(Cliente.estado).order_by(
        func.count(Cliente.id_cliente).desc()
    ).all()

    # Por ciudad (top 10)
    stats_ciudad = db.query(
        Cliente.ciudad,
        Cliente.estado,
        func.count(Cliente.id_cliente).label('total_clientes')
    ).filter(
        Cliente.ciudad.isnot(None),
        Cliente.activo == True
    ).group_by(
        Cliente.ciudad, Cliente.estado
    ).order_by(
        func.count(Cliente.id_cliente).desc()
    ).limit(10).all()

    return {
        "por_estado": [
            {
                "estado": stat.estado or "Sin especificar",
                "total_clientes": stat.total_clientes or 0
            }
            for stat in stats_estado
        ],
        "top_ciudades": [
            {
                "ciudad": stat.ciudad or "Sin especificar",
                "estado": stat.estado or "Sin especificar",
                "total_clientes": stat.total_clientes or 0
            }
            for stat in stats_ciudad
        ]
    }

@router.get("/stats/contacto")
def estadisticas_contacto(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de información de contacto"""
    from sqlalchemy import func

    stats = db.query(
        func.count(Cliente.id_cliente).label('total_clientes'),
        func.count(Cliente.telefono).label('con_telefono'),
        func.count(Cliente.email).label('con_email'),
        func.count(Cliente.contacto_principal).label('con_contacto'),
        func.count(func.case(
            [(Cliente.telefono.isnot(None) & Cliente.email.isnot(None), 1)]
        )).label('con_telefono_y_email')
    ).filter(Cliente.activo == True).first()

    total = stats.total_clientes or 0

    return {
        "total_clientes_activos": total,
        "con_telefono": {
            "cantidad": stats.con_telefono or 0,
            "porcentaje": round((stats.con_telefono / total * 100) if total > 0 else 0, 2)
        },
        "con_email": {
            "cantidad": stats.con_email or 0,
            "porcentaje": round((stats.con_email / total * 100) if total > 0 else 0, 2)
        },
        "con_contacto_principal": {
            "cantidad": stats.con_contacto or 0,
            "porcentaje": round((stats.con_contacto / total * 100) if total > 0 else 0, 2)
        },
        "con_telefono_y_email": {
            "cantidad": stats.con_telefono_y_email or 0,
            "porcentaje": round((stats.con_telefono_y_email / total * 100) if total > 0 else 0, 2)
        }
    }