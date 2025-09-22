# Sistema de Workflow de Órdenes de Compra - ERP DAEL

## Resumen

Se ha implementado un sistema completo de workflow de 5 pasos para el manejo de órdenes de compra, que incluye desde la creación de la orden hasta el pago final, con soporte para documentos XML DTE de Chile, conciliación automática y dashboard de monitoreo.

## Arquitectura del Sistema

### Flujo de 5 Pasos

1. **Paso 1: Orden de Compra** - Creación y aprobación de órdenes de compra
2. **Paso 2: Recepción de Mercancía** - Recepción física de productos
3. **Paso 3: Recepción de Factura** - Procesamiento de documentos fiscales
4. **Paso 4: Conciliación** - Conciliación entre OC y factura
5. **Paso 5: Pago** - Procesamiento y confirmación de pagos

### Estados de la Orden

```
BORRADOR → PENDIENTE → APROBADA → ENVIADA → RECIBIDA → FACTURADA → CONCILIADA → PAGADA → CERRADA
```

## Nuevas Tablas Implementadas

### 1. documentos_orden_compra
- Gestiona todos los documentos asociados a una OC (facturas, remisiones, XMLs DTE, PDFs)
- Soporte para procesamiento automático de XMLs DTE chilenos
- Validación contra SII (Servicio de Impuestos Internos)
- Almacenamiento de rutas de archivos

### 2. conciliacion_oc_facturas
- Proceso de conciliación entre orden de compra y factura
- Soporte para conciliación automática y manual
- Cálculo de diferencias y porcentajes de coincidencia

### 3. conciliacion_detalle
- Detalle producto por producto de la conciliación
- Comparación de cantidades, precios e importes
- Estados por producto (COINCIDE, DIFERENCIA_CANTIDAD, etc.)

### 4. ajustes_conciliacion
- Ajustes necesarios basados en discrepancias encontradas
- Generación automática de movimientos de inventario
- Trazabilidad de autorizaciones

### 5. historial_estados_oc
- Trazabilidad completa de cambios de estado
- Auditoría de quién y cuándo realizó cambios

### 6. pagos_ordenes_compra
- Gestión completa de pagos
- Múltiples métodos de pago
- Control de retenciones e impuestos
- Estados: PENDIENTE → PROCESADO → CONFIRMADO

## APIs Implementadas

### Documentos de Orden de Compra (`/api/v1/documentos-orden-compra`)

#### Endpoints principales:
- `POST /` - Crear documento
- `GET /{documento_id}` - Obtener documento
- `PUT /{documento_id}` - Actualizar documento
- `POST /upload/{id_orden_compra}` - Subir archivo (XML/PDF)
- `POST /procesar-xml/{documento_id}` - Procesar XML
- `GET /orden/{id_orden_compra}` - Documentos por orden
- `GET /por-uuid/{uuid_fiscal}` - Buscar por UUID

#### Ejemplo de uso:
```bash
# Subir XML de factura
curl -X POST "/api/v1/documentos-orden-compra/upload/123" \
  -F "file=@factura.xml" \
  -F "tipo_documento=FACTURA"

# Procesar XML automáticamente
curl -X POST "/api/v1/documentos-orden-compra/procesar-xml/456" \
  -d '{"validar_sat": true, "auto_conciliar": true}'
```

### Conciliación OC-Facturas (`/api/v1/conciliacion-oc-facturas`)

#### Endpoints principales:
- `POST /conciliar-automatica/{id_orden_compra}` - Conciliación automática
- `GET /{conciliacion_id}/detalles` - Ver detalles de conciliación
- `POST /{conciliacion_id}/aprobar` - Aprobar conciliación
- `POST /{conciliacion_id}/rechazar` - Rechazar conciliación
- `GET /pendientes` - Conciliaciones pendientes
- `GET /resumen/{id_orden_compra}` - Resumen de conciliación

#### Ejemplo de conciliación automática:
```bash
curl -X POST "/api/v1/conciliacion-oc-facturas/conciliar-automatica/123" \
  -d '{
    "id_documento_factura": 456,
    "id_usuario_concilia": 1,
    "tolerancia_precio": 5.0,
    "tolerancia_cantidad": 2.0
  }'
```

### Pagos de Órdenes de Compra (`/api/v1/pagos-ordenes-compra`)

#### Endpoints principales:
- `POST /` - Crear pago
- `POST /{pago_id}/procesar` - Procesar pago
- `POST /{pago_id}/confirmar` - Confirmar pago
- `POST /generar-desde-conciliacion/{id_conciliacion}` - Generar pago automático
- `GET /resumen-pagos/{id_orden_compra}` - Resumen de pagos por orden
- `POST /validar-pago` - Validar datos antes de crear pago

#### Ejemplo de flujo de pago:
```bash
# 1. Crear pago
curl -X POST "/api/v1/pagos-ordenes-compra/" \
  -d '{
    "id_orden_compra": 123,
    "numero_pago": "PAG-2024-000123",
    "fecha_pago": "2024-01-15",
    "monto_pago": 10000.00,
    "metodo_pago": "TRANSFERENCIA",
    "autorizado_por": 1,
    "fecha_autorizacion": "2024-01-15T10:00:00"
  }'

# 2. Procesar pago
curl -X POST "/api/v1/pagos-ordenes-compra/1/procesar" \
  -d '{"id_usuario_procesa": 1}'

# 3. Confirmar pago
curl -X POST "/api/v1/pagos-ordenes-compra/1/confirmar" \
  -d '{
    "id_usuario_confirma": 1,
    "referencia_confirmacion": "REF123456"
  }'
```

### Dashboard de Workflow (`/api/v1/workflow-dashboard`)

#### Endpoints de monitoreo:
- `GET /resumen-general` - Resumen general del workflow
- `GET /ordenes-workflow` - Lista de órdenes con estado del workflow
- `GET /pendientes-por-paso` - Órdenes pendientes por cada paso
- `GET /metricas-tiempo-promedio` - Métricas de tiempo por paso
- `GET /eficiencia-workflow` - KPIs de eficiencia
- `GET /alertas-workflow` - Alertas que requieren atención
- `GET /reporte-ejecutivo` - Reporte ejecutivo completo

#### Ejemplo de respuesta del dashboard:
```json
{
  "resumen_general": {
    "total_ordenes": 150,
    "ordenes_completadas": 45,
    "porcentaje_completado": 30.0
  },
  "progreso_workflow": {
    "paso_1_orden_compra": 25,
    "paso_2_recepcion": 35,
    "paso_3_facturacion": 20,
    "paso_4_conciliacion": 15,
    "paso_5_pago": 10,
    "completadas": 45
  },
  "pendientes_atencion": {
    "documentos_por_procesar": 8,
    "conciliaciones_pendientes": 5,
    "pagos_por_confirmar": 3
  }
}
```

### Procesamiento de XML DTE (`/api/v1/xml-processor`)

#### Endpoints especializados:
- `POST /procesar-xml-factura/{documento_id}` - Procesar XML DTE individual
- `POST /procesar-lote-xml` - Procesar lote de XMLs DTE pendientes
- `GET /validar-folio/{folio_dte}` - Validar folio DTE contra SII
- `POST /extraer-datos-xml` - Extraer datos de XML DTE como texto
- `GET /estadisticas-procesamiento` - Estadísticas de procesamiento

## Configuraciones del Sistema

### Parámetros añadidos a configuracion_sistema:

```sql
-- Rutas de almacenamiento
'RUTA_ALMACEN_XML' = '/var/erp/documentos/xml/'
'RUTA_ALMACEN_PDF' = '/var/erp/documentos/pdf/'

-- Validaciones
'VALIDAR_XML_SII' = 'TRUE'
'AUTO_CONCILIAR_OC' = 'TRUE'

-- Tolerancias para conciliación automática
'TOLERANCIA_PRECIO_CONCILIACION' = '5.00'
'TOLERANCIA_CANTIDAD_CONCILIACION' = '2.00'

-- Workflow
'REQUIERE_APROBACION_AJUSTES' = 'TRUE'
'DIAS_LIMITE_CONCILIACION' = '30'
'GENERAR_MOVIMIENTO_AUTO_RECEPCION' = 'TRUE'
```

## Nuevos Estados de Órdenes de Compra

```sql
INSERT INTO estados_orden_compra VALUES
('RECIBIDA', 'Mercancía Recibida', 'Mercancía recibida físicamente'),
('FACTURADA', 'Facturada', 'Factura recibida y procesada'),
('CONCILIADA', 'Conciliada', 'Orden conciliada con factura'),
('PAGADA', 'Pagada', 'Orden pagada al proveedor'),
('CERRADA', 'Cerrada', 'Orden cerrada y archivada');
```

## Automatización Implementada

### 1. Triggers de Estado
- Cambio automático de estado después de recepción completa
- Cambio automático después de procesar factura
- Cambio automático después de conciliación aprobada
- Cambio automático después de pago confirmado

### 2. Conciliación Automática
- Comparación automática de productos entre OC y factura
- Cálculo de diferencias con tolerancias configurables
- Generación automática de ajustes necesarios

### 3. Procesamiento de XML DTE
- Extracción automática de datos fiscales chilenos
- Validación de estructura XML DTE
- Integración con servicios del SII (framework preparado)

## Alertas del Sistema

### Tipos de alertas implementadas:
- **ORDENES_VENCIDAS**: Órdenes sin recepción después de fecha requerida
- **DOCUMENTOS_ERROR**: XMLs con errores de procesamiento
- **CONCILIACIONES_PROBLEMA**: Conciliaciones con diferencias significativas
- **PAGOS_PENDIENTES**: Pagos pendientes de confirmación

## Reportes y Métricas

### KPIs disponibles:
- Tiempo promedio por paso del workflow
- Tasa de completado de órdenes
- Tasa de problemas en conciliación
- Eficiencia de procesamiento de documentos
- Top proveedores por volumen

## Instalación y Configuración

### 1. Ejecutar Script de Base de Datos
```bash
mysql -u usuario -p erp-dael < database/purchase_order_workflow.sql
```

### 2. Crear Directorios de Almacenamiento
```bash
sudo mkdir -p /var/erp/documentos/{xml,pdf,imagenes}
sudo chown -R www-data:www-data /var/erp/documentos
sudo chmod -R 755 /var/erp/documentos
```

### 3. Configurar Variables de Entorno
```bash
# Añadir al .env
XML_STORAGE_PATH=/var/erp/documentos/xml/
PDF_STORAGE_PATH=/var/erp/documentos/pdf/
SAT_VALIDATION_ENABLED=true
AUTO_CONCILIATION_ENABLED=true
```

### 4. Verificar APIs
```bash
# Verificar que todas las nuevas rutas están disponibles
curl http://localhost:8000/api/v1/workflow-dashboard/resumen-general
```

## Casos de Uso Principales

### Caso 1: Flujo Completo Manual
1. Crear orden de compra → Estado: BORRADOR
2. Aprobar orden → Estado: APROBADA
3. Enviar a proveedor → Estado: ENVIADA
4. Recibir mercancía → Estado: RECIBIDA
5. Subir XML de factura → Procesar XML
6. Conciliar OC vs Factura → Estado: CONCILIADA
7. Crear y confirmar pago → Estado: PAGADA

### Caso 2: Flujo Automático con XML
1. Crear y aprobar orden de compra
2. Recibir mercancía (automático → RECIBIDA)
3. Subir XML (automático → extrae datos → FACTURADA)
4. Conciliación automática (automático → CONCILIADA si coincide)
5. Generar pago desde conciliación (automático → crear pago)
6. Confirmar pago → PAGADA

### Caso 3: Manejo de Excepciones
1. XML con errores → Estado: ERROR → Alertas
2. Conciliación con diferencias → Estado: CON_DIFERENCIAS → Revisión manual
3. Ajustes necesarios → Crear ajustes → Aprobar → Procesar

## Integraciones Futuras

El sistema está preparado para:
- **Validación SII**: Framework listo para integrar con servicios oficiales del SII de Chile
- **Pagos bancarios**: Estructura preparada para APIs bancarias
- **Documentos electrónicos**: Sistema extensible para más tipos de DTE
- **Workflow personalizable**: Estados y pasos configurables por empresa

## Monitoreo y Mantenimiento

### Endpoints de monitoreo:
- `/api/v1/workflow-dashboard/alertas-workflow` - Alertas activas
- `/api/v1/xml-processor/estadisticas-procesamiento` - Estado de procesamiento XML
- `/api/v1/workflow-dashboard/eficiencia-workflow` - Métricas de rendimiento

### Tareas de mantenimiento recomendadas:
- Revisar alertas diariamente
- Procesar XMLs pendientes en lotes
- Monitorear conciliaciones con diferencias
- Verificar pagos pendientes de confirmación
- Generar reportes ejecutivos semanales

## Soporte y Documentación

- **API Documentation**: `/docs` (Swagger UI)
- **API Schema**: `/redoc` (ReDoc)
- **Health Check**: `/health`
- **Status**: `/api/v1/workflow-dashboard/resumen-general`