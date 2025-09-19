from datetime import datetime, date, time
from pydantic import BaseModel, Field, EmailStr
from typing import Dict, List, Optional
from enum import Enum
from decimal import Decimal

# Schema base
class UnidadMedidaBase(BaseModel):
    codigo_unidad: str
    nombre_unidad: str
    descripcion: Optional[str] = None
    activo: bool = True

# Schema para crear (POST)
class UnidadMedidaCreate(UnidadMedidaBase):
    pass

# Schema para actualizar (PUT)
class UnidadMedidaUpdate(BaseModel):
    codigo_unidad: Optional[str] = None
    nombre_unidad: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

# Schema para respuesta (GET)
class UnidadMedidaResponse(UnidadMedidaBase):
    id_unidad: int
    
    class Config:
        from_attributes = True  # Para SQLAlchemy models


class AfectaStock(str, Enum):
    AUMENTA = "aumenta"
    DISMINUYE = "disminuye"
    NO_AFECTA = "no_afecta"

# Schema base
class TipoMovimientoBase(BaseModel):
    codigo_tipo: str
    nombre_tipo: str
    afecta_stock: AfectaStock
    requiere_autorizacion: Optional[bool] = None
    activo: bool = True

# Schema para crear (POST)
class TipoMovimientoCreate(TipoMovimientoBase):
    pass

# Schema para actualizar (PUT)
class TipoMovimientoUpdate(BaseModel):
    codigo_tipo: Optional[str] = None
    nombre_tipo: Optional[str] = None
    afecta_stock: AfectaStock
    requiere_autorizacion: Optional[bool] = None
    activo: Optional[bool] = None

# Schema para respuesta (GET)
class TipoMovimientoResponse(TipoMovimientoBase):
    id_tipo_movimiento: int
    
    class Config:
        from_attributes = True  # Para SQLAlchemy models


class CategoriaBase(BaseModel):
    codigo_categoria: str
    nombre_categoria: str
    descripcion: Optional[str] = None
    activo: Optional[bool] = True

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(CategoriaBase):
    codigo_categoria: str
    nombre_categoria: str
    descripcion: Optional[str] = None
    activo: Optional[bool] = True

class SubcategoriaBase(BaseModel):
    id_categoria: int
    codigo_subcategoria: str = Field(..., min_length=1, max_length=10)
    nombre_subcategoria: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    activo: bool = True

class SubcategoriaCreate(SubcategoriaBase):
    pass

class SubcategoriaUpdate(SubcategoriaBase):
    id_categoria: Optional[int] = None

class SubcategoriaResponse(SubcategoriaBase):
    id_subcategoria: int

    class Config:
        from_attributes = True
        
class CategoriaResponse(CategoriaBase):
    id_categoria: int
    subcategorias: List[SubcategoriaResponse] = []

    class Config:
        from_attributes = True

class SubcategoriaWithCategoria(SubcategoriaResponse):
    categoria: Optional['CategoriaResponse'] = None  # Importa CategoriaResponse desde schemas.py si existe

class TipoProductoBase(BaseModel):
    id_subcategoria: int
    codigo_tipo: str = Field(..., min_length=1, max_length=10)
    nombre_tipo: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    activo: bool = True

class TipoProductoCreate(TipoProductoBase):
    pass

class TipoProductoUpdate(BaseModel):
    id_subcategoria: Optional[int] = None
    codigo_tipo: Optional[str] = Field(None, min_length=1, max_length=10)
    nombre_tipo: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

class TipoProductoResponse(TipoProductoBase):
    id_tipo_producto: int

    class Config:
        from_attributes = True

class TipoProductoWithSubcategoria(TipoProductoResponse):
    subcategoria: Optional[SubcategoriaWithCategoria] = None

class MarcaBase(BaseModel):
    nombre_marca: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    pais_origen: Optional[str] = Field(None, max_length=50)
    sitio_web: Optional[str] = Field(None, max_length=200)
    contacto_tecnico: Optional[str] = Field(None, max_length=200)
    activo: bool = True

class MarcaCreate(MarcaBase):
    pass

class MarcaUpdate(BaseModel):
    nombre_marca: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    pais_origen: Optional[str] = Field(None, max_length=50)
    sitio_web: Optional[str] = Field(None, max_length=200)
    contacto_tecnico: Optional[str] = Field(None, max_length=200)
    activo: Optional[bool] = None

class MarcaResponse(MarcaBase):
    id_marca: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class ProveedorBase(BaseModel):
    codigo_proveedor: str = Field(..., min_length=1, max_length=20)
    nombre_proveedor: str = Field(..., min_length=1, max_length=200)
    razon_social: Optional[str] = Field(None, max_length=200)
    rfc: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    ciudad: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=50)
    codigo_postal: Optional[str] = Field(None, max_length=10)
    pais: str = Field(default='México', max_length=50)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    contacto_principal: Optional[str] = Field(None, max_length=100)
    dias_credito: int = Field(default=0, ge=0)
    limite_credito: Decimal = Field(default=Decimal('0'), ge=0)
    descuento_general: Decimal = Field(default=Decimal('0'), ge=0, le=100)
    activo: bool = True

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(BaseModel):
    codigo_proveedor: Optional[str] = Field(None, min_length=1, max_length=20)
    nombre_proveedor: Optional[str] = Field(None, min_length=1, max_length=200)
    razon_social: Optional[str] = Field(None, max_length=200)
    rfc: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    ciudad: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=50)
    codigo_postal: Optional[str] = Field(None, max_length=10)
    pais: Optional[str] = Field(None, max_length=50)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    contacto_principal: Optional[str] = Field(None, max_length=100)
    dias_credito: Optional[int] = Field(None, ge=0)
    limite_credito: Optional[Decimal] = Field(None, ge=0)
    descuento_general: Optional[Decimal] = Field(None, ge=0, le=100)
    activo: Optional[bool] = None

class ProveedorResponse(ProveedorBase):
    id_proveedor: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True

# ========================================
# SCHEMAS PARA ALMACÉN - BODEGAS
# ========================================

class BodegaBase(BaseModel):
    codigo_bodega: str = Field(..., min_length=1, max_length=1)
    nombre_bodega: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    temperatura_min: Optional[Decimal] = Field(None, ge=-50, le=50)
    temperatura_max: Optional[Decimal] = Field(None, ge=-50, le=50)
    humedad_max: Optional[Decimal] = Field(None, ge=0, le=100)
    requiere_certificacion: bool = False
    activo: bool = True

class BodegaCreate(BodegaBase):
    pass

class BodegaUpdate(BaseModel):
    codigo_bodega: Optional[str] = Field(None, min_length=1, max_length=1)
    nombre_bodega: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = None
    temperatura_min: Optional[Decimal] = Field(None, ge=-50, le=50)
    temperatura_max: Optional[Decimal] = Field(None, ge=-50, le=50)
    humedad_max: Optional[Decimal] = Field(None, ge=0, le=100)
    requiere_certificacion: Optional[bool] = None
    activo: Optional[bool] = None

class BodegaResponse(BodegaBase):
    id_bodega: int

    class Config:
        from_attributes = True

# ========================================
# SCHEMAS PARA PASILLOS
# ========================================

class PasilloBase(BaseModel):
    id_bodega: int
    numero_pasillo: int = Field(..., ge=1)
    nombre_pasillo: Optional[str] = Field(None, max_length=50)
    longitud_metros: Optional[Decimal] = Field(None, ge=0)
    activo: bool = True

class PasilloCreate(PasilloBase):
    pass

class PasilloUpdate(BaseModel):
    id_bodega: Optional[int] = None
    numero_pasillo: Optional[int] = Field(None, ge=1)
    nombre_pasillo: Optional[str] = Field(None, max_length=50)
    longitud_metros: Optional[Decimal] = Field(None, ge=0)
    activo: Optional[bool] = None

class PasilloResponse(PasilloBase):
    id_pasillo: int

    class Config:
        from_attributes = True

class PasilloWithBodega(PasilloResponse):
    bodega: Optional[BodegaResponse] = None

# ========================================
# SCHEMAS PARA ESTANTES
# ========================================

class EstanteBase(BaseModel):
    id_pasillo: int
    codigo_estante: str = Field(..., min_length=1, max_length=5)
    altura_metros: Optional[Decimal] = Field(None, ge=0)
    capacidad_peso_kg: Optional[Decimal] = Field(None, ge=0)
    activo: bool = True

class EstanteCreate(EstanteBase):
    pass

class EstanteUpdate(BaseModel):
    id_pasillo: Optional[int] = None
    codigo_estante: Optional[str] = Field(None, min_length=1, max_length=5)
    altura_metros: Optional[Decimal] = Field(None, ge=0)
    capacidad_peso_kg: Optional[Decimal] = Field(None, ge=0)
    activo: Optional[bool] = None

class EstanteResponse(EstanteBase):
    id_estante: int

    class Config:
        from_attributes = True

class EstanteWithPasillo(EstanteResponse):
    pasillo: Optional[PasilloWithBodega] = None

# ========================================
# SCHEMAS PARA NIVELES
# ========================================

class NivelBase(BaseModel):
    id_estante: int
    numero_nivel: int = Field(..., ge=1)
    altura_cm: Optional[Decimal] = Field(None, ge=0)
    capacidad_peso_kg: Optional[Decimal] = Field(None, ge=0)
    activo: bool = True

class NivelCreate(NivelBase):
    pass

class NivelUpdate(BaseModel):
    id_estante: Optional[int] = None
    numero_nivel: Optional[int] = Field(None, ge=1)
    altura_cm: Optional[Decimal] = Field(None, ge=0)
    capacidad_peso_kg: Optional[Decimal] = Field(None, ge=0)
    activo: Optional[bool] = None

class NivelResponse(NivelBase):
    id_nivel: int

    class Config:
        from_attributes = True

class NivelWithEstante(NivelResponse):
    estante: Optional[EstanteWithPasillo] = None

# ========================================
# SCHEMAS PARA PRODUCTOS
# ========================================

class ProductoBase(BaseModel):
    sku: str = Field(..., min_length=1, max_length=50)
    nombre_producto: str = Field(..., min_length=1, max_length=200)
    descripcion_corta: Optional[str] = Field(None, max_length=500)
    descripcion_detallada: Optional[str] = None
    id_marca: Optional[int] = None
    modelo: Optional[str] = Field(None, max_length=100)
    numero_parte: Optional[str] = Field(None, max_length=100)
    id_tipo_producto: int
    id_unidad_medida: int

    # Especificaciones técnicas generales
    peso_kg: Optional[Decimal] = Field(None, ge=0)
    dimensiones_largo_cm: Optional[Decimal] = Field(None, ge=0)
    dimensiones_ancho_cm: Optional[Decimal] = Field(None, ge=0)
    dimensiones_alto_cm: Optional[Decimal] = Field(None, ge=0)
    material_principal: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=50)

    # Información para sistemas contra incendios
    presion_trabajo_bar: Optional[Decimal] = Field(None, ge=0)
    presion_maxima_bar: Optional[Decimal] = Field(None, ge=0)
    temperatura_min_celsius: Optional[Decimal] = None
    temperatura_max_celsius: Optional[Decimal] = None
    temperatura_activacion_celsius: Optional[Decimal] = None
    factor_k: Optional[Decimal] = Field(None, ge=0)
    conexion_entrada: Optional[str] = Field(None, max_length=50)
    conexion_salida: Optional[str] = Field(None, max_length=50)

    # Certificaciones y normativas
    certificacion_ul: Optional[str] = Field(None, max_length=50)
    certificacion_fm: Optional[str] = Field(None, max_length=50)
    certificacion_nfpa: Optional[str] = Field(None, max_length=100)
    otras_certificaciones: Optional[str] = None

    # Control de inventario
    stock_actual: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=0, ge=0)
    stock_maximo: int = Field(default=0, ge=0)
    punto_reorden: int = Field(default=0, ge=0)
    lead_time_dias: int = Field(default=0, ge=0)

    # Información comercial
    costo_promedio: Decimal = Field(default=Decimal('0'), ge=0)
    precio_venta: Decimal = Field(default=Decimal('0'), ge=0)
    margen_ganancia: Decimal = Field(default=Decimal('0'), ge=0, le=100)

    # Control de calidad y almacenamiento
    requiere_refrigeracion: bool = False
    vida_util_meses: Optional[int] = Field(None, ge=0)
    condiciones_almacenamiento: Optional[str] = None
    manejo_especial: Optional[str] = None

    activo: bool = True

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    nombre_producto: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion_corta: Optional[str] = Field(None, max_length=500)
    descripcion_detallada: Optional[str] = None
    id_marca: Optional[int] = None
    modelo: Optional[str] = Field(None, max_length=100)
    numero_parte: Optional[str] = Field(None, max_length=100)
    id_tipo_producto: Optional[int] = None
    id_unidad_medida: Optional[int] = None

    # Especificaciones técnicas generales
    peso_kg: Optional[Decimal] = Field(None, ge=0)
    dimensiones_largo_cm: Optional[Decimal] = Field(None, ge=0)
    dimensiones_ancho_cm: Optional[Decimal] = Field(None, ge=0)
    dimensiones_alto_cm: Optional[Decimal] = Field(None, ge=0)
    material_principal: Optional[str] = Field(None, max_length=100)
    color: Optional[str] = Field(None, max_length=50)

    # Información para sistemas contra incendios
    presion_trabajo_bar: Optional[Decimal] = Field(None, ge=0)
    presion_maxima_bar: Optional[Decimal] = Field(None, ge=0)
    temperatura_min_celsius: Optional[Decimal] = None
    temperatura_max_celsius: Optional[Decimal] = None
    temperatura_activacion_celsius: Optional[Decimal] = None
    factor_k: Optional[Decimal] = Field(None, ge=0)
    conexion_entrada: Optional[str] = Field(None, max_length=50)
    conexion_salida: Optional[str] = Field(None, max_length=50)

    # Certificaciones y normativas
    certificacion_ul: Optional[str] = Field(None, max_length=50)
    certificacion_fm: Optional[str] = Field(None, max_length=50)
    certificacion_nfpa: Optional[str] = Field(None, max_length=100)
    otras_certificaciones: Optional[str] = None

    # Control de inventario
    stock_actual: Optional[int] = Field(None, ge=0)
    stock_minimo: Optional[int] = Field(None, ge=0)
    stock_maximo: Optional[int] = Field(None, ge=0)
    punto_reorden: Optional[int] = Field(None, ge=0)
    lead_time_dias: Optional[int] = Field(None, ge=0)

    # Información comercial
    costo_promedio: Optional[Decimal] = Field(None, ge=0)
    precio_venta: Optional[Decimal] = Field(None, ge=0)
    margen_ganancia: Optional[Decimal] = Field(None, ge=0, le=100)

    # Control de calidad y almacenamiento
    requiere_refrigeracion: Optional[bool] = None
    vida_util_meses: Optional[int] = Field(None, ge=0)
    condiciones_almacenamiento: Optional[str] = None
    manejo_especial: Optional[str] = None

    activo: Optional[bool] = None

class ProductoResponse(ProductoBase):
    id_producto: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    usuario_creacion: Optional[int] = None
    usuario_modificacion: Optional[int] = None

    class Config:
        from_attributes = True

# Schemas con relaciones
class ProductoWithRelations(ProductoResponse):
    marca: Optional['MarcaResponse'] = None
    tipo_producto: Optional['TipoProductoResponse'] = None
    unidad_medida: Optional['UnidadMedidaResponse'] = None

# ========================================
# SCHEMAS PARA PRODUCTO-PROVEEDORES
# ========================================

class ProductoProveedorBase(BaseModel):
    id_producto: int
    id_proveedor: int
    es_principal: bool = False
    codigo_proveedor_producto: Optional[str] = Field(None, max_length=100)
    costo_actual: Optional[Decimal] = Field(None, ge=0)
    descuento_producto: Decimal = Field(default=Decimal('0'), ge=0, le=100)
    tiempo_entrega_dias: int = Field(default=0, ge=0)
    cantidad_minima_orden: int = Field(default=1, ge=1)
    activo: bool = True
    fecha_vigencia_desde: Optional[date] = None
    fecha_vigencia_hasta: Optional[date] = None

class ProductoProveedorCreate(ProductoProveedorBase):
    pass

class ProductoProveedorUpdate(BaseModel):
    id_producto: Optional[int] = None
    id_proveedor: Optional[int] = None
    es_principal: Optional[bool] = None
    codigo_proveedor_producto: Optional[str] = Field(None, max_length=100)
    costo_actual: Optional[Decimal] = Field(None, ge=0)
    descuento_producto: Optional[Decimal] = Field(None, ge=0, le=100)
    tiempo_entrega_dias: Optional[int] = Field(None, ge=0)
    cantidad_minima_orden: Optional[int] = Field(None, ge=1)
    activo: Optional[bool] = None
    fecha_vigencia_desde: Optional[date] = None
    fecha_vigencia_hasta: Optional[date] = None

class ProductoProveedorResponse(ProductoProveedorBase):
    id_producto_proveedor: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class ProductoProveedorWithRelations(ProductoProveedorResponse):
    producto: Optional[ProductoResponse] = None
    proveedor: Optional['ProveedorResponse'] = None

# ========================================
# SCHEMAS PARA UBICACIONES E INVENTARIO
# ========================================

class ProductoUbicacionBase(BaseModel):
    id_producto: int
    id_nivel: int
    cantidad: int = Field(..., ge=0)
    cantidad_reservada: int = Field(default=0, ge=0)
    posicion_especifica: Optional[str] = Field(None, max_length=20)
    fecha_ultima_conteo: Optional[date] = None
    observaciones: Optional[str] = None
    activo: bool = True

class ProductoUbicacionCreate(ProductoUbicacionBase):
    pass

class ProductoUbicacionUpdate(BaseModel):
    id_producto: Optional[int] = None
    id_nivel: Optional[int] = None
    cantidad: Optional[int] = Field(None, ge=0)
    cantidad_reservada: Optional[int] = Field(None, ge=0)
    posicion_especifica: Optional[str] = Field(None, max_length=20)
    fecha_ultima_conteo: Optional[date] = None
    observaciones: Optional[str] = None
    activo: Optional[bool] = None

class ProductoUbicacionResponse(ProductoUbicacionBase):
    id_ubicacion: int

    class Config:
        from_attributes = True

class ProductoUbicacionWithRelations(ProductoUbicacionResponse):
    producto: Optional[ProductoResponse] = None
    nivel: Optional[NivelWithEstante] = None

# Enum para afecta stock
class AfectaStockEnum(str, Enum):
    AUMENTA = "AUMENTA"
    DISMINUYE = "DISMINUYE"
    NO_AFECTA = "NO_AFECTA"

# Enum para estados de movimiento
class EstadoMovimientoEnum(str, Enum):
    PENDIENTE = "PENDIENTE"
    AUTORIZADO = "AUTORIZADO"
    PROCESADO = "PROCESADO"
    CANCELADO = "CANCELADO"

# ========================================
# SCHEMAS PARA DOCUMENTOS DE MOVIMIENTO
# ========================================

class DocumentoMovimientoBase(BaseModel):
    tipo_documento: str = Field(..., min_length=1, max_length=20)
    numero_documento: str = Field(..., min_length=1, max_length=50)
    fecha_documento: date
    id_proveedor: Optional[int] = None
    total_documento: Optional[Decimal] = Field(None, ge=0)
    observaciones: Optional[str] = None
    ruta_archivo: Optional[str] = Field(None, max_length=500)

class DocumentoMovimientoCreate(DocumentoMovimientoBase):
    pass

class DocumentoMovimientoUpdate(BaseModel):
    tipo_documento: Optional[str] = Field(None, min_length=1, max_length=20)
    numero_documento: Optional[str] = Field(None, min_length=1, max_length=50)
    fecha_documento: Optional[date] = None
    id_proveedor: Optional[int] = None
    total_documento: Optional[Decimal] = Field(None, ge=0)
    observaciones: Optional[str] = None
    ruta_archivo: Optional[str] = Field(None, max_length=500)

class DocumentoMovimientoResponse(DocumentoMovimientoBase):
    id_documento: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class DocumentoMovimientoWithRelations(DocumentoMovimientoResponse):
    proveedor: Optional['ProveedorResponse'] = None

# ========================================
# SCHEMAS PARA MOVIMIENTOS DE INVENTARIO
# ========================================

class MovimientoInventarioBase(BaseModel):
    id_tipo_movimiento: int
    numero_movimiento: str = Field(..., min_length=1, max_length=50)
    fecha_movimiento: datetime
    id_documento: Optional[int] = None
    id_usuario: int
    motivo: Optional[str] = None
    observaciones: Optional[str] = None
    autorizado_por: Optional[int] = None
    fecha_autorizacion: Optional[datetime] = None
    estado: EstadoMovimientoEnum = EstadoMovimientoEnum.PENDIENTE

class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass

class MovimientoInventarioUpdate(BaseModel):
    id_tipo_movimiento: Optional[int] = None
    numero_movimiento: Optional[str] = Field(None, min_length=1, max_length=50)
    fecha_movimiento: Optional[datetime] = None
    id_documento: Optional[int] = None
    id_usuario: Optional[int] = None
    motivo: Optional[str] = None
    observaciones: Optional[str] = None
    autorizado_por: Optional[int] = None
    fecha_autorizacion: Optional[datetime] = None
    estado: Optional[EstadoMovimientoEnum] = None

class MovimientoInventarioResponse(MovimientoInventarioBase):
    id_movimiento: int

    class Config:
        from_attributes = True

# ========================================
# SCHEMAS PARA DETALLE DE MOVIMIENTOS
# ========================================

class MovimientoDetalleBase(BaseModel):
    id_movimiento: int
    id_producto: int
    id_ubicacion_origen: Optional[int] = None
    id_ubicacion_destino: Optional[int] = None
    cantidad: int = Field(..., gt=0)
    costo_unitario: Decimal = Field(default=Decimal('0'), ge=0)
    costo_total: Decimal = Field(default=Decimal('0'), ge=0)
    observaciones: Optional[str] = None

class MovimientoDetalleCreate(MovimientoDetalleBase):
    pass

class MovimientoDetalleUpdate(BaseModel):
    id_movimiento: Optional[int] = None
    id_producto: Optional[int] = None
    id_ubicacion_origen: Optional[int] = None
    id_ubicacion_destino: Optional[int] = None
    cantidad: Optional[int] = Field(None, gt=0)
    costo_unitario: Optional[Decimal] = Field(None, ge=0)
    costo_total: Optional[Decimal] = Field(None, ge=0)
    observaciones: Optional[str] = None

class MovimientoDetalleResponse(MovimientoDetalleBase):
    id_detalle: int

    class Config:
        from_attributes = True

class MovimientoDetalleWithRelations(MovimientoDetalleResponse):
    producto: Optional[ProductoResponse] = None
    ubicacion_origen: Optional[ProductoUbicacionWithRelations] = None
    ubicacion_destino: Optional[ProductoUbicacionWithRelations] = None

# Schema completo de movimiento con detalles
class MovimientoInventarioWithRelations(MovimientoInventarioResponse):
    tipo_movimiento: Optional['TipoMovimientoResponse'] = None
    documento: Optional[DocumentoMovimientoWithRelations] = None
    detalles: List[MovimientoDetalleWithRelations] = []

# Schema para crear movimiento completo con detalles
class MovimientoInventarioCompleto(BaseModel):
    movimiento: MovimientoInventarioCreate
    detalles: List[MovimientoDetalleCreate]


# ========================================
# SCHEMAS PARA LOTES
# ========================================

class EstadoLoteEnum(str, Enum):
    ACTIVO = "ACTIVO"
    VENCIDO = "VENCIDO"
    CUARENTENA = "CUARENTENA"
    AGOTADO = "AGOTADO"

class LoteBase(BaseModel):
    numero_lote: str = Field(..., max_length=50, description="Número único del lote")
    fecha_fabricacion: Optional[date] = Field(None, description="Fecha de fabricación")
    fecha_vencimiento: Optional[date] = Field(None, description="Fecha de vencimiento")
    cantidad_inicial: int = Field(..., ge=0, description="Cantidad inicial del lote")
    cantidad_actual: int = Field(..., ge=0, description="Cantidad actual disponible")
    costo_promedio: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=4)
    certificado_calidad: Optional[str] = Field(None, max_length=500, description="Ruta del certificado")
    observaciones: Optional[str] = Field(None, description="Observaciones del lote")
    estado: EstadoLoteEnum = EstadoLoteEnum.ACTIVO

class LoteCreate(LoteBase):
    id_producto: int = Field(..., description="ID del producto")
    id_proveedor: Optional[int] = Field(None, description="ID del proveedor")

class LoteUpdate(BaseModel):
    numero_lote: Optional[str] = Field(None, max_length=50)
    fecha_fabricacion: Optional[date] = None
    fecha_vencimiento: Optional[date] = None
    id_proveedor: Optional[int] = None
    cantidad_inicial: Optional[int] = Field(None, ge=0)
    cantidad_actual: Optional[int] = Field(None, ge=0)
    costo_promedio: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=4)
    certificado_calidad: Optional[str] = Field(None, max_length=500)
    observaciones: Optional[str] = None
    estado: Optional[EstadoLoteEnum] = None

class LoteResponse(LoteBase):
    id_lote: int
    id_producto: int
    id_proveedor: Optional[int] = None
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class LoteWithRelations(LoteResponse):
    producto: Optional['ProductoResponse'] = None
    proveedor: Optional['ProveedorResponse'] = None
    numeros_serie: List['NumeroSerieResponse'] = []


# ========================================
# SCHEMAS PARA NÚMEROS DE SERIE
# ========================================

class EstadoSerieEnum(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    RESERVADO = "RESERVADO"
    VENDIDO = "VENDIDO"
    DEFECTUOSO = "DEFECTUOSO"
    EN_REPARACION = "EN_REPARACION"

class NumeroSerieBase(BaseModel):
    numero_serie: str = Field(..., max_length=100, description="Número de serie único")
    fecha_ingreso: date = Field(..., description="Fecha de ingreso al inventario")
    estado: EstadoSerieEnum = EstadoSerieEnum.DISPONIBLE
    cliente_asignado: Optional[str] = Field(None, max_length=200, description="Cliente asignado")
    fecha_venta: Optional[date] = Field(None, description="Fecha de venta")
    observaciones: Optional[str] = Field(None, description="Observaciones")

class NumeroSerieCreate(NumeroSerieBase):
    id_producto: int = Field(..., description="ID del producto")
    id_lote: Optional[int] = Field(None, description="ID del lote")
    id_ubicacion: Optional[int] = Field(None, description="ID de la ubicación")

class NumeroSerieUpdate(BaseModel):
    numero_serie: Optional[str] = Field(None, max_length=100)
    id_lote: Optional[int] = None
    fecha_ingreso: Optional[date] = None
    id_ubicacion: Optional[int] = None
    estado: Optional[EstadoSerieEnum] = None
    cliente_asignado: Optional[str] = Field(None, max_length=200)
    fecha_venta: Optional[date] = None
    observaciones: Optional[str] = None

class NumeroSerieResponse(NumeroSerieBase):
    id_serie: int
    id_producto: int
    id_lote: Optional[int] = None
    id_ubicacion: Optional[int] = None

    class Config:
        from_attributes = True

class NumeroSerieWithRelations(NumeroSerieResponse):
    producto: Optional['ProductoResponse'] = None
    lote: Optional['LoteResponse'] = None
    ubicacion: Optional['ProductoUbicacionResponse'] = None


# ========================================
# SCHEMAS PARA CLIENTES
# ========================================

class TipoClienteEnum(str, Enum):
    GOBIERNO = "GOBIERNO"
    PRIVADO = "PRIVADO"
    CONSTRUCTORA = "CONSTRUCTORA"
    DISTRIBUIDOR = "DISTRIBUIDOR"

class ClienteBase(BaseModel):
    codigo_cliente: str = Field(..., max_length=20, description="Código único del cliente")
    nombre_cliente: str = Field(..., max_length=200, description="Nombre del cliente")
    razon_social: Optional[str] = Field(None, max_length=200, description="Razón social")
    rfc: Optional[str] = Field(None, max_length=20, description="RFC del cliente")
    direccion: Optional[str] = Field(None, description="Dirección completa")
    ciudad: Optional[str] = Field(None, max_length=100, description="Ciudad")
    estado: Optional[str] = Field(None, max_length=50, description="Estado/Provincia")
    codigo_postal: Optional[str] = Field(None, max_length=10, description="Código postal")
    pais: str = Field(default="México", max_length=50, description="País")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono principal")
    email: Optional[EmailStr] = Field(None, description="Email de contacto")
    contacto_principal: Optional[str] = Field(None, max_length=100, description="Nombre del contacto principal")
    tipo_cliente: TipoClienteEnum = Field(..., description="Tipo de cliente")
    activo: bool = Field(default=True, description="Cliente activo")

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    codigo_cliente: Optional[str] = Field(None, max_length=20)
    nombre_cliente: Optional[str] = Field(None, max_length=200)
    razon_social: Optional[str] = Field(None, max_length=200)
    rfc: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    ciudad: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=50)
    codigo_postal: Optional[str] = Field(None, max_length=10)
    pais: Optional[str] = Field(None, max_length=50)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    contacto_principal: Optional[str] = Field(None, max_length=100)
    tipo_cliente: Optional[TipoClienteEnum] = None
    activo: Optional[bool] = None

class ClienteResponse(ClienteBase):
    id_cliente: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True

class ClienteWithObras(ClienteResponse):
    obras: List['ObraResponse'] = []


# ========================================
# SCHEMAS PARA OBRAS
# ========================================

class EstadoObraEnum(str, Enum):
    PLANIFICACION = "PLANIFICACION"
    EN_EJECUCION = "EN_EJECUCION"
    SUSPENDIDA = "SUSPENDIDA"
    FINALIZADA = "FINALIZADA"
    CANCELADA = "CANCELADA"

class PrioridadObraEnum(str, Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    CRITICA = "CRITICA"

class ObraBase(BaseModel):
    codigo_obra: str = Field(..., max_length=50, description="Código único de la obra")
    nombre_obra: str = Field(..., max_length=200, description="Nombre de la obra")
    descripcion: Optional[str] = Field(None, description="Descripción detallada de la obra")
    direccion_obra: Optional[str] = Field(None, description="Dirección de la obra")
    ciudad: Optional[str] = Field(None, max_length=100, description="Ciudad donde se ubica la obra")
    codigo_postal: Optional[str] = Field(None, max_length=10, description="Código postal")

    # Responsables
    supervisor_obra: Optional[str] = Field(None, max_length=100, description="Supervisor de la obra")
    contacto_obra: Optional[str] = Field(None, max_length=100, description="Contacto en la obra")
    telefono_obra: Optional[str] = Field(None, max_length=20, description="Teléfono de la obra")

    # Fechas del proyecto
    fecha_inicio_programada: Optional[date] = Field(None, description="Fecha programada de inicio")
    fecha_fin_programada: Optional[date] = Field(None, description="Fecha programada de finalización")
    fecha_inicio_real: Optional[date] = Field(None, description="Fecha real de inicio")
    fecha_fin_real: Optional[date] = Field(None, description="Fecha real de finalización")

    # Control financiero
    valor_contrato: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=2, description="Valor del contrato")
    moneda: str = Field(default="MXN", max_length=10, description="Moneda del contrato")

    # Control de inventario
    requiere_devolucion_sobrantes: bool = Field(default=True, description="Requiere devolución de sobrantes")
    dias_limite_devolucion: int = Field(default=30, ge=1, le=365, description="Días límite para devolución")
    porcentaje_merma_permitida: Decimal = Field(default=5.00, ge=0, le=100, max_digits=5, decimal_places=2, description="Porcentaje de merma permitida")

    # Estado y control
    estado: EstadoObraEnum = EstadoObraEnum.PLANIFICACION
    prioridad: PrioridadObraEnum = PrioridadObraEnum.MEDIA
    observaciones: Optional[str] = Field(None, description="Observaciones generales")
    activo: bool = Field(default=True, description="Obra activa")

class ObraCreate(ObraBase):
    id_cliente: int = Field(..., description="ID del cliente")

class ObraUpdate(BaseModel):
    codigo_obra: Optional[str] = Field(None, max_length=50)
    nombre_obra: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    id_cliente: Optional[int] = None
    direccion_obra: Optional[str] = None
    ciudad: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = Field(None, max_length=10)

    # Responsables
    supervisor_obra: Optional[str] = Field(None, max_length=100)
    contacto_obra: Optional[str] = Field(None, max_length=100)
    telefono_obra: Optional[str] = Field(None, max_length=20)

    # Fechas del proyecto
    fecha_inicio_programada: Optional[date] = None
    fecha_fin_programada: Optional[date] = None
    fecha_inicio_real: Optional[date] = None
    fecha_fin_real: Optional[date] = None

    # Control financiero
    valor_contrato: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=2)
    moneda: Optional[str] = Field(None, max_length=10)

    # Control de inventario
    requiere_devolucion_sobrantes: Optional[bool] = None
    dias_limite_devolucion: Optional[int] = Field(None, ge=1, le=365)
    porcentaje_merma_permitida: Optional[Decimal] = Field(None, ge=0, le=100, max_digits=5, decimal_places=2)

    # Estado y control
    estado: Optional[EstadoObraEnum] = None
    prioridad: Optional[PrioridadObraEnum] = None
    observaciones: Optional[str] = None
    activo: Optional[bool] = None
    usuario_modificacion: Optional[int] = None

class ObraResponse(ObraBase):
    id_obra: int
    id_cliente: int
    fecha_creacion: datetime
    fecha_modificacion: datetime
    usuario_creacion: Optional[int] = None
    usuario_modificacion: Optional[int] = None

    class Config:
        from_attributes = True

class ObraWithRelations(ObraResponse):
    cliente: Optional['ClienteResponse'] = None
    almacen_obra: Optional['AlmacenObraResponse'] = None


# ========================================
# SCHEMAS PARA ALMACÉN DE OBRA
# ========================================

class AlmacenObraBase(BaseModel):
    nombre_almacen: str = Field(..., max_length=100, description="Nombre del almacén")
    descripcion: Optional[str] = Field(None, description="Descripción del almacén")
    direccion: Optional[str] = Field(None, description="Dirección del almacén")
    responsable: Optional[str] = Field(None, max_length=100, description="Responsable del almacén")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono de contacto")

    # Condiciones del almacén
    tiene_seguridad: bool = Field(default=False, description="Tiene seguridad")
    tiene_techo: bool = Field(default=True, description="Tiene techo")
    capacidad_m3: Optional[Decimal] = Field(None, ge=0, max_digits=10, decimal_places=2, description="Capacidad en metros cúbicos")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")
    activo: bool = Field(default=True, description="Almacén activo")

class AlmacenObraCreate(AlmacenObraBase):
    id_obra: int = Field(..., description="ID de la obra")

class AlmacenObraUpdate(BaseModel):
    nombre_almacen: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    direccion: Optional[str] = None
    responsable: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)

    # Condiciones del almacén
    tiene_seguridad: Optional[bool] = None
    tiene_techo: Optional[bool] = None
    capacidad_m3: Optional[Decimal] = Field(None, ge=0, max_digits=10, decimal_places=2)
    observaciones: Optional[str] = None
    activo: Optional[bool] = None

class AlmacenObraResponse(AlmacenObraBase):
    id_almacen_obra: int
    id_obra: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class AlmacenObraWithRelations(AlmacenObraResponse):
    obra: Optional['ObraResponse'] = None


# ========================================
# SCHEMAS PARA DESPACHOS DE OBRA
# ========================================

class DespachosObraBase(BaseModel):
    numero_despacho: str = Field(..., max_length=50, description="Número único del despacho")
    fecha_despacho: date = Field(..., description="Fecha del despacho")

    # Transporte
    transportista: Optional[str] = Field(None, max_length=100, description="Empresa transportista")
    vehiculo: Optional[str] = Field(None, max_length=50, description="Vehículo utilizado")
    chofer: Optional[str] = Field(None, max_length=100, description="Chofer responsable")

    # Entrega
    id_usuario_despacha: int = Field(..., description="ID del usuario que realiza el despacho")
    recibido_por: Optional[str] = Field(None, max_length=100, description="Persona que recibe")
    fecha_entrega: Optional[date] = Field(None, description="Fecha de entrega")
    hora_entrega: Optional[time] = Field(None, description="Hora de entrega")

    # Control
    requiere_devolucion: bool = Field(default=True, description="Requiere devolución")
    fecha_limite_devolucion: Optional[date] = Field(None, description="Fecha límite para devolución")
    motivo_despacho: Optional[str] = Field(None, description="Motivo del despacho")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")

    estado: str = Field(default="PREPARADO", description="Estado del despacho")

class DespachosObraCreate(DespachosObraBase):
    id_obra: int = Field(..., description="ID de la obra")

class DespachosObraUpdate(BaseModel):
    numero_despacho: Optional[str] = Field(None, max_length=50)
    fecha_despacho: Optional[date] = None

    # Transporte
    transportista: Optional[str] = Field(None, max_length=100)
    vehiculo: Optional[str] = Field(None, max_length=50)
    chofer: Optional[str] = Field(None, max_length=100)

    # Entrega
    id_usuario_despacha: Optional[int] = None
    recibido_por: Optional[str] = Field(None, max_length=100)
    fecha_entrega: Optional[date] = None
    hora_entrega: Optional[time] = None

    # Control
    requiere_devolucion: Optional[bool] = None
    fecha_limite_devolucion: Optional[date] = None
    motivo_despacho: Optional[str] = None
    observaciones: Optional[str] = None

    estado: Optional[str] = None

class DespachosObraResponse(DespachosObraBase):
    id_despacho: int
    id_obra: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True

class DespachosObraWithRelations(DespachosObraResponse):
    obra: Optional['ObraResponse'] = None


# ========================================
# SCHEMAS PARA DETALLE DE DESPACHOS DE OBRA
# ========================================

class DespachosObraDetalleBase(BaseModel):
    id_producto: int = Field(..., description="ID del producto")
    cantidad_despachada: int = Field(..., ge=1, description="Cantidad despachada")
    cantidad_utilizada: int = Field(default=0, ge=0, description="Cantidad utilizada")
    cantidad_devuelta: int = Field(default=0, ge=0, description="Cantidad devuelta")
    cantidad_perdida: int = Field(default=0, ge=0, description="Cantidad perdida")

    # Trazabilidad
    id_lote: Optional[int] = Field(None, description="ID del lote")
    numeros_serie: Optional[str] = Field(None, description="Números de serie separados por comas")

    # Costos
    costo_unitario: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=4, description="Costo unitario")
    costo_total: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=2, description="Costo total")

    # Para herramientas y equipos
    es_herramienta: bool = Field(default=False, description="Es herramienta")
    requiere_devolucion_obligatoria: bool = Field(default=False, description="Requiere devolución obligatoria")

    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")

class DespachosObraDetalleCreate(DespachosObraDetalleBase):
    id_despacho: int = Field(..., description="ID del despacho")

class DespachosObraDetalleUpdate(BaseModel):
    id_producto: Optional[int] = None
    cantidad_despachada: Optional[int] = Field(None, ge=1)
    cantidad_utilizada: Optional[int] = Field(None, ge=0)
    cantidad_devuelta: Optional[int] = Field(None, ge=0)
    cantidad_perdida: Optional[int] = Field(None, ge=0)

    # Trazabilidad
    id_lote: Optional[int] = None
    numeros_serie: Optional[str] = None

    # Costos
    costo_unitario: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=4)
    costo_total: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=2)

    # Para herramientas y equipos
    es_herramienta: Optional[bool] = None
    requiere_devolucion_obligatoria: Optional[bool] = None

    observaciones: Optional[str] = None

class DespachosObraDetalleResponse(DespachosObraDetalleBase):
    id_despacho_detalle: int
    id_despacho: int

    class Config:
        from_attributes = True

class DespachosObraDetalleWithRelations(DespachosObraDetalleResponse):
    despacho: Optional['DespachosObraResponse'] = None
    producto: Optional['ProductoResponse'] = None
    lote: Optional['LoteResponse'] = None


# ========================================
# SCHEMAS PARA DEVOLUCIONES DE OBRA
# ========================================

class DevolucionesObraBase(BaseModel):
    numero_devolucion: str = Field(..., max_length=50, description="Número único de devolución")
    fecha_devolucion: date = Field(..., description="Fecha de devolución")

    # Transporte de devolución
    transportista: Optional[str] = Field(None, max_length=100, description="Empresa transportista")
    vehiculo: Optional[str] = Field(None, max_length=50, description="Vehículo utilizado")
    chofer: Optional[str] = Field(None, max_length=100, description="Chofer responsable")

    # Recepción
    id_usuario_recibe: int = Field(..., description="ID del usuario que recibe")
    entregado_por: Optional[str] = Field(None, max_length=100, description="Persona que entrega")
    fecha_recepcion: Optional[date] = Field(None, description="Fecha de recepción")
    hora_recepcion: Optional[time] = Field(None, description="Hora de recepción")

    # Motivos de devolución
    motivo_devolucion: str = Field(..., description="Motivo de la devolución")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")

    estado: str = Field(default="EN_TRANSITO", description="Estado de la devolución")

class DevolucionesObraCreate(DevolucionesObraBase):
    id_obra: int = Field(..., description="ID de la obra")
    id_despacho: int = Field(..., description="ID del despacho")

class DevolucionesObraUpdate(BaseModel):
    numero_devolucion: Optional[str] = Field(None, max_length=50)
    fecha_devolucion: Optional[date] = None

    # Transporte de devolución
    transportista: Optional[str] = Field(None, max_length=100)
    vehiculo: Optional[str] = Field(None, max_length=50)
    chofer: Optional[str] = Field(None, max_length=100)

    # Recepción
    id_usuario_recibe: Optional[int] = None
    entregado_por: Optional[str] = Field(None, max_length=100)
    fecha_recepcion: Optional[date] = None
    hora_recepcion: Optional[time] = None

    # Motivos de devolución
    motivo_devolucion: Optional[str] = None
    observaciones: Optional[str] = None

    estado: Optional[str] = None

class DevolucionesObraResponse(DevolucionesObraBase):
    id_devolucion: int
    id_obra: int
    id_despacho: int
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True

class DevolucionesObraWithRelations(DevolucionesObraResponse):
    obra: Optional['ObraResponse'] = None
    despacho: Optional['DespachosObraResponse'] = None
    detalles: Optional[List['DevolucionesObraDetalleResponse']] = None


# ========================================
# SCHEMAS PARA DETALLE DE DEVOLUCIONES DE OBRA
# ========================================

class DevolucionesObraDetalleBase(BaseModel):
    id_producto: int = Field(..., description="ID del producto")
    cantidad_devuelta: int = Field(..., ge=1, description="Cantidad devuelta")

    # Estado del producto devuelto
    estado_producto: str = Field(..., description="Estado del producto devuelto")
    requiere_limpieza: bool = Field(default=False, description="Requiere limpieza")
    requiere_reparacion: bool = Field(default=False, description="Requiere reparación")
    requiere_calibracion: bool = Field(default=False, description="Requiere calibración")

    # Trazabilidad
    id_lote: Optional[int] = Field(None, description="ID del lote")
    numeros_serie: Optional[str] = Field(None, description="Números de serie separados por comas")

    # Ubicación de recepción
    id_ubicacion_recepcion: Optional[int] = Field(None, description="ID de ubicación de recepción")

    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")

class DevolucionesObraDetalleCreate(DevolucionesObraDetalleBase):
    id_devolucion: int = Field(..., description="ID de la devolución")

class DevolucionesObraDetalleUpdate(BaseModel):
    id_producto: Optional[int] = None
    cantidad_devuelta: Optional[int] = Field(None, ge=1)

    # Estado del producto devuelto
    estado_producto: Optional[str] = None
    requiere_limpieza: Optional[bool] = None
    requiere_reparacion: Optional[bool] = None
    requiere_calibracion: Optional[bool] = None

    # Trazabilidad
    id_lote: Optional[int] = None
    numeros_serie: Optional[str] = None

    # Ubicación de recepción
    id_ubicacion_recepcion: Optional[int] = None

    observaciones: Optional[str] = None

class DevolucionesObraDetalleResponse(DevolucionesObraDetalleBase):
    id_devolucion_detalle: int
    id_devolucion: int

    class Config:
        from_attributes = True

class DevolucionesObraDetalleWithRelations(DevolucionesObraDetalleResponse):
    devolucion: Optional['DevolucionesObraResponse'] = None
    producto: Optional['ProductoResponse'] = None
    lote: Optional['LoteResponse'] = None
    ubicacion_recepcion: Optional['ProductoUbicacionResponse'] = None


# ========================================
# SCHEMAS PARA INVENTARIO DE OBRA
# ========================================

class InventarioObraBase(BaseModel):
    id_producto: int = Field(..., description="ID del producto")
    cantidad_actual: int = Field(default=0, ge=0, description="Cantidad actual en la obra")
    cantidad_utilizada_acumulada: int = Field(default=0, ge=0, description="Cantidad utilizada acumulada")
    cantidad_devuelta_acumulada: int = Field(default=0, ge=0, description="Cantidad devuelta acumulada")

    # Control de costos
    costo_promedio: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=4, description="Costo promedio")

    # Trazabilidad
    fecha_ultimo_movimiento: Optional[datetime] = Field(None, description="Fecha del último movimiento")

    # Para herramientas
    es_herramienta: bool = Field(default=False, description="Es herramienta")
    ubicacion_especifica: Optional[str] = Field(None, max_length=100, description="Ubicación específica en la obra")
    responsable_herramienta: Optional[str] = Field(None, max_length=100, description="Responsable de la herramienta")

    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")

class InventarioObraCreate(InventarioObraBase):
    id_obra: int = Field(..., description="ID de la obra")

class InventarioObraUpdate(BaseModel):
    cantidad_actual: Optional[int] = Field(None, ge=0)
    cantidad_utilizada_acumulada: Optional[int] = Field(None, ge=0)
    cantidad_devuelta_acumulada: Optional[int] = Field(None, ge=0)

    # Control de costos
    costo_promedio: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=4)

    # Trazabilidad
    fecha_ultimo_movimiento: Optional[datetime] = None

    # Para herramientas
    es_herramienta: Optional[bool] = None
    ubicacion_especifica: Optional[str] = Field(None, max_length=100)
    responsable_herramienta: Optional[str] = Field(None, max_length=100)

    observaciones: Optional[str] = None

class InventarioObraResponse(InventarioObraBase):
    id_inventario_obra: int
    id_obra: int
    valor_inventario: float = Field(description="Valor calculado del inventario")

    class Config:
        from_attributes = True

class InventarioObraWithRelations(InventarioObraResponse):
    obra: Optional['ObraResponse'] = None
    producto: Optional['ProductoResponse'] = None


# ========================================
# SCHEMAS PARA RESERVAS
# ========================================

class ReservasBase(BaseModel):
    numero_reserva: str = Field(..., max_length=50, description="Número único de reserva")
    id_producto: int = Field(..., description="ID del producto")
    cantidad_reservada: int = Field(..., ge=1, description="Cantidad reservada")
    id_ubicacion: int = Field(..., description="ID de la ubicación")

    # Puede ser para cliente/obra específica o genérica
    id_cliente: Optional[int] = Field(None, description="ID del cliente")
    id_obra: Optional[int] = Field(None, description="ID de la obra")
    cliente_externo: Optional[str] = Field(None, max_length=200, description="Cliente externo no registrado")
    proyecto_externo: Optional[str] = Field(None, max_length=200, description="Proyecto externo")

    fecha_vencimiento_reserva: Optional[datetime] = Field(None, description="Fecha de vencimiento de la reserva")
    motivo_reserva: Optional[str] = Field(None, description="Motivo de la reserva")
    id_usuario: int = Field(..., description="ID del usuario que crea la reserva")

    estado: str = Field(default="ACTIVA", description="Estado de la reserva")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales")

class ReservasCreate(ReservasBase):
    pass

class ReservasUpdate(BaseModel):
    numero_reserva: Optional[str] = Field(None, max_length=50)
    cantidad_reservada: Optional[int] = Field(None, ge=1)
    id_ubicacion: Optional[int] = None

    # Puede ser para cliente/obra específica o genérica
    id_cliente: Optional[int] = None
    id_obra: Optional[int] = None
    cliente_externo: Optional[str] = Field(None, max_length=200)
    proyecto_externo: Optional[str] = Field(None, max_length=200)

    fecha_vencimiento_reserva: Optional[datetime] = None
    motivo_reserva: Optional[str] = None
    id_usuario: Optional[int] = None

    estado: Optional[str] = None
    observaciones: Optional[str] = None

class ReservasResponse(ReservasBase):
    id_reserva: int
    fecha_reserva: datetime

    class Config:
        from_attributes = True

class ReservasWithRelations(ReservasResponse):
    producto: Optional['ProductoResponse'] = None
    ubicacion: Optional['ProductoUbicacionResponse'] = None
    cliente: Optional['ClienteResponse'] = None
    obra: Optional['ObraResponse'] = None

# Enums para ProgramacionConteos
class TipoConteo(str, Enum):
    COMPLETO = "COMPLETO"
    CICLICO = "CICLICO"
    CATEGORIA = "CATEGORIA"
    BODEGA = "BODEGA"
    OBRA = "OBRA"
    ALMACEN_OBRA = "ALMACEN_OBRA"

class EstadoProgramacion(str, Enum):
    PROGRAMADO = "PROGRAMADO"
    EN_PROCESO = "EN_PROCESO"
    COMPLETADO = "COMPLETADO"
    CANCELADO = "CANCELADO"

# Schema base para ProgramacionConteos
class ProgramacionConteosBase(BaseModel):
    nombre_conteo: str = Field(..., max_length=100)
    fecha_programada: date
    tipo_conteo: TipoConteo
    id_bodega: Optional[int] = None
    id_categoria: Optional[int] = None
    id_obra: Optional[int] = None
    id_usuario_responsable: int
    observaciones: Optional[str] = None

# Schema para crear (POST)
class ProgramacionConteosCreate(ProgramacionConteosBase):
    pass

# Schema para actualizar (PUT)
class ProgramacionConteosUpdate(BaseModel):
    nombre_conteo: Optional[str] = Field(None, max_length=100)
    fecha_programada: Optional[date] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    tipo_conteo: Optional[TipoConteo] = None
    id_bodega: Optional[int] = None
    id_categoria: Optional[int] = None
    id_obra: Optional[int] = None
    id_usuario_responsable: Optional[int] = None
    estado: Optional[EstadoProgramacion] = None
    observaciones: Optional[str] = None

# Schema para respuesta (GET)
class ProgramacionConteosResponse(ProgramacionConteosBase):
    id_programacion: int
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: EstadoProgramacion = EstadoProgramacion.PROGRAMADO

    class Config:
        from_attributes = True

# Schema con relaciones
class ProgramacionConteosWithRelations(ProgramacionConteosResponse):
    bodega: Optional['BodegaResponse'] = None
    categoria: Optional['CategoriaResponse'] = None
    obra: Optional['ObraResponse'] = None

# Schema base para ConteosFisicos
class ConteosFisicosBase(BaseModel):
    id_programacion: int
    id_producto: int
    id_ubicacion: Optional[int] = None
    id_obra: Optional[int] = None
    cantidad_sistema: int
    cantidad_fisica: int
    id_usuario_contador: int
    observaciones: Optional[str] = None

# Schema para crear (POST)
class ConteosFisicosCreate(ConteosFisicosBase):
    pass

# Schema para actualizar (PUT)
class ConteosFisicosUpdate(BaseModel):
    cantidad_fisica: Optional[int] = None
    observaciones: Optional[str] = None
    ajuste_procesado: Optional[bool] = None

# Schema para respuesta (GET)
class ConteosFisicosResponse(ConteosFisicosBase):
    id_conteo: int
    fecha_conteo: datetime
    ajuste_procesado: bool = False
    id_movimiento_ajuste: Optional[int] = None
    diferencia: int

    class Config:
        from_attributes = True

    @property
    def diferencia(self) -> int:
        return self.cantidad_fisica - self.cantidad_sistema

# Schema con relaciones
class ConteosFisicosWithRelations(ConteosFisicosResponse):
    programacion: Optional['ProgramacionConteosResponse'] = None
    producto: Optional['ProductoResponse'] = None
    ubicacion: Optional['ProductoUbicacionResponse'] = None
    obra: Optional['ObraResponse'] = None
    movimiento_ajuste: Optional['MovimientoInventarioResponse'] = None

# Enums para ConfiguracionAlertas
class TipoAlerta(str, Enum):
    STOCK_MINIMO = "STOCK_MINIMO"
    VENCIMIENTO = "VENCIMIENTO"
    SIN_MOVIMIENTO = "SIN_MOVIMIENTO"
    CERTIFICACION_VENCIDA = "CERTIFICACION_VENCIDA"
    DEVOLUCION_PENDIENTE = "DEVOLUCION_PENDIENTE"
    OBRA_SIN_ACTIVIDAD = "OBRA_SIN_ACTIVIDAD"
    MATERIAL_VENCIDO_EN_OBRA = "MATERIAL_VENCIDO_EN_OBRA"
    DESPACHO_NO_ENTREGADO = "DESPACHO_NO_ENTREGADO"

# Schema base para ConfiguracionAlertas
class ConfiguracionAlertasBase(BaseModel):
    nombre_alerta: str = Field(..., max_length=100)
    tipo_alerta: TipoAlerta
    activa: bool = True
    dias_anticipacion: int = Field(default=0, ge=0)
    usuarios_notificar: Optional[List[int]] = None
    email_notificar: Optional[List[str]] = None
    frecuencia_revision_horas: int = Field(default=24, ge=1)

# Schema para crear (POST)
class ConfiguracionAlertasCreate(ConfiguracionAlertasBase):
    pass

# Schema para actualizar (PUT)
class ConfiguracionAlertasUpdate(BaseModel):
    nombre_alerta: Optional[str] = Field(None, max_length=100)
    tipo_alerta: Optional[TipoAlerta] = None
    activa: Optional[bool] = None
    dias_anticipacion: Optional[int] = Field(None, ge=0)
    usuarios_notificar: Optional[List[int]] = None
    email_notificar: Optional[List[str]] = None
    frecuencia_revision_horas: Optional[int] = Field(None, ge=1)

# Schema para respuesta (GET)
class ConfiguracionAlertasResponse(BaseModel):
    id_alerta: int
    nombre_alerta: str
    tipo_alerta: TipoAlerta
    activa: bool
    dias_anticipacion: int
    usuarios_notificar: Optional[List[int]] = None
    email_notificar: Optional[List[str]] = None
    frecuencia_revision_horas: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        """Convertir desde el modelo ORM, manejando las listas CSV"""
        return cls(
            id_alerta=obj.id_alerta,
            nombre_alerta=obj.nombre_alerta,
            tipo_alerta=obj.tipo_alerta,
            activa=obj.activa,
            dias_anticipacion=obj.dias_anticipacion,
            usuarios_notificar=obj.get_usuarios_lista(),
            email_notificar=obj.get_emails_lista(),
            frecuencia_revision_horas=obj.frecuencia_revision_horas,
            fecha_creacion=obj.fecha_creacion
        )

# Enums para LogAlertas
class NivelPrioridad(str, Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    CRITICA = "CRITICA"

class EstadoAlerta(str, Enum):
    PENDIENTE = "PENDIENTE"
    VISTA = "VISTA"
    RESUELTA = "RESUELTA"
    IGNORADA = "IGNORADA"

# Schema base para LogAlertas
class LogAlertasBase(BaseModel):
    id_alerta: int
    id_producto: Optional[int] = None
    id_obra: Optional[int] = None
    id_despacho: Optional[int] = None
    mensaje: str
    nivel_prioridad: NivelPrioridad = NivelPrioridad.MEDIA

# Schema para crear (POST)
class LogAlertasCreate(LogAlertasBase):
    pass

# Schema para actualizar (PUT)
class LogAlertasUpdate(BaseModel):
    nivel_prioridad: Optional[NivelPrioridad] = None
    estado: Optional[EstadoAlerta] = None
    observaciones_resolucion: Optional[str] = None

# Schema para respuesta (GET)
class LogAlertasResponse(LogAlertasBase):
    id_log_alerta: int
    fecha_generacion: datetime
    fecha_visualizacion: Optional[datetime] = None
    fecha_resolucion: Optional[datetime] = None
    estado: EstadoAlerta = EstadoAlerta.PENDIENTE
    usuario_resolucion: Optional[int] = None
    observaciones_resolucion: Optional[str] = None

    # Propiedades calculadas
    es_pendiente: bool
    es_critica: bool
    tiempo_sin_resolver: float

    class Config:
        from_attributes = True

# Schema con relaciones
class LogAlertasWithRelations(LogAlertasResponse):
    configuracion_alerta: Optional['ConfiguracionAlertasResponse'] = None
    producto: Optional['ProductoResponse'] = None
    obra: Optional['ObraResponse'] = None
    despacho: Optional['DespachosObraResponse'] = None

# Schema para marcar como vista
class MarcarVistaRequest(BaseModel):
    fecha_visualizacion: Optional[datetime] = None

# Schema para resolver alerta
class ResolverAlertaRequest(BaseModel):
    usuario_resolucion: int
    observaciones_resolucion: Optional[str] = None
    fecha_resolucion: Optional[datetime] = None

# Schema para ignorar alerta
class IgnorarAlertaRequest(BaseModel):
    usuario_resolucion: int
    motivo: Optional[str] = None

# Schema base para Roles
class RolesBase(BaseModel):
    nombre_rol: str = Field(..., max_length=50)
    descripcion: Optional[str] = None
    activo: bool = True

# Schema para crear (POST)
class RolesCreate(RolesBase):
    pass

# Schema para actualizar (PUT)
class RolesUpdate(BaseModel):
    nombre_rol: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

# Schema para respuesta (GET)
class RolesResponse(RolesBase):
    id_rol: int

    class Config:
        from_attributes = True

# Schema base para Usuarios
class UsuariosBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: str = Field(..., max_length=100)
    nombre_completo: str = Field(..., max_length=200)
    id_rol: int
    activo: bool = True

# Schema para crear (POST)
class UsuariosCreate(UsuariosBase):
    password: str = Field(..., min_length=8, description="Contraseña (mínimo 8 caracteres)")

# Schema para actualizar (PUT)
class UsuariosUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    nombre_completo: Optional[str] = Field(None, max_length=200)
    id_rol: Optional[int] = None
    activo: Optional[bool] = None

# Schema para cambiar contraseña
class CambiarPasswordRequest(BaseModel):
    password_actual: str
    password_nueva: str = Field(..., min_length=8, description="Nueva contraseña (mínimo 8 caracteres)")

# Schema para respuesta (GET) - Sin password_hash
class UsuariosResponse(UsuariosBase):
    id_usuario: int
    ultimo_acceso: Optional[datetime] = None
    fecha_creacion: datetime
    fecha_modificacion: datetime

    class Config:
        from_attributes = True

# Schema con relaciones
class UsuariosWithRelations(UsuariosResponse):
    rol: Optional['RolesResponse'] = None

# Schema para login
class LoginRequest(BaseModel):
    username: str
    password: str

# Schema para respuesta de login
class LoginResponse(BaseModel):
    usuario: UsuariosResponse
    token: Optional[str] = None  # Para futura implementación de JWT
    mensaje: str

# ========================================
# SCHEMAS PARA PERMISOS
# ========================================

# Schema base para Permisos
class PermisoBase(BaseModel):
    id_rol: int
    modulo: str = Field(..., max_length=50)
    crear: bool = False
    leer: bool = False
    actualizar: bool = False
    eliminar: bool = False
    autorizar: bool = False

# Schema para crear (POST)
class PermisoCreate(PermisoBase):
    pass

# Schema para actualizar (PUT)
class PermisoUpdate(BaseModel):
    id_rol: Optional[int] = None
    modulo: Optional[str] = Field(None, max_length=50)
    crear: Optional[bool] = None
    leer: Optional[bool] = None
    actualizar: Optional[bool] = None
    eliminar: Optional[bool] = None
    autorizar: Optional[bool] = None

# Schema para respuesta (GET)
class PermisoResponse(PermisoBase):
    id_permiso: int

    class Config:
        from_attributes = True

# Schema con relaciones
class PermisoWithRol(PermisoResponse):
    rol: Optional['RolesResponse'] = None

# ========================================
# SCHEMAS PARA CONFIGURACION SISTEMA
# ========================================

# Enum para tipos de dato
class TipoDatoConfig(str, Enum):
    STRING = "STRING"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"

# Schema base para ConfiguracionSistema
class ConfiguracionSistemaBase(BaseModel):
    parametro: str = Field(..., max_length=100)
    valor: Optional[str] = None
    tipo_dato: TipoDatoConfig = TipoDatoConfig.STRING
    descripcion: Optional[str] = None
    modificable: bool = True
    usuario_modificacion: Optional[int] = None

# Schema para crear (POST)
class ConfiguracionSistemaCreate(ConfiguracionSistemaBase):
    pass

# Schema para actualizar (PUT)
class ConfiguracionSistemaUpdate(BaseModel):
    parametro: Optional[str] = Field(None, max_length=100)
    valor: Optional[str] = None
    tipo_dato: Optional[TipoDatoConfig] = None
    descripcion: Optional[str] = None
    modificable: Optional[bool] = None
    usuario_modificacion: Optional[int] = None

# Schema para respuesta (GET)
class ConfiguracionSistemaResponse(ConfiguracionSistemaBase):
    id_config: int
    fecha_modificacion: datetime

    class Config:
        from_attributes = True

# Schema con información completa incluyendo valor tipado
class ConfiguracionSistemaCompleta(ConfiguracionSistemaResponse):
    valor_typed: Optional[str] = None  # Se calculará en el endpoint

# ========================================
# SCHEMAS PARA INVENTARIO CONSOLIDADO
# ========================================

# Enum para niveles de stock
class NivelStock(str, Enum):
    AGOTADO = "AGOTADO"
    CRITICO = "CRITICO"
    BAJO = "BAJO"
    NORMAL = "NORMAL"
    EXCESO = "EXCESO"
    SIN_DATOS = "SIN_DATOS"

# Schema para filtros de inventario consolidado
class InventarioConsolidadoFilters(BaseModel):
    nivel_stock: Optional[NivelStock] = None
    necesita_reposicion: Optional[bool] = None
    exceso_stock: Optional[bool] = None
    stock_minimo_desde: Optional[int] = Field(None, ge=0)
    stock_maximo_hasta: Optional[int] = Field(None, ge=0)
    valor_minimo: Optional[Decimal] = Field(None, ge=0)
    valor_maximo: Optional[Decimal] = Field(None, ge=0)
    es_alto_valor: Optional[bool] = None
    buscar_sku: Optional[str] = Field(None, max_length=50)
    buscar_nombre: Optional[str] = Field(None, max_length=200)

# Schema base para inventario consolidado
class InventarioConsolidadoBase(BaseModel):
    id_producto: int
    sku: str
    nombre_producto: str
    stock_almacen: int
    stock_obras: int
    stock_total: int
    stock_minimo: int
    stock_maximo: int
    costo_promedio: Decimal
    valor_total: Decimal

# Schema para respuesta básica
class InventarioConsolidadoResponse(InventarioConsolidadoBase):
    nivel_stock: str
    necesita_reposicion: bool
    exceso_stock: bool
    porcentaje_stock_minimo: float
    porcentaje_stock_maximo: float
    es_producto_alto_valor: bool

    class Config:
        from_attributes = True

# Schema para respuesta completa con información detallada
class InventarioConsolidadoCompleto(InventarioConsolidadoResponse):
    distribucion_stock: dict
    valor_promedio_unitario: float
    dias_stock_estimados: Optional[int] = None

# Schema para estadísticas de inventario
class EstadisticasInventario(BaseModel):
    total_productos: int
    total_valor_inventario: Decimal
    productos_criticos: int
    productos_exceso: int
    productos_agotados: int
    productos_normales: int
    valor_promedio_por_producto: Decimal
    porcentaje_productos_criticos: float
    distribucion_por_nivel: dict

# Schema para alertas de inventario
class AlertaInventario(BaseModel):
    id_producto: int
    sku: str
    nombre_producto: str
    tipo_alerta: str  # "CRITICO", "AGOTADO", "EXCESO", "ALTO_VALOR"
    nivel_actual: int
    nivel_referencia: int
    porcentaje_diferencia: float
    valor_total: Decimal
    mensaje: str

# Schema para recomendaciones de reposición
class RecomendacionReposicion(BaseModel):
    id_producto: int
    sku: str
    nombre_producto: str
    stock_actual: int
    stock_minimo: int
    stock_recomendado: int
    cantidad_sugerida: int
    costo_estimado: Decimal
    prioridad: str  # "ALTA", "MEDIA", "BAJA"
    justificacion: str

# Schema para análisis de rotación
class AnalisisRotacion(BaseModel):
    id_producto: int
    sku: str
    nombre_producto: str
    stock_total: int
    valor_total: Decimal
    rotacion_estimada: Optional[str] = None  # "ALTA", "MEDIA", "BAJA", "NULA"
    dias_sin_movimiento: Optional[int] = None
    recomendacion: str

# Schema para comparativo de períodos
class ComparativoPeriodo(BaseModel):
    id_producto: int
    sku: str
    nombre_producto: str
    stock_actual: int
    stock_anterior: int
    variacion_absoluta: int
    variacion_porcentual: float
    valor_actual: Decimal
    valor_anterior: Decimal
    variacion_valor: Decimal
    tendencia: str  # "AUMENTANDO", "DISMINUYENDO", "ESTABLE"

# Schema para exportación
class ExportInventarioCompleto(BaseModel):
    fecha_exportacion: datetime
    total_registros: int
    criterios_filtro: Optional[dict] = None
    productos: List[InventarioConsolidadoCompleto]
    resumen_estadisticas: EstadisticasInventario

# ========================================
# SCHEMAS PARA OBRAS INVENTARIO
# ========================================

# Enum para estados de obra
class EstadoObra(str, Enum):
    PLANIFICACION = "PLANIFICACION"
    EN_EJECUCION = "EN_EJECUCION"
    SUSPENDIDA = "SUSPENDIDA"
    FINALIZADA = "FINALIZADA"
    CANCELADA = "CANCELADA"

# Enum para tipos de obra
class TipoObra(str, Enum):
    CONSTRUCCION = "CONSTRUCCION"
    MANTENIMIENTO = "MANTENIMIENTO"
    INSTALACION = "INSTALACION"
    REPARACION = "REPARACION"
    INSPECCION = "INSPECCION"
    AUDITORIA = "AUDITORIA"
    CONSULTORIA = "CONSULTORIA"

# Enum para urgencia de obra
class UrgenciaObra(str, Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    CRITICA = "CRITICA"
    EMERGENCIA = "EMERGENCIA"

# Enum para categorías de estado
class EstadoObraCategoria(str, Enum):
    PREPARACION = "PREPARACION"
    ACTIVA = "ACTIVA"
    SUSPENDIDA = "SUSPENDIDA"
    FINALIZADA = "FINALIZADA"
    CANCELADA = "CANCELADA"
    DESCONOCIDO = "DESCONOCIDO"

# Enum para densidad de inventario
class DensidadInventario(str, Enum):
    SIN_INVENTARIO = "SIN_INVENTARIO"
    MINIMA = "MINIMA"
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"

# Enum para categoría de valor
class CategoriaValor(str, Enum):
    SIN_VALOR = "SIN_VALOR"
    VALOR_MINIMO = "VALOR_MINIMO"
    VALOR_BAJO = "VALOR_BAJO"
    VALOR_MEDIO = "VALOR_MEDIO"
    ALTO_VALOR = "ALTO_VALOR"

# Enum para urgencia de finalización
class UrgenciaFinalizacion(str, Enum):
    NORMAL = "NORMAL"
    PRÓXIMA = "PRÓXIMA"
    URGENTE = "URGENTE"
    RETRASADA = "RETRASADA"
    SIN_FECHA = "SIN_FECHA"

# Schema para filtros de obras inventario
class ObrasInventarioFilters(BaseModel):
    estado: Optional[EstadoObra] = None
    estado_categoria: Optional[EstadoObraCategoria] = None
    densidad_inventario: Optional[DensidadInventario] = None
    categoria_valor: Optional[CategoriaValor] = None
    urgencia_finalizacion: Optional[UrgenciaFinalizacion] = None
    tiene_inventario: Optional[bool] = None
    requiere_atencion: Optional[bool] = None
    esta_retrasada: Optional[bool] = None
    valor_minimo: Optional[Decimal] = Field(None, ge=0)
    valor_maximo: Optional[Decimal] = Field(None, ge=0)
    productos_minimos: Optional[int] = Field(None, ge=0)
    productos_maximos: Optional[int] = Field(None, ge=0)
    buscar_codigo: Optional[str] = Field(None, max_length=50)
    buscar_nombre: Optional[str] = Field(None, max_length=200)
    buscar_cliente: Optional[str] = Field(None, max_length=200)

# Schema base para obras inventario
class ObrasInventarioBase(BaseModel):
    id_obra: int
    codigo_obra: str
    nombre_obra: str
    estado: str
    nombre_cliente: str
    productos_diferentes: int
    cantidad_total_productos: int
    valor_total_inventario: Decimal
    fecha_inicio_real: Optional[date] = None
    fecha_fin_programada: Optional[date] = None

# Schema para respuesta básica
class ObrasInventarioResponse(ObrasInventarioBase):
    estado_obra_categoria: str
    tiene_inventario: bool
    valor_promedio_por_producto: float
    densidad_inventario: str
    categoria_valor: str
    dias_en_ejecucion: Optional[int] = None
    dias_restantes: Optional[int] = None
    esta_retrasada: bool
    urgencia_finalizacion: str
    requiere_atencion: bool

    class Config:
        from_attributes = True

# Schema para respuesta completa con información detallada
class ObrasInventarioCompleto(ObrasInventarioResponse):
    eficiencia_inventario: float
    indicadores_riesgo: List[str]
    metricas_performance: dict
    resumen_completo: dict

# Schema para estadísticas de obras
class EstadisticasObras(BaseModel):
    total_obras: int
    obras_activas: int
    obras_suspendidas: int
    obras_finalizadas: int
    obras_con_inventario: int
    obras_sin_inventario: int
    obras_retrasadas: int
    obras_requieren_atencion: int
    valor_total_inventario_obras: Decimal
    valor_promedio_por_obra: Decimal
    productos_promedio_por_obra: float
    distribucion_por_estado: dict
    distribucion_por_categoria_valor: dict

# Schema para alertas de obras
class AlertaObra(BaseModel):
    id_obra: int
    codigo_obra: str
    nombre_obra: str
    nombre_cliente: str
    tipo_alerta: str  # "RETRASADA", "URGENTE", "ALTO_VALOR_SUSPENDIDA", etc.
    nivel_criticidad: str  # "ALTA", "MEDIA", "BAJA"
    descripcion: str
    valor_inventario: Decimal
    dias_retraso: Optional[int] = None
    fecha_limite: Optional[date] = None
    acciones_recomendadas: List[str]

# Schema para análisis temporal de obras
class AnalisisTemporalObras(BaseModel):
    id_obra: int
    codigo_obra: str
    nombre_obra: str
    dias_programados: Optional[int] = None
    dias_transcurridos: Optional[int] = None
    dias_restantes: Optional[int] = None
    porcentaje_completado: float
    tendencia: str  # "EN_TIEMPO", "RETRASADA", "ADELANTADA"
    eficiencia_temporal: float

# Schema para ranking de obras por valor
class RankingObrasValor(BaseModel):
    posicion: int
    id_obra: int
    codigo_obra: str
    nombre_obra: str
    nombre_cliente: str
    valor_total_inventario: Decimal
    productos_diferentes: int
    categoria_valor: str
    porcentaje_del_total: float

# Schema para comparativo de obras
class ComparativoObras(BaseModel):
    id_obra: int
    codigo_obra: str
    nombre_obra: str
    valor_actual: Decimal
    valor_anterior: Optional[Decimal] = None
    variacion_valor: Optional[Decimal] = None
    variacion_porcentual: Optional[float] = None
    productos_actual: int
    productos_anterior: Optional[int] = None
    variacion_productos: Optional[int] = None
    estado_actual: str
    estado_anterior: Optional[str] = None

# Schema para recomendaciones de obras
class RecomendacionObra(BaseModel):
    id_obra: int
    codigo_obra: str
    nombre_obra: str
    tipo_recomendacion: str  # "REVISAR_INVENTARIO", "ACELERAR_PROYECTO", "CONSOLIDAR_RECURSOS"
    prioridad: str  # "ALTA", "MEDIA", "BAJA"
    descripcion: str
    acciones_sugeridas: List[str]
    impacto_estimado: str
    plazo_recomendado: str

# Schema para dashboard de obras
class DashboardObras(BaseModel):
    resumen_general: EstadisticasObras
    obras_requieren_atencion: List[ObrasInventarioResponse]
    alertas_criticas: List[AlertaObra]
    ranking_por_valor: List[RankingObrasValor]
    obras_proximas_vencimiento: List[ObrasInventarioResponse]
    analisis_temporal: List[AnalisisTemporalObras]

# Schema para vista de obras inventario (lectura)
class VistaObrasInventarioRead(BaseModel):
    id_obra: int
    codigo_obra: str
    nombre_obra: str
    descripcion_obra: Optional[str] = None
    estado_obra: EstadoObra
    tipo_obra: TipoObra
    urgencia_obra: UrgenciaObra
    fecha_inicio: Optional[date] = None
    fecha_fin_programada: Optional[date] = None
    fecha_fin_real: Optional[date] = None
    porcentaje_completado: float
    id_cliente: int
    nombre_cliente: str
    email_cliente: Optional[str] = None
    telefono_cliente: Optional[str] = None
    id_bodega: int
    nombre_bodega: str
    codigo_bodega: str
    id_producto: int
    codigo_producto: str
    nombre_producto: str
    id_categoria: int
    nombre_categoria: str
    cantidad_asignada: float
    cantidad_despachada: float
    cantidad_devuelta: float
    cantidad_pendiente: float
    cantidad_disponible: float
    precio_unitario: Decimal
    costo_unitario: Decimal
    valor_total_asignado: Decimal
    valor_total_despachado: Decimal
    valor_total_pendiente: Decimal
    stock_minimo: float
    stock_maximo: float
    punto_reorden: float
    unidad_medida: str
    # Propiedades calculadas
    valor_neto: Optional[Decimal] = None
    margen_ganancia: Optional[float] = None
    es_rentable: Optional[bool] = None
    dias_desde_inicio: Optional[int] = None
    dias_para_fin: Optional[int] = None
    esta_retrasada: Optional[bool] = None
    esta_en_tiempo: Optional[bool] = None
    necesita_atencion: Optional[bool] = None
    tiene_stock_critico: Optional[bool] = None
    tiene_sobrecosto: Optional[bool] = None
    eficiencia_despacho: Optional[float] = None
    calificacion_riesgo: Optional[str] = None
    metrica_rendimiento: Optional[float] = None
    categoria_valor: Optional[str] = None
    indicador_urgencia: Optional[str] = None

    class Config:
        from_attributes = True

# Schema para filtros de vista de obras inventario
class VistaObrasInventarioFilter(BaseModel):
    obra_id: Optional[int] = None
    cliente_id: Optional[int] = None
    bodega_id: Optional[int] = None
    producto_id: Optional[int] = None
    estado_obra: Optional[EstadoObra] = None
    tipo_obra: Optional[TipoObra] = None
    urgencia_obra: Optional[UrgenciaObra] = None
    fecha_inicio_desde: Optional[date] = None
    fecha_inicio_hasta: Optional[date] = None
    fecha_fin_desde: Optional[date] = None
    fecha_fin_hasta: Optional[date] = None
    tiene_stock_critico: Optional[bool] = None
    tiene_sobrecosto: Optional[bool] = None
    valor_minimo: Optional[Decimal] = None
    valor_maximo: Optional[Decimal] = None
    porcentaje_completado_min: Optional[float] = None
    porcentaje_completado_max: Optional[float] = None

# Enums adicionales para alertas y métricas
class AlertaObra(str, Enum):
    STOCK_CRITICO = "STOCK_CRITICO"
    OBRA_RETRASADA = "OBRA_RETRASADA"
    SOBRECOSTO = "SOBRECOSTO"
    URGENTE_SIN_STOCK = "URGENTE_SIN_STOCK"
    ALTO_VALOR_SUSPENDIDA = "ALTO_VALOR_SUSPENDIDA"
    BAJA_EFICIENCIA = "BAJA_EFICIENCIA"
    PRODUCTO_FALTANTE = "PRODUCTO_FALTANTE"

class MetricaObra(str, Enum):
    EFICIENCIA_DESPACHO = "EFICIENCIA_DESPACHO"
    MARGEN_GANANCIA = "MARGEN_GANANCIA"
    PORCENTAJE_COMPLETADO = "PORCENTAJE_COMPLETADO"
    VALOR_TOTAL = "VALOR_TOTAL"
    DIAS_RETRASO = "DIAS_RETRASO"
    CALIFICACION_RIESGO = "CALIFICACION_RIESGO"

# Schema para exportación de obras
class ExportObrasCompleto(BaseModel):
    fecha_exportacion: datetime
    total_registros: int
    criterios_filtro: Optional[dict] = None
    obras: List[ObrasInventarioCompleto]
    resumen_estadisticas: EstadisticasObras
    alertas_incluidas: List[AlertaObra]


# ========================================
# SCHEMAS PARA DEVOLUCIONES PENDIENTES
# ========================================

# Enums para devoluciones pendientes
class EstadoDevolucion(str, Enum):
    VENCIDA = "VENCIDA"
    URGENTE = "URGENTE"
    PROXIMO_VENCIMIENTO = "PROXIMO_VENCIMIENTO"
    EN_PLAZO = "EN_PLAZO"
    SIN_FECHA_LIMITE = "SIN_FECHA_LIMITE"

class CriticidadDevolucion(str, Enum):
    CRITICA = "CRITICA"
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"

class CategoriaValorDevolucion(str, Enum):
    MUY_ALTO = "MUY_ALTO"
    ALTO = "ALTO"
    MEDIO = "MEDIO"
    BAJO = "BAJO"
    MINIMO = "MINIMO"

class TipoAlertaDevolucion(str, Enum):
    DEVOLUCION_VENCIDA = "DEVOLUCION_VENCIDA"
    DEVOLUCION_URGENTE = "DEVOLUCION_URGENTE"
    ALTO_VALOR_PENDIENTE = "ALTO_VALOR_PENDIENTE"
    MUCHOS_PRODUCTOS_PENDIENTES = "MUCHOS_PRODUCTOS_PENDIENTES"
    SEGUIMIENTO_NORMAL = "SEGUIMIENTO_NORMAL"

# Schema principal para lectura de devoluciones pendientes
class VistaDevolucionesPendientesRead(BaseModel):
    id_despacho: int
    numero_despacho: str
    codigo_obra: str
    nombre_obra: str
    fecha_despacho: date
    fecha_limite_devolucion: Optional[date] = None
    dias_para_limite: Optional[int] = None
    productos_diferentes: int
    cantidad_pendiente_devolucion: float
    valor_pendiente: Decimal
    # Propiedades calculadas
    esta_vencida: Optional[bool] = None
    estado_devolucion: Optional[str] = None
    nivel_criticidad: Optional[str] = None
    categoria_valor: Optional[str] = None
    requiere_atencion_inmediata: Optional[bool] = None
    porcentaje_tiempo_transcurrido: Optional[float] = None
    alerta_generada: Optional[str] = None
    valor_promedio_por_producto: Optional[float] = None
    cantidad_promedio_por_producto: Optional[float] = None
    indicador_urgencia: Optional[int] = None
    resumen_estado: Optional[str] = None
    acciones_recomendadas: Optional[List[str]] = None

    class Config:
        from_attributes = True

# Schema para filtros de devoluciones pendientes
class VistaDevolucionesPendientesFilter(BaseModel):
    id_despacho: Optional[int] = None
    numero_despacho: Optional[str] = None
    codigo_obra: Optional[str] = None
    fecha_despacho_desde: Optional[date] = None
    fecha_despacho_hasta: Optional[date] = None
    fecha_limite_desde: Optional[date] = None
    fecha_limite_hasta: Optional[date] = None
    dias_para_limite_min: Optional[int] = None
    dias_para_limite_max: Optional[int] = None
    estado_devolucion: Optional[EstadoDevolucion] = None
    criticidad: Optional[CriticidadDevolucion] = None
    categoria_valor: Optional[CategoriaValorDevolucion] = None
    valor_pendiente_min: Optional[Decimal] = None
    valor_pendiente_max: Optional[Decimal] = None
    productos_min: Optional[int] = None
    productos_max: Optional[int] = None
    solo_vencidas: Optional[bool] = None
    solo_urgentes: Optional[bool] = None
    solo_atencion_inmediata: Optional[bool] = None

# Schema para estadísticas de devoluciones pendientes
class EstadisticasDevolucionesPendientes(BaseModel):
    total_devoluciones: int
    total_valor_pendiente: Decimal
    total_productos_pendientes: int
    total_cantidad_pendiente: float
    devoluciones_vencidas: int
    devoluciones_urgentes: int
    devoluciones_en_plazo: int
    valor_promedio_devolucion: Decimal
    productos_promedio_devolucion: float
    porcentaje_vencidas: float
    porcentaje_urgentes: float

# Schema para alertas de devoluciones
class AlertaDevolucionPendiente(BaseModel):
    id_despacho: int
    numero_despacho: str
    codigo_obra: str
    nombre_obra: str
    tipo_alerta: TipoAlertaDevolucion
    nivel_criticidad: CriticidadDevolucion
    descripcion: str
    valor_pendiente: Decimal
    dias_para_limite: Optional[int] = None
    fecha_limite: Optional[date] = None
    acciones_recomendadas: List[str]
    fecha_generacion: datetime

# Schema para ranking de devoluciones por valor
class RankingDevolucionesPorValor(BaseModel):
    posicion: int
    id_despacho: int
    numero_despacho: str
    codigo_obra: str
    nombre_obra: str
    valor_pendiente: Decimal
    productos_diferentes: int
    dias_para_limite: Optional[int] = None
    categoria_valor: str
    porcentaje_del_total: float

# Schema para análisis temporal de devoluciones
class AnalisisTemporalDevoluciones(BaseModel):
    id_despacho: int
    numero_despacho: str
    codigo_obra: str
    dias_desde_despacho: int
    dias_para_limite: Optional[int] = None
    porcentaje_tiempo_transcurrido: float
    tendencia: str  # "VENCIDA", "CRITICA", "NORMAL"
    eficiencia_tiempo: float

# Schema para recomendaciones de devoluciones
class RecomendacionDevolucion(BaseModel):
    id_despacho: int
    numero_despacho: str
    codigo_obra: str
    tipo_recomendacion: str  # "CONTACTAR_CLIENTE", "VISITA_SEGUIMIENTO", "ESCALAR_GERENCIA"
    prioridad: CriticidadDevolucion
    descripcion: str
    acciones_sugeridas: List[str]
    impacto_estimado: str
    plazo_recomendado: str

# Schema para dashboard de devoluciones
class DashboardDevoluciones(BaseModel):
    resumen_general: EstadisticasDevolucionesPendientes
    devoluciones_criticas: List[VistaDevolucionesPendientesRead]
    alertas_activas: List[AlertaDevolucionPendiente]
    ranking_por_valor: List[RankingDevolucionesPorValor]
    devoluciones_vencen_hoy: List[VistaDevolucionesPendientesRead]
    analisis_temporal: List[AnalisisTemporalDevoluciones]

# Schema para exportación de devoluciones
class ExportDevolucionesCompleto(BaseModel):
    fecha_exportacion: datetime
    total_registros: int
    criterios_filtro: Optional[dict] = None
    devoluciones: List[VistaDevolucionesPendientesRead]
    resumen_estadisticas: EstadisticasDevolucionesPendientes
    alertas_incluidas: List[AlertaDevolucionPendiente]


# ========================================
# SCHEMAS PARA PRODUCTOS ABC
# ========================================

# Enums para análisis ABC de productos
class ClasificacionABC(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    SIN_MOVIMIENTO = "SIN_MOVIMIENTO"
    POR_CLASIFICAR = "POR_CLASIFICAR"

class CategoriaValorInventario(str, Enum):
    MUY_ALTO = "MUY_ALTO"
    ALTO = "ALTO"
    MEDIO = "MEDIO"
    BAJO = "BAJO"
    MINIMO = "MINIMO"

class CategoriaRotacion(str, Enum):
    MUY_ALTA = "MUY_ALTA"
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"
    SIN_ROTACION = "SIN_ROTACION"

class CriticidadProducto(str, Enum):
    CRITICA = "CRITICA"
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    NORMAL = "NORMAL"
    BAJA = "BAJA"

class AccionRecomendada(str, Enum):
    REPOSICION_URGENTE = "REPOSICION_URGENTE"
    AUMENTAR_STOCK_MINIMO = "AUMENTAR_STOCK_MINIMO"
    REVISAR_DEMANDA = "REVISAR_DEMANDA"
    MANTENER_SEGUIMIENTO = "MANTENER_SEGUIMIENTO"
    PROGRAMAR_REPOSICION = "PROGRAMAR_REPOSICION"
    EVALUAR_DESCONTINUAR = "EVALUAR_DESCONTINUAR"
    SEGUIMIENTO_PERIODICO = "SEGUIMIENTO_PERIODICO"
    CONSIDERAR_LIQUIDACION = "CONSIDERAR_LIQUIDACION"
    MANTENER_STOCK_MINIMO = "MANTENER_STOCK_MINIMO"
    REVISAR_NECESIDAD = "REVISAR_NECESIDAD"
    EVALUAR_LIQUIDACION = "EVALUAR_LIQUIDACION"
    CONSIDERAR_DESCONTINUAR = "CONSIDERAR_DESCONTINUAR"

class ImpactoFinanciero(str, Enum):
    MUY_ALTO = "MUY_ALTO"
    ALTO = "ALTO"
    MEDIO = "MEDIO"
    BAJO = "BAJO"
    NULO = "NULO"

# Schema principal para lectura de productos ABC
class VistaProductosABCRead(BaseModel):
    id_producto: int
    sku: str
    nombre_producto: str
    stock_actual: float
    costo_promedio: Decimal
    valor_inventario: Decimal
    movimientos_anuales: float
    clasificacion_abc: str
    # Propiedades calculadas
    rotacion_inventario: Optional[float] = None
    valor_movimiento_anual: Optional[float] = None
    clasificacion_abc_calculada: Optional[str] = None
    categoria_valor_inventario: Optional[str] = None
    categoria_rotacion: Optional[str] = None
    requiere_atencion: Optional[bool] = None
    nivel_criticidad: Optional[str] = None
    recomendacion_accion: Optional[str] = None
    dias_inventario: Optional[float] = None
    punto_reorden_sugerido: Optional[float] = None
    stock_maximo_sugerido: Optional[float] = None
    impacto_financiero: Optional[str] = None
    indicador_obsolescencia: Optional[float] = None
    acciones_recomendadas: Optional[List[str]] = None

    class Config:
        from_attributes = True

# Schema para filtros de productos ABC
class VistaProductosABCFilter(BaseModel):
    id_producto: Optional[int] = None
    sku: Optional[str] = None
    nombre_producto: Optional[str] = None
    clasificacion_abc: Optional[ClasificacionABC] = None
    categoria_valor: Optional[CategoriaValorInventario] = None
    categoria_rotacion: Optional[CategoriaRotacion] = None
    criticidad: Optional[CriticidadProducto] = None
    accion_recomendada: Optional[AccionRecomendada] = None
    impacto_financiero: Optional[ImpactoFinanciero] = None
    stock_actual_min: Optional[float] = None
    stock_actual_max: Optional[float] = None
    valor_inventario_min: Optional[Decimal] = None
    valor_inventario_max: Optional[Decimal] = None
    movimientos_anuales_min: Optional[float] = None
    movimientos_anuales_max: Optional[float] = None
    rotacion_min: Optional[float] = None
    rotacion_max: Optional[float] = None
    dias_inventario_min: Optional[float] = None
    dias_inventario_max: Optional[float] = None
    obsolescencia_min: Optional[float] = None
    obsolescencia_max: Optional[float] = None
    solo_requieren_atencion: Optional[bool] = None
    solo_sin_stock: Optional[bool] = None
    solo_sin_movimiento: Optional[bool] = None

# Schema para estadísticas de productos ABC
class EstadisticasProductosABC(BaseModel):
    total_productos: int
    total_valor_inventario: Decimal
    total_movimientos_anuales: float
    promedio_rotacion: float
    productos_clase_a: int
    productos_clase_b: int
    productos_clase_c: int
    productos_sin_movimiento: int
    valor_clase_a: Decimal
    valor_clase_b: Decimal
    valor_clase_c: Decimal
    valor_sin_movimiento: Decimal
    porcentaje_valor_a: float
    porcentaje_valor_b: float
    porcentaje_valor_c: float
    porcentaje_sin_movimiento: float
    productos_requieren_atencion: int
    productos_obsolescencia_alta: int

# Schema para ranking ABC por valor
class RankingProductosABCValor(BaseModel):
    posicion: int
    id_producto: int
    sku: str
    nombre_producto: str
    clasificacion_abc: str
    valor_inventario: Decimal
    valor_movimiento_anual: float
    rotacion_inventario: float
    porcentaje_del_total: float

# Schema para análisis de obsolescencia
class AnalisisObsolescencia(BaseModel):
    id_producto: int
    sku: str
    nombre_producto: str
    valor_inventario: Decimal
    movimientos_anuales: float
    dias_inventario: float
    indicador_obsolescencia: float
    nivel_riesgo: str  # "ALTO", "MEDIO", "BAJO"
    acciones_sugeridas: List[str]
    impacto_financiero: str

# Schema para recomendaciones ABC
class RecomendacionProductoABC(BaseModel):
    id_producto: int
    sku: str
    nombre_producto: str
    clasificacion_abc: str
    tipo_recomendacion: AccionRecomendada
    prioridad: CriticidadProducto
    descripcion: str
    acciones_sugeridas: List[str]
    impacto_estimado: str
    punto_reorden_sugerido: float
    stock_maximo_sugerido: float

# Schema para alertas de productos ABC
class AlertaProductoABC(BaseModel):
    id_producto: int
    sku: str
    nombre_producto: str
    tipo_alerta: str  # "SIN_STOCK_CLASE_A", "OBSOLESCENCIA_ALTA", "ROTACION_CRITICA"
    nivel_criticidad: CriticidadProducto
    descripcion: str
    valor_afectado: Decimal
    acciones_recomendadas: List[str]
    fecha_generacion: datetime

# Schema para dashboard ABC
class DashboardProductosABC(BaseModel):
    resumen_general: EstadisticasProductosABC
    productos_criticos: List[VistaProductosABCRead]
    alertas_activas: List[AlertaProductoABC]
    ranking_por_valor: List[RankingProductosABCValor]
    productos_obsolescencia: List[AnalisisObsolescencia]
    recomendaciones_principales: List[RecomendacionProductoABC]

# Schema para análisis de rotación
class AnalisisRotacionProductos(BaseModel):
    id_producto: int
    sku: str
    nombre_producto: str
    rotacion_actual: float
    rotacion_optima: float
    dias_inventario: float
    categoria_rotacion: str
    tendencia: str  # "MEJORANDO", "EMPEORANDO", "ESTABLE"
    recomendacion: str

# Schema para optimización de inventario
class OptimizacionInventario(BaseModel):
    id_producto: int
    sku: str
    nombre_producto: str
    stock_actual: float
    stock_optimo: float
    punto_reorden_actual: Optional[float] = None
    punto_reorden_sugerido: float
    stock_maximo_sugerido: float
    ajuste_requerido: float
    tipo_ajuste: str  # "REDUCIR", "AUMENTAR", "MANTENER"
    prioridad_ajuste: str

# Schema para reportes ABC
class ReporteProductosABC(BaseModel):
    fecha_generacion: datetime
    periodo_analisis: str
    resumen_ejecutivo: EstadisticasProductosABC
    clasificacion_detallada: Dict[str, int]
    productos_criticos: List[VistaProductosABCRead]
    oportunidades_mejora: List[str]
    recomendaciones_estrategicas: List[str]
    impacto_financiero_total: Decimal

# Schema para exportación ABC
class ExportProductosABCCompleto(BaseModel):
    fecha_exportacion: datetime
    total_registros: int
    criterios_filtro: Optional[dict] = None
    productos: List[VistaProductosABCRead]
    resumen_estadisticas: EstadisticasProductosABC
    analisis_obsolescencia: List[AnalisisObsolescencia]
    recomendaciones: List[RecomendacionProductoABC]
