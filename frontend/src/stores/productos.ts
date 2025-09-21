import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface Producto {
  id_producto: number
  sku: string
  nombre_producto: string
  descripcion_corta?: string
  descripcion_detallada?: string
  id_marca?: number
  modelo?: string
  numero_parte?: string
  id_tipo_producto: number
  id_unidad_medida: number

  // Especificaciones técnicas generales
  peso_kg?: number
  dimensiones_largo_cm?: number
  dimensiones_ancho_cm?: number
  dimensiones_alto_cm?: number
  material_principal?: string
  color?: string

  // Información para sistemas contra incendios
  presion_trabajo_bar?: number
  presion_maxima_bar?: number
  temperatura_min_celsius?: number
  temperatura_max_celsius?: number
  temperatura_activacion_celsius?: number
  factor_k?: number
  conexion_entrada?: string
  conexion_salida?: string

  // Certificaciones y normativas
  certificacion_ul?: string
  certificacion_fm?: string
  certificacion_vds?: string
  certificacion_lpcb?: string
  norma_nfpa?: string
  norma_en?: string
  norma_iso?: string

  // Información de inventario
  stock_actual?: number
  stock_minimo: number
  stock_maximo: number
  punto_reorden: number
  tiempo_entrega_dias?: number
  costo_promedio?: number
  precio_venta?: number
  ubicacion_principal?: string

  // Almacenamiento
  condiciones_especiales?: string
  vida_util_meses?: number
  requiere_refrigeracion: boolean

  // Control
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string
  usuario_creacion?: number
  usuario_modificacion?: number

  // Relaciones
  marca?: any
  tipo_producto?: any
  unidad_medida?: any
}

export interface ProductoCreate {
  sku: string
  nombre_producto: string
  descripcion_corta?: string
  descripcion_detallada?: string
  id_marca?: number
  modelo?: string
  numero_parte?: string
  id_tipo_producto: number
  id_unidad_medida: number

  // Especificaciones técnicas generales
  peso_kg?: number
  dimensiones_largo_cm?: number
  dimensiones_ancho_cm?: number
  dimensiones_alto_cm?: number
  material_principal?: string
  color?: string

  // Información para sistemas contra incendios
  presion_trabajo_bar?: number
  presion_maxima_bar?: number
  temperatura_min_celsius?: number
  temperatura_max_celsius?: number
  temperatura_activacion_celsius?: number
  factor_k?: number
  conexion_entrada?: string
  conexion_salida?: string

  // Certificaciones y normativas
  certificacion_ul?: string
  certificacion_fm?: string
  certificacion_vds?: string
  certificacion_lpcb?: string
  norma_nfpa?: string
  norma_en?: string
  norma_iso?: string

  // Información de inventario
  stock_minimo: number
  stock_maximo: number
  punto_reorden: number
  tiempo_entrega_dias?: number
  costo_promedio?: number
  precio_venta?: number
  ubicacion_principal?: string

  // Almacenamiento
  condiciones_especiales?: string
  vida_util_meses?: number
  requiere_refrigeracion: boolean

  // Control
  activo: boolean
}

export interface ProductoUpdate {
  sku?: string
  nombre_producto?: string
  descripcion_corta?: string
  descripcion_detallada?: string
  id_marca?: number
  modelo?: string
  numero_parte?: string
  id_tipo_producto?: number
  id_unidad_medida?: number

  // Especificaciones técnicas generales
  peso_kg?: number
  dimensiones_largo_cm?: number
  dimensiones_ancho_cm?: number
  dimensiones_alto_cm?: number
  material_principal?: string
  color?: string

  // Información para sistemas contra incendios
  presion_trabajo_bar?: number
  presion_maxima_bar?: number
  temperatura_min_celsius?: number
  temperatura_max_celsius?: number
  temperatura_activacion_celsius?: number
  factor_k?: number
  conexion_entrada?: string
  conexion_salida?: string

  // Certificaciones y normativas
  certificacion_ul?: string
  certificacion_fm?: string
  certificacion_vds?: string
  certificacion_lpcb?: string
  norma_nfpa?: string
  norma_en?: string
  norma_iso?: string

  // Información de inventario
  stock_actual?: number
  stock_minimo?: number
  stock_maximo?: number
  punto_reorden?: number
  tiempo_entrega_dias?: number
  costo_promedio?: number
  precio_venta?: number
  ubicacion_principal?: string

  // Almacenamiento
  condiciones_especiales?: string
  vida_util_meses?: number
  requiere_refrigeracion?: boolean

  // Control
  activo?: boolean
}

// Interfaces para relaciones
export interface Marca {
  id_marca: number
  codigo_marca: string
  nombre_marca: string
  activo: boolean
}

export interface TipoProducto {
  id_tipo_producto: number
  codigo_tipo: string
  nombre_tipo: string
  activo: boolean
}

export interface UnidadMedida {
  id_unidad: number
  codigo_unidad: string
  nombre_unidad: string
  activo: boolean
}

// Interfaces para producto_proveedores - Relación Comercial
export interface ProductoProveedor {
  id_producto_proveedor: number
  id_producto: number
  id_proveedor: number
  es_proveedor_principal: boolean
  precio_proveedor?: number
  moneda?: string
  tiempo_entrega_dias?: number
  cantidad_minima?: number
  fecha_vigencia_desde?: string
  fecha_vigencia_hasta?: string
  descuento_volumen?: number
  condiciones_especiales?: string
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string

  // Relaciones
  proveedor?: any
}

export interface ProductoProveedorCreate {
  id_producto: number
  id_proveedor: number
  es_proveedor_principal: boolean
  precio_proveedor?: number
  moneda?: string
  tiempo_entrega_dias?: number
  cantidad_minima?: number
  fecha_vigencia_desde?: string
  fecha_vigencia_hasta?: string
  descuento_volumen?: number
  condiciones_especiales?: string
  activo: boolean
}

export interface ProductoProveedorUpdate {
  id_proveedor?: number
  es_proveedor_principal?: boolean
  precio_proveedor?: number
  moneda?: string
  tiempo_entrega_dias?: number
  cantidad_minima?: number
  fecha_vigencia_desde?: string
  fecha_vigencia_hasta?: string
  descuento_volumen?: number
  condiciones_especiales?: string
  activo?: boolean
}

// Interfaces para producto_ubicaciones - Ubicación Física
export interface ProductoUbicacion {
  id_producto_ubicacion: number
  id_producto: number
  id_bodega: number
  id_pasillo?: number
  id_estante?: number
  ubicacion_codigo?: string
  ubicacion_descripcion?: string
  cantidad_actual: number
  cantidad_reservada: number
  cantidad_disponible: number
  fecha_ultimo_conteo?: string
  fecha_ultimo_movimiento?: string
  observaciones?: string
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string

  // Relaciones
  bodega?: any
  pasillo?: any
  estante?: any
}

export interface ProductoUbicacionCreate {
  id_producto: number
  id_bodega: number
  id_pasillo?: number
  id_estante?: number
  ubicacion_codigo?: string
  ubicacion_descripcion?: string
  cantidad_actual: number
  cantidad_reservada?: number
  observaciones?: string
  activo: boolean
}

export interface ProductoUbicacionUpdate {
  id_bodega?: number
  id_pasillo?: number
  id_estante?: number
  ubicacion_codigo?: string
  ubicacion_descripcion?: string
  cantidad_actual?: number
  cantidad_reservada?: number
  observaciones?: string
  activo?: boolean
}

export interface MovimientoUbicacion {
  id_movimiento: number
  id_producto_ubicacion: number
  tipo_movimiento: 'entrada' | 'salida' | 'transferencia' | 'ajuste' | 'conteo'
  cantidad: number
  cantidad_anterior: number
  cantidad_nueva: number
  motivo?: string
  usuario?: string
  fecha_movimiento: string
}

export const useProductoStore = defineStore('productos', () => {
  const apiStore = useApiStore()

  const productos = ref<Producto[]>([])
  const marcas = ref<Marca[]>([])
  const tiposProducto = ref<TipoProducto[]>([])
  const unidadesMedida = ref<UnidadMedida[]>([])
  const productoProveedores = ref<ProductoProveedor[]>([])
  const productoUbicaciones = ref<ProductoUbicacion[]>([])
  const movimientosUbicacion = ref<MovimientoUbicacion[]>([])
  const isLoading = ref(false)

  // CRUD Productos
  const obtenerProductos = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
    marca_id?: number
    tipo_id?: number
  }): Promise<Producto[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')
      if (params?.marca_id !== undefined) queryParams.append('marca_id', params.marca_id.toString())
      if (params?.tipo_id !== undefined) queryParams.append('tipo_id', params.tipo_id.toString())

      const url = `/productos?${queryParams.toString()}`
      console.log('URL construida productos:', url, 'params recibidos:', params)
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener productos')
      }
      productos.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener productos:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const buscarProductos = async (
    searchTerm: string,
    params?: {
      skip?: number
      limit?: number
      activo?: boolean
    }
  ): Promise<Producto[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()
      queryParams.append('q', searchTerm)

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const response = await apiStore.get(`/productos/search?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al buscar productos')
      }
      return response.data
    } catch (error) {
      console.error('Error al buscar productos:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerProducto = async (id: number): Promise<Producto> => {
    try {
      const response = await apiStore.get(`/productos/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener producto')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener producto:', error)
      throw error
    }
  }

  const obtenerProductoPorSku = async (sku: string): Promise<Producto> => {
    try {
      const response = await apiStore.get(`/productos/sku/${sku}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener producto por SKU')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener producto por SKU:', error)
      throw error
    }
  }

  const crearProducto = async (producto: ProductoCreate): Promise<Producto> => {
    try {
      const response = await apiStore.post('/productos', producto)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear producto')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear producto:', error)
      throw error
    }
  }

  const actualizarProducto = async (id: number, producto: ProductoUpdate): Promise<Producto> => {
    try {
      const response = await apiStore.put(`/productos/${id}`, producto)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar producto')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar producto:', error)
      throw error
    }
  }

  const eliminarProducto = async (id: number, permanente: boolean = false): Promise<void> => {
    try {
      const params = new URLSearchParams()
      params.append('permanente', permanente.toString())

      const response = await apiStore.delete(`/productos/${id}?${params.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar producto')
      }
    } catch (error) {
      console.error('Error al eliminar producto:', error)
      throw error
    }
  }

  const activarProducto = async (id: number): Promise<Producto> => {
    try {
      const response = await apiStore.patch(`/productos/${id}/activar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al activar producto')
      }
      return response.data.producto
    } catch (error) {
      console.error('Error al activar producto:', error)
      throw error
    }
  }

  // Métodos para datos relacionados
  const obtenerMarcas = async (): Promise<Marca[]> => {
    try {
      const response = await apiStore.get('/marcas?activo=true')
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener marcas')
      }
      marcas.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener marcas:', error)
      throw error
    }
  }

  const obtenerTiposProducto = async (): Promise<TipoProducto[]> => {
    try {
      const response = await apiStore.get('/tipos-producto?activo=true')
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener tipos de producto')
      }
      tiposProducto.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener tipos de producto:', error)
      throw error
    }
  }

  const obtenerUnidadesMedida = async (): Promise<UnidadMedida[]> => {
    try {
      const response = await apiStore.get('/unidades-medida?activo=true')
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener unidades de medida')
      }
      unidadesMedida.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener unidades de medida:', error)
      throw error
    }
  }

  // CRUD Producto Proveedores
  const obtenerProductoProveedores = async (productoId: number, params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<ProductoProveedor[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/producto-proveedores/producto/${productoId}?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener proveedores del producto')
      }
      productoProveedores.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener proveedores del producto:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerProductoProveedor = async (id: number): Promise<ProductoProveedor> => {
    try {
      const response = await apiStore.get(`/producto-proveedores/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener relación producto-proveedor')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener relación producto-proveedor:', error)
      throw error
    }
  }

  const crearProductoProveedor = async (productoProveedor: ProductoProveedorCreate): Promise<ProductoProveedor> => {
    try {
      const response = await apiStore.post('/producto-proveedores', productoProveedor)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear relación producto-proveedor')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear relación producto-proveedor:', error)
      throw error
    }
  }

  const actualizarProductoProveedor = async (id: number, productoProveedor: ProductoProveedorUpdate): Promise<ProductoProveedor> => {
    try {
      const response = await apiStore.put(`/producto-proveedores/${id}`, productoProveedor)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar relación producto-proveedor')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar relación producto-proveedor:', error)
      throw error
    }
  }

  const eliminarProductoProveedor = async (id: number, permanente: boolean = false): Promise<void> => {
    try {
      const params = new URLSearchParams()
      params.append('permanente', permanente.toString())

      const response = await apiStore.delete(`/producto-proveedores/${id}?${params.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar relación producto-proveedor')
      }
    } catch (error) {
      console.error('Error al eliminar relación producto-proveedor:', error)
      throw error
    }
  }

  const activarProductoProveedor = async (id: number): Promise<ProductoProveedor> => {
    try {
      const response = await apiStore.patch(`/producto-proveedores/${id}/activar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al activar relación producto-proveedor')
      }
      return response.data.producto_proveedor
    } catch (error) {
      console.error('Error al activar relación producto-proveedor:', error)
      throw error
    }
  }

  const establecerProveedorPrincipal = async (id: number): Promise<ProductoProveedor> => {
    try {
      const response = await apiStore.patch(`/producto-proveedores/${id}/principal`)
      if (!response.success) {
        throw new Error(response.error || 'Error al establecer proveedor principal')
      }
      return response.data.producto_proveedor
    } catch (error) {
      console.error('Error al establecer proveedor principal:', error)
      throw error
    }
  }

  const validarVigenciaProveedores = async (productoId: number): Promise<{
    vigentes: number
    vencidos: number
    por_vencer: number
  }> => {
    try {
      const response = await apiStore.get(`/producto-proveedores/producto/${productoId}/vigencia`)
      if (!response.success) {
        throw new Error(response.error || 'Error al validar vigencia de proveedores')
      }
      return response.data
    } catch (error) {
      console.error('Error al validar vigencia de proveedores:', error)
      throw error
    }
  }

  // CRUD Producto Ubicaciones
  const obtenerProductoUbicaciones = async (productoId: number, params?: {
    skip?: number
    limit?: number
    activo?: boolean
    bodega_id?: number
  }): Promise<ProductoUbicacion[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')
      if (params?.bodega_id !== undefined) queryParams.append('bodega_id', params.bodega_id.toString())

      const url = `/producto-ubicaciones/producto/${productoId}?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener ubicaciones del producto')
      }
      productoUbicaciones.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener ubicaciones del producto:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerProductoUbicacion = async (id: number): Promise<ProductoUbicacion> => {
    try {
      const response = await apiStore.get(`/producto-ubicaciones/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener ubicación del producto')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener ubicación del producto:', error)
      throw error
    }
  }

  const crearProductoUbicacion = async (productoUbicacion: ProductoUbicacionCreate): Promise<ProductoUbicacion> => {
    try {
      const response = await apiStore.post('/producto-ubicaciones', productoUbicacion)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear ubicación del producto')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear ubicación del producto:', error)
      throw error
    }
  }

  const actualizarProductoUbicacion = async (id: number, productoUbicacion: ProductoUbicacionUpdate): Promise<ProductoUbicacion> => {
    try {
      const response = await apiStore.put(`/producto-ubicaciones/${id}`, productoUbicacion)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar ubicación del producto')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar ubicación del producto:', error)
      throw error
    }
  }

  const eliminarProductoUbicacion = async (id: number, permanente: boolean = false): Promise<void> => {
    try {
      const params = new URLSearchParams()
      params.append('permanente', permanente.toString())

      const response = await apiStore.delete(`/producto-ubicaciones/${id}?${params.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar ubicación del producto')
      }
    } catch (error) {
      console.error('Error al eliminar ubicación del producto:', error)
      throw error
    }
  }

  const transferirProductoUbicacion = async (
    id: number,
    nuevaUbicacion: {
      id_bodega: number
      id_pasillo?: number
      id_estante?: number
      cantidad: number
      motivo?: string
    }
  ): Promise<ProductoUbicacion> => {
    try {
      const response = await apiStore.post(`/producto-ubicaciones/${id}/transferir`, nuevaUbicacion)
      if (!response.success) {
        throw new Error(response.error || 'Error al transferir producto')
      }
      return response.data
    } catch (error) {
      console.error('Error al transferir producto:', error)
      throw error
    }
  }

  const ajustarCantidadUbicacion = async (
    id: number,
    ajuste: {
      cantidad_nueva: number
      motivo: string
      tipo_ajuste: 'conteo' | 'ajuste' | 'entrada' | 'salida'
    }
  ): Promise<ProductoUbicacion> => {
    try {
      const response = await apiStore.post(`/producto-ubicaciones/${id}/ajustar`, ajuste)
      if (!response.success) {
        throw new Error(response.error || 'Error al ajustar cantidad')
      }
      return response.data
    } catch (error) {
      console.error('Error al ajustar cantidad:', error)
      throw error
    }
  }

  const reservarCantidadUbicacion = async (
    id: number,
    reserva: {
      cantidad_reservar: number
      motivo?: string
    }
  ): Promise<ProductoUbicacion> => {
    try {
      const response = await apiStore.post(`/producto-ubicaciones/${id}/reservar`, reserva)
      if (!response.success) {
        throw new Error(response.error || 'Error al reservar cantidad')
      }
      return response.data
    } catch (error) {
      console.error('Error al reservar cantidad:', error)
      throw error
    }
  }

  const liberarReservaUbicacion = async (
    id: number,
    liberacion: {
      cantidad_liberar: number
      motivo?: string
    }
  ): Promise<ProductoUbicacion> => {
    try {
      const response = await apiStore.post(`/producto-ubicaciones/${id}/liberar-reserva`, liberacion)
      if (!response.success) {
        throw new Error(response.error || 'Error al liberar reserva')
      }
      return response.data
    } catch (error) {
      console.error('Error al liberar reserva:', error)
      throw error
    }
  }

  const obtenerMovimientosUbicacion = async (ubicacionId: number, params?: {
    skip?: number
    limit?: number
    fecha_desde?: string
    fecha_hasta?: string
  }): Promise<MovimientoUbicacion[]> => {
    try {
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.fecha_desde) queryParams.append('fecha_desde', params.fecha_desde)
      if (params?.fecha_hasta) queryParams.append('fecha_hasta', params.fecha_hasta)

      const url = `/producto-ubicaciones/${ubicacionId}/movimientos?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener movimientos de ubicación')
      }
      movimientosUbicacion.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener movimientos de ubicación:', error)
      throw error
    }
  }

  const consolidarStockProducto = async (productoId: number): Promise<{
    stock_total: number
    stock_disponible: number
    stock_reservado: number
    ubicaciones_activas: number
  }> => {
    try {
      const response = await apiStore.get(`/productos/${productoId}/stock/consolidar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al consolidar stock del producto')
      }
      return response.data
    } catch (error) {
      console.error('Error al consolidar stock del producto:', error)
      throw error
    }
  }

  return {
    // State
    productos,
    marcas,
    tiposProducto,
    unidadesMedida,
    productoProveedores,
    productoUbicaciones,
    movimientosUbicacion,
    isLoading,

    // Methods - Productos
    obtenerProductos,
    buscarProductos,
    obtenerProducto,
    obtenerProductoPorSku,
    crearProducto,
    actualizarProducto,
    eliminarProducto,
    activarProducto,

    // Methods - Datos relacionados
    obtenerMarcas,
    obtenerTiposProducto,
    obtenerUnidadesMedida,

    // Methods - Producto Proveedores
    obtenerProductoProveedores,
    obtenerProductoProveedor,
    crearProductoProveedor,
    actualizarProductoProveedor,
    eliminarProductoProveedor,
    activarProductoProveedor,
    establecerProveedorPrincipal,
    validarVigenciaProveedores,

    // Methods - Producto Ubicaciones
    obtenerProductoUbicaciones,
    obtenerProductoUbicacion,
    crearProductoUbicacion,
    actualizarProductoUbicacion,
    eliminarProductoUbicacion,
    transferirProductoUbicacion,
    ajustarCantidadUbicacion,
    reservarCantidadUbicacion,
    liberarReservaUbicacion,
    obtenerMovimientosUbicacion,
    consolidarStockProducto
  }
})