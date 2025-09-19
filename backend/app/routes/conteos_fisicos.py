from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import ConteosFisicos
from schemas import (
    ConteosFisicosCreate,
    ConteosFisicosUpdate,
    ConteosFisicosResponse,
    ConteosFisicosWithRelations
)
from crud import conteos_fisicos_crud

router = APIRouter(
    prefix="/conteos-fisicos",
    tags=["Conteos Físicos"]
)

@router.post("/", response_model=ConteosFisicosResponse)
def crear_conteo(
    conteo: ConteosFisicosCreate,
    db: Session = Depends(get_db)
):
    return conteos_fisicos_crud.create_conteo(db, conteo)

@router.get("/", response_model=List[ConteosFisicosResponse])
def listar_conteos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return conteos_fisicos_crud.get_conteos(db, skip=skip, limit=limit)

@router.get("/con-relaciones", response_model=List[ConteosFisicosWithRelations])
def listar_conteos_con_relaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    return (db.query(ConteosFisicos)
            .options(
                joinedload(ConteosFisicos.programacion),
                joinedload(ConteosFisicos.producto),
                joinedload(ConteosFisicos.ubicacion),
                joinedload(ConteosFisicos.obra),
                joinedload(ConteosFisicos.movimiento_ajuste)
            )
            .offset(skip)
            .limit(limit)
            .all())

@router.get("/{id_conteo}", response_model=ConteosFisicosWithRelations)
def obtener_conteo(
    id_conteo: int,
    db: Session = Depends(get_db)
):
    conteo = (db.query(ConteosFisicos)
              .options(
                  joinedload(ConteosFisicos.programacion),
                  joinedload(ConteosFisicos.producto),
                  joinedload(ConteosFisicos.ubicacion),
                  joinedload(ConteosFisicos.obra),
                  joinedload(ConteosFisicos.movimiento_ajuste)
              )
              .filter(ConteosFisicos.id_conteo == id_conteo)
              .first())
    if not conteo:
        raise HTTPException(status_code=404, detail="Conteo no encontrado")
    return conteo

@router.put("/{id_conteo}", response_model=ConteosFisicosResponse)
def actualizar_conteo(
    id_conteo: int,
    conteo: ConteosFisicosUpdate,
    db: Session = Depends(get_db)
):
    db_conteo = conteos_fisicos_crud.update_conteo(db, id_conteo, conteo)
    if not db_conteo:
        raise HTTPException(status_code=404, detail="Conteo no encontrado")
    return db_conteo

@router.delete("/{id_conteo}")
def eliminar_conteo(
    id_conteo: int,
    db: Session = Depends(get_db)
):
    success = conteos_fisicos_crud.delete_conteo(db, id_conteo)
    if not success:
        raise HTTPException(status_code=404, detail="Conteo no encontrado")
    return {"message": "Conteo eliminado correctamente"}

@router.get("/programacion/{id_programacion}", response_model=List[ConteosFisicosWithRelations])
def listar_conteos_por_programacion(
    id_programacion: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    conteos = (db.query(ConteosFisicos)
               .options(
                   joinedload(ConteosFisicos.producto),
                   joinedload(ConteosFisicos.ubicacion),
                   joinedload(ConteosFisicos.obra),
                   joinedload(ConteosFisicos.movimiento_ajuste)
               )
               .filter(ConteosFisicos.id_programacion == id_programacion)
               .offset(skip)
               .limit(limit)
               .all())
    return conteos

@router.get("/producto/{id_producto}", response_model=List[ConteosFisicosWithRelations])
def listar_conteos_por_producto(
    id_producto: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    conteos = (db.query(ConteosFisicos)
               .options(
                   joinedload(ConteosFisicos.programacion),
                   joinedload(ConteosFisicos.ubicacion),
                   joinedload(ConteosFisicos.obra),
                   joinedload(ConteosFisicos.movimiento_ajuste)
               )
               .filter(ConteosFisicos.id_producto == id_producto)
               .offset(skip)
               .limit(limit)
               .all())
    return conteos

@router.get("/obra/{id_obra}", response_model=List[ConteosFisicosWithRelations])
def listar_conteos_por_obra(
    id_obra: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    conteos = (db.query(ConteosFisicos)
               .options(
                   joinedload(ConteosFisicos.programacion),
                   joinedload(ConteosFisicos.producto),
                   joinedload(ConteosFisicos.ubicacion),
                   joinedload(ConteosFisicos.movimiento_ajuste)
               )
               .filter(ConteosFisicos.id_obra == id_obra)
               .offset(skip)
               .limit(limit)
               .all())
    return conteos

@router.get("/ubicacion/{id_ubicacion}", response_model=List[ConteosFisicosWithRelations])
def listar_conteos_por_ubicacion(
    id_ubicacion: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    conteos = (db.query(ConteosFisicos)
               .options(
                   joinedload(ConteosFisicos.programacion),
                   joinedload(ConteosFisicos.producto),
                   joinedload(ConteosFisicos.obra),
                   joinedload(ConteosFisicos.movimiento_ajuste)
               )
               .filter(ConteosFisicos.id_ubicacion == id_ubicacion)
               .offset(skip)
               .limit(limit)
               .all())
    return conteos

@router.get("/contador/{id_usuario}", response_model=List[ConteosFisicosWithRelations])
def listar_conteos_por_contador(
    id_usuario: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    conteos = (db.query(ConteosFisicos)
               .options(
                   joinedload(ConteosFisicos.programacion),
                   joinedload(ConteosFisicos.producto),
                   joinedload(ConteosFisicos.ubicacion),
                   joinedload(ConteosFisicos.obra),
                   joinedload(ConteosFisicos.movimiento_ajuste)
               )
               .filter(ConteosFisicos.id_usuario_contador == id_usuario)
               .offset(skip)
               .limit(limit)
               .all())
    return conteos

@router.get("/diferencias/listar", response_model=List[ConteosFisicosWithRelations])
def listar_conteos_con_diferencias(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    conteos = (db.query(ConteosFisicos)
               .options(
                   joinedload(ConteosFisicos.programacion),
                   joinedload(ConteosFisicos.producto),
                   joinedload(ConteosFisicos.ubicacion),
                   joinedload(ConteosFisicos.obra),
                   joinedload(ConteosFisicos.movimiento_ajuste)
               )
               .filter(ConteosFisicos.cantidad_fisica != ConteosFisicos.cantidad_sistema)
               .offset(skip)
               .limit(limit)
               .all())
    return conteos

@router.get("/pendientes-ajuste/listar", response_model=List[ConteosFisicosWithRelations])
def listar_conteos_pendientes_ajuste(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    conteos = (db.query(ConteosFisicos)
               .options(
                   joinedload(ConteosFisicos.programacion),
                   joinedload(ConteosFisicos.producto),
                   joinedload(ConteosFisicos.ubicacion),
                   joinedload(ConteosFisicos.obra)
               )
               .filter(
                   ConteosFisicos.cantidad_fisica != ConteosFisicos.cantidad_sistema,
                   ConteosFisicos.ajuste_procesado == False
               )
               .offset(skip)
               .limit(limit)
               .all())
    return conteos

@router.get("/exactitud/listar", response_model=List[ConteosFisicosWithRelations])
def listar_conteos_por_exactitud(
    exactos: bool = Query(True, description="True para conteos exactos, False para conteos con diferencias"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    if exactos:
        conteos = (db.query(ConteosFisicos)
                   .options(
                       joinedload(ConteosFisicos.programacion),
                       joinedload(ConteosFisicos.producto),
                       joinedload(ConteosFisicos.ubicacion),
                       joinedload(ConteosFisicos.obra),
                       joinedload(ConteosFisicos.movimiento_ajuste)
                   )
                   .filter(ConteosFisicos.cantidad_fisica == ConteosFisicos.cantidad_sistema)
                   .offset(skip)
                   .limit(limit)
                   .all())
    else:
        conteos = (db.query(ConteosFisicos)
                   .options(
                       joinedload(ConteosFisicos.programacion),
                       joinedload(ConteosFisicos.producto),
                       joinedload(ConteosFisicos.ubicacion),
                       joinedload(ConteosFisicos.obra),
                       joinedload(ConteosFisicos.movimiento_ajuste)
                   )
                   .filter(ConteosFisicos.cantidad_fisica != ConteosFisicos.cantidad_sistema)
                   .offset(skip)
                   .limit(limit)
                   .all())
    return conteos

@router.get("/rango-fechas", response_model=List[ConteosFisicosWithRelations])
def listar_conteos_por_rango_fechas(
    fecha_inicio: datetime = Query(..., description="Fecha y hora de inicio del rango"),
    fecha_fin: datetime = Query(..., description="Fecha y hora de fin del rango"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    conteos = (db.query(ConteosFisicos)
               .options(
                   joinedload(ConteosFisicos.programacion),
                   joinedload(ConteosFisicos.producto),
                   joinedload(ConteosFisicos.ubicacion),
                   joinedload(ConteosFisicos.obra),
                   joinedload(ConteosFisicos.movimiento_ajuste)
               )
               .filter(
                   ConteosFisicos.fecha_conteo >= fecha_inicio,
                   ConteosFisicos.fecha_conteo <= fecha_fin
               )
               .offset(skip)
               .limit(limit)
               .all())
    return conteos

@router.patch("/{id_conteo}/marcar-ajuste", response_model=ConteosFisicosResponse)
def marcar_ajuste_procesado(
    id_conteo: int,
    id_movimiento_ajuste: int = Query(..., description="ID del movimiento de ajuste creado"),
    db: Session = Depends(get_db)
):
    conteo = conteos_fisicos_crud.marcar_ajuste_procesado(db, id_conteo, id_movimiento_ajuste)
    if not conteo:
        raise HTTPException(status_code=404, detail="Conteo no encontrado")
    return conteo

@router.post("/programacion/{id_programacion}/procesar-ajustes")
def procesar_ajustes_automaticos(
    id_programacion: int,
    db: Session = Depends(get_db)
):
    ajustes = conteos_fisicos_crud.procesar_ajustes_automaticos(db, id_programacion)
    return {
        "message": f"Procesados {len(ajustes)} ajustes para la programación {id_programacion}",
        "ajustes": ajustes
    }

@router.get("/estadisticas/generales")
def obtener_estadisticas_generales(db: Session = Depends(get_db)):
    return conteos_fisicos_crud.get_estadisticas_generales(db)

@router.get("/estadisticas/programacion/{id_programacion}")
def obtener_estadisticas_programacion(
    id_programacion: int,
    db: Session = Depends(get_db)
):
    return conteos_fisicos_crud.get_estadisticas_programacion(db, id_programacion)

@router.get("/resumen/producto/{id_producto}")
def obtener_resumen_por_producto(
    id_producto: int,
    db: Session = Depends(get_db)
):
    return conteos_fisicos_crud.get_resumen_por_producto(db, id_producto)

@router.get("/resumen/pendientes")
def obtener_resumen_pendientes(db: Session = Depends(get_db)):
    conteos_pendientes = conteos_fisicos_crud.get_conteos_pendientes_ajuste(db, limit=1000)
    diferencias_positivas = len([c for c in conteos_pendientes if c.cantidad_fisica > c.cantidad_sistema])
    diferencias_negativas = len([c for c in conteos_pendientes if c.cantidad_fisica < c.cantidad_sistema])

    return {
        "total_pendientes": len(conteos_pendientes),
        "diferencias_positivas": diferencias_positivas,
        "diferencias_negativas": diferencias_negativas,
        "total_productos_afectados": len(set(c.id_producto for c in conteos_pendientes))
    }

@router.get("/analisis/diferencias")
def analizar_diferencias(
    id_programacion: Optional[int] = Query(None, description="Filtrar por programación específica"),
    db: Session = Depends(get_db)
):
    query = db.query(ConteosFisicos).filter(
        ConteosFisicos.cantidad_fisica != ConteosFisicos.cantidad_sistema
    )

    if id_programacion:
        query = query.filter(ConteosFisicos.id_programacion == id_programacion)

    conteos = query.all()

    if not conteos:
        return {"message": "No se encontraron diferencias"}

    diferencias = [c.cantidad_fisica - c.cantidad_sistema for c in conteos]

    return {
        "total_diferencias": len(diferencias),
        "diferencia_promedio": sum(diferencias) / len(diferencias),
        "diferencia_maxima": max(diferencias),
        "diferencia_minima": min(diferencias),
        "sobrantes": len([d for d in diferencias if d > 0]),
        "faltantes": len([d for d in diferencias if d < 0]),
        "valor_total_sobrantes": sum([d for d in diferencias if d > 0]),
        "valor_total_faltantes": abs(sum([d for d in diferencias if d < 0]))
    }