from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
import base64

# Imports locales
from database import get_db
from models import (
    Proveedor, DireccionProveedor, Empresa, DocumentoCompra,
    DocumentoCompraDetalle, ReferenciaDocumento, TipoDocumentoCompra
)
from schemas import DocumentoCompraResponse
from utils.dte_parser import parse_dte_xml

# Configuración del router
router = APIRouter(
    prefix="/importacion-dte",
    tags=["Importación DTE"],
    responses={404: {"description": "No encontrado"}}
)


def buscar_o_crear_proveedor(
    db: Session,
    datos_emisor: Dict[str, Any]
) -> Proveedor:
    """
    Busca un proveedor por RUT o lo crea si no existe

    Args:
        db: Sesión de base de datos
        datos_emisor: Datos del emisor extraídos del XML

    Returns:
        Proveedor encontrado o creado
    """
    rut = datos_emisor.get('rut', '')

    if not rut:
        raise ValueError("El RUT del emisor es requerido")

    # Buscar proveedor por RFC (RUT)
    proveedor = db.query(Proveedor).filter(Proveedor.rfc == rut).first()

    if proveedor:
        # Actualizar datos del proveedor SOLO si los nuevos datos son más completos
        # (para evitar sobrescribir con datos truncados del XML)
        nueva_razon_social = datos_emisor.get('razon_social', '')
        if nueva_razon_social and len(nueva_razon_social) > len(proveedor.razon_social or ''):
            proveedor.razon_social = nueva_razon_social
            proveedor.nombre_proveedor = nueva_razon_social

        if datos_emisor.get('giro') and not proveedor.giro_comercial:
            proveedor.giro_comercial = datos_emisor['giro']
        if datos_emisor.get('telefono') and not proveedor.telefono:
            proveedor.telefono = datos_emisor['telefono']
        if datos_emisor.get('email') and not proveedor.email:
            proveedor.email = datos_emisor['email']

        # Actualizar ACTECOs solo si no existen
        if datos_emisor.get('acteco_1') and not proveedor.acteco_1:
            proveedor.acteco_1 = datos_emisor['acteco_1']
        if datos_emisor.get('acteco_2') and not proveedor.acteco_2:
            proveedor.acteco_2 = datos_emisor['acteco_2']
        if datos_emisor.get('acteco_3') and not proveedor.acteco_3:
            proveedor.acteco_3 = datos_emisor['acteco_3']
        if datos_emisor.get('acteco_4') and not proveedor.acteco_4:
            proveedor.acteco_4 = datos_emisor['acteco_4']

        db.commit()
        db.refresh(proveedor)
    else:
        # Crear nuevo proveedor
        # Generar código de proveedor a partir del RUT
        codigo_proveedor = rut.replace('-', '').replace('.', '')

        proveedor = Proveedor(
            codigo_proveedor=codigo_proveedor,
            nombre_proveedor=datos_emisor.get('razon_social', ''),
            razon_social=datos_emisor.get('razon_social'),
            rfc=rut,
            giro_comercial=datos_emisor.get('giro'),
            acteco_1=datos_emisor.get('acteco_1'),
            acteco_2=datos_emisor.get('acteco_2'),
            acteco_3=datos_emisor.get('acteco_3'),
            acteco_4=datos_emisor.get('acteco_4'),
            telefono=datos_emisor.get('telefono'),
            email=datos_emisor.get('email'),
            pais='Chile',
            activo=True
        )

        db.add(proveedor)
        db.commit()
        db.refresh(proveedor)

        # Crear dirección del proveedor si se proporciona
        if datos_emisor.get('direccion'):
            direccion = DireccionProveedor(
                id_proveedor=proveedor.id_proveedor,
                tipo_direccion='FISCAL',
                direccion=datos_emisor['direccion'],
                comuna=datos_emisor.get('comuna'),
                ciudad=datos_emisor.get('ciudad'),
                pais='Chile',
                es_principal=True,
                activo=True
            )
            db.add(direccion)
            db.commit()

    return proveedor


def buscar_empresa_receptora(
    db: Session,
    rut_receptor: str
) -> Optional[Empresa]:
    """
    Busca la empresa receptora por RUT

    Args:
        db: Sesión de base de datos
        rut_receptor: RUT de la empresa receptora

    Returns:
        Empresa encontrada o None
    """
    if not rut_receptor:
        return None

    return db.query(Empresa).filter(Empresa.rut_empresa == rut_receptor).first()


def buscar_o_crear_tipo_documento(
    db: Session,
    codigo_dte: str
) -> Optional[TipoDocumentoCompra]:
    """
    Busca un tipo de documento por código DTE

    Args:
        db: Sesión de base de datos
        codigo_dte: Código DTE (33, 34, 46, etc.)

    Returns:
        Tipo de documento encontrado o None
    """
    if not codigo_dte:
        return None

    return db.query(TipoDocumentoCompra).filter(
        TipoDocumentoCompra.codigo_dte == codigo_dte
    ).first()


@router.post("/procesar-xml", response_model=DocumentoCompraResponse)
async def procesar_xml_dte(
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Procesa un archivo XML DTE y crea el documento de compra completo

    - Lee el archivo XML
    - Extrae toda la información (encabezado, detalles, referencias)
    - Crea o actualiza el proveedor
    - Verifica la empresa receptora
    - Crea el documento de compra con todos sus detalles y referencias
    """
    try:
        # Leer contenido del archivo
        contenido_xml = await archivo.read()
        xml_string = contenido_xml.decode('utf-8')

        # Parsear el XML
        datos_dte = parse_dte_xml(xml_string)

        encabezado = datos_dte['encabezado']
        detalles = datos_dte['detalles']
        referencias = datos_dte['referencias']

        # 1. Buscar o crear proveedor
        proveedor = buscar_o_crear_proveedor(db, encabezado['emisor'])

        # 2. Buscar empresa receptora
        empresa_receptora = buscar_empresa_receptora(db, encabezado['receptor']['rut'])

        # 3. Buscar tipo de documento
        tipo_documento = buscar_o_crear_tipo_documento(db, encabezado['tipo_dte'])

        # 4. Calcular totales
        totales = encabezado['totales']
        monto_neto = totales.get('monto_neto', 0)
        monto_exento = totales.get('monto_exento', 0)
        iva = totales.get('iva', 0)
        monto_total = totales.get('monto_total', 0)

        # Si hay monto exento, el subtotal es neto + exento
        subtotal = monto_neto + monto_exento if monto_exento > 0 else monto_neto

        # 5. Preparar observaciones con forma de pago y fecha vencimiento
        forma_pago_map = {
            '1': 'CONTADO',
            '2': 'CREDITO',
            '3': 'SIN COSTO'
        }
        forma_pago = forma_pago_map.get(encabezado.get('forma_pago', '1'), 'CONTADO')

        observaciones_parts = [f"Forma de pago: {forma_pago}"]
        if encabezado.get('fecha_vencimiento'):
            observaciones_parts.append(f"Fecha vencimiento: {encabezado['fecha_vencimiento']}")
        observaciones = " | ".join(observaciones_parts)

        # 6. Crear documento de compra
        documento = DocumentoCompra(
            id_proveedor=proveedor.id_proveedor,
            id_tipo_documento=tipo_documento.id_tipo_documento if tipo_documento else None,
            tipo_documento=None,  # Se usará el tipo de documento relacionado
            numero_documento=encabezado['folio'],
            fecha_documento=encabezado['fecha_emision'],
            folio=encabezado['folio'],
            rut_emisor=encabezado['emisor']['rut'],
            rut_receptor=encabezado['receptor']['rut'],
            observaciones=observaciones,
            subtotal=subtotal,
            impuestos=iva,
            descuentos=0,
            total=monto_total,
            moneda='CLP',
            tipo_cambio=1.0,
            contenido_xml=xml_string,
            estado='PENDIENTE',
            disponible_bodega=False,
            activo=True
        )

        db.add(documento)
        db.flush()  # Para obtener el ID del documento

        # 7. Crear detalles del documento
        for detalle_data in detalles:
            # Calcular subtotal y totales de línea
            cantidad = detalle_data.get('cantidad', 1)
            precio_unitario = detalle_data.get('precio_unitario', 0)
            descuento_linea = detalle_data.get('descuento_monto', 0)

            subtotal_linea = (cantidad * precio_unitario) - descuento_linea

            # El IVA se calcula sobre el subtotal si el documento no es exento
            tasa_iva = totales.get('tasa_iva', 19) / 100 if monto_neto > 0 else 0
            impuesto_linea = subtotal_linea * tasa_iva

            total_linea = subtotal_linea + impuesto_linea

            detalle = DocumentoCompraDetalle(
                id_documento=documento.id_documento,
                codigo_producto=detalle_data.get('codigo_item'),
                descripcion=detalle_data.get('nombre_item') or detalle_data.get('descripcion', 'Sin descripción'),
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                descuento_linea=descuento_linea,
                subtotal_linea=subtotal_linea,
                impuesto_linea=impuesto_linea,
                total_linea=total_linea,
                numero_linea=detalle_data.get('numero_linea', 1),
                activo=True
            )

            db.add(detalle)

        # 8. Crear referencias si existen
        for ref_data in referencias:
            # Convertir cadenas vacías a None para campos Enum
            codigo_ref = ref_data.get('codigo_ref')
            if codigo_ref == '':
                codigo_ref = None

            referencia = ReferenciaDocumento(
                id_documento=documento.id_documento,
                numero_linea_ref=ref_data.get('numero_linea_ref', 1),
                tipo_documento_ref=ref_data.get('tipo_documento_ref') or None,
                folio_ref=ref_data.get('folio_ref') or None,
                fecha_ref=ref_data.get('fecha_ref'),
                codigo_ref=codigo_ref,
                razon_ref=ref_data.get('razon_ref') or None,
                activo=True
            )

            db.add(referencia)

        # 9. Guardar todo
        db.commit()
        db.refresh(documento)

        return documento

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar XML: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/test-upload")
async def test_upload(
    archivo: UploadFile = File(...),
):
    """Endpoint de prueba para verificar que el upload funciona"""
    return {
        "filename": archivo.filename,
        "content_type": archivo.content_type,
        "size": archivo.size
    }


@router.post("/debug-request")
async def debug_request(request: Request):
    """Endpoint de diagnóstico para ver qué está llegando"""
    headers = dict(request.headers)
    body = await request.body()

    return {
        "method": request.method,
        "url": str(request.url),
        "headers": headers,
        "body_length": len(body),
        "body_preview": body[:200].decode('utf-8', errors='ignore') if body else None
    }


@router.post("/validar-xml")
async def validar_xml_dte(
    archivo: UploadFile
):
    """
    Valida un archivo XML DTE y retorna la información extraída sin guardarla

    - Lee el archivo XML
    - Extrae toda la información
    - Retorna los datos para previsualización
    """
    try:
        # Leer contenido del archivo
        contenido_xml = await archivo.read()
        xml_string = contenido_xml.decode('utf-8')

        # Parsear el XML
        datos_dte = parse_dte_xml(xml_string)

        return {
            "success": True,
            "datos": datos_dte
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar XML: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
