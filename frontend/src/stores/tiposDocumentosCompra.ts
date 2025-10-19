import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface TipoDocumentoCompra {
  id_tipo_documento: number
  nombre: string
  codigo_dte?: string
  descripcion?: string
  requiere_folio: boolean
  activo: boolean
  fecha_creacion: string
  fecha_actualizacion: string
}

export interface TipoDocumentoCompraCreate {
  nombre: string
  codigo_dte?: string
  descripcion?: string
  requiere_folio?: boolean
  activo?: boolean
}

export interface TipoDocumentoCompraUpdate {
  nombre?: string
  codigo_dte?: string
  descripcion?: string
  requiere_folio?: boolean
  activo?: boolean
}

export const useTiposDocumentosCompraStore = defineStore('tiposDocumentosCompra', () => {
  const apiStore = useApiStore()

  const tiposDocumentos = ref<TipoDocumentoCompra[]>([])
  const isLoading = ref(false)

  const obtenerTiposDocumentos = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<TipoDocumentoCompra[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/tipos-documentos-compra?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener tipos de documentos')
      }
      tiposDocumentos.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener tipos de documentos:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerTipoDocumento = async (id: number): Promise<TipoDocumentoCompra> => {
    try {
      const response = await apiStore.get(`/tipos-documentos-compra/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener tipo de documento')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener tipo de documento:', error)
      throw error
    }
  }

  const obtenerTipoDocumentoPorNombre = async (nombre: string): Promise<TipoDocumentoCompra> => {
    try {
      const response = await apiStore.get(`/tipos-documentos-compra/nombre/${nombre}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener tipo de documento por nombre')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener tipo de documento por nombre:', error)
      throw error
    }
  }

  const obtenerTipoDocumentoPorCodigoDTE = async (codigoDTE: string): Promise<TipoDocumentoCompra> => {
    try {
      const response = await apiStore.get(`/tipos-documentos-compra/codigo-dte/${codigoDTE}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener tipo de documento por código DTE')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener tipo de documento por código DTE:', error)
      throw error
    }
  }

  const crearTipoDocumento = async (tipoDocumento: TipoDocumentoCompraCreate): Promise<TipoDocumentoCompra> => {
    try {
      const response = await apiStore.post('/tipos-documentos-compra', tipoDocumento)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear tipo de documento')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear tipo de documento:', error)
      throw error
    }
  }

  const actualizarTipoDocumento = async (id: number, tipoDocumento: TipoDocumentoCompraUpdate): Promise<TipoDocumentoCompra> => {
    try {
      const response = await apiStore.put(`/tipos-documentos-compra/${id}`, tipoDocumento)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar tipo de documento')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar tipo de documento:', error)
      throw error
    }
  }

  const eliminarTipoDocumento = async (id: number): Promise<void> => {
    try {
      const response = await apiStore.delete(`/tipos-documentos-compra/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar tipo de documento')
      }
    } catch (error) {
      console.error('Error al eliminar tipo de documento:', error)
      throw error
    }
  }

  const toggleEstadoTipoDocumento = async (id: number): Promise<TipoDocumentoCompra> => {
    try {
      const response = await apiStore.patch(`/tipos-documentos-compra/${id}/toggle`)
      if (!response.success) {
        throw new Error(response.error || 'Error al cambiar estado del tipo de documento')
      }
      return response.data
    } catch (error) {
      console.error('Error al cambiar estado del tipo de documento:', error)
      throw error
    }
  }

  const buscarTiposDocumentos = async (
    searchTerm: string,
    params?: {
      activo?: boolean
    }
  ): Promise<TipoDocumentoCompra[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()
      queryParams.append('q', searchTerm)

      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const response = await apiStore.get(`/tipos-documentos-compra/search?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al buscar tipos de documentos')
      }
      return response.data
    } catch (error) {
      console.error('Error al buscar tipos de documentos:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const contarTiposDocumentos = async (params?: {
    activo?: boolean
  }): Promise<{ total_tipos_documentos: number }> => {
    try {
      const queryParams = new URLSearchParams()

      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const response = await apiStore.get(`/tipos-documentos-compra/stats/count?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al contar tipos de documentos')
      }
      return response.data
    } catch (error) {
      console.error('Error al contar tipos de documentos:', error)
      throw error
    }
  }

  return {
    // State
    tiposDocumentos,
    isLoading,

    // Methods
    obtenerTiposDocumentos,
    obtenerTipoDocumento,
    obtenerTipoDocumentoPorNombre,
    obtenerTipoDocumentoPorCodigoDTE,
    crearTipoDocumento,
    actualizarTipoDocumento,
    eliminarTipoDocumento,
    toggleEstadoTipoDocumento,
    buscarTiposDocumentos,
    contarTiposDocumentos
  }
})
