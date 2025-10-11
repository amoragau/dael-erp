import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface LogAprobacion {
  id_log: number
  id_orden_compra: number
  numero_orden: string
  accion: 'APROBADA' | 'RECHAZADA' | 'ENVIADA' | 'CERRADA' | 'CANCELADA'
  usuario_id: number
  usuario_nombre: string
  motivo?: string
  fecha_accion: string
  ip_address?: string
  user_agent?: string
}

export interface LogAprobacionCreate {
  id_orden_compra: number
  accion: 'APROBADA' | 'RECHAZADA' | 'ENVIADA' | 'CERRADA' | 'CANCELADA'
  usuario_id: number
  motivo?: string
}

export const useLogStore = defineStore('logs', () => {
  const apiStore = useApiStore()

  const logs = ref<LogAprobacion[]>([])
  const isLoading = ref(false)

  // CRUD Logs
  const obtenerLogs = async (params?: {
    skip?: number
    limit?: number
    id_orden_compra?: number
    accion?: string
    fecha_desde?: string
    fecha_hasta?: string
  }): Promise<LogAprobacion[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.id_orden_compra) queryParams.append('id_orden_compra', params.id_orden_compra.toString())
      if (params?.accion) queryParams.append('accion', params.accion)
      if (params?.fecha_desde) queryParams.append('fecha_desde', params.fecha_desde)
      if (params?.fecha_hasta) queryParams.append('fecha_hasta', params.fecha_hasta)

      const url = `/logs/aprobaciones?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener logs')
      }
      logs.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener logs:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerLogsPorOrden = async (idOrdenCompra: number): Promise<LogAprobacion[]> => {
    try {
      const response = await apiStore.get(`/logs/aprobaciones/orden/${idOrdenCompra}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener logs de la orden')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener logs de la orden:', error)
      throw error
    }
  }

  const crearLog = async (log: LogAprobacionCreate): Promise<LogAprobacion> => {
    try {
      const response = await apiStore.post('/logs/aprobaciones', log)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear log')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear log:', error)
      throw error
    }
  }

  // Métodos de conveniencia para diferentes acciones
  const logAprobacion = async (idOrdenCompra: number, usuarioId: number, motivo?: string): Promise<LogAprobacion> => {
    return await crearLog({
      id_orden_compra: idOrdenCompra,
      accion: 'APROBADA',
      usuario_id: usuarioId,
      motivo
    })
  }

  const logRechazo = async (idOrdenCompra: number, usuarioId: number, motivo: string): Promise<LogAprobacion> => {
    return await crearLog({
      id_orden_compra: idOrdenCompra,
      accion: 'RECHAZADA',
      usuario_id: usuarioId,
      motivo
    })
  }

  const logEnvio = async (idOrdenCompra: number, usuarioId: number, motivo?: string): Promise<LogAprobacion> => {
    return await crearLog({
      id_orden_compra: idOrdenCompra,
      accion: 'ENVIADA',
      usuario_id: usuarioId,
      motivo
    })
  }

  const logCierre = async (idOrdenCompra: number, usuarioId: number, motivo?: string): Promise<LogAprobacion> => {
    return await crearLog({
      id_orden_compra: idOrdenCompra,
      accion: 'CERRADA',
      usuario_id: usuarioId,
      motivo
    })
  }

  const logCancelacion = async (idOrdenCompra: number, usuarioId: number, motivo: string): Promise<LogAprobacion> => {
    return await crearLog({
      id_orden_compra: idOrdenCompra,
      accion: 'CANCELADA',
      usuario_id: usuarioId,
      motivo
    })
  }

  // Obtener estadísticas de aprobaciones
  const obtenerEstadisticasAprobaciones = async (params?: {
    fecha_desde?: string
    fecha_hasta?: string
    usuario_id?: number
  }): Promise<{
    total_aprobaciones: number
    total_rechazos: number
    aprobaciones_por_usuario: Array<{
      usuario_id: number
      usuario_nombre: string
      total_aprobaciones: number
      total_rechazos: number
    }>
    tiempo_promedio_aprobacion: number
  }> => {
    try {
      const queryParams = new URLSearchParams()
      if (params?.fecha_desde) queryParams.append('fecha_desde', params.fecha_desde)
      if (params?.fecha_hasta) queryParams.append('fecha_hasta', params.fecha_hasta)
      if (params?.usuario_id) queryParams.append('usuario_id', params.usuario_id.toString())

      const response = await apiStore.get(`/logs/aprobaciones/estadisticas?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener estadísticas')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas:', error)
      throw error
    }
  }

  return {
    // State
    logs,
    isLoading,

    // Methods - CRUD
    obtenerLogs,
    obtenerLogsPorOrden,
    crearLog,

    // Methods - Conveniencia
    logAprobacion,
    logRechazo,
    logEnvio,
    logCierre,
    logCancelacion,

    // Methods - Estadísticas
    obtenerEstadisticasAprobaciones
  }
})