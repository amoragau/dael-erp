import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface Proveedor {
  id_proveedor: number
  codigo_proveedor: string
  nombre_proveedor: string
  razon_social?: string
  rfc?: string
  direccion?: string
  telefono?: string
  email?: string
  contacto?: string
  telefono_contacto?: string
  email_contacto?: string
  observaciones?: string
  activo: boolean
  fecha_creacion?: string
  fecha_actualizacion?: string
  sucursales?: SucursalProveedor[]
}

export interface SucursalProveedor {
  id_sucursal: number
  id_proveedor: number
  codigo_sucursal: string
  nombre_sucursal: string
  direccion?: string
  ciudad?: string
  estado?: string
  codigo_postal?: string
  pais?: string
  telefono?: string
  email?: string
  contacto?: string
  telefono_contacto?: string
  email_contacto?: string
  es_sucursal_principal: boolean
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string
}

export interface SucursalProveedorCreate {
  id_proveedor: number
  codigo_sucursal: string
  nombre_sucursal: string
  direccion?: string
  ciudad?: string
  estado?: string
  codigo_postal?: string
  pais?: string
  telefono?: string
  email?: string
  contacto?: string
  telefono_contacto?: string
  email_contacto?: string
  es_sucursal_principal: boolean
  activo: boolean
}

export interface SucursalProveedorUpdate {
  codigo_sucursal?: string
  nombre_sucursal?: string
  direccion?: string
  ciudad?: string
  estado?: string
  codigo_postal?: string
  pais?: string
  telefono?: string
  email?: string
  contacto?: string
  telefono_contacto?: string
  email_contacto?: string
  es_sucursal_principal?: boolean
  activo?: boolean
}

export interface ProveedorCreate {
  codigo_proveedor: string
  nombre_proveedor: string
  razon_social?: string
  rfc?: string
  direccion?: string
  telefono?: string
  email?: string
  contacto?: string
  telefono_contacto?: string
  email_contacto?: string
  observaciones?: string
  activo: boolean
}

export interface ProveedorUpdate {
  codigo_proveedor?: string
  nombre_proveedor?: string
  razon_social?: string
  rfc?: string
  direccion?: string
  telefono?: string
  email?: string
  contacto?: string
  telefono_contacto?: string
  email_contacto?: string
  observaciones?: string
  activo?: boolean
}

export const useProveedorStore = defineStore('proveedores', () => {
  const apiStore = useApiStore()

  const proveedores = ref<Proveedor[]>([])
  const sucursales = ref<SucursalProveedor[]>([])
  const isLoading = ref(false)

  // CRUD Proveedores
  const obtenerProveedores = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<Proveedor[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/proveedores?${queryParams.toString()}`
      console.log('URL construida proveedores:', url, 'params recibidos:', params)
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener proveedores')
      }
      proveedores.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener proveedores:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const buscarProveedores = async (
    searchTerm: string,
    params?: {
      skip?: number
      limit?: number
    }
  ): Promise<Proveedor[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()
      queryParams.append('q', searchTerm)

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())

      const response = await apiStore.get(`/proveedores/search?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al buscar proveedores')
      }
      return response.data
    } catch (error) {
      console.error('Error al buscar proveedores:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerProveedor = async (id: number): Promise<Proveedor> => {
    try {
      const response = await apiStore.get(`/proveedores/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener proveedor')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener proveedor:', error)
      throw error
    }
  }

  const obtenerProveedorPorCodigo = async (codigo: string): Promise<Proveedor> => {
    try {
      const response = await apiStore.get(`/proveedores/codigo/${codigo}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener proveedor por código')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener proveedor por código:', error)
      throw error
    }
  }

  const obtenerProveedorPorRfc = async (rfc: string): Promise<Proveedor> => {
    try {
      const response = await apiStore.get(`/proveedores/rfc/${rfc}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener proveedor por RFC')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener proveedor por RFC:', error)
      throw error
    }
  }

  const crearProveedor = async (proveedor: ProveedorCreate): Promise<Proveedor> => {
    try {
      const response = await apiStore.post('/proveedores', proveedor)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear proveedor')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear proveedor:', error)
      throw error
    }
  }

  const actualizarProveedor = async (id: number, proveedor: ProveedorUpdate): Promise<Proveedor> => {
    try {
      const response = await apiStore.put(`/proveedores/${id}`, proveedor)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar proveedor')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar proveedor:', error)
      throw error
    }
  }

  const eliminarProveedor = async (id: number, permanente: boolean = false): Promise<void> => {
    try {
      const params = new URLSearchParams()
      params.append('permanente', permanente.toString())

      const response = await apiStore.delete(`/proveedores/${id}?${params.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar proveedor')
      }
    } catch (error) {
      console.error('Error al eliminar proveedor:', error)
      throw error
    }
  }

  const activarProveedor = async (id: number): Promise<Proveedor> => {
    try {
      const response = await apiStore.patch(`/proveedores/${id}/activar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al activar proveedor')
      }
      return response.data.proveedor
    } catch (error) {
      console.error('Error al activar proveedor:', error)
      throw error
    }
  }

  // CRUD Sucursales
  const obtenerSucursalesPorProveedor = async (proveedorId: number, params?: {
    skip?: number
    limit?: number
    activo?: boolean
  }): Promise<SucursalProveedor[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/sucursales-proveedor/proveedor/${proveedorId}?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener sucursales')
      }
      sucursales.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener sucursales:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerSucursal = async (id: number): Promise<SucursalProveedor> => {
    try {
      const response = await apiStore.get(`/sucursales-proveedor/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener sucursal')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener sucursal:', error)
      throw error
    }
  }

  const crearSucursal = async (sucursal: SucursalProveedorCreate): Promise<SucursalProveedor> => {
    try {
      const response = await apiStore.post('/sucursales-proveedor', sucursal)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear sucursal')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear sucursal:', error)
      throw error
    }
  }

  const actualizarSucursal = async (id: number, sucursal: SucursalProveedorUpdate): Promise<SucursalProveedor> => {
    try {
      const response = await apiStore.put(`/sucursales-proveedor/${id}`, sucursal)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar sucursal')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar sucursal:', error)
      throw error
    }
  }

  const eliminarSucursal = async (id: number, permanente: boolean = false): Promise<void> => {
    try {
      const params = new URLSearchParams()
      params.append('permanente', permanente.toString())

      const response = await apiStore.delete(`/sucursales-proveedor/${id}?${params.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar sucursal')
      }
    } catch (error) {
      console.error('Error al eliminar sucursal:', error)
      throw error
    }
  }

  const activarSucursal = async (id: number): Promise<SucursalProveedor> => {
    try {
      const response = await apiStore.patch(`/sucursales-proveedor/${id}/activar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al activar sucursal')
      }
      return response.data.sucursal
    } catch (error) {
      console.error('Error al activar sucursal:', error)
      throw error
    }
  }

  const establecerSucursalPrincipal = async (id: number): Promise<SucursalProveedor> => {
    try {
      const response = await apiStore.patch(`/sucursales-proveedor/${id}/principal`)
      if (!response.success) {
        throw new Error(response.error || 'Error al establecer sucursal principal')
      }
      return response.data.sucursal
    } catch (error) {
      console.error('Error al establecer sucursal principal:', error)
      throw error
    }
  }

  return {
    // State
    proveedores,
    sucursales,
    isLoading,

    // Methods - Proveedores
    obtenerProveedores,
    buscarProveedores,
    obtenerProveedor,
    obtenerProveedorPorCodigo,
    obtenerProveedorPorRfc,
    crearProveedor,
    actualizarProveedor,
    eliminarProveedor,
    activarProveedor,

    // Methods - Sucursales
    obtenerSucursalesPorProveedor,
    obtenerSucursal,
    crearSucursal,
    actualizarSucursal,
    eliminarSucursal,
    activarSucursal,
    establecerSucursalPrincipal
  }
})