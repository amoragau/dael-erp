import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface Categoria {
  id_categoria: number
  codigo_categoria: string
  nombre_categoria: string
  descripcion?: string
  activo: boolean
  subcategorias?: Subcategoria[]
}

export interface CategoriaCreate {
  codigo_categoria: string
  nombre_categoria: string
  descripcion?: string
  activo: boolean
}

export interface CategoriaUpdate {
  codigo_categoria?: string
  nombre_categoria?: string
  descripcion?: string
  activo?: boolean
}

export interface Subcategoria {
  id_subcategoria: number
  id_categoria: number
  codigo_subcategoria: string
  nombre_subcategoria: string
  descripcion?: string
  activo: boolean
  categoria?: Categoria
}

export interface SubcategoriaCreate {
  id_categoria: number
  codigo_subcategoria: string
  nombre_subcategoria: string
  descripcion?: string
  activo: boolean
}

export interface SubcategoriaUpdate {
  id_categoria?: number
  codigo_subcategoria?: string
  nombre_subcategoria?: string
  descripcion?: string
  activo?: boolean
}

export const useCategoriaStore = defineStore('categorias', () => {
  const apiStore = useApiStore()

  const categorias = ref<Categoria[]>([])
  const subcategorias = ref<Subcategoria[]>([])
  const isLoading = ref(false)

  // CRUD Categorías
  const obtenerCategorias = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<Categoria[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/categorias?${queryParams.toString()}`
      console.log('URL construida:', url, 'params recibidos:', params)
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener categorías')
      }
      categorias.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener categorías:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerCategoria = async (id: number): Promise<Categoria> => {
    try {
      const response = await apiStore.get(`/categorias/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener categoría')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener categoría:', error)
      throw error
    }
  }

  const obtenerCategoriaPorCodigo = async (codigo: string): Promise<Categoria> => {
    try {
      const response = await apiStore.get(`/categorias/codigo/${codigo}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener categoría por código')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener categoría por código:', error)
      throw error
    }
  }

  const crearCategoria = async (categoria: CategoriaCreate): Promise<Categoria> => {
    try {
      const response = await apiStore.post('/categorias', categoria)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear categoría')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear categoría:', error)
      throw error
    }
  }

  const actualizarCategoria = async (id: number, categoria: CategoriaUpdate): Promise<Categoria> => {
    try {
      const response = await apiStore.put(`/categorias/${id}`, categoria)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar categoría')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar categoría:', error)
      throw error
    }
  }

  const eliminarCategoria = async (id: number, permanente: boolean = false): Promise<void> => {
    try {
      const params = new URLSearchParams()
      params.append('permanente', permanente.toString())

      const response = await apiStore.delete(`/categorias/${id}?${params.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar categoría')
      }
    } catch (error) {
      console.error('Error al eliminar categoría:', error)
      throw error
    }
  }

  const activarCategoria = async (id: number): Promise<Categoria> => {
    try {
      const response = await apiStore.patch(`/categorias/${id}/activar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al activar categoría')
      }
      return response.data.categoria
    } catch (error) {
      console.error('Error al activar categoría:', error)
      throw error
    }
  }

  const obtenerEstadisticasCategorias = async () => {
    try {
      const response = await apiStore.get('/categorias/estadisticas/resumen')
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener estadísticas de categorías')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas de categorías:', error)
      throw error
    }
  }

  const crearCategoriasMasivo = async (categorias: CategoriaCreate[]): Promise<Categoria[]> => {
    try {
      const response = await apiStore.post('/categorias/bulk', categorias)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear categorías masivo')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear categorías masivo:', error)
      throw error
    }
  }

  // CRUD Subcategorías
  const obtenerSubcategorias = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<Subcategoria[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo.toString())

      const response = await apiStore.get(`/subcategorias?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener subcategorías')
      }
      subcategorias.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener subcategorías:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerSubcategoria = async (id: number): Promise<Subcategoria> => {
    try {
      const response = await apiStore.get(`/subcategorias/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener subcategoría')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener subcategoría:', error)
      throw error
    }
  }

  const obtenerSubcategoriaPorCodigo = async (codigo: string): Promise<Subcategoria> => {
    try {
      const response = await apiStore.get(`/subcategorias/codigo/${codigo}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener subcategoría por código')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener subcategoría por código:', error)
      throw error
    }
  }

  const obtenerSubcategoriasPorCategoria = async (
    idCategoria: number,
    params?: {
      skip?: number
      limit?: number
      activo?: boolean
    }
  ): Promise<Subcategoria[]> => {
    try {
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo.toString())

      const response = await apiStore.get(`/subcategorias/por-categoria/${idCategoria}?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener subcategorías por categoría')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener subcategorías por categoría:', error)
      throw error
    }
  }

  const crearSubcategoria = async (subcategoria: SubcategoriaCreate): Promise<Subcategoria> => {
    try {
      const response = await apiStore.post('/subcategorias', subcategoria)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear subcategoría')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear subcategoría:', error)
      throw error
    }
  }

  const actualizarSubcategoria = async (id: number, subcategoria: SubcategoriaUpdate): Promise<Subcategoria> => {
    try {
      const response = await apiStore.put(`/subcategorias/${id}`, subcategoria)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar subcategoría')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar subcategoría:', error)
      throw error
    }
  }

  const eliminarSubcategoria = async (id: number, permanente: boolean = false): Promise<void> => {
    try {
      const params = new URLSearchParams()
      params.append('permanente', permanente.toString())

      const response = await apiStore.delete(`/subcategorias/${id}?${params.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar subcategoría')
      }
    } catch (error) {
      console.error('Error al eliminar subcategoría:', error)
      throw error
    }
  }

  const activarSubcategoria = async (id: number): Promise<Subcategoria> => {
    try {
      const response = await apiStore.patch(`/subcategorias/${id}/activar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al activar subcategoría')
      }
      return response.data.subcategoria
    } catch (error) {
      console.error('Error al activar subcategoría:', error)
      throw error
    }
  }

  const obtenerEstadisticasSubcategorias = async () => {
    try {
      const response = await apiStore.get('/subcategorias/estadisticas/resumen')
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener estadísticas de subcategorías')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas de subcategorías:', error)
      throw error
    }
  }

  const crearSubcategoriasMasivo = async (subcategorias: SubcategoriaCreate[]): Promise<Subcategoria[]> => {
    try {
      const response = await apiStore.post('/subcategorias/bulk', subcategorias)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear subcategorías masivo')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear subcategorías masivo:', error)
      throw error
    }
  }

  return {
    // State
    categorias,
    subcategorias,
    isLoading,

    // Categorías
    obtenerCategorias,
    obtenerCategoria,
    obtenerCategoriaPorCodigo,
    crearCategoria,
    actualizarCategoria,
    eliminarCategoria,
    activarCategoria,
    obtenerEstadisticasCategorias,
    crearCategoriasMasivo,

    // Subcategorías
    obtenerSubcategorias,
    obtenerSubcategoria,
    obtenerSubcategoriaPorCodigo,
    obtenerSubcategoriasPorCategoria,
    crearSubcategoria,
    actualizarSubcategoria,
    eliminarSubcategoria,
    activarSubcategoria,
    obtenerEstadisticasSubcategorias,
    crearSubcategoriasMasivo
  }
})