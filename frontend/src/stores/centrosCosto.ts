import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface CentroCosto {
  id_centro_costo: number
  codigo_centro_costo: string
  nombre_centro_costo: string
  descripcion?: string
  id_responsable?: number
  presupuesto_anual: number
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string
  usuario_creacion?: number
  usuario_modificacion?: number
}

export interface CentroCostoCreate {
  codigo_centro_costo: string
  nombre_centro_costo: string
  descripcion?: string
  id_responsable?: number
  presupuesto_anual?: number
  activo?: boolean
}

export interface CentroCostoUpdate {
  codigo_centro_costo?: string
  nombre_centro_costo?: string
  descripcion?: string
  id_responsable?: number
  presupuesto_anual?: number
  activo?: boolean
}

export const useCentroCostoStore = defineStore('centros-costo', () => {
  const apiStore = useApiStore()

  const centrosCosto = ref<CentroCosto[]>([])
  const isLoading = ref(false)

  const obtenerCentrosCosto = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<CentroCosto[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/centros-costo?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener centros de costo')
      }
      centrosCosto.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener centros de costo:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerCentrosCostoActivos = async (): Promise<CentroCosto[]> => {
    try {
      isLoading.value = true
      const response = await apiStore.get('/centros-costo/activos')
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener centros de costo activos')
      }
      centrosCosto.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener centros de costo activos:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const buscarCentrosCosto = async (
    searchTerm: string,
    params?: {
      activo?: boolean
    }
  ): Promise<CentroCosto[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()
      queryParams.append('q', searchTerm)

      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const response = await apiStore.get(`/centros-costo/buscar?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al buscar centros de costo')
      }
      return response.data
    } catch (error) {
      console.error('Error al buscar centros de costo:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerCentroCosto = async (id: number): Promise<CentroCosto> => {
    try {
      const response = await apiStore.get(`/centros-costo/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener centro de costo')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener centro de costo:', error)
      throw error
    }
  }

  const crearCentroCosto = async (centroCosto: CentroCostoCreate): Promise<CentroCosto> => {
    try {
      const response = await apiStore.post('/centros-costo', centroCosto)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear centro de costo')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear centro de costo:', error)
      throw error
    }
  }

  const actualizarCentroCosto = async (id: number, centroCosto: CentroCostoUpdate): Promise<CentroCosto> => {
    try {
      const response = await apiStore.put(`/centros-costo/${id}`, centroCosto)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar centro de costo')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar centro de costo:', error)
      throw error
    }
  }

  const eliminarCentroCosto = async (id: number): Promise<void> => {
    try {
      const response = await apiStore.delete(`/centros-costo/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar centro de costo')
      }
    } catch (error) {
      console.error('Error al eliminar centro de costo:', error)
      throw error
    }
  }

  return {
    // State
    centrosCosto,
    isLoading,

    // Methods
    obtenerCentrosCosto,
    obtenerCentrosCostoActivos,
    buscarCentrosCosto,
    obtenerCentroCosto,
    crearCentroCosto,
    actualizarCentroCosto,
    eliminarCentroCosto
  }
})
