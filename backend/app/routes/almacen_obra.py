from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

# Imports locales
from database import get_db
from models import AlmacenObra, Obra
from schemas import AlmacenObraCreate, AlmacenObraUpdate, AlmacenObraResponse, AlmacenObraWithRelations
from crud import almacen_obra_crud, obra_crud

# Configuración del router
router = APIRouter(
    prefix="/almacen-obra",
    tags=["Almacén de Obra"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[AlmacenObraWithRelations])
def listar_almacenes_obra(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    responsable: Optional[str] = Query(None, description="Filtrar por responsable"),
    tiene_seguridad: Optional[bool] = Query(None, description="Filtrar por seguridad"),
    tiene_techo: Optional[bool] = Query(None, description="Filtrar por techo"),
    search: Optional[str] = Query(None, description="Buscar por nombre, descripción o responsable"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de almacenes de obra con paginación y filtros
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo almacenes activos (true) o inactivos (false)
    - **responsable**: Filtrar por responsable
    - **tiene_seguridad**: Filtrar por almacenes con/sin seguridad
    - **tiene_techo**: Filtrar por almacenes con/sin techo
    - **search**: Buscar en nombre, descripción o responsable
    """
    # Si hay búsqueda, usar el método de búsqueda
    if search:
        almacenes = almacen_obra_crud.search_almacenes(db, search, activo)
    # Si hay filtro por responsable, usar método específico
    elif responsable:
        almacenes = almacen_obra_crud.get_almacenes_by_responsable(db, responsable, activo)
    # Si hay filtro específico de seguridad
    elif tiene_seguridad is True:
        almacenes = almacen_obra_crud.get_almacenes_con_seguridad(db, activo)
    # Si hay filtro específico de techo
    elif tiene_techo is False:
        almacenes = almacen_obra_crud.get_almacenes_sin_techo(db, activo)
    # Lista general con paginación
    else:
        almacenes = almacen_obra_crud.get_almacenes_obra(db, skip=skip, limit=limit, activo=activo)

    # Aplicar filtros adicionales si se especifican
    if tiene_seguridad is not None or tiene_techo is not None:
        almacenes_filtrados = []
        for almacen in almacenes:
            incluir = True
            if tiene_seguridad is not None and almacen.tiene_seguridad != tiene_seguridad:
                incluir = False
            if tiene_techo is not None and almacen.tiene_techo != tiene_techo:
                incluir = False
            if incluir:
                almacenes_filtrados.append(almacen)
        almacenes = almacenes_filtrados

    # Cargar con relaciones
    almacenes_ids = [almacen.id_almacen_obra for almacen in almacenes]
    if not almacenes_ids:
        return []

    return db.query(AlmacenObra).options(
        joinedload(AlmacenObra.obra).joinedload(Obra.cliente)
    ).filter(AlmacenObra.id_almacen_obra.in_(almacenes_ids)).all()

@router.get("/{almacen_id}", response_model=AlmacenObraWithRelations)
def obtener_almacen_obra(
    almacen_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un almacén de obra por su ID con información completa"""
    almacen = db.query(AlmacenObra).options(
        joinedload(AlmacenObra.obra).joinedload(Obra.cliente)
    ).filter(AlmacenObra.id_almacen_obra == almacen_id).first()

    if almacen is None:
        raise HTTPException(status_code=404, detail="Almacén de obra no encontrado")
    return almacen

@router.get("/obra/{obra_id}/almacen", response_model=AlmacenObraWithRelations)
def obtener_almacen_por_obra(
    obra_id: int,
    db: Session = Depends(get_db)
):
    """Obtener el almacén de una obra específica"""
    # Verificar que la obra existe
    obra = obra_crud.get_obra(db, obra_id)
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")

    almacen = db.query(AlmacenObra).options(
        joinedload(AlmacenObra.obra).joinedload(Obra.cliente)
    ).filter(AlmacenObra.id_obra == obra_id).first()

    if almacen is None:
        raise HTTPException(status_code=404, detail="La obra no tiene almacén configurado")
    return almacen

@router.post("/", response_model=AlmacenObraWithRelations, status_code=201)
def crear_almacen_obra(
    almacen: AlmacenObraCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo almacén de obra
    - Cada obra solo puede tener un almacén
    - Valida que exista la obra
    """
    # Verificar que la obra existe
    obra = obra_crud.get_obra(db, almacen.id_obra)
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")

    # Verificar que la obra no tenga ya un almacén
    existing_almacen = almacen_obra_crud.get_almacen_by_obra(db, almacen.id_obra)
    if existing_almacen:
        raise HTTPException(
            status_code=400,
            detail=f"La obra {obra.codigo_obra} ya tiene un almacén configurado"
        )

    nuevo_almacen = almacen_obra_crud.create_almacen_obra(db=db, almacen=almacen)

    # Cargar el almacén con todas las relaciones
    return db.query(AlmacenObra).options(
        joinedload(AlmacenObra.obra).joinedload(Obra.cliente)
    ).filter(AlmacenObra.id_almacen_obra == nuevo_almacen.id_almacen_obra).first()

@router.put("/{almacen_id}", response_model=AlmacenObraWithRelations)
def actualizar_almacen_obra(
    almacen_id: int,
    almacen_update: AlmacenObraUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar almacén de obra existente
    - Solo se actualizan los campos proporcionados
    """
    # Verificar que el almacén existe
    db_almacen = almacen_obra_crud.get_almacen_obra(db, almacen_id)
    if not db_almacen:
        raise HTTPException(status_code=404, detail="Almacén de obra no encontrado")

    updated_almacen = almacen_obra_crud.update_almacen_obra(
        db=db, almacen_id=almacen_id, almacen_update=almacen_update
    )
    if not updated_almacen:
        raise HTTPException(status_code=404, detail="Error al actualizar el almacén")

    # Cargar el almacén con todas las relaciones
    return db.query(AlmacenObra).options(
        joinedload(AlmacenObra.obra).joinedload(Obra.cliente)
    ).filter(AlmacenObra.id_almacen_obra == almacen_id).first()

@router.delete("/{almacen_id}")
def eliminar_almacen_obra(
    almacen_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar almacén de obra (soft delete)
    - Marca el almacén como inactivo en lugar de eliminarlo físicamente
    """
    success = almacen_obra_crud.delete_almacen_obra(db=db, almacen_id=almacen_id)
    if not success:
        raise HTTPException(status_code=404, detail="Almacén de obra no encontrado")

    return {"message": "Almacén de obra eliminado correctamente"}

@router.patch("/{almacen_id}/toggle", response_model=AlmacenObraWithRelations)
def toggle_estado_almacen(
    almacen_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de un almacén
    """
    almacen = almacen_obra_crud.toggle_almacen_activo(db=db, almacen_id=almacen_id)
    if not almacen:
        raise HTTPException(status_code=404, detail="Almacén de obra no encontrado")

    # Cargar el almacén con todas las relaciones
    return db.query(AlmacenObra).options(
        joinedload(AlmacenObra.obra).joinedload(Obra.cliente)
    ).filter(AlmacenObra.id_almacen_obra == almacen_id).first()

# ========================================
# ENDPOINTS DE CONSULTA ESPECÍFICA
# ========================================

@router.get("/responsable/{responsable}/almacenes", response_model=List[AlmacenObraWithRelations])
def obtener_almacenes_por_responsable(
    responsable: str,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener almacenes de un responsable específico"""
    almacenes = almacen_obra_crud.get_almacenes_by_responsable(db, responsable, activo)

    if not almacenes:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron almacenes para el responsable: {responsable}"
        )

    # Cargar con relaciones
    almacenes_ids = [almacen.id_almacen_obra for almacen in almacenes]
    return db.query(AlmacenObra).options(
        joinedload(AlmacenObra.obra).joinedload(Obra.cliente)
    ).filter(AlmacenObra.id_almacen_obra.in_(almacenes_ids)).all()

@router.get("/condiciones/con-seguridad", response_model=List[AlmacenObraWithRelations])
def obtener_almacenes_con_seguridad(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener almacenes que tienen seguridad"""
    almacenes = almacen_obra_crud.get_almacenes_con_seguridad(db, activo)

    # Cargar con relaciones
    almacenes_ids = [almacen.id_almacen_obra for almacen in almacenes]
    if not almacenes_ids:
        return []

    return db.query(AlmacenObra).options(
        joinedload(AlmacenObra.obra).joinedload(Obra.cliente)
    ).filter(AlmacenObra.id_almacen_obra.in_(almacenes_ids)).all()

@router.get("/condiciones/sin-techo", response_model=List[AlmacenObraWithRelations])
def obtener_almacenes_sin_techo(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener almacenes sin techo (a la intemperie)"""
    almacenes = almacen_obra_crud.get_almacenes_sin_techo(db, activo)

    # Cargar con relaciones
    almacenes_ids = [almacen.id_almacen_obra for almacen in almacenes]
    if not almacenes_ids:
        return []

    return db.query(AlmacenObra).options(
        joinedload(AlmacenObra.obra).joinedload(Obra.cliente)
    ).filter(AlmacenObra.id_almacen_obra.in_(almacenes_ids)).all()

@router.get("/capacidad/rango", response_model=List[AlmacenObraWithRelations])
def obtener_almacenes_por_capacidad(
    capacidad_minima: Optional[float] = Query(None, ge=0, description="Capacidad mínima en m³"),
    capacidad_maxima: Optional[float] = Query(None, ge=0, description="Capacidad máxima en m³"),
    db: Session = Depends(get_db)
):
    """Obtener almacenes filtrados por rango de capacidad"""
    if capacidad_minima is None and capacidad_maxima is None:
        raise HTTPException(
            status_code=400,
            detail="Debe especificar al menos capacidad_minima o capacidad_maxima"
        )

    almacenes = almacen_obra_crud.get_almacenes_por_capacidad(db, capacidad_minima, capacidad_maxima)

    # Cargar con relaciones
    almacenes_ids = [almacen.id_almacen_obra for almacen in almacenes]
    if not almacenes_ids:
        return []

    return db.query(AlmacenObra).options(
        joinedload(AlmacenObra.obra).joinedload(Obra.cliente)
    ).filter(AlmacenObra.id_almacen_obra.in_(almacenes_ids)).all()

@router.get("/buscar/{search_term}", response_model=List[AlmacenObraWithRelations])
def buscar_almacenes(
    search_term: str,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Buscar almacenes por nombre, descripción o responsable
    - Búsqueda insensible a mayúsculas/minúsculas
    - Busca coincidencias parciales
    """
    almacenes = almacen_obra_crud.search_almacenes(db, search_term, activo)

    if not almacenes:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron almacenes con el término de búsqueda: {search_term}"
        )

    # Cargar con relaciones
    almacenes_ids = [almacen.id_almacen_obra for almacen in almacenes]
    return db.query(AlmacenObra).options(
        joinedload(AlmacenObra.obra).joinedload(Obra.cliente)
    ).filter(AlmacenObra.id_almacen_obra.in_(almacenes_ids)).all()

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_almacenes(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de almacenes de obra"""
    from sqlalchemy import func
    query = db.query(func.count(AlmacenObra.id_almacen_obra))

    if activo is not None:
        query = query.filter(AlmacenObra.activo == activo)

    total = query.scalar()
    return {"total_almacenes": total}

@router.get("/stats/resumen")
def estadisticas_resumen(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas generales de almacenes de obra"""
    return almacen_obra_crud.get_estadisticas_almacenes(db)

@router.get("/stats/condiciones")
def estadisticas_condiciones(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de condiciones de almacenes"""
    from sqlalchemy import func

    stats = db.query(
        func.count(AlmacenObra.id_almacen_obra).label('total_almacenes'),
        func.count(func.case(
            [(AlmacenObra.tiene_seguridad == True, 1)]
        )).label('con_seguridad'),
        func.count(func.case(
            [(AlmacenObra.tiene_techo == True, 1)]
        )).label('con_techo'),
        func.count(func.case(
            [(AlmacenObra.tiene_seguridad == True, AlmacenObra.tiene_techo == True, 1)]
        )).label('seguros_y_techados'),
        func.count(func.case(
            [(AlmacenObra.capacidad_m3.isnot(None), 1)]
        )).label('con_capacidad_definida')
    ).filter(AlmacenObra.activo == True).first()

    total = stats.total_almacenes or 0

    return {
        "total_almacenes_activos": total,
        "con_seguridad": {
            "cantidad": stats.con_seguridad or 0,
            "porcentaje": round((stats.con_seguridad / total * 100) if total > 0 else 0, 2)
        },
        "con_techo": {
            "cantidad": stats.con_techo or 0,
            "porcentaje": round((stats.con_techo / total * 100) if total > 0 else 0, 2)
        },
        "seguros_y_techados": {
            "cantidad": stats.seguros_y_techados or 0,
            "porcentaje": round((stats.seguros_y_techados / total * 100) if total > 0 else 0, 2)
        },
        "con_capacidad_definida": {
            "cantidad": stats.con_capacidad_definida or 0,
            "porcentaje": round((stats.con_capacidad_definida / total * 100) if total > 0 else 0, 2)
        }
    }

@router.get("/stats/capacidad")
def estadisticas_capacidad(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de capacidad de almacenes"""
    from sqlalchemy import func

    stats = db.query(
        func.count(AlmacenObra.id_almacen_obra).label('total_con_capacidad'),
        func.sum(AlmacenObra.capacidad_m3).label('capacidad_total'),
        func.avg(AlmacenObra.capacidad_m3).label('capacidad_promedio'),
        func.max(AlmacenObra.capacidad_m3).label('capacidad_maxima'),
        func.min(AlmacenObra.capacidad_m3).label('capacidad_minima')
    ).filter(
        AlmacenObra.activo == True,
        AlmacenObra.capacidad_m3.isnot(None)
    ).first()

    return {
        "almacenes_con_capacidad": stats.total_con_capacidad or 0,
        "capacidad_total_m3": float(stats.capacidad_total or 0),
        "capacidad_promedio_m3": float(stats.capacidad_promedio or 0),
        "capacidad_maxima_m3": float(stats.capacidad_maxima or 0),
        "capacidad_minima_m3": float(stats.capacidad_minima or 0)
    }

@router.get("/stats/por-obra")
def estadisticas_por_obra(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de almacenes por obra"""
    from sqlalchemy import func

    stats = db.query(
        Obra.codigo_obra,
        Obra.nombre_obra,
        Obra.estado,
        AlmacenObra.nombre_almacen,
        AlmacenObra.capacidad_m3,
        AlmacenObra.tiene_seguridad,
        AlmacenObra.tiene_techo
    ).join(AlmacenObra).filter(
        AlmacenObra.activo == True,
        Obra.activo == True
    ).order_by(Obra.codigo_obra.asc()).all()

    return [
        {
            "codigo_obra": stat.codigo_obra,
            "nombre_obra": stat.nombre_obra,
            "estado_obra": stat.estado,
            "nombre_almacen": stat.nombre_almacen,
            "capacidad_m3": float(stat.capacidad_m3 or 0),
            "tiene_seguridad": stat.tiene_seguridad,
            "tiene_techo": stat.tiene_techo
        }
        for stat in stats
    ]