import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface Obra {
  id_obra: number
  codigo_obra: string
  nombre_obra: string
  descripcion?: string
  id_cliente: number
  direccion_obra?: string
  ciudad?: string
  codigo_postal?: string

  // Responsables
  supervisor_obra?: string
  contacto_obra?: string
  telefono_obra?: string

  // Fechas del proyecto
  fecha_inicio_programada?: string
  fecha_fin_programada?: string
  fecha_inicio_real?: string
  fecha_fin_real?: string

  // Control financiero
  valor_contrato?: number
  moneda: string

  // Control de inventario
  requiere_devolucion_sobrantes: boolean
  dias_limite_devolucion: number

  // Estado
  estado: string
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string
  usuario_creacion?: number
  usuario_modificacion?: number

  // Relaciones
  cliente?: any
  almacen_obra?: any
}

export interface ObraCreate {
  codigo_obra: string
  nombre_obra: string
  descripcion?: string
  id_cliente: number
  direccion_obra?: string
  ciudad?: string
  codigo_postal?: string

  // Responsables
  supervisor_obra?: string
  contacto_obra?: string
  telefono_obra?: string

  // Fechas del proyecto
  fecha_inicio_programada?: string
  fecha_fin_programada?: string
  fecha_inicio_real?: string
  fecha_fin_real?: string

  // Control financiero
  valor_contrato?: number
  moneda: string

  // Control de inventario
  requiere_devolucion_sobrantes: boolean
  dias_limite_devolucion: number

  // Estado
  estado: string
  activo: boolean
}

export interface ObraUpdate {
  codigo_obra?: string
  nombre_obra?: string
  descripcion?: string
  id_cliente?: number
  direccion_obra?: string
  ciudad?: string
  codigo_postal?: string

  // Responsables
  supervisor_obra?: string
  contacto_obra?: string
  telefono_obra?: string

  // Fechas del proyecto
  fecha_inicio_programada?: string
  fecha_fin_programada?: string
  fecha_inicio_real?: string
  fecha_fin_real?: string

  // Control financiero
  valor_contrato?: number
  moneda?: string

  // Control de inventario
  requiere_devolucion_sobrantes?: boolean
  dias_limite_devolucion?: number

  // Estado
  estado?: string
  activo?: boolean
}

export interface Cliente {
  id_cliente: number
  codigo_cliente: string
  nombre_cliente: string
  activo: boolean
}

export interface AlmacenObra {
  id_almacen: number
  id_obra: number
  nombre_almacen: string
  descripcion?: string
  direccion?: string
  responsable?: string
  telefono?: string
  tiene_seguridad: boolean
  tiene_techo: boolean
  capacidad_m3?: number
  observaciones?: string
  activo: boolean
}

export interface AlmacenObraCreate {
  id_obra: number
  nombre_almacen: string
  descripcion?: string
  direccion?: string
  responsable?: string
  telefono?: string
  tiene_seguridad: boolean
  tiene_techo: boolean
  capacidad_m3?: number
  observaciones?: string
  activo: boolean
}

// Estados disponibles para obras
export const ESTADOS_OBRA = [
  'PLANIFICACION',
  'EN_EJECUCION',
  'SUSPENDIDA',
  'FINALIZADA',
  'CANCELADA'
] as const

export type EstadoObra = typeof ESTADOS_OBRA[number]

export const useObraStore = defineStore('obras', () => {
  const apiStore = useApiStore()

  const obras = ref<Obra[]>([])
  const clientes = ref<Cliente[]>([])
  const almacenesObra = ref<AlmacenObra[]>([])
  const isLoading = ref(false)

  // CRUD Obras
  const obtenerObras = async (params?: {
    skip?: number
    limit?: number
    estado?: EstadoObra
    activo?: boolean
    cliente_id?: number
  }): Promise<Obra[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.estado !== undefined) queryParams.append('estado', params.estado)
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')
      if (params?.cliente_id !== undefined) queryParams.append('cliente_id', params.cliente_id.toString())

      const url = `/obras?${queryParams.toString()}`
      console.log('URL construida obras:', url, 'params recibidos:', params)
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener obras')
      }
      obras.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener obras:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const buscarObras = async (
    searchTerm: string,
    params?: {
      skip?: number
      limit?: number
      estado?: EstadoObra
    }
  ): Promise<Obra[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()
      queryParams.append('q', searchTerm)

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.estado !== undefined) queryParams.append('estado', params.estado)

      const response = await apiStore.get(`/obras/search?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al buscar obras')
      }
      return response.data
    } catch (error) {
      console.error('Error al buscar obras:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerObra = async (id: number): Promise<Obra> => {
    try {
      const response = await apiStore.get(`/obras/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener obra')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener obra:', error)
      throw error
    }
  }

  const obtenerObraPorCodigo = async (codigo: string): Promise<Obra> => {
    try {
      const response = await apiStore.get(`/obras/codigo/${codigo}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener obra por código')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener obra por código:', error)
      throw error
    }
  }

  const crearObra = async (obra: ObraCreate): Promise<Obra> => {
    try {
      const response = await apiStore.post('/obras', obra)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear obra')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear obra:', error)
      throw error
    }
  }

  const actualizarObra = async (id: number, obra: ObraUpdate): Promise<Obra> => {
    try {
      const response = await apiStore.put(`/obras/${id}`, obra)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar obra')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar obra:', error)
      throw error
    }
  }

  const eliminarObra = async (id: number, permanente: boolean = false): Promise<void> => {
    try {
      const params = new URLSearchParams()
      params.append('permanente', permanente.toString())

      const response = await apiStore.delete(`/obras/${id}?${params.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar obra')
      }
    } catch (error) {
      console.error('Error al eliminar obra:', error)
      throw error
    }
  }

  const activarObra = async (id: number): Promise<Obra> => {
    try {
      const response = await apiStore.patch(`/obras/${id}/activar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al activar obra')
      }
      return response.data.obra
    } catch (error) {
      console.error('Error al activar obra:', error)
      throw error
    }
  }

  const cambiarEstadoObra = async (id: number, estado: EstadoObra): Promise<Obra> => {
    try {
      const response = await apiStore.patch(`/obras/${id}/estado`, { estado })
      if (!response.success) {
        throw new Error(response.error || 'Error al cambiar estado de obra')
      }
      return response.data.obra
    } catch (error) {
      console.error('Error al cambiar estado de obra:', error)
      throw error
    }
  }

  // CRUD Almacenes de Obra
  const obtenerAlmacenesPorObra = async (obraId: number): Promise<AlmacenObra[]> => {
    try {
      isLoading.value = true
      const response = await apiStore.get(`/almacen-obra/obra/${obraId}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener almacenes')
      }
      almacenesObra.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener almacenes:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const crearAlmacenObra = async (almacen: AlmacenObraCreate): Promise<AlmacenObra> => {
    try {
      const response = await apiStore.post('/almacen-obra', almacen)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear almacén')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear almacén:', error)
      throw error
    }
  }

  const actualizarAlmacenObra = async (id: number, almacen: Partial<AlmacenObraCreate>): Promise<AlmacenObra> => {
    try {
      const response = await apiStore.put(`/almacen-obra/${id}`, almacen)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar almacén')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar almacén:', error)
      throw error
    }
  }

  const eliminarAlmacenObra = async (id: number): Promise<void> => {
    try {
      const response = await apiStore.delete(`/almacen-obra/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar almacén')
      }
    } catch (error) {
      console.error('Error al eliminar almacén:', error)
      throw error
    }
  }

  // Métodos para datos relacionados
  const obtenerClientes = async (): Promise<Cliente[]> => {
    try {
      const response = await apiStore.get('/clientes?activo=true')
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener clientes')
      }
      clientes.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener clientes:', error)
      throw error
    }
  }

  return {
    // State
    obras,
    clientes,
    almacenesObra,
    isLoading,

    // Methods - Obras
    obtenerObras,
    buscarObras,
    obtenerObra,
    obtenerObraPorCodigo,
    crearObra,
    actualizarObra,
    eliminarObra,
    activarObra,
    cambiarEstadoObra,

    // Methods - Almacenes de Obra
    obtenerAlmacenesPorObra,
    crearAlmacenObra,
    actualizarAlmacenObra,
    eliminarAlmacenObra,

    // Methods - Datos relacionados
    obtenerClientes
  }
})