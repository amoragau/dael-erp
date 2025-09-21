import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface TipoProducto {
  id_tipo_producto: number
  id_subcategoria: number
  codigo_tipo: string
  nombre_tipo: string
  descripcion?: string
  activo: boolean
}

export interface TipoProductoCreate {
  id_subcategoria: number
  codigo_tipo: string
  nombre_tipo: string
  descripcion?: string
  activo: boolean
}

export interface TipoProductoUpdate {
  id_subcategoria?: number
  codigo_tipo?: string
  nombre_tipo?: string
  descripcion?: string
  activo?: boolean
}

export interface TipoProductoWithSubcategoria extends TipoProducto {
  subcategoria?: {
    id_subcategoria: number
    codigo_subcategoria: string
    nombre_subcategoria: string
    categoria?: {
      id_categoria: number
      codigo_categoria: string
      nombre_categoria: string
    }
  }
}

export const useTipoProductoStore = defineStore('tiposProducto', () => {
  const apiStore = useApiStore()

  const tiposProducto = ref<TipoProducto[]>([])
  const isLoading = ref(false)

  // CRUD Tipos de Producto
  const obtenerTiposProducto = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<TipoProducto[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/tipos-producto?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener tipos de producto')
      }
      tiposProducto.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener tipos de producto:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerTipoProducto = async (id: number): Promise<TipoProductoWithSubcategoria> => {
    try {
      const response = await apiStore.get(`/tipos-producto/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener tipo de producto')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener tipo de producto:', error)
      throw error
    }
  }

  const obtenerTipoProductoPorCodigo = async (codigo: string): Promise<TipoProductoWithSubcategoria> => {
    try {
      const response = await apiStore.get(`/tipos-producto/codigo/${codigo}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener tipo de producto por código')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener tipo de producto por código:', error)
      throw error
    }
  }

  const obtenerTiposProductoPorSubcategoria = async (
    subcategoriaId: number,
    params?: {
      skip?: number
      limit?: number
      activo?: boolean
    }
  ): Promise<TipoProducto[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/tipos-producto/por-subcategoria/${subcategoriaId}?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener tipos de producto por subcategoría')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener tipos de producto por subcategoría:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const crearTipoProducto = async (tipoProducto: TipoProductoCreate): Promise<TipoProducto> => {
    try {
      const response = await apiStore.post('/tipos-producto', tipoProducto)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear tipo de producto')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear tipo de producto:', error)
      throw error
    }
  }

  const crearTiposProductoMasivos = async (tiposProducto: TipoProductoCreate[]): Promise<TipoProducto[]> => {
    try {
      const response = await apiStore.post('/tipos-producto/bulk', tiposProducto)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear tipos de producto masivos')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear tipos de producto masivos:', error)
      throw error
    }
  }

  const actualizarTipoProducto = async (id: number, tipoProducto: TipoProductoUpdate): Promise<TipoProducto> => {
    try {
      const response = await apiStore.put(`/tipos-producto/${id}`, tipoProducto)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar tipo de producto')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar tipo de producto:', error)
      throw error
    }
  }

  const eliminarTipoProducto = async (id: number, permanente: boolean = false): Promise<void> => {
    try {
      const queryParams = new URLSearchParams()
      if (permanente) queryParams.append('permanente', 'true')

      const url = `/tipos-producto/${id}?${queryParams.toString()}`
      const response = await apiStore.delete(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar tipo de producto')
      }
    } catch (error) {
      console.error('Error al eliminar tipo de producto:', error)
      throw error
    }
  }

  const activarTipoProducto = async (id: number): Promise<TipoProducto> => {
    try {
      const response = await apiStore.patch(`/tipos-producto/${id}/activar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al activar tipo de producto')
      }
      return response.data.tipo_producto
    } catch (error) {
      console.error('Error al activar tipo de producto:', error)
      throw error
    }
  }

  const obtenerEstadisticas = async (): Promise<{
    total: number
    activos: number
    inactivos: number
  }> => {
    try {
      const response = await apiStore.get('/tipos-producto/estadisticas/resumen')
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener estadísticas')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas:', error)
      throw error
    }
  }

  return {
    // State
    tiposProducto,
    isLoading,

    // Methods
    obtenerTiposProducto,
    obtenerTipoProducto,
    obtenerTipoProductoPorCodigo,
    obtenerTiposProductoPorSubcategoria,
    crearTipoProducto,
    crearTiposProductoMasivos,
    actualizarTipoProducto,
    eliminarTipoProducto,
    activarTipoProducto,
    obtenerEstadisticas
  }
})