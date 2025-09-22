from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from datetime import datetime
import re
from decimal import Decimal
from database import get_db
from models import (
    DocumentoOrdenCompra, OrdenCompra, OrdenCompraDetalle,
    Producto, ConciliacionOcFacturas
)
from schemas import (
    ProcesarXMLRequest, ProcesarXMLResponse,
    TipoDocumentoOC, EstadoDocumento
)

router = APIRouter()

# ========================================
# PROCESAMIENTO DE XML DE FACTURAS
# ========================================

@router.post("/procesar-xml-factura/{documento_id}")
def procesar_xml_factura(
    documento_id: int,
    validar_sii: bool = True,
    auto_conciliar: bool = True,
    db: Session = Depends(get_db)
):
    """Procesar XML de factura chilena (DTE) y extraer datos estructurados"""

    documento = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.id_documento_oc == documento_id,
        DocumentoOrdenCompra.activo == True
    ).first()

    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    if not documento.contenido_xml:
        raise HTTPException(
            status_code=400,
            detail="El documento no contiene XML para procesar"
        )

    try:
        # Extraer datos del XML
        datos_extraidos = extraer_datos_completos_xml(documento.contenido_xml)
        errores = []

        # Validar estructura del XML
        validacion_estructura = validar_estructura_xml(documento.contenido_xml)
        if not validacion_estructura["valido"]:
            errores.append(f"Estructura XML inválida: {validacion_estructura['error']}")

        # Validar con SII si se requiere
        if validar_sii and datos_extraidos.get("folio_dte"):
            validacion_sii = validar_xml_contra_sii(datos_extraidos["folio_dte"], datos_extraidos.get("rut_emisor"))
            if not validacion_sii["valido"]:
                errores.append(f"XML no válido en SII: {validacion_sii['error']}")

        # Actualizar documento con datos extraídos
        actualizar_documento_con_datos_xml(documento, datos_extraidos, db)

        # Cambiar estado según resultado
        documento.estado = EstadoDocumento.VALIDADO if not errores else EstadoDocumento.ERROR
        documento.errores_procesamiento = "; ".join(errores) if errores else None
        documento.fecha_procesamiento = datetime.now()

        db.commit()

        # Intentar conciliación automática si se requiere
        resultado_conciliacion = None
        if auto_conciliar and not errores and documento.tipo_documento == TipoDocumentoOC.FACTURA:
            try:
                resultado_conciliacion = iniciar_conciliacion_automatica(documento, datos_extraidos, db)
            except Exception as e:
                resultado_conciliacion = {"error": f"Error en conciliación automática: {str(e)}"}

        return {
            "exito": True,
            "mensaje": "XML procesado exitosamente",
            "datos_extraidos": datos_extraidos,
            "errores": errores,
            "validaciones": {
                "estructura_valida": validacion_estructura["valido"],
                "sii_valido": validacion_sii["valido"] if validar_sii else None
            },
            "conciliacion": resultado_conciliacion
        }

    except Exception as e:
        documento.estado = EstadoDocumento.ERROR
        documento.errores_procesamiento = f"Error procesando XML: {str(e)}"
        documento.fecha_procesamiento = datetime.now()
        db.commit()

        raise HTTPException(
            status_code=500,
            detail=f"Error procesando XML: {str(e)}"
        )

@router.post("/procesar-lote-xml")
def procesar_lote_xml(
    validar_sii: bool = True,
    auto_conciliar: bool = True,
    limite: int = 50,
    db: Session = Depends(get_db)
):
    """Procesar un lote de documentos XML pendientes"""

    # Obtener documentos pendientes de procesar
    documentos_pendientes = db.query(DocumentoOrdenCompra).filter(
        DocumentoOrdenCompra.estado == EstadoDocumento.PENDIENTE,
        DocumentoOrdenCompra.contenido_xml.isnot(None),
        DocumentoOrdenCompra.activo == True
    ).limit(limite).all()

    if not documentos_pendientes:
        return {
            "mensaje": "No hay documentos XML pendientes de procesar",
            "procesados": 0
        }

    resultados = []
    procesados_exitosos = 0
    procesados_con_errores = 0

    for documento in documentos_pendientes:
        try:
            # Procesar cada documento individualmente
            resultado = procesar_xml_factura(
                documento.id_documento_oc,
                validar_sii=validar_sii,
                auto_conciliar=auto_conciliar,
                db=db
            )
            procesados_exitosos += 1
            resultados.append({
                "id_documento": documento.id_documento_oc,
                "numero_documento": documento.numero_documento,
                "exito": True,
                "resultado": resultado
            })

        except Exception as e:
            procesados_con_errores += 1
            resultados.append({
                "id_documento": documento.id_documento_oc,
                "numero_documento": documento.numero_documento,
                "exito": False,
                "error": str(e)
            })

    return {
        "mensaje": f"Procesamiento de lote completado",
        "total_documentos": len(documentos_pendientes),
        "procesados_exitosos": procesados_exitosos,
        "procesados_con_errores": procesados_con_errores,
        "resultados": resultados
    }

# ========================================
# FUNCIONES DE EXTRACCIÓN DE DATOS XML
# ========================================

def extraer_datos_completos_xml(contenido_xml: str) -> Dict[str, Any]:
    """Extraer datos completos de un XML de factura chilena (DTE)"""
    try:
        root = ET.fromstring(contenido_xml)

        # Namespaces comunes para DTE chilenos
        namespaces = {
            'dte': 'http://www.sii.cl/SiiDte',
            'ted': 'http://www.sii.cl/SiiDte/TED'
        }

        datos = {}

        # Buscar documento DTE
        documento_dte = root.find('.//dte:Documento', namespaces)
        if documento_dte is None:
            documento_dte = root.find('.//Documento')  # Sin namespace

        if documento_dte is None:
            raise Exception("No se encontró el elemento Documento en el XML")

        # Buscar encabezado
        encabezado = documento_dte.find('.//Encabezado')
        id_doc = encabezado.find('.//IdDoc') if encabezado else None
        emisor = encabezado.find('.//Emisor') if encabezado else None
        receptor = encabezado.find('.//Receptor') if encabezado else None
        totales = encabezado.find('.//Totales') if encabezado else None

        # Datos del documento
        if id_doc is not None:
            datos['tipo_dte'] = id_doc.findtext('TipoDTE', '')
            datos['folio_dte'] = id_doc.findtext('Folio', '')
            datos['fecha_emision'] = id_doc.findtext('FchEmis', '')
            datos['forma_pago'] = id_doc.findtext('FmaPago', '')
            datos['fecha_vencimiento'] = id_doc.findtext('FchVenc', '')
            datos['terminos_pago'] = id_doc.findtext('TermPagoGlosa', '')

        # Datos del emisor
        if emisor is not None:
            datos['rut_emisor'] = emisor.findtext('RUTEmisor', '')
            datos['razon_social_emisor'] = emisor.findtext('RznSoc', '')
            datos['giro_emisor'] = emisor.findtext('GiroEmis', '')
            datos['telefono_emisor'] = emisor.findtext('Telefono', '')
            datos['correo_emisor'] = emisor.findtext('CorreoEmisor', '')
            datos['codigo_sii_emisor'] = emisor.findtext('CdgSIISucur', '')

            # Dirección del emisor
            dir_emisor = emisor.find('.//DirOrigen')
            if dir_emisor is not None:
                datos['direccion_emisor'] = dir_emisor.findtext('DirOrigen', '')
                datos['comuna_emisor'] = dir_emisor.findtext('CmnaOrigen', '')
                datos['ciudad_emisor'] = dir_emisor.findtext('CiudadOrigen', '')

        # Datos del receptor
        if receptor is not None:
            datos['rut_receptor'] = receptor.findtext('RUTRecep', '')
            datos['razon_social_receptor'] = receptor.findtext('RznSocRecep', '')
            datos['giro_receptor'] = receptor.findtext('GiroRecep', '')
            datos['contacto_receptor'] = receptor.findtext('Contacto', '')
            datos['correo_receptor'] = receptor.findtext('CorreoRecep', '')

            # Dirección del receptor
            dir_receptor = receptor.find('.//DirRecep')
            if dir_receptor is not None:
                datos['direccion_receptor'] = dir_receptor.findtext('DirRecep', '')
                datos['comuna_receptor'] = dir_receptor.findtext('CmnaRecep', '')
                datos['ciudad_receptor'] = dir_receptor.findtext('CiudadRecep', '')

        # Totales
        if totales is not None:
            datos['monto_neto'] = Decimal(totales.findtext('MntNeto', '0'))
            datos['monto_exento'] = Decimal(totales.findtext('MntExe', '0'))
            datos['tasa_iva'] = Decimal(totales.findtext('TasaIVA', '19'))
            datos['iva'] = Decimal(totales.findtext('IVA', '0'))
            datos['monto_total'] = Decimal(totales.findtext('MntTotal', '0'))
            datos['moneda'] = totales.findtext('TpoMoneda', 'CLP')

        # Detalle de productos/servicios
        detalles = []
        for detalle in documento_dte.findall('.//Detalle'):
            detalle_data = {
                'numero_linea': detalle.findtext('NroLinDet', ''),
                'codigo_item': detalle.findtext('CdgItem/VlrCodigo', ''),
                'nombre_item': detalle.findtext('NmbItem', ''),
                'descripcion_item': detalle.findtext('DscItem', ''),
                'cantidad': Decimal(detalle.findtext('QtyItem', '0')),
                'unidad_medida': detalle.findtext('UnmdItem', ''),
                'precio_unitario': Decimal(detalle.findtext('PrcItem', '0')),
                'descuento_pct': Decimal(detalle.findtext('DescuentoPct', '0')),
                'descuento_monto': Decimal(detalle.findtext('DescuentoMonto', '0')),
                'monto_item': Decimal(detalle.findtext('MontoItem', '0'))
            }
            detalles.append(detalle_data)

        datos['detalles'] = detalles

        # CAF (Código de Autorización de Folios) - opcional
        caf_data = {}
        ted = documento_dte.find('.//TED')
        if ted is not None:
            datos['ted_timbre'] = ET.tostring(ted, encoding='unicode')

            # Extraer datos del timbre electrónico
            dd = ted.find('.//DD')
            if dd is not None:
                caf_data['rut_emisor_ted'] = dd.findtext('RE', '')
                caf_data['tipo_dte_ted'] = dd.findtext('TD', '')
                caf_data['folio_ted'] = dd.findtext('F', '')
                caf_data['fecha_ted'] = dd.findtext('FE', '')
                caf_data['rut_receptor_ted'] = dd.findtext('RR', '')
                caf_data['monto_total_ted'] = dd.findtext('MNT', '')

        datos['caf_info'] = caf_data

        return datos

    except Exception as e:
        raise Exception(f"Error extrayendo datos del XML: {str(e)}")

def validar_estructura_xml(contenido_xml: str) -> Dict[str, Any]:
    """Validar estructura básica de XML de DTE chileno"""
    try:
        root = ET.fromstring(contenido_xml)

        errores = []

        # Buscar documento DTE
        namespaces = {'dte': 'http://www.sii.cl/SiiDte'}
        documento = root.find('.//dte:Documento', namespaces)
        if documento is None:
            documento = root.find('.//Documento')  # Sin namespace

        if documento is None:
            errores.append("No se encontró el elemento Documento")
            return {
                "valido": False,
                "errores": errores,
                "version_dte": None
            }

        # Buscar encabezado
        encabezado = documento.find('.//Encabezado')
        if encabezado is None:
            errores.append("Falta encabezado del documento")

        # Validar IdDoc
        id_doc = encabezado.find('.//IdDoc') if encabezado else None
        if id_doc is None:
            errores.append("Falta información del documento (IdDoc)")
        else:
            if not id_doc.findtext('TipoDTE'):
                errores.append("Falta tipo de DTE")
            if not id_doc.findtext('Folio'):
                errores.append("Falta número de folio")
            if not id_doc.findtext('FchEmis'):
                errores.append("Falta fecha de emisión")

        # Validar emisor
        emisor = encabezado.find('.//Emisor') if encabezado else None
        if emisor is None:
            errores.append("Falta información del emisor")
        else:
            if not emisor.findtext('RUTEmisor'):
                errores.append("Falta RUT del emisor")
            if not emisor.findtext('RznSoc'):
                errores.append("Falta razón social del emisor")

        # Validar receptor
        receptor = encabezado.find('.//Receptor') if encabezado else None
        if receptor is None:
            errores.append("Falta información del receptor")
        else:
            if not receptor.findtext('RUTRecep'):
                errores.append("Falta RUT del receptor")

        # Validar totales
        totales = encabezado.find('.//Totales') if encabezado else None
        if totales is None:
            errores.append("Falta información de totales")
        else:
            if not totales.findtext('MntTotal'):
                errores.append("Falta monto total")

        # Validar TED (Timbre Electrónico) - opcional pero recomendado
        ted = documento.find('.//TED')
        if ted is None:
            errores.append("Advertencia: Falta Timbre Electrónico (TED)")

        return {
            "valido": len(errores) == 0,
            "errores": errores,
            "version_dte": root.get('version', 'No identificada'),
            "tipo_documento": "DTE Chileno"
        }

    except ET.ParseError as e:
        return {
            "valido": False,
            "errores": [f"XML malformado: {str(e)}"],
            "version_cfdi": None
        }
    except Exception as e:
        return {
            "valido": False,
            "errores": [f"Error validando XML: {str(e)}"],
            "version_cfdi": None
        }

def validar_xml_contra_sii(folio_dte: str, rut_emisor: str = None) -> Dict[str, Any]:
    """Validar DTE contra el servicio del SII (implementación simplificada)"""

    # TODO: Implementar validación real contra el SII
    # Este sería el endpoint real del SII para verificación de DTE

    try:
        # Validar formato del folio
        if not folio_dte or not folio_dte.isdigit():
            return {
                "valido": False,
                "error": "Formato de folio DTE inválido",
                "folio": folio_dte
            }

        # Validar formato del RUT si se proporciona
        if rut_emisor:
            # Patrón básico para RUT chileno (12345678-9)
            rut_pattern = re.compile(r'^\d{7,8}-[\dkK]$')
            if not rut_pattern.match(rut_emisor):
                return {
                    "valido": False,
                    "error": "Formato de RUT inválido",
                    "rut": rut_emisor
                }

        # Por ahora retornamos válido para folios con formato correcto
        # En implementación real se haría la consulta al SII
        return {
            "valido": True,
            "mensaje": "Folio DTE con formato válido (validación SII pendiente de implementar)",
            "folio": folio_dte,
            "rut_emisor": rut_emisor,
            "estado_sii": "NO_VERIFICADO"
        }

    except Exception as e:
        return {
            "valido": False,
            "error": f"Error validando con SII: {str(e)}",
            "folio": folio_dte
        }

def actualizar_documento_con_datos_xml(documento: DocumentoOrdenCompra, datos: Dict[str, Any], db: Session):
    """Actualizar documento con datos extraídos del XML de DTE chileno"""

    # Actualizar campos básicos del DTE
    documento.serie = datos.get('tipo_dte', '')  # Tipo de DTE como serie
    documento.folio = datos.get('folio_dte', '')
    documento.uuid_fiscal = datos.get('ted_timbre', '')  # TED como identificador único
    documento.rfc_emisor = datos.get('rut_emisor', '')  # RUT emisor
    documento.rfc_receptor = datos.get('rut_receptor', '')  # RUT receptor
    documento.subtotal = datos.get('monto_neto', 0)
    documento.impuestos = datos.get('iva', 0)
    documento.descuentos = datos.get('monto_exento', 0)  # Monto exento como descuento
    documento.total = datos.get('monto_total', 0)
    documento.moneda = datos.get('moneda', 'CLP')
    documento.tipo_cambio = Decimal('1.0')  # CLP es moneda base

    # Procesar fecha de emisión
    if datos.get('fecha_emision'):
        try:
            # Formato fecha chilena YYYY-MM-DD
            fecha_str = datos['fecha_emision']
            if len(fecha_str) == 10:  # YYYY-MM-DD
                documento.fecha_documento = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            pass  # Mantener fecha actual si no se puede parsear

    if datos.get('numero_documento'):
        documento.numero_documento = datos['numero_documento']

def iniciar_conciliacion_automatica(documento: DocumentoOrdenCompra, datos_xml: Dict[str, Any], db: Session):
    """Iniciar proceso de conciliación automática basado en XML procesado"""

    try:
        # Buscar orden de compra asociada
        orden = db.query(OrdenCompra).filter(
            OrdenCompra.id_orden_compra == documento.id_orden_compra
        ).first()

        if not orden:
            return {"error": "Orden de compra no encontrada"}

        # Verificar que no existe conciliación previa
        conciliacion_existente = db.query(ConciliacionOcFacturas).filter(
            ConciliacionOcFacturas.id_orden_compra == documento.id_orden_compra,
            ConciliacionOcFacturas.id_documento_factura == documento.id_documento_oc,
            ConciliacionOcFacturas.activo == True
        ).first()

        if conciliacion_existente:
            return {"mensaje": "Ya existe una conciliación para esta orden y factura"}

        # TODO: Implementar lógica de conciliación automática más sofisticada
        # Por ahora solo retornamos que está pendiente

        return {
            "mensaje": "Conciliación automática iniciada",
            "requiere_revision_manual": True,
            "motivo": "Implementación de conciliación automática pendiente"
        }

    except Exception as e:
        return {"error": f"Error en conciliación automática: {str(e)}"}

# ========================================
# UTILIDADES ADICIONALES
# ========================================

@router.get("/validar-folio/{folio_dte}")
def validar_folio_individual(folio_dte: str, rut_emisor: str = None):
    """Validar un folio DTE específico contra el SII"""
    resultado = validar_xml_contra_sii(folio_dte, rut_emisor)
    return resultado

@router.post("/extraer-datos-xml")
def extraer_datos_xml_texto(contenido_xml: str):
    """Extraer datos de XML proporcionado como texto"""
    try:
        datos = extraer_datos_completos_xml(contenido_xml)
        validacion = validar_estructura_xml(contenido_xml)

        return {
            "exito": True,
            "datos_extraidos": datos,
            "validacion_estructura": validacion
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error procesando XML: {str(e)}"
        )

@router.get("/estadisticas-procesamiento")
def get_estadisticas_procesamiento_xml(db: Session = Depends(get_db)):
    """Obtener estadísticas de procesamiento de documentos XML"""

    # Contar documentos por estado
    stats = db.query(
        DocumentoOrdenCompra.estado,
        func.count(DocumentoOrdenCompra.id_documento_oc).label('cantidad')
    ).filter(
        DocumentoOrdenCompra.contenido_xml.isnot(None),
        DocumentoOrdenCompra.activo == True
    ).group_by(DocumentoOrdenCompra.estado).all()

    estadisticas = {estado: 0 for estado in ['PENDIENTE', 'PROCESADO', 'ERROR', 'VALIDADO']}
    for stat in stats:
        estadisticas[stat.estado] = stat.cantidad

    # Documentos procesados hoy
    hoy = datetime.now().date()
    procesados_hoy = db.query(func.count(DocumentoOrdenCompra.id_documento_oc)).filter(
        func.date(DocumentoOrdenCompra.fecha_procesamiento) == hoy,
        DocumentoOrdenCompra.activo == True
    ).scalar()

    # Errores más comunes
    errores_comunes = db.query(
        DocumentoOrdenCompra.errores_procesamiento,
        func.count(DocumentoOrdenCompra.id_documento_oc).label('frecuencia')
    ).filter(
        DocumentoOrdenCompra.estado == 'ERROR',
        DocumentoOrdenCompra.errores_procesamiento.isnot(None),
        DocumentoOrdenCompra.activo == True
    ).group_by(
        DocumentoOrdenCompra.errores_procesamiento
    ).order_by(
        func.count(DocumentoOrdenCompra.id_documento_oc).desc()
    ).limit(5).all()

    return {
        "estadisticas_por_estado": estadisticas,
        "total_documentos_xml": sum(estadisticas.values()),
        "procesados_hoy": procesados_hoy,
        "tasa_exito": round(
            (estadisticas['PROCESADO'] + estadisticas['VALIDADO']) / sum(estadisticas.values()) * 100
            if sum(estadisticas.values()) > 0 else 0, 2
        ),
        "errores_mas_comunes": [
            {"error": error.errores_procesamiento, "frecuencia": error.frecuencia}
            for error in errores_comunes
        ]
    }