from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from database import get_db
from models import InventarioObra
from schemas import (
    InventarioObraCreate,
    InventarioObraUpdate,
    InventarioObraResponse,
    InventarioObraWithRelations
)
from crud import inventario_obra_crud

router = APIRouter(
    prefix="/inventario-obra",
    tags=["Inventario de Obra"]
)

@router.post("/", response_model=InventarioObraResponse)
def crear_inventario(
    inventario: InventarioObraCreate,
    db: Session = Depends(get_db)
):
    # Verificar si ya existe inventario para esta obra y producto
    existing = inventario_obra_crud.get_inventario_by_obra_producto(db, inventario.id_obra, inventario.id_producto)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe inventario para este producto en esta obra")

    return inventario_obra_crud.create_inventario(db, inventario)

@router.get("/", response_model=List[InventarioObraResponse])
def listar_inventarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return inventario_obra_crud.get_inventarios(db, skip=skip, limit=limit)

@router.get("/con-relaciones", response_model=List[InventarioObraWithRelations])
def listar_inventarios_con_relaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return (db.query(InventarioObra)
            .options(
                joinedload(InventarioObra.obra),
                joinedload(InventarioObra.producto)
            )
            .offset(skip)
            .limit(limit)
            .all())

@router.get("/{id_inventario}", response_model=InventarioObraWithRelations)
def obtener_inventario(
    id_inventario: int,
    db: Session = Depends(get_db)
):
    inventario = (db.query(InventarioObra)
                  .options(
                      joinedload(InventarioObra.obra),
                      joinedload(InventarioObra.producto)
                  )
                  .filter(InventarioObra.id_inventario_obra == id_inventario)
                  .first())
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario

@router.put("/{id_inventario}", response_model=InventarioObraResponse)
def actualizar_inventario(
    id_inventario: int,
    inventario: InventarioObraUpdate,
    db: Session = Depends(get_db)
):
    db_inventario = inventario_obra_crud.update_inventario(db, id_inventario, inventario)
    if not db_inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return db_inventario

@router.delete("/{id_inventario}")
def eliminar_inventario(
    id_inventario: int,
    db: Session = Depends(get_db)
):
    success = inventario_obra_crud.delete_inventario(db, id_inventario)
    if not success:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return {"message": "Inventario eliminado correctamente"}

@router.get("/obra/{id_obra}", response_model=List[InventarioObraWithRelations])
def listar_inventario_por_obra(
    id_obra: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    inventarios = (db.query(InventarioObra)
                   .options(joinedload(InventarioObra.producto))
                   .filter(InventarioObra.id_obra == id_obra)
                   .offset(skip)
                   .limit(limit)
                   .all())
    return inventarios

@router.get("/producto/{id_producto}", response_model=List[InventarioObraWithRelations])
def listar_inventario_por_producto(
    id_producto: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    inventarios = (db.query(InventarioObra)
                   .options(joinedload(InventarioObra.obra))
                   .filter(InventarioObra.id_producto == id_producto)
                   .offset(skip)
                   .limit(limit)
                   .all())
    return inventarios

@router.get("/obra/{id_obra}/producto/{id_producto}", response_model=InventarioObraWithRelations)
def obtener_inventario_obra_producto(
    id_obra: int,
    id_producto: int,
    db: Session = Depends(get_db)
):
    inventario = (db.query(InventarioObra)
                  .options(
                      joinedload(InventarioObra.obra),
                      joinedload(InventarioObra.producto)
                  )
                  .filter(
                      InventarioObra.id_obra == id_obra,
                      InventarioObra.id_producto == id_producto
                  )
                  .first())
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado para esta obra y producto")
    return inventario

@router.get("/obra/{id_obra}/herramientas", response_model=List[InventarioObraWithRelations])
def listar_herramientas_por_obra(
    id_obra: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    herramientas = (db.query(InventarioObra)
                    .options(joinedload(InventarioObra.producto))
                    .filter(
                        InventarioObra.id_obra == id_obra,
                        InventarioObra.es_herramienta == True
                    )
                    .offset(skip)
                    .limit(limit)
                    .all())
    return herramientas

@router.get("/obra/{id_obra}/con-stock", response_model=List[InventarioObraWithRelations])
def listar_productos_con_stock(
    id_obra: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    productos = (db.query(InventarioObra)
                 .options(joinedload(InventarioObra.producto))
                 .filter(
                     InventarioObra.id_obra == id_obra,
                     InventarioObra.cantidad_actual > 0
                 )
                 .offset(skip)
                 .limit(limit)
                 .all())
    return productos

@router.get("/obra/{id_obra}/sin-stock", response_model=List[InventarioObraWithRelations])
def listar_productos_sin_stock(
    id_obra: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    productos = (db.query(InventarioObra)
                 .options(joinedload(InventarioObra.producto))
                 .filter(
                     InventarioObra.id_obra == id_obra,
                     InventarioObra.cantidad_actual == 0
                 )
                 .offset(skip)
                 .limit(limit)
                 .all())
    return productos

@router.patch("/{id_inventario}/stock", response_model=InventarioObraResponse)
def actualizar_stock_inventario(
    id_inventario: int,
    cantidad_cambio: int = Query(..., description="Cantidad a agregar (positivo) o quitar (negativo)"),
    motivo: Optional[str] = Query(None, description="Motivo del cambio de stock"),
    db: Session = Depends(get_db)
):
    db_inventario = inventario_obra_crud.get_inventario(db, id_inventario)
    if not db_inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")

    inventario = inventario_obra_crud.actualizar_stock(
        db, db_inventario.id_obra, db_inventario.id_producto, cantidad_cambio, motivo
    )
    return inventario

@router.patch("/obra/{id_obra}/producto/{id_producto}/stock", response_model=InventarioObraResponse)
def actualizar_stock_obra_producto(
    id_obra: int,
    id_producto: int,
    cantidad_cambio: int = Query(..., description="Cantidad a agregar (positivo) o quitar (negativo)"),
    motivo: Optional[str] = Query(None, description="Motivo del cambio de stock"),
    db: Session = Depends(get_db)
):
    inventario = inventario_obra_crud.actualizar_stock(db, id_obra, id_producto, cantidad_cambio, motivo)
    if not inventario:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el stock")
    return inventario

@router.patch("/{id_inventario}/asignar-herramienta", response_model=InventarioObraResponse)
def asignar_herramienta(
    id_inventario: int,
    responsable: str = Query(..., description="Responsable de la herramienta"),
    ubicacion: Optional[str] = Query(None, description="Ubicación específica"),
    db: Session = Depends(get_db)
):
    inventario = inventario_obra_crud.asignar_herramienta(db, id_inventario, responsable, ubicacion)
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado o no es herramienta")
    return inventario

@router.get("/resumen/obra/{id_obra}")
def obtener_resumen_inventario_obra(
    id_obra: int,
    db: Session = Depends(get_db)
):
    return inventario_obra_crud.get_resumen_por_obra(db, id_obra)

@router.get("/estadisticas/general")
def obtener_estadisticas_inventarios(db: Session = Depends(get_db)):
    return inventario_obra_crud.get_estadisticas_generales(db)