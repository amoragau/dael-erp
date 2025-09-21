import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

// clientes - Información de Clientes
export interface Cliente {
  id_cliente: number
  codigo_cliente: string
  nombre_cliente: string
  razon_social?: string
  tipo_cliente: 'gobierno' | 'privado' | 'constructora' | 'distribuidor'

  // Datos fiscales
  rut?: string
  giro_comercial?: string
  direccion_fiscal?: string
  ciudad_fiscal?: string
  estado_fiscal?: string
  codigo_postal_fiscal?: string
  pais_fiscal?: string

  // Información de contacto principal
  direccion_comercial?: string
  ciudad_comercial?: string
  estado_comercial?: string
  codigo_postal_comercial?: string
  pais_comercial?: string
  telefono_principal?: string
  email_principal?: string
  sitio_web?: string

  // Contacto principal
  contacto_principal?: string
  telefono_contacto?: string
  email_contacto?: string
  puesto_contacto?: string

  // Información comercial
  condiciones_pago?: string
  dias_credito?: number
  limite_credito?: number
  descuento_comercial?: number
  moneda_preferida?: string

  // Control
  observaciones?: string
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string
  usuario_creacion?: number
  usuario_modificacion?: number

  // Estadísticas
  total_obras?: number
  obras_activas?: number
  valor_contratos?: number
}

export interface ClienteCreate {
  codigo_cliente: string
  nombre_cliente: string
  razon_social?: string
  tipo_cliente: 'gobierno' | 'privado' | 'constructora' | 'distribuidor'

  // Datos fiscales
  rut?: string
  giro_comercial?: string
  direccion_fiscal?: string
  ciudad_fiscal?: string
  estado_fiscal?: string
  codigo_postal_fiscal?: string
  pais_fiscal?: string

  // Información de contacto
  direccion_comercial?: string
  ciudad_comercial?: string
  estado_comercial?: string
  codigo_postal_comercial?: string
  pais_comercial?: string
  telefono_principal?: string
  email_principal?: string
  sitio_web?: string

  // Contacto principal
  contacto_principal?: string
  telefono_contacto?: string
  email_contacto?: string
  puesto_contacto?: string

  // Información comercial
  condiciones_pago?: string
  dias_credito?: number
  limite_credito?: number
  descuento_comercial?: number
  moneda_preferida?: string

  observaciones?: string
  activo: boolean
}

export interface ClienteUpdate {
  codigo_cliente?: string
  nombre_cliente?: string
  razon_social?: string
  tipo_cliente?: 'gobierno' | 'privado' | 'constructora' | 'distribuidor'

  // Datos fiscales
  rut?: string
  giro_comercial?: string
  direccion_fiscal?: string
  ciudad_fiscal?: string
  estado_fiscal?: string
  codigo_postal_fiscal?: string
  pais_fiscal?: string

  // Información de contacto
  direccion_comercial?: string
  ciudad_comercial?: string
  estado_comercial?: string
  codigo_postal_comercial?: string
  pais_comercial?: string
  telefono_principal?: string
  email_principal?: string
  sitio_web?: string

  // Contacto principal
  contacto_principal?: string
  telefono_contacto?: string
  email_contacto?: string
  puesto_contacto?: string

  // Información comercial
  condiciones_pago?: string
  dias_credito?: number
  limite_credito?: number
  descuento_comercial?: number
  moneda_preferida?: string

  observaciones?: string
  activo?: boolean
}

export const useClienteStore = defineStore('clientes', () => {
  const apiStore = useApiStore()

  const clientes = ref<Cliente[]>([])
  const isLoading = ref(false)

  // CRUD Clientes
  const obtenerClientes = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
    tipo?: string
  }): Promise<Cliente[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')
      if (params?.tipo) queryParams.append('tipo', params.tipo)

      const url = `/clientes?${queryParams.toString()}`
      console.log('URL construida clientes:', url, 'params recibidos:', params)
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener clientes')
      }
      clientes.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener clientes:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const buscarClientes = async (
    searchTerm: string,
    params?: {
      skip?: number
      limit?: number
      activo?: boolean
      tipo?: string
    }
  ): Promise<Cliente[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()
      queryParams.append('q', searchTerm)

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')
      if (params?.tipo) queryParams.append('tipo', params.tipo)

      const response = await apiStore.get(`/clientes/search?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al buscar clientes')
      }
      return response.data
    } catch (error) {
      console.error('Error al buscar clientes:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerCliente = async (id: number): Promise<Cliente> => {
    try {
      const response = await apiStore.get(`/clientes/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener cliente')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener cliente:', error)
      throw error
    }
  }

  const obtenerClientePorCodigo = async (codigo: string): Promise<Cliente> => {
    try {
      const response = await apiStore.get(`/clientes/codigo/${codigo}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener cliente por código')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener cliente por código:', error)
      throw error
    }
  }

  const crearCliente = async (cliente: ClienteCreate): Promise<Cliente> => {
    try {
      const response = await apiStore.post('/clientes', cliente)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear cliente')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear cliente:', error)
      throw error
    }
  }

  const actualizarCliente = async (id: number, cliente: ClienteUpdate): Promise<Cliente> => {
    try {
      const response = await apiStore.put(`/clientes/${id}`, cliente)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar cliente')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar cliente:', error)
      throw error
    }
  }

  const eliminarCliente = async (id: number, permanente: boolean = false): Promise<void> => {
    try {
      const params = new URLSearchParams()
      params.append('permanente', permanente.toString())

      const response = await apiStore.delete(`/clientes/${id}?${params.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar cliente')
      }
    } catch (error) {
      console.error('Error al eliminar cliente:', error)
      throw error
    }
  }

  const activarCliente = async (id: number): Promise<Cliente> => {
    try {
      const response = await apiStore.patch(`/clientes/${id}/activar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al activar cliente')
      }
      return response.data.cliente
    } catch (error) {
      console.error('Error al activar cliente:', error)
      throw error
    }
  }

  const obtenerEstadisticasCliente = async (id: number): Promise<{
    total_obras: number
    obras_activas: number
    obras_finalizadas: number
    valor_total_contratos: number
    obra_mas_reciente: any
  }> => {
    try {
      const response = await apiStore.get(`/clientes/${id}/estadisticas`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener estadísticas del cliente')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas del cliente:', error)
      throw error
    }
  }

  const validarCreditoCliente = async (id: number): Promise<{
    credito_disponible: number
    credito_utilizado: number
    estado_credito: 'disponible' | 'limite_alcanzado' | 'sobregiro'
    facturas_pendientes: number
  }> => {
    try {
      const response = await apiStore.get(`/clientes/${id}/credito/validar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al validar crédito del cliente')
      }
      return response.data
    } catch (error) {
      console.error('Error al validar crédito del cliente:', error)
      throw error
    }
  }

  const obtenerEstadisticasGenerales = async (): Promise<{
    total_clientes: number
    activos: number
    inactivos: number
    por_tipo: { [key: string]: number }
    clientes_con_obras_activas: number
    valor_total_contratos: number
  }> => {
    try {
      const response = await apiStore.get('/clientes/stats/generales')
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener estadísticas generales')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas generales:', error)
      throw error
    }
  }

  return {
    // State
    clientes,
    isLoading,

    // Methods
    obtenerClientes,
    buscarClientes,
    obtenerCliente,
    obtenerClientePorCodigo,
    crearCliente,
    actualizarCliente,
    eliminarCliente,
    activarCliente,
    obtenerEstadisticasCliente,
    validarCreditoCliente,
    obtenerEstadisticasGenerales
  }
})