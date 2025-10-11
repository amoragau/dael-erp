<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Ajustes de Inventario</h4>
          <p class="text-grey-7 q-mb-none">Registro y control de ajustes de stock por diferencias e inventarios</p>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nuevo Ajuste"
          @click="abrirFormularioAjuste"
        />
      </div>

      <!-- Stats Cards -->
      <div class="row q-gutter-md q-mb-md" v-if="estadisticas">
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-primary">{{ estadisticas.total_ajustes }}</div>
              <div class="text-caption">Total Ajustes</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-warning">{{ estadisticas.pendientes }}</div>
              <div class="text-caption">Pendientes</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-positive">{{ estadisticas.procesados }}</div>
              <div class="text-caption">Procesados</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-3">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-info">{{ estadisticas.ajustes_positivos }}</div>
              <div class="text-caption">Ajustes Positivos</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-negative">{{ estadisticas.ajustes_negativos }}</div>
              <div class="text-caption">Ajustes Negativos</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-gutter-md items-center">
            <q-input
              v-model="filtros.busqueda"
              placeholder="Buscar por número, motivo..."
              outlined
              dense
              clearable
              style="min-width: 250px"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
            <q-select
              v-model="filtros.estado"
              :options="estadoOptions"
              label="Estado"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 150px"
            />
            <q-select
              v-model="filtros.tipo_ajuste"
              :options="tipoAjusteOptions"
              label="Tipo Ajuste"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 150px"
            />
            <q-select
              v-model="filtros.id_bodega"
              :options="bodegasOptions"
              label="Bodega"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 180px"
            />
            <q-input
              v-model="filtros.fecha_desde"
              label="Desde"
              outlined
              dense
              type="date"
              style="min-width: 150px"
            />
            <q-input
              v-model="filtros.fecha_hasta"
              label="Hasta"
              outlined
              dense
              type="date"
              style="min-width: 150px"
            />
            <q-btn
              color="primary"
              icon="search"
              label="Filtrar"
              @click="aplicarFiltros"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Adjustments Table -->
      <q-table
        :rows="ajustes"
        :columns="columnsAjustes"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_ajuste"
        flat
        bordered
        @request="onRequestAjustes"
      >
        <template v-slot:body-cell-numero_ajuste="props">
          <q-td :props="props">
            <div class="text-weight-medium">{{ props.value }}</div>
          </q-td>
        </template>

        <template v-slot:body-cell-tipo_ajuste="props">
          <q-td :props="props">
            <q-badge
              :color="getTipoAjusteColor(props.value)"
              :label="getTipoAjusteLabel(props.value)"
              :icon="getTipoAjusteIcon(props.value)"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-estado="props">
          <q-td :props="props">
            <q-badge
              :color="getEstadoColor(props.value)"
              :label="getEstadoLabel(props.value)"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-bodega="props">
          <q-td :props="props">
            {{ getBodegaNombre(props.row.id_bodega) }}
          </q-td>
        </template>

        <template v-slot:body-cell-valor_total="props">
          <q-td :props="props">
            <div class="text-right text-weight-medium">
              <span :class="props.value > 0 ? 'text-positive' : 'text-negative'">
                ${{ Number(Math.abs(props.value)).toLocaleString() }}
              </span>
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-cantidad_productos="props">
          <q-td :props="props">
            <div class="text-center">{{ props.value }}</div>
          </q-td>
        </template>

        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn
              flat
              round
              icon="visibility"
              color="info"
              size="sm"
              @click="verDetalleAjuste(props.row)"
            >
              <q-tooltip>Ver Detalles</q-tooltip>
            </q-btn>
            <q-btn
              v-if="props.row.estado === 'pendiente'"
              flat
              round
              icon="edit"
              color="primary"
              size="sm"
              @click="editarAjuste(props.row)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              v-if="props.row.estado === 'pendiente'"
              flat
              round
              icon="check"
              color="positive"
              size="sm"
              @click="procesarAjuste(props.row)"
            >
              <q-tooltip>Procesar</q-tooltip>
            </q-btn>
            <q-btn
              v-if="props.row.estado === 'pendiente'"
              flat
              round
              icon="cancel"
              color="negative"
              size="sm"
              @click="cancelarAjuste(props.row)"
            >
              <q-tooltip>Cancelar</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Adjustment Dialog -->
      <q-dialog v-model="showCreateAjusteDialog" persistent>
        <q-card style="min-width: 1200px; max-width: 1400px; max-height: 90vh">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">{{ editandoAjuste ? 'Editar' : 'Nuevo' }} Ajuste de Inventario</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section class="q-pt-none" style="max-height: calc(90vh - 120px);">
            <q-form @submit="guardarAjuste">
              <div class="row" style="height: calc(90vh - 160px);">
                <div class="col-3">
                  <q-tabs
                    v-model="tabActivo"
                    vertical
                    class="text-primary full-height"
                  >
                    <q-tab name="general" icon="description" label="Información General" />
                    <q-tab name="productos" icon="list" label="Productos a Ajustar" />
                    <q-tab name="auditoria" icon="history" label="Auditoría" />
                  </q-tabs>
                </div>
                <div class="col-9">
                  <q-tab-panels
                    v-model="tabActivo"
                    animated
                    class="full-height"
                    style="overflow-y: auto;"
                  >
                    <!-- Panel Información General -->
                    <q-tab-panel name="general">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="description" class="q-mr-sm" />
                        Información General del Ajuste
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-4">
                          <q-select
                            v-model="formAjuste.tipo_ajuste"
                            :options="tipoAjusteOptions"
                            label="Tipo de Ajuste *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'El tipo de ajuste es requerido']"
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-select
                            v-model="formAjuste.id_bodega"
                            :options="bodegasOptions"
                            label="Bodega *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'La bodega es requerida']"
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model="formAjuste.fecha_ajuste"
                            label="Fecha Ajuste *"
                            outlined
                            dense
                            type="date"
                            :rules="[val => !!val || 'La fecha es requerida']"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12">
                          <q-input
                            v-model="formAjuste.motivo"
                            label="Motivo del Ajuste *"
                            outlined
                            dense
                            :rules="[val => !!val || 'El motivo es requerido']"
                            hint="Explique la razón del ajuste"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formAjuste.observaciones"
                            label="Observaciones"
                            outlined
                            type="textarea"
                            rows="3"
                            hint="Comentarios adicionales sobre el ajuste"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formAjuste.numero_documento_referencia"
                            label="Número Documento Referencia"
                            outlined
                            dense
                            hint="Documento que justifica el ajuste"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formAjuste.fecha_documento_referencia"
                            label="Fecha Documento"
                            outlined
                            dense
                            type="date"
                          />
                        </div>
                      </div>

                      <q-banner v-if="tipoAjusteSeleccionado" class="bg-info text-white q-mt-md">
                        <q-icon name="info" class="q-mr-sm" />
                        {{ getTipoAjusteDescripcion(formAjuste.tipo_ajuste) }}
                      </q-banner>
                    </q-tab-panel>

                    <!-- Panel Productos -->
                    <q-tab-panel name="productos">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="list" class="q-mr-sm" />
                        Productos a Ajustar
                      </div>

                      <div class="row items-center justify-between q-mb-md">
                        <div class="text-subtitle2">Detalle de Productos</div>
                        <q-btn
                          color="primary"
                          icon="add"
                          label="Agregar Producto"
                          size="sm"
                          @click="abrirFormularioDetalleAjuste"
                        />
                      </div>

                      <q-table
                        :rows="detallesAjuste"
                        :columns="columnsDetalles"
                        :loading="isLoadingDetalles"
                        row-key="id_detalle"
                        flat
                        bordered
                        dense
                      >
                        <template v-slot:body-cell-producto="props">
                          <q-td :props="props">
                            <div class="text-weight-medium">{{ getProductoNombre(props.row.id_producto) }}</div>
                            <div class="text-caption text-grey-6">{{ getProductoCodigo(props.row.id_producto) }}</div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-stock_actual="props">
                          <q-td :props="props">
                            <div class="text-center">{{ Number(props.value).toLocaleString() }}</div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-stock_ajustado="props">
                          <q-td :props="props">
                            <div class="text-center text-weight-medium">{{ Number(props.value).toLocaleString() }}</div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-diferencia="props">
                          <q-td :props="props">
                            <div class="text-center text-weight-medium" :class="props.value > 0 ? 'text-positive' : 'text-negative'">
                              {{ props.value > 0 ? '+' : '' }}{{ Number(props.value).toLocaleString() }}
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-costo_unitario="props">
                          <q-td :props="props">
                            <div class="text-right">${{ Number(props.value).toLocaleString() }}</div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-valor_ajuste="props">
                          <q-td :props="props">
                            <div class="text-right text-weight-medium" :class="props.value > 0 ? 'text-positive' : 'text-negative'">
                              {{ props.value > 0 ? '+' : '' }}${{ Number(Math.abs(props.value)).toLocaleString() }}
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-actions="props">
                          <q-td :props="props">
                            <q-btn
                              flat
                              round
                              icon="edit"
                              color="primary"
                              size="sm"
                              @click="editarDetalleAjuste(props.row)"
                            >
                              <q-tooltip>Editar</q-tooltip>
                            </q-btn>
                            <q-btn
                              flat
                              round
                              icon="delete"
                              color="negative"
                              size="sm"
                              @click="eliminarDetalleAjuste(props.row)"
                            >
                              <q-tooltip>Eliminar</q-tooltip>
                            </q-btn>
                          </q-td>
                        </template>
                      </q-table>

                      <div v-if="detallesAjuste.length > 0" class="q-mt-md">
                        <q-separator />
                        <div class="row justify-end q-mt-sm">
                          <div class="text-h6" :class="calcularTotalAjuste() > 0 ? 'text-positive' : 'text-negative'">
                            Total: {{ calcularTotalAjuste() > 0 ? '+' : '' }}${{ Math.abs(calcularTotalAjuste()).toLocaleString() }}
                          </div>
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Auditoría -->
                    <q-tab-panel name="auditoria">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="history" class="q-mr-sm" />
                        Información de Auditoría
                      </div>

                      <div v-if="formAjuste.id_ajuste">
                        <div class="row q-gutter-md">
                          <div class="col-12 col-md-6">
                            <q-list bordered separator>
                              <q-item-label header>Información de Creación</q-item-label>
                              <q-item>
                                <q-item-section>
                                  <q-item-label caption>Creado por</q-item-label>
                                  <q-item-label>{{ ajusteDetalle?.usuario_crea?.nombre || 'Usuario' }}</q-item-label>
                                </q-item-section>
                              </q-item>
                              <q-item>
                                <q-item-section>
                                  <q-item-label caption>Fecha de Creación</q-item-label>
                                  <q-item-label>{{ formatDateTime(ajusteDetalle?.fecha_creacion) }}</q-item-label>
                                </q-item-section>
                              </q-item>
                            </q-list>
                          </div>
                          <div class="col-12 col-md-6">
                            <q-list bordered separator>
                              <q-item-label header>Información de Procesamiento</q-item-label>
                              <q-item v-if="ajusteDetalle?.usuario_procesa">
                                <q-item-section>
                                  <q-item-label caption>Procesado por</q-item-label>
                                  <q-item-label>{{ ajusteDetalle.usuario_procesa.nombre }}</q-item-label>
                                </q-item-section>
                              </q-item>
                              <q-item v-if="ajusteDetalle?.fecha_procesamiento">
                                <q-item-section>
                                  <q-item-label caption>Fecha de Procesamiento</q-item-label>
                                  <q-item-label>{{ formatDateTime(ajusteDetalle.fecha_procesamiento) }}</q-item-label>
                                </q-item-section>
                              </q-item>
                            </q-list>
                          </div>
                        </div>
                      </div>

                      <div v-else class="text-grey-6">
                        <q-icon name="info" class="q-mr-sm" />
                        Guarde el ajuste primero para ver la información de auditoría
                      </div>
                    </q-tab-panel>
                  </q-tab-panels>
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right" class="q-pa-md">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar Ajuste"
              @click="guardarAjuste"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Adjustment Detail Dialog -->
      <q-dialog v-model="showDetalleDialog" persistent>
        <q-card style="min-width: 900px; max-width: 1100px">
          <q-card-section class="row items-center">
            <div class="text-h6">Detalle del Ajuste</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section v-if="ajusteDetalle">
            <div class="row q-col-gutter-md">
              <!-- Información General -->
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Información General</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Número</q-item-label>
                      <q-item-label>{{ ajusteDetalle.numero_ajuste }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Tipo</q-item-label>
                      <q-item-label>
                        <q-badge
                          :color="getTipoAjusteColor(ajusteDetalle.tipo_ajuste)"
                          :label="getTipoAjusteLabel(ajusteDetalle.tipo_ajuste)"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Estado</q-item-label>
                      <q-item-label>
                        <q-badge
                          :color="getEstadoColor(ajusteDetalle.estado)"
                          :label="getEstadoLabel(ajusteDetalle.estado)"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Bodega</q-item-label>
                      <q-item-label>{{ getBodegaNombre(ajusteDetalle.id_bodega) }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Fecha</q-item-label>
                      <q-item-label>{{ formatDate(ajusteDetalle.fecha_ajuste) }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>

              <!-- Valores -->
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Valores</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Productos Ajustados</q-item-label>
                      <q-item-label>{{ ajusteDetalle.cantidad_productos }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Valor Total</q-item-label>
                      <q-item-label class="text-weight-medium" :class="ajusteDetalle.valor_total > 0 ? 'text-positive' : 'text-negative'">
                        {{ ajusteDetalle.valor_total > 0 ? '+' : '' }}${{ Math.abs(Number(ajusteDetalle.valor_total)).toLocaleString() }}
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Motivo</q-item-label>
                      <q-item-label>{{ ajusteDetalle.motivo }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item v-if="ajusteDetalle.observaciones">
                    <q-item-section>
                      <q-item-label caption>Observaciones</q-item-label>
                      <q-item-label>{{ ajusteDetalle.observaciones }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>

              <!-- Productos -->
              <div class="col-12">
                <q-expansion-item
                  icon="list"
                  label="Productos Ajustados"
                  class="q-mt-md"
                >
                  <q-card flat bordered>
                    <q-card-section>
                      <q-table
                        :rows="ajusteDetalle.detalles || []"
                        :columns="columnsDetallesView"
                        row-key="id_detalle"
                        flat
                        dense
                      />
                    </q-card-section>
                  </q-card>
                </q-expansion-item>
              </div>
            </div>
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
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// Types
interface AjusteInventario {
  id_ajuste: number
  numero_ajuste: string
  tipo_ajuste: string
  id_bodega: number
  fecha_ajuste: string
  motivo: string
  observaciones?: string
  numero_documento_referencia?: string
  fecha_documento_referencia?: string
  estado: string
  cantidad_productos: number
  valor_total: number
  fecha_creacion: string
  usuario_crea?: { nombre: string }
  fecha_procesamiento?: string
  usuario_procesa?: { nombre: string }
  detalles?: DetalleAjuste[]
}

interface AjusteInventarioCreate {
  tipo_ajuste: string
  id_bodega: number
  fecha_ajuste: string
  motivo: string
  observaciones?: string
  numero_documento_referencia?: string
  fecha_documento_referencia?: string
  activo: boolean
}

interface DetalleAjuste {
  id_detalle?: number
  id_ajuste?: number
  id_producto: number
  stock_actual: number
  stock_ajustado: number
  diferencia: number
  costo_unitario: number
  valor_ajuste: number
  motivo_detalle?: string
}

// Reactive data
const ajustes = ref<AjusteInventario[]>([])
const detallesAjuste = ref<DetalleAjuste[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const isLoadingDetalles = ref(false)
const showCreateAjusteDialog = ref(false)
const showDetalleDialog = ref(false)
const editandoAjuste = ref(false)
const ajusteDetalle = ref<AjusteInventario | null>(null)
const estadisticas = ref<any>(null)
const tabActivo = ref('general')

// Filters
const filtros = ref({
  busqueda: '',
  estado: null as string | null,
  tipo_ajuste: null as string | null,
  id_bodega: null as number | null,
  fecha_desde: '',
  fecha_hasta: ''
})

// Options
const estadoOptions = [
  { label: 'Pendiente', value: 'pendiente' },
  { label: 'Procesado', value: 'procesado' },
  { label: 'Cancelado', value: 'cancelado' }
]

const tipoAjusteOptions = [
  { label: 'Positivo - Sobrante', value: 'positivo' },
  { label: 'Negativo - Faltante', value: 'negativo' },
  { label: 'Conteo Físico', value: 'conteo_fisico' },
  { label: 'Corrección Error', value: 'correccion_error' },
  { label: 'Merma', value: 'merma' },
  { label: 'Obsolescencia', value: 'obsolescencia' }
]

const bodegasOptions = ref([])

// Pagination
const paginacion = ref({
  sortBy: 'id_ajuste',
  descending: true,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formAjuste = ref<AjusteInventarioCreate & { id_ajuste?: number }>({
  tipo_ajuste: '',
  id_bodega: 0,
  fecha_ajuste: new Date().toISOString().split('T')[0],
  motivo: '',
  observaciones: '',
  numero_documento_referencia: '',
  fecha_documento_referencia: '',
  activo: true
})

// Computed
const tipoAjusteSeleccionado = computed(() => {
  return tipoAjusteOptions.find(tipo => tipo.value === formAjuste.value.tipo_ajuste)
})

// Table columns
const columnsAjustes = [
  {
    name: 'numero_ajuste',
    required: true,
    label: 'Número',
    align: 'left' as const,
    field: 'numero_ajuste',
    sortable: true
  },
  {
    name: 'tipo_ajuste',
    label: 'Tipo',
    align: 'center' as const,
    field: 'tipo_ajuste',
    sortable: true
  },
  {
    name: 'bodega',
    label: 'Bodega',
    align: 'left' as const,
    field: 'id_bodega',
    sortable: true
  },
  {
    name: 'fecha_ajuste',
    label: 'Fecha',
    align: 'center' as const,
    field: 'fecha_ajuste',
    sortable: true,
    format: (val: string) => formatDate(val)
  },
  {
    name: 'motivo',
    label: 'Motivo',
    align: 'left' as const,
    field: 'motivo'
  },
  {
    name: 'estado',
    label: 'Estado',
    align: 'center' as const,
    field: 'estado',
    sortable: true
  },
  {
    name: 'cantidad_productos',
    label: 'Productos',
    align: 'center' as const,
    field: 'cantidad_productos',
    sortable: true
  },
  {
    name: 'valor_total',
    label: 'Valor',
    align: 'right' as const,
    field: 'valor_total',
    sortable: true
  },
  {
    name: 'actions',
    label: 'Acciones',
    align: 'center' as const,
    field: 'actions'
  }
]

const columnsDetalles = [
  {
    name: 'producto',
    required: true,
    label: 'Producto',
    align: 'left' as const,
    field: 'id_producto'
  },
  {
    name: 'stock_actual',
    label: 'Stock Actual',
    align: 'center' as const,
    field: 'stock_actual'
  },
  {
    name: 'stock_ajustado',
    label: 'Stock Ajustado',
    align: 'center' as const,
    field: 'stock_ajustado'
  },
  {
    name: 'diferencia',
    label: 'Diferencia',
    align: 'center' as const,
    field: 'diferencia'
  },
  {
    name: 'costo_unitario',
    label: 'Costo Unit.',
    align: 'right' as const,
    field: 'costo_unitario'
  },
  {
    name: 'valor_ajuste',
    label: 'Valor Ajuste',
    align: 'right' as const,
    field: 'valor_ajuste'
  },
  {
    name: 'actions',
    label: 'Acciones',
    align: 'center' as const,
    field: 'actions'
  }
]

const columnsDetallesView = [
  {
    name: 'producto',
    required: true,
    label: 'Producto',
    align: 'left' as const,
    field: (row: DetalleAjuste) => getProductoNombre(row.id_producto)
  },
  {
    name: 'stock_actual',
    label: 'Stock Actual',
    align: 'center' as const,
    field: 'stock_actual',
    format: (val: number) => Number(val).toLocaleString()
  },
  {
    name: 'stock_ajustado',
    label: 'Stock Ajustado',
    align: 'center' as const,
    field: 'stock_ajustado',
    format: (val: number) => Number(val).toLocaleString()
  },
  {
    name: 'diferencia',
    label: 'Diferencia',
    align: 'center' as const,
    field: 'diferencia',
    format: (val: number) => `${val > 0 ? '+' : ''}${Number(val).toLocaleString()}`
  },
  {
    name: 'valor_ajuste',
    label: 'Valor Ajuste',
    align: 'right' as const,
    field: 'valor_ajuste',
    format: (val: number) => `${val > 0 ? '+' : ''}$${Math.abs(Number(val)).toLocaleString()}`
  }
]

// Methods
const onRequestAjustes = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarAjustes()
}

const cargarAjustes = async () => {
  try {
    isLoading.value = true
    // TODO: Implement API call
    ajustes.value = []
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar ajustes',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const cargarEstadisticas = async () => {
  try {
    // TODO: Implement API call
    estadisticas.value = {
      total_ajustes: 0,
      pendientes: 0,
      procesados: 0,
      ajustes_positivos: 0,
      ajustes_negativos: 0
    }
  } catch (error: any) {
    console.error('Error al cargar estadísticas:', error)
  }
}

const aplicarFiltros = async () => {
  paginacion.value.page = 1
  await cargarAjustes()
  await cargarEstadisticas()
}

const abrirFormularioAjuste = () => {
  resetFormAjuste()
  showCreateAjusteDialog.value = true
}

const editarAjuste = (ajuste: AjusteInventario) => {
  editandoAjuste.value = true
  formAjuste.value = { ...ajuste }
  showCreateAjusteDialog.value = true
}

const guardarAjuste = async () => {
  try {
    isGuardando.value = true

    if (editandoAjuste.value && formAjuste.value.id_ajuste) {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Ajuste actualizado correctamente'
      })
    } else {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Ajuste creado correctamente'
      })
    }

    showCreateAjusteDialog.value = false
    resetFormAjuste()
    await cargarAjustes()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar ajuste',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const verDetalleAjuste = async (ajuste: AjusteInventario) => {
  try {
    // TODO: Implement API call
    ajusteDetalle.value = ajuste
    showDetalleDialog.value = true
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar detalles del ajuste',
      caption: error.message
    })
  }
}

const procesarAjuste = async (ajuste: AjusteInventario) => {
  $q.dialog({
    title: 'Procesar Ajuste',
    message: `¿Está seguro de procesar el ajuste ${ajuste.numero_ajuste}? Esta acción afectará el inventario y no se puede deshacer.`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Ajuste procesado correctamente'
      })
      await cargarAjustes()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al procesar ajuste',
        caption: error.message
      })
    }
  })
}

const cancelarAjuste = async (ajuste: AjusteInventario) => {
  $q.dialog({
    title: 'Cancelar Ajuste',
    message: `¿Está seguro de cancelar el ajuste ${ajuste.numero_ajuste}?`,
    prompt: {
      model: '',
      type: 'text',
      label: 'Motivo de cancelación *',
      isValid: val => !!val
    },
    cancel: true,
    persistent: true
  }).onOk(async (motivo) => {
    try {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Ajuste cancelado correctamente'
      })
      await cargarAjustes()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al cancelar ajuste',
        caption: error.message
      })
    }
  })
}

const resetFormAjuste = () => {
  editandoAjuste.value = false
  tabActivo.value = 'general'
  formAjuste.value = {
    tipo_ajuste: '',
    id_bodega: 0,
    fecha_ajuste: new Date().toISOString().split('T')[0],
    motivo: '',
    observaciones: '',
    numero_documento_referencia: '',
    fecha_documento_referencia: '',
    activo: true
  }
  detallesAjuste.value = []
}

const abrirFormularioDetalleAjuste = () => {
  // TODO: Implement detail form
}

const editarDetalleAjuste = (detalle: DetalleAjuste) => {
  // TODO: Implement detail editing
}

const eliminarDetalleAjuste = (detalle: DetalleAjuste) => {
  // TODO: Implement detail deletion
}

const calcularTotalAjuste = (): number => {
  return detallesAjuste.value.reduce((total, detalle) => total + detalle.valor_ajuste, 0)
}

// Helper methods
const getTipoAjusteColor = (tipo: string): string => {
  const colorMap: { [key: string]: string } = {
    'positivo': 'positive',
    'negativo': 'negative',
    'conteo_fisico': 'info',
    'correccion_error': 'warning',
    'merma': 'deep-orange',
    'obsolescencia': 'brown'
  }

  return colorMap[tipo] || 'grey'
}

const getTipoAjusteLabel = (tipo: string): string => {
  const labelMap: { [key: string]: string } = {
    'positivo': 'Positivo',
    'negativo': 'Negativo',
    'conteo_fisico': 'Conteo Físico',
    'correccion_error': 'Corrección Error',
    'merma': 'Merma',
    'obsolescencia': 'Obsolescencia'
  }

  return labelMap[tipo] || tipo
}

const getTipoAjusteIcon = (tipo: string): string => {
  const iconMap: { [key: string]: string } = {
    'positivo': 'add',
    'negativo': 'remove',
    'conteo_fisico': 'inventory',
    'correccion_error': 'build',
    'merma': 'trending_down',
    'obsolescencia': 'delete_forever'
  }

  return iconMap[tipo] || 'help'
}

const getTipoAjusteDescripcion = (tipo: string): string => {
  const descripcionMap: { [key: string]: string } = {
    'positivo': 'Ajuste por sobrante de inventario detectado',
    'negativo': 'Ajuste por faltante de inventario detectado',
    'conteo_fisico': 'Ajuste basado en conteo físico de inventario',
    'correccion_error': 'Corrección de errores en registros de inventario',
    'merma': 'Ajuste por merma o deterioro de productos',
    'obsolescencia': 'Ajuste por productos obsoletos o vencidos'
  }

  return descripcionMap[tipo] || ''
}

const getEstadoColor = (estado: string): string => {
  const colorMap: { [key: string]: string } = {
    'pendiente': 'warning',
    'procesado': 'positive',
    'cancelado': 'negative'
  }

  return colorMap[estado] || 'grey'
}

const getEstadoLabel = (estado: string): string => {
  const labelMap: { [key: string]: string } = {
    'pendiente': 'Pendiente',
    'procesado': 'Procesado',
    'cancelado': 'Cancelado'
  }

  return labelMap[estado] || estado
}

const getProductoNombre = (productoId: number): string => {
  // TODO: Get from products store
  return `Producto ${productoId}`
}

const getProductoCodigo = (productoId: number): string => {
  // TODO: Get from products store
  return `PRD-${productoId}`
}

const getBodegaNombre = (bodegaId: number): string => {
  // TODO: Get from bodegas store
  return `Bodega ${bodegaId}`
}

const formatDate = (dateString: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-CL')
}

const formatDateTime = (dateString?: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('es-CL')
}

// Lifecycle
onMounted(async () => {
  await cargarAjustes()
  await cargarEstadisticas()
})
</script>