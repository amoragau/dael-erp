import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

// tipos_movimiento - Clasificación de Operaciones
export interface TipoMovimiento {
  id_tipo_movimiento: number
  codigo_tipo: string
  nombre_tipo: string
  descripcion: string
  afecta_stock: boolean
  requiere_autorizacion: boolean
  permite_costo_cero: boolean
  es_entrada: boolean
  es_salida: boolean
  icono?: string
  color?: string
  activo: boolean
  fecha_creacion?: string
}

// documentos_movimiento - Respaldo Legal
export interface DocumentoMovimiento {
  id_documento: number
  tipo_documento: 'factura' | 'remision' | 'orden_compra' | 'guia_despacho' | 'nota_credito' | 'nota_debito' | 'otro'
  numero_documento: string
  fecha_documento: string
  proveedor_cliente?: string
  rut_proveedor_cliente?: string
  monto_total?: number
  moneda?: string
  archivo_digital?: string
  url_archivo?: string
  observaciones?: string
  activo: boolean
  fecha_creacion?: string
}

export interface DocumentoMovimientoCreate {
  tipo_documento: 'factura' | 'remision' | 'orden_compra' | 'guia_despacho' | 'nota_credito' | 'nota_debito' | 'otro'
  numero_documento: string
  fecha_documento: string
  proveedor_cliente?: string
  rut_proveedor_cliente?: string
  monto_total?: number
  moneda?: string
  archivo_digital?: string
  observaciones?: string
  activo: boolean
}

// movimientos_inventario - Cabecera del Movimiento
export interface MovimientoInventario {
  id_movimiento: number
  numero_movimiento: string
  id_tipo_movimiento: number
  fecha_movimiento: string
  fecha_procesamiento?: string
  estado: 'pendiente' | 'autorizado' | 'procesado' | 'cancelado'
  motivo: string
  observaciones?: string

  // Usuario y autorización
  id_usuario_crea: number
  id_usuario_autoriza?: number
  id_usuario_procesa?: number
  requiere_autorizacion: boolean
  fecha_autorizacion?: string

  // Documento soporte
  id_documento?: number

  // Ubicaciones (para transferencias)
  id_bodega_origen?: number
  id_bodega_destino?: number

  // Totales
  cantidad_productos: number
  valor_total: number

  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string

  // Relaciones
  tipo_movimiento?: TipoMovimiento
  documento?: DocumentoMovimiento
  usuario_crea?: any
  usuario_autoriza?: any
  usuario_procesa?: any
  bodega_origen?: any
  bodega_destino?: any
  detalles?: MovimientoDetalle[]
}

export interface MovimientoInventarioCreate {
  id_tipo_movimiento: number
  fecha_movimiento: string
  motivo: string
  observaciones?: string
  id_documento?: number
  id_bodega_origen?: number
  id_bodega_destino?: number
  activo: boolean
}

export interface MovimientoInventarioUpdate {
  fecha_movimiento?: string
  motivo?: string
  observaciones?: string
  id_documento?: number
  id_bodega_origen?: number
  id_bodega_destino?: number
  activo?: boolean
}

// movimientos_detalle - Detalle por Producto (SIMPLIFICADO)
export interface MovimientoDetalle {
  id_detalle: number
  id_movimiento: number
  id_producto: number
  cantidad: number
  costo_unitario: number
  costo_total: number

  // Ubicaciones origen y destino
  id_ubicacion_origen?: number
  id_ubicacion_destino?: number

  observaciones?: string
  activo: boolean
  fecha_creacion?: string

  // Relaciones
  producto?: any
  ubicacion_origen?: any
  ubicacion_destino?: any
}

export interface MovimientoDetalleCreate {
  id_producto: number
  cantidad: number
  costo_unitario: number
  id_ubicacion_origen?: number
  id_ubicacion_destino?: number
  observaciones?: string
  activo: boolean
}

export interface MovimientoDetalleUpdate {
  cantidad?: number
  costo_unitario?: number
  id_ubicacion_origen?: number
  id_ubicacion_destino?: number
  observaciones?: string
  activo?: boolean
}

export const useMovimientoStore = defineStore('movimientos', () => {
  const apiStore = useApiStore()

  const tiposMovimiento = ref<TipoMovimiento[]>([])
  const documentosMovimiento = ref<DocumentoMovimiento[]>([])
  const movimientosInventario = ref<MovimientoInventario[]>([])
  const movimientosDetalle = ref<MovimientoDetalle[]>([])
  const isLoading = ref(false)

  // CRUD Tipos de Movimiento
  const obtenerTiposMovimiento = async (params?: {
    activo?: boolean
  }): Promise<TipoMovimiento[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const url = `/tipos-movimiento?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener tipos de movimiento')
      }
      tiposMovimiento.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener tipos de movimiento:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerTipoMovimiento = async (id: number): Promise<TipoMovimiento> => {
    try {
      const response = await apiStore.get(`/tipos-movimiento/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener tipo de movimiento')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener tipo de movimiento:', error)
      throw error
    }
  }

  // CRUD Documentos Movimiento
  const obtenerDocumentosMovimiento = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
    tipo?: string
  }): Promise<DocumentoMovimiento[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')
      if (params?.tipo) queryParams.append('tipo', params.tipo)

      const url = `/documentos-movimiento?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener documentos')
      }
      documentosMovimiento.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener documentos:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const crearDocumentoMovimiento = async (documento: DocumentoMovimientoCreate): Promise<DocumentoMovimiento> => {
    try {
      const response = await apiStore.post('/documentos-movimiento', documento)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear documento')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear documento:', error)
      throw error
    }
  }

  const subirArchivoDocumento = async (documentoId: number, archivo: File): Promise<string> => {
    try {
      const formData = new FormData()
      formData.append('archivo', archivo)

      const response = await apiStore.post(`/documentos-movimiento/${documentoId}/archivo`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      if (!response.success) {
        throw new Error(response.error || 'Error al subir archivo')
      }
      return response.data.url_archivo
    } catch (error) {
      console.error('Error al subir archivo:', error)
      throw error
    }
  }

  // CRUD Movimientos Inventario
  const obtenerMovimientosInventario = async (params?: {
    skip?: number
    limit?: number
    estado?: string
    tipo_movimiento?: number
    fecha_desde?: string
    fecha_hasta?: string
    usuario_id?: number
  }): Promise<MovimientoInventario[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.estado) queryParams.append('estado', params.estado)
      if (params?.tipo_movimiento) queryParams.append('tipo_movimiento', params.tipo_movimiento.toString())
      if (params?.fecha_desde) queryParams.append('fecha_desde', params.fecha_desde)
      if (params?.fecha_hasta) queryParams.append('fecha_hasta', params.fecha_hasta)
      if (params?.usuario_id) queryParams.append('usuario_id', params.usuario_id.toString())

      const url = `/movimientos-inventario?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener movimientos')
      }
      movimientosInventario.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener movimientos:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerMovimientoInventario = async (id: number): Promise<MovimientoInventario> => {
    try {
      const response = await apiStore.get(`/movimientos-inventario/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener movimiento')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener movimiento:', error)
      throw error
    }
  }

  const crearMovimientoInventario = async (movimiento: MovimientoInventarioCreate): Promise<MovimientoInventario> => {
    try {
      const response = await apiStore.post('/movimientos-inventario', movimiento)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear movimiento')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear movimiento:', error)
      throw error
    }
  }

  const actualizarMovimientoInventario = async (id: number, movimiento: MovimientoInventarioUpdate): Promise<MovimientoInventario> => {
    try {
      const response = await apiStore.put(`/movimientos-inventario/${id}`, movimiento)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar movimiento')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar movimiento:', error)
      throw error
    }
  }

  const autorizarMovimiento = async (id: number, observaciones?: string): Promise<MovimientoInventario> => {
    try {
      const response = await apiStore.post(`/movimientos-inventario/${id}/autorizar`, { observaciones })
      if (!response.success) {
        throw new Error(response.error || 'Error al autorizar movimiento')
      }
      return response.data
    } catch (error) {
      console.error('Error al autorizar movimiento:', error)
      throw error
    }
  }

  const procesarMovimiento = async (id: number): Promise<MovimientoInventario> => {
    try {
      const response = await apiStore.post(`/movimientos-inventario/${id}/procesar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al procesar movimiento')
      }
      return response.data
    } catch (error) {
      console.error('Error al procesar movimiento:', error)
      throw error
    }
  }

  const cancelarMovimiento = async (id: number, motivo: string): Promise<MovimientoInventario> => {
    try {
      const response = await apiStore.post(`/movimientos-inventario/${id}/cancelar`, { motivo })
      if (!response.success) {
        throw new Error(response.error || 'Error al cancelar movimiento')
      }
      return response.data
    } catch (error) {
      console.error('Error al cancelar movimiento:', error)
      throw error
    }
  }

  // CRUD Movimientos Detalle
  const obtenerMovimientosDetalle = async (movimientoId: number): Promise<MovimientoDetalle[]> => {
    try {
      const response = await apiStore.get(`/movimientos-detalle/movimiento/${movimientoId}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener detalles del movimiento')
      }
      movimientosDetalle.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener detalles del movimiento:', error)
      throw error
    }
  }

  const crearMovimientoDetalle = async (movimientoId: number, detalle: MovimientoDetalleCreate): Promise<MovimientoDetalle> => {
    try {
      const response = await apiStore.post(`/movimientos-detalle/movimiento/${movimientoId}`, detalle)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear detalle del movimiento')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear detalle del movimiento:', error)
      throw error
    }
  }

  const actualizarMovimientoDetalle = async (id: number, detalle: MovimientoDetalleUpdate): Promise<MovimientoDetalle> => {
    try {
      const response = await apiStore.put(`/movimientos-detalle/${id}`, detalle)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar detalle del movimiento')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar detalle del movimiento:', error)
      throw error
    }
  }

  const eliminarMovimientoDetalle = async (id: number): Promise<void> => {
    try {
      const response = await apiStore.delete(`/movimientos-detalle/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar detalle del movimiento')
      }
    } catch (error) {
      console.error('Error al eliminar detalle del movimiento:', error)
      throw error
    }
  }

  // Métodos de validación y estadísticas
  const validarMovimiento = async (movimientoId: number): Promise<{
    valido: boolean
    errores: string[]
    advertencias: string[]
  }> => {
    try {
      const response = await apiStore.get(`/movimientos-inventario/${movimientoId}/validar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al validar movimiento')
      }
      return response.data
    } catch (error) {
      console.error('Error al validar movimiento:', error)
      throw error
    }
  }

  const obtenerEstadisticasMovimientos = async (params?: {
    fecha_desde?: string
    fecha_hasta?: string
    tipo_movimiento?: number
  }): Promise<{
    total_movimientos: number
    pendientes: number
    autorizados: number
    procesados: number
    cancelados: number
    valor_total: number
    movimientos_por_tipo: any[]
  }> => {
    try {
      const queryParams = new URLSearchParams()

      if (params?.fecha_desde) queryParams.append('fecha_desde', params.fecha_desde)
      if (params?.fecha_hasta) queryParams.append('fecha_hasta', params.fecha_hasta)
      if (params?.tipo_movimiento) queryParams.append('tipo_movimiento', params.tipo_movimiento.toString())

      const url = `/movimientos-inventario/stats?${queryParams.toString()}`
      const response = await apiStore.get(url)
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
    tiposMovimiento,
    documentosMovimiento,
    movimientosInventario,
    movimientosDetalle,
    isLoading,

    // Methods - Tipos Movimiento
    obtenerTiposMovimiento,
    obtenerTipoMovimiento,

    // Methods - Documentos
    obtenerDocumentosMovimiento,
    crearDocumentoMovimiento,
    subirArchivoDocumento,

    // Methods - Movimientos Inventario
    obtenerMovimientosInventario,
    obtenerMovimientoInventario,
    crearMovimientoInventario,
    actualizarMovimientoInventario,
    autorizarMovimiento,
    procesarMovimiento,
    cancelarMovimiento,

    // Methods - Movimientos Detalle
    obtenerMovimientosDetalle,
    crearMovimientoDetalle,
    actualizarMovimientoDetalle,
    eliminarMovimientoDetalle,

    // Methods - Validación y Estadísticas
    validarMovimiento,
    obtenerEstadisticasMovimientos
  }
})