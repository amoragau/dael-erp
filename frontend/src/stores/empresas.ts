import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface Empresa {
  id_empresa: number
  rut_empresa: string
  razon_social: string
  nombre_fantasia?: string
  giro?: string
  direccion?: string
  comuna?: string
  ciudad?: string
  region?: string
  telefono?: string
  email?: string
  sitio_web?: string
  logo_url?: string
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string
  usuario_creacion?: number
  usuario_modificacion?: number
}

export interface EmpresaCreate {
  rut_empresa: string
  razon_social: string
  nombre_fantasia?: string
  giro?: string
  direccion?: string
  comuna?: string
  ciudad?: string
  region?: string
  telefono?: string
  email?: string
  sitio_web?: string
  logo_url?: string
  activo?: boolean
}

export interface EmpresaUpdate {
  rut_empresa?: string
  razon_social?: string
  nombre_fantasia?: string
  giro?: string
  direccion?: string
  comuna?: string
  ciudad?: string
  region?: string
  telefono?: string
  email?: string
  sitio_web?: string
  logo_url?: string
  activo?: boolean
}

export const useEmpresaStore = defineStore('empresas', () => {
  const apiStore = useApiStore()

  const empresas = ref<Empresa[]>([])
  const isLoading = ref(false)

  const obtenerEmpresas = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<Empresa[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/empresas?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener empresas')
      }
      empresas.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener empresas:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerEmpresasActivas = async (): Promise<Empresa[]> => {
    try {
      isLoading.value = true
      const response = await apiStore.get('/empresas/activos')
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener empresas activas')
      }
      empresas.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener empresas activas:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const buscarEmpresas = async (
    searchTerm: string,
    params?: {
      activo?: boolean
    }
  ): Promise<Empresa[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()
      queryParams.append('q', searchTerm)

      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const response = await apiStore.get(`/empresas/buscar?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al buscar empresas')
      }
      return response.data
    } catch (error) {
      console.error('Error al buscar empresas:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerEmpresa = async (id: number): Promise<Empresa> => {
    try {
      const response = await apiStore.get(`/empresas/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener empresa')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener empresa:', error)
      throw error
    }
  }

  const crearEmpresa = async (empresa: EmpresaCreate): Promise<Empresa> => {
    try {
      const response = await apiStore.post('/empresas', empresa)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear empresa')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear empresa:', error)
      throw error
    }
  }

  const actualizarEmpresa = async (id: number, empresa: EmpresaUpdate): Promise<Empresa> => {
    try {
      const response = await apiStore.put(`/empresas/${id}`, empresa)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar empresa')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar empresa:', error)
      throw error
    }
  }

  const eliminarEmpresa = async (id: number): Promise<void> => {
    try {
      const response = await apiStore.delete(`/empresas/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar empresa')
      }
    } catch (error) {
      console.error('Error al eliminar empresa:', error)
      throw error
    }
  }

  return {
    // State
    empresas,
    isLoading,

    // Methods
    obtenerEmpresas,
    obtenerEmpresasActivas,
    buscarEmpresas,
    obtenerEmpresa,
    crearEmpresa,
    actualizarEmpresa,
    eliminarEmpresa
  }
})
