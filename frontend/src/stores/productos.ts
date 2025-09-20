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
  stock_minimo: number
  stock_maximo: number
  punto_reorden: number
  stock_disponible?: number
  costo_promedio?: number
  precio_venta?: number
  ubicacion_principal?: string
  requiere_lote: boolean
  requiere_numero_serie: boolean
  dias_vida_util?: number

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
  costo_promedio?: number
  precio_venta?: number
  ubicacion_principal?: string
  requiere_lote: boolean
  requiere_numero_serie: boolean
  dias_vida_util?: number

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
  stock_minimo?: number
  stock_maximo?: number
  punto_reorden?: number
  costo_promedio?: number
  precio_venta?: number
  ubicacion_principal?: string
  requiere_lote?: boolean
  requiere_numero_serie?: boolean
  dias_vida_util?: number

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

export const useProductoStore = defineStore('productos', () => {
  const apiStore = useApiStore()

  const productos = ref<Producto[]>([])
  const marcas = ref<Marca[]>([])
  const tiposProducto = ref<TipoProducto[]>([])
  const unidadesMedida = ref<UnidadMedida[]>([])
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

  return {
    // State
    productos,
    marcas,
    tiposProducto,
    unidadesMedida,
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
    obtenerUnidadesMedida
  }
})