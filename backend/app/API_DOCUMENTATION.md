# Documentación API - ERP DAEL

## Información General

La API de ERP DAEL es un sistema completo de gestión de inventario para equipos contra incendios, construido con FastAPI y diseñado para proporcionar funcionalidades avanzadas de análisis y control de inventario.

### Información Base
- **URL Base**: `http://localhost:8000`
- **Versión API**: `v1`
- **Prefijo de rutas**: `/api/v1`
- **Documentación interactiva**: `http://localhost:8000/docs`
- **Documentación alternativa**: `http://localhost:8000/redoc`

### Autenticación
Actualmente la API no requiere autenticación, pero incluye un sistema de usuarios y permisos preparado para implementación futura.

## Endpoints Principales

### 1. Salud del Sistema

#### GET `/health`
Verifica el estado de la API y la conexión a la base de datos.

**Respuesta:**
```json
{
  "status": "healthy",
  "database": "connected",
  "mysql_url": "mysql://localhost:3306",
  "message": "API funcionando correctamente"
}
```

#### GET `/`
Información general de la API y listado de endpoints disponibles.

**Respuesta:**
```json
{
  "message": "ERP DAEL API - Sistema de Inventario",
  "version": "1.0.0",
  "python": "3.13",
  "status": "running",
  "endpoints": {
    "docs": "/docs",
    "redoc": "/redoc",
    "health": "/health",
    // ... listado completo de endpoints
  }
}
```

## Módulos de la API

### 2. Gestión de Catálogos

#### Unidades de Medida (`/api/v1/unidades-medida`)
- `GET /` - Listar unidades de medida
- `GET /{id}` - Obtener unidad específica
- `POST /` - Crear nueva unidad
- `PUT /{id}` - Actualizar unidad
- `DELETE /{id}` - Eliminar unidad

#### Tipos de Movimiento (`/api/v1/tipos-movimiento`)
- `GET /` - Listar tipos de movimiento
- `GET /{id}` - Obtener tipo específico
- `POST /` - Crear nuevo tipo
- `PUT /{id}` - Actualizar tipo
- `DELETE /{id}` - Eliminar tipo

#### Categorías (`/api/v1/categorias`)
- `GET /` - Listar categorías
- `GET /{id}` - Obtener categoría específica
- `POST /` - Crear nueva categoría
- `PUT /{id}` - Actualizar categoría
- `DELETE /{id}` - Eliminar categoría

#### Subcategorías (`/api/v1/subcategorias`)
- `GET /` - Listar subcategorías
- `GET /{id}` - Obtener subcategoría específica
- `POST /` - Crear nueva subcategoría
- `PUT /{id}` - Actualizar subcategoría
- `DELETE /{id}` - Eliminar subcategoría

#### Tipos de Producto (`/api/v1/tipos-producto`)
- `GET /` - Listar tipos de producto
- `GET /{id}` - Obtener tipo específico
- `POST /` - Crear nuevo tipo
- `PUT /{id}` - Actualizar tipo
- `DELETE /{id}` - Eliminar tipo

#### Marcas (`/api/v1/marcas`)
- `GET /` - Listar marcas
- `GET /{id}` - Obtener marca específica
- `POST /` - Crear nueva marca
- `PUT /{id}` - Actualizar marca
- `DELETE /{id}` - Eliminar marca

#### Proveedores (`/api/v1/proveedores`)
- `GET /` - Listar proveedores
- `GET /{id}` - Obtener proveedor específico
- `POST /` - Crear nuevo proveedor
- `PUT /{id}` - Actualizar proveedor
- `DELETE /{id}` - Eliminar proveedor

### 3. Gestión de Ubicaciones

#### Bodegas (`/api/v1/bodegas`)
- `GET /` - Listar bodegas
- `GET /{id}` - Obtener bodega específica
- `POST /` - Crear nueva bodega
- `PUT /{id}` - Actualizar bodega
- `DELETE /{id}` - Eliminar bodega

#### Pasillos (`/api/v1/pasillos`)
- `GET /` - Listar pasillos
- `GET /{id}` - Obtener pasillo específico
- `GET /estadisticas` - Estadísticas de pasillos
- `POST /` - Crear nuevo pasillo
- `PUT /{id}` - Actualizar pasillo
- `DELETE /{id}` - Eliminar pasillo

#### Estantes (`/api/v1/estantes`)
- `GET /` - Listar estantes
- `GET /{id}` - Obtener estante específico
- `POST /` - Crear nuevo estante
- `PUT /{id}` - Actualizar estante
- `DELETE /{id}` - Eliminar estante

#### Niveles (`/api/v1/niveles`)
- `GET /` - Listar niveles
- `GET /{id}` - Obtener nivel específico
- `POST /` - Crear nuevo nivel
- `PUT /{id}` - Actualizar nivel
- `DELETE /{id}` - Eliminar nivel

### 4. Gestión de Productos

#### Productos (`/api/v1/productos`)
- `GET /` - Listar productos con filtros
- `GET /{id}` - Obtener producto específico
- `POST /` - Crear nuevo producto
- `PUT /{id}` - Actualizar producto
- `DELETE /{id}` - Eliminar producto

**Parámetros de filtro:**
- `activo`: Filtrar por estado activo
- `categoria_id`: Filtrar por categoría
- `marca_id`: Filtrar por marca
- `proveedor_id`: Filtrar por proveedor
- `skip`: Paginación (omitir registros)
- `limit`: Límite de registros

#### Producto-Proveedores (`/api/v1/producto-proveedores`)
- `GET /` - Listar relaciones producto-proveedor
- `GET /{id}` - Obtener relación específica
- `POST /` - Crear nueva relación
- `PUT /{id}` - Actualizar relación
- `DELETE /{id}` - Eliminar relación

#### Producto-Ubicaciones (`/api/v1/producto-ubicaciones`)
- `GET /` - Listar ubicaciones de productos
- `GET /{id}` - Obtener ubicación específica
- `POST /` - Crear nueva ubicación
- `PUT /{id}` - Actualizar ubicación
- `DELETE /{id}` - Eliminar ubicación

### 5. Gestión de Inventario

#### Movimientos de Inventario (`/api/v1/movimientos-inventario`)
- `GET /` - Listar movimientos
- `GET /{id}` - Obtener movimiento específico
- `POST /` - Crear nuevo movimiento
- `PUT /{id}` - Actualizar movimiento
- `DELETE /{id}` - Eliminar movimiento

#### Movimientos Detalle (`/api/v1/movimientos-detalle`)
- `GET /` - Listar detalles de movimientos
- `GET /{id}` - Obtener detalle específico
- `POST /` - Crear nuevo detalle
- `PUT /{id}` - Actualizar detalle
- `DELETE /{id}` - Eliminar detalle

#### Lotes (`/api/v1/lotes`)
- `GET /` - Listar lotes
- `GET /{id}` - Obtener lote específico
- `POST /` - Crear nuevo lote
- `PUT /{id}` - Actualizar lote
- `DELETE /{id}` - Eliminar lote

#### Números de Serie (`/api/v1/numeros-serie`)
- `GET /` - Listar números de serie
- `GET /{id}` - Obtener número específico
- `POST /` - Crear nuevo número
- `PUT /{id}` - Actualizar número
- `DELETE /{id}` - Eliminar número

### 6. Gestión de Obras

#### Clientes (`/api/v1/clientes`)
- `GET /` - Listar clientes
- `GET /{id}` - Obtener cliente específico
- `POST /` - Crear nuevo cliente
- `PUT /{id}` - Actualizar cliente
- `DELETE /{id}` - Eliminar cliente

#### Obras (`/api/v1/obras`)
- `GET /` - Listar obras
- `GET /{id}` - Obtener obra específica
- `POST /` - Crear nueva obra
- `PUT /{id}` - Actualizar obra
- `DELETE /{id}` - Eliminar obra

#### Almacén de Obra (`/api/v1/almacen-obra`)
- `GET /` - Listar almacenes de obra
- `GET /{id}` - Obtener almacén específico
- `POST /` - Crear nuevo almacén
- `PUT /{id}` - Actualizar almacén
- `DELETE /{id}` - Eliminar almacén

#### Despachos de Obra (`/api/v1/despachos-obra`)
- `GET /` - Listar despachos
- `GET /{id}` - Obtener despacho específico
- `POST /` - Crear nuevo despacho
- `PUT /{id}` - Actualizar despacho
- `DELETE /{id}` - Eliminar despacho

#### Devoluciones de Obra (`/api/v1/devoluciones-obra`)
- `GET /` - Listar devoluciones
- `GET /{id}` - Obtener devolución específica
- `POST /` - Crear nueva devolución
- `PUT /{id}` - Actualizar devolución
- `DELETE /{id}` - Eliminar devolución

### 7. Sistema de Usuarios y Permisos

#### Roles (`/api/v1/roles`)
- `GET /` - Listar roles
- `GET /{id}` - Obtener rol específico
- `GET /estadisticas` - Estadísticas de roles
- `POST /` - Crear nuevo rol
- `PUT /{id}` - Actualizar rol
- `DELETE /{id}` - Eliminar rol

#### Usuarios (`/api/v1/usuarios`)
- `GET /` - Listar usuarios
- `GET /{id}` - Obtener usuario específico
- `POST /` - Crear nuevo usuario
- `PUT /{id}` - Actualizar usuario
- `DELETE /{id}` - Eliminar usuario

#### Permisos (`/api/v1/permisos`)
- `GET /` - Listar permisos
- `GET /{id}` - Obtener permiso específico
- `GET /estadisticas` - Estadísticas de permisos
- `POST /` - Crear nuevo permiso
- `PUT /{id}` - Actualizar permiso
- `DELETE /{id}` - Eliminar permiso

### 8. Configuración del Sistema

#### Configuración Sistema (`/api/v1/configuracion-sistema`)
- `GET /` - Listar configuraciones
- `GET /{clave}` - Obtener configuración específica
- `GET /categoria/{categoria}` - Obtener por categoría
- `POST /` - Crear nueva configuración
- `PUT /{clave}` - Actualizar configuración
- `DELETE /{clave}` - Eliminar configuración

**Categorías de configuración:**
- `GENERAL`: Configuraciones generales
- `INVENTARIO`: Configuraciones de inventario
- `REPORTES`: Configuraciones de reportes
- `NOTIFICACIONES`: Configuraciones de notificaciones
- `SEGURIDAD`: Configuraciones de seguridad

### 9. Vistas Analíticas Avanzadas

#### Inventario Consolidado (`/api/v1/inventario-consolidado`)

**Endpoints principales:**
- `GET /` - Listado con filtros avanzados
- `GET /{id}` - Producto específico
- `GET /criticos/listar` - Productos críticos
- `GET /bajo-stock/listar` - Productos con bajo stock
- `GET /alto-valor/listar` - Productos de alto valor
- `GET /sin-movimiento/listar` - Productos sin movimiento

**Estadísticas y análisis:**
- `GET /estadisticas/generales` - Estadísticas generales
- `GET /estadisticas/por-categoria` - Por categoría
- `GET /estadisticas/por-bodega` - Por bodega
- `GET /estadisticas/por-proveedor` - Por proveedor
- `GET /estadisticas/financieras` - Financieras

**Alertas y recomendaciones:**
- `GET /alertas/listar` - Alertas del sistema
- `GET /alertas/resumen` - Resumen de alertas
- `GET /recomendaciones/reposicion` - Recomendaciones de reposición
- `GET /recomendaciones/optimizacion` - Optimización de inventario

**Dashboard y reportes:**
- `GET /dashboard/kpis` - KPIs principales
- `GET /reportes/ejecutivo` - Reporte ejecutivo
- `GET /exportar/excel` - Exportación a Excel

#### Obras Inventario (`/api/v1/obras-inventario`)

**Endpoints principales:**
- `GET /` - Listado con filtros por obra
- `GET /{id}` - Obra específica
- `GET /activas/listar` - Obras activas
- `GET /retrasadas/listar` - Obras retrasadas
- `GET /urgentes/listar` - Obras urgentes
- `GET /alto-valor/listar` - Obras de alto valor

**Estadísticas especializadas:**
- `GET /estadisticas/generales` - Estadísticas generales
- `GET /estadisticas/por-estado` - Por estado de obra
- `GET /estadisticas/por-tipo` - Por tipo de obra
- `GET /estadisticas/por-cliente` - Por cliente
- `GET /estadisticas/financieras` - Financieras

**Análisis y seguimiento:**
- `GET /alertas/listar` - Alertas de obras
- `GET /ranking/eficiencia` - Ranking por eficiencia
- `GET /ranking/rentabilidad` - Ranking por rentabilidad
- `GET /analisis/tendencias` - Análisis de tendencias

#### Devoluciones Pendientes (`/api/v1/devoluciones-pendientes`)

**Endpoints principales:**
- `GET /` - Listado con filtros avanzados
- `GET /{id}` - Devolución específica
- `GET /vencidas/listar` - Devoluciones vencidas
- `GET /urgentes/listar` - Devoluciones urgentes
- `GET /alto-valor/listar` - Devoluciones de alto valor
- `GET /atencion-inmediata/listar` - Requieren atención inmediata

**Análisis y seguimiento:**
- `GET /estadisticas/generales` - Estadísticas generales
- `GET /estadisticas/por-estado` - Por estado
- `GET /ranking/por-valor` - Ranking por valor
- `GET /alertas/listar` - Alertas activas
- `GET /recomendaciones/listar` - Recomendaciones

**Métricas avanzadas:**
- `GET /metricas/tiempo-respuesta` - Métricas de tiempo
- `GET /analisis/tendencias` - Análisis de tendencias
- `GET /reportes/ejecutivo` - Reporte ejecutivo

#### Productos ABC (`/api/v1/productos-abc`)

**Clasificación ABC:**
- `GET /` - Listado con análisis ABC
- `GET /{id}` - Producto específico
- `GET /clase-a/listar` - Productos clase A
- `GET /clase-b/listar` - Productos clase B
- `GET /clase-c/listar` - Productos clase C
- `GET /sin-movimiento/listar` - Sin movimiento

**Análisis especializado:**
- `GET /requieren-atencion/listar` - Requieren atención
- `GET /obsolescencia-alta/listar` - Alta obsolescencia
- `GET /analisis/obsolescencia` - Análisis de obsolescencia
- `GET /analisis/pareto` - Análisis de Pareto (80/20)

**Optimización:**
- `GET /optimizacion/inventario` - Optimización de inventario
- `GET /simulacion/punto-reorden` - Simulación de puntos de reorden
- `GET /metricas/rotacion` - Métricas de rotación

**Reportes ABC:**
- `GET /estadisticas/generales` - Estadísticas ABC
- `GET /ranking/por-valor` - Ranking por valor
- `GET /dashboard/kpis` - KPIs ABC
- `GET /reportes/ejecutivo` - Reporte ejecutivo ABC

## Formatos de Respuesta

### Respuestas de Éxito

#### Listado de Recursos
```json
{
  "data": [...],
  "total": 150,
  "skip": 0,
  "limit": 100
}
```

#### Recurso Individual
```json
{
  "id": 1,
  "campo1": "valor1",
  "campo2": "valor2",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### Estadísticas
```json
{
  "total_items": 1500,
  "categories": {
    "category1": 500,
    "category2": 300
  },
  "percentages": {
    "category1": 33.33,
    "category2": 20.00
  }
}
```

### Respuestas de Error

#### Error 400 - Bad Request
```json
{
  "detail": "Datos de entrada inválidos",
  "error_code": "VALIDATION_ERROR",
  "fields": {
    "campo1": ["Campo requerido"],
    "campo2": ["Valor debe ser positivo"]
  }
}
```

#### Error 404 - Not Found
```json
{
  "detail": "Recurso no encontrado",
  "error_code": "NOT_FOUND"
}
```

#### Error 500 - Internal Server Error
```json
{
  "detail": "Error interno del servidor",
  "error_code": "INTERNAL_ERROR"
}
```

## Filtros Comunes

### Paginación
- `skip`: Número de registros a omitir (default: 0)
- `limit`: Límite de registros (default: 100, max: 1000)

### Filtros por Fecha
- `fecha_desde`: Fecha inicio (formato: YYYY-MM-DD)
- `fecha_hasta`: Fecha fin (formato: YYYY-MM-DD)

### Filtros por Estado
- `activo`: true/false
- `estado`: Depende del recurso

### Búsqueda
- `q`: Término de búsqueda en campos relevantes

## Códigos de Estado HTTP

- `200 OK` - Operación exitosa
- `201 Created` - Recurso creado exitosamente
- `400 Bad Request` - Datos de entrada inválidos
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - No autorizado
- `404 Not Found` - Recurso no encontrado
- `422 Unprocessable Entity` - Error de validación
- `500 Internal Server Error` - Error del servidor

## Ejemplos de Uso

### Obtener Productos con Filtros
```bash
GET /api/v1/productos?activo=true&categoria_id=1&skip=0&limit=50
```

### Crear Nuevo Producto
```bash
POST /api/v1/productos
Content-Type: application/json

{
  "sku": "PROD001",
  "nombre": "Extintor CO2 5kg",
  "descripcion": "Extintor de CO2 de 5 kilogramos",
  "categoria_id": 1,
  "marca_id": 1,
  "activo": true
}
```

### Obtener Estadísticas de Inventario
```bash
GET /api/v1/inventario-consolidado/estadisticas/generales
```

### Buscar Productos ABC
```bash
GET /api/v1/productos-abc/buscar/texto?q=extintor&skip=0&limit=20
```

## Consideraciones Técnicas

### Rendimiento
- Implementa paginación en todos los listados
- Usa índices en campos de búsqueda frecuente
- Limita el número máximo de registros por consulta

### Seguridad
- Validación de entrada en todos los endpoints
- Sanitización de datos de búsqueda
- Logs de auditoría en operaciones críticas

### Versionado
- La API está versionada en la URL (`/api/v1`)
- Cambios breaking se manejan con nuevas versiones
- Deprecación gradual de versiones antiguas

### Monitoreo
- Endpoint `/health` para verificación de estado
- Métricas de rendimiento disponibles
- Logs estructurados para debugging

## Contacto y Soporte

Para soporte técnico o preguntas sobre la API:
- Documentación interactiva: `/docs`
- Documentación alternativa: `/redoc`
- Verificación de estado: `/health`

La API está diseñada para ser autoexplicativa y proporciona documentación completa en tiempo real a través de los endpoints de documentación integrados.