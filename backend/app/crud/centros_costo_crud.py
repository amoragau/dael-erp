"""
CRUD operations for Centros de Costo
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import CentroCosto
from app.schemas import CentroCostoCreate, CentroCostoUpdate


def get_all_centros_costo(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    activo: Optional[bool] = None
) -> List[CentroCosto]:
    """
    Obtener todos los centros de costo con paginación opcional
    """
    query = db.query(CentroCosto)

    if activo is not None:
        query = query.filter(CentroCosto.activo == activo)

    return query.offset(skip).limit(limit).all()


def get_centro_costo_by_id(db: Session, id_centro_costo: int) -> Optional[CentroCosto]:
    """
    Obtener un centro de costo por su ID
    """
    return db.query(CentroCosto).filter(CentroCosto.id_centro_costo == id_centro_costo).first()


def get_centro_costo_by_codigo(db: Session, codigo_centro_costo: str) -> Optional[CentroCosto]:
    """
    Obtener un centro de costo por su código
    """
    return db.query(CentroCosto).filter(CentroCosto.codigo_centro_costo == codigo_centro_costo).first()


def create_centro_costo(
    db: Session,
    centro_costo: CentroCostoCreate,
    usuario_id: Optional[int] = None
) -> CentroCosto:
    """
    Crear un nuevo centro de costo
    """
    db_centro_costo = CentroCosto(
        codigo_centro_costo=centro_costo.codigo_centro_costo,
        nombre_centro_costo=centro_costo.nombre_centro_costo,
        descripcion=centro_costo.descripcion,
        id_responsable=centro_costo.id_responsable,
        presupuesto_anual=centro_costo.presupuesto_anual,
        activo=centro_costo.activo,
        usuario_creacion=usuario_id
    )

    db.add(db_centro_costo)
    db.commit()
    db.refresh(db_centro_costo)

    return db_centro_costo


def update_centro_costo(
    db: Session,
    id_centro_costo: int,
    centro_costo: CentroCostoUpdate,
    usuario_id: Optional[int] = None
) -> Optional[CentroCosto]:
    """
    Actualizar un centro de costo existente
    """
    db_centro_costo = get_centro_costo_by_id(db, id_centro_costo)

    if not db_centro_costo:
        return None

    update_data = centro_costo.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_centro_costo, field, value)

    if usuario_id:
        db_centro_costo.usuario_modificacion = usuario_id

    db.commit()
    db.refresh(db_centro_costo)

    return db_centro_costo


def delete_centro_costo(
    db: Session,
    id_centro_costo: int,
    usuario_id: Optional[int] = None
) -> Optional[CentroCosto]:
    """
    Desactivar un centro de costo (soft delete)
    """
    db_centro_costo = get_centro_costo_by_id(db, id_centro_costo)

    if not db_centro_costo:
        return None

    db_centro_costo.activo = False

    if usuario_id:
        db_centro_costo.usuario_modificacion = usuario_id

    db.commit()
    db.refresh(db_centro_costo)

    return db_centro_costo


def get_centros_costo_activos(db: Session) -> List[CentroCosto]:
    """
    Obtener todos los centros de costo activos
    """
    return db.query(CentroCosto).filter(CentroCosto.activo == True).all()


def search_centros_costo(
    db: Session,
    search_term: str,
    activo: Optional[bool] = None
) -> List[CentroCosto]:
    """
    Buscar centros de costo por código o nombre
    """
    query = db.query(CentroCosto).filter(
        (CentroCosto.codigo_centro_costo.contains(search_term)) |
        (CentroCosto.nombre_centro_costo.contains(search_term))
    )

    if activo is not None:
        query = query.filter(CentroCosto.activo == activo)

    return query.all()
