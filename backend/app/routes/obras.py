from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

# Imports locales
from database import get_db
from models import Obra, Cliente
from schemas import ObraCreate, ObraUpdate, ObraResponse, ObraWithRelations, EstadoObraEnum, PrioridadObraEnum
from crud import obra_crud, cliente_crud

# Configuración del router
router = APIRouter(
    prefix="/obras",
    tags=["Obras"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[ObraWithRelations])
def listar_obras(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    estado: Optional[EstadoObraEnum] = Query(None, description="Filtrar por estado de la obra"),
    prioridad: Optional[PrioridadObraEnum] = Query(None, description="Filtrar por prioridad"),
    cliente_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    ciudad: Optional[str] = Query(None, description="Filtrar por ciudad"),
    search: Optional[str] = Query(None, description="Buscar por nombre, código o descripción"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de obras con paginación y filtros
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo obras activas (true) o inactivas (false)
    - **estado**: Filtrar por estado de la obra
    - **prioridad**: Filtrar por prioridad
    - **cliente_id**: Filtrar obras de un cliente específico
    - **ciudad**: Filtrar por ciudad
    - **search**: Buscar en nombre, código o descripción
    """
    # Si hay búsqueda, usar el método de búsqueda
    if search:
        obras = obra_crud.search_obras(db, search, activo)
    # Si hay filtro por cliente, usar método específico
    elif cliente_id:
        obras = obra_crud.get_obras_by_cliente(db, cliente_id, activo)
    # Si hay filtro por estado, usar método específico
    elif estado:
        obras = obra_crud.get_obras_by_estado(db, estado.value, activo)
    # Si hay filtro por prioridad, usar método específico
    elif prioridad:
        obras = obra_crud.get_obras_by_prioridad(db, prioridad.value, activo)
    # Si hay filtro por ciudad, usar método específico
    elif ciudad:
        obras = obra_crud.get_obras_by_ciudad(db, ciudad, activo)
    # Lista general con paginación
    else:
        obras = obra_crud.get_obras(db, skip=skip, limit=limit, activo=activo)

    # Cargar con relaciones
    obras_ids = [obra.id_obra for obra in obras]
    if not obras_ids:
        return []

    return db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra.in_(obras_ids)).all()

@router.get("/{obra_id}", response_model=ObraWithRelations)
def obtener_obra(
    obra_id: int,
    db: Session = Depends(get_db)
):
    """Obtener una obra por su ID con información completa"""
    obra = db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra == obra_id).first()

    if obra is None:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    return obra

@router.get("/codigo/{codigo_obra}", response_model=ObraWithRelations)
def obtener_obra_por_codigo(
    codigo_obra: str,
    db: Session = Depends(get_db)
):
    """Obtener una obra por su código"""
    obra = db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.codigo_obra == codigo_obra).first()

    if obra is None:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    return obra

@router.get("/cliente/{cliente_id}/obras", response_model=List[ObraWithRelations])
def obtener_obras_por_cliente(
    cliente_id: int,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener todas las obras de un cliente específico"""
    # Verificar que el cliente existe
    cliente = cliente_crud.get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    query = db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_cliente == cliente_id)

    if activo is not None:
        query = query.filter(Obra.activo == activo)

    return query.order_by(Obra.fecha_creacion.desc()).all()

@router.post("/", response_model=ObraWithRelations, status_code=201)
def crear_obra(
    obra: ObraCreate,
    usuario_id: Optional[int] = Query(None, description="ID del usuario que crea la obra"),
    db: Session = Depends(get_db)
):
    """
    Crear nueva obra
    - Requiere código único
    - Valida que exista el cliente
    - Valida fechas lógicas
    """
    # Verificar que no existe una obra con el mismo código
    existing_obra = obra_crud.get_obra_by_codigo(db, obra.codigo_obra)
    if existing_obra:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe una obra con código {obra.codigo_obra}"
        )

    # Verificar que el cliente existe
    cliente = cliente_crud.get_cliente(db, obra.id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Validar fechas lógicas
    if obra.fecha_inicio_programada and obra.fecha_fin_programada:
        if obra.fecha_inicio_programada > obra.fecha_fin_programada:
            raise HTTPException(
                status_code=400,
                detail="La fecha de inicio programada no puede ser posterior a la fecha de fin programada"
            )

    if obra.fecha_inicio_real and obra.fecha_fin_real:
        if obra.fecha_inicio_real > obra.fecha_fin_real:
            raise HTTPException(
                status_code=400,
                detail="La fecha de inicio real no puede ser posterior a la fecha de fin real"
            )

    nueva_obra = obra_crud.create_obra(db=db, obra=obra, usuario_id=usuario_id)

    # Cargar la obra con todas las relaciones
    return db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra == nueva_obra.id_obra).first()

@router.put("/{obra_id}", response_model=ObraWithRelations)
def actualizar_obra(
    obra_id: int,
    obra_update: ObraUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar obra existente
    - Solo se actualizan los campos proporcionados
    - Valida relaciones y restricciones
    """
    # Verificar que la obra existe
    db_obra = obra_crud.get_obra(db, obra_id)
    if not db_obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")

    # Si se actualiza el código, verificar unicidad
    if obra_update.codigo_obra and obra_update.codigo_obra != db_obra.codigo_obra:
        existing_obra = obra_crud.get_obra_by_codigo(db, obra_update.codigo_obra)
        if existing_obra:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe una obra con código {obra_update.codigo_obra}"
            )

    # Verificar que el cliente existe (si se actualiza)
    if obra_update.id_cliente:
        cliente = cliente_crud.get_cliente(db, obra_update.id_cliente)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Validar fechas lógicas
    fecha_inicio_prog = obra_update.fecha_inicio_programada if obra_update.fecha_inicio_programada is not None else db_obra.fecha_inicio_programada
    fecha_fin_prog = obra_update.fecha_fin_programada if obra_update.fecha_fin_programada is not None else db_obra.fecha_fin_programada

    if fecha_inicio_prog and fecha_fin_prog:
        if fecha_inicio_prog > fecha_fin_prog:
            raise HTTPException(
                status_code=400,
                detail="La fecha de inicio programada no puede ser posterior a la fecha de fin programada"
            )

    fecha_inicio_real = obra_update.fecha_inicio_real if obra_update.fecha_inicio_real is not None else db_obra.fecha_inicio_real
    fecha_fin_real = obra_update.fecha_fin_real if obra_update.fecha_fin_real is not None else db_obra.fecha_fin_real

    if fecha_inicio_real and fecha_fin_real:
        if fecha_inicio_real > fecha_fin_real:
            raise HTTPException(
                status_code=400,
                detail="La fecha de inicio real no puede ser posterior a la fecha de fin real"
            )

    updated_obra = obra_crud.update_obra(db=db, obra_id=obra_id, obra_update=obra_update)
    if not updated_obra:
        raise HTTPException(status_code=404, detail="Error al actualizar la obra")

    # Cargar la obra con todas las relaciones
    return db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra == obra_id).first()

@router.delete("/{obra_id}")
def eliminar_obra(
    obra_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar obra (soft delete)
    - Solo se pueden eliminar obras en PLANIFICACION o CANCELADAS
    - Marca la obra como inactiva en lugar de eliminarla físicamente
    """
    # Verificar que la obra existe
    db_obra = obra_crud.get_obra(db, obra_id)
    if not db_obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")

    # Intentar eliminar (el CRUD verifica las restricciones)
    success = obra_crud.delete_obra(db=db, obra_id=obra_id)
    if not success:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar la obra. Solo se pueden eliminar obras en PLANIFICACION o CANCELADAS"
        )

    return {"message": "Obra eliminada correctamente"}

@router.patch("/{obra_id}/toggle", response_model=ObraWithRelations)
def toggle_estado_obra(
    obra_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de una obra
    """
    obra = obra_crud.toggle_obra_activa(db=db, obra_id=obra_id)
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")

    # Cargar la obra con todas las relaciones
    return db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra == obra_id).first()

# ========================================
# ENDPOINTS DE GESTIÓN DE ESTADOS
# ========================================

@router.patch("/{obra_id}/estado", response_model=ObraWithRelations)
def cambiar_estado_obra(
    obra_id: int,
    nuevo_estado: EstadoObraEnum,
    usuario_id: Optional[int] = Query(None, description="ID del usuario que realiza el cambio"),
    db: Session = Depends(get_db)
):
    """
    Cambiar estado de una obra con validaciones de negocio
    - Valida transiciones permitidas entre estados
    - Actualiza fechas automáticamente
    """
    obra = obra_crud.cambiar_estado_obra(db=db, obra_id=obra_id, nuevo_estado=nuevo_estado.value, usuario_id=usuario_id)
    if not obra:
        raise HTTPException(
            status_code=400,
            detail="No se puede realizar esta transición de estado o la obra no existe"
        )

    # Cargar la obra con todas las relaciones
    return db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra == obra_id).first()

# ========================================
# ENDPOINTS DE CONSULTA ESPECÍFICA
# ========================================

@router.get("/estado/{estado}/obras", response_model=List[ObraWithRelations])
def obtener_obras_por_estado(
    estado: EstadoObraEnum,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener todas las obras en un estado específico"""
    obras = obra_crud.get_obras_by_estado(db, estado.value, activo)

    # Cargar con relaciones
    obras_ids = [obra.id_obra for obra in obras]
    if not obras_ids:
        return []

    return db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra.in_(obras_ids)).order_by(Obra.fecha_inicio_programada.asc()).all()

@router.get("/prioridad/{prioridad}/obras", response_model=List[ObraWithRelations])
def obtener_obras_por_prioridad(
    prioridad: PrioridadObraEnum,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener todas las obras con una prioridad específica"""
    obras = obra_crud.get_obras_by_prioridad(db, prioridad.value, activo)

    # Cargar con relaciones
    obras_ids = [obra.id_obra for obra in obras]
    if not obras_ids:
        return []

    return db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra.in_(obras_ids)).order_by(Obra.fecha_inicio_programada.asc()).all()

@router.get("/ciudad/{ciudad}/obras", response_model=List[ObraWithRelations])
def obtener_obras_por_ciudad(
    ciudad: str,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener obras de una ciudad específica"""
    obras = obra_crud.get_obras_by_ciudad(db, ciudad, activo)

    if not obras:
        raise HTTPException(status_code=404, detail=f"No se encontraron obras en {ciudad}")

    # Cargar con relaciones
    obras_ids = [obra.id_obra for obra in obras]
    return db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra.in_(obras_ids)).order_by(Obra.nombre_obra.asc()).all()

@router.get("/buscar/{search_term}", response_model=List[ObraWithRelations])
def buscar_obras(
    search_term: str,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Buscar obras por nombre, código o descripción
    - Búsqueda insensible a mayúsculas/minúsculas
    - Busca coincidencias parciales
    """
    obras = obra_crud.search_obras(db, search_term, activo)

    if not obras:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron obras con el término de búsqueda: {search_term}"
        )

    # Cargar con relaciones
    obras_ids = [obra.id_obra for obra in obras]
    return db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra.in_(obras_ids)).order_by(Obra.nombre_obra.asc()).all()

# ========================================
# ENDPOINTS ESPECIALES DE ALERTAS
# ========================================

@router.get("/especiales/vencidas", response_model=List[ObraWithRelations])
def obtener_obras_vencidas(
    db: Session = Depends(get_db)
):
    """Obtener obras que deberían haber terminado pero siguen activas"""
    obras_vencidas = obra_crud.get_obras_vencidas(db)

    # Cargar con relaciones
    obras_ids = [obra.id_obra for obra in obras_vencidas]
    if not obras_ids:
        return []

    return db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra.in_(obras_ids)).order_by(Obra.fecha_fin_programada.asc()).all()

@router.get("/especiales/proximas-inicio", response_model=List[ObraWithRelations])
def obtener_obras_proximas_inicio(
    dias: int = Query(7, ge=1, le=90, description="Días de anticipación"),
    db: Session = Depends(get_db)
):
    """Obtener obras que inician en los próximos X días"""
    obras_proximas = obra_crud.get_obras_proximas_inicio(db, dias)

    # Cargar con relaciones
    obras_ids = [obra.id_obra for obra in obras_proximas]
    if not obras_ids:
        return []

    return db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra.in_(obras_ids)).order_by(Obra.fecha_inicio_programada.asc()).all()

@router.get("/especiales/proximas-fin", response_model=List[ObraWithRelations])
def obtener_obras_proximas_fin(
    dias: int = Query(7, ge=1, le=90, description="Días de anticipación"),
    db: Session = Depends(get_db)
):
    """Obtener obras que terminan en los próximos X días"""
    obras_proximas = obra_crud.get_obras_proximas_fin(db, dias)

    # Cargar con relaciones
    obras_ids = [obra.id_obra for obra in obras_proximas]
    if not obras_ids:
        return []

    return db.query(Obra).options(
        joinedload(Obra.cliente)
    ).filter(Obra.id_obra.in_(obras_ids)).order_by(Obra.fecha_fin_programada.asc()).all()

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_obras(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    estado: Optional[EstadoObraEnum] = Query(None, description="Filtrar por estado"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de obras"""
    from sqlalchemy import func
    query = db.query(func.count(Obra.id_obra))

    if activo is not None:
        query = query.filter(Obra.activo == activo)
    if estado:
        query = query.filter(Obra.estado == estado.value)

    total = query.scalar()
    return {"total_obras": total}

@router.get("/stats/resumen")
def estadisticas_resumen(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas generales de obras"""
    return obra_crud.get_estadisticas_obras(db)

@router.get("/stats/por-estado")
def estadisticas_por_estado(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas detalladas de obras por estado"""
    from sqlalchemy import func

    stats = db.query(
        Obra.estado,
        func.count(Obra.id_obra).label('total_obras'),
        func.sum(Obra.valor_contrato).label('valor_total'),
        func.avg(Obra.valor_contrato).label('valor_promedio')
    ).filter(Obra.activo == True).group_by(Obra.estado).all()

    return [
        {
            "estado": stat.estado,
            "total_obras": stat.total_obras or 0,
            "valor_total": float(stat.valor_total or 0),
            "valor_promedio": float(stat.valor_promedio or 0)
        }
        for stat in stats
    ]

@router.get("/stats/por-cliente")
def estadisticas_por_cliente(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de obras por cliente"""
    from sqlalchemy import func

    stats = db.query(
        Cliente.nombre_cliente,
        Cliente.codigo_cliente,
        func.count(Obra.id_obra).label('total_obras'),
        func.sum(Obra.valor_contrato).label('valor_total'),
        func.count(func.case(
            [(Obra.estado == 'FINALIZADA', 1)]
        )).label('obras_finalizadas')
    ).join(Obra).filter(
        Obra.activo == True
    ).group_by(
        Cliente.id_cliente, Cliente.nombre_cliente, Cliente.codigo_cliente
    ).order_by(
        func.count(Obra.id_obra).desc()
    ).all()

    return [
        {
            "cliente": stat.nombre_cliente,
            "codigo_cliente": stat.codigo_cliente,
            "total_obras": stat.total_obras or 0,
            "valor_total": float(stat.valor_total or 0),
            "obras_finalizadas": stat.obras_finalizadas or 0
        }
        for stat in stats
    ]

@router.get("/stats/cronograma")
def estadisticas_cronograma(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de cumplimiento de cronograma"""
    from sqlalchemy import func
    from datetime import date

    # Obras finalizadas
    obras_finalizadas = db.query(
        func.count(Obra.id_obra).label('total_finalizadas'),
        func.count(func.case(
            [(Obra.fecha_fin_real <= Obra.fecha_fin_programada, 1)]
        )).label('finalizadas_a_tiempo'),
        func.count(func.case(
            [(Obra.fecha_fin_real > Obra.fecha_fin_programada, 1)]
        )).label('finalizadas_tarde')
    ).filter(
        Obra.estado == 'FINALIZADA',
        Obra.fecha_fin_real.isnot(None),
        Obra.fecha_fin_programada.isnot(None),
        Obra.activo == True
    ).first()

    # Obras en ejecución
    obras_ejecucion = db.query(
        func.count(Obra.id_obra).label('total_en_ejecucion'),
        func.count(func.case(
            [(Obra.fecha_fin_programada >= date.today(), 1)]
        )).label('en_tiempo'),
        func.count(func.case(
            [(Obra.fecha_fin_programada < date.today(), 1)]
        )).label('retrasadas')
    ).filter(
        Obra.estado == 'EN_EJECUCION',
        Obra.fecha_fin_programada.isnot(None),
        Obra.activo == True
    ).first()

    total_finalizadas = obras_finalizadas.total_finalizadas or 0
    total_en_ejecucion = obras_ejecucion.total_en_ejecucion or 0

    return {
        "obras_finalizadas": {
            "total": total_finalizadas,
            "a_tiempo": obras_finalizadas.finalizadas_a_tiempo or 0,
            "tarde": obras_finalizadas.finalizadas_tarde or 0,
            "porcentaje_puntualidad": round((obras_finalizadas.finalizadas_a_tiempo / total_finalizadas * 100) if total_finalizadas > 0 else 0, 2)
        },
        "obras_en_ejecucion": {
            "total": total_en_ejecucion,
            "en_tiempo": obras_ejecucion.en_tiempo or 0,
            "retrasadas": obras_ejecucion.retrasadas or 0,
            "porcentaje_en_tiempo": round((obras_ejecucion.en_tiempo / total_en_ejecucion * 100) if total_en_ejecucion > 0 else 0, 2)
        }
    }