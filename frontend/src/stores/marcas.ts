import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface Marca {
  id_marca: number
  nombre_marca: string
  descripcion?: string
  pais_origen?: string
  sitio_web?: string
  contacto_tecnico?: string
  activo: boolean
  fecha_creacion: string
}

export interface MarcaCreate {
  nombre_marca: string
  descripcion?: string
  pais_origen?: string
  sitio_web?: string
  contacto_tecnico?: string
  activo: boolean
}

export interface MarcaUpdate {
  nombre_marca?: string
  descripcion?: string
  pais_origen?: string
  sitio_web?: string
  contacto_tecnico?: string
  activo?: boolean
}

export const useMarcaStore = defineStore('marcas', () => {
  const apiStore = useApiStore()

  const marcas = ref<Marca[]>([])
  const isLoading = ref(false)

  // CRUD Marcas
  const obtenerMarcas = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<Marca[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/marcas?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener marcas')
      }
      marcas.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener marcas:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const buscarMarcas = async (
    searchTerm: string,
    params?: {
      skip?: number
      limit?: number
    }
  ): Promise<Marca[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()
      queryParams.append('q', searchTerm)

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())

      const response = await apiStore.get(`/marcas/search?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al buscar marcas')
      }
      return response.data
    } catch (error) {
      console.error('Error al buscar marcas:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerMarca = async (id: number): Promise<Marca> => {
    try {
      const response = await apiStore.get(`/marcas/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener marca')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener marca:', error)
      throw error
    }
  }

  const obtenerMarcaPorNombre = async (nombre: string): Promise<Marca> => {
    try {
      const response = await apiStore.get(`/marcas/nombre/${nombre}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener marca por nombre')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener marca por nombre:', error)
      throw error
    }
  }

  const crearMarca = async (marca: MarcaCreate): Promise<Marca> => {
    try {
      const response = await apiStore.post('/marcas', marca)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear marca')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear marca:', error)
      throw error
    }
  }

  const actualizarMarca = async (id: number, marca: MarcaUpdate): Promise<Marca> => {
    try {
      const response = await apiStore.put(`/marcas/${id}`, marca)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar marca')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar marca:', error)
      throw error
    }
  }

  const eliminarMarca = async (id: number): Promise<void> => {
    try {
      const response = await apiStore.delete(`/marcas/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar marca')
      }
    } catch (error) {
      console.error('Error al eliminar marca:', error)
      throw error
    }
  }

  const toggleEstadoMarca = async (id: number): Promise<Marca> => {
    try {
      const response = await apiStore.patch(`/marcas/${id}/toggle`)
      if (!response.success) {
        throw new Error(response.error || 'Error al cambiar estado de marca')
      }
      return response.data
    } catch (error) {
      console.error('Error al cambiar estado de marca:', error)
      throw error
    }
  }

  const contarMarcas = async (activo?: boolean): Promise<{ total_marcas: number }> => {
    try {
      const queryParams = new URLSearchParams()
      if (activo !== undefined) queryParams.append('activo', activo === true ? 'true' : 'false')

      const url = `/marcas/stats/count?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al contar marcas')
      }
      return response.data
    } catch (error) {
      console.error('Error al contar marcas:', error)
      throw error
    }
  }

  const obtenerEstadisticas = async (): Promise<{
    total: number
    activas: number
    inactivas: number
  }> => {
    try {
      const [totalRes, activasRes, inactivasRes] = await Promise.all([
        contarMarcas(),
        contarMarcas(true),
        contarMarcas(false)
      ])

      return {
        total: totalRes.total_marcas,
        activas: activasRes.total_marcas,
        inactivas: inactivasRes.total_marcas
      }
    } catch (error) {
      console.error('Error al obtener estadísticas:', error)
      throw error
    }
  }

  return {
    // State
    marcas,
    isLoading,

    // Methods
    obtenerMarcas,
    buscarMarcas,
    obtenerMarca,
    obtenerMarcaPorNombre,
    crearMarca,
    actualizarMarca,
    eliminarMarca,
    toggleEstadoMarca,
    contarMarcas,
    obtenerEstadisticas
  }
})