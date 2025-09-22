import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface DocumentoCompraDetalle {
  id_detalle?: number
  id_documento?: number
  id_producto?: number
  codigo_producto?: string
  descripcion: string
  cantidad: number
  id_unidad_medida?: number
  precio_unitario: number
  descuento_linea: number
  subtotal_linea: number
  impuesto_linea: number
  total_linea: number
  numero_linea: number
  cantidad_recibida?: number
  diferencia_cantidad?: number
  motivo_diferencia?: string
  activo?: boolean
  fecha_creacion?: string
  fecha_modificacion?: string
}

export interface DocumentoCompraArchivo {
  id_archivo?: number
  id_documento?: number
  nombre_archivo: string
  ruta_archivo: string
  tipo_archivo: 'XML' | 'PDF' | 'IMAGEN' | 'OTRO'
  tamaño_archivo?: number
  mime_type?: string
  hash_archivo?: string
  activo?: boolean
  fecha_subida?: string
  usuario_subida?: number
}

export interface DocumentoCompra {
  id_documento?: number
  id_orden_compra?: number
  tipo_documento: 'FACTURA' | 'FACTURA_EXENTA' | 'BOLETA' | 'NOTA_CREDITO' | 'NOTA_DEBITO' | 'GUIA_DESPACHO' | 'OTRO'
  numero_documento: string
  fecha_documento: string
  serie?: string
  folio?: string
  uuid_fiscal?: string
  rut_emisor?: string
  rut_receptor?: string
  subtotal: number
  impuestos: number
  descuentos: number
  total: number
  moneda: string
  tipo_cambio: number
  contenido_xml?: string
  estado: 'PENDIENTE' | 'VALIDADO' | 'DISPONIBLE_BODEGA' | 'INGRESADO_BODEGA' | 'ANULADO'
  disponible_bodega: boolean
  fecha_ingreso_bodega?: string
  usuario_ingreso_bodega?: number
  errores_procesamiento?: string
  observaciones?: string
  activo: boolean
  fecha_creacion?: string
  fecha_modificacion?: string
  usuario_creacion?: number
  usuario_modificacion?: number
  detalles?: DocumentoCompraDetalle[]
  archivos?: DocumentoCompraArchivo[]
}

export interface DocumentoCreate {
  id_orden_compra?: number
  tipo_documento: 'FACTURA' | 'FACTURA_EXENTA' | 'BOLETA' | 'NOTA_CREDITO' | 'NOTA_DEBITO' | 'GUIA_DESPACHO' | 'OTRO'
  numero_documento: string
  fecha_documento: string
  serie?: string
  folio?: string
  uuid_fiscal?: string
  rut_emisor?: string
  rut_receptor?: string
  subtotal: number
  impuestos: number
  descuentos: number
  total: number
  moneda: string
  tipo_cambio: number
  contenido_xml?: string
  observaciones?: string
  activo?: boolean
  detalles: DocumentoCompraDetalle[]
}

export interface DocumentoUpdate {
  id_orden_compra?: number
  tipo_documento?: 'FACTURA' | 'FACTURA_EXENTA' | 'BOLETA' | 'NOTA_CREDITO' | 'NOTA_DEBITO' | 'GUIA_DESPACHO' | 'OTRO'
  numero_documento?: string
  fecha_documento?: string
  serie?: string
  folio?: string
  uuid_fiscal?: string
  rut_emisor?: string
  rut_receptor?: string
  subtotal?: number
  impuestos?: number
  descuentos?: number
  total?: number
  moneda?: string
  tipo_cambio?: number
  contenido_xml?: string
  estado?: 'PENDIENTE' | 'VALIDADO' | 'DISPONIBLE_BODEGA' | 'INGRESADO_BODEGA' | 'ANULADO'
  disponible_bodega?: boolean
  observaciones?: string
  activo?: boolean
}


export const useDocumentoStore = defineStore('documentos', () => {
  const apiStore = useApiStore()

  const documentos = ref<DocumentoCompra[]>([])
  const isLoading = ref(false)

  // CRUD Documentos
  const obtenerDocumentos = async (params?: {
    skip?: number
    limit?: number
    activo?: boolean
    estado?: string
    tipo_documento?: string
  }): Promise<DocumentoCompra[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')
      if (params?.estado) queryParams.append('estado', params.estado)
      if (params?.tipo_documento) queryParams.append('tipo_documento', params.tipo_documento)
      const url = `/documentos-compra?${queryParams.toString()}`
      console.log('URL construida documentos:', url, 'params recibidos:', params)
      const response = await apiStore.get(url)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener documentos')
      }
      documentos.value = response.data
      return response.data
    } catch (error) {
      console.error('Error al obtener documentos:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const obtenerDocumento = async (id: number): Promise<DocumentoCompra> => {
    try {
      const response = await apiStore.get(`/documentos-compra/${id}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al obtener documento')
      }
      return response.data
    } catch (error) {
      console.error('Error al obtener documento:', error)
      throw error
    }
  }


  const crearDocumento = async (documento: DocumentoCreate): Promise<DocumentoCompra> => {
    try {
      const response = await apiStore.post('/documentos-compra', documento)
      if (!response.success) {
        throw new Error(response.error || 'Error al crear documento')
      }
      return response.data
    } catch (error) {
      console.error('Error al crear documento:', error)
      throw error
    }
  }

  const actualizarDocumento = async (id: number, documento: DocumentoUpdate): Promise<DocumentoCompra> => {
    try {
      const response = await apiStore.put(`/documentos-compra/${id}`, documento)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar documento')
      }
      return response.data
    } catch (error) {
      console.error('Error al actualizar documento:', error)
      throw error
    }
  }

  const eliminarDocumento = async (id: number, permanente: boolean = false): Promise<void> => {
    try {
      const params = new URLSearchParams()
      params.append('permanente', permanente.toString())

      const response = await apiStore.delete(`/documentos-compra/${id}?${params.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al eliminar documento')
      }
    } catch (error) {
      console.error('Error al eliminar documento:', error)
      throw error
    }
  }

  const activarDocumento = async (id: number): Promise<DocumentoCompra> => {
    try {
      const response = await apiStore.patch(`/documentos-compra/${id}/activar`)
      if (!response.success) {
        throw new Error(response.error || 'Error al activar documento')
      }
      return response.data.documento
    } catch (error) {
      console.error('Error al activar documento:', error)
      throw error
    }
  }



  // Búsqueda
  const buscarDocumentos = async (
    searchTerm: string,
    params?: {
      skip?: number
      limit?: number
      activo?: boolean
    }
  ): Promise<DocumentoCompra[]> => {
    try {
      isLoading.value = true
      const queryParams = new URLSearchParams()
      queryParams.append('q', searchTerm)

      if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
      if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString())
      if (params?.activo !== undefined) queryParams.append('activo', params.activo === true ? 'true' : 'false')

      const response = await apiStore.get(`/documentos-compra/search?${queryParams.toString()}`)
      if (!response.success) {
        throw new Error(response.error || 'Error al buscar documentos')
      }
      return response.data
    } catch (error) {
      console.error('Error al buscar documentos:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }




  // Búsqueda de órdenes de compra (para el selector)
  const buscarOrdenesCompra = async (searchTerm: string) => {
    try {
      const response = await apiStore.get(`/ordenes-compra/search?q=${encodeURIComponent(searchTerm)}&limit=20`)
      if (!response.success) {
        throw new Error(response.error || 'Error al buscar órdenes de compra')
      }
      return response.data
    } catch (error) {
      console.error('Error al buscar órdenes de compra:', error)
      throw error
    }
  }

  return {
    // State
    documentos,
    isLoading,

    // Methods - CRUD
    obtenerDocumentos,
    obtenerDocumento,
    crearDocumento,
    actualizarDocumento,
    eliminarDocumento,
    activarDocumento,

    // Methods - Búsqueda
    buscarDocumentos,
    buscarOrdenesCompra
  }
})