import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface Bodega {
  id_bodega: number
  codigo_bodega: string
  nombre_bodega: string
  descripcion?: string
  temperatura_min?: number
  temperatura_max?: number
  humedad_max?: number
  requiere_certificacion: boolean
  activo: boolean
}

export interface BodegaCreate {
  codigo_bodega: string
  nombre_bodega: string
  descripcion?: string
  temperatura_min?: number
  temperatura_max?: number
  humedad_max?: number
  requiere_certificacion: boolean
  activo: boolean
}

export interface BodegaUpdate {
  codigo_bodega?: string
  nombre_bodega?: string
  descripcion?: string
  temperatura_min?: number
  temperatura_max?: number
  humedad_max?: number
  requiere_certificacion?: boolean
  activo?: boolean
}

export interface Pasillo {
  id_pasillo: number
  id_bodega: number
  numero_pasillo: number
  nombre_pasillo?: string
  longitud_metros?: number
  activo: boolean
}

export interface PasilloCreate {
  id_bodega: number
  numero_pasillo: number
  nombre_pasillo?: string
  longitud_metros?: number
  activo: boolean
}

export interface PasilloUpdate {
  id_bodega?: number
  numero_pasillo?: number
  nombre_pasillo?: string
  longitud_metros?: number
  activo?: boolean
}

export interface Estante {
  id_estante: number
  id_pasillo: number
  codigo_estante: string
  altura_metros?: number
  capacidad_peso_kg?: number
  activo: boolean
}

export interface EstanteCreate {
  id_pasillo: number
  codigo_estante: string
  altura_metros?: number
  capacidad_peso_kg?: number
  activo: boolean
}

export interface EstanteUpdate {
  id_pasillo?: number
  codigo_estante?: string
  altura_metros?: number
  capacidad_peso_kg?: number
  activo?: boolean
}

export const useBodegaStore = defineStore('bodegas', () => {
  const apiStore = useApiStore()

  const bodegas = ref<Bodega[]>([])
  const pasillos = ref<Pasillo[]>([])
  const estantes = ref<Estante[]>([])
  const isLoading = ref(false)

  // CRUD Bodegas
  const obtenerBodegas = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<Bodega[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/bodegas?${queryParams.toString()}`
      console.log('URL construida bodegas:', url, 'params recibidos:', params)
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener bodegas')
      }
      bodegas.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener bodegas:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const buscarBodegas = async (
    searchTerm: string,
    params?: {
      skip?: number
      limit?: number
    }
  ): Promise<Bodega[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()
      queryParams.append('q', searchTerm)

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())

      const response = await apiStore.get(`/bodegas/search?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al buscar bodegas')
      }
      return response.data
    } catch (error) {
      console.error('Error al buscar bodegas:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerBodega = async (id: number): Promise<Bodega> => {
    try {
      const response = await apiStore.get(`/bodegas/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener bodega')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener bodega:', error)
      throw error
    }
  }

  const obtenerBodegaPorCodigo = async (codigo: string): Promise<Bodega> => {
    try {
      const response = await apiStore.get(`/bodegas/codigo/${codigo}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener bodega por código')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener bodega por código:', error)
      throw error
    }
  }

  const crearBodega = async (bodega: BodegaCreate): Promise<Bodega> => {
    try {
      const response = await apiStore.post('/bodegas', bodega)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear bodega')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear bodega:', error)
      throw error
    }
  }

  const actualizarBodega = async (id: number, bodega: BodegaUpdate): Promise<Bodega> => {
    try {
      const response = await apiStore.put(`/bodegas/${id}`, bodega)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar bodega')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar bodega:', error)
      throw error
    }
  }

  const eliminarBodega = async (id: number): Promise<void> => {
    try {
      const response = await apiStore.delete(`/bodegas/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar bodega')
      }
    } catch (error) {
      console.error('Error al eliminar bodega:', error)
      throw error
    }
  }

  const toggleEstadoBodega = async (id: number): Promise<Bodega> => {
    try {
      const response = await apiStore.patch(`/bodegas/${id}/toggle`)
      if (!response.success) {
        throw new Error(response.error || 'Error al cambiar estado de bodega')
      }
      return response.data
    } catch (error) {
      console.error('Error al cambiar estado de bodega:', error)
      throw error
    }
  }

  // CRUD Pasillos
  const obtenerPasillosPorBodega = async (bodegaId: number, params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<Pasillo[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/pasillos/bodega/${bodegaId}/pasillos?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener pasillos')
      }
      pasillos.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener pasillos:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerPasillo = async (id: number): Promise<Pasillo> => {
    try {
      const response = await apiStore.get(`/pasillos/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener pasillo')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener pasillo:', error)
      throw error
    }
  }

  const crearPasillo = async (pasillo: PasilloCreate): Promise<Pasillo> => {
    try {
      const response = await apiStore.post('/pasillos', pasillo)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear pasillo')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear pasillo:', error)
      throw error
    }
  }

  const actualizarPasillo = async (id: number, pasillo: PasilloUpdate): Promise<Pasillo> => {
    try {
      const response = await apiStore.put(`/pasillos/${id}`, pasillo)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar pasillo')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar pasillo:', error)
      throw error
    }
  }

  const eliminarPasillo = async (id: number): Promise<void> => {
    try {
      const response = await apiStore.delete(`/pasillos/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar pasillo')
      }
    } catch (error) {
      console.error('Error al eliminar pasillo:', error)
      throw error
    }
  }

  const toggleEstadoPasillo = async (id: number): Promise<Pasillo> => {
    try {
      const response = await apiStore.patch(`/pasillos/${id}/toggle`)
      if (!response.success) {
        throw new Error(response.error || 'Error al cambiar estado de pasillo')
      }
      return response.data
    } catch (error) {
      console.error('Error al cambiar estado de pasillo:', error)
      throw error
    }
  }

  // CRUD Estantes
  const obtenerEstantesPorPasillo = async (pasilloId: number, params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<Estante[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/estantes/pasillo/${pasilloId}/estantes?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener estantes')
      }
      estantes.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener estantes:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerEstante = async (id: number): Promise<Estante> => {
    try {
      const response = await apiStore.get(`/estantes/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener estante')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener estante:', error)
      throw error
    }
  }

  const crearEstante = async (estante: EstanteCreate): Promise<Estante> => {
    try {
      const response = await apiStore.post('/estantes', estante)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear estante')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear estante:', error)
      throw error
    }
  }

  const actualizarEstante = async (id: number, estante: EstanteUpdate): Promise<Estante> => {
    try {
      const response = await apiStore.put(`/estantes/${id}`, estante)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar estante')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar estante:', error)
      throw error
    }
  }

  const eliminarEstante = async (id: number): Promise<void> => {
    try {
      const response = await apiStore.delete(`/estantes/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar estante')
      }
    } catch (error) {
      console.error('Error al eliminar estante:', error)
      throw error
    }
  }

  const toggleEstadoEstante = async (id: number): Promise<Estante> => {
    try {
      const response = await apiStore.patch(`/estantes/${id}/toggle`)
      if (!response.success) {
        throw new Error(response.error || 'Error al cambiar estado de estante')
      }
      return response.data
    } catch (error) {
      console.error('Error al cambiar estado de estante:', error)
      throw error
    }
  }

  return {
    // State
    bodegas,
    pasillos,
    estantes,
    isLoading,

    // Methods - Bodegas
    obtenerBodegas,
    buscarBodegas,
    obtenerBodega,
    obtenerBodegaPorCodigo,
    crearBodega,
    actualizarBodega,
    eliminarBodega,
    toggleEstadoBodega,

    // Methods - Pasillos
    obtenerPasillosPorBodega,
    obtenerPasillo,
    crearPasillo,
    actualizarPasillo,
    eliminarPasillo,
    toggleEstadoPasillo,

    // Methods - Estantes
    obtenerEstantesPorPasillo,
    obtenerEstante,
    crearEstante,
    actualizarEstante,
    eliminarEstante,
    toggleEstadoEstante
  }
})