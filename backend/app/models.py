from typing import List, Optional
from sqlalchemy import Column, Float, Index, Integer, String, Boolean, Text, TIMESTAMP, Time, func, ForeignKey, DECIMAL, Date, DateTime, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base  # ← IMPORT ABSOLUTO, no relativo
from datetime import datetime

class UnidadMedida(Base):
    __tablename__ = "unidades_medida"
    
    id_unidad = Column(Integer, primary_key=True, index=True)
    codigo_unidad = Column(String(10), unique=True, nullable=False, index=True)
    nombre_unidad = Column(String(50), nullable=False)
    descripcion = Column(String(100))
    activo = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<UnidadMedida(codigo='{self.codigo_unidad}', nombre='{self.nombre_unidad}')>"

class TipoMovimiento(Base):
    __tablename__ = "tipos_movimiento"
    
    id_tipo_movimiento = Column(Integer, primary_key=True, index=True)
    codigo_tipo = Column(String(10), unique=True, nullable=False, index=True)
    nombre_tipo = Column(String(50), nullable=False)
    afecta_stock = Column(String(50), nullable=False)
    requiere_autorizacion= Column(Boolean, nullable=False)
    activo = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<TipoMovimiento(codigo='{self.codigo_tipo}', nombre='{self.nombre_tipo}')>"

class Subcategoria(Base):
    __tablename__ = "subcategorias"

    id_subcategoria = Column(Integer, primary_key=True, index=True)
    id_categoria = Column(Integer, ForeignKey("categorias.id_categoria"), nullable=False)
    codigo_subcategoria = Column(String(10), unique=True, nullable=False)
    nombre_subcategoria = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)

    categoria = relationship("Categoria", back_populates="subcategorias")

    def __repr__(self):
        return f"<Subcategoria(id={self.id_subcategoria}, nombre={self.codigo_subcategoria})>"
    

class Categoria(Base):
    __tablename__ = 'categorias'

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    codigo_categoria = Column(String(10), nullable=False, unique=True)
    nombre_categoria = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    subcategorias = relationship("Subcategoria", back_populates="categoria")
    programaciones_conteo = relationship("ProgramacionConteos", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(id={self.id_categoria}, nombre={self.nombre_categoria})>"

class TipoProducto(Base):
    __tablename__ = "tipos_producto"

    id_tipo_producto = Column(Integer, primary_key=True, index=True)
    id_subcategoria = Column(Integer, ForeignKey("subcategorias.id_subcategoria"), nullable=False)
    codigo_tipo = Column(String(10), nullable=False, index=True)
    nombre_tipo = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)

    subcategoria = relationship("Subcategoria")

    def __repr__(self):
        return f"<TipoProducto(codigo='{self.codigo_tipo}', nombre='{self.nombre_tipo}')>"

class Marca(Base):
    __tablename__ = "marcas"

    id_marca = Column(Integer, primary_key=True, autoincrement=True)
    nombre_marca = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text)
    pais_origen = Column(String(50))
    sitio_web = Column(String(200))
    contacto_tecnico = Column(String(200))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<Marca(id={self.id_marca}, nombre='{self.nombre_marca}')>"

class Proveedor(Base):
    __tablename__ = "proveedores"

    id_proveedor = Column(Integer, primary_key=True, autoincrement=True)
    codigo_proveedor = Column(String(20), nullable=False, unique=True)
    nombre_proveedor = Column(String(200), nullable=False)
    razon_social = Column(String(200))
    rfc = Column(String(20))
    direccion = Column(Text)
    ciudad = Column(String(100))
    estado = Column(String(50))
    codigo_postal = Column(String(10))
    pais = Column(String(50), default='México')
    telefono = Column(String(20))
    email = Column(String(100))
    contacto_principal = Column(String(100))
    dias_credito = Column(Integer, default=0)
    limite_credito = Column(DECIMAL(15,2), default=0)
    descuento_general = Column(DECIMAL(5,2), default=0)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relación con sucursales
    sucursales = relationship("SucursalProveedor", back_populates="proveedor")

    def __repr__(self):
        return f"<Proveedor(id={self.id_proveedor}, codigo='{self.codigo_proveedor}', nombre='{self.nombre_proveedor}')>"

class SucursalProveedor(Base):
    __tablename__ = "sucursales_proveedor"

    id_sucursal = Column(Integer, primary_key=True, autoincrement=True)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id_proveedor"), nullable=False)
    codigo_sucursal = Column(String(20), nullable=False)
    nombre_sucursal = Column(String(200), nullable=False)
    direccion = Column(Text)
    ciudad = Column(String(100))
    estado = Column(String(50))
    codigo_postal = Column(String(10))
    pais = Column(String(50), default='Chile')
    telefono = Column(String(20))
    email = Column(String(100))
    contacto = Column(String(100))
    telefono_contacto = Column(String(20))
    email_contacto = Column(String(100))
    es_sucursal_principal = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Índice único para asegurar que el código de sucursal sea único por proveedor
    __table_args__ = (
        UniqueConstraint('id_proveedor', 'codigo_sucursal', name='uq_proveedor_codigo_sucursal'),
    )

    # Relación con proveedor
    proveedor = relationship("Proveedor", back_populates="sucursales")

    def __repr__(self):
        return f"<SucursalProveedor(id={self.id_sucursal}, codigo='{self.codigo_sucursal}', nombre='{self.nombre_sucursal}')>"

class Bodega(Base):
    __tablename__ = "bodegas"

    id_bodega = Column(Integer, primary_key=True, autoincrement=True)
    codigo_bodega = Column(String(1), nullable=False, unique=True)
    nombre_bodega = Column(String(100), nullable=False)
    descripcion = Column(Text)
    temperatura_min = Column(DECIMAL(5,2))
    temperatura_max = Column(DECIMAL(5,2))
    humedad_max = Column(DECIMAL(5,2))
    requiere_certificacion = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)

    pasillos = relationship("Pasillo", back_populates="bodega")
    programaciones_conteo = relationship("ProgramacionConteos", back_populates="bodega")

    def __repr__(self):
        return f"<Bodega(id={self.id_bodega}, codigo='{self.codigo_bodega}', nombre='{self.nombre_bodega}')>"

class Pasillo(Base):
    __tablename__ = "pasillos"

    id_pasillo = Column(Integer, primary_key=True, autoincrement=True)
    id_bodega = Column(Integer, ForeignKey("bodegas.id_bodega"), nullable=False)
    numero_pasillo = Column(Integer, nullable=False)
    nombre_pasillo = Column(String(50))
    longitud_metros = Column(DECIMAL(6,2))
    activo = Column(Boolean, default=True)

    bodega = relationship("Bodega", back_populates="pasillos")
    estantes = relationship("Estante", back_populates="pasillo")

    def __repr__(self):
        return f"<Pasillo(id={self.id_pasillo}, bodega_id={self.id_bodega}, numero={self.numero_pasillo})>"

class Estante(Base):
    __tablename__ = "estantes"

    id_estante = Column(Integer, primary_key=True, autoincrement=True)
    id_pasillo = Column(Integer, ForeignKey("pasillos.id_pasillo"), nullable=False)
    codigo_estante = Column(String(5), nullable=False)
    altura_metros = Column(DECIMAL(4,2))
    capacidad_peso_kg = Column(DECIMAL(8,2))
    activo = Column(Boolean, default=True)

    pasillo = relationship("Pasillo", back_populates="estantes")
    niveles = relationship("Nivel", back_populates="estante")

    def __repr__(self):
        return f"<Estante(id={self.id_estante}, pasillo_id={self.id_pasillo}, codigo='{self.codigo_estante}')>"

class Nivel(Base):
    __tablename__ = "niveles"

    id_nivel = Column(Integer, primary_key=True, autoincrement=True)
    id_estante = Column(Integer, ForeignKey("estantes.id_estante"), nullable=False)
    numero_nivel = Column(Integer, nullable=False)
    altura_cm = Column(DECIMAL(6,2))
    capacidad_peso_kg = Column(DECIMAL(8,2))
    activo = Column(Boolean, default=True)

    estante = relationship("Estante", back_populates="niveles")

    def __repr__(self):
        return f"<Nivel(id={self.id_nivel}, estante_id={self.id_estante}, numero={self.numero_nivel})>"

class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(50), nullable=False, unique=True, index=True)
    nombre_producto = Column(String(200), nullable=False, index=True)
    descripcion_corta = Column(String(500))
    descripcion_detallada = Column(Text)
    id_marca = Column(Integer, ForeignKey("marcas.id_marca"))
    modelo = Column(String(100))
    numero_parte = Column(String(100))
    id_tipo_producto = Column(Integer, ForeignKey("tipos_producto.id_tipo_producto"), nullable=False, index=True)
    id_unidad_medida = Column(Integer, ForeignKey("unidades_medida.id_unidad"), nullable=False)

    # Especificaciones técnicas generales
    peso_kg = Column(DECIMAL(8,3))
    dimensiones_largo_cm = Column(DECIMAL(8,2))
    dimensiones_ancho_cm = Column(DECIMAL(8,2))
    dimensiones_alto_cm = Column(DECIMAL(8,2))
    material_principal = Column(String(100))
    color = Column(String(50))

    # Información para sistemas contra incendios
    presion_trabajo_bar = Column(DECIMAL(6,2))
    presion_maxima_bar = Column(DECIMAL(6,2))
    temperatura_min_celsius = Column(DECIMAL(6,2))
    temperatura_max_celsius = Column(DECIMAL(6,2))
    temperatura_activacion_celsius = Column(DECIMAL(6,2))
    factor_k = Column(DECIMAL(6,3))  # Para rociadores
    conexion_entrada = Column(String(50))
    conexion_salida = Column(String(50))

    # Certificaciones y normativas
    certificacion_ul = Column(String(50))
    certificacion_fm = Column(String(50))
    certificacion_nfpa = Column(String(100))
    otras_certificaciones = Column(Text)

    # Control de inventario
    stock_actual = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=0)
    stock_maximo = Column(Integer, default=0)
    punto_reorden = Column(Integer, default=0)
    lead_time_dias = Column(Integer, default=0)

    # Información comercial
    costo_promedio = Column(DECIMAL(15,4), default=0)
    precio_venta = Column(DECIMAL(15,2), default=0)
    margen_ganancia = Column(DECIMAL(5,2), default=0)

    # Control de calidad y almacenamiento
    requiere_refrigeracion = Column(Boolean, default=False)
    vida_util_meses = Column(Integer)
    condiciones_almacenamiento = Column(Text)
    manejo_especial = Column(Text)

    # Control del sistema
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    usuario_creacion = Column(Integer)
    usuario_modificacion = Column(Integer)

    # Relaciones
    marca = relationship("Marca")
    tipo_producto = relationship("TipoProducto")
    unidad_medida = relationship("UnidadMedida")
    producto_proveedores = relationship("ProductoProveedor", back_populates="producto")
    lotes = relationship("Lote", back_populates="producto")
    numeros_serie = relationship("NumeroSerie", back_populates="producto")
    despachos_detalle = relationship("DespachosObraDetalle", back_populates="producto")
    devoluciones_detalle = relationship("DevolucionesObraDetalle", back_populates="producto")
    inventario_obras = relationship("InventarioObra", back_populates="producto")
    reservas = relationship("Reservas", back_populates="producto")
    conteos_fisicos = relationship("ConteosFisicos", back_populates="producto")
    logs_alertas = relationship("LogAlertas", back_populates="producto")

    def __repr__(self):
        return f"<Producto(id={self.id_producto}, sku='{self.sku}', nombre='{self.nombre_producto}')>"

class ProductoProveedor(Base):
    __tablename__ = "producto_proveedores"

    id_producto_proveedor = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id_proveedor"), nullable=False)
    es_principal = Column(Boolean, default=False)
    codigo_proveedor_producto = Column(String(100))
    costo_actual = Column(DECIMAL(15,4))
    descuento_producto = Column(DECIMAL(5,2), default=0)
    tiempo_entrega_dias = Column(Integer, default=0)
    cantidad_minima_orden = Column(Integer, default=1)
    activo = Column(Boolean, default=True)
    fecha_vigencia_desde = Column(Date)
    fecha_vigencia_hasta = Column(Date)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relaciones
    producto = relationship("Producto", back_populates="producto_proveedores")
    proveedor = relationship("Proveedor")

    def __repr__(self):
        return f"<ProductoProveedor(id={self.id_producto_proveedor}, producto_id={self.id_producto}, proveedor_id={self.id_proveedor})>"

# ========================================
# MODELOS PARA UBICACIONES E INVENTARIO
# ========================================

class ProductoUbicacion(Base):
    __tablename__ = "producto_ubicaciones"

    id_ubicacion = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False, index=True)
    id_nivel = Column(Integer, ForeignKey("niveles.id_nivel"), nullable=False, index=True)
    cantidad = Column(Integer, nullable=False, default=0)
    cantidad_reservada = Column(Integer, default=0)
    posicion_especifica = Column(String(20))
    fecha_ultima_conteo = Column(Date)
    observaciones = Column(Text)
    activo = Column(Boolean, default=True)

    # Relaciones
    producto = relationship("Producto")
    nivel = relationship("Nivel")

    def __repr__(self):
        return f"<ProductoUbicacion(id={self.id_ubicacion}, producto_id={self.id_producto}, nivel_id={self.id_nivel}, cantidad={self.cantidad})>"

class DocumentoMovimiento(Base):
    __tablename__ = "documentos_movimiento"

    id_documento = Column(Integer, primary_key=True, autoincrement=True)
    tipo_documento = Column(String(20), nullable=False)
    numero_documento = Column(String(50), nullable=False)
    fecha_documento = Column(Date, nullable=False)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id_proveedor"))
    total_documento = Column(DECIMAL(15,2))
    observaciones = Column(Text)
    ruta_archivo = Column(String(500))
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relaciones
    proveedor = relationship("Proveedor")
    movimientos = relationship("MovimientoInventario", back_populates="documento")

    def __repr__(self):
        return f"<DocumentoMovimiento(id={self.id_documento}, tipo='{self.tipo_documento}', numero='{self.numero_documento}')>"

class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id_movimiento = Column(Integer, primary_key=True, autoincrement=True)
    id_tipo_movimiento = Column(Integer, ForeignKey("tipos_movimiento.id_tipo_movimiento"), nullable=False)
    numero_movimiento = Column(String(50), nullable=False, index=True)
    fecha_movimiento = Column(DateTime, nullable=False, server_default=func.current_timestamp(), index=True)
    id_documento = Column(Integer, ForeignKey("documentos_movimiento.id_documento"))
    id_usuario = Column(Integer, nullable=False)
    motivo = Column(Text)
    observaciones = Column(Text)
    autorizado_por = Column(Integer)
    fecha_autorizacion = Column(DateTime)
    estado = Column(
        Enum('PENDIENTE', 'AUTORIZADO', 'PROCESADO', 'CANCELADO', name='estado_movimiento'),
        default='PENDIENTE',
        index=True
    )

    # Relaciones
    tipo_movimiento = relationship("TipoMovimiento")
    documento = relationship("DocumentoMovimiento", back_populates="movimientos")
    detalles = relationship("MovimientoDetalle", back_populates="movimiento")

    def __repr__(self):
        return f"<MovimientoInventario(id={self.id_movimiento}, numero='{self.numero_movimiento}', estado='{self.estado}')>"

class MovimientoDetalle(Base):
    __tablename__ = "movimientos_detalle"

    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_movimiento = Column(Integer, ForeignKey("movimientos_inventario.id_movimiento"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    id_ubicacion_origen = Column(Integer, ForeignKey("producto_ubicaciones.id_ubicacion"))
    id_ubicacion_destino = Column(Integer, ForeignKey("producto_ubicaciones.id_ubicacion"))
    cantidad = Column(Integer, nullable=False)
    costo_unitario = Column(DECIMAL(15,4), default=0)
    costo_total = Column(DECIMAL(15,2), default=0)
    observaciones = Column(Text)

    # Relaciones
    movimiento = relationship("MovimientoInventario", back_populates="detalles")
    producto = relationship("Producto")
    ubicacion_origen = relationship("ProductoUbicacion", foreign_keys=[id_ubicacion_origen])
    ubicacion_destino = relationship("ProductoUbicacion", foreign_keys=[id_ubicacion_destino])

    def __repr__(self):
        return f"<MovimientoDetalle(id={self.id_detalle}, movimiento_id={self.id_movimiento}, producto_id={self.id_producto}, cantidad={self.cantidad})>"


# ========================================
# MODELOS DE LOTES Y NÚMEROS DE SERIE
# ========================================

class Lote(Base):
    __tablename__ = "lotes"

    id_lote = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    numero_lote = Column(String(50), nullable=False)
    fecha_fabricacion = Column(Date)
    fecha_vencimiento = Column(Date)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id_proveedor"))
    cantidad_inicial = Column(Integer, nullable=False)
    cantidad_actual = Column(Integer, nullable=False)
    costo_promedio = Column(DECIMAL(15,4))
    certificado_calidad = Column(String(500))  # Ruta del archivo
    observaciones = Column(Text)
    estado = Column(Enum('ACTIVO', 'VENCIDO', 'CUARENTENA', 'AGOTADO'), default='ACTIVO')
    fecha_creacion = Column(TIMESTAMP, default=func.current_timestamp())

    # Índices únicos
    __table_args__ = (
        UniqueConstraint('id_producto', 'numero_lote', name='unique_producto_lote'),
        Index('idx_lote_producto', 'id_producto'),
        Index('idx_lote_proveedor', 'id_proveedor'),
        Index('idx_lote_estado', 'estado'),
        Index('idx_lote_fecha_vencimiento', 'fecha_vencimiento'),
    )

    # Relaciones
    producto = relationship("Producto", back_populates="lotes")
    proveedor = relationship("Proveedor")
    numeros_serie = relationship("NumeroSerie", back_populates="lote")
    despachos_detalle = relationship("DespachosObraDetalle", back_populates="lote")
    devoluciones_detalle = relationship("DevolucionesObraDetalle", back_populates="lote")

    def __repr__(self):
        return f"<Lote(id={self.id_lote}, numero={self.numero_lote}, producto_id={self.id_producto}, estado={self.estado})>"


class NumeroSerie(Base):
    __tablename__ = "numeros_serie"

    id_serie = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    numero_serie = Column(String(100), nullable=False)
    id_lote = Column(Integer, ForeignKey("lotes.id_lote"))
    fecha_ingreso = Column(Date, nullable=False)
    id_ubicacion = Column(Integer, ForeignKey("producto_ubicaciones.id_ubicacion"))
    estado = Column(Enum('DISPONIBLE', 'RESERVADO', 'VENDIDO', 'DEFECTUOSO', 'EN_REPARACION'), default='DISPONIBLE')
    cliente_asignado = Column(String(200))
    fecha_venta = Column(Date)
    observaciones = Column(Text)

    # Índices únicos
    __table_args__ = (
        UniqueConstraint('id_producto', 'numero_serie', name='unique_producto_serie'),
        Index('idx_serie_producto', 'id_producto'),
        Index('idx_serie_lote', 'id_lote'),
        Index('idx_serie_ubicacion', 'id_ubicacion'),
        Index('idx_serie_estado', 'estado'),
    )

    # Relaciones
    producto = relationship("Producto", back_populates="numeros_serie")
    lote = relationship("Lote", back_populates="numeros_serie")
    ubicacion = relationship("ProductoUbicacion")

    def __repr__(self):
        return f"<NumeroSerie(id={self.id_serie}, numero={self.numero_serie}, producto_id={self.id_producto}, estado={self.estado})>"


# ========================================
# MODELO DE CLIENTES
# ========================================

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    codigo_cliente = Column(String(20), nullable=False, unique=True, index=True)
    nombre_cliente = Column(String(200), nullable=False, index=True)
    razon_social = Column(String(200))
    rfc = Column(String(20))
    direccion = Column(Text)
    ciudad = Column(String(100))
    estado = Column(String(50))
    codigo_postal = Column(String(10))
    pais = Column(String(50), default='México')
    telefono = Column(String(20))
    email = Column(String(100))
    contacto_principal = Column(String(100))
    tipo_cliente = Column(Enum('GOBIERNO', 'PRIVADO', 'CONSTRUCTORA', 'DISTRIBUIDOR'), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Índices
    __table_args__ = (
        Index('idx_cliente_codigo', 'codigo_cliente'),
        Index('idx_cliente_nombre', 'nombre_cliente'),
        Index('idx_cliente_tipo', 'tipo_cliente'),
        Index('idx_cliente_activo', 'activo'),
        Index('idx_cliente_ciudad', 'ciudad'),
        Index('idx_cliente_estado', 'estado'),
    )

    # Relaciones
    obras = relationship("Obra", back_populates="cliente")
    reservas = relationship("Reservas", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(id={self.id_cliente}, codigo='{self.codigo_cliente}', nombre='{self.nombre_cliente}', tipo={self.tipo_cliente})>"


# ========================================
# MODELO DE OBRAS
# ========================================

class Obra(Base):
    __tablename__ = "obras"

    id_obra = Column(Integer, primary_key=True, autoincrement=True)
    codigo_obra = Column(String(50), nullable=False, unique=True, index=True)
    nombre_obra = Column(String(200), nullable=False, index=True)
    descripcion = Column(Text)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False, index=True)
    direccion_obra = Column(Text)
    ciudad = Column(String(100))
    codigo_postal = Column(String(10))

    # Responsables
    supervisor_obra = Column(String(100))
    contacto_obra = Column(String(100))
    telefono_obra = Column(String(20))

    # Fechas del proyecto
    fecha_inicio_programada = Column(Date)
    fecha_fin_programada = Column(Date)
    fecha_inicio_real = Column(Date)
    fecha_fin_real = Column(Date)

    # Control financiero
    valor_contrato = Column(DECIMAL(15,2))
    moneda = Column(String(10), default='MXN')

    # Control de inventario
    requiere_devolucion_sobrantes = Column(Boolean, default=True)
    dias_limite_devolucion = Column(Integer, default=30)
    porcentaje_merma_permitida = Column(DECIMAL(5,2), default=5.00)

    # Estado y control
    estado = Column(Enum('PLANIFICACION', 'EN_EJECUCION', 'SUSPENDIDA', 'FINALIZADA', 'CANCELADA'), default='PLANIFICACION')
    prioridad = Column(Enum('BAJA', 'MEDIA', 'ALTA', 'CRITICA'), default='MEDIA')
    observaciones = Column(Text)
    activo = Column(Boolean, default=True)

    fecha_creacion = Column(TIMESTAMP, default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    usuario_creacion = Column(Integer)
    usuario_modificacion = Column(Integer)

    # Índices
    __table_args__ = (
        Index('idx_cliente_obra', 'id_cliente'),
        Index('idx_estado_obra', 'estado'),
        Index('idx_codigo_obra', 'codigo_obra'),
        Index('idx_obra_fechas', 'fecha_inicio_programada', 'fecha_fin_programada'),
        Index('idx_obra_prioridad', 'prioridad'),
        Index('idx_obra_activo', 'activo'),
    )

    # Relaciones
    cliente = relationship("Cliente", back_populates="obras")
    almacen_obra = relationship("AlmacenObra", back_populates="obra", uselist=False)
    despachos = relationship("DespachosObra", back_populates="obra")
    devoluciones = relationship("DevolucionesObra", back_populates="obra")
    inventario = relationship("InventarioObra", back_populates="obra")
    reservas = relationship("Reservas", back_populates="obra")
    programaciones_conteo = relationship("ProgramacionConteos", back_populates="obra")
    conteos_fisicos = relationship("ConteosFisicos", back_populates="obra")
    logs_alertas = relationship("LogAlertas", back_populates="obra")

    def __repr__(self):
        return f"<Obra(id={self.id_obra}, codigo='{self.codigo_obra}', nombre='{self.nombre_obra}', estado={self.estado})>"


# ========================================
# MODELO DE ALMACÉN DE OBRA
# ========================================

class AlmacenObra(Base):
    __tablename__ = "almacen_obra"

    id_almacen_obra = Column(Integer, primary_key=True, autoincrement=True)
    id_obra = Column(Integer, ForeignKey("obras.id_obra"), nullable=False, unique=True, index=True)
    nombre_almacen = Column(String(100), nullable=False)
    descripcion = Column(Text)
    direccion = Column(Text)
    responsable = Column(String(100))
    telefono = Column(String(20))

    # Condiciones del almacén
    tiene_seguridad = Column(Boolean, default=False)
    tiene_techo = Column(Boolean, default=True)
    capacidad_m3 = Column(DECIMAL(10,2))
    observaciones = Column(Text)

    activo = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=func.current_timestamp())

    # Índices
    __table_args__ = (
        Index('idx_obra_almacen', 'id_obra'),
    )

    # Relaciones
    obra = relationship("Obra", back_populates="almacen_obra")

    def __repr__(self):
        return f"<AlmacenObra(id={self.id_almacen_obra}, obra_id={self.id_obra}, nombre='{self.nombre_almacen}')>"


# ========================================
# MODELO DE DESPACHOS DE OBRA
# ========================================

class DespachosObra(Base):
    __tablename__ = "despachos_obra"

    id_despacho = Column(Integer, primary_key=True, autoincrement=True)
    numero_despacho = Column(String(50), nullable=False, unique=True, index=True)
    id_obra = Column(Integer, ForeignKey("obras.id_obra"), nullable=False, index=True)
    fecha_despacho = Column(Date, nullable=False)

    # Transporte
    transportista = Column(String(100))
    vehiculo = Column(String(50))
    chofer = Column(String(100))

    # Entrega
    id_usuario_despacha = Column(Integer, nullable=False)
    recibido_por = Column(String(100))
    fecha_entrega = Column(Date)
    hora_entrega = Column(Time)

    # Control
    requiere_devolucion = Column(Boolean, default=True)
    fecha_limite_devolucion = Column(Date)
    motivo_despacho = Column(Text)
    observaciones = Column(Text)

    estado = Column(Enum("PREPARADO", "EN_TRANSITO", "ENTREGADO", "DEVOLUCION_PARCIAL", "DEVOLUCION_COMPLETA", "CERRADO", name="estado_despacho"), default="PREPARADO")

    fecha_creacion = Column(TIMESTAMP, default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Índices
    __table_args__ = (
        Index('idx_obra_despacho', 'id_obra'),
        Index('idx_estado_despacho', 'estado'),
        Index('idx_fecha_limite_devolucion', 'fecha_limite_devolucion'),
    )

    # Relaciones
    obra = relationship("Obra", back_populates="despachos")
    detalles = relationship("DespachosObraDetalle", back_populates="despacho")
    devoluciones = relationship("DevolucionesObra", back_populates="despacho")
    logs_alertas = relationship("LogAlertas", back_populates="despacho")

    def __repr__(self):
        return f"<DespachosObra(id={self.id_despacho}, numero='{self.numero_despacho}', obra_id={self.id_obra}, estado={self.estado})>"


# ========================================
# MODELO DE DETALLE DE DESPACHOS DE OBRA
# ========================================

class DespachosObraDetalle(Base):
    __tablename__ = "despachos_obra_detalle"

    id_despacho_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_despacho = Column(Integer, ForeignKey("despachos_obra.id_despacho"), nullable=False, index=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False, index=True)
    cantidad_despachada = Column(Integer, nullable=False)
    cantidad_utilizada = Column(Integer, default=0)
    cantidad_devuelta = Column(Integer, default=0)
    cantidad_perdida = Column(Integer, default=0)

    # Trazabilidad
    id_lote = Column(Integer, ForeignKey("lotes.id_lote"))
    numeros_serie = Column(Text)

    # Costos
    costo_unitario = Column(DECIMAL(15,4))
    costo_total = Column(DECIMAL(15,2))

    # Para herramientas y equipos
    es_herramienta = Column(Boolean, default=False)
    requiere_devolucion_obligatoria = Column(Boolean, default=False)

    observaciones = Column(Text)

    # Índices
    __table_args__ = (
        Index('idx_despacho_producto', 'id_despacho', 'id_producto'),
        Index('idx_herramientas', 'es_herramienta', 'requiere_devolucion_obligatoria'),
    )

    # Relaciones
    despacho = relationship("DespachosObra", back_populates="detalles")
    producto = relationship("Producto", back_populates="despachos_detalle")
    lote = relationship("Lote", back_populates="despachos_detalle")

    def __repr__(self):
        return f"<DespachosObraDetalle(id={self.id_despacho_detalle}, despacho_id={self.id_despacho}, producto_id={self.id_producto}, cantidad={self.cantidad_despachada})>"


# ========================================
# MODELO DE DEVOLUCIONES DE OBRA
# ========================================

class DevolucionesObra(Base):
    __tablename__ = "devoluciones_obra"

    id_devolucion = Column(Integer, primary_key=True, autoincrement=True)
    numero_devolucion = Column(String(50), nullable=False, unique=True, index=True)
    id_obra = Column(Integer, ForeignKey("obras.id_obra"), nullable=False, index=True)
    id_despacho = Column(Integer, ForeignKey("despachos_obra.id_despacho"), nullable=False, index=True)
    fecha_devolucion = Column(Date, nullable=False)

    # Transporte de devolución
    transportista = Column(String(100))
    vehiculo = Column(String(50))
    chofer = Column(String(100))

    # Recepción
    id_usuario_recibe = Column(Integer, nullable=False)
    entregado_por = Column(String(100))
    fecha_recepcion = Column(Date)
    hora_recepcion = Column(Time)

    # Motivos de devolución
    motivo_devolucion = Column(Enum("FIN_OBRA", "SOBRANTE", "CAMBIO_ESPECIFICACION", "DEFECTUOSO", "NO_UTILIZADO", "DEVOLUCION_HERRAMIENTAS", name="motivo_devolucion"), nullable=False)
    observaciones = Column(Text)

    estado = Column(Enum("EN_TRANSITO", "RECIBIDA", "EN_REVISION", "PROCESADA", "RECHAZADA", name="estado_devolucion"), default="EN_TRANSITO")

    fecha_creacion = Column(TIMESTAMP, default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Índices
    __table_args__ = (
        Index('idx_obra_devolucion', 'id_obra'),
        Index('idx_despacho_devolucion', 'id_despacho'),
        Index('idx_estado_devolucion', 'estado'),
    )

    # Relaciones
    obra = relationship("Obra", back_populates="devoluciones")
    despacho = relationship("DespachosObra", back_populates="devoluciones")
    detalles = relationship("DevolucionesObraDetalle", back_populates="devolucion")

    def __repr__(self):
        return f"<DevolucionesObra(id={self.id_devolucion}, numero='{self.numero_devolucion}', obra_id={self.id_obra}, estado={self.estado})>"


# ========================================
# MODELO DE DETALLE DE DEVOLUCIONES DE OBRA
# ========================================

class DevolucionesObraDetalle(Base):
    __tablename__ = "devoluciones_obra_detalle"

    id_devolucion_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_devolucion = Column(Integer, ForeignKey("devoluciones_obra.id_devolucion"), nullable=False, index=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False, index=True)
    cantidad_devuelta = Column(Integer, nullable=False)

    # Estado del producto devuelto
    estado_producto = Column(Enum("NUEVO", "USADO_BUENO", "USADO_REGULAR", "DEFECTUOSO", "NO_REUTILIZABLE", name="estado_producto_devuelto"), nullable=False)
    requiere_limpieza = Column(Boolean, default=False)
    requiere_reparacion = Column(Boolean, default=False)
    requiere_calibracion = Column(Boolean, default=False)

    # Trazabilidad
    id_lote = Column(Integer, ForeignKey("lotes.id_lote"))
    numeros_serie = Column(Text)

    # Ubicación de recepción
    id_ubicacion_recepcion = Column(Integer, ForeignKey("producto_ubicaciones.id_ubicacion"))

    observaciones = Column(Text)

    # Índices
    __table_args__ = (
        Index('idx_devolucion_producto', 'id_devolucion', 'id_producto'),
    )

    # Relaciones
    devolucion = relationship("DevolucionesObra", back_populates="detalles")
    producto = relationship("Producto", back_populates="devoluciones_detalle")
    lote = relationship("Lote", back_populates="devoluciones_detalle")
    ubicacion_recepcion = relationship("ProductoUbicacion", foreign_keys=[id_ubicacion_recepcion])

    def __repr__(self):
        return f"<DevolucionesObraDetalle(id={self.id_devolucion_detalle}, devolucion_id={self.id_devolucion}, producto_id={self.id_producto}, cantidad={self.cantidad_devuelta})>"


# ========================================
# MODELO DE INVENTARIO DE OBRA
# ========================================

class InventarioObra(Base):
    __tablename__ = "inventario_obra"

    id_inventario_obra = Column(Integer, primary_key=True, autoincrement=True)
    id_obra = Column(Integer, ForeignKey("obras.id_obra"), nullable=False, index=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False, index=True)
    cantidad_actual = Column(Integer, nullable=False, default=0)
    cantidad_utilizada_acumulada = Column(Integer, default=0)
    cantidad_devuelta_acumulada = Column(Integer, default=0)

    # Control de costos
    costo_promedio = Column(DECIMAL(15,4))
    # valor_inventario será calculado en aplicación ya que GENERATED ALWAYS AS no es ampliamente soportado

    # Trazabilidad
    fecha_ultimo_movimiento = Column(DateTime)

    # Para herramientas
    es_herramienta = Column(Boolean, default=False)
    ubicacion_especifica = Column(String(100))
    responsable_herramienta = Column(String(100))

    observaciones = Column(Text)

    # Índices
    __table_args__ = (
        UniqueConstraint('id_obra', 'id_producto', name='unique_obra_producto'),
        Index('idx_obra_producto', 'id_obra', 'id_producto'),
        Index('idx_herramientas_obra', 'id_obra', 'es_herramienta'),
    )

    # Relaciones
    obra = relationship("Obra", back_populates="inventario")
    producto = relationship("Producto", back_populates="inventario_obras")

    @property
    def valor_inventario(self) -> float:
        """Calcula el valor del inventario (cantidad_actual * costo_promedio)"""
        if self.cantidad_actual and self.costo_promedio:
            return float(self.cantidad_actual * self.costo_promedio)
        return 0.0

    def __repr__(self):
        return f"<InventarioObra(id={self.id_inventario_obra}, obra_id={self.id_obra}, producto_id={self.id_producto}, cantidad={self.cantidad_actual})>"


# ========================================
# MODELO DE RESERVAS
# ========================================

class Reservas(Base):
    __tablename__ = "reservas"

    id_reserva = Column(Integer, primary_key=True, autoincrement=True)
    numero_reserva = Column(String(50), nullable=False, unique=True, index=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False, index=True)
    cantidad_reservada = Column(Integer, nullable=False)
    id_ubicacion = Column(Integer, ForeignKey("producto_ubicaciones.id_ubicacion"), nullable=False, index=True)

    # Puede ser para cliente/obra específica o genérica
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    id_obra = Column(Integer, ForeignKey("obras.id_obra"))
    cliente_externo = Column(String(200))
    proyecto_externo = Column(String(200))

    fecha_reserva = Column(DateTime, default=func.current_timestamp())
    fecha_vencimiento_reserva = Column(DateTime)
    motivo_reserva = Column(Text)
    id_usuario = Column(Integer, nullable=False)

    estado = Column(Enum("ACTIVA", "UTILIZADA", "VENCIDA", "CANCELADA", name="estado_reserva"), default="ACTIVA")
    observaciones = Column(Text)

    # Índices
    __table_args__ = (
        Index('idx_fecha_vencimiento', 'fecha_vencimiento_reserva'),
        Index('idx_estado_reserva', 'estado'),
        Index('idx_obra_reserva', 'id_obra'),
    )

    # Relaciones
    producto = relationship("Producto", back_populates="reservas")
    ubicacion = relationship("ProductoUbicacion", foreign_keys=[id_ubicacion])
    cliente = relationship("Cliente", back_populates="reservas")
    obra = relationship("Obra", back_populates="reservas")

    def __repr__(self):
        return f"<Reservas(id={self.id_reserva}, numero='{self.numero_reserva}', producto_id={self.id_producto}, cantidad={self.cantidad_reservada}, estado={self.estado})>"

class ProgramacionConteos(Base):
    __tablename__ = "programacion_conteos"

    id_programacion = Column(Integer, primary_key=True, index=True)
    nombre_conteo = Column(String(100), nullable=False)
    fecha_programada = Column(Date, nullable=False)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)

    # Tipo y alcance del conteo
    tipo_conteo = Column(Enum('COMPLETO', 'CICLICO', 'CATEGORIA', 'BODEGA', 'OBRA', 'ALMACEN_OBRA'), nullable=False)
    id_bodega = Column(Integer, ForeignKey("bodegas.id_bodega"), nullable=True)
    id_categoria = Column(Integer, ForeignKey("categorias.id_categoria"), nullable=True)
    id_obra = Column(Integer, ForeignKey("obras.id_obra"), nullable=True)

    id_usuario_responsable = Column(Integer, nullable=False)
    estado = Column(Enum('PROGRAMADO', 'EN_PROCESO', 'COMPLETADO', 'CANCELADO'), default='PROGRAMADO')
    observaciones = Column(Text, nullable=True)

    # Relaciones
    bodega = relationship("Bodega", back_populates="programaciones_conteo")
    categoria = relationship("Categoria", back_populates="programaciones_conteo")
    obra = relationship("Obra", back_populates="programaciones_conteo")
    conteos_fisicos = relationship("ConteosFisicos", back_populates="programacion")
    # logs = relationship("LogAlertas", back_populates="configuracion_alerta")

    def __repr__(self):
        return f"<ProgramacionConteos(id={self.id_programacion}, nombre='{self.nombre_conteo}', tipo={self.tipo_conteo}, estado={self.estado})>"

class ConteosFisicos(Base):
    __tablename__ = "conteos_fisicos"

    id_conteo = Column(Integer, primary_key=True, index=True)
    id_programacion = Column(Integer, ForeignKey("programacion_conteos.id_programacion"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)

    # Ubicación: puede ser en almacén principal o en obra
    id_ubicacion = Column(Integer, ForeignKey("producto_ubicaciones.id_ubicacion"), nullable=True)
    id_obra = Column(Integer, ForeignKey("obras.id_obra"), nullable=True)

    cantidad_sistema = Column(Integer, nullable=False)
    cantidad_fisica = Column(Integer, nullable=False)
    # La diferencia se calcula automáticamente en la aplicación ya que SQLAlchemy no soporta GENERATED columns directamente

    id_usuario_contador = Column(Integer, nullable=False)
    fecha_conteo = Column(DateTime, default=func.current_timestamp())
    observaciones = Column(Text, nullable=True)

    ajuste_procesado = Column(Boolean, default=False)
    id_movimiento_ajuste = Column(Integer, ForeignKey("movimientos_inventario.id_movimiento"), nullable=True)

    # Relaciones
    programacion = relationship("ProgramacionConteos", back_populates="conteos_fisicos")
    producto = relationship("Producto", back_populates="conteos_fisicos")
    ubicacion = relationship("ProductoUbicacion", foreign_keys=[id_ubicacion])
    obra = relationship("Obra", back_populates="conteos_fisicos")
    movimiento_ajuste = relationship("MovimientoInventario", foreign_keys=[id_movimiento_ajuste])

    @property
    def diferencia(self):
        """Calcular la diferencia entre cantidad física y sistema"""
        return self.cantidad_fisica - self.cantidad_sistema

    def __repr__(self):
        return f"<ConteosFisicos(id={self.id_conteo}, programacion_id={self.id_programacion}, producto_id={self.id_producto}, diferencia={self.diferencia})>"

class ConfiguracionAlertas(Base):
    __tablename__ = "configuracion_alertas"

    id_alerta = Column(Integer, primary_key=True, index=True)
    nombre_alerta = Column(String(100), nullable=False)
    tipo_alerta = Column(Enum(
        'STOCK_MINIMO',
        'VENCIMIENTO',
        'SIN_MOVIMIENTO',
        'CERTIFICACION_VENCIDA',
        'DEVOLUCION_PENDIENTE',
        'OBRA_SIN_ACTIVIDAD',
        'MATERIAL_VENCIDO_EN_OBRA',
        'DESPACHO_NO_ENTREGADO'
    ), nullable=False)
    activa = Column(Boolean, default=True)
    dias_anticipacion = Column(Integer, default=0)
    usuarios_notificar = Column(Text, nullable=True)  # IDs separados por comas
    email_notificar = Column(Text, nullable=True)     # Emails separados por comas
    frecuencia_revision_horas = Column(Integer, default=24)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())

    logs = relationship('LogAlertas', back_populates='configuracion_alerta')

    def get_usuarios_lista(self):
        """Convertir usuarios_notificar de string CSV a lista de enteros"""
        if not self.usuarios_notificar:
            return []
        try:
            return [int(user_id.strip()) for user_id in self.usuarios_notificar.split(',') if user_id.strip()]
        except ValueError:
            return []

    def set_usuarios_lista(self, usuarios_list):
        """Convertir lista de enteros a string CSV para usuarios_notificar"""
        if not usuarios_list:
            self.usuarios_notificar = None
        else:
            self.usuarios_notificar = ','.join(map(str, usuarios_list))

    def get_emails_lista(self):
        """Convertir email_notificar de string CSV a lista de strings"""
        if not self.email_notificar:
            return []
        return [email.strip() for email in self.email_notificar.split(',') if email.strip()]

    def set_emails_lista(self, emails_list):
        """Convertir lista de strings a string CSV para email_notificar"""
        if not emails_list:
            self.email_notificar = None
        else:
            self.email_notificar = ','.join(emails_list)

    def __repr__(self):
        return f"<ConfiguracionAlertas(id={self.id_alerta}, nombre='{self.nombre_alerta}', tipo={self.tipo_alerta}, activa={self.activa})>"

class LogAlertas(Base):
    __tablename__ = "log_alertas"

    id_log_alerta = Column(Integer, primary_key=True, index=True)
    id_alerta = Column(Integer, ForeignKey("configuracion_alertas.id_alerta"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=True)
    id_obra = Column(Integer, ForeignKey("obras.id_obra"), nullable=True)
    id_despacho = Column(Integer, ForeignKey("despachos_obra.id_despacho"), nullable=True)

    mensaje = Column(Text, nullable=False)
    nivel_prioridad = Column(Enum('BAJA', 'MEDIA', 'ALTA', 'CRITICA'), default='MEDIA')

    fecha_generacion = Column(DateTime, default=func.current_timestamp())
    fecha_visualizacion = Column(DateTime, nullable=True)
    fecha_resolucion = Column(DateTime, nullable=True)
    estado = Column(Enum('PENDIENTE', 'VISTA', 'RESUELTA', 'IGNORADA'), default='PENDIENTE')

    usuario_resolucion = Column(Integer, nullable=True)
    observaciones_resolucion = Column(Text, nullable=True)

    # Relaciones
    configuracion_alerta = relationship("ConfiguracionAlertas", back_populates="logs")
    producto = relationship("Producto", back_populates="logs_alertas")
    obra = relationship("Obra", back_populates="logs_alertas")
    despacho = relationship("DespachosObra", back_populates="logs_alertas")
    

    @property
    def es_pendiente(self):
        """Verificar si la alerta está pendiente"""
        return self.estado == 'PENDIENTE'

    @property
    def es_critica(self):
        """Verificar si la alerta es crítica"""
        return self.nivel_prioridad == 'CRITICA'

    @property
    def tiempo_sin_resolver(self):
        """Calcular tiempo transcurrido sin resolver (en horas)"""
        if self.estado in ['RESUELTA', 'IGNORADA']:
            return 0

        from datetime import datetime
        ahora = datetime.now()
        diferencia = ahora - self.fecha_generacion
        return diferencia.total_seconds() / 3600  # Convertir a horas

    def marcar_como_vista(self, fecha_vista=None):
        """Marcar la alerta como vista"""
        if fecha_vista is None:
            from datetime import datetime
            fecha_vista = datetime.now()

        if self.estado == 'PENDIENTE':
            self.estado = 'VISTA'
            self.fecha_visualizacion = fecha_vista

    def resolver(self, usuario_id, observaciones=None, fecha_resolucion=None):
        """Resolver la alerta"""
        if fecha_resolucion is None:
            from datetime import datetime
            fecha_resolucion = datetime.now()

        self.estado = 'RESUELTA'
        self.fecha_resolucion = fecha_resolucion
        self.usuario_resolucion = usuario_id
        if observaciones:
            self.observaciones_resolucion = observaciones

    def ignorar(self, usuario_id, motivo=None):
        """Ignorar la alerta"""
        from datetime import datetime
        self.estado = 'IGNORADA'
        self.fecha_resolucion = datetime.now()
        self.usuario_resolucion = usuario_id
        if motivo:
            self.observaciones_resolucion = f"Ignorada: {motivo}"

    def __repr__(self):
        return f"<LogAlertas(id={self.id_log_alerta}, alerta_id={self.id_alerta}, nivel={self.nivel_prioridad}, estado={self.estado})>"

class Roles(Base):
    __tablename__ = "roles"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), nullable=False, unique=True, index=True)
    descripcion = Column(Text, nullable=True)
    activo = Column(Boolean, default=True)

    # Relaciones
    usuarios = relationship("Usuarios", back_populates="rol")
    permisos = relationship("Permisos", back_populates="rol")

    def __repr__(self):
        return f"<Roles(id={self.id_rol}, nombre='{self.nombre_rol}', activo={self.activo})>"

class Usuarios(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    nombre_completo = Column(String(200), nullable=False)
    password_hash = Column(String(255), nullable=False)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False)
    activo = Column(Boolean, default=True)
    ultimo_acceso = Column(DateTime, nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relaciones
    rol = relationship("Roles", back_populates="usuarios")

    def actualizar_ultimo_acceso(self):
        """Actualizar la fecha de último acceso"""
        from datetime import datetime
        self.ultimo_acceso = datetime.now()

    def es_activo(self):
        """Verificar si el usuario está activo"""
        return self.activo

    def get_nombre_rol(self):
        """Obtener el nombre del rol del usuario"""
        return self.rol.nombre_rol if self.rol else None

    def __repr__(self):
        return f"<Usuarios(id={self.id_usuario}, username='{self.username}', email='{self.email}', activo={self.activo})>"

class Permisos(Base):
    __tablename__ = "permisos"

    id_permiso = Column(Integer, primary_key=True, autoincrement=True)
    id_rol = Column(Integer, ForeignKey("roles.id_rol"), nullable=False, index=True)
    modulo = Column(String(50), nullable=False)
    crear = Column(Boolean, default=False)
    leer = Column(Boolean, default=False)
    actualizar = Column(Boolean, default=False)
    eliminar = Column(Boolean, default=False)
    autorizar = Column(Boolean, default=False)

    # Índices y restricciones
    __table_args__ = (
        UniqueConstraint('id_rol', 'modulo', name='unique_rol_modulo'),
        Index('idx_rol_permiso', 'id_rol'),
        Index('idx_modulo_permiso', 'modulo'),
    )

    # Relaciones
    rol = relationship("Roles", back_populates="permisos")

    def tiene_permiso(self, accion: str) -> bool:
        """Verificar si el rol tiene un permiso específico"""
        acciones_validas = ['crear', 'leer', 'actualizar', 'eliminar', 'autorizar']
        if accion not in acciones_validas:
            return False
        return getattr(self, accion, False)

    def get_permisos_activos(self) -> list:
        """Obtener lista de permisos activos"""
        permisos_activos = []
        if self.crear:
            permisos_activos.append('crear')
        if self.leer:
            permisos_activos.append('leer')
        if self.actualizar:
            permisos_activos.append('actualizar')
        if self.eliminar:
            permisos_activos.append('eliminar')
        if self.autorizar:
            permisos_activos.append('autorizar')
        return permisos_activos

    def __repr__(self):
        return f"<Permisos(id={self.id_permiso}, rol_id={self.id_rol}, modulo='{self.modulo}', permisos={self.get_permisos_activos()})>"

class ConfiguracionSistema(Base):
    __tablename__ = "configuracion_sistema"

    id_config = Column(Integer, primary_key=True, autoincrement=True)
    parametro = Column(String(100), nullable=False, unique=True, index=True)
    valor = Column(Text, nullable=True)
    tipo_dato = Column(
        Enum('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'DATE', name='tipo_dato_config'),
        default='STRING'
    )
    descripcion = Column(Text, nullable=True)
    modificable = Column(Boolean, default=True)
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    usuario_modificacion = Column(Integer, nullable=True)

    # Índices
    __table_args__ = (
        Index('idx_parametro_config', 'parametro'),
        Index('idx_tipo_dato_config', 'tipo_dato'),
        Index('idx_modificable_config', 'modificable'),
    )

    def get_valor_typed(self):
        """Obtener el valor convertido al tipo de dato correcto"""
        if not self.valor:
            return None

        try:
            if self.tipo_dato == 'INTEGER':
                return int(self.valor)
            elif self.tipo_dato == 'DECIMAL':
                from decimal import Decimal
                return Decimal(self.valor)
            elif self.tipo_dato == 'BOOLEAN':
                return self.valor.lower() in ('true', '1', 'yes', 'on')
            elif self.tipo_dato == 'DATE':
                from datetime import datetime
                return datetime.strptime(self.valor, '%Y-%m-%d').date()
            else:  # STRING
                return self.valor
        except (ValueError, TypeError):
            return self.valor

    def set_valor_from_type(self, valor):
        """Establecer valor convirtiendo del tipo de dato apropiado"""
        if valor is None:
            self.valor = None
            return

        if self.tipo_dato == 'BOOLEAN':
            self.valor = 'true' if valor else 'false'
        elif self.tipo_dato == 'DATE':
            from datetime import date
            if isinstance(valor, date):
                self.valor = valor.strftime('%Y-%m-%d')
            else:
                self.valor = str(valor)
        else:
            self.valor = str(valor)

    def es_modificable(self) -> bool:
        """Verificar si el parámetro es modificable"""
        return self.modificable

    def get_info_config(self) -> dict:
        """Obtener información completa de la configuración"""
        return {
            'id_config': self.id_config,
            'parametro': self.parametro,
            'valor': self.valor,
            'valor_typed': self.get_valor_typed(),
            'tipo_dato': self.tipo_dato,
            'descripcion': self.descripcion,
            'modificable': self.modificable,
            'fecha_modificacion': self.fecha_modificacion,
            'usuario_modificacion': self.usuario_modificacion
        }

    def __repr__(self):
        return f"<ConfiguracionSistema(id={self.id_config}, parametro='{self.parametro}', tipo={self.tipo_dato}, modificable={self.modificable})>"

# ========================================
# VISTA DE INVENTARIO CONSOLIDADO
# ========================================

class VistaInventarioConsolidado(Base):
    __tablename__ = "vista_inventario_consolidado"
    __table_args__ = {'info': {'is_view': True}}  # Marcar como vista SQL

    id_producto = Column(Integer, primary_key=True)
    sku = Column(String(50))
    nombre_producto = Column(String(200))
    stock_almacen = Column(Integer)
    stock_obras = Column(Integer)
    stock_total = Column(Integer)
    stock_minimo = Column(Integer)
    stock_maximo = Column(Integer)
    costo_promedio = Column(DECIMAL(15,4))
    valor_total = Column(DECIMAL(15,2))

    @property
    def nivel_stock(self) -> str:
        """Determinar el nivel de stock basado en mínimos y máximos"""
        if not self.stock_total or not self.stock_minimo:
            return "SIN_DATOS"

        if self.stock_total == 0:
            return "AGOTADO"
        elif self.stock_total < self.stock_minimo:
            return "CRITICO"
        elif self.stock_total <= (self.stock_minimo * 1.2):  # 20% por encima del mínimo
            return "BAJO"
        elif self.stock_maximo and self.stock_total > self.stock_maximo:
            return "EXCESO"
        else:
            return "NORMAL"

    @property
    def necesita_reposicion(self) -> bool:
        """Verificar si el producto necesita reposición"""
        if not self.stock_total or not self.stock_minimo:
            return False
        return self.stock_total < self.stock_minimo

    @property
    def exceso_stock(self) -> bool:
        """Verificar si hay exceso de stock"""
        if not self.stock_total or not self.stock_maximo:
            return False
        return self.stock_total > self.stock_maximo

    @property
    def porcentaje_stock_minimo(self) -> float:
        """Calcular porcentaje actual vs stock mínimo"""
        if not self.stock_minimo or self.stock_minimo == 0:
            return 0.0
        return round((self.stock_total / self.stock_minimo) * 100, 2)

    @property
    def porcentaje_stock_maximo(self) -> float:
        """Calcular porcentaje actual vs stock máximo"""
        if not self.stock_maximo or self.stock_maximo == 0:
            return 0.0
        return round((self.stock_total / self.stock_maximo) * 100, 2)

    @property
    def distribucion_stock(self) -> dict:
        """Obtener distribución del stock entre almacén y obras"""
        if not self.stock_total or self.stock_total == 0:
            return {"almacen_porcentaje": 0.0, "obras_porcentaje": 0.0}

        almacen_pct = round((self.stock_almacen / self.stock_total) * 100, 2)
        obras_pct = round((self.stock_obras / self.stock_total) * 100, 2)

        return {
            "almacen_porcentaje": almacen_pct,
            "obras_porcentaje": obras_pct
        }

    @property
    def valor_promedio_unitario(self) -> float:
        """Calcular valor promedio por unidad"""
        if not self.costo_promedio:
            return 0.0
        return float(self.costo_promedio)

    @property
    def es_producto_alto_valor(self) -> bool:
        """Determinar si es un producto de alto valor (más de $10,000 total)"""
        if not self.valor_total:
            return False
        return float(self.valor_total) > 10000.0

    @property
    def dias_stock_estimados(self) -> Optional[int]:
        """Estimar días de stock disponible (requeriría datos de consumo)"""
        # Esta propiedad se puede extender cuando se tenga data de consumo promedio
        return None

    def get_info_completa(self) -> dict:
        """Obtener información completa del inventario consolidado"""
        return {
            'id_producto': self.id_producto,
            'sku': self.sku,
            'nombre_producto': self.nombre_producto,
            'stock': {
                'almacen': self.stock_almacen,
                'obras': self.stock_obras,
                'total': self.stock_total,
                'minimo': self.stock_minimo,
                'maximo': self.stock_maximo
            },
            'costos': {
                'promedio_unitario': self.valor_promedio_unitario,
                'valor_total': float(self.valor_total) if self.valor_total else 0.0
            },
            'indicadores': {
                'nivel_stock': self.nivel_stock,
                'necesita_reposicion': self.necesita_reposicion,
                'exceso_stock': self.exceso_stock,
                'porcentaje_minimo': self.porcentaje_stock_minimo,
                'porcentaje_maximo': self.porcentaje_stock_maximo,
                'es_alto_valor': self.es_producto_alto_valor
            },
            'distribucion': self.distribucion_stock
        }

    def __repr__(self):
        return f"<VistaInventarioConsolidado(id={self.id_producto}, sku='{self.sku}', stock_total={self.stock_total}, nivel='{self.nivel_stock}')>"

# ========================================
# VISTA DE OBRAS INVENTARIO
# ========================================

class VistaObrasInventario(Base):
    __tablename__ = "vista_obras_inventario"
    __table_args__ = {'info': {'is_view': True}}  # Marcar como vista SQL

    id_obra = Column(Integer, primary_key=True)
    codigo_obra = Column(String(50))
    nombre_obra = Column(String(200))
    estado = Column(String(50))  # Enum de estado de obra
    nombre_cliente = Column(String(200))
    productos_diferentes = Column(Integer)
    cantidad_total_productos = Column(Integer)
    valor_total_inventario = Column(DECIMAL(15,2))
    fecha_inicio_real = Column(Date)
    fecha_fin_programada = Column(Date)

    @property
    def estado_obra_categoria(self) -> str:
        """Categorizar el estado de la obra"""
        if self.estado in ['PLANIFICACION']:
            return "PREPARACION"
        elif self.estado in ['EN_EJECUCION']:
            return "ACTIVA"
        elif self.estado in ['SUSPENDIDA']:
            return "SUSPENDIDA"
        elif self.estado in ['FINALIZADA']:
            return "FINALIZADA"
        elif self.estado in ['CANCELADA']:
            return "CANCELADA"
        else:
            return "DESCONOCIDO"

    @property
    def tiene_inventario(self) -> bool:
        """Verificar si la obra tiene inventario asignado"""
        return (self.productos_diferentes and self.productos_diferentes > 0) or \
               (self.cantidad_total_productos and self.cantidad_total_productos > 0)

    @property
    def valor_promedio_por_producto(self) -> float:
        """Calcular valor promedio por tipo de producto"""
        if not self.productos_diferentes or self.productos_diferentes == 0:
            return 0.0
        if not self.valor_total_inventario:
            return 0.0
        return round(float(self.valor_total_inventario) / self.productos_diferentes, 2)

    @property
    def densidad_inventario(self) -> str:
        """Determinar la densidad del inventario (ALTA, MEDIA, BAJA)"""
        if not self.productos_diferentes or self.productos_diferentes == 0:
            return "SIN_INVENTARIO"

        # Basado en número de productos diferentes
        if self.productos_diferentes >= 50:
            return "ALTA"
        elif self.productos_diferentes >= 20:
            return "MEDIA"
        elif self.productos_diferentes >= 5:
            return "BAJA"
        else:
            return "MINIMA"

    @property
    def categoria_valor(self) -> str:
        """Categorizar la obra por valor del inventario"""
        if not self.valor_total_inventario:
            return "SIN_VALOR"

        valor = float(self.valor_total_inventario)
        if valor >= 100000:
            return "ALTO_VALOR"
        elif valor >= 50000:
            return "VALOR_MEDIO"
        elif valor >= 10000:
            return "VALOR_BAJO"
        else:
            return "VALOR_MINIMO"

    @property
    def dias_en_ejecucion(self) -> Optional[int]:
        """Calcular días desde el inicio real"""
        if not self.fecha_inicio_real:
            return None

        from datetime import date
        today = date.today()
        if self.fecha_inicio_real <= today:
            return (today - self.fecha_inicio_real).days
        return 0

    @property
    def dias_restantes(self) -> Optional[int]:
        """Calcular días restantes hasta la fecha programada de fin"""
        if not self.fecha_fin_programada:
            return None

        from datetime import date
        today = date.today()
        if self.fecha_fin_programada >= today:
            return (self.fecha_fin_programada - today).days
        return 0  # Ya pasó la fecha

    @property
    def esta_retrasada(self) -> bool:
        """Verificar si la obra está retrasada"""
        if not self.fecha_fin_programada:
            return False

        from datetime import date
        today = date.today()
        return self.fecha_fin_programada < today and self.estado in ['EN_EJECUCION', 'SUSPENDIDA']

    @property
    def urgencia_finalizacion(self) -> str:
        """Determinar urgencia basada en fechas"""
        dias_restantes = self.dias_restantes

        if self.esta_retrasada:
            return "RETRASADA"
        elif not dias_restantes:
            return "SIN_FECHA"
        elif dias_restantes <= 7:
            return "URGENTE"
        elif dias_restantes <= 30:
            return "PRÓXIMA"
        else:
            return "NORMAL"

    @property
    def eficiencia_inventario(self) -> float:
        """Calcular eficiencia del inventario (valor/producto)"""
        if not self.productos_diferentes or self.productos_diferentes == 0:
            return 0.0
        if not self.valor_total_inventario:
            return 0.0
        return round(float(self.valor_total_inventario) / self.productos_diferentes, 2)

    @property
    def requiere_atencion(self) -> bool:
        """Determinar si la obra requiere atención especial"""
        return (
            self.esta_retrasada or
            self.urgencia_finalizacion == "URGENTE" or
            self.categoria_valor == "ALTO_VALOR" or
            (self.tiene_inventario and self.estado == "SUSPENDIDA")
        )

    @property
    def indicadores_riesgo(self) -> List[str]:
        """Obtener lista de indicadores de riesgo"""
        riesgos = []

        if self.esta_retrasada:
            riesgos.append("OBRA_RETRASADA")

        if self.urgencia_finalizacion == "URGENTE":
            riesgos.append("FINALIZACION_URGENTE")

        if self.categoria_valor == "ALTO_VALOR" and self.estado == "SUSPENDIDA":
            riesgos.append("ALTO_VALOR_SUSPENDIDA")

        if self.tiene_inventario and self.estado == "CANCELADA":
            riesgos.append("INVENTARIO_OBRA_CANCELADA")

        if not self.fecha_inicio_real and self.estado == "EN_EJECUCION":
            riesgos.append("SIN_FECHA_INICIO")

        return riesgos

    def get_resumen_obra(self) -> dict:
        """Obtener resumen completo de la obra"""
        return {
            'id_obra': self.id_obra,
            'codigo_obra': self.codigo_obra,
            'nombre_obra': self.nombre_obra,
            'estado': self.estado,
            'nombre_cliente': self.nombre_cliente,
            'inventario': {
                'productos_diferentes': self.productos_diferentes,
                'cantidad_total': self.cantidad_total_productos,
                'valor_total': float(self.valor_total_inventario) if self.valor_total_inventario else 0.0,
                'valor_promedio_producto': self.valor_promedio_por_producto,
                'tiene_inventario': self.tiene_inventario
            },
            'fechas': {
                'inicio_real': self.fecha_inicio_real.isoformat() if self.fecha_inicio_real else None,
                'fin_programada': self.fecha_fin_programada.isoformat() if self.fecha_fin_programada else None,
                'dias_en_ejecucion': self.dias_en_ejecucion,
                'dias_restantes': self.dias_restantes,
                'esta_retrasada': self.esta_retrasada
            },
            'clasificaciones': {
                'estado_categoria': self.estado_obra_categoria,
                'densidad_inventario': self.densidad_inventario,
                'categoria_valor': self.categoria_valor,
                'urgencia_finalizacion': self.urgencia_finalizacion
            },
            'alertas': {
                'requiere_atencion': self.requiere_atencion,
                'indicadores_riesgo': self.indicadores_riesgo
            }
        }

    def get_metricas_performance(self) -> dict:
        """Obtener métricas de performance de la obra"""
        return {
            'eficiencia_inventario': self.eficiencia_inventario,
            'densidad_productos': self.productos_diferentes or 0,
            'utilizacion_temporal': {
                'dias_transcurridos': self.dias_en_ejecucion,
                'dias_restantes': self.dias_restantes,
                'porcentaje_completado': self._calcular_porcentaje_tiempo_transcurrido()
            },
            'valor_por_dia': self._calcular_valor_por_dia()
        }

    def _calcular_porcentaje_tiempo_transcurrido(self) -> float:
        """Calcular porcentaje de tiempo transcurrido del proyecto"""
        if not self.fecha_inicio_real or not self.fecha_fin_programada:
            return 0.0

        total_dias = (self.fecha_fin_programada - self.fecha_inicio_real).days
        if total_dias <= 0:
            return 0.0

        dias_transcurridos = self.dias_en_ejecucion or 0
        return round((dias_transcurridos / total_dias) * 100, 2)

    def _calcular_valor_por_dia(self) -> float:
        """Calcular valor de inventario por día de ejecución"""
        if not self.dias_en_ejecucion or self.dias_en_ejecucion == 0:
            return 0.0
        if not self.valor_total_inventario:
            return 0.0

        return round(float(self.valor_total_inventario) / self.dias_en_ejecucion, 2)

    def __repr__(self):
        return f"<VistaObrasInventario(id={self.id_obra}, codigo='{self.codigo_obra}', estado='{self.estado}', productos={self.productos_diferentes}, valor={self.valor_total_inventario})>"


# ========================================
# VISTA DEVOLUCIONES PENDIENTES
# ========================================

class VistaDevolucionesPendientes(Base):
    """
    Vista para el seguimiento de devoluciones pendientes de obras
    """
    __tablename__ = 'vista_devoluciones_pendientes'
    __table_args__ = {'info': {'is_view': True}}

    # Campos principales de la vista
    id_despacho = Column(Integer, primary_key=True, index=True)
    numero_despacho = Column(String(50), nullable=False, index=True)
    codigo_obra = Column(String(50), nullable=False, index=True)
    nombre_obra = Column(String(200), nullable=False)
    fecha_despacho = Column(Date, nullable=False, index=True)
    fecha_limite_devolucion = Column(Date, nullable=True, index=True)
    dias_para_limite = Column(Integer, nullable=True)
    productos_diferentes = Column(Integer, nullable=False, default=0)
    cantidad_pendiente_devolucion = Column(Float, nullable=False, default=0.0)
    valor_pendiente = Column(DECIMAL(15, 2), nullable=False, default=0.00)

    # Propiedades calculadas
    @property
    def esta_vencida(self) -> bool:
        """Indica si la devolución está vencida"""
        if not self.fecha_limite_devolucion:
            return False
        from datetime import date
        return date.today() > self.fecha_limite_devolucion

    @property
    def estado_devolucion(self) -> str:
        """Estado actual de la devolución"""
        if self.esta_vencida:
            return "VENCIDA"
        elif self.dias_para_limite is not None:
            if self.dias_para_limite <= 0:
                return "VENCIDA"
            elif self.dias_para_limite <= 7:
                return "URGENTE"
            elif self.dias_para_limite <= 15:
                return "PROXIMO_VENCIMIENTO"
            else:
                return "EN_PLAZO"
        return "SIN_FECHA_LIMITE"

    @property
    def nivel_criticidad(self) -> str:
        """Nivel de criticidad basado en valor y tiempo"""
        valor_float = float(self.valor_pendiente) if self.valor_pendiente else 0.0

        if self.esta_vencida:
            if valor_float > 50000:
                return "CRITICA"
            elif valor_float > 20000:
                return "ALTA"
            else:
                return "MEDIA"
        elif self.dias_para_limite is not None and self.dias_para_limite <= 7:
            if valor_float > 30000:
                return "ALTA"
            elif valor_float > 10000:
                return "MEDIA"
            else:
                return "BAJA"
        else:
            if valor_float > 100000:
                return "ALTA"
            elif valor_float > 30000:
                return "MEDIA"
            else:
                return "BAJA"

    @property
    def categoria_valor(self) -> str:
        """Categoría del valor pendiente"""
        valor_float = float(self.valor_pendiente) if self.valor_pendiente else 0.0

        if valor_float >= 100000:
            return "MUY_ALTO"
        elif valor_float >= 50000:
            return "ALTO"
        elif valor_float >= 20000:
            return "MEDIO"
        elif valor_float >= 5000:
            return "BAJO"
        else:
            return "MINIMO"

    @property
    def requiere_atencion_inmediata(self) -> bool:
        """Indica si requiere atención inmediata"""
        return (
            self.esta_vencida or
            (self.dias_para_limite is not None and self.dias_para_limite <= 3) or
            float(self.valor_pendiente or 0) > 50000
        )

    @property
    def porcentaje_tiempo_transcurrido(self) -> float:
        """Porcentaje del tiempo transcurrido desde el despacho"""
        if not self.fecha_limite_devolucion:
            return 0.0

        from datetime import date
        dias_totales = (self.fecha_limite_devolucion - self.fecha_despacho).days
        dias_transcurridos = (date.today() - self.fecha_despacho).days

        if dias_totales <= 0:
            return 100.0

        porcentaje = (dias_transcurridos / dias_totales) * 100
        return min(round(porcentaje, 2), 100.0)

    @property
    def alerta_generada(self) -> str:
        """Tipo de alerta que debe generarse"""
        if self.esta_vencida:
            return "DEVOLUCION_VENCIDA"
        elif self.dias_para_limite is not None and self.dias_para_limite <= 3:
            return "DEVOLUCION_URGENTE"
        elif float(self.valor_pendiente or 0) > 50000:
            return "ALTO_VALOR_PENDIENTE"
        elif self.productos_diferentes >= 20:
            return "MUCHOS_PRODUCTOS_PENDIENTES"
        else:
            return "SEGUIMIENTO_NORMAL"

    @property
    def valor_promedio_por_producto(self) -> float:
        """Valor promedio por producto pendiente"""
        if self.productos_diferentes <= 0:
            return 0.0
        return round(float(self.valor_pendiente or 0) / self.productos_diferentes, 2)

    @property
    def cantidad_promedio_por_producto(self) -> float:
        """Cantidad promedio por producto pendiente"""
        if self.productos_diferentes <= 0:
            return 0.0
        return round(self.cantidad_pendiente_devolucion / self.productos_diferentes, 2)

    @property
    def indicador_urgencia(self) -> int:
        """Indicador numérico de urgencia (1-10, donde 10 es más urgente)"""
        puntuacion = 0

        # Por tiempo
        if self.esta_vencida:
            puntuacion += 5
        elif self.dias_para_limite is not None:
            if self.dias_para_limite <= 3:
                puntuacion += 4
            elif self.dias_para_limite <= 7:
                puntuacion += 3
            elif self.dias_para_limite <= 15:
                puntuacion += 2
            else:
                puntuacion += 1

        # Por valor
        valor_float = float(self.valor_pendiente or 0)
        if valor_float > 100000:
            puntuacion += 4
        elif valor_float > 50000:
            puntuacion += 3
        elif valor_float > 20000:
            puntuacion += 2
        elif valor_float > 5000:
            puntuacion += 1

        # Por cantidad de productos
        if self.productos_diferentes >= 20:
            puntuacion += 1

        return min(puntuacion, 10)

    @property
    def resumen_estado(self) -> str:
        """Resumen del estado actual"""
        estado = self.estado_devolucion
        criticidad = self.nivel_criticidad
        return f"{estado} - {criticidad}"

    @property
    def acciones_recomendadas(self) -> list:
        """Lista de acciones recomendadas"""
        acciones = []

        if self.esta_vencida:
            acciones.append("Contactar inmediatamente al cliente")
            acciones.append("Evaluar penalizaciones por retraso")

        if self.dias_para_limite is not None and self.dias_para_limite <= 7:
            acciones.append("Enviar recordatorio urgente al cliente")
            acciones.append("Programar visita de seguimiento")

        if float(self.valor_pendiente or 0) > 50000:
            acciones.append("Escalar a gerencia")
            acciones.append("Revisar garantías y seguros")

        if self.productos_diferentes >= 15:
            acciones.append("Generar reporte detallado de productos")
            acciones.append("Considerar devolución parcial")

        if not acciones:
            acciones.append("Mantener seguimiento regular")

        return acciones

    def __repr__(self):
        return f"<VistaDevolucionesPendientes(id={self.id_despacho}, numero='{self.numero_despacho}', obra='{self.codigo_obra}', valor={self.valor_pendiente})>"


# ========================================
# VISTA PRODUCTOS ABC
# ========================================

class VistaProductosABC(Base):
    """
    Vista para análisis ABC de productos basado en movimientos y valor de inventario
    """
    __tablename__ = 'vista_productos_abc'
    __table_args__ = {'info': {'is_view': True}}

    # Campos principales de la vista
    id_producto = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), nullable=False, index=True)
    nombre_producto = Column(String(200), nullable=False)
    stock_actual = Column(Float, nullable=False, default=0.0)
    costo_promedio = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    valor_inventario = Column(DECIMAL(15, 2), nullable=False, default=0.00)
    movimientos_anuales = Column(Float, nullable=False, default=0.0)
    clasificacion_abc = Column(String(20), nullable=False, default='POR_CLASIFICAR')

    # Propiedades calculadas para análisis ABC
    @property
    def rotacion_inventario(self) -> float:
        """Cálculo de rotación de inventario"""
        if self.stock_actual <= 0:
            return 0.0
        return round(self.movimientos_anuales / self.stock_actual, 2)

    @property
    def valor_movimiento_anual(self) -> float:
        """Valor de los movimientos anuales"""
        return round(float(self.movimientos_anuales * self.costo_promedio), 2)

    @property
    def clasificacion_abc_calculada(self) -> str:
        """Clasificación ABC calculada basada en valor y movimientos"""
        if self.movimientos_anuales == 0:
            return "SIN_MOVIMIENTO"

        valor_movimiento = self.valor_movimiento_anual

        # Estos umbrales podrían ser configurables en el futuro
        if valor_movimiento >= 100000:  # Productos de alto valor/movimiento
            return "A"
        elif valor_movimiento >= 20000:  # Productos de valor/movimiento medio
            return "B"
        elif valor_movimiento > 0:  # Productos de bajo valor/movimiento
            return "C"
        else:
            return "SIN_MOVIMIENTO"

    @property
    def categoria_valor_inventario(self) -> str:
        """Categoría del valor de inventario actual"""
        valor = float(self.valor_inventario) if self.valor_inventario else 0.0

        if valor >= 50000:
            return "MUY_ALTO"
        elif valor >= 20000:
            return "ALTO"
        elif valor >= 5000:
            return "MEDIO"
        elif valor >= 1000:
            return "BAJO"
        else:
            return "MINIMO"

    @property
    def categoria_rotacion(self) -> str:
        """Categoría de rotación de inventario"""
        rotacion = self.rotacion_inventario

        if rotacion >= 12:  # Más de una vez por mes
            return "MUY_ALTA"
        elif rotacion >= 6:  # Cada 2 meses
            return "ALTA"
        elif rotacion >= 3:  # Cada 4 meses
            return "MEDIA"
        elif rotacion >= 1:  # Menos de una vez por año
            return "BAJA"
        else:
            return "SIN_ROTACION"

    @property
    def requiere_atencion(self) -> bool:
        """Indica si el producto requiere atención especial"""
        return (
            self.movimientos_anuales == 0 and float(self.valor_inventario) > 5000 or  # Stock alto sin movimiento
            self.rotacion_inventario > 20 or  # Rotación muy alta (posible desabasto)
            (self.clasificacion_abc_calculada == "A" and self.stock_actual <= 0)  # Producto A sin stock
        )

    @property
    def nivel_criticidad(self) -> str:
        """Nivel de criticidad para gestión de inventario"""
        clasificacion = self.clasificacion_abc_calculada
        rotacion = self.rotacion_inventario
        valor = float(self.valor_inventario) if self.valor_inventario else 0.0

        if clasificacion == "A":
            if self.stock_actual <= 0:
                return "CRITICA"
            elif rotacion < 1:
                return "ALTA"
            else:
                return "NORMAL"
        elif clasificacion == "B":
            if valor > 20000 and rotacion < 0.5:
                return "ALTA"
            elif self.stock_actual <= 0 and self.movimientos_anuales > 0:
                return "MEDIA"
            else:
                return "NORMAL"
        elif clasificacion == "C":
            if valor > 10000 and rotacion == 0:
                return "MEDIA"
            else:
                return "BAJA"
        else:  # SIN_MOVIMIENTO
            if valor > 5000:
                return "MEDIA"
            else:
                return "BAJA"

    @property
    def recomendacion_accion(self) -> str:
        """Recomendación de acción basada en análisis ABC"""
        clasificacion = self.clasificacion_abc_calculada
        rotacion = self.rotacion_inventario
        valor = float(self.valor_inventario) if self.valor_inventario else 0.0

        if clasificacion == "A":
            if self.stock_actual <= 0:
                return "REPOSICION_URGENTE"
            elif rotacion > 15:
                return "AUMENTAR_STOCK_MINIMO"
            elif rotacion < 1:
                return "REVISAR_DEMANDA"
            else:
                return "MANTENER_SEGUIMIENTO"
        elif clasificacion == "B":
            if self.stock_actual <= 0 and self.movimientos_anuales > 0:
                return "PROGRAMAR_REPOSICION"
            elif rotacion < 0.5 and valor > 10000:
                return "EVALUAR_DESCONTINUAR"
            else:
                return "SEGUIMIENTO_PERIODICO"
        elif clasificacion == "C":
            if valor > 10000 and rotacion == 0:
                return "CONSIDERAR_LIQUIDACION"
            elif rotacion > 0:
                return "MANTENER_STOCK_MINIMO"
            else:
                return "REVISAR_NECESIDAD"
        else:  # SIN_MOVIMIENTO
            if valor > 5000:
                return "EVALUAR_LIQUIDACION"
            else:
                return "CONSIDERAR_DESCONTINUAR"

    @property
    def dias_inventario(self) -> float:
        """Días de inventario disponible basado en consumo promedio"""
        if self.movimientos_anuales <= 0:
            return 999.0  # Valor alto para productos sin movimiento

        consumo_diario = self.movimientos_anuales / 365
        if consumo_diario <= 0:
            return 999.0

        return round(self.stock_actual / consumo_diario, 1)

    @property
    def punto_reorden_sugerido(self) -> float:
        """Punto de reorden sugerido basado en clasificación ABC"""
        clasificacion = self.clasificacion_abc_calculada
        consumo_mensual = self.movimientos_anuales / 12

        if clasificacion == "A":
            # 2 meses de inventario para productos A
            return round(consumo_mensual * 2, 1)
        elif clasificacion == "B":
            # 1.5 meses de inventario para productos B
            return round(consumo_mensual * 1.5, 1)
        elif clasificacion == "C":
            # 1 mes de inventario para productos C
            return round(consumo_mensual * 1, 1)
        else:
            # Sin movimiento, mantener stock mínimo
            return round(self.stock_actual * 0.1, 1)

    @property
    def stock_maximo_sugerido(self) -> float:
        """Stock máximo sugerido basado en clasificación ABC"""
        clasificacion = self.clasificacion_abc_calculada
        consumo_mensual = self.movimientos_anuales / 12

        if clasificacion == "A":
            # 4 meses de inventario máximo para productos A
            return round(consumo_mensual * 4, 1)
        elif clasificacion == "B":
            # 3 meses de inventario máximo para productos B
            return round(consumo_mensual * 3, 1)
        elif clasificacion == "C":
            # 2 meses de inventario máximo para productos C
            return round(consumo_mensual * 2, 1)
        else:
            # Sin movimiento, reducir gradualmente
            return round(self.stock_actual * 0.5, 1)

    @property
    def impacto_financiero(self) -> str:
        """Impacto financiero del producto en el inventario"""
        valor = float(self.valor_inventario) if self.valor_inventario else 0.0
        valor_movimiento = self.valor_movimiento_anual

        if valor_movimiento >= 100000:
            return "MUY_ALTO"
        elif valor_movimiento >= 50000:
            return "ALTO"
        elif valor_movimiento >= 10000:
            return "MEDIO"
        elif valor_movimiento > 0:
            return "BAJO"
        else:
            return "NULO"

    @property
    def indicador_obsolescencia(self) -> float:
        """Indicador de riesgo de obsolescencia (0-10, donde 10 es mayor riesgo)"""
        puntuacion = 0

        # Por falta de movimiento
        if self.movimientos_anuales == 0:
            puntuacion += 4
        elif self.rotacion_inventario < 0.5:
            puntuacion += 2
        elif self.rotacion_inventario < 1:
            puntuacion += 1

        # Por valor de inventario alto
        valor = float(self.valor_inventario) if self.valor_inventario else 0.0
        if valor > 20000 and self.movimientos_anuales == 0:
            puntuacion += 3
        elif valor > 10000 and self.rotacion_inventario < 0.5:
            puntuacion += 2
        elif valor > 5000 and self.rotacion_inventario < 1:
            puntuacion += 1

        # Por exceso de días de inventario
        dias = self.dias_inventario
        if dias > 365:
            puntuacion += 2
        elif dias > 180:
            puntuacion += 1

        return min(puntuacion, 10)

    @property
    def acciones_recomendadas(self) -> list:
        """Lista de acciones recomendadas basadas en análisis ABC"""
        acciones = []

        clasificacion = self.clasificacion_abc_calculada
        rotacion = self.rotacion_inventario
        valor = float(self.valor_inventario) if self.valor_inventario else 0.0
        obsolescencia = self.indicador_obsolescencia

        # Acciones por clasificación
        if clasificacion == "A":
            if self.stock_actual <= 0:
                acciones.append("Reposición urgente - Producto crítico sin stock")
            if rotacion > 15:
                acciones.append("Revisar stock mínimo - Alta rotación")
            acciones.append("Mantener seguimiento semanal")

        elif clasificacion == "B":
            if self.stock_actual <= 0 and self.movimientos_anuales > 0:
                acciones.append("Programar reposición")
            acciones.append("Seguimiento quincenal")

        elif clasificacion == "C":
            if valor > 10000 and rotacion == 0:
                acciones.append("Evaluar liquidación o promoción")
            acciones.append("Seguimiento mensual")

        else:  # SIN_MOVIMIENTO
            if valor > 5000:
                acciones.append("Evaluar descontinuación del producto")
            acciones.append("Revisar necesidad en catálogo")

        # Acciones por obsolescencia
        if obsolescencia >= 7:
            acciones.append("Riesgo alto de obsolescencia - Acción inmediata")
        elif obsolescencia >= 4:
            acciones.append("Monitorear riesgo de obsolescencia")

        # Acciones por días de inventario
        if self.dias_inventario > 365:
            acciones.append("Exceso de inventario - Evaluar liquidación")
        elif self.dias_inventario > 180:
            acciones.append("Inventario alto - Reducir próximas compras")

        if not acciones:
            acciones.append("Producto en condiciones normales")

        return acciones

    def __repr__(self):
        return f"<VistaProductosABC(id={self.id_producto}, sku='{self.sku}', clasificacion='{self.clasificacion_abc_calculada}', valor={self.valor_inventario})>"


# ========================================
# MODELOS PARA ESTADOS DE ORDEN DE COMPRA
# ========================================

class EstadoOrdenCompra(Base):
    __tablename__ = "estados_orden_compra"

    id_estado = Column(Integer, primary_key=True, autoincrement=True)
    codigo_estado = Column(String(20), nullable=False, unique=True, index=True)
    nombre_estado = Column(String(50), nullable=False)
    descripcion = Column(String(200), nullable=True)
    es_estado_inicial = Column(Boolean, default=False)
    es_estado_final = Column(Boolean, default=False)
    permite_edicion = Column(Boolean, default=True)
    permite_cancelacion = Column(Boolean, default=True)
    activo = Column(Boolean, default=True, index=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f"<EstadoOrdenCompra(codigo='{self.codigo_estado}', nombre='{self.nombre_estado}')>"


class OrdenCompra(Base):
    __tablename__ = "ordenes_compra"

    id_orden_compra = Column(Integer, primary_key=True, autoincrement=True)
    numero_orden = Column(String(50), nullable=False, unique=True, index=True)

    # Referencias
    id_proveedor = Column(Integer, ForeignKey("proveedores.id_proveedor"), nullable=False, index=True)
    id_usuario_solicitante = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False, index=True)
    id_usuario_aprobador = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    id_estado = Column(Integer, ForeignKey("estados_orden_compra.id_estado"), nullable=False, index=True)

    # Fechas
    fecha_orden = Column(Date, nullable=False, index=True)
    fecha_requerida = Column(Date, nullable=False, index=True)
    fecha_esperada_entrega = Column(Date, nullable=True)
    fecha_entrega_real = Column(Date, nullable=True)

    # Totales
    subtotal = Column(DECIMAL(15,4), nullable=False, default=0)
    impuestos = Column(DECIMAL(15,4), nullable=False, default=0)
    descuentos = Column(DECIMAL(15,4), nullable=False, default=0)
    total = Column(DECIMAL(15,4), nullable=False, default=0)

    # Información adicional
    observaciones = Column(Text, nullable=True)
    terminos_pago = Column(String(100), nullable=True)
    moneda = Column(String(3), default='MXN')
    tipo_cambio = Column(DECIMAL(10,4), default=1.0000)

    # Dirección de entrega
    direccion_entrega = Column(Text, nullable=True)
    contacto_entrega = Column(String(100), nullable=True)
    telefono_contacto = Column(String(20), nullable=True)

    # Control
    activo = Column(Boolean, default=True, index=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    fecha_aprobacion = Column(TIMESTAMP, nullable=True)
    fecha_cancelacion = Column(TIMESTAMP, nullable=True)
    motivo_cancelacion = Column(String(200), nullable=True)

    # Relationships
    proveedor = relationship("Proveedor")
    usuario_solicitante = relationship("Usuarios", foreign_keys=[id_usuario_solicitante])
    usuario_aprobador = relationship("Usuarios", foreign_keys=[id_usuario_aprobador])
    estado = relationship("EstadoOrdenCompra")
    detalles = relationship("OrdenCompraDetalle", back_populates="orden_compra", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<OrdenCompra(numero='{self.numero_orden}', proveedor_id={self.id_proveedor}, total={self.total})>"


class OrdenCompraDetalle(Base):
    __tablename__ = "ordenes_compra_detalle"

    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_orden_compra = Column(Integer, ForeignKey("ordenes_compra.id_orden_compra"), nullable=False, index=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False, index=True)

    # Cantidades
    cantidad_solicitada = Column(DECIMAL(12,4), nullable=False)
    cantidad_recibida = Column(DECIMAL(12,4), nullable=False, default=0)
    cantidad_pendiente = Column(DECIMAL(12,4), nullable=False, default=0)

    # Precios
    precio_unitario = Column(DECIMAL(15,4), nullable=False)
    descuento_porcentaje = Column(DECIMAL(5,2), nullable=False, default=0)
    descuento_importe = Column(DECIMAL(15,4), nullable=False, default=0)
    precio_neto = Column(DECIMAL(15,4), nullable=False)
    importe_total = Column(DECIMAL(15,4), nullable=False)

    # Información adicional
    observaciones = Column(Text, nullable=True)
    numero_linea = Column(Integer, nullable=False, index=True)
    codigo_producto_proveedor = Column(String(100), nullable=True)

    # Fechas esperadas
    fecha_entrega_esperada = Column(Date, nullable=True)
    fecha_entrega_real = Column(Date, nullable=True)

    # Control
    activo = Column(Boolean, default=True, index=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    orden_compra = relationship("OrdenCompra", back_populates="detalles")
    producto = relationship("Producto")

    def __repr__(self):
        return f"<OrdenCompraDetalle(orden_id={self.id_orden_compra}, producto_id={self.id_producto}, cantidad={self.cantidad_solicitada})>"


class RecepcionMercancia(Base):
    __tablename__ = "recepciones_mercancia"

    id_recepcion = Column(Integer, primary_key=True, autoincrement=True)
    numero_recepcion = Column(String(50), nullable=False, unique=True, index=True)
    id_orden_compra = Column(Integer, ForeignKey("ordenes_compra.id_orden_compra"), nullable=False, index=True)
    id_usuario_receptor = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False, index=True)

    # Información de recepción
    fecha_recepcion = Column(Date, nullable=False, index=True)
    numero_factura_proveedor = Column(String(100), nullable=True)
    numero_remision = Column(String(100), nullable=True)
    numero_guia = Column(String(100), nullable=True)
    transportista = Column(String(200), nullable=True)

    # Estado de la recepción
    recepcion_completa = Column(Boolean, default=False)
    observaciones = Column(Text, nullable=True)

    # Control
    activo = Column(Boolean, default=True, index=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    orden_compra = relationship("OrdenCompra")
    usuario_receptor = relationship("Usuarios")
    detalles = relationship("RecepcionMercanciaDetalle", back_populates="recepcion", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<RecepcionMercancia(numero='{self.numero_recepcion}', orden_id={self.id_orden_compra})>"


class RecepcionMercanciaDetalle(Base):
    __tablename__ = "recepciones_mercancia_detalle"

    id_detalle_recepcion = Column(Integer, primary_key=True, autoincrement=True)
    id_recepcion = Column(Integer, ForeignKey("recepciones_mercancia.id_recepcion"), nullable=False, index=True)
    id_detalle_orden = Column(Integer, ForeignKey("ordenes_compra_detalle.id_detalle"), nullable=False, index=True)

    # Cantidades
    cantidad_recibida = Column(DECIMAL(12,4), nullable=False)
    cantidad_aceptada = Column(DECIMAL(12,4), nullable=False)
    cantidad_rechazada = Column(DECIMAL(12,4), nullable=False, default=0)

    # Información de calidad
    observaciones_calidad = Column(Text, nullable=True)
    motivo_rechazo = Column(String(200), nullable=True)
    lote_proveedor = Column(String(100), nullable=True, index=True)
    fecha_vencimiento = Column(Date, nullable=True, index=True)

    # Ubicación en almacén
    ubicacion_almacen = Column(String(100), nullable=True)

    # Control
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    recepcion = relationship("RecepcionMercancia", back_populates="detalles")
    detalle_orden = relationship("OrdenCompraDetalle")

    def __repr__(self):
        return f"<RecepcionMercanciaDetalle(recepcion_id={self.id_recepcion}, cantidad_recibida={self.cantidad_recibida})>"


# ========================================
# VISTAS PARA ÓRDENES DE COMPRA
# ========================================

class VistaOrdenesCompraResumen(Base):
    __tablename__ = "vista_ordenes_compra_resumen"

    id_orden_compra = Column(Integer, primary_key=True)
    numero_orden = Column(String(50))
    nombre_proveedor = Column(String(200))
    codigo_proveedor = Column(String(20))
    solicitante = Column(String(200))
    aprobador = Column(String(200))
    nombre_estado = Column(String(50))
    fecha_orden = Column(Date)
    fecha_requerida = Column(Date)
    total = Column(DECIMAL(15,4))
    moneda = Column(String(3))
    total_lineas = Column(Integer)
    lineas_pendientes = Column(Integer)
    estado_recepcion = Column(String(20))

    def __repr__(self):
        return f"<VistaOrdenesCompraResumen(numero='{self.numero_orden}', estado='{self.estado_recepcion}')>"


class VistaOrdenesDetalleCompleto(Base):
    __tablename__ = "vista_ordenes_detalle_completo"

    id_detalle = Column(Integer, primary_key=True)
    numero_orden = Column(String(50))
    numero_linea = Column(Integer)
    sku = Column(String(50))
    producto_nombre = Column(String(200))
    producto_descripcion = Column(String(500))
    nombre_unidad = Column(String(50))
    cantidad_solicitada = Column(DECIMAL(12,4))
    cantidad_recibida = Column(DECIMAL(12,4))
    cantidad_pendiente = Column(DECIMAL(12,4))
    precio_unitario = Column(DECIMAL(15,4))
    descuento_porcentaje = Column(DECIMAL(5,2))
    precio_neto = Column(DECIMAL(15,4))
    importe_total = Column(DECIMAL(15,4))
    fecha_entrega_esperada = Column(Date)
    codigo_producto_proveedor = Column(String(100))
    nombre_proveedor = Column(String(200))

    def __repr__(self):
        return f"<VistaOrdenesDetalleCompleto(orden='{self.numero_orden}', producto='{self.sku}')>"
