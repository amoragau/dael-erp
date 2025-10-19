import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface ProveedorSimple {
  id_proveedor: number
  nombre_proveedor?: string
  razon_social: string
  rfc: string
}

export interface EstadoSimple {
  id_estado: number
  codigo_estado: string
  nombre_estado: string
}

export interface CentroCostoSimple {
  id_centro_costo: number
  codigo_centro_costo: string
  nombre_centro_costo: string
}

export interface EmpresaSimple {
  id_empresa: number
  rut_empresa: string
  razon_social: string
  nombre_fantasia?: string
}

export interface OrdenCompra {
  id_orden_compra: number
  numero_orden: string
  id_proveedor: number
  id_centro_costo: number
  id_empresa?: number
  fecha_orden: string
  fecha_requerida: string
  fecha_prometida?: string
  subtotal: number
  impuestos: number
  iva_porcentaje: number
  descuentos: number
  total: number
  moneda: string
  tipo_cambio: number
  terminos_pago?: string
  terminos_entrega?: string
  direccion_entrega?: string
  contacto_entrega?: string
  telefono_contacto?: string
  contacto_proveedor?: string
  observaciones?: string
  aprobada_por?: number
  fecha_aprobacion?: string
  autorizada_por?: number
  fecha_autorizacion?: string
  enviada_por?: number
  fecha_envio?: string
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string
  usuario_creacion?: number
  usuario_modificacion?: number

  // Relaciones
  proveedor?: ProveedorSimple
  estado?: EstadoSimple
  centro_costo?: CentroCostoSimple
  empresa?: EmpresaSimple
  usuario_aprobacion?: any
  usuario_autorizacion?: any
  usuario_envio?: any
  detalles?: OrdenCompraDetalle[]
}

export interface OrdenCompraDetalle {
  id_detalle_oc: number
  id_orden_compra: number
  numero_linea: number
  id_producto: number
  cantidad_solicitada: number
  cantidad_recibida: number
  precio_unitario: number
  descuento_porcentaje: number
  descuento_monto: number
  impuesto_porcentaje: number
  impuesto_monto: number
  precio_neto: number
  importe_total: number
  especificaciones?: string
  observaciones?: string
  fecha_requerida?: string
  fecha_prometida?: string
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string

  // Relaciones
  producto?: any
}

export interface OrdenCompraCreate {
  numero_orden?: string
  id_proveedor: number
  id_usuario_solicitante: number
  id_centro_costo: number
  id_empresa?: number
  fecha_orden: string
  fecha_requerida: string
  fecha_prometida?: string
  estado?: string
  subtotal: number
  impuestos: number
  iva_porcentaje?: number
  descuentos: number
  total: number
  moneda?: string
  tipo_cambio?: number
  terminos_pago?: string
  terminos_entrega?: string
  direccion_entrega?: string
  contacto_entrega?: string
  telefono_contacto?: string
  contacto_proveedor?: string
  observaciones?: string
  activo?: boolean
  detalles: OrdenCompraDetalleCreate[]
}

export interface OrdenCompraDetalleCreate {
  numero_linea: number
  id_producto: number
  cantidad_solicitada: number
  precio_unitario: number
  descuento_porcentaje?: number
  descuento_monto?: number
  impuesto_porcentaje?: number
  impuesto_monto?: number
  precio_neto: number
  importe_total: number
  especificaciones?: string
  observaciones?: string
  fecha_requerida?: string
  fecha_prometida?: string
  activo?: boolean
}

export interface OrdenCompraUpdate {
  numero_orden?: string
  id_proveedor?: number
  fecha_orden?: string
  fecha_requerida?: string
  fecha_prometida?: string
  estado?: string
  subtotal?: number
  impuestos?: number
  iva_porcentaje?: number
  descuentos?: number
  total?: number
  moneda?: string
  tipo_cambio?: number
  terminos_pago?: string
  terminos_entrega?: string
  direccion_entrega?: string
  contacto_entrega?: string
  telefono_contacto?: string
  contacto_proveedor?: string
  observaciones?: string
  activo?: boolean
}

export interface EstadoOrdenCompra {
  estado: string
  nombre_estado: string
  descripcion: string
}

export interface Proveedor {
  id_proveedor: number
  rut_proveedor: string
  razon_social: string
  nombre_contacto?: string
  email?: string
  telefono?: string
  direccion?: string
  activo: boolean
}

export interface Producto {
  id_producto: number
  sku: string
  nombre_producto: string
  descripcion_corta?: string
  precio_venta?: number
  costo_promedio?: number
  stock_actual?: number
  unidad_medida?: any
}

export const useOrdenCompraStore = defineStore('ordenesCompra', () => {
  const apiStore = useApiStore()

  const ordenesCompra = ref<OrdenCompra[]>([])
  const estadosOrdenCompra = ref<EstadoOrdenCompra[]>([])
  const proveedores = ref<Proveedor[]>([])
  const productos = ref<Producto[]>([])
  const isLoading = ref(false)

  // CRUD Órdenes de Compra
  const obtenerOrdenesCompra = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
    estado?: string
    proveedor_id?: number
    fecha_desde?: string
    fecha_hasta?: string
  }): Promise<OrdenCompra[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')
      if (params?.estado) queryParams.append('estado', params.estado)
      if (params?.proveedor_id !== undefined) queryParams.append('proveedor_id', params.proveedor_id.toString())
      if (params?.fecha_desde) queryParams.append('fecha_desde', params.fecha_desde)
      if (params?.fecha_hasta) queryParams.append('fecha_hasta', params.fecha_hasta)

      const url = `/ordenes-compra?${queryParams.toString()}`
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener órdenes de compra')
      }
      ordenesCompra.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener órdenes de compra:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const buscarOrdenesCompra = async (
    searchTerm: string,
    params?: {
      skip?: number
      limit?: number
      activo?: boolean
    }
  ): Promise<OrdenCompra[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()
      queryParams.append('q', searchTerm)

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const response = await apiStore.get(`/ordenes-compra/search?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al buscar órdenes de compra')
      }
      return response.data
    } catch (error) {
      console.error('Error al buscar órdenes de compra:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerOrdenCompra = async (id: number): Promise<OrdenCompra> => {
    try {
      const response = await apiStore.get(`/ordenes-compra/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener orden de compra')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener orden de compra:', error)
      throw error
    }
  }

  const obtenerOrdenCompraPorNumero = async (numeroOrden: string): Promise<OrdenCompra> => {
    try {
      const response = await apiStore.get(`/ordenes-compra/numero/${numeroOrden}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener orden de compra por número')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener orden de compra por número:', error)
      throw error
    }
  }

  const generarSiguienteNumeroOrden = async (): Promise<string> => {
    try {
      const response = await apiStore.get('/ordenes-compra/generar-numero/')
      if (!response.success) {
        throw new Error(response.error || 'Error al generar número de orden')
      }
      return response.data.numero_orden
    } catch (error) {
      console.error('Error al generar número de orden:', error)
      throw error
    }
  }

  const crearOrdenCompra = async (ordenCompra: OrdenCompraCreate): Promise<OrdenCompra> => {
    try {
      // Si la orden tiene detalles, usar el endpoint completo
      const endpoint = ordenCompra.detalles && ordenCompra.detalles.length > 0
        ? '/ordenes-compra/completa/'
        : '/ordenes-compra/'

      // Adaptar el formato si se usa el endpoint completo
      const payload = ordenCompra.detalles && ordenCompra.detalles.length > 0
        ? {
            orden: {
              numero_orden: ordenCompra.numero_orden,
              id_proveedor: ordenCompra.id_proveedor,
              id_usuario_solicitante: ordenCompra.id_usuario_solicitante,
              id_centro_costo: ordenCompra.id_centro_costo,
              id_empresa: ordenCompra.id_empresa,
              fecha_orden: ordenCompra.fecha_orden,
              fecha_requerida: ordenCompra.fecha_requerida,
              fecha_esperada_entrega: ordenCompra.fecha_prometida,
              subtotal: ordenCompra.subtotal,
              impuestos: ordenCompra.impuestos,
              iva_porcentaje: ordenCompra.iva_porcentaje || 19.00,
              descuentos: ordenCompra.descuentos,
              total: ordenCompra.total,
              observaciones: ordenCompra.observaciones,
              terminos_pago: ordenCompra.terminos_pago,
              moneda: ordenCompra.moneda,
              tipo_cambio: ordenCompra.tipo_cambio,
              direccion_entrega: ordenCompra.direccion_entrega,
              contacto_entrega: ordenCompra.contacto_entrega,
              telefono_contacto: ordenCompra.telefono_contacto,
              activo: ordenCompra.activo
            },
            detalles: ordenCompra.detalles.map(detalle => ({
              id_producto: detalle.id_producto,
              cantidad_solicitada: detalle.cantidad_solicitada,
              precio_unitario: detalle.precio_unitario,
              descuento_porcentaje: detalle.descuento_porcentaje || 0,
              descuento_importe: detalle.descuento_monto || 0,
              precio_neto: detalle.precio_neto || 0,
              importe_total: detalle.importe_total || 0,
              observaciones: detalle.observaciones || '',
              numero_linea: detalle.numero_linea,
              activo: detalle.activo !== false
            }))
          }
        : ordenCompra

      const response = await apiStore.post(endpoint, payload)
      if (!response.success) {
        const error: any = new Error(response.error || 'Error al crear orden de compra')
        error.response = { data: response.data }
        throw error
      }
      return response.data
    } catch (error) {
      throw error
    }
  }

  const actualizarOrdenCompra = async (id: number, ordenCompra: OrdenCompraUpdate): Promise<OrdenCompra> => {
    try {
      const response = await apiStore.put(`/ordenes-compra/${id}`, ordenCompra)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar orden de compra')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar orden de compra:', error)
      throw error
    }
  }

  const eliminarOrdenCompra = async (id: number, permanente: boolean = false): Promise<void> => {
    try {
      const params = new URLSearchParams()
      params.append('permanente', permanente.toString())

      const response = await apiStore.delete(`/ordenes-compra/${id}?${params.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar orden de compra')
      }
    } catch (error) {
      console.error('Error al eliminar orden de compra:', error)
      throw error
    }
  }

  const activarOrdenCompra = async (id: number): Promise<OrdenCompra> => {
    try {
      const response = await apiStore.patch(`/ordenes-compra/${id}/activar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al activar orden de compra')
      }
      return response.data.orden_compra
    } catch (error) {
      console.error('Error al activar orden de compra:', error)
      throw error
    }
  }

  // Acciones de workflow
  const aprobarOrdenCompra = async (id: number, aprobadaPor: number): Promise<OrdenCompra> => {
    try {
      const response = await apiStore.patch(`/ordenes-compra/${id}/aprobar`, { aprobada_por: aprobadaPor })
      if (!response.success) {
        throw new Error(response.error || 'Error al aprobar orden de compra')
      }
      return response.data.orden_compra
    } catch (error) {
      console.error('Error al aprobar orden de compra:', error)
      throw error
    }
  }

  const autorizarOrdenCompra = async (id: number, autorizadaPor: number): Promise<OrdenCompra> => {
    try {
      const response = await apiStore.patch(`/ordenes-compra/${id}/autorizar`, { autorizada_por: autorizadaPor })
      if (!response.success) {
        throw new Error(response.error || 'Error al autorizar orden de compra')
      }
      return response.data.orden_compra
    } catch (error) {
      console.error('Error al autorizar orden de compra:', error)
      throw error
    }
  }

  const enviarOrdenCompra = async (id: number, enviadaPor: number): Promise<OrdenCompra> => {
    try {
      const response = await apiStore.patch(`/ordenes-compra/${id}/enviar`, { enviada_por: enviadaPor })
      if (!response.success) {
        throw new Error(response.error || 'Error al enviar orden de compra')
      }
      return response.data.orden_compra
    } catch (error) {
      console.error('Error al enviar orden de compra:', error)
      throw error
    }
  }

  const cerrarOrdenCompra = async (id: number): Promise<OrdenCompra> => {
    try {
      const response = await apiStore.patch(`/ordenes-compra/${id}/cerrar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al cerrar orden de compra')
      }
      return response.data.orden_compra
    } catch (error) {
      console.error('Error al cerrar orden de compra:', error)
      throw error
    }
  }

  const cancelarOrdenCompra = async (id: number, motivo?: string): Promise<OrdenCompra> => {
    try {
      const response = await apiStore.patch(`/ordenes-compra/${id}/cancelar`, { motivo })
      if (!response.success) {
        throw new Error(response.error || 'Error al cancelar orden de compra')
      }
      return response.data.orden_compra
    } catch (error) {
      console.error('Error al cancelar orden de compra:', error)
      throw error
    }
  }

  const rechazarOrdenCompra = async (id: number, motivo: string): Promise<OrdenCompra> => {
    try {
      const response = await apiStore.patch(`/ordenes-compra/${id}/rechazar`, { motivo })
      if (!response.success) {
        throw new Error(response.error || 'Error al rechazar orden de compra')
      }
      return response.data
    } catch (error) {
      console.error('Error al rechazar orden de compra:', error)
      throw error
    }
  }

  // Detalles de orden de compra
  const obtenerDetallesOrdenCompra = async (ordenCompraId: number): Promise<OrdenCompraDetalle[]> => {
    try {
      const response = await apiStore.get(`/ordenes-compra/${ordenCompraId}/detalles`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener detalles de orden de compra')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener detalles de orden de compra:', error)
      throw error
    }
  }

  const agregarDetalleOrdenCompra = async (
    ordenCompraId: number,
    detalle: OrdenCompraDetalleCreate
  ): Promise<OrdenCompraDetalle> => {
    try {
      const response = await apiStore.post(`/ordenes-compra/${ordenCompraId}/detalles`, detalle)
      if (!response.success) {
        throw new Error(response.error || 'Error al agregar detalle a orden de compra')
      }
      return response.data
    } catch (error) {
      console.error('Error al agregar detalle a orden de compra:', error)
      throw error
    }
  }

  const actualizarDetalleOrdenCompra = async (
    detalleId: number,
    detalle: Partial<OrdenCompraDetalle>
  ): Promise<OrdenCompraDetalle> => {
    try {
      const response = await apiStore.put(`/ordenes-compra/detalles/${detalleId}`, detalle)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar detalle de orden de compra')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar detalle de orden de compra:', error)
      throw error
    }
  }

  const eliminarDetalleOrdenCompra = async (detalleId: number): Promise<void> => {
    try {
      const response = await apiStore.delete(`/ordenes-compra/detalles/${detalleId}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar detalle de orden de compra')
      }
    } catch (error) {
      console.error('Error al eliminar detalle de orden de compra:', error)
      throw error
    }
  }

  // Datos relacionados
  const obtenerEstadosOrdenCompra = async (): Promise<EstadoOrdenCompra[]> => {
    try {
      const response = await apiStore.get('/estados-orden-compra')
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener estados de orden de compra')
      }
      estadosOrdenCompra.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener estados de orden de compra:', error)
      throw error
    }
  }

  const obtenerProveedores = async (): Promise<Proveedor[]> => {
    try {
      const response = await apiStore.get('/proveedores?activo=true')
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener proveedores')
      }
      proveedores.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener proveedores:', error)
      throw error
    }
  }

  const obtenerProductos = async (params?: {
    activo?: boolean
    busqueda?: string
  }): Promise<Producto[]> => {
    try {
      const queryParams = new URLSearchParams()
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')
      if (params?.busqueda) queryParams.append('q', params.busqueda)

      const response = await apiStore.get(`/productos?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener productos')
      }
      productos.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener productos:', error)
      throw error
    }
  }

  // Reportes y análisis
  const obtenerResumenOrdenesCompra = async (params?: {
    fecha_desde?: string
    fecha_hasta?: string
    proveedor_id?: number
  }): Promise<any> => {
    try {
      const queryParams = new URLSearchParams()
      if (params?.fecha_desde) queryParams.append('fecha_desde', params.fecha_desde)
      if (params?.fecha_hasta) queryParams.append('fecha_hasta', params.fecha_hasta)
      if (params?.proveedor_id !== undefined) queryParams.append('proveedor_id', params.proveedor_id.toString())

      const response = await apiStore.get(`/ordenes-compra/resumen?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener resumen de órdenes de compra')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener resumen de órdenes de compra:', error)
      throw error
    }
  }

  const obtenerEstadisticasOrdenesCompra = async (params?: {
    fecha_desde?: string
    fecha_hasta?: string
  }): Promise<any> => {
    try {
      const queryParams = new URLSearchParams()
      if (params?.fecha_desde) queryParams.append('fecha_desde', params.fecha_desde)
      if (params?.fecha_hasta) queryParams.append('fecha_hasta', params.fecha_hasta)

      const response = await apiStore.get(`/ordenes-compra/estadisticas?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener estadísticas de órdenes de compra')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener estadísticas de órdenes de compra:', error)
      throw error
    }
  }

  // Duplicar orden de compra
  const duplicarOrdenCompra = async (id: number): Promise<OrdenCompra> => {
    try {
      const response = await apiStore.post(`/ordenes-compra/${id}/duplicar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al duplicar orden de compra')
      }
      return response.data
    } catch (error) {
      console.error('Error al duplicar orden de compra:', error)
      throw error
    }
  }

  return {
    // State
    ordenesCompra,
    estadosOrdenCompra,
    proveedores,
    productos,
    isLoading,

    // Methods - Órdenes de Compra
    obtenerOrdenesCompra,
    buscarOrdenesCompra,
    obtenerOrdenCompra,
    obtenerOrdenCompraPorNumero,
    generarSiguienteNumeroOrden,
    crearOrdenCompra,
    actualizarOrdenCompra,
    eliminarOrdenCompra,
    activarOrdenCompra,

    // Methods - Workflow
    aprobarOrdenCompra,
    autorizarOrdenCompra,
    enviarOrdenCompra,
    cerrarOrdenCompra,
    cancelarOrdenCompra,
    rechazarOrdenCompra,

    // Methods - Detalles
    obtenerDetallesOrdenCompra,
    agregarDetalleOrdenCompra,
    actualizarDetalleOrdenCompra,
    eliminarDetalleOrdenCompra,

    // Methods - Datos relacionados
    obtenerEstadosOrdenCompra,
    obtenerProveedores,
    obtenerProductos,

    // Methods - Reportes
    obtenerResumenOrdenesCompra,
    obtenerEstadisticasOrdenesCompra,
    duplicarOrdenCompra
  }
})