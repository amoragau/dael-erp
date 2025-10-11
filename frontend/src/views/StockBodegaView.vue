<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Stock de Bodega</h4>
          <p class="text-grey-7 q-mb-none">Consulta y gestión del inventario por bodega</p>
        </div>
        <div class="q-gutter-sm">
          <q-btn
            color="secondary"
            icon="file_download"
            label="Exportar"
            @click="exportarStock"
          />
          <q-btn
            color="primary"
            icon="add"
            label="Ajuste de Stock"
            @click="abrirAjusteStock"
          />
        </div>
      </div>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-gutter-md items-end">
            <div class="col-12 col-md-3">
              <q-input
                v-model="filtros.busqueda"
                placeholder="Buscar por SKU o nombre..."
                outlined
                dense
                clearable
              >
                <template v-slot:prepend>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>

            <div class="col-12 col-md-2">
              <q-select
                v-model="filtros.bodega"
                :options="bodegasOptions"
                label="Bodega"
                outlined
                dense
                clearable
                emit-value
                map-options
              />
            </div>

            <div class="col-12 col-md-2">
              <q-select
                v-model="filtros.categoria"
                :options="categoriasOptions"
                label="Categoría"
                outlined
                dense
                clearable
                emit-value
                map-options
              />
            </div>

            <div class="col-12 col-md-2">
              <q-select
                v-model="filtros.estado_stock"
                :options="estadosStockOptions"
                label="Estado de Stock"
                outlined
                dense
                clearable
                emit-value
                map-options
              />
            </div>

            <div class="col-12 col-md-2">
              <q-toggle
                v-model="filtros.solo_activos"
                label="Solo activos"
                left-label
              />
            </div>

            <div class="col-auto">
              <q-btn
                color="primary"
                icon="search"
                label="Buscar"
                @click="buscarStock"
              />
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Summary Cards -->
      <div class="row q-gutter-md q-mb-md">
        <div class="col-12 col-sm-6 col-md-3">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-primary">{{ resumen.total_productos }}</div>
              <div class="text-caption text-grey-7">Productos Total</div>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-sm-6 col-md-3">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-green">{{ resumen.productos_stock_ok }}</div>
              <div class="text-caption text-grey-7">Stock Normal</div>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-sm-6 col-md-3">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-orange">{{ resumen.productos_stock_bajo }}</div>
              <div class="text-caption text-grey-7">Stock Bajo</div>
            </q-card-section>
          </q-card>
        </div>

        <div class="col-12 col-sm-6 col-md-3">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-red">{{ resumen.productos_sin_stock }}</div>
              <div class="text-caption text-grey-7">Sin Stock</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Stock Table -->
      <q-table
        :rows="stockItems"
        :columns="columnsStock"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_stock"
        flat
        bordered
        @request="onRequestStock"
      >
        <template v-slot:body-cell-producto="props">
          <q-td :props="props">
            <div>
              <div class="text-weight-bold">{{ props.row.producto?.sku }}</div>
              <div class="text-caption">{{ props.row.producto?.nombre_producto }}</div>
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-bodega="props">
          <q-td :props="props">
            <div>
              <div class="text-weight-bold">{{ props.row.bodega?.codigo_bodega }}</div>
              <div class="text-caption">{{ props.row.bodega?.nombre_bodega }}</div>
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-ubicacion="props">
          <q-td :props="props">
            <q-chip
              v-if="props.row.ubicacion_completa"
              size="sm"
              color="blue"
              text-color="white"
              icon="place"
            >
              {{ props.row.ubicacion_completa }}
            </q-chip>
            <span v-else class="text-grey-5">Sin ubicación</span>
          </q-td>
        </template>

        <template v-slot:body-cell-stock_actual="props">
          <q-td :props="props">
            <q-badge
              :color="getStockColor(props.row)"
              :label="formatStock(props.row.stock_actual)"
              class="q-mr-xs"
            />
            <span class="text-caption">{{ props.row.producto?.unidad_medida?.codigo || 'UN' }}</span>
          </q-td>
        </template>

        <template v-slot:body-cell-stock_minimo="props">
          <q-td :props="props">
            {{ formatStock(props.row.stock_minimo) }}
          </q-td>
        </template>

        <template v-slot:body-cell-punto_reorden="props">
          <q-td :props="props">
            {{ formatStock(props.row.punto_reorden) }}
          </q-td>
        </template>

        <template v-slot:body-cell-costo_promedio="props">
          <q-td :props="props">
            {{ formatCurrency(props.row.costo_promedio || 0) }}
          </q-td>
        </template>

        <template v-slot:body-cell-valor_total="props">
          <q-td :props="props">
            <span class="text-weight-bold">
              {{ formatCurrency((props.row.stock_actual || 0) * (props.row.costo_promedio || 0)) }}
            </span>
          </q-td>
        </template>

        <template v-slot:body-cell-estado="props">
          <q-td :props="props">
            <q-chip
              :color="getEstadoStockColor(props.row)"
              text-color="white"
              size="sm"
            >
              {{ getEstadoStockLabel(props.row) }}
            </q-chip>
          </q-td>
        </template>

        <template v-slot:body-cell-ultima_actualizacion="props">
          <q-td :props="props">
            {{ formatDateTime(props.row.fecha_ultima_actualizacion) }}
          </q-td>
        </template>

        <template v-slot:body-cell-acciones="props">
          <q-td :props="props">
            <div class="q-gutter-xs">
              <q-btn
                size="sm"
                color="blue"
                icon="visibility"
                @click="verHistorialMovimientos(props.row)"
                dense
                round
              >
                <q-tooltip>Ver historial</q-tooltip>
              </q-btn>
              <q-btn
                size="sm"
                color="green"
                icon="edit"
                @click="ajustarStock(props.row)"
                dense
                round
              >
                <q-tooltip>Ajustar stock</q-tooltip>
              </q-btn>
              <q-btn
                size="sm"
                color="orange"
                icon="transfer_within_a_station"
                @click="transferirStock(props.row)"
                dense
                round
              >
                <q-tooltip>Transferir</q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </template>
      </q-table>

      <!-- Dialog para ajuste de stock -->
      <q-dialog v-model="mostrarAjusteStock" persistent>
        <q-card style="min-width: 600px">
          <q-card-section class="row items-center">
            <div class="text-h6">
              {{ stockSeleccionado ? 'Ajustar Stock' : 'Nuevo Ajuste de Stock' }}
            </div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarAjusteStock">
              <div class="row q-gutter-md">
                <div class="col-12" v-if="!stockSeleccionado">
                  <q-select
                    v-model="formAjuste.id_producto"
                    :options="productosOptions"
                    label="Producto *"
                    outlined
                    dense
                    emit-value
                    map-options
                    use-input
                    clearable
                    input-debounce="300"
                    @filter="filtrarProductos"
                    :rules="[val => !!val || 'Producto es requerido']"
                  >
                    <template v-slot:option="scope">
                      <q-item v-bind="scope.itemProps">
                        <q-item-section>
                          <q-item-label>{{ scope.opt.label }}</q-item-label>
                          <q-item-label caption>SKU: {{ scope.opt.sku }}</q-item-label>
                        </q-item-section>
                      </q-item>
                    </template>
                  </q-select>
                </div>

                <div class="col-12" v-if="!stockSeleccionado">
                  <q-select
                    v-model="formAjuste.id_bodega"
                    :options="bodegasOptions"
                    label="Bodega *"
                    outlined
                    dense
                    emit-value
                    map-options
                    :rules="[val => !!val || 'Bodega es requerida']"
                  />
                </div>

                <div class="col-6" v-if="stockSeleccionado">
                  <q-input
                    :model-value="stockSeleccionado.producto?.sku"
                    label="SKU"
                    outlined
                    dense
                    readonly
                  />
                </div>

                <div class="col-6" v-if="stockSeleccionado">
                  <q-input
                    :model-value="stockSeleccionado.bodega?.nombre_bodega"
                    label="Bodega"
                    outlined
                    dense
                    readonly
                  />
                </div>

                <div class="col-6">
                  <q-input
                    :model-value="stockSeleccionado?.stock_actual || 0"
                    label="Stock Actual"
                    outlined
                    dense
                    readonly
                    type="number"
                  />
                </div>

                <div class="col-6">
                  <q-input
                    v-model.number="formAjuste.nuevo_stock"
                    label="Nuevo Stock *"
                    outlined
                    dense
                    type="number"
                    step="0.01"
                    min="0"
                    :rules="[val => val >= 0 || 'Debe ser mayor o igual a 0']"
                  />
                </div>

                <div class="col-12">
                  <q-select
                    v-model="formAjuste.tipo_ajuste"
                    :options="tiposAjusteOptions"
                    label="Tipo de Ajuste *"
                    outlined
                    dense
                    emit-value
                    map-options
                    :rules="[val => !!val || 'Tipo de ajuste es requerido']"
                  />
                </div>

                <div class="col-12">
                  <q-input
                    v-model="formAjuste.motivo"
                    label="Motivo del Ajuste *"
                    outlined
                    dense
                    type="textarea"
                    rows="3"
                    :rules="[val => !!val || 'Motivo es requerido']"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar Ajuste"
              @click="guardarAjusteStock"
              :loading="guardandoAjuste"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Dialog para transferencia de stock -->
      <q-dialog v-model="mostrarTransferencia" persistent>
        <q-card style="min-width: 600px">
          <q-card-section class="row items-center">
            <div class="text-h6">Transferir Stock</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarTransferencia">
              <div class="row q-gutter-md">
                <div class="col-6">
                  <q-input
                    :model-value="stockSeleccionado?.producto?.sku"
                    label="SKU"
                    outlined
                    dense
                    readonly
                  />
                </div>

                <div class="col-6">
                  <q-input
                    :model-value="stockSeleccionado?.bodega?.nombre_bodega"
                    label="Bodega Origen"
                    outlined
                    dense
                    readonly
                  />
                </div>

                <div class="col-6">
                  <q-input
                    :model-value="stockSeleccionado?.stock_actual || 0"
                    label="Stock Disponible"
                    outlined
                    dense
                    readonly
                    type="number"
                  />
                </div>

                <div class="col-6">
                  <q-select
                    v-model="formTransferencia.id_bodega_destino"
                    :options="bodegasDestinoOptions"
                    label="Bodega Destino *"
                    outlined
                    dense
                    emit-value
                    map-options
                    :rules="[val => !!val || 'Bodega destino es requerida']"
                  />
                </div>

                <div class="col-12">
                  <q-input
                    v-model.number="formTransferencia.cantidad"
                    label="Cantidad a Transferir *"
                    outlined
                    dense
                    type="number"
                    step="0.01"
                    min="0.01"
                    :max="stockSeleccionado?.stock_actual || 0"
                    :rules="[
                      val => val > 0 || 'Debe ser mayor a 0',
                      val => val <= (stockSeleccionado?.stock_actual || 0) || 'No puede exceder el stock disponible'
                    ]"
                  />
                </div>

                <div class="col-12">
                  <q-input
                    v-model="formTransferencia.motivo"
                    label="Motivo de la Transferencia *"
                    outlined
                    dense
                    type="textarea"
                    rows="3"
                    :rules="[val => !!val || 'Motivo es requerido']"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Transferir"
              @click="guardarTransferencia"
              :loading="guardandoTransferencia"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Dialog para historial de movimientos -->
      <q-dialog v-model="mostrarHistorial" persistent>
        <q-card style="min-width: 1000px; max-width: 1200px; max-height: 80vh">
          <q-card-section class="row items-center">
            <div class="text-h6">
              Historial de Movimientos - {{ stockSeleccionado?.producto?.sku }}
            </div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section style="max-height: 60vh; overflow-y: auto;">
            <q-table
              :rows="historialMovimientos"
              :columns="columnsHistorial"
              :loading="cargandoHistorial"
              row-key="id_movimiento"
              flat
              bordered
              dense
              :hide-bottom="historialMovimientos.length === 0"
            >
              <template v-slot:body-cell-tipo_movimiento="props">
                <q-td :props="props">
                  <q-chip
                    :color="getTipoMovimientoColor(props.value)"
                    text-color="white"
                    size="sm"
                  >
                    {{ getTipoMovimientoLabel(props.value) }}
                  </q-chip>
                </q-td>
              </template>

              <template v-slot:body-cell-cantidad="props">
                <q-td :props="props">
                  <span :class="props.row.tipo_movimiento === 'SALIDA' ? 'text-red' : 'text-green'">
                    {{ props.row.tipo_movimiento === 'SALIDA' ? '-' : '+' }}{{ formatStock(props.value) }}
                  </span>
                </q-td>
              </template>

              <template v-slot:body-cell-fecha_movimiento="props">
                <q-td :props="props">
                  {{ formatDateTime(props.value) }}
                </q-td>
              </template>
            </q-table>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cerrar" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useQuasar } from 'quasar'
import { useStockStore, type StockItem, type MovimientoStock } from '@/stores/stock'

const $q = useQuasar()
const stockStore = useStockStore()

// Types locales adicionales si es necesario
type MovimientoHistorial = MovimientoStock

// Estado reactivo
const guardandoAjuste = ref(false)
const guardandoTransferencia = ref(false)
const cargandoHistorial = ref(false)
const mostrarAjusteStock = ref(false)
const mostrarTransferencia = ref(false)
const mostrarHistorial = ref(false)
const stockSeleccionado = ref<StockItem | null>(null)

// Tipos para opciones
interface BodegaOption {
  label: string
  value: number
}

interface CategoriaOption {
  label: string
  value: number
}

interface ProductoOption {
  label: string
  value: number
  sku: string
}

// Datos
const historialMovimientos = ref<MovimientoHistorial[]>([])
const bodegasOptions = ref<BodegaOption[]>([])
const categoriasOptions = ref<CategoriaOption[]>([])
const productosOptions = ref<ProductoOption[]>([])

// Computed con datos del store
const isLoading = computed(() => stockStore.isLoading)
const stockItems = computed(() => stockStore.stockItems)

// Filtros
const filtros = reactive({
  busqueda: '',
  bodega: null,
  categoria: null,
  estado_stock: null,
  solo_activos: true
})

// Paginación
const paginacion = ref({
  sortBy: 'producto.sku',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Formularios
const formAjuste = ref({
  id_producto: null as number | null,
  id_bodega: null as number | null,
  nuevo_stock: 0,
  tipo_ajuste: '',
  motivo: ''
})

const formTransferencia = ref({
  id_bodega_destino: null as number | null,
  cantidad: 0,
  motivo: ''
})

// Opciones
const estadosStockOptions = [
  { label: 'Stock Normal', value: 'normal' },
  { label: 'Stock Bajo', value: 'bajo' },
  { label: 'Sin Stock', value: 'sin_stock' },
  { label: 'Sobre Stock', value: 'sobre_stock' }
]

const tiposAjusteOptions = [
  { label: 'Inventario Físico', value: 'INVENTARIO_FISICO' },
  { label: 'Ajuste por Merma', value: 'MERMA' },
  { label: 'Ajuste por Daño', value: 'DANO' },
  { label: 'Corrección de Error', value: 'CORRECCION' },
  { label: 'Ajuste Manual', value: 'MANUAL' }
]

// Computed adicionales
const resumen = computed(() => {
  const items = stockItems.value
  const total = items.length
  const stockOk = items.filter(item =>
    (item.stock_actual || 0) >= item.punto_reorden
  ).length
  const stockBajo = items.filter(item =>
    (item.stock_actual || 0) > 0 && (item.stock_actual || 0) < item.punto_reorden
  ).length
  const sinStock = items.filter(item =>
    (item.stock_actual || 0) === 0
  ).length

  return {
    total_productos: total,
    productos_stock_ok: stockOk,
    productos_stock_bajo: stockBajo,
    productos_sin_stock: sinStock
  }
})

const bodegasDestinoOptions = computed(() => {
  if (!stockSeleccionado.value) return bodegasOptions.value

  return bodegasOptions.value.filter(bodega =>
    bodega.value !== stockSeleccionado.value?.id_bodega
  )
})

// Columnas de la tabla
const columnsStock = [
  {
    name: 'producto',
    label: 'Producto',
    align: 'left' as const,
    field: 'producto',
    sortable: true
  },
  {
    name: 'bodega',
    label: 'Bodega',
    align: 'left' as const,
    field: 'bodega',
    sortable: true
  },
  {
    name: 'ubicacion',
    label: 'Ubicación',
    align: 'center' as const,
    field: 'ubicacion_completa'
  },
  {
    name: 'stock_actual',
    label: 'Stock Actual',
    align: 'center' as const,
    field: 'stock_actual',
    sortable: true
  },
  {
    name: 'stock_minimo',
    label: 'Stock Mínimo',
    align: 'center' as const,
    field: 'stock_minimo',
    sortable: true
  },
  {
    name: 'punto_reorden',
    label: 'Punto Reorden',
    align: 'center' as const,
    field: 'punto_reorden',
    sortable: true
  },
  {
    name: 'costo_promedio',
    label: 'Costo Promedio',
    align: 'right' as const,
    field: 'costo_promedio',
    sortable: true
  },
  {
    name: 'valor_total',
    label: 'Valor Total',
    align: 'right' as const,
    field: 'valor_total'
  },
  {
    name: 'estado',
    label: 'Estado',
    align: 'center' as const,
    field: 'estado'
  },
  {
    name: 'ultima_actualizacion',
    label: 'Última Actualización',
    align: 'center' as const,
    field: 'fecha_ultima_actualizacion',
    sortable: true
  },
  {
    name: 'acciones',
    label: 'Acciones',
    align: 'center' as const,
    field: 'acciones'
  }
]

const columnsHistorial = [
  {
    name: 'fecha_movimiento',
    label: 'Fecha',
    align: 'center' as const,
    field: 'fecha_movimiento',
    sortable: true
  },
  {
    name: 'tipo_movimiento',
    label: 'Tipo',
    align: 'center' as const,
    field: 'tipo_movimiento'
  },
  {
    name: 'cantidad',
    label: 'Cantidad',
    align: 'right' as const,
    field: 'cantidad'
  },
  {
    name: 'stock_anterior',
    label: 'Stock Anterior',
    align: 'right' as const,
    field: 'stock_anterior'
  },
  {
    name: 'stock_nuevo',
    label: 'Stock Nuevo',
    align: 'right' as const,
    field: 'stock_nuevo'
  },
  {
    name: 'motivo',
    label: 'Motivo',
    align: 'left' as const,
    field: 'motivo'
  },
  {
    name: 'usuario',
    label: 'Usuario',
    align: 'left' as const,
    field: 'usuario'
  }
]

// Métodos
const cargarDatos = async () => {
  try {
    const params = {
      activo: filtros.solo_activos,
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    // Aplicar filtros
    if (filtros.busqueda) {
      await stockStore.buscarStock(filtros.busqueda, {
        ...params,
        bodega_id: filtros.bodega,
        categoria: filtros.categoria
      })
    } else if (filtros.bodega) {
      await stockStore.obtenerStockPorBodega(filtros.bodega, params)
    } else {
      await stockStore.obtenerStockConsolidado(params)
    }

    // Cargar opciones (esto podría venir de otros stores)
    await cargarOpciones()

  } catch (error) {
    console.error('Error cargando datos:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al cargar los datos de stock'
    })
  }
}

const cargarOpciones = async () => {
  // Simulación de carga de opciones - estas podrían venir de otros stores
  bodegasOptions.value = [
    { label: 'Bodega Principal', value: 1 },
    { label: 'Bodega Equipos', value: 2 },
    { label: 'Bodega Repuestos', value: 3 }
  ]

  categoriasOptions.value = [
    { label: 'Sprinklers', value: 1 },
    { label: 'Válvulas', value: 2 },
    { label: 'Bombas', value: 3 },
    { label: 'Tuberías', value: 4 }
  ]

  productosOptions.value = [
    { label: 'Sprinkler Estándar 15mm', value: 1, sku: 'SPRK-001' },
    { label: 'Válvula de Control 2"', value: 2, sku: 'VAL-002' },
    { label: 'Bomba Centrífuga 5HP', value: 3, sku: 'BOMB-003' }
  ]
}

const buscarStock = () => {
  // Implementar lógica de búsqueda
  cargarDatos()
}

const onRequestStock = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarDatos()
}

const abrirAjusteStock = () => {
  stockSeleccionado.value = null
  formAjuste.value = {
    id_producto: null,
    id_bodega: null,
    nuevo_stock: 0,
    tipo_ajuste: '',
    motivo: ''
  }
  mostrarAjusteStock.value = true
}

const ajustarStock = (stock: StockItem) => {
  stockSeleccionado.value = stock
  formAjuste.value = {
    id_producto: stock.id_producto,
    id_bodega: stock.id_bodega,
    nuevo_stock: stock.stock_actual || 0,
    tipo_ajuste: '',
    motivo: ''
  }
  mostrarAjusteStock.value = true
}

const guardarAjusteStock = async () => {
  try {
    guardandoAjuste.value = true

    const ajuste = {
      id_producto: formAjuste.value.id_producto!,
      id_bodega: formAjuste.value.id_bodega!,
      stock_anterior: stockSeleccionado.value?.stock_actual || 0,
      stock_nuevo: formAjuste.value.nuevo_stock,
      tipo_ajuste: formAjuste.value.tipo_ajuste,
      motivo: formAjuste.value.motivo
    }

    await stockStore.realizarAjusteStock(ajuste)

    $q.notify({
      type: 'positive',
      message: 'Ajuste de stock realizado correctamente'
    })

    mostrarAjusteStock.value = false
    await cargarDatos()

  } catch (error) {
    console.error('Error guardando ajuste:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al realizar el ajuste de stock'
    })
  } finally {
    guardandoAjuste.value = false
  }
}

const transferirStock = (stock: StockItem) => {
  stockSeleccionado.value = stock
  formTransferencia.value = {
    id_bodega_destino: null,
    cantidad: 0,
    motivo: ''
  }
  mostrarTransferencia.value = true
}

const guardarTransferencia = async () => {
  try {
    guardandoTransferencia.value = true

    const transferencia = {
      id_producto: stockSeleccionado.value!.id_producto,
      id_bodega_origen: stockSeleccionado.value!.id_bodega,
      id_bodega_destino: formTransferencia.value.id_bodega_destino!,
      cantidad: formTransferencia.value.cantidad,
      motivo: formTransferencia.value.motivo
    }

    await stockStore.realizarTransferenciaStock(transferencia)

    $q.notify({
      type: 'positive',
      message: 'Transferencia realizada correctamente'
    })

    mostrarTransferencia.value = false
    await cargarDatos()

  } catch (error) {
    console.error('Error en transferencia:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al realizar la transferencia'
    })
  } finally {
    guardandoTransferencia.value = false
  }
}

const verHistorialMovimientos = async (stock: StockItem) => {
  stockSeleccionado.value = stock
  mostrarHistorial.value = true

  try {
    cargandoHistorial.value = true

    const movimientos = await stockStore.obtenerHistorialMovimientos(
      stock.id_producto,
      stock.id_bodega,
      { limit: 50 }
    )

    historialMovimientos.value = movimientos

  } catch (error) {
    console.error('Error cargando historial:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al cargar el historial de movimientos'
    })
  } finally {
    cargandoHistorial.value = false
  }
}

const exportarStock = async () => {
  try {
    $q.notify({
      type: 'info',
      message: 'Preparando exportación...'
    })

    const params = {
      bodega_id: filtros.bodega,
      categoria: filtros.categoria,
      estado_stock: filtros.estado_stock
    }

    const blob = await stockStore.exportarStock('xlsx', params)

    // Crear enlace de descarga
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `stock_bodega_${new Date().toISOString().split('T')[0]}.xlsx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    $q.notify({
      type: 'positive',
      message: 'Stock exportado correctamente'
    })

  } catch (error) {
    console.error('Error exportando stock:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al exportar el stock'
    })
  }
}

const filtrarProductos = (val: string, update: any) => {
  update(() => {
    if (val === '') {
      productosOptions.value = [
        { label: 'Sprinkler Estándar 15mm', value: 1, sku: 'SPRK-001' },
        { label: 'Válvula de Control 2"', value: 2, sku: 'VAL-002' },
        { label: 'Bomba Centrífuga 5HP', value: 3, sku: 'BOMB-003' }
      ]
    } else {
      const needle = val.toLowerCase()
      productosOptions.value = [
        { label: 'Sprinkler Estándar 15mm', value: 1, sku: 'SPRK-001' },
        { label: 'Válvula de Control 2"', value: 2, sku: 'VAL-002' },
        { label: 'Bomba Centrífuga 5HP', value: 3, sku: 'BOMB-003' }
      ].filter(producto =>
        producto.label.toLowerCase().includes(needle) ||
        producto.sku.toLowerCase().includes(needle)
      )
    }
  })
}

// Funciones de utilidad
const formatStock = (value: number): string => {
  return new Intl.NumberFormat('es-CL', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  }).format(value || 0)
}

const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP'
  }).format(value || 0)
}

const formatDateTime = (date: string): string => {
  if (!date) return ''
  return new Date(date).toLocaleString('es-CL')
}

const getStockColor = (stock: StockItem): string => {
  const actual = stock.stock_actual || 0

  if (actual === 0) return 'red'
  if (actual < stock.punto_reorden) return 'orange'
  if (actual > stock.stock_maximo) return 'purple'
  return 'green'
}

const getEstadoStockColor = (stock: StockItem): string => {
  const actual = stock.stock_actual || 0

  if (actual === 0) return 'red'
  if (actual < stock.punto_reorden) return 'orange'
  if (actual > stock.stock_maximo) return 'purple'
  return 'green'
}

const getEstadoStockLabel = (stock: StockItem): string => {
  const actual = stock.stock_actual || 0

  if (actual === 0) return 'Sin Stock'
  if (actual < stock.punto_reorden) return 'Stock Bajo'
  if (actual > stock.stock_maximo) return 'Sobre Stock'
  return 'Normal'
}

const getTipoMovimientoColor = (tipo: string): string => {
  const colores: { [key: string]: string } = {
    'ENTRADA': 'green',
    'SALIDA': 'red',
    'TRANSFERENCIA': 'blue',
    'AJUSTE': 'orange'
  }
  return colores[tipo] || 'grey'
}

const getTipoMovimientoLabel = (tipo: string): string => {
  const labels: { [key: string]: string } = {
    'ENTRADA': 'Entrada',
    'SALIDA': 'Salida',
    'TRANSFERENCIA': 'Transferencia',
    'AJUSTE': 'Ajuste'
  }
  return labels[tipo] || tipo
}

// Lifecycle
onMounted(() => {
  cargarDatos()
})
</script>

<style scoped>
.q-table th {
  font-weight: bold;
}
</style>