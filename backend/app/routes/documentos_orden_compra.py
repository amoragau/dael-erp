from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import DocumentoOrdenCompra, OrdenCompra
from schemas import (
    DocumentoOrdenCompraCreate,
    DocumentoOrdenCompraUpdate,
    DocumentoOrdenCompraResponse,
    TipoDocumentoOC,
    EstadoDocumento
)
import os
import uuid
from datetime import datetime
import xml.etree.ElementTree as ET
import tempfile

router = APIRouter()

# ========================================
# CRUD BÁSICO PARA DOCUMENTOS DE ORDEN DE COMPRA
# ========================================

@router.post("/", response_model=DocumentoOrdenCompraResponse)
def create_documento(
    documento: DocumentoOrdenCompraCreate,
    db: Session = Depends(get_db)
):
    """Crear un nuevo documento asociado a una orden de compra"""

    # Verificar que la orden de compra existe
    orden = db.query(OrdenCompra).filter(OrdenCompra.id_orden_compra == documento.id_orden_compra).first()
    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden de compra no encontrada"
        )

    # Verificar que no existe un documento duplicado
    existing_doc = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.id_orden_compra == documento.id_orden_compra,
        DocumentoOrdenCompra.tipo_documento == documento.tipo_documento,
        DocumentoOrdenCompra.numero_documento == documento.numero_documento,
        DocumentoOrdenCompra.activo == True
    ).first()

    if existing_doc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un documento con este número para esta orden de compra"
        )

    db_documento = DocumentoOrdenCompra(**documento.dict())
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)

    return db_documento

@router.get("/{documento_id}", response_model=DocumentoOrdenCompraResponse)
def get_documento(documento_id: int, db: Session = Depends(get_db)):
    """Obtener un documento por ID"""
    documento = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.id_documento_oc == documento_id,
        DocumentoOrdenCompra.activo == True
    ).first()

    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )

    return documento

@router.get("/", response_model=List[DocumentoOrdenCompraResponse])
def get_documentos(
    id_orden_compra: Optional[int] = None,
    tipo_documento: Optional[TipoDocumentoOC] = None,
    estado: Optional[EstadoDocumento] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener lista de documentos con filtros opcionales"""
    query = db.query(DocumentoOrdenCompra).filter(DocumentoOrdenCompra.activo == True)

    if id_orden_compra:
        query = query.filter(DocumentoOrdenCompra.id_orden_compra == id_orden_compra)

    if tipo_documento:
        query = query.filter(DocumentoOrdenCompra.tipo_documento == tipo_documento)

    if estado:
        query = query.filter(DocumentoOrdenCompra.estado == estado)

    documentos = query.offset(skip).limit(limit).all()
    return documentos

@router.put("/{documento_id}", response_model=DocumentoOrdenCompraResponse)
def update_documento(
    documento_id: int,
    documento: DocumentoOrdenCompraUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un documento"""
    db_documento = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.id_documento_oc == documento_id,
        DocumentoOrdenCompra.activo == True
    ).first()

    if not db_documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )

    update_data = documento.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_documento, field, value)

    db.commit()
    db.refresh(db_documento)

    return db_documento

@router.delete("/{documento_id}")
def delete_documento(documento_id: int, db: Session = Depends(get_db)):
    """Eliminar (desactivar) un documento"""
    db_documento = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.id_documento_oc == documento_id,
        DocumentoOrdenCompra.activo == True
    ).first()

    if not db_documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )

    db_documento.activo = False
    db.commit()

    return {"message": "Documento eliminado exitosamente"}

# ========================================
# ENDPOINTS PARA UPLOAD DE ARCHIVOS
# ========================================

@router.post("/upload/{id_orden_compra}")
def upload_documento(
    id_orden_compra: int,
    tipo_documento: TipoDocumentoOC,
    file: UploadFile = File(...),
    numero_documento: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Subir archivo de documento (XML, PDF, etc.)"""

    # Verificar que la orden de compra existe
    orden = db.query(OrdenCompra).filter(OrdenCompra.id_orden_compra == id_orden_compra).first()
    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden de compra no encontrada"
        )

    # Validar tipo de archivo
    allowed_extensions = {'.xml', '.pdf', '.png', '.jpg', '.jpeg'}
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no permitido. Extensiones permitidas: {allowed_extensions}"
        )

    try:
        # Crear directorio si no existe
        upload_dir = "/var/erp/documentos"
        tipo_dir = "xml" if file_extension == ".xml" else "pdf" if file_extension == ".pdf" else "imagenes"
        full_upload_dir = os.path.join(upload_dir, tipo_dir)
        os.makedirs(full_upload_dir, exist_ok=True)

        # Generar nombre único para el archivo
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(full_upload_dir, unique_filename)

        # Guardar archivo
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)

        # Procesar archivo XML si es el caso
        contenido_xml = None
        datos_extraidos = {}
        errores = []

        if file_extension == ".xml":
            try:
                contenido_xml = content.decode('utf-8')
                datos_extraidos = extraer_datos_xml(contenido_xml)
            except Exception as e:
                errores.append(f"Error procesando XML: {str(e)}")

        # Crear registro en base de datos
        documento_data = {
            "id_orden_compra": id_orden_compra,
            "tipo_documento": tipo_documento,
            "numero_documento": numero_documento or datos_extraidos.get("numero_documento", file.filename),
            "fecha_documento": datos_extraidos.get("fecha_documento", datetime.now().date()),
            "ruta_archivo_original": file_path,
            "contenido_xml": contenido_xml,
            "estado": EstadoDocumento.PROCESADO if not errores else EstadoDocumento.ERROR,
            "errores_procesamiento": "; ".join(errores) if errores else None
        }

        # Agregar datos fiscales si se extrajeron del XML
        if datos_extraidos:
            documento_data.update({
                "serie": datos_extraidos.get("serie"),
                "folio": datos_extraidos.get("folio"),
                "uuid_fiscal": datos_extraidos.get("uuid_fiscal"),
                "rfc_emisor": datos_extraidos.get("rfc_emisor"),
                "rfc_receptor": datos_extraidos.get("rfc_receptor"),
                "subtotal": datos_extraidos.get("subtotal", 0),
                "impuestos": datos_extraidos.get("impuestos", 0),
                "total": datos_extraidos.get("total", 0),
                "moneda": datos_extraidos.get("moneda", "MXN")
            })

        if file_extension == ".xml":
            documento_data["ruta_archivo_xml"] = file_path
        elif file_extension == ".pdf":
            documento_data["ruta_archivo_pdf"] = file_path

        db_documento = DocumentoOrdenCompra(**documento_data)
        db.add(db_documento)
        db.commit()
        db.refresh(db_documento)

        return {
            "mensaje": "Archivo subido exitosamente",
            "id_documento": db_documento.id_documento_oc,
            "archivo_procesado": unique_filename,
            "datos_extraidos": datos_extraidos,
            "errores": errores if errores else None
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error subiendo archivo: {str(e)}"
        )

# ========================================
# ENDPOINTS PARA PROCESAMIENTO DE XML
# ========================================

@router.post("/procesar-xml/{documento_id}")
def procesar_xml_documento(
    documento_id: int,
    validar_sat: bool = True,
    auto_conciliar: bool = True,
    db: Session = Depends(get_db)
):
    """Procesar XML y extraer datos fiscales"""

    documento = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.id_documento_oc == documento_id,
        DocumentoOrdenCompra.activo == True
    ).first()

    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )

    if not documento.contenido_xml:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El documento no contiene XML para procesar"
        )

    try:
        # Extraer datos del XML
        datos_extraidos = extraer_datos_xml(documento.contenido_xml)
        errores = []

        # Validar con SAT si se requiere
        if validar_sat:
            validacion_sat = validar_xml_sat(documento.uuid_fiscal)
            if not validacion_sat["valido"]:
                errores.append(f"XML no válido en SAT: {validacion_sat['error']}")

        # Actualizar documento con datos extraídos
        for campo, valor in datos_extraidos.items():
            if hasattr(documento, campo):
                setattr(documento, campo, valor)

        documento.estado = EstadoDocumento.VALIDADO if not errores else EstadoDocumento.ERROR
        documento.errores_procesamiento = "; ".join(errores) if errores else None
        documento.fecha_procesamiento = datetime.now()

        db.commit()

        # Intentar conciliación automática si se requiere
        resultado_conciliacion = None
        if auto_conciliar and not errores and documento.tipo_documento == TipoDocumentoOC.FACTURA:
            # TODO: Implementar conciliación automática
            resultado_conciliacion = {"mensaje": "Conciliación automática pendiente de implementación"}

        return {
            "exito": True,
            "mensaje": "XML procesado exitosamente",
            "datos_extraidos": datos_extraidos,
            "errores": errores,
            "conciliacion": resultado_conciliacion
        }

    except Exception as e:
        documento.estado = EstadoDocumento.ERROR
        documento.errores_procesamiento = f"Error procesando XML: {str(e)}"
        documento.fecha_procesamiento = datetime.now()
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando XML: {str(e)}"
        )

# ========================================
# FUNCIONES AUXILIARES
# ========================================

def extraer_datos_xml(contenido_xml: str) -> dict:
    """Extraer datos fiscales de un XML de factura"""
    try:
        root = ET.fromstring(contenido_xml)

        # Namespaces comunes para facturas mexicanas
        namespaces = {
            'cfdi': 'http://www.sat.gob.mx/cfd/4',
            'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
        }

        datos = {}

        # Datos básicos del comprobante
        comprobante = root
        datos['serie'] = comprobante.get('Serie', '')
        datos['folio'] = comprobante.get('Folio', '')
        datos['fecha_documento'] = datetime.fromisoformat(comprobante.get('Fecha', '').replace('T', ' ')).date()
        datos['subtotal'] = float(comprobante.get('SubTotal', '0'))
        datos['total'] = float(comprobante.get('Total', '0'))
        datos['moneda'] = comprobante.get('Moneda', 'MXN')
        datos['numero_documento'] = f"{datos['serie']}-{datos['folio']}" if datos['serie'] and datos['folio'] else datos['folio']

        # Impuestos
        impuestos_elem = comprobante.find('.//cfdi:Impuestos', namespaces)
        if impuestos_elem is not None:
            datos['impuestos'] = float(impuestos_elem.get('TotalImpuestosTrasladados', '0'))

        # RFC Emisor
        emisor = comprobante.find('.//cfdi:Emisor', namespaces)
        if emisor is not None:
            datos['rfc_emisor'] = emisor.get('Rfc', '')

        # RFC Receptor
        receptor = comprobante.find('.//cfdi:Receptor', namespaces)
        if receptor is not None:
            datos['rfc_receptor'] = receptor.get('Rfc', '')

        # UUID del Timbre Fiscal Digital
        tfd = comprobante.find('.//tfd:TimbreFiscalDigital', namespaces)
        if tfd is not None:
            datos['uuid_fiscal'] = tfd.get('UUID', '')

        return datos

    except Exception as e:
        raise Exception(f"Error extrayendo datos del XML: {str(e)}")

def validar_xml_sat(uuid_fiscal: str) -> dict:
    """Validar UUID contra el SAT (implementación simplificada)"""
    # TODO: Implementar validación real contra el SAT
    # Por ahora retornamos válido siempre
    if uuid_fiscal:
        return {"valido": True, "mensaje": "UUID válido"}
    else:
        return {"valido": False, "error": "UUID no proporcionado"}

# ========================================
# ENDPOINTS DE CONSULTA
# ========================================

@router.get("/orden/{id_orden_compra}", response_model=List[DocumentoOrdenCompraResponse])
def get_documentos_por_orden(
    id_orden_compra: int,
    tipo_documento: Optional[TipoDocumentoOC] = None,
    db: Session = Depends(get_db)
):
    """Obtener todos los documentos de una orden de compra específica"""

    # Verificar que la orden existe
    orden = db.query(OrdenCompra).filter(OrdenCompra.id_orden_compra == id_orden_compra).first()
    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orden de compra no encontrada"
        )

    query = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.id_orden_compra == id_orden_compra,
        DocumentoOrdenCompra.activo == True
    )

    if tipo_documento:
        query = query.filter(DocumentoOrdenCompra.tipo_documento == tipo_documento)

    return query.all()

@router.get("/por-uuid/{uuid_fiscal}", response_model=DocumentoOrdenCompraResponse)
def get_documento_por_uuid(uuid_fiscal: str, db: Session = Depends(get_db)):
    """Buscar documento por UUID fiscal"""
    documento = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.uuid_fiscal == uuid_fiscal,
        DocumentoOrdenCompra.activo == True
    ).first()

    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento con UUID fiscal no encontrado"
        )

    return documento

@router.get("/pendientes-procesar")
def get_documentos_pendientes_procesar(db: Session = Depends(get_db)):
    """Obtener documentos pendientes de procesar"""
    documentos = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.estado == EstadoDocumento.PENDIENTE,
        DocumentoOrdenCompra.activo == True
    ).all()

    return {
        "total": len(documentos),
        "documentos": documentos
    }