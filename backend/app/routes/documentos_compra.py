from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import DocumentoCompra, DocumentoCompraDetalle, DocumentoCompraArchivo
from schemas import (
    DocumentoCompraCreate,
    DocumentoCompraUpdate,
    DocumentoCompraResponse,
    DocumentoCompraDetalleCreate,
    DocumentoCompraDetalleUpdate,
    DocumentoCompraDetalleResponse
)
import crud

router = APIRouter(prefix="/documentos-compra", tags=["documentos-compra"])

# ========================================
# ENDPOINTS PRINCIPALES DOCUMENTOS
# ========================================

@router.get("/", response_model=List[DocumentoCompraResponse])
def obtener_documentos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    activo: Optional[bool] = Query(None),
    estado: Optional[str] = Query(None),
    tipo_documento: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Obtener lista de documentos de compra con filtros opcionales"""
    try:
        documentos = crud.get_documentos_compra(
            db=db,
            skip=skip,
            limit=limit,
            activo=activo,
            estado=estado,
            tipo_documento=tipo_documento
        )
        return documentos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener documentos: {str(e)}")

@router.get("/{documento_id}", response_model=DocumentoCompraResponse)
def obtener_documento(documento_id: int, db: Session = Depends(get_db)):
    """Obtener un documento específico por ID"""
    documento = crud.get_documento_compra(db=db, documento_id=documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return documento

@router.post("/", response_model=DocumentoCompraResponse)
def crear_documento(documento: DocumentoCompraCreate, db: Session = Depends(get_db)):
    """Crear un nuevo documento de compra"""
    try:
        return crud.create_documento_compra(db=db, documento=documento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear documento: {str(e)}")

@router.put("/{documento_id}", response_model=DocumentoCompraResponse)
def actualizar_documento(
    documento_id: int,
    documento: DocumentoCompraUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un documento existente"""
    documento_existente = crud.get_documento_compra(db=db, documento_id=documento_id)
    if not documento_existente:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    try:
        return crud.update_documento_compra(db=db, documento_id=documento_id, documento=documento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar documento: {str(e)}")

@router.delete("/{documento_id}")
def eliminar_documento(
    documento_id: int,
    permanente: bool = Query(False),
    db: Session = Depends(get_db)
):
    """Eliminar un documento (soft delete por defecto)"""
    documento = crud.get_documento_compra(db=db, documento_id=documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    try:
        if permanente:
            crud.delete_documento_compra_permanent(db=db, documento_id=documento_id)
        else:
            crud.delete_documento_compra(db=db, documento_id=documento_id)
        return {"message": "Documento eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar documento: {str(e)}")

@router.patch("/{documento_id}/activar")
def activar_documento(documento_id: int, db: Session = Depends(get_db)):
    """Activar un documento desactivado"""
    documento = crud.get_documento_compra(db=db, documento_id=documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    try:
        documento_activado = crud.activate_documento_compra(db=db, documento_id=documento_id)
        return {"documento": documento_activado, "message": "Documento activado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al activar documento: {str(e)}")

# ========================================
# ENDPOINTS GESTIÓN DE BODEGA
# ========================================

@router.patch("/{documento_id}/disponible-bodega")
def marcar_disponible_bodega(documento_id: int, db: Session = Depends(get_db)):
    """Marcar documento como disponible para ingreso a bodega"""
    documento = crud.get_documento_compra(db=db, documento_id=documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    if documento.estado != "VALIDADO":
        raise HTTPException(
            status_code=400,
            detail="El documento debe estar validado para ser marcado como disponible para bodega"
        )

    try:
        documento_actualizado = crud.marcar_disponible_bodega(db=db, documento_id=documento_id)
        return {"documento": documento_actualizado, "message": "Documento marcado como disponible para bodega"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al marcar documento: {str(e)}")

@router.patch("/{documento_id}/ingresar-bodega")
def ingresar_bodega(
    documento_id: int,
    usuario_bodeguero_id: int,
    db: Session = Depends(get_db)
):
    """Marcar documento como ingresado a bodega"""
    documento = crud.get_documento_compra(db=db, documento_id=documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    if not documento.disponible_bodega:
        raise HTTPException(
            status_code=400,
            detail="El documento debe estar disponible para bodega"
        )

    try:
        documento_actualizado = crud.ingresar_bodega(
            db=db,
            documento_id=documento_id,
            usuario_bodeguero_id=usuario_bodeguero_id
        )
        return {"documento": documento_actualizado, "message": "Documento ingresado a bodega exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al ingresar documento a bodega: {str(e)}")

# ========================================
# ENDPOINTS DETALLES DEL DOCUMENTO
# ========================================

@router.get("/{documento_id}/detalles", response_model=List[DocumentoCompraDetalleResponse])
def obtener_detalles_documento(documento_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de un documento"""
    documento = crud.get_documento_compra(db=db, documento_id=documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    return crud.get_documento_detalles(db=db, documento_id=documento_id)

@router.post("/{documento_id}/detalles", response_model=DocumentoCompraDetalleResponse)
def agregar_detalle_documento(
    documento_id: int,
    detalle: DocumentoCompraDetalleCreate,
    db: Session = Depends(get_db)
):
    """Agregar un detalle al documento"""
    documento = crud.get_documento_compra(db=db, documento_id=documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    try:
        return crud.create_documento_detalle(db=db, documento_id=documento_id, detalle=detalle)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al agregar detalle: {str(e)}")

@router.put("/{documento_id}/detalles/{detalle_id}", response_model=DocumentoCompraDetalleResponse)
def actualizar_detalle_documento(
    documento_id: int,
    detalle_id: int,
    detalle: DocumentoCompraDetalleUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un detalle del documento"""
    detalle_existente = crud.get_documento_detalle(db=db, detalle_id=detalle_id)
    if not detalle_existente or detalle_existente.id_documento != documento_id:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    try:
        return crud.update_documento_detalle(db=db, detalle_id=detalle_id, detalle=detalle)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al actualizar detalle: {str(e)}")

@router.delete("/{documento_id}/detalles/{detalle_id}")
def eliminar_detalle_documento(
    documento_id: int,
    detalle_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un detalle del documento"""
    detalle = crud.get_documento_detalle(db=db, detalle_id=detalle_id)
    if not detalle or detalle.id_documento != documento_id:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")

    try:
        crud.delete_documento_detalle(db=db, detalle_id=detalle_id)
        return {"message": "Detalle eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al eliminar detalle: {str(e)}")

# ========================================
# ENDPOINTS BÚSQUEDA
# ========================================

@router.get("/search", response_model=List[DocumentoCompraResponse])
def buscar_documentos(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    activo: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Buscar documentos por número, RUT emisor, UUID fiscal, etc."""
    try:
        return crud.search_documentos_compra(
            db=db,
            search_term=q,
            skip=skip,
            limit=limit,
            activo=activo
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en búsqueda: {str(e)}")

# ========================================
# ENDPOINTS ARCHIVOS
# ========================================

@router.post("/{documento_id}/archivos")
def subir_archivo(
    documento_id: int,
    file: UploadFile = File(...),
    tipo_archivo: str = Query(...),
    db: Session = Depends(get_db)
):
    """Subir archivo adjunto al documento"""
    documento = crud.get_documento_compra(db=db, documento_id=documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    # Validar tipo de archivo
    tipos_validos = ["XML", "PDF", "IMAGEN", "OTRO"]
    if tipo_archivo not in tipos_validos:
        raise HTTPException(status_code=400, detail=f"Tipo de archivo debe ser uno de: {tipos_validos}")

    try:
        archivo = crud.upload_documento_archivo(
            db=db,
            documento_id=documento_id,
            file=file,
            tipo_archivo=tipo_archivo
        )
        return {"archivo": archivo, "message": "Archivo subido exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al subir archivo: {str(e)}")

@router.get("/{documento_id}/archivos")
def obtener_archivos_documento(documento_id: int, db: Session = Depends(get_db)):
    """Obtener archivos adjuntos de un documento"""
    documento = crud.get_documento_compra(db=db, documento_id=documento_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    return crud.get_documento_archivos(db=db, documento_id=documento_id)

# ========================================
# ENDPOINTS DESDE ORDEN DE COMPRA
# ========================================

@router.post("/desde-orden-compra/{orden_compra_id}", response_model=DocumentoCompraResponse)
def crear_documento_desde_oc(
    orden_compra_id: int,
    tipo_documento: str,
    db: Session = Depends(get_db)
):
    """Crear documento pre-llenado desde una orden de compra"""
    try:
        documento = crud.create_documento_desde_orden_compra(
            db=db,
            orden_compra_id=orden_compra_id,
            tipo_documento=tipo_documento
        )
        return documento
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear documento desde OC: {str(e)}")

@router.get("/por-orden-compra/{orden_compra_id}", response_model=List[DocumentoCompraResponse])
def obtener_documentos_por_oc(orden_compra_id: int, db: Session = Depends(get_db)):
    """Obtener todos los documentos asociados a una orden de compra"""
    try:
        return crud.get_documentos_by_orden_compra(db=db, orden_compra_id=orden_compra_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener documentos: {str(e)}")