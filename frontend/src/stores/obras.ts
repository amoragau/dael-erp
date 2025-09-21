import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

// obras - Proyectos Específicos
export interface Obra {
  id_obra: number
  codigo_obra: string
  nombre_obra: string
  descripcion?: string
  id_cliente: number

  // Ubicación física
  direccion?: string
  ciudad?: string
  estado?: string
  codigo_postal?: string
  pais?: string
  coordenadas_gps?: string

  // Personal
  supervisor_obra?: string
  telefono_supervisor?: string
  email_supervisor?: string
  contacto_obra?: string
  telefono_contacto?: string
  email_contacto?: string

  // Control de fechas
  fecha_inicio_programada?: string
  fecha_fin_programada?: string
  fecha_inicio_real?: string
  fecha_fin_real?: string
  estado: 'planificacion' | 'ejecucion' | 'suspendida' | 'finalizada' | 'cancelada'

  // Control financiero
  valor_contrato?: number
  moneda?: string
  porcentaje_merma_permitida?: number

  // Políticas de inventario
  requiere_devolucion_sobrantes: boolean
  dias_limite_devolucion: number

  // Control
  observaciones?: string
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string
  usuario_creacion?: number
  usuario_modificacion?: number

  // Relaciones
  cliente?: any
  almacen_obra?: AlmacenObra
}

export interface ObraCreate {
  codigo_obra: string
  nombre_obra: string
  descripcion?: string
  id_cliente: number

  // Ubicación física
  direccion?: string
  ciudad?: string
  estado?: string
  codigo_postal?: string
  pais?: string
  coordenadas_gps?: string

  // Personal
  supervisor_obra?: string
  telefono_supervisor?: string
  email_supervisor?: string
  contacto_obra?: string
  telefono_contacto?: string
  email_contacto?: string

  // Control de fechas
  fecha_inicio_programada?: string
  fecha_fin_programada?: string
  fecha_inicio_real?: string
  fecha_fin_real?: string
  estado: 'planificacion' | 'ejecucion' | 'suspendida' | 'finalizada' | 'cancelada'

  // Control financiero
  valor_contrato?: number
  moneda?: string
  porcentaje_merma_permitida?: number

  // Políticas de inventario
  requiere_devolucion_sobrantes: boolean
  dias_limite_devolucion: number

  observaciones?: string
  activo: boolean
}

export interface ObraUpdate {
  codigo_obra?: string
  nombre_obra?: string
  descripcion?: string
  id_cliente?: number

  // Ubicación física
  direccion?: string
  ciudad?: string
  estado?: string
  codigo_postal?: string
  pais?: string
  coordenadas_gps?: string

  // Personal
  supervisor_obra?: string
  telefono_supervisor?: string
  email_supervisor?: string
  contacto_obra?: string
  telefono_contacto?: string
  email_contacto?: string

  // Control de fechas
  fecha_inicio_programada?: string
  fecha_fin_programada?: string
  fecha_inicio_real?: string
  fecha_fin_real?: string
  estado?: 'planificacion' | 'ejecucion' | 'suspendida' | 'finalizada' | 'cancelada'

  // Control financiero
  valor_contrato?: number
  moneda?: string
  porcentaje_merma_permitida?: number

  // Políticas de inventario
  requiere_devolucion_sobrantes?: boolean
  dias_limite_devolucion?: number

  observaciones?: string
  activo?: boolean
}

// almacen_obra - Almacén Único por Obra (Relación 1:1)
export interface AlmacenObra {
  id_almacen_obra: number
  id_obra: number
  ubicacion_almacen: string
  direccion_almacen?: string
  responsable_almacen?: string
  telefono_responsable?: string
  email_responsable?: string

  // Condiciones del almacén
  tiene_techo: boolean
  tiene_seguridad: boolean
  capacidad_m3?: number
  condiciones_especiales?: string

  observaciones?: string
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string

  // Relación
  obra?: Obra
}

export interface AlmacenObraCreate {
  id_obra: number
  ubicacion_almacen: string
  direccion_almacen?: string
  responsable_almacen?: string
  telefono_responsable?: string
  email_responsable?: string

  // Condiciones del almacén
  tiene_techo: boolean
  tiene_seguridad: boolean
  capacidad_m3?: number
  condiciones_especiales?: string

  observaciones?: string
  activo: boolean
}

export interface AlmacenObraUpdate {
  ubicacion_almacen?: string
  direccion_almacen?: string
  responsable_almacen?: string
  telefono_responsable?: string
  email_responsable?: string

  // Condiciones del almacén
  tiene_techo?: boolean
  tiene_seguridad?: boolean
  capacidad_m3?: number
  condiciones_especiales?: string

  observaciones?: string
  activo?: boolean
}

export const useObraStore = defineStore('obras', () => {
  const apiStore = useApiStore()

  const obras = ref<Obra[]>([])
  const almacenesObra = ref<AlmacenObra[]>([])
  const isLoading = ref(false)

  // CRUD Obras
  const obtenerObras = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
    estado?: string
    cliente_id?: number
  }): Promise<Obra[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')
      if (params?.estado) queryParams.append('estado', params.estado)
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
      activo?: boolean
      estado?: string
    }
  ): Promise<Obra[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()
      queryParams.append('q', searchTerm)

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')
      if (params?.estado) queryParams.append('estado', params.estado)

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

  const cambiarEstadoObra = async (id: number, nuevoEstado: string, observaciones?: string): Promise<Obra> => {
    try {
      const response = await apiStore.patch(`/obras/${id}/estado`, {
        estado: nuevoEstado,
        observaciones
      })
      if (!response.success) {
        throw new Error(response.error || 'Error al cambiar estado de obra')
      }
      return response.data
    } catch (error) {
      console.error('Error al cambiar estado de obra:', error)
      throw error
    }
  }

  const iniciarObra = async (id: number): Promise<Obra> => {
    try {
      const response = await apiStore.patch(`/obras/${id}/iniciar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al iniciar obra')
      }
      return response.data
    } catch (error) {
      console.error('Error al iniciar obra:', error)
      throw error
    }
  }

  const finalizarObra = async (id: number, observaciones?: string): Promise<Obra> => {
    try {
      const response = await apiStore.patch(`/obras/${id}/finalizar`, { observaciones })
      if (!response.success) {
        throw new Error(response.error || 'Error al finalizar obra')
      }
      return response.data
    } catch (error) {
      console.error('Error al finalizar obra:', error)
      throw error
    }
  }

  const suspenderObra = async (id: number, motivo: string): Promise<Obra> => {
    try {
      const response = await apiStore.patch(`/obras/${id}/suspender`, { motivo })
      if (!response.success) {
        throw new Error(response.error || 'Error al suspender obra')
      }
      return response.data
    } catch (error) {
      console.error('Error al suspender obra:', error)
      throw error
    }
  }

  const reanudarObra = async (id: number): Promise<Obra> => {
    try {
      const response = await apiStore.patch(`/obras/${id}/reanudar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al reanudar obra')
      }
      return response.data
    } catch (error) {
      console.error('Error al reanudar obra:', error)
      throw error
    }
  }

  // CRUD Almacenes Obra
  const obtenerAlmacenObra = async (obraId: number): Promise<AlmacenObra | null> => {
    try {
      const response = await apiStore.get(`/almacenes-obra/obra/${obraId}`)
      if (!response.success) {
        if (response.error?.includes('not found')) {
          return null // No hay almacén para esta obra
        }
        throw new Error(response.error || 'Error al obtener almacén de obra')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener almacén de obra:', error)
      throw error
    }
  }

  const crearAlmacenObra = async (almacen: AlmacenObraCreate): Promise<AlmacenObra> => {
    try {
      const response = await apiStore.post('/almacenes-obra', almacen)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear almacén de obra')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear almacén de obra:', error)
      throw error
    }
  }

  const actualizarAlmacenObra = async (id: number, almacen: AlmacenObraUpdate): Promise<AlmacenObra> => {
    try {
      const response = await apiStore.put(`/almacenes-obra/${id}`, almacen)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar almacén de obra')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar almacén de obra:', error)
      throw error
    }
  }

  const eliminarAlmacenObra = async (id: number): Promise<void> => {
    try {
      const response = await apiStore.delete(`/almacenes-obra/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar almacén de obra')
      }
    } catch (error) {
      console.error('Error al eliminar almacén de obra:', error)
      throw error
    }
  }

  // Métodos de análisis y reportes
  const obtenerEstadisticasObra = async (id: number): Promise<{
    dias_transcurridos: number
    dias_restantes: number
    porcentaje_avance_tiempo: number
    valor_despachos: number
    valor_devoluciones: number
    productos_despachados: number
    productos_devueltos: number
    porcentaje_merma_actual: number
  }> => {
    try {
      const response = await apiStore.get(`/obras/${id}/estadisticas`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener estadísticas de obra')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas de obra:', error)
      throw error
    }
  }

  const validarPoliticasInventario = async (obraId: number): Promise<{
    requiere_devolucion: boolean
    dias_limite: number
    dias_transcurridos: number
    vencimiento_devolucion: string
    productos_pendientes_devolucion: number
  }> => {
    try {
      const response = await apiStore.get(`/obras/${obraId}/inventario/validar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al validar políticas de inventario')
      }
      return response.data
    } catch (error) {
      console.error('Error al validar políticas de inventario:', error)
      throw error
    }
  }

  const obtenerEstadisticasGenerales = async (): Promise<{
    total_obras: number
    por_estado: { [key: string]: number }
    valor_total_contratos: number
    obras_vencidas: number
    obras_por_vencer: number
    almacenes_configurados: number
  }> => {
    try {
      const response = await apiStore.get('/obras/stats/generales')
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
    obras,
    almacenesObra,
    isLoading,

    // Methods - Obras
    obtenerObras,
    buscarObras,
    obtenerObra,
    crearObra,
    actualizarObra,
    cambiarEstadoObra,
    iniciarObra,
    finalizarObra,
    suspenderObra,
    reanudarObra,

    // Methods - Almacenes Obra
    obtenerAlmacenObra,
    crearAlmacenObra,
    actualizarAlmacenObra,
    eliminarAlmacenObra,

    // Methods - Análisis
    obtenerEstadisticasObra,
    validarPoliticasInventario,
    obtenerEstadisticasGenerales
  }
})