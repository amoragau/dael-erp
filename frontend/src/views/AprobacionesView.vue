<template>
  <q-page class="bg-grey-1">
    <div class="q-pa-lg">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-xl">
        <div>
          <div class="row items-center q-mb-sm">
            <q-icon name="check_circle" size="32px" color="primary" class="q-mr-md" />
            <div>
              <h4 class="q-my-none text-h4 text-weight-light">Centro de <span class="text-weight-bold text-primary">Aprobaciones</span></h4>
              <p class="text-grey-6 q-mb-none text-body2">Aprobación de órdenes de compra pendientes</p>
            </div>
          </div>
        </div>
        <div class="column items-end">
          <div class="text-h6 text-primary text-weight-bold">{{ ordenesFiltradas.length }}</div>
          <div class="text-caption text-grey-6">Órdenes pendientes</div>
        </div>
      </div>

      <!-- Filters -->
      <q-card flat class="q-mb-lg shadow-light">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-weight-medium q-mb-md text-grey-8">
            <q-icon name="filter_list" class="q-mr-sm" />
            Filtros de búsqueda
          </div>
          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-3">
              <q-input
                v-model="filtros.busqueda"
                placeholder="Buscar por número de orden..."
                outlined
                clearable
                dense
              >
                <template v-slot:prepend>
                  <q-icon name="search" color="grey-5" />
                </template>
              </q-input>
            </div>
            <div class="col-12 col-md-3">
              <q-select
                v-model="filtros.proveedor"
                :options="proveedoresOptions"
                label="Proveedor"
                outlined
                clearable
                emit-value
                map-options
                dense
              />
            </div>
            <div class="col-12 col-md-2">
              <q-input
                v-model="filtros.fechaDesde"
                type="date"
                label="Fecha desde"
                outlined
                clearable
                dense
              />
            </div>
            <div class="col-12 col-md-2">
              <q-input
                v-model="filtros.fechaHasta"
                type="date"
                label="Fecha hasta"
                outlined
                clearable
                dense
              />
            </div>
            <div class="col-12 col-md-2 row q-gutter-sm justify-end items-center">
              <q-btn
                color="primary"
                icon="search"
                label="Buscar"
                @click="aplicarFiltros"
                unelevated
                no-caps
              />
              <q-btn
                color="grey-6"
                icon="clear"
                label="Limpiar"
                @click="limpiarFiltros"
                flat
                no-caps
              />
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Loading -->
      <div v-if="cargando" class="row justify-center q-my-lg">
        <q-spinner-dots color="primary" size="50px" />
      </div>

      <!-- Table -->
      <q-card v-else>
        <q-card-section class="q-pa-none">
          <q-table
            :rows="ordenesFiltradas"
            :columns="columnas"
            row-key="id_orden_compra"
            :pagination="{ rowsPerPage: 20 }"
            :loading="cargando"
            class="full-width"
          >
            <template v-slot:body-cell-numero_orden="props">
              <q-td :props="props">
                <div class="text-primary text-weight-medium">
                  {{ props.row.numero_orden }}
                </div>
              </q-td>
            </template>

            <template v-slot:body-cell-proveedor="props">
              <q-td :props="props">
                <div>
                  <div class="text-weight-medium">{{ getNombreProveedor(props.row.id_proveedor) }}</div>
                  <div class="text-caption text-grey-6">RUT: {{ getRutProveedor(props.row.id_proveedor) }}</div>
                </div>
              </q-td>
            </template>

            <template v-slot:body-cell-total="props">
              <q-td :props="props">
                <div class="text-weight-medium">
                  {{ formatearMoneda(props.row.total, props.row.moneda) }}
                </div>
              </q-td>
            </template>

            <template v-slot:body-cell-fecha_orden="props">
              <q-td :props="props">
                {{ formatearFecha(props.row.fecha_orden) }}
              </q-td>
            </template>

            <template v-slot:body-cell-estado="props">
              <q-td :props="props">
                <q-badge
                  :color="getEstadoColor(props.row.estado)"
                  :label="getNombreEstado(props.row.estado)"
                />
              </q-td>
            </template>

            <template v-slot:body-cell-acciones="props">
              <q-td :props="props">
                <div class="row no-wrap q-gutter-xs">
                  <q-btn
                    size="sm"
                    color="primary"
                    icon="visibility"
                    round
                    flat
                    @click="verDetalleOrden(props.row)"
                  >
                    <q-tooltip>Ver detalle</q-tooltip>
                  </q-btn>
                  <q-btn
                    size="sm"
                    color="positive"
                    icon="check"
                    round
                    flat
                    @click="aprobarOrden(props.row)"
                    :loading="aprobando === props.row.id_orden_compra"
                  >
                    <q-tooltip>Aprobar orden</q-tooltip>
                  </q-btn>
                  <q-btn
                    size="sm"
                    color="negative"
                    icon="close"
                    round
                    flat
                    @click="rechazarOrden(props.row)"
                    :loading="rechazando === props.row.id_orden_compra"
                  >
                    <q-tooltip>Rechazar orden</q-tooltip>
                  </q-btn>
                </div>
              </q-td>
            </template>
          </q-table>
        </q-card-section>
      </q-card>

      <!-- Dialog para ver detalle de la orden -->
      <q-dialog v-model="mostrarDetalle" persistent maximized>
        <q-card class="column">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Detalle Orden de Compra {{ ordenSeleccionada?.numero_orden }}</div>
            <q-space />
            <q-btn icon="close" flat round dense @click="cerrarDetalle" />
          </q-card-section>

          <q-card-section class="col">
            <div v-if="ordenSeleccionada" class="q-gutter-md">
              <!-- Información general -->
              <q-card flat bordered>
                <q-card-section>
                  <div class="text-h6 q-mb-md">Información General</div>
                  <div class="row q-gutter-md">
                    <div class="col-md-3 col-sm-6 col-xs-12">
                      <q-field label="Número de Orden" stack-label>
                        <template v-slot:control>
                          <div class="self-center full-width no-outline" tabindex="0">
                            {{ ordenSeleccionada.numero_orden }}
                          </div>
                        </template>
                      </q-field>
                    </div>
                    <div class="col-md-3 col-sm-6 col-xs-12">
                      <q-field label="Proveedor" stack-label>
                        <template v-slot:control>
                          <div class="self-center full-width no-outline" tabindex="0">
                            {{ getNombreProveedor(ordenSeleccionada.id_proveedor) }}
                          </div>
                        </template>
                      </q-field>
                    </div>
                    <div class="col-md-3 col-sm-6 col-xs-12">
                      <q-field label="Fecha de Orden" stack-label>
                        <template v-slot:control>
                          <div class="self-center full-width no-outline" tabindex="0">
                            {{ formatearFecha(ordenSeleccionada.fecha_orden) }}
                          </div>
                        </template>
                      </q-field>
                    </div>
                    <div class="col-md-3 col-sm-6 col-xs-12">
                      <q-field label="Estado" stack-label>
                        <template v-slot:control>
                          <div class="self-center full-width no-outline" tabindex="0">
                            <q-badge
                              :color="getEstadoColor(ordenSeleccionada.estado)"
                              :label="getNombreEstado(ordenSeleccionada.estado)"
                            />
                          </div>
                        </template>
                      </q-field>
                    </div>
                  </div>
                </q-card-section>
              </q-card>

              <!-- Productos -->
              <q-card flat bordered>
                <q-card-section>
                  <div class="text-h6 q-mb-md">Productos</div>
                  <q-table
                    :rows="ordenSeleccionada.detalles || []"
                    :columns="columnasDetalle"
                    row-key="id_detalle"
                    :pagination="{ rowsPerPage: 0 }"
                    hide-pagination
                  >
                    <template v-slot:body-cell-total="props">
                      <q-td :props="props">
                        {{ formatearMoneda(props.row.cantidad * props.row.precio_unitario, ordenSeleccionada.moneda) }}
                      </q-td>
                    </template>
                  </q-table>
                </q-card-section>
              </q-card>

              <!-- Totales -->
              <q-card flat bordered>
                <q-card-section>
                  <div class="text-h6 q-mb-md">Totales</div>
                  <div class="row q-gutter-md">
                    <div class="col">
                      <q-field label="Subtotal" stack-label>
                        <template v-slot:control>
                          <div class="self-center full-width no-outline text-weight-bold" tabindex="0">
                            {{ formatearMoneda(ordenSeleccionada.subtotal, ordenSeleccionada.moneda) }}
                          </div>
                        </template>
                      </q-field>
                    </div>
                    <div class="col">
                      <q-field label="Impuestos" stack-label>
                        <template v-slot:control>
                          <div class="self-center full-width no-outline text-weight-bold" tabindex="0">
                            {{ formatearMoneda(ordenSeleccionada.impuestos, ordenSeleccionada.moneda) }}
                          </div>
                        </template>
                      </q-field>
                    </div>
                    <div class="col">
                      <q-field label="Total" stack-label>
                        <template v-slot:control>
                          <div class="self-center full-width no-outline text-weight-bold text-primary text-h6" tabindex="0">
                            {{ formatearMoneda(ordenSeleccionada.total, ordenSeleccionada.moneda) }}
                          </div>
                        </template>
                      </q-field>
                    </div>
                  </div>
                </q-card-section>
              </q-card>
            </div>
          </q-card-section>

          <q-card-actions align="right" class="q-pa-md">
            <q-btn
              color="negative"
              icon="close"
              label="Rechazar"
              @click="rechazarOrden(ordenSeleccionada)"
              :loading="rechazando === ordenSeleccionada?.id_orden_compra"
            />
            <q-btn
              color="positive"
              icon="check"
              label="Aprobar"
              @click="aprobarOrden(ordenSeleccionada)"
              :loading="aprobando === ordenSeleccionada?.id_orden_compra"
            />
            <q-btn
              color="grey"
              label="Cerrar"
              @click="cerrarDetalle"
              flat
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Dialog de confirmación para rechazo -->
      <q-dialog v-model="mostrarDialogoRechazo" persistent>
        <q-card style="min-width: 400px">
          <q-card-section>
            <div class="text-h6">Rechazar Orden de Compra</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <div class="q-mb-md">
              ¿Está seguro que desea rechazar la orden de compra
              <strong>{{ ordenParaRechazar?.numero_orden }}</strong>?
            </div>
            <q-input
              v-model="motivoRechazo"
              label="Motivo del rechazo"
              type="textarea"
              rows="3"
              outlined
              autofocus
              :rules="[val => !!val || 'El motivo es obligatorio']"
            />
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" @click="cancelarRechazo" />
            <q-btn
              color="negative"
              label="Rechazar"
              @click="confirmarRechazo"
              :disable="!motivoRechazo"
              :loading="rechazando === ordenParaRechazar?.id_orden_compra"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useOrdenCompraStore } from '../stores/ordenesCompra'
import { useProveedorStore } from '../stores/proveedores'
import { useLogStore } from '../stores/logs'
import { useAuthStore } from '../stores/auth'
import type { OrdenCompra } from '../stores/ordenesCompra'
import { formatCurrency } from '@/utils/formatters'

const $q = useQuasar()
const ordenCompraStore = useOrdenCompraStore()
const proveedorStore = useProveedorStore()
const logStore = useLogStore()
const authStore = useAuthStore()

// Estados reactivos
const cargando = ref(false)
const aprobando = ref<number | null>(null)
const rechazando = ref<number | null>(null)
const mostrarDetalle = ref(false)
const mostrarDialogoRechazo = ref(false)
const ordenSeleccionada = ref<OrdenCompra | null>(null)
const ordenParaRechazar = ref<OrdenCompra | null>(null)
const motivoRechazo = ref('')

// Filtros
const filtros = ref({
  busqueda: '',
  proveedor: null as number | null,
  fechaDesde: '',
  fechaHasta: ''
})

// Columnas de la tabla principal
const columnas = [
  {
    name: 'numero_orden',
    label: 'Número de Orden',
    align: 'left' as const,
    field: 'numero_orden',
    sortable: true
  },
  {
    name: 'proveedor',
    label: 'Proveedor',
    align: 'left' as const,
    field: 'id_proveedor'
  },
  {
    name: 'fecha_orden',
    label: 'Fecha',
    align: 'center' as const,
    field: 'fecha_orden',
    sortable: true
  },
  {
    name: 'total',
    label: 'Total',
    align: 'right' as const,
    field: 'total',
    sortable: true
  },
  {
    name: 'estado',
    label: 'Estado',
    align: 'center' as const,
    field: 'estado'
  },
  {
    name: 'acciones',
    label: 'Acciones',
    align: 'center' as const,
    field: 'acciones'
  }
]

// Columnas para el detalle de productos
const columnasDetalle = [
  {
    name: 'sku',
    label: 'SKU',
    align: 'left' as const,
    field: 'sku'
  },
  {
    name: 'nombre_producto',
    label: 'Producto',
    align: 'left' as const,
    field: 'nombre_producto'
  },
  {
    name: 'cantidad',
    label: 'Cantidad',
    align: 'center' as const,
    field: 'cantidad'
  },
  {
    name: 'precio_unitario',
    label: 'Precio Unit.',
    align: 'right' as const,
    field: 'precio_unitario'
  },
  {
    name: 'total',
    label: 'Total',
    align: 'right' as const,
    field: (row: any) => row.cantidad * row.precio_unitario
  }
]

// Computed
const ordenesFiltradas = computed(() => {
  // Solo mostrar órdenes en estado CREADA (pendientes de aprobación)
  let resultado = ordenCompraStore.ordenesCompra.filter(orden => {
    // Si el estado es un objeto con codigo_estado, comparar directamente
    if (orden.estado && typeof orden.estado === 'object' && 'codigo_estado' in orden.estado) {
      return orden.estado.codigo_estado === 'CREADA'
    }
    // Si el estado es un string, comparar directamente
    if (typeof orden.estado === 'string') {
      return orden.estado === 'CREADA'
    }
    return false
  })

  // Aplicar filtros
  if (filtros.value.busqueda && filtros.value.busqueda.trim()) {
    const busqueda = filtros.value.busqueda.toLowerCase().trim()
    resultado = resultado.filter(orden =>
      orden.numero_orden.toLowerCase().includes(busqueda)
    )
  }

  if (filtros.value.proveedor) {
    resultado = resultado.filter(orden => orden.id_proveedor === filtros.value.proveedor)
  }

  if (filtros.value.fechaDesde) {
    resultado = resultado.filter(orden => orden.fecha_orden >= filtros.value.fechaDesde)
  }

  if (filtros.value.fechaHasta) {
    resultado = resultado.filter(orden => orden.fecha_orden <= filtros.value.fechaHasta)
  }

  return resultado.sort((a, b) => new Date(b.fecha_orden).getTime() - new Date(a.fecha_orden).getTime())
})

const proveedoresOptions = computed(() => {
  return proveedorStore.proveedores.map(proveedor => ({
    label: `${proveedor.codigo_proveedor} - ${proveedor.nombre_proveedor}`,
    value: proveedor.id_proveedor
  }))
})

// Métodos
const cargarDatos = async () => {
  try {
    cargando.value = true
    await Promise.all([
      ordenCompraStore.obtenerOrdenesCompra(),
      ordenCompraStore.obtenerEstadosOrdenCompra(),
      proveedorStore.obtenerProveedores({ activo: true })
    ])
  } catch (error) {
    console.error('Error cargando datos:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al cargar los datos'
    })
  } finally {
    cargando.value = false
  }
}

const aplicarFiltros = () => {
  // Los filtros se aplican automáticamente por el computed
}

const limpiarFiltros = () => {
  filtros.value = {
    busqueda: '',
    proveedor: null,
    fechaDesde: '',
    fechaHasta: ''
  }
}

const verDetalleOrden = (orden: OrdenCompra) => {
  ordenSeleccionada.value = orden
  mostrarDetalle.value = true
}

const cerrarDetalle = () => {
  mostrarDetalle.value = false
  ordenSeleccionada.value = null
}

const aprobarOrden = async (orden: OrdenCompra | null) => {
  if (!orden) return

  try {
    aprobando.value = orden.id_orden_compra

    const usuarioId = authStore.user?.id_usuario || 1

    // Aprobar la orden
    await ordenCompraStore.aprobarOrdenCompra(orden.id_orden_compra, usuarioId)

    // Registrar log de aprobación (opcional - no bloquear si falla)
    try {
      await logStore.logAprobacion(orden.id_orden_compra, usuarioId, 'Orden aprobada desde módulo de aprobaciones')
    } catch (logError) {
      console.warn('No se pudo registrar el log de aprobación:', logError)
    }

    $q.notify({
      type: 'positive',
      message: `Orden ${orden.numero_orden} aprobada exitosamente`
    })

    await cargarDatos()

    if (mostrarDetalle.value) {
      cerrarDetalle()
    }
  } catch (error) {
    console.error('Error aprobando orden:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al aprobar la orden de compra'
    })
  } finally {
    aprobando.value = null
  }
}

const rechazarOrden = (orden: OrdenCompra | null) => {
  if (!orden) return

  ordenParaRechazar.value = orden
  motivoRechazo.value = ''
  mostrarDialogoRechazo.value = true
}

const cancelarRechazo = () => {
  mostrarDialogoRechazo.value = false
  ordenParaRechazar.value = null
  motivoRechazo.value = ''
}

const confirmarRechazo = async () => {
  if (!ordenParaRechazar.value || !motivoRechazo.value) return

  try {
    rechazando.value = ordenParaRechazar.value.id_orden_compra

    const usuarioId = authStore.user?.id_usuario || 1

    // Rechazar la orden con el motivo
    await ordenCompraStore.rechazarOrdenCompra(ordenParaRechazar.value.id_orden_compra, motivoRechazo.value)

    // Registrar log de rechazo (opcional - no bloquear si falla)
    try {
      await logStore.logRechazo(ordenParaRechazar.value.id_orden_compra, usuarioId, motivoRechazo.value)
    } catch (logError) {
      console.warn('No se pudo registrar el log de rechazo:', logError)
    }

    $q.notify({
      type: 'positive',
      message: `Orden ${ordenParaRechazar.value.numero_orden} rechazada exitosamente`
    })

    await cargarDatos()

    if (mostrarDetalle.value) {
      cerrarDetalle()
    }

    cancelarRechazo()
  } catch (error) {
    console.error('Error rechazando orden:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al rechazar la orden de compra'
    })
  } finally {
    rechazando.value = null
  }
}

// Helpers
const getNombreProveedor = (idProveedor: number): string => {
  const proveedor = proveedorStore.proveedores.find(p => p.id_proveedor === idProveedor)
  return proveedor ? proveedor.nombre_proveedor : '-'
}

const getRutProveedor = (idProveedor: number): string => {
  const proveedor = proveedorStore.proveedores.find(p => p.id_proveedor === idProveedor)
  return proveedor ? (proveedor.rfc || '-') : '-'
}

const formatearFecha = (fecha: string): string => {
  if (!fecha) return '-'
  return new Date(fecha).toLocaleDateString('es-CL')
}

const formatearMoneda = (cantidad: number, moneda: string = 'CLP'): string => {
  // Usar el formatter centralizado para formato chileno
  return formatCurrency(cantidad)
}

const getCodigoEstado = (estadoOrden: any): string => {
  // Si el estado es un objeto con codigo_estado
  if (estadoOrden && typeof estadoOrden === 'object' && 'codigo_estado' in estadoOrden) {
    return estadoOrden.codigo_estado
  }
  // Si el estado es un string
  if (typeof estadoOrden === 'string') {
    return estadoOrden
  }
  // Si no tenemos estado, retornar vacío
  return ''
}

const getNombreEstado = (estadoOrden: any): string => {
  // Si el estado es un objeto con nombre_estado
  if (estadoOrden && typeof estadoOrden === 'object' && 'nombre_estado' in estadoOrden) {
    return estadoOrden.nombre_estado
  }
  // Si el estado es un string o código, retornar tal cual
  if (typeof estadoOrden === 'string') {
    return estadoOrden
  }
  // Si no tenemos estado, retornar '-'
  return '-'
}

const getEstadoColor = (estadoOrden: any): string => {
  const codigo = getCodigoEstado(estadoOrden)
  const colores: { [key: string]: string } = {
    'CREADA': 'grey',
    'APROBADA': 'blue',
    'RECHAZADA': 'negative',
    'ENVIADA': 'purple',
    'RECIBIDA': 'green',
    'FACTURADA': 'teal',
    'CONCILIADA': 'indigo',
    'PAGADA': 'positive',
    'CERRADA': 'dark',
    'CANCELADA': 'negative'
  }
  return colores[codigo] || 'grey'
}

// Lifecycle
onMounted(() => {
  cargarDatos()
})
</script>