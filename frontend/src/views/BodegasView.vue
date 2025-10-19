<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-xl">
        <div>
          <div class="row items-center q-mb-sm">
            <q-icon name="warehouse" size="32px" color="primary" class="q-mr-md" />
            <div>
              <h4 class="q-my-none text-h4 text-weight-light">Gestión de <span class="text-weight-bold text-primary">Bodegas</span></h4>
              <p class="text-grey-6 q-mb-none text-body2">Administración de almacenes y ubicaciones de inventario</p>
            </div>
          </div>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nueva Bodega"
          @click="abrirFormularioBodega"
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
            <div class="col-12 col-md-4">
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
            <div class="col-12 col-md-2">
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
            <div class="col-12 col-md-3">
              <q-select
                v-model="filtros.certificacion"
                :options="certificacionOptions"
                label="Certificación"
                outlined
                dense
                clearable
                emit-value
                map-options
              />
            </div>
            <div class="col-12 col-md-3 row q-gutter-sm justify-end items-center">
              <q-btn color="primary" icon="search" label="Buscar" @click="buscarBodegas" unelevated no-caps />
              <q-btn color="grey-6" icon="clear" label="Limpiar" @click="limpiarFiltros" flat no-caps />
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Bodegas Table -->
      <q-table
        :rows="bodegas"
        :columns="columnsBodegas"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_bodega"
        flat
        bordered
        @request="onRequestBodegas"
      >
        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'green' : 'red'"
              :label="props.value ? 'Activo' : 'Inactivo'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-requiere_certificacion="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'blue' : 'grey'"
              :label="props.value ? 'Sí' : 'No'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-temperatura="props">
          <q-td :props="props">
            <span v-if="props.row.temperatura_min || props.row.temperatura_max">
              {{ formatTemperatura(props.row.temperatura_min, props.row.temperatura_max) }}
            </span>
            <span v-else class="text-grey-5">-</span>
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
              @click="editarBodega(props.row as Bodega)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="route"
              color="info"
              size="sm"
              @click="verPasillos(props.row as Bodega)"
            >
              <q-tooltip>Ver Estantes</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'negative' : 'positive'"
              size="sm"
              @click="toggleEstadoBodega(props.row as Bodega)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="delete"
              color="negative"
              size="sm"
              @click="eliminarBodega(props.row as Bodega)"
            >
              <q-tooltip>Eliminar</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Bodega Dialog -->
      <q-dialog v-model="showCreateBodegaDialog" persistent>
        <q-card style="min-width: 600px; max-width: 800px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoBodega ? 'Editar' : 'Nueva' }} Bodega</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarBodega">
              <div class="row q-gutter-md">
                <div class="col-12 col-md-3">
                  <q-input
                    v-model="formBodega.codigo_bodega"
                    label="Código *"
                    outlined
                    dense
                    maxlength="1"
                    :rules="[val => !!val || 'El código es requerido']"
                  />
                </div>
                <div class="col-12 col-md-8">
                  <q-input
                    v-model="formBodega.nombre_bodega"
                    label="Nombre *"
                    outlined
                    dense
                    :rules="[val => !!val || 'El nombre es requerido']"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formBodega.descripcion"
                    label="Descripción"
                    outlined
                    type="textarea"
                    rows="3"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model.number="formBodega.temperatura_min"
                    label="Temperatura Mínima (°C)"
                    outlined
                    dense
                    type="number"
                    step="0.1"
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input
                    v-model.number="formBodega.temperatura_max"
                    label="Temperatura Máxima (°C)"
                    outlined
                    dense
                    type="number"
                    step="0.1"
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-input
                    v-model.number="formBodega.humedad_max"
                    label="Humedad Máxima (%)"
                    outlined
                    dense
                    type="number"
                    step="0.1"
                    min="0"
                    max="100"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-6">
                  <q-toggle
                    v-model="formBodega.requiere_certificacion"
                    label="Requiere Certificación"
                  />
                </div>
                <div class="col-12 col-md-5">
                  <q-toggle
                    v-model="formBodega.activo"
                    label="Activo"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar"
              @click="guardarBodega"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Pasillos Dialog -->
      <q-dialog v-model="showPasillosDialog" persistent>
        <q-card style="min-width: 1000px; max-width: 1200px">
          <q-card-section class="row items-center">
            <div class="text-h6">Estantes de {{ bodegaSeleccionada?.nombre_bodega }}</div>
            <q-space />
            <q-btn
              color="primary"
              icon="add"
              label="Nuevo Estante"
              @click="abrirFormularioPasillo"
              class="q-mr-sm"
            />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <!-- Pasillos Table -->
            <q-table
              :rows="pasillos"
              :columns="columnsPasillos"
              :loading="isLoading"
              row-key="id_pasillo"
              flat
              bordered
            >
              <template v-slot:body-cell-activo="props">
                <q-td :props="props">
                  <q-badge
                    :color="props.value ? 'green' : 'red'"
                    :label="props.value ? 'Activo' : 'Inactivo'"
                  />
                </q-td>
              </template>

              <template v-slot:body-cell-longitud_metros="props">
                <q-td :props="props">
                  {{ props.value ? `${props.value} m` : '-' }}
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
                    @click="editarPasillo(props.row as Pasillo)"
                  >
                    <q-tooltip>Editar</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    round
                    icon="shelves"
                    color="info"
                    size="sm"
                    @click="verEstantes(props.row as Pasillo)"
                  >
                    <q-tooltip>Ver Nivel</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    round
                    :icon="props.row.activo ? 'block' : 'check_circle'"
                    :color="props.row.activo ? 'negative' : 'positive'"
                    size="sm"
                    @click="toggleEstadoPasillo(props.row as Pasillo)"
                  >
                    <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    round
                    icon="delete"
                    color="negative"
                    size="sm"
                    @click="eliminarPasillo(props.row as Pasillo)"
                  >
                    <q-tooltip>Eliminar</q-tooltip>
                  </q-btn>
                </q-td>
              </template>
            </q-table>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cerrar" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Create/Edit Pasillo Dialog -->
      <q-dialog v-model="showCreatePasilloDialog" persistent>
        <q-card style="min-width: 500px; max-width: 600px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoPasillo ? 'Editar' : 'Nuevo' }} Pasillo</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarPasillo">
              <div class="row q-gutter-md">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model.number="formPasillo.numero_pasillo"
                    label="Número *"
                    outlined
                    dense
                    type="number"
                    min="1"
                    :rules="[val => !!val || 'El número es requerido']"
                  />
                </div>
                <div class="col-12 col-md-7">
                  <q-input
                    v-model="formPasillo.nombre_pasillo"
                    label="Nombre"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model.number="formPasillo.longitud_metros"
                    label="Longitud (metros)"
                    outlined
                    dense
                    type="number"
                    step="0.1"
                    min="0"
                  />
                </div>
                <div class="col-12 col-md-5">
                  <q-toggle
                    v-model="formPasillo.activo"
                    label="Activo"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar"
              @click="guardarPasillo"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Estantes Dialog -->
      <q-dialog v-model="showEstantesDialog" persistent>
        <q-card style="min-width: 1000px; max-width: 1200px">
          <q-card-section class="row items-center">
            <div class="text-h6">Niveles del Estante {{ pasilloSeleccionado?.numero_pasillo }}</div>
            <q-space />
            <q-btn
              color="primary"
              icon="add"
              label="Nuevo Nivel"
              @click="abrirFormularioEstante"
              class="q-mr-sm"
            />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <!-- Estantes Table -->
            <q-table
              :rows="estantes"
              :columns="columnsEstantes"
              :loading="isLoading"
              row-key="id_estante"
              flat
              bordered
            >
              <template v-slot:body-cell-activo="props">
                <q-td :props="props">
                  <q-badge
                    :color="props.value ? 'green' : 'red'"
                    :label="props.value ? 'Activo' : 'Inactivo'"
                  />
                </q-td>
              </template>

              <template v-slot:body-cell-altura_metros="props">
                <q-td :props="props">
                  {{ props.value ? `${props.value} m` : '-' }}
                </q-td>
              </template>

              <template v-slot:body-cell-capacidad_peso_kg="props">
                <q-td :props="props">
                  {{ props.value ? `${props.value} kg` : '-' }}
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
                    @click="editarEstante(props.row as Estante)"
                  >
                    <q-tooltip>Editar</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    round
                    :icon="props.row.activo ? 'block' : 'check_circle'"
                    :color="props.row.activo ? 'negative' : 'positive'"
                    size="sm"
                    @click="toggleEstadoEstante(props.row as Estante)"
                  >
                    <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    round
                    icon="delete"
                    color="negative"
                    size="sm"
                    @click="eliminarEstante(props.row as Estante)"
                  >
                    <q-tooltip>Eliminar</q-tooltip>
                  </q-btn>
                </q-td>
              </template>
            </q-table>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cerrar" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Create/Edit Estante Dialog -->
      <q-dialog v-model="showCreateEstanteDialog" persistent>
        <q-card style="min-width: 500px; max-width: 600px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoEstante ? 'Editar' : 'Nuevo' }} Estante</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarEstante">
              <div class="row q-gutter-md">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formEstante.codigo_estante"
                    label="Código *"
                    outlined
                    dense
                    maxlength="5"
                    :rules="[val => !!val || 'El código es requerido']"
                  />
                </div>
                <div class="col-12 col-md-5">
                  <q-toggle
                    v-model="formEstante.activo"
                    label="Activo"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model.number="formEstante.altura_metros"
                    label="Altura (metros)"
                    outlined
                    dense
                    type="number"
                    step="0.1"
                    min="0"
                  />
                </div>
                <div class="col-12 col-md-5">
                  <q-input
                    v-model.number="formEstante.capacidad_peso_kg"
                    label="Capacidad (kg)"
                    outlined
                    dense
                    type="number"
                    step="0.1"
                    min="0"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar"
              @click="guardarEstante"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import {
  useBodegaStore,
  type Bodega,
  type BodegaCreate,
  type Pasillo,
  type PasilloCreate,
  type Estante,
  type EstanteCreate
} from '../stores/bodegas'

const $q = useQuasar()
const bodegaStore = useBodegaStore()

// Reactive data
const bodegas = ref<Bodega[]>([])
const pasillos = ref<Pasillo[]>([])
const estantes = ref<Estante[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const showCreateBodegaDialog = ref(false)
const showPasillosDialog = ref(false)
const showCreatePasilloDialog = ref(false)
const showEstantesDialog = ref(false)
const showCreateEstanteDialog = ref(false)
const editandoBodega = ref(false)
const editandoPasillo = ref(false)
const editandoEstante = ref(false)
const bodegaSeleccionada = ref<Bodega | null>(null)
const pasilloSeleccionado = ref<Pasillo | null>(null)

// Filters
const filtros = ref({
  busqueda: '',
  estado: null as boolean | null,
  certificacion: null as boolean | null
})

const estadoOptions = [
  { label: 'Activo', value: true },
  { label: 'Inactivo', value: false }
]

const certificacionOptions = [
  { label: 'Requiere Certificación', value: true },
  { label: 'No Requiere Certificación', value: false }
]

// Pagination
const paginacion = ref({
  sortBy: 'id_bodega',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formBodega = ref<BodegaCreate & { id_bodega?: number }>({
  codigo_bodega: '',
  nombre_bodega: '',
  descripcion: '',
  temperatura_min: undefined,
  temperatura_max: undefined,
  humedad_max: undefined,
  requiere_certificacion: false,
  activo: true
})

const formPasillo = ref<PasilloCreate & { id_pasillo?: number }>({
  id_bodega: 0,
  numero_pasillo: 1,
  nombre_pasillo: '',
  longitud_metros: undefined,
  activo: true
})

const formEstante = ref<EstanteCreate & { id_estante?: number }>({
  id_pasillo: 0,
  codigo_estante: '',
  altura_metros: undefined,
  capacidad_peso_kg: undefined,
  activo: true
})

// Table columns for bodegas
const columnsBodegas = [
  {
    name: 'codigo_bodega',
    required: true,
    label: 'Código',
    align: 'left' as const,
    field: 'codigo_bodega',
    sortable: true
  },
  {
    name: 'nombre_bodega',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_bodega',
    sortable: true
  },
  {
    name: 'descripcion',
    label: 'Descripción',
    align: 'left' as const,
    field: 'descripcion'
  },
  {
    name: 'temperatura',
    label: 'Temperatura',
    align: 'center' as const,
    field: 'temperatura'
  },
  {
    name: 'requiere_certificacion',
    label: 'Certificación',
    align: 'center' as const,
    field: 'requiere_certificacion',
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

// Table columns for pasillos
const columnsPasillos = [
  {
    name: 'numero_pasillo',
    required: true,
    label: 'Número',
    align: 'center' as const,
    field: 'numero_pasillo',
    sortable: true
  },
  {
    name: 'nombre_pasillo',
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_pasillo'
  },
  {
    name: 'longitud_metros',
    label: 'Longitud',
    align: 'center' as const,
    field: 'longitud_metros',
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

// Table columns for estantes
const columnsEstantes = [
  {
    name: 'codigo_estante',
    required: true,
    label: 'Código',
    align: 'center' as const,
    field: 'codigo_estante',
    sortable: true
  },
  {
    name: 'altura_metros',
    label: 'Altura',
    align: 'center' as const,
    field: 'altura_metros',
    sortable: true
  },
  {
    name: 'capacidad_peso_kg',
    label: 'Capacidad',
    align: 'center' as const,
    field: 'capacidad_peso_kg',
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
const onRequestBodegas = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarBodegas()
}

const cargarBodegas = async () => {
  try {
    isLoading.value = true
    const params: any = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    if (filtros.value.estado !== null) {
      params.activo = filtros.value.estado
    }

    let response = await bodegaStore.obtenerBodegas(params)

    // Filtrar por búsqueda en el frontend
    if (filtros.value.busqueda && filtros.value.busqueda.trim()) {
      const busqueda = filtros.value.busqueda.toLowerCase().trim()
      response = response.filter((bodega: any) =>
        bodega.codigo_bodega.toLowerCase().includes(busqueda) ||
        bodega.nombre_bodega.toLowerCase().includes(busqueda) ||
        (bodega.descripcion && bodega.descripcion.toLowerCase().includes(busqueda))
      )
    }

    // Filtrar por certificación
    if (filtros.value.certificacion !== null) {
      response = response.filter((bodega: any) =>
        bodega.requiere_certificacion === filtros.value.certificacion
      )
    }

    bodegas.value = response

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar bodegas',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const buscarBodegas = async () => {
  paginacion.value.page = 1
  await cargarBodegas()
}

const limpiarFiltros = () => {
  filtros.value.busqueda = ''
  filtros.value.estado = null
  filtros.value.certificacion = null
  buscarBodegas()
}

const abrirFormularioBodega = () => {
  resetFormBodega()
  showCreateBodegaDialog.value = true
}

const editarBodega = (bodega: Bodega) => {
  editandoBodega.value = true
  formBodega.value = { ...bodega }
  showCreateBodegaDialog.value = true
}

const guardarBodega = async () => {
  try {
    isGuardando.value = true

    if (editandoBodega.value && formBodega.value.id_bodega) {
      await bodegaStore.actualizarBodega(formBodega.value.id_bodega, formBodega.value)
      $q.notify({
        type: 'positive',
        message: 'Bodega actualizada correctamente'
      })
    } else {
      await bodegaStore.crearBodega(formBodega.value)
      $q.notify({
        type: 'positive',
        message: 'Bodega creada correctamente'
      })
    }

    showCreateBodegaDialog.value = false
    resetFormBodega()
    await cargarBodegas()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar bodega',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoBodega = async (bodega: Bodega) => {
  try {
    await bodegaStore.toggleEstadoBodega(bodega.id_bodega)

    const nuevoEstado = !bodega.activo
    $q.notify({
      type: 'positive',
      message: `Bodega ${nuevoEstado ? 'activada' : 'desactivada'}`
    })

    await cargarBodegas()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de bodega',
      caption: error.message
    })
  }
}

const eliminarBodega = async (bodega: Bodega) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de eliminar la bodega "${bodega.nombre_bodega}"? Esta acción la marcará como inactiva.`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await bodegaStore.eliminarBodega(bodega.id_bodega)
      $q.notify({
        type: 'positive',
        message: 'Bodega eliminada correctamente'
      })
      await cargarBodegas()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar bodega',
        caption: error.message
      })
    }
  })
}

const resetFormBodega = () => {
  editandoBodega.value = false
  formBodega.value = {
    codigo_bodega: '',
    nombre_bodega: '',
    descripcion: '',
    temperatura_min: undefined,
    temperatura_max: undefined,
    humedad_max: undefined,
    requiere_certificacion: false,
    activo: true
  }
}

// Pasillos methods
const verPasillos = async (bodega: Bodega) => {
  bodegaSeleccionada.value = bodega
  await cargarPasillos(bodega.id_bodega)
  showPasillosDialog.value = true
}

const cargarPasillos = async (bodegaId: number) => {
  try {
    isLoading.value = true
    const response = await bodegaStore.obtenerPasillosPorBodega(bodegaId)
    pasillos.value = response
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar estantes',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const abrirFormularioPasillo = () => {
  resetFormPasillo()
  if (bodegaSeleccionada.value) {
    formPasillo.value.id_bodega = bodegaSeleccionada.value.id_bodega
  }
  showCreatePasilloDialog.value = true
}

const editarPasillo = (pasillo: Pasillo) => {
  editandoPasillo.value = true
  formPasillo.value = { ...pasillo }
  showCreatePasilloDialog.value = true
}

const guardarPasillo = async () => {
  try {
    isGuardando.value = true

    if (editandoPasillo.value && formPasillo.value.id_pasillo) {
      await bodegaStore.actualizarPasillo(formPasillo.value.id_pasillo, formPasillo.value)
      $q.notify({
        type: 'positive',
        message: 'Estante actualizado correctamente'
      })
    } else {
      await bodegaStore.crearPasillo(formPasillo.value)
      $q.notify({
        type: 'positive',
        message: 'Estante creado correctamente'
      })
    }

    showCreatePasilloDialog.value = false
    resetFormPasillo()
    if (bodegaSeleccionada.value) {
      await cargarPasillos(bodegaSeleccionada.value.id_bodega)
    }

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar estante',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoPasillo = async (pasillo: Pasillo) => {
  try {
    await bodegaStore.toggleEstadoPasillo(pasillo.id_pasillo)

    const nuevoEstado = !pasillo.activo
    $q.notify({
      type: 'positive',
      message: `Estante ${nuevoEstado ? 'activado' : 'desactivado'}`
    })

    if (bodegaSeleccionada.value) {
      await cargarPasillos(bodegaSeleccionada.value.id_bodega)
    }

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de estante',
      caption: error.message
    })
  }
}

const eliminarPasillo = async (pasillo: Pasillo) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de eliminar el estante "${pasillo.numero_pasillo}"? Esta acción lo marcará como inactivo.`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await bodegaStore.eliminarPasillo(pasillo.id_pasillo)
      $q.notify({
        type: 'positive',
        message: 'Estante eliminado correctamente'
      })
      if (bodegaSeleccionada.value) {
        await cargarPasillos(bodegaSeleccionada.value.id_bodega)
      }
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar estante',
        caption: error.message
      })
    }
  })
}

const resetFormPasillo = () => {
  editandoPasillo.value = false
  formPasillo.value = {
    id_bodega: bodegaSeleccionada.value?.id_bodega || 0,
    numero_pasillo: 1,
    nombre_pasillo: '',
    longitud_metros: undefined,
    activo: true
  }
}

// Estantes methods
const verEstantes = async (pasillo: Pasillo) => {
  pasilloSeleccionado.value = pasillo
  await cargarEstantes(pasillo.id_pasillo)
  showEstantesDialog.value = true
}

const cargarEstantes = async (pasilloId: number) => {
  try {
    isLoading.value = true
    const response = await bodegaStore.obtenerEstantesPorPasillo(pasilloId)
    estantes.value = response
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar niveles',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const abrirFormularioEstante = () => {
  resetFormEstante()
  if (pasilloSeleccionado.value) {
    formEstante.value.id_pasillo = pasilloSeleccionado.value.id_pasillo
  }
  showCreateEstanteDialog.value = true
}

const editarEstante = (estante: Estante) => {
  editandoEstante.value = true
  formEstante.value = { ...estante }
  showCreateEstanteDialog.value = true
}

const guardarEstante = async () => {
  try {
    isGuardando.value = true

    if (editandoEstante.value && formEstante.value.id_estante) {
      await bodegaStore.actualizarEstante(formEstante.value.id_estante, formEstante.value)
      $q.notify({
        type: 'positive',
        message: 'Nivel actualizado correctamente'
      })
    } else {
      await bodegaStore.crearEstante(formEstante.value)
      $q.notify({
        type: 'positive',
        message: 'Nivel creado correctamente'
      })
    }

    showCreateEstanteDialog.value = false
    resetFormEstante()
    if (pasilloSeleccionado.value) {
      await cargarEstantes(pasilloSeleccionado.value.id_pasillo)
    }

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar nivel',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoEstante = async (estante: Estante) => {
  try {
    await bodegaStore.toggleEstadoEstante(estante.id_estante)

    const nuevoEstado = !estante.activo
    $q.notify({
      type: 'positive',
      message: `Nivel ${nuevoEstado ? 'activado' : 'desactivado'}`
    })

    if (pasilloSeleccionado.value) {
      await cargarEstantes(pasilloSeleccionado.value.id_pasillo)
    }

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de nivel',
      caption: error.message
    })
  }
}

const eliminarEstante = async (estante: Estante) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de eliminar el nivel "${estante.codigo_estante}"? Esta acción lo marcará como inactivo.`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await bodegaStore.eliminarEstante(estante.id_estante)
      $q.notify({
        type: 'positive',
        message: 'Nivel eliminado correctamente'
      })
      if (pasilloSeleccionado.value) {
        await cargarEstantes(pasilloSeleccionado.value.id_pasillo)
      }
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar nivel',
        caption: error.message
      })
    }
  })
}

const resetFormEstante = () => {
  editandoEstante.value = false
  formEstante.value = {
    id_pasillo: pasilloSeleccionado.value?.id_pasillo || 0,
    codigo_estante: '',
    altura_metros: undefined,
    capacidad_peso_kg: undefined,
    activo: true
  }
}

const formatTemperatura = (min?: number, max?: number) => {
  if (min !== undefined && max !== undefined) {
    return `${min}°C - ${max}°C`
  } else if (min !== undefined) {
    return `Min: ${min}°C`
  } else if (max !== undefined) {
    return `Max: ${max}°C`
  }
  return '-'
}

// Lifecycle
onMounted(() => {
  cargarBodegas()
})
</script>