from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from database import get_db
from models import DespachosObraDetalle
from schemas import (
    DespachosObraDetalleCreate,
    DespachosObraDetalleUpdate,
    DespachosObraDetalleResponse,
    DespachosObraDetalleWithRelations
)
from crud import despachos_obra_detalle_crud

router = APIRouter(
    prefix="/despachos-obra-detalle",
    tags=["Detalle Despachos de Obra"]
)

@router.post("/", response_model=DespachosObraDetalleResponse)
def crear_detalle_despacho(
    detalle: DespachosObraDetalleCreate,
    db: Session = Depends(get_db)
):
    return despachos_obra_detalle_crud.create_detalle(db, detalle)

@router.get("/", response_model=List[DespachosObraDetalleResponse])
def listar_detalles_despacho(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return despachos_obra_detalle_crud.get_detalles(db, skip=skip, limit=limit)

@router.get("/con-relaciones", response_model=List[DespachosObraDetalleWithRelations])
def listar_detalles_con_relaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return (db.query(DespachosObraDetalle)
            .options(
                joinedload(DespachosObraDetalle.despacho),
                joinedload(DespachosObraDetalle.producto),
                joinedload(DespachosObraDetalle.lote)
            )
            .offset(skip)
            .limit(limit)
            .all())

@router.get("/{id_detalle}", response_model=DespachosObraDetalleWithRelations)
def obtener_detalle_despacho(
    id_detalle: int,
    db: Session = Depends(get_db)
):
    detalle = (db.query(DespachosObraDetalle)
               .options(
                   joinedload(DespachosObraDetalle.despacho),
                   joinedload(DespachosObraDetalle.producto),
                   joinedload(DespachosObraDetalle.lote)
               )
               .filter(DespachosObraDetalle.id_despacho_detalle == id_detalle)
               .first())
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de despacho no encontrado")
    return detalle

@router.put("/{id_detalle}", response_model=DespachosObraDetalleResponse)
def actualizar_detalle_despacho(
    id_detalle: int,
    detalle: DespachosObraDetalleUpdate,
    db: Session = Depends(get_db)
):
    db_detalle = despachos_obra_detalle_crud.update_detalle(db, id_detalle, detalle)
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle de despacho no encontrado")
    return db_detalle

@router.delete("/{id_detalle}")
def eliminar_detalle_despacho(
    id_detalle: int,
    db: Session = Depends(get_db)
):
    success = despachos_obra_detalle_crud.delete_detalle(db, id_detalle)
    if not success:
        raise HTTPException(status_code=404, detail="Detalle de despacho no encontrado")
    return {"message": "Detalle de despacho eliminado correctamente"}

@router.get("/despacho/{id_despacho}", response_model=List[DespachosObraDetalleWithRelations])
def listar_detalles_por_despacho(
    id_despacho: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    detalles = (db.query(DespachosObraDetalle)
                .options(
                    joinedload(DespachosObraDetalle.producto),
                    joinedload(DespachosObraDetalle.lote)
                )
                .filter(DespachosObraDetalle.id_despacho == id_despacho)
                .offset(skip)
                .limit(limit)
                .all())
    return detalles

@router.get("/producto/{id_producto}", response_model=List[DespachosObraDetalleWithRelations])
def listar_detalles_por_producto(
    id_producto: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    detalles = (db.query(DespachosObraDetalle)
                .options(
                    joinedload(DespachosObraDetalle.despacho),
                    joinedload(DespachosObraDetalle.lote)
                )
                .filter(DespachosObraDetalle.id_producto == id_producto)
                .offset(skip)
                .limit(limit)
                .all())
    return detalles

@router.get("/herramientas/despachadas", response_model=List[DespachosObraDetalleWithRelations])
def listar_herramientas_despachadas(
    id_obra: Optional[int] = Query(None, description="Filtrar por obra específica"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    query = (db.query(DespachosObraDetalle)
             .options(
                 joinedload(DespachosObraDetalle.despacho),
                 joinedload(DespachosObraDetalle.producto),
                 joinedload(DespachosObraDetalle.lote)
             )
             .filter(DespachosObraDetalle.es_herramienta == True))

    if id_obra:
        from models import DespachosObra
        query = query.join(DespachosObra).filter(DespachosObra.id_obra == id_obra)

    return query.offset(skip).limit(limit).all()

@router.get("/herramientas/pendientes-devolucion", response_model=List[DespachosObraDetalleWithRelations])
def listar_herramientas_pendientes_devolucion(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    herramientas = (db.query(DespachosObraDetalle)
                    .options(
                        joinedload(DespachosObraDetalle.despacho),
                        joinedload(DespachosObraDetalle.producto),
                        joinedload(DespachosObraDetalle.lote)
                    )
                    .filter(
                        DespachosObraDetalle.es_herramienta == True,
                        DespachosObraDetalle.requiere_devolucion_obligatoria == True,
                        DespachosObraDetalle.cantidad_devuelta < DespachosObraDetalle.cantidad_despachada
                    )
                    .offset(skip)
                    .limit(limit)
                    .all())
    return herramientas

@router.get("/productos/perdidos", response_model=List[DespachosObraDetalleWithRelations])
def listar_productos_perdidos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    productos = (db.query(DespachosObraDetalle)
                 .options(
                     joinedload(DespachosObraDetalle.despacho),
                     joinedload(DespachosObraDetalle.producto),
                     joinedload(DespachosObraDetalle.lote)
                 )
                 .filter(DespachosObraDetalle.cantidad_perdida > 0)
                 .offset(skip)
                 .limit(limit)
                 .all())
    return productos

@router.patch("/{id_detalle}/cantidades", response_model=DespachosObraDetalleResponse)
def actualizar_cantidades_utilizadas(
    id_detalle: int,
    cantidad_utilizada: int = Query(..., ge=0),
    cantidad_devuelta: int = Query(0, ge=0),
    cantidad_perdida: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    detalle = despachos_obra_detalle_crud.actualizar_cantidades_utilizadas(
        db, id_detalle, cantidad_utilizada, cantidad_devuelta, cantidad_perdida
    )
    if not detalle:
        raise HTTPException(
            status_code=400,
            detail="No se pudo actualizar: detalle no encontrado o cantidades exceden lo despachado"
        )
    return detalle

@router.get("/resumen/despacho/{id_despacho}")
def obtener_resumen_despacho(
    id_despacho: int,
    db: Session = Depends(get_db)
):
    return despachos_obra_detalle_crud.get_resumen_por_despacho(db, id_despacho)

@router.get("/estadisticas/herramientas")
def obtener_estadisticas_herramientas(db: Session = Depends(get_db)):
    return despachos_obra_detalle_crud.get_estadisticas_herramientas(db)