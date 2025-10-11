import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useApiStore } from './api'

export interface StockItem {
  id_stock: number
  id_producto: number
  id_bodega: number
  stock_actual: number
  stock_minimo: number
  stock_maximo: number
  punto_reorden: number
  costo_promedio?: number
  fecha_ultima_actualizacion?: string
  ubicacion_completa?: string
  producto?: {
    sku: string
    nombre_producto: string
    unidad_medida?: {
      codigo: string
    }
  }
  bodega?: {
    codigo_bodega: string
    nombre_bodega: string
  }
}

export interface AjusteStock {
  id_producto: number
  id_bodega: number
  stock_anterior: number
  stock_nuevo: number
  tipo_ajuste: string
  motivo: string
}

export interface TransferenciaStock {
  id_producto: number
  id_bodega_origen: number
  id_bodega_destino: number
  cantidad: number
  motivo: string
}

export interface MovimientoStock {
  id_movimiento: number
  id_producto: number
  id_bodega: number
  tipo_movimiento: 'ENTRADA' | 'SALIDA' | 'TRANSFERENCIA' | 'AJUSTE'
  cantidad: number
  stock_anterior: number
  stock_nuevo: number
  fecha_movimiento: string
  motivo?: string
  usuario?: string
}

export const useStockStore = defineStore('stock', () => {
  const apiStore = useApiStore()

  // Estado reactivo
  const stockItems = ref<StockItem[]>([])
  const isLoading = ref(false)

  // Obtener stock por bodega
  const obtenerStockPorBodega = async (bodegaId?: number, params?: any): Promise<StockItem[]> => {
    try {
      isLoading.value = true

      // Simulación temporal hasta que el backend esté listo
      await new Promise(resolve => setTimeout(resolve, 500))

      const datosSimulados: StockItem[] = [
        {
          id_stock: 1,
          id_producto: 1,
          id_bodega: 1,
          stock_actual: 150,
          stock_minimo: 50,
          stock_maximo: 500,
          punto_reorden: 75,
          costo_promedio: 25.50,
          fecha_ultima_actualizacion: '2024-01-15T10:30:00',
          ubicacion_completa: 'A-01-A',
          producto: {
            sku: 'SPRK-001',
            nombre_producto: 'Sprinkler Estándar 15mm',
            unidad_medida: { codigo: 'UN' }
          },
          bodega: {
            codigo_bodega: 'A',
            nombre_bodega: 'Bodega Principal'
          }
        },
        {
          id_stock: 2,
          id_producto: 2,
          id_bodega: 1,
          stock_actual: 25,
          stock_minimo: 30,
          stock_maximo: 200,
          punto_reorden: 40,
          costo_promedio: 45.75,
          fecha_ultima_actualizacion: '2024-01-14T16:45:00',
          ubicacion_completa: 'B-02-C',
          producto: {
            sku: 'VAL-002',
            nombre_producto: 'Válvula de Control 2"',
            unidad_medida: { codigo: 'UN' }
          },
          bodega: {
            codigo_bodega: 'A',
            nombre_bodega: 'Bodega Principal'
          }
        },
        {
          id_stock: 3,
          id_producto: 3,
          id_bodega: 2,
          stock_actual: 0,
          stock_minimo: 10,
          stock_maximo: 100,
          punto_reorden: 15,
          costo_promedio: 120.00,
          fecha_ultima_actualizacion: '2024-01-10T09:15:00',
          ubicacion_completa: null,
          producto: {
            sku: 'BOMB-003',
            nombre_producto: 'Bomba Centrífuga 5HP',
            unidad_medida: { codigo: 'UN' }
          },
          bodega: {
            codigo_bodega: 'B',
            nombre_bodega: 'Bodega Equipos'
          }
        },
        {
          id_stock: 4,
          id_producto: 4,
          id_bodega: 1,
          stock_actual: 75,
          stock_minimo: 20,
          stock_maximo: 300,
          punto_reorden: 30,
          costo_promedio: 15.25,
          fecha_ultima_actualizacion: '2024-01-16T08:20:00',
          ubicacion_completa: 'C-03-B',
          producto: {
            sku: 'TUB-004',
            nombre_producto: 'Tubería CPVC 2" SCH40',
            unidad_medida: { codigo: 'MT' }
          },
          bodega: {
            codigo_bodega: 'A',
            nombre_bodega: 'Bodega Principal'
          }
        },
        {
          id_stock: 5,
          id_producto: 5,
          id_bodega: 3,
          stock_actual: 5,
          stock_minimo: 15,
          stock_maximo: 100,
          punto_reorden: 20,
          costo_promedio: 85.00,
          fecha_ultima_actualizacion: '2024-01-12T14:30:00',
          ubicacion_completa: 'A-01-C',
          producto: {
            sku: 'DET-005',
            nombre_producto: 'Detector de Humo Fotoeléctrico',
            unidad_medida: { codigo: 'UN' }
          },
          bodega: {
            codigo_bodega: 'C',
            nombre_bodega: 'Bodega Repuestos'
          }
        }
      ]

      // Filtrar por bodega si se especifica
      let resultado = bodegaId ? datosSimulados.filter(item => item.id_bodega === bodegaId) : datosSimulados

      // Aplicar otros filtros si existen
      if (params?.busqueda) {
        const busqueda = params.busqueda.toLowerCase()
        resultado = resultado.filter(item =>
          item.producto?.sku.toLowerCase().includes(busqueda) ||
          item.producto?.nombre_producto.toLowerCase().includes(busqueda)
        )
      }

      stockItems.value = resultado
      return resultado
    } catch (error) {
      console.error('Error obteniendo stock:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // Obtener stock consolidado (todos las bodegas)
  const obtenerStockConsolidado = async (params?: any): Promise<StockItem[]> => {
    // Reutilizar la simulación del método anterior sin filtro de bodega
    return await obtenerStockPorBodega(undefined, params)
  }

  // Obtener stock de un producto específico
  const obtenerStockProducto = async (productoId: number): Promise<StockItem[]> => {
    try {
      const response = await apiStore.get(`/stock/producto/${productoId}`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo stock del producto:', error)
      throw error
    }
  }

  // Realizar ajuste de stock
  const realizarAjusteStock = async (ajuste: AjusteStock): Promise<void> => {
    try {
      // Simulación temporal
      await new Promise(resolve => setTimeout(resolve, 1000))
      console.log('Ajuste de stock simulado:', ajuste)
    } catch (error) {
      console.error('Error realizando ajuste de stock:', error)
      throw error
    }
  }

  // Realizar transferencia de stock
  const realizarTransferenciaStock = async (transferencia: TransferenciaStock): Promise<void> => {
    try {
      // Simulación temporal
      await new Promise(resolve => setTimeout(resolve, 1000))
      console.log('Transferencia de stock simulada:', transferencia)
    } catch (error) {
      console.error('Error realizando transferencia de stock:', error)
      throw error
    }
  }

  // Obtener historial de movimientos
  const obtenerHistorialMovimientos = async (
    productoId: number,
    bodegaId?: number,
    params?: any
  ): Promise<MovimientoStock[]> => {
    try {
      // Simulación temporal
      await new Promise(resolve => setTimeout(resolve, 300))

      const movimientosSimulados: MovimientoStock[] = [
        {
          id_movimiento: 1,
          id_producto: productoId,
          id_bodega: bodegaId || 1,
          tipo_movimiento: 'ENTRADA',
          cantidad: 100,
          stock_anterior: 50,
          stock_nuevo: 150,
          fecha_movimiento: '2024-01-15T10:30:00',
          motivo: 'Compra a proveedor',
          usuario: 'Juan Pérez'
        },
        {
          id_movimiento: 2,
          id_producto: productoId,
          id_bodega: bodegaId || 1,
          tipo_movimiento: 'SALIDA',
          cantidad: 25,
          stock_anterior: 150,
          stock_nuevo: 125,
          fecha_movimiento: '2024-01-14T14:20:00',
          motivo: 'Despacho a obra',
          usuario: 'María García'
        },
        {
          id_movimiento: 3,
          id_producto: productoId,
          id_bodega: bodegaId || 1,
          tipo_movimiento: 'AJUSTE',
          cantidad: 25,
          stock_anterior: 125,
          stock_nuevo: 150,
          fecha_movimiento: '2024-01-13T09:15:00',
          motivo: 'Ajuste por inventario físico',
          usuario: 'Carlos López'
        }
      ]

      return movimientosSimulados
    } catch (error) {
      console.error('Error obteniendo historial de movimientos:', error)
      throw error
    }
  }

  // Obtener resumen de stock
  const obtenerResumenStock = async (bodegaId?: number): Promise<any> => {
    try {
      const queryParams = new URLSearchParams()
      if (bodegaId) queryParams.append('bodega_id', bodegaId.toString())

      const response = await apiStore.get(`/stock/resumen?${queryParams}`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo resumen de stock:', error)
      throw error
    }
  }

  // Exportar stock
  const exportarStock = async (formato: 'xlsx' | 'csv', params?: any): Promise<Blob> => {
    try {
      // Simulación temporal - crear un blob simulado
      await new Promise(resolve => setTimeout(resolve, 2000))

      const csvContent = `SKU,Producto,Bodega,Stock Actual,Stock Mínimo,Punto Reorden,Costo Promedio,Valor Total
SPRK-001,Sprinkler Estándar 15mm,Bodega Principal,150,50,75,25.50,3825.00
VAL-002,Válvula de Control 2",Bodega Principal,25,30,40,45.75,1143.75
BOMB-003,Bomba Centrífuga 5HP,Bodega Equipos,0,10,15,120.00,0.00
TUB-004,Tubería CPVC 2" SCH40,Bodega Principal,75,20,30,15.25,1143.75
DET-005,Detector de Humo Fotoeléctrico,Bodega Repuestos,5,15,20,85.00,425.00`

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      return blob
    } catch (error) {
      console.error('Error exportando stock:', error)
      throw error
    }
  }

  // Obtener productos con stock bajo
  const obtenerProductosStockBajo = async (bodegaId?: number): Promise<StockItem[]> => {
    try {
      const queryParams = new URLSearchParams()
      if (bodegaId) queryParams.append('bodega_id', bodegaId.toString())

      const response = await apiStore.get(`/stock/stock-bajo?${queryParams}`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo productos con stock bajo:', error)
      throw error
    }
  }

  // Obtener productos sin stock
  const obtenerProductosSinStock = async (bodegaId?: number): Promise<StockItem[]> => {
    try {
      const queryParams = new URLSearchParams()
      if (bodegaId) queryParams.append('bodega_id', bodegaId.toString())

      const response = await apiStore.get(`/stock/sin-stock?${queryParams}`)
      return response.data
    } catch (error) {
      console.error('Error obteniendo productos sin stock:', error)
      throw error
    }
  }

  // Buscar stock por SKU o nombre
  const buscarStock = async (termino: string, params?: any): Promise<StockItem[]> => {
    // Reutilizar el método obtenerStockPorBodega con parámetros de búsqueda
    return await obtenerStockPorBodega(params?.bodega_id, { ...params, busqueda: termino })
  }

  return {
    // Estado
    stockItems,
    isLoading,

    // Métodos
    obtenerStockPorBodega,
    obtenerStockConsolidado,
    obtenerStockProducto,
    realizarAjusteStock,
    realizarTransferenciaStock,
    obtenerHistorialMovimientos,
    obtenerResumenStock,
    exportarStock,
    obtenerProductosStockBajo,
    obtenerProductosSinStock,
    buscarStock
  }
})