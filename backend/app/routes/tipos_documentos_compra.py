from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Imports locales
from database import get_db
from models import TipoDocumentoCompra
from schemas import TipoDocumentoCompraCreate, TipoDocumentoCompraUpdate, TipoDocumentoCompraResponse
from crud import tipos_documentos_compra_crud

# Configuración del router
router = APIRouter(
    prefix="/tipos-documentos-compra",
    tags=["Tipos de Documentos de Compra"],
    responses={404: {"description": "No encontrado"}}
)

# ========================================
# ENDPOINTS CRUD
# ========================================

@router.get("/", response_model=List[TipoDocumentoCompraResponse])
def listar_tipos_documentos(
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Máximo registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de tipos de documentos de compra con paginación
    - **skip**: Número de registros a saltar (para paginación)
    - **limit**: Máximo número de registros a retornar
    - **activo**: Filtrar solo tipos activos (true) o inactivos (false)
    """
    return tipos_documentos_compra_crud.get_tipos_documentos(db, skip=skip, limit=limit, activo=activo)

@router.get("/{tipo_documento_id}", response_model=TipoDocumentoCompraResponse)
def obtener_tipo_documento(
    tipo_documento_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un tipo de documento por su ID"""
    tipo_documento = tipos_documentos_compra_crud.get_tipo_documento(db, tipo_documento_id)
    if tipo_documento is None:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
    return tipo_documento

@router.get("/nombre/{nombre}", response_model=TipoDocumentoCompraResponse)
def obtener_tipo_documento_por_nombre(
    nombre: str,
    db: Session = Depends(get_db)
):
    """Obtener un tipo de documento por su nombre"""
    tipo_documento = tipos_documentos_compra_crud.get_tipo_documento_by_nombre(db, nombre)
    if tipo_documento is None:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
    return tipo_documento

@router.get("/codigo-dte/{codigo_dte}", response_model=TipoDocumentoCompraResponse)
def obtener_tipo_documento_por_codigo_dte(
    codigo_dte: str,
    db: Session = Depends(get_db)
):
    """Obtener un tipo de documento por su código DTE"""
    tipo_documento = tipos_documentos_compra_crud.get_tipo_documento_by_codigo_dte(db, codigo_dte)
    if tipo_documento is None:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")
    return tipo_documento

@router.post("/", response_model=TipoDocumentoCompraResponse, status_code=201)
def crear_tipo_documento(
    tipo_documento: TipoDocumentoCompraCreate,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo tipo de documento de compra
    - Requiere nombre único
    - Código DTE opcional pero único si se proporciona
    """
    # Verificar si ya existe un tipo con el mismo nombre
    db_tipo = tipos_documentos_compra_crud.get_tipo_documento_by_nombre(db, tipo_documento.nombre)
    if db_tipo:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un tipo de documento con ese nombre"
        )

    # Verificar si ya existe un tipo con el mismo código DTE
    if tipo_documento.codigo_dte:
        db_tipo = tipos_documentos_compra_crud.get_tipo_documento_by_codigo_dte(db, tipo_documento.codigo_dte)
        if db_tipo:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un tipo de documento con ese código DTE"
            )

    return tipos_documentos_compra_crud.create_tipo_documento(db=db, tipo_documento=tipo_documento)

@router.put("/{tipo_documento_id}", response_model=TipoDocumentoCompraResponse)
def actualizar_tipo_documento(
    tipo_documento_id: int,
    tipo_documento_update: TipoDocumentoCompraUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar tipo de documento existente
    - Solo se actualizan los campos proporcionados
    - Si se cambia el nombre o código DTE, deben ser únicos
    """
    # Verificar que el tipo de documento existe
    db_tipo = tipos_documentos_compra_crud.get_tipo_documento(db, tipo_documento_id)
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")

    # Si se está actualizando el nombre, verificar que sea único
    if tipo_documento_update.nombre and tipo_documento_update.nombre != db_tipo.nombre:
        existing_tipo = tipos_documentos_compra_crud.get_tipo_documento_by_nombre(db, tipo_documento_update.nombre)
        if existing_tipo:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un tipo de documento con ese nombre"
            )

    # Si se está actualizando el código DTE, verificar que sea único
    if tipo_documento_update.codigo_dte and tipo_documento_update.codigo_dte != db_tipo.codigo_dte:
        existing_tipo = tipos_documentos_compra_crud.get_tipo_documento_by_codigo_dte(db, tipo_documento_update.codigo_dte)
        if existing_tipo:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un tipo de documento con ese código DTE"
            )

    updated_tipo = tipos_documentos_compra_crud.update_tipo_documento(
        db=db,
        tipo_documento_id=tipo_documento_id,
        tipo_documento_update=tipo_documento_update
    )
    if not updated_tipo:
        raise HTTPException(status_code=404, detail="Error al actualizar el tipo de documento")

    return updated_tipo

@router.delete("/{tipo_documento_id}")
def eliminar_tipo_documento(
    tipo_documento_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar tipo de documento (soft delete)
    - Marca el tipo como inactivo en lugar de eliminarlo físicamente
    """
    success = tipos_documentos_compra_crud.delete_tipo_documento(db=db, tipo_documento_id=tipo_documento_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")

    return {"message": "Tipo de documento eliminado correctamente"}

@router.patch("/{tipo_documento_id}/toggle", response_model=TipoDocumentoCompraResponse)
def toggle_estado_tipo_documento(
    tipo_documento_id: int,
    db: Session = Depends(get_db)
):
    """
    Cambiar estado activo/inactivo de un tipo de documento
    """
    db_tipo = tipos_documentos_compra_crud.get_tipo_documento(db, tipo_documento_id)
    if not db_tipo:
        raise HTTPException(status_code=404, detail="Tipo de documento no encontrado")

    # Cambiar el estado
    tipo_update = TipoDocumentoCompraUpdate(activo=not db_tipo.activo)
    updated_tipo = tipos_documentos_compra_crud.update_tipo_documento(
        db=db,
        tipo_documento_id=tipo_documento_id,
        tipo_documento_update=tipo_update
    )

    return updated_tipo

# ========================================
# ENDPOINTS DE BÚSQUEDA Y ESTADÍSTICAS
# ========================================

@router.get("/search/", response_model=List[TipoDocumentoCompraResponse])
def buscar_tipos_documentos(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """
    Buscar tipos de documentos por nombre o código DTE
    - **q**: Término de búsqueda
    - **activo**: Filtrar solo tipos activos (true) o inactivos (false)
    """
    return tipos_documentos_compra_crud.search(db, search_term=q, activo=activo)

@router.get("/stats/count")
def contar_tipos_documentos(
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    db: Session = Depends(get_db)
):
    """Obtener conteo de tipos de documentos"""
    query = db.query(TipoDocumentoCompra)
    if activo is not None:
        query = query.filter(TipoDocumentoCompra.activo == activo)

    total = query.count()
    return {"total_tipos_documentos": total}
