from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from database import get_db
from models import DevolucionesObraDetalle
from schemas import (
    DevolucionesObraDetalleCreate,
    DevolucionesObraDetalleUpdate,
    DevolucionesObraDetalleResponse,
    DevolucionesObraDetalleWithRelations
)
from crud import devoluciones_obra_detalle_crud

router = APIRouter(
    prefix="/devoluciones-obra-detalle",
    tags=["Detalle Devoluciones de Obra"]
)

@router.post("/", response_model=DevolucionesObraDetalleResponse)
def crear_detalle_devolucion(
    detalle: DevolucionesObraDetalleCreate,
    db: Session = Depends(get_db)
):
    return devoluciones_obra_detalle_crud.create_detalle(db, detalle)

@router.get("/", response_model=List[DevolucionesObraDetalleResponse])
def listar_detalles_devolucion(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return devoluciones_obra_detalle_crud.get_detalles(db, skip=skip, limit=limit)

@router.get("/con-relaciones", response_model=List[DevolucionesObraDetalleWithRelations])
def listar_detalles_con_relaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return (db.query(DevolucionesObraDetalle)
            .options(
                joinedload(DevolucionesObraDetalle.devolucion),
                joinedload(DevolucionesObraDetalle.producto),
                joinedload(DevolucionesObraDetalle.lote),
                joinedload(DevolucionesObraDetalle.ubicacion_recepcion)
            )
            .offset(skip)
            .limit(limit)
            .all())

@router.get("/{id_detalle}", response_model=DevolucionesObraDetalleWithRelations)
def obtener_detalle_devolucion(
    id_detalle: int,
    db: Session = Depends(get_db)
):
    detalle = (db.query(DevolucionesObraDetalle)
               .options(
                   joinedload(DevolucionesObraDetalle.devolucion),
                   joinedload(DevolucionesObraDetalle.producto),
                   joinedload(DevolucionesObraDetalle.lote),
                   joinedload(DevolucionesObraDetalle.ubicacion_recepcion)
               )
               .filter(DevolucionesObraDetalle.id_devolucion_detalle == id_detalle)
               .first())
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de devolución no encontrado")
    return detalle

@router.put("/{id_detalle}", response_model=DevolucionesObraDetalleResponse)
def actualizar_detalle_devolucion(
    id_detalle: int,
    detalle: DevolucionesObraDetalleUpdate,
    db: Session = Depends(get_db)
):
    db_detalle = devoluciones_obra_detalle_crud.update_detalle(db, id_detalle, detalle)
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle de devolución no encontrado")
    return db_detalle

@router.delete("/{id_detalle}")
def eliminar_detalle_devolucion(
    id_detalle: int,
    db: Session = Depends(get_db)
):
    success = devoluciones_obra_detalle_crud.delete_detalle(db, id_detalle)
    if not success:
        raise HTTPException(status_code=404, detail="Detalle de devolución no encontrado")
    return {"message": "Detalle de devolución eliminado correctamente"}

@router.get("/devolucion/{id_devolucion}", response_model=List[DevolucionesObraDetalleWithRelations])
def listar_detalles_por_devolucion(
    id_devolucion: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    detalles = (db.query(DevolucionesObraDetalle)
                .options(
                    joinedload(DevolucionesObraDetalle.producto),
                    joinedload(DevolucionesObraDetalle.lote),
                    joinedload(DevolucionesObraDetalle.ubicacion_recepcion)
                )
                .filter(DevolucionesObraDetalle.id_devolucion == id_devolucion)
                .offset(skip)
                .limit(limit)
                .all())
    return detalles

@router.get("/producto/{id_producto}", response_model=List[DevolucionesObraDetalleWithRelations])
def listar_detalles_por_producto(
    id_producto: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    detalles = (db.query(DevolucionesObraDetalle)
                .options(
                    joinedload(DevolucionesObraDetalle.devolucion),
                    joinedload(DevolucionesObraDetalle.lote),
                    joinedload(DevolucionesObraDetalle.ubicacion_recepcion)
                )
                .filter(DevolucionesObraDetalle.id_producto == id_producto)
                .offset(skip)
                .limit(limit)
                .all())
    return detalles

@router.get("/estado/{estado_producto}", response_model=List[DevolucionesObraDetalleWithRelations])
def listar_productos_por_estado(
    estado_producto: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    estados_validos = ["NUEVO", "USADO_BUENO", "USADO_REGULAR", "DEFECTUOSO", "NO_REUTILIZABLE"]
    if estado_producto not in estados_validos:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Estados válidos: {estados_validos}")

    productos = (db.query(DevolucionesObraDetalle)
                 .options(
                     joinedload(DevolucionesObraDetalle.devolucion),
                     joinedload(DevolucionesObraDetalle.producto),
                     joinedload(DevolucionesObraDetalle.lote),
                     joinedload(DevolucionesObraDetalle.ubicacion_recepcion)
                 )
                 .filter(DevolucionesObraDetalle.estado_producto == estado_producto)
                 .offset(skip)
                 .limit(limit)
                 .all())
    return productos

@router.get("/mantenimiento/limpieza", response_model=List[DevolucionesObraDetalleWithRelations])
def listar_productos_requieren_limpieza(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    productos = (db.query(DevolucionesObraDetalle)
                 .options(
                     joinedload(DevolucionesObraDetalle.devolucion),
                     joinedload(DevolucionesObraDetalle.producto),
                     joinedload(DevolucionesObraDetalle.lote),
                     joinedload(DevolucionesObraDetalle.ubicacion_recepcion)
                 )
                 .filter(DevolucionesObraDetalle.requiere_limpieza == True)
                 .offset(skip)
                 .limit(limit)
                 .all())
    return productos

@router.get("/mantenimiento/reparacion", response_model=List[DevolucionesObraDetalleWithRelations])
def listar_productos_requieren_reparacion(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    productos = (db.query(DevolucionesObraDetalle)
                 .options(
                     joinedload(DevolucionesObraDetalle.devolucion),
                     joinedload(DevolucionesObraDetalle.producto),
                     joinedload(DevolucionesObraDetalle.lote),
                     joinedload(DevolucionesObraDetalle.ubicacion_recepcion)
                 )
                 .filter(DevolucionesObraDetalle.requiere_reparacion == True)
                 .offset(skip)
                 .limit(limit)
                 .all())
    return productos

@router.get("/mantenimiento/calibracion", response_model=List[DevolucionesObraDetalleWithRelations])
def listar_productos_requieren_calibracion(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    productos = (db.query(DevolucionesObraDetalle)
                 .options(
                     joinedload(DevolucionesObraDetalle.devolucion),
                     joinedload(DevolucionesObraDetalle.producto),
                     joinedload(DevolucionesObraDetalle.lote),
                     joinedload(DevolucionesObraDetalle.ubicacion_recepcion)
                 )
                 .filter(DevolucionesObraDetalle.requiere_calibracion == True)
                 .offset(skip)
                 .limit(limit)
                 .all())
    return productos

@router.get("/defectuosos/lista", response_model=List[DevolucionesObraDetalleWithRelations])
def listar_productos_defectuosos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    productos = (db.query(DevolucionesObraDetalle)
                 .options(
                     joinedload(DevolucionesObraDetalle.devolucion),
                     joinedload(DevolucionesObraDetalle.producto),
                     joinedload(DevolucionesObraDetalle.lote),
                     joinedload(DevolucionesObraDetalle.ubicacion_recepcion)
                 )
                 .filter(DevolucionesObraDetalle.estado_producto.in_(["DEFECTUOSO", "NO_REUTILIZABLE"]))
                 .offset(skip)
                 .limit(limit)
                 .all())
    return productos

@router.patch("/{id_detalle}/procesar", response_model=DevolucionesObraDetalleResponse)
def procesar_producto_devuelto(
    id_detalle: int,
    nueva_ubicacion: Optional[int] = Query(None, description="Nueva ubicación de recepción"),
    db: Session = Depends(get_db)
):
    detalle = devoluciones_obra_detalle_crud.procesar_producto_devuelto(db, id_detalle, nueva_ubicacion)
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de devolución no encontrado")
    return detalle

@router.get("/resumen/devolucion/{id_devolucion}")
def obtener_resumen_devolucion(
    id_devolucion: int,
    db: Session = Depends(get_db)
):
    return devoluciones_obra_detalle_crud.get_resumen_por_devolucion(db, id_devolucion)

@router.get("/estadisticas/productos-devueltos")
def obtener_estadisticas_productos_devueltos(db: Session = Depends(get_db)):
    return devoluciones_obra_detalle_crud.get_estadisticas_productos_devueltos(db)