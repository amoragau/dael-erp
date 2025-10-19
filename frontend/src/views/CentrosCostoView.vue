<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-xl">
        <div>
          <div class="row items-center q-mb-sm">
            <q-icon name="account_balance" size="32px" color="primary" class="q-mr-md" />
            <div>
              <h4 class="q-my-none text-h4 text-weight-light">Centros de <span class="text-weight-bold text-primary">Costo</span></h4>
              <p class="text-grey-6 q-mb-none text-body2">Gestión de centros de costo para asignación de gastos y control presupuestario</p>
            </div>
          </div>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nuevo Centro de Costo"
          @click="abrirFormularioCentroCosto"
          unelevated
          class="q-px-lg q-py-sm"
          no-caps
        />
      </div>

      <!-- Filters -->
      <q-card flat class="q-mb-lg shadow-light">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-weight-medium q-mb-md text-grey-8">
            <q-icon name="filter_list" class="q-mr-sm" />
            Filtros de búsqueda
          </div>
          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-5">
              <q-input
                v-model="filtros.busqueda"
                placeholder="Buscar por código o nombre..."
                outlined
                dense
                clearable
              >
                <template v-slot:prepend>
                  <q-icon name="search" color="grey-5" />
                </template>
              </q-input>
            </div>
            <div class="col-12 col-md-3">
              <q-select
                v-model="filtros.estado"
                :options="estadoOptions"
                label="Estado"
                outlined
                dense
                clearable
                emit-value
                map-options
              />
            </div>
            <div class="col-12 col-md-4 row q-gutter-sm justify-end items-center">
              <q-btn color="primary" icon="search" label="Buscar" @click="buscarCentrosCosto" unelevated no-caps />
              <q-btn color="grey-6" icon="clear" label="Limpiar" @click="limpiarFiltros" flat no-caps />
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Cost Centers Table -->
      <q-table
        :rows="centrosCosto"
        :columns="columnsCentrosCosto"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_centro_costo"
        flat
        bordered
        @request="onRequestCentrosCosto"
      >
        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'green' : 'red'"
              :label="props.value ? 'Activo' : 'Inactivo'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-presupuesto_anual="props">
          <q-td :props="props">
            <span v-if="props.value && props.value > 0" class="text-weight-medium">
              {{ formatCurrency(props.value) }}
            </span>
            <span v-else class="text-grey-5">Sin presupuesto</span>
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
              @click="verDetalleCentroCosto(props.row as CentroCosto)"
            >
              <q-tooltip>Ver Detalles</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="edit"
              color="primary"
              size="sm"
              @click="editarCentroCosto(props.row as CentroCosto)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'negative' : 'positive'"
              size="sm"
              @click="toggleEstadoCentroCosto(props.row as CentroCosto)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Centro de Costo Dialog -->
      <q-dialog v-model="showCreateDialog" persistent>
        <q-card style="min-width: 600px; max-width: 800px">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">{{ editando ? 'Editar' : 'Nuevo' }} Centro de Costo</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-form @submit="guardarCentroCosto">
              <div class="row q-gutter-md q-mt-md">
                <div class="col-12 col-md-5">
                  <q-input
                    v-model="formCentroCosto.codigo_centro_costo"
                    label="Código *"
                    outlined
                    dense
                    maxlength="20"
                    :rules="[val => !!val || 'El código es requerido']"
                    hint="Código único del centro de costo"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formCentroCosto.nombre_centro_costo"
                    label="Nombre *"
                    outlined
                    dense
                    maxlength="100"
                    :rules="[val => !!val || 'El nombre es requerido']"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formCentroCosto.descripcion"
                    label="Descripción"
                    outlined
                    dense
                    type="textarea"
                    rows="3"
                    hint="Descripción detallada del centro de costo"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-5">
                  <q-input
                    v-model.number="formCentroCosto.presupuesto_anual"
                    label="Presupuesto Anual"
                    outlined
                    dense
                    type="number"
                    step="0.01"
                    min="0"
                    prefix="$"
                    hint="Presupuesto asignado para el año"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-toggle
                    v-model="formCentroCosto.activo"
                    label="Centro de Costo Activo"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right" class="q-pa-md">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar"
              @click="guardarCentroCosto"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Centro de Costo Detail Dialog -->
      <q-dialog v-model="showDetalleDialog" persistent>
        <q-card style="min-width: 600px; max-width: 800px">
          <q-card-section class="row items-center">
            <div class="text-h6">Detalles del Centro de Costo</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section v-if="centroCostoDetalle">
            <div class="row q-col-gutter-md">
              <div class="col-12">
                <q-list bordered separator>
                  <q-item-label header>Información General</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Código</q-item-label>
                      <q-item-label>{{ centroCostoDetalle.codigo_centro_costo }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Nombre</q-item-label>
                      <q-item-label>{{ centroCostoDetalle.nombre_centro_costo }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item v-if="centroCostoDetalle.descripcion">
                    <q-item-section>
                      <q-item-label caption>Descripción</q-item-label>
                      <q-item-label>{{ centroCostoDetalle.descripcion }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Presupuesto Anual</q-item-label>
                      <q-item-label>
                        <span v-if="centroCostoDetalle.presupuesto_anual > 0" class="text-weight-medium">
                          {{ formatCurrency(centroCostoDetalle.presupuesto_anual) }}
                        </span>
                        <span v-else class="text-grey-5">Sin presupuesto asignado</span>
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Estado</q-item-label>
                      <q-item-label>
                        <q-badge
                          :color="centroCostoDetalle.activo ? 'green' : 'red'"
                          :label="centroCostoDetalle.activo ? 'Activo' : 'Inactivo'"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item v-if="centroCostoDetalle.fecha_creacion">
                    <q-item-section>
                      <q-item-label caption>Fecha de Creación</q-item-label>
                      <q-item-label>{{ formatDate(centroCostoDetalle.fecha_creacion) }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>
            </div>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cerrar" v-close-popup />
            <q-btn
              color="primary"
              label="Editar"
              @click="editarDesdeDetalle"
              v-if="centroCostoDetalle"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import {
  useCentroCostoStore,
  type CentroCosto,
  type CentroCostoCreate
} from '../stores/centrosCosto'
import { formatCurrency, formatDate as formatDateUtil } from '@/utils/formatters'

const $q = useQuasar()
const centroCostoStore = useCentroCostoStore()

// Reactive data
const centrosCosto = ref<CentroCosto[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const showCreateDialog = ref(false)
const editando = ref(false)
const showDetalleDialog = ref(false)
const centroCostoDetalle = ref<CentroCosto | null>(null)

// Filters
const filtros = ref({
  busqueda: '',
  estado: null as boolean | null
})

const estadoOptions = [
  { label: 'Activo', value: true },
  { label: 'Inactivo', value: false }
]

// Pagination
const paginacion = ref({
  sortBy: 'id_centro_costo',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Form
const formCentroCosto = ref<CentroCostoCreate & { id_centro_costo?: number }>({
  codigo_centro_costo: '',
  nombre_centro_costo: '',
  descripcion: '',
  presupuesto_anual: 0,
  activo: true
})

// Table columns
const columnsCentrosCosto = [
  {
    name: 'codigo_centro_costo',
    required: true,
    label: 'Código',
    align: 'left' as const,
    field: 'codigo_centro_costo',
    sortable: true
  },
  {
    name: 'nombre_centro_costo',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_centro_costo',
    sortable: true
  },
  {
    name: 'descripcion',
    label: 'Descripción',
    align: 'left' as const,
    field: 'descripcion'
  },
  {
    name: 'presupuesto_anual',
    label: 'Presupuesto Anual',
    align: 'right' as const,
    field: 'presupuesto_anual',
    sortable: true
  },
  {
    name: 'activo',
    label: 'Estado',
    align: 'center' as const,
    field: 'activo',
    sortable: true
  },
  {
    name: 'actions',
    label: 'Acciones',
    align: 'center' as const,
    field: 'actions'
  }
]

// Methods
const onRequestCentrosCosto = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarCentrosCosto()
}

const cargarCentrosCosto = async () => {
  try {
    isLoading.value = true
    const params: any = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    if (filtros.value.estado !== null) {
      params.activo = filtros.value.estado
    }

    const response = await centroCostoStore.obtenerCentrosCosto(params)

    // Filtrar por búsqueda en el frontend si hay texto de búsqueda
    let centrosFiltered = response
    if (filtros.value.busqueda && filtros.value.busqueda.trim()) {
      const busqueda = filtros.value.busqueda.toLowerCase().trim()
      centrosFiltered = response.filter((centro: any) =>
        centro.codigo_centro_costo.toLowerCase().includes(busqueda) ||
        centro.nombre_centro_costo.toLowerCase().includes(busqueda) ||
        (centro.descripcion && centro.descripcion.toLowerCase().includes(busqueda))
      )
    }

    centrosCosto.value = centrosFiltered

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar centros de costo',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const buscarCentrosCosto = async () => {
  paginacion.value.page = 1
  await cargarCentrosCosto()
}

const limpiarFiltros = () => {
  filtros.value.busqueda = ''
  filtros.value.estado = null
  buscarCentrosCosto()
}

const abrirFormularioCentroCosto = () => {
  resetForm()
  showCreateDialog.value = true
}

const editarCentroCosto = (centroCosto: CentroCosto) => {
  editando.value = true
  formCentroCosto.value = { ...centroCosto }
  showCreateDialog.value = true
}

const verDetalleCentroCosto = async (centroCosto: CentroCosto) => {
  try {
    centroCostoDetalle.value = await centroCostoStore.obtenerCentroCosto(centroCosto.id_centro_costo)
    showDetalleDialog.value = true
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar detalles del centro de costo',
      caption: error.message
    })
  }
}

const editarDesdeDetalle = () => {
  if (centroCostoDetalle.value) {
    showDetalleDialog.value = false
    editarCentroCosto(centroCostoDetalle.value)
  }
}

const guardarCentroCosto = async () => {
  try {
    isGuardando.value = true

    if (editando.value && formCentroCosto.value.id_centro_costo) {
      await centroCostoStore.actualizarCentroCosto(formCentroCosto.value.id_centro_costo, formCentroCosto.value)
      $q.notify({
        type: 'positive',
        message: 'Centro de costo actualizado correctamente'
      })
    } else {
      await centroCostoStore.crearCentroCosto(formCentroCosto.value)
      $q.notify({
        type: 'positive',
        message: 'Centro de costo creado correctamente'
      })
    }

    showCreateDialog.value = false
    resetForm()
    await cargarCentrosCosto()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar centro de costo',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoCentroCosto = async (centroCosto: CentroCosto) => {
  try {
    if (centroCosto.activo) {
      await centroCostoStore.eliminarCentroCosto(centroCosto.id_centro_costo)
      $q.notify({
        type: 'positive',
        message: 'Centro de costo desactivado'
      })
    } else {
      // Reactivar mediante actualización
      await centroCostoStore.actualizarCentroCosto(centroCosto.id_centro_costo, { activo: true })
      $q.notify({
        type: 'positive',
        message: 'Centro de costo activado'
      })
    }

    await cargarCentrosCosto()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado del centro de costo',
      caption: error.message
    })
  }
}

const resetForm = () => {
  editando.value = false
  formCentroCosto.value = {
    codigo_centro_costo: '',
    nombre_centro_costo: '',
    descripcion: '',
    presupuesto_anual: 0,
    activo: true
  }
}

// Usar formatters centralizados
const formatDate = formatDateUtil

// Lifecycle
onMounted(() => {
  cargarCentrosCosto()
})
</script>
