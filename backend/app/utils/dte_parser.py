"""
Parser para archivos XML de DTE (Documentos Tributarios Electrónicos) chilenos
Extrae toda la información relevante del XML excluyendo TED y Signature
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any
from datetime import datetime, date
import re


class DTEParser:
    """Parser para archivos XML DTE"""

    # Namespace del SII (Servicio de Impuestos Internos de Chile)
    NAMESPACES = {
        'sii': 'http://www.sii.cl/SiiDte',
        '': 'http://www.sii.cl/SiiDte'
    }

    def __init__(self, xml_content: str):
        """
        Inicializa el parser con el contenido XML

        Args:
            xml_content: Contenido del archivo XML como string
        """
        # Limpiar espacios en blanco al inicio y final del XML
        self.xml_content = xml_content.strip()
        self.root = None
        self._parse_xml()

    def _parse_xml(self):
        """Parse el XML y guarda el elemento raíz"""
        try:
            self.root = ET.fromstring(self.xml_content)
        except ET.ParseError as e:
            raise ValueError(f"Error al parsear XML: {str(e)}")

    def _get_text(self, element: Optional[ET.Element], path: str, default: str = "") -> str:
        """
        Obtiene el texto de un elemento usando XPath

        Args:
            element: Elemento padre
            path: Ruta XPath al elemento
            default: Valor por defecto si no se encuentra

        Returns:
            Texto del elemento o valor por defecto
        """
        if element is None:
            return default

        # Intentar sin namespace primero (más común en DTEs simples)
        found = element.find(path.replace('sii:', ''))
        if found is not None and found.text:
            return found.text.strip()

        # Intentar con namespace (DTEs del SII oficiales)
        found = element.find(path, self.NAMESPACES)
        if found is not None and found.text:
            return found.text.strip()

        return default

    def _format_rut(self, rut: str) -> str:
        """
        Formatea RUT chileno eliminando puntos y dejando el guión

        Args:
            rut: RUT a formatear

        Returns:
            RUT formateado
        """
        if not rut:
            return ""

        # Eliminar puntos y espacios
        rut = rut.replace('.', '').replace(' ', '')

        # Asegurar que tenga guión
        if '-' not in rut and len(rut) > 1:
            rut = rut[:-1] + '-' + rut[-1]

        return rut

    def _parse_date(self, date_str: str) -> Optional[date]:
        """
        Parsea una fecha en formato YYYY-MM-DD

        Args:
            date_str: Fecha como string

        Returns:
            Objeto date o None
        """
        if not date_str:
            return None

        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return None

    def extract_encabezado(self) -> Dict[str, Any]:
        """
        Extrae la información del encabezado del DTE

        Returns:
            Diccionario con datos del encabezado
        """
        # Buscar el elemento Documento (sin namespace primero, luego con namespace)
        documento = self.root.find('.//Documento')
        if documento is None:
            documento = self.root.find('.//DTE/Documento')
        if documento is None:
            documento = self.root.find('.//Documento', self.NAMESPACES)
        if documento is None:
            documento = self.root.find('.//DTE/Documento', self.NAMESPACES)
        if documento is None:
            raise ValueError("No se encontró el elemento Documento en el XML")

        # Buscar Encabezado (sin namespace primero)
        encabezado = documento.find('.//Encabezado') or documento.find('.//Encabezado', self.NAMESPACES)
        if encabezado is None:
            raise ValueError("No se encontró el elemento Encabezado en el XML")

        # ID del documento
        id_doc = encabezado.find('.//IdDoc') or encabezado.find('.//IdDoc', self.NAMESPACES)

        # Emisor (Proveedor)
        emisor = encabezado.find('.//Emisor') or encabezado.find('.//Emisor', self.NAMESPACES)

        # Receptor (Empresa)
        receptor = encabezado.find('.//Receptor') or encabezado.find('.//Receptor', self.NAMESPACES)

        # Totales
        totales = encabezado.find('.//Totales') or encabezado.find('.//Totales', self.NAMESPACES)

        data = {
            # Información del documento
            'tipo_dte': self._get_text(id_doc, './/TipoDTE'),
            'folio': self._get_text(id_doc, './/Folio'),
            'fecha_emision': self._parse_date(self._get_text(id_doc, './/FchEmis')),
            'fecha_vencimiento': self._parse_date(self._get_text(id_doc, './/FchVenc')),
            'forma_pago': self._get_text(id_doc, './/FmaPago'),  # 1=Contado, 2=Crédito, 3=Sin costo
            'fecha_cancelacion': self._parse_date(self._get_text(id_doc, './/FchCancel')),
            'periodo_desde': self._parse_date(self._get_text(id_doc, './/PeriodoDesde')),
            'periodo_hasta': self._parse_date(self._get_text(id_doc, './/PeriodoHasta')),

            # Emisor (Proveedor)
            'emisor': {
                'rut': self._format_rut(self._get_text(emisor, './/RUTEmisor')),
                'razon_social': self._get_text(emisor, './/RznSoc') or self._get_text(emisor, './/RznSocEmisor'),
                'giro': self._get_text(emisor, './/GiroEmis') or self._get_text(emisor, './/GiroEmisor'),
                'telefono': self._get_text(emisor, './/Telefono'),
                'email': self._get_text(emisor, './/CorreoEmisor'),
                'acteco_1': self._get_text(emisor, './/Acteco'),
                'acteco_2': self._get_text(emisor, './/Acteco[2]'),
                'acteco_3': self._get_text(emisor, './/Acteco[3]'),
                'acteco_4': self._get_text(emisor, './/Acteco[4]'),
                'codigo_sucursal': self._get_text(emisor, './/CdgSIISucur'),
                'direccion': self._get_text(emisor, './/DirOrigen'),
                'comuna': self._get_text(emisor, './/CmnaOrigen'),
                'ciudad': self._get_text(emisor, './/CiudadOrigen'),
            },

            # Receptor (Empresa)
            'receptor': {
                'rut': self._format_rut(self._get_text(receptor, './/RUTRecep')),
                'razon_social': self._get_text(receptor, './/RznSocRecep'),
                'giro': self._get_text(receptor, './/GiroRecep'),
                'direccion': self._get_text(receptor, './/DirRecep'),
                'comuna': self._get_text(receptor, './/CmnaRecep'),
                'ciudad': self._get_text(receptor, './/CiudadRecep'),
                'contacto': self._get_text(receptor, './/Contacto'),
                'email': self._get_text(receptor, './/CorreoRecep'),
            },

            # Totales
            'totales': {
                'monto_neto': float(self._get_text(totales, './/MntNeto', '0')),
                'monto_exento': float(self._get_text(totales, './/MntExe', '0')),
                'tasa_iva': float(self._get_text(totales, './/TasaIVA', '19')),
                'iva': float(self._get_text(totales, './/IVA', '0')),
                'monto_total': float(self._get_text(totales, './/MntTotal', '0')),
            }
        }

        return data

    def extract_detalles(self) -> List[Dict[str, Any]]:
        """
        Extrae los detalles (líneas) del documento

        Returns:
            Lista de diccionarios con los detalles
        """
        # Buscar documento sin namespace primero
        documento = self.root.find('.//Documento')
        if documento is None:
            documento = self.root.find('.//DTE/Documento')
        if documento is None:
            documento = self.root.find('.//Documento', self.NAMESPACES)
        if documento is None:
            documento = self.root.find('.//DTE/Documento', self.NAMESPACES)
        if documento is None:
            return []

        detalles = []

        # Buscar todos los elementos Detalle (sin namespace primero)
        detalle_elements = documento.findall('.//Detalle')
        if not detalle_elements:
            detalle_elements = documento.findall('.//Detalle', self.NAMESPACES)

        for idx, detalle in enumerate(detalle_elements, start=1):
            detalle_data = {
                'numero_linea': int(self._get_text(detalle, './/NroLinDet', str(idx))),
                'codigo_item': self._get_text(detalle, './/VlrCodigo') or self._get_text(detalle, './/CdgItem/VlrCodigo'),
                'tipo_codigo': self._get_text(detalle, './/TpoCodigo') or self._get_text(detalle, './/CdgItem/TpoCodigo'),
                'nombre_item': self._get_text(detalle, './/NmbItem'),
                'descripcion': self._get_text(detalle, './/DscItem'),
                'cantidad': float(self._get_text(detalle, './/QtyItem', '1')),
                'unidad_medida': self._get_text(detalle, './/UnmdItem'),
                'precio_unitario': float(self._get_text(detalle, './/PrcItem', '0')),
                'descuento_porcentaje': float(self._get_text(detalle, './/DescuentoPct', '0')),
                'descuento_monto': float(self._get_text(detalle, './/DescuentoMonto', '0')),
                'monto_item': float(self._get_text(detalle, './/MontoItem', '0')),
            }
            detalles.append(detalle_data)

        return detalles

    def extract_referencias(self) -> List[Dict[str, Any]]:
        """
        Extrae las referencias del documento (si existen)

        Returns:
            Lista de diccionarios con las referencias
        """
        # Buscar documento sin namespace primero
        documento = self.root.find('.//Documento')
        if documento is None:
            documento = self.root.find('.//DTE/Documento')
        if documento is None:
            documento = self.root.find('.//Documento', self.NAMESPACES)
        if documento is None:
            documento = self.root.find('.//DTE/Documento', self.NAMESPACES)
        if documento is None:
            return []

        referencias = []

        # Buscar todos los elementos Referencia (sin namespace primero)
        ref_elements = documento.findall('.//Referencia')
        if not ref_elements:
            ref_elements = documento.findall('.//Referencia', self.NAMESPACES)

        for idx, ref in enumerate(ref_elements, start=1):
            ref_data = {
                'numero_linea_ref': int(self._get_text(ref, './/NroLinRef', str(idx))),
                'tipo_documento_ref': self._get_text(ref, './/TpoDocRef'),
                'folio_ref': self._get_text(ref, './/FolioRef'),
                'fecha_ref': self._parse_date(self._get_text(ref, './/FchRef')),
                'codigo_ref': self._get_text(ref, './/CodRef'),  # 1, 2, 3
                'razon_ref': self._get_text(ref, './/RazonRef'),
            }
            referencias.append(ref_data)

        return referencias

    def extract_all(self) -> Dict[str, Any]:
        """
        Extrae toda la información del DTE

        Returns:
            Diccionario con toda la información
        """
        return {
            'encabezado': self.extract_encabezado(),
            'detalles': self.extract_detalles(),
            'referencias': self.extract_referencias(),
            'xml_original': self.xml_content
        }


def parse_dte_xml(xml_content: str) -> Dict[str, Any]:
    """
    Función helper para parsear un XML DTE

    Args:
        xml_content: Contenido del XML como string

    Returns:
        Diccionario con toda la información extraída
    """
    parser = DTEParser(xml_content)
    return parser.extract_all()
