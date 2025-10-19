"""
Generador de PDFs para Órdenes de Compra
"""
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
from decimal import Decimal


def formatear_numero_chileno(numero, decimales=2):
    """
    Formatea un número con el formato chileno:
    - Separador de miles: punto (.)
    - Separador de decimales: coma (,)

    Args:
        numero: Número a formatear
        decimales: Cantidad de decimales (default: 2)

    Returns:
        String con el número formateado
    """
    # Convertir a float
    valor = float(numero)

    # Formatear con separador de miles y decimales
    # Primero formateamos con el formato estándar (coma para miles, punto para decimales)
    formato_estandar = f"{valor:,.{decimales}f}"

    # Luego intercambiamos: punto por coma y coma por punto
    formato_chileno = formato_estandar.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')

    return formato_chileno


def generar_pdf_orden_compra(orden, detalles):
    """
    Genera un PDF de la orden de compra

    Args:
        orden: Objeto OrdenCompra con todos sus datos
        detalles: Lista de OrdenCompraDetalle

    Returns:
        BytesIO con el contenido del PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.5*inch, bottomMargin=0.5*inch)

    # Container para los elementos del PDF
    story = []
    styles = getSampleStyleSheet()

    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1976D2'),
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1976D2'),
        spaceAfter=12,
        spaceBefore=12
    )

    normal_style = styles['Normal']

    # ========================================
    # ENCABEZADO - Datos de la Empresa Emisora
    # ========================================
    if orden.empresa:
        empresa_data = [
            [Paragraph(f"<b>{orden.empresa.razon_social}</b>", styles['Heading1'])],
            [Paragraph(f"RUT: {orden.empresa.rut_empresa}", normal_style)],
        ]

        if orden.empresa.giro:
            empresa_data.append([Paragraph(f"Giro: {orden.empresa.giro}", normal_style)])
        if orden.empresa.direccion:
            empresa_data.append([Paragraph(f"Dirección: {orden.empresa.direccion}", normal_style)])
        if orden.empresa.comuna:
            direccion_completa = f"{orden.empresa.comuna}"
            if orden.empresa.ciudad:
                direccion_completa += f", {orden.empresa.ciudad}"
            if orden.empresa.region:
                direccion_completa += f", {orden.empresa.region}"
            empresa_data.append([Paragraph(direccion_completa, normal_style)])
        if orden.empresa.telefono:
            empresa_data.append([Paragraph(f"Teléfono: {orden.empresa.telefono}", normal_style)])
        if orden.empresa.email:
            empresa_data.append([Paragraph(f"Email: {orden.empresa.email}", normal_style)])

        empresa_table = Table(empresa_data, colWidths=[7*inch])
        empresa_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(empresa_table)
        story.append(Spacer(1, 20))

    # ========================================
    # TÍTULO Y NÚMERO DE ORDEN
    # ========================================
    story.append(Paragraph("ORDEN DE COMPRA", title_style))

    # Información básica de la orden
    orden_info_data = [
        ['Número de Orden:', orden.numero_orden],
        ['Fecha de Orden:', orden.fecha_orden.strftime('%d/%m/%Y')],
        ['Fecha Requerida:', orden.fecha_requerida.strftime('%d/%m/%Y')],
    ]

    if orden.estado:
        orden_info_data.append(['Estado:', orden.estado.nombre_estado])

    orden_info_table = Table(orden_info_data, colWidths=[2*inch, 3*inch])
    orden_info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1976D2')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(orden_info_table)
    story.append(Spacer(1, 20))

    # ========================================
    # DATOS DEL PROVEEDOR
    # ========================================
    story.append(Paragraph("PROVEEDOR", heading_style))

    proveedor_data = [
        ['Razón Social:', orden.proveedor.razon_social if orden.proveedor else ''],
        ['RUT:', orden.proveedor.rfc if orden.proveedor else ''],
    ]

    proveedor_table = Table(proveedor_data, colWidths=[2*inch, 5*inch])
    proveedor_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1976D2')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(proveedor_table)
    story.append(Spacer(1, 20))

    # ========================================
    # DATOS DE ENTREGA Y CENTRO DE COSTO
    # ========================================
    if orden.direccion_entrega or orden.centro_costo:
        story.append(Paragraph("INFORMACIÓN ADICIONAL", heading_style))

        info_adicional = []

        if orden.centro_costo:
            info_adicional.append(['Centro de Costo:', f"{orden.centro_costo.codigo_centro_costo} - {orden.centro_costo.nombre_centro_costo}"])

        if orden.direccion_entrega:
            info_adicional.append(['Dirección de Entrega:', orden.direccion_entrega])

        if orden.contacto_entrega:
            info_adicional.append(['Contacto Entrega:', orden.contacto_entrega])

        if orden.telefono_contacto:
            info_adicional.append(['Teléfono Contacto:', orden.telefono_contacto])

        if orden.terminos_pago:
            info_adicional.append(['Términos de Pago:', orden.terminos_pago])

        if info_adicional:
            info_table = Table(info_adicional, colWidths=[2*inch, 5*inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1976D2')),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            story.append(info_table)
            story.append(Spacer(1, 20))

    # ========================================
    # DETALLE DE PRODUCTOS
    # ========================================
    story.append(Paragraph("DETALLE DE LA ORDEN", heading_style))

    # Encabezados de la tabla de detalles
    detalle_data = [
        ['#', 'Código', 'Producto', 'Cantidad', 'Precio Unit.', 'Desc.', 'Total']
    ]

    # Agregar cada detalle
    for detalle in detalles:
        producto_nombre = detalle.producto.nombre_producto if detalle.producto else 'N/A'
        producto_sku = detalle.producto.sku if detalle.producto else 'N/A'

        detalle_data.append([
            str(detalle.numero_linea),
            producto_sku,
            producto_nombre,
            formatear_numero_chileno(detalle.cantidad_solicitada, 2),
            f"${formatear_numero_chileno(detalle.precio_unitario, 2)}",
            f"{formatear_numero_chileno(detalle.descuento_porcentaje, 1)}%",
            f"${formatear_numero_chileno(detalle.importe_total, 2)}"
        ])

    detalle_table = Table(detalle_data, colWidths=[0.4*inch, 1*inch, 2.5*inch, 0.8*inch, 1*inch, 0.7*inch, 1*inch])
    detalle_table.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

        # Contenido
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # Número de línea
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Código
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),    # Producto
        ('ALIGN', (3, 1), (3, -1), 'RIGHT'),   # Cantidad
        ('ALIGN', (4, 1), (4, -1), 'RIGHT'),   # Precio
        ('ALIGN', (5, 1), (5, -1), 'RIGHT'),   # Descuento
        ('ALIGN', (6, 1), (6, -1), 'RIGHT'),   # Total

        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(detalle_table)
    story.append(Spacer(1, 20))

    # ========================================
    # TOTALES
    # ========================================
    totales_data = [
        ['Subtotal:', f"${formatear_numero_chileno(orden.subtotal, 2)}"],
        ['Descuentos:', f"-${formatear_numero_chileno(orden.descuentos, 2)}"],
        [f'IVA ({formatear_numero_chileno(orden.iva_porcentaje, 1)}%):', f"${formatear_numero_chileno(orden.impuestos, 2)}"],
        ['TOTAL:', f"${formatear_numero_chileno(orden.total, 2)}"]
    ]

    totales_table = Table(totales_data, colWidths=[1.5*inch, 1.5*inch])
    totales_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#1976D2')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#1976D2')),
    ]))

    # Alinear totales a la derecha
    totales_wrapper = Table([[totales_table]], colWidths=[7*inch])
    totales_wrapper.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
    ]))
    story.append(totales_wrapper)
    story.append(Spacer(1, 20))

    # ========================================
    # OBSERVACIONES
    # ========================================
    if orden.observaciones:
        story.append(Paragraph("OBSERVACIONES", heading_style))
        story.append(Paragraph(orden.observaciones, normal_style))
        story.append(Spacer(1, 20))

    # ========================================
    # PIE DE PÁGINA
    # ========================================
    story.append(Spacer(1, 30))

    firmas_data = [
        ['_' * 30, '_' * 30],
        ['Firma Autorizada', 'Recepción Proveedor'],
        ['Nombre:', 'Nombre:'],
        ['Fecha:', 'Fecha:']
    ]

    firmas_table = Table(firmas_data, colWidths=[3.5*inch, 3.5*inch])
    firmas_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 20),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 10),
    ]))
    story.append(firmas_table)

    # ========================================
    # Información de generación
    # ========================================
    story.append(Spacer(1, 20))
    footer_text = f"Documento generado electrónicamente el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}"
    story.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)))

    # Construir el PDF
    doc.build(story)

    # Obtener el contenido del buffer
    pdf_content = buffer.getvalue()
    buffer.close()

    return pdf_content
