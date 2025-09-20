import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface Categoria {
  id_categoria: number
  codigo: string
  nombre: string
  descripcion?: string
  activo: boolean
}

export interface CategoriaCreate {
  codigo: string
  nombre: string
  descripcion?: string
  activo: boolean
}

export interface CategoriaUpdate {
  codigo?: string
  nombre?: string
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
      if (params?.activo !== undefined) queryParams.append('activo', params.activo.toString())

      const response = await apiStore.apiClient.get(`/categorias?${queryParams.toString()}`)
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
      const response = await apiStore.apiClient.get(`/categorias/${id}`)
      return response.data
    } catch (error) {
      console.error('Error al obtener categoría:', error)
      throw error
    }
  }

  const obtenerCategoriaPorCodigo = async (codigo: string): Promise<Categoria> => {
    try {
      const response = await apiStore.apiClient.get(`/categorias/codigo/${codigo}`)
      return response.data
    } catch (error) {
      console.error('Error al obtener categoría por código:', error)
      throw error
    }
  }

  const crearCategoria = async (categoria: CategoriaCreate): Promise<Categoria> => {
    try {
      const response = await apiStore.apiClient.post('/categorias', categoria)
      return response.data
    } catch (error) {
      console.error('Error al crear categoría:', error)
      throw error
    }
  }

  const actualizarCategoria = async (id: number, categoria: CategoriaUpdate): Promise<Categoria> => {
    try {
      const response = await apiStore.apiClient.put(`/categorias/${id}`, categoria)
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

      await apiStore.apiClient.delete(`/categorias/${id}?${params.toString()}`)
    } catch (error) {
      console.error('Error al eliminar categoría:', error)
      throw error
    }
  }

  const activarCategoria = async (id: number): Promise<Categoria> => {
    try {
      const response = await apiStore.apiClient.patch(`/categorias/${id}/activar`)
      return response.data.categoria
    } catch (error) {
      console.error('Error al activar categoría:', error)
      throw error
    }
  }

  const obtenerEstadisticasCategorias = async () => {
    try {
      const response = await apiStore.apiClient.get('/categorias/estadisticas/resumen')
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas de categorías:', error)
      throw error
    }
  }

  const crearCategoriasMasivo = async (categorias: CategoriaCreate[]): Promise<Categoria[]> => {
    try {
      const response = await apiStore.apiClient.post('/categorias/bulk', categorias)
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

      const response = await apiStore.apiClient.get(`/subcategorias?${queryParams.toString()}`)
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
      const response = await apiStore.apiClient.get(`/subcategorias/${id}`)
      return response.data
    } catch (error) {
      console.error('Error al obtener subcategoría:', error)
      throw error
    }
  }

  const obtenerSubcategoriaPorCodigo = async (codigo: string): Promise<Subcategoria> => {
    try {
      const response = await apiStore.apiClient.get(`/subcategorias/codigo/${codigo}`)
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

      const response = await apiStore.apiClient.get(`/subcategorias/por-categoria/${idCategoria}?${queryParams.toString()}`)
      return response.data
    } catch (error) {
      console.error('Error al obtener subcategorías por categoría:', error)
      throw error
    }
  }

  const crearSubcategoria = async (subcategoria: SubcategoriaCreate): Promise<Subcategoria> => {
    try {
      const response = await apiStore.apiClient.post('/subcategorias', subcategoria)
      return response.data
    } catch (error) {
      console.error('Error al crear subcategoría:', error)
      throw error
    }
  }

  const actualizarSubcategoria = async (id: number, subcategoria: SubcategoriaUpdate): Promise<Subcategoria> => {
    try {
      const response = await apiStore.apiClient.put(`/subcategorias/${id}`, subcategoria)
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

      await apiStore.apiClient.delete(`/subcategorias/${id}?${params.toString()}`)
    } catch (error) {
      console.error('Error al eliminar subcategoría:', error)
      throw error
    }
  }

  const activarSubcategoria = async (id: number): Promise<Subcategoria> => {
    try {
      const response = await apiStore.apiClient.patch(`/subcategorias/${id}/activar`)
      return response.data.subcategoria
    } catch (error) {
      console.error('Error al activar subcategoría:', error)
      throw error
    }
  }

  const obtenerEstadisticasSubcategorias = async () => {
    try {
      const response = await apiStore.apiClient.get('/subcategorias/estadisticas/resumen')
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas de subcategorías:', error)
      throw error
    }
  }

  const crearSubcategoriasMasivo = async (subcategorias: SubcategoriaCreate[]): Promise<Subcategoria[]> => {
    try {
      const response = await apiStore.apiClient.post('/subcategorias/bulk', subcategorias)
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