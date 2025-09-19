from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import Nivel, Estante
from schemas import NivelCreate, NivelUpdate, NivelResponse, NivelWithEstante
from crud import nivel_crud, estante_crud

# Configuración del router
router = APIRouter(
    prefix="/niveles",
    tags=["Niveles"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[NivelResponse])
def listar_niveles(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    estante_id: Optional[int] = Query(None, description="Filtrar por estante"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de niveles con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo niveles activos (true) o inactivos (false)
    - **estante_id**: Filtrar niveles de un estante específico
    """
    if estante_id:
        return nivel_crud.get_niveles_by_estante(db, estante_id=estante_id, activo=activo)

    return nivel_crud.get_niveles(db, skip=skip, limit=limit, activo=activo)

@router.get("/{nivel_id}", response_model=NivelWithEstante)
def obtener_nivel(
    nivel_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un nivel por su ID con información del estante, pasillo y bodega"""
    nivel = db.query(Nivel).filter(Nivel.id_nivel == nivel_id).first()
    if nivel is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return nivel

@router.get("/estante/{estante_id}/niveles", response_model=List[NivelResponse])
def obtener_niveles_por_estante(
    estante_id: int,
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener todos los niveles de un estante específico ordenados por número"""
    # Verificar que el estante existe
    estante = estante_crud.get_estante(db, estante_id)
    if not estante:
        raise HTTPException(status_code=404, detail="Estante no encontrado")

    return nivel_crud.get_niveles_by_estante(db, estante_id=estante_id, activo=activo)

@router.post("/", response_model=NivelResponse, status_code=201)
def crear_nivel(
    nivel: NivelCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo nivel
    - Requiere que el estante exista
    - El número de nivel debe ser único dentro del estante
    """
    # Verificar que el estante existe
    estante = estante_crud.get_estante(db, nivel.id_estante)
    if not estante:
        raise HTTPException(status_code=404, detail="Estante no encontrado")

    # Verificar que no existe un nivel con el mismo número en el estante
    existing_nivel = db.query(Nivel).filter(
        Nivel.id_estante == nivel.id_estante,
        Nivel.numero_nivel == nivel.numero_nivel
    ).first()

    if existing_nivel:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe el nivel número {nivel.numero_nivel} en este estante"
        )

    return nivel_crud.create_nivel(db=db, nivel=nivel)

@router.put("/{nivel_id}", response_model=NivelResponse)
def actualizar_nivel(
    nivel_id: int,
    nivel_update: NivelUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar nivel existente
    - Solo se actualizan los campos proporcionados
    - Si se cambia el estante, debe existir
    - Si se cambia el número, debe ser único en el estante
    """
    # Verificar que el nivel existe
    db_nivel = nivel_crud.get_nivel(db, nivel_id)
    if not db_nivel:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    # Si se está actualizando el estante, verificar que existe
    if nivel_update.id_estante and nivel_update.id_estante != db_nivel.id_estante:
        estante = estante_crud.get_estante(db, nivel_update.id_estante)
        if not estante:
            raise HTTPException(status_code=404, detail="Estante no encontrado")

    # Si se está actualizando el número de nivel, verificar unicidad
    if nivel_update.numero_nivel:
        estante_id = nivel_update.id_estante or db_nivel.id_estante
        numero_nivel = nivel_update.numero_nivel

        # Solo verificar si es diferente al actual
        if numero_nivel != db_nivel.numero_nivel or estante_id != db_nivel.id_estante:
            existing_nivel = db.query(Nivel).filter(
                Nivel.id_estante == estante_id,
                Nivel.numero_nivel == numero_nivel,
                Nivel.id_nivel != nivel_id
            ).first()

            if existing_nivel:
                raise HTTPException(
                    status_code=400,
                    detail=f"Ya existe el nivel número {numero_nivel} en este estante"
                )

    updated_nivel = nivel_crud.update_nivel(db=db, nivel_id=nivel_id, nivel_update=nivel_update)
    if not updated_nivel:
        raise HTTPException(status_code=404, detail="Error al actualizar el nivel")

    return updated_nivel

@router.delete("/{nivel_id}")
def eliminar_nivel(
    nivel_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar nivel (soft delete)
    - Marca el nivel como inactivo en lugar de eliminarlo físicamente
    """
    success = nivel_crud.delete_nivel(db=db, nivel_id=nivel_id)
    if not success:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    return {"message": "Nivel eliminado correctamente"}

@router.patch("/{nivel_id}/toggle", response_model=NivelResponse)
def toggle_estado_nivel(
    nivel_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de un nivel
    """
    db_nivel = nivel_crud.get_nivel(db, nivel_id)
    if not db_nivel:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    # Cambiar el estado
    nivel_update = NivelUpdate(activo=not db_nivel.activo)
    updated_nivel = nivel_crud.update_nivel(db=db, nivel_id=nivel_id, nivel_update=nivel_update)

    return updated_nivel

# ========================================
# ENDPOINTS DE ESTADÍSTICAS
# ========================================

@router.get("/stats/count")
def contar_niveles(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    estante_id: Optional[int] = Query(None, description="Filtrar por estante"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de niveles"""
    query = db.query(Nivel)

    if activo is not None:
        query = query.filter(Nivel.activo == activo)

    if estante_id is not None:
        query = query.filter(Nivel.id_estante == estante_id)

    total = query.count()
    return {"total_niveles": total}

@router.get("/stats/por-estante")
def estadisticas_por_estante(
    pasillo_id: Optional[int] = Query(None, description="Filtrar por pasillo"),
    bodega_id: Optional[int] = Query(None, description="Filtrar por bodega"),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de niveles por estante"""
    from sqlalchemy import func
    from models import Bodega, Pasillo

    query = db.query(
        Bodega.codigo_bodega,
        Pasillo.numero_pasillo,
        Estante.codigo_estante,
        func.count(Nivel.id_nivel).label('total_niveles'),
        func.sum(func.cast(Nivel.activo, db.Integer)).label('niveles_activos'),
        func.avg(Nivel.altura_cm).label('altura_promedio'),
        func.sum(Nivel.capacidad_peso_kg).label('capacidad_total')
    ).select_from(Bodega).join(Pasillo).join(Estante).outerjoin(Nivel).group_by(
        Bodega.id_bodega, Bodega.codigo_bodega,
        Pasillo.id_pasillo, Pasillo.numero_pasillo,
        Estante.id_estante, Estante.codigo_estante
    ).filter(
        Bodega.activo == True,
        Pasillo.activo == True,
        Estante.activo == True
    )

    if bodega_id:
        query = query.filter(Bodega.id_bodega == bodega_id)

    if pasillo_id:
        query = query.filter(Pasillo.id_pasillo == pasillo_id)

    stats = query.all()

    return [
        {
            "codigo_bodega": stat.codigo_bodega,
            "numero_pasillo": stat.numero_pasillo,
            "codigo_estante": stat.codigo_estante,
            "total_niveles": stat.total_niveles or 0,
            "niveles_activos": stat.niveles_activos or 0,
            "altura_promedio_cm": float(stat.altura_promedio or 0),
            "capacidad_total_kg": float(stat.capacidad_total or 0)
        }
        for stat in stats
    ]

@router.get("/stats/capacidad")
def estadisticas_capacidad(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de capacidad de niveles"""
    from sqlalchemy import func

    stats = db.query(
        func.count(Nivel.id_nivel).label('total'),
        func.sum(Nivel.capacidad_peso_kg).label('capacidad_total'),
        func.avg(Nivel.capacidad_peso_kg).label('capacidad_promedio'),
        func.avg(Nivel.altura_cm).label('altura_promedio'),
        func.max(Nivel.capacidad_peso_kg).label('capacidad_maxima'),
        func.min(Nivel.capacidad_peso_kg).label('capacidad_minima'),
        func.max(Nivel.altura_cm).label('altura_maxima'),
        func.min(Nivel.altura_cm).label('altura_minima')
    ).filter(Nivel.activo == True).first()

    return {
        "total_niveles_activos": stats.total or 0,
        "capacidad_total_kg": float(stats.capacidad_total or 0),
        "capacidad_promedio_kg": float(stats.capacidad_promedio or 0),
        "capacidad_maxima_kg": float(stats.capacidad_maxima or 0),
        "capacidad_minima_kg": float(stats.capacidad_minima or 0),
        "altura_promedio_cm": float(stats.altura_promedio or 0),
        "altura_maxima_cm": float(stats.altura_maxima or 0),
        "altura_minima_cm": float(stats.altura_minima or 0)
    }

@router.get("/stats/distribucion")
def estadisticas_distribucion(
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de distribución de niveles por ubicación"""
    from sqlalchemy import func
    from models import Bodega, Pasillo

    # Distribución por bodega
    bodega_stats = db.query(
        Bodega.codigo_bodega,
        Bodega.nombre_bodega,
        func.count(Nivel.id_nivel).label('total_niveles')
    ).select_from(Bodega).join(Pasillo).join(Estante).join(Nivel).filter(
        Bodega.activo == True,
        Pasillo.activo == True,
        Estante.activo == True,
        Nivel.activo == True
    ).group_by(Bodega.id_bodega, Bodega.codigo_bodega, Bodega.nombre_bodega).all()

    # Estadísticas generales
    total_niveles = db.query(func.count(Nivel.id_nivel)).filter(Nivel.activo == True).scalar()

    return {
        "total_niveles_sistema": total_niveles or 0,
        "distribucion_por_bodega": [
            {
                "codigo_bodega": stat.codigo_bodega,
                "nombre_bodega": stat.nombre_bodega,
                "total_niveles": stat.total_niveles,
                "porcentaje": round((stat.total_niveles / total_niveles * 100) if total_niveles > 0 else 0, 2)
            }
            for stat in bodega_stats
        ]
    }