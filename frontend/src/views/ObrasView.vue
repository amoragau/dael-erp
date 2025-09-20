<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Gestión de Obras</h4>
          <p class="text-grey-7 q-mb-none">Administra las obras y proyectos del sistema</p>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nueva Obra"
          @click="abrirFormularioObra"
        />
      </div>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-gutter-md items-center">
            <q-input
              v-model="filtros.busqueda"
              placeholder="Buscar por código, nombre o cliente..."
              outlined
              dense
              clearable
              style="min-width: 300px"
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
              v-model="filtros.cliente"
              :options="clientesOptions"
              label="Cliente"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 200px"
            />
            <q-select
              v-model="filtros.activo"
              :options="activoOptions"
              label="Activo"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 120px"
            />
            <q-btn
              color="primary"
              icon="search"
              label="Buscar"
              @click="buscarObras"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Obras Table -->
      <q-table
        :rows="obras"
        :columns="columnsObras"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_obra"
        flat
        bordered
        @request="onRequestObras"
      >
        <template v-slot:body-cell-estado="props">
          <q-td :props="props">
            <q-badge
              :color="getEstadoColor(props.value)"
              :label="getEstadoLabel(props.value)"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'green' : 'red'"
              :label="props.value ? 'Activo' : 'Inactivo'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-valor_contrato="props">
          <q-td :props="props">
            {{ formatCurrency(props.value, props.row.moneda) }}
          </q-td>
        </template>

        <template v-slot:body-cell-fecha_fin_programada="props">
          <q-td :props="props">
            <span v-if="props.value">
              {{ formatDate(props.value) }}
              <q-badge
                v-if="isObraRetrasada(props.row)"
                color="red"
                text-color="white"
                label="RETRASADA"
                class="q-ml-sm"
              />
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
              @click="editarObra(props.row as Obra)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="warehouse"
              color="info"
              size="sm"
              @click="verAlmacenes(props.row as Obra)"
            >
              <q-tooltip>Ver Almacenes</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="timeline"
              color="warning"
              size="sm"
              @click="cambiarEstado(props.row as Obra)"
            >
              <q-tooltip>Cambiar Estado</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'negative' : 'positive'"
              size="sm"
              @click="toggleEstadoObra(props.row as Obra)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="delete"
              color="negative"
              size="sm"
              @click="eliminarObra(props.row as Obra)"
            >
              <q-tooltip>Eliminar</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Obra Dialog -->
      <q-dialog v-model="showCreateObraDialog" persistent maximized>
        <q-card>
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoObra ? 'Editar' : 'Nueva' }} Obra</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-form @submit="guardarObra">
              <q-tabs v-model="tabActual" dense class="text-grey" active-color="primary" indicator-color="primary" align="justify">
                <q-tab name="general" label="Información General" />
                <q-tab name="fechas" label="Fechas y Cronograma" />
                <q-tab name="financiero" label="Información Financiera" />
                <q-tab name="inventario" label="Control de Inventario" />
              </q-tabs>

              <q-separator />

              <q-tab-panels v-model="tabActual" animated>
                <!-- Tab General -->
                <q-tab-panel name="general">
                  <div class="row q-gutter-md">
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model="formObra.codigo_obra"
                        label="Código *"
                        outlined
                        dense
                        :rules="[val => !!val || 'El código es requerido']"
                      />
                    </div>
                    <div class="col-12 col-md-8">
                      <q-input
                        v-model="formObra.nombre_obra"
                        label="Nombre de la Obra *"
                        outlined
                        dense
                        :rules="[val => !!val || 'El nombre es requerido']"
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12">
                      <q-input
                        v-model="formObra.descripcion"
                        label="Descripción"
                        outlined
                        type="textarea"
                        rows="3"
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-6">
                      <q-select
                        v-model="formObra.id_cliente"
                        :options="clientesOptions"
                        label="Cliente *"
                        outlined
                        dense
                        emit-value
                        map-options
                        :rules="[val => !!val || 'El cliente es requerido']"
                      />
                    </div>
                    <div class="col-12 col-md-5">
                      <q-select
                        v-model="formObra.estado"
                        :options="estadoOptions"
                        label="Estado *"
                        outlined
                        dense
                        emit-value
                        map-options
                        :rules="[val => !!val || 'El estado es requerido']"
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12">
                      <q-input
                        v-model="formObra.direccion_obra"
                        label="Dirección de la Obra"
                        outlined
                        dense
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="formObra.ciudad"
                        label="Ciudad"
                        outlined
                        dense
                      />
                    </div>
                    <div class="col-12 col-md-5">
                      <q-input
                        v-model="formObra.codigo_postal"
                        label="Código Postal"
                        outlined
                        dense
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model="formObra.supervisor_obra"
                        label="Supervisor de Obra"
                        outlined
                        dense
                      />
                    </div>
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model="formObra.contacto_obra"
                        label="Contacto en Obra"
                        outlined
                        dense
                      />
                    </div>
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model="formObra.telefono_obra"
                        label="Teléfono de Obra"
                        outlined
                        dense
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-6">
                      <q-toggle
                        v-model="formObra.activo"
                        label="Activo"
                      />
                    </div>
                  </div>
                </q-tab-panel>

                <!-- Tab Fechas -->
                <q-tab-panel name="fechas">
                  <div class="row q-gutter-md">
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="formObra.fecha_inicio_programada"
                        label="Fecha Inicio Programada"
                        outlined
                        dense
                        type="date"
                      />
                    </div>
                    <div class="col-12 col-md-5">
                      <q-input
                        v-model="formObra.fecha_fin_programada"
                        label="Fecha Fin Programada"
                        outlined
                        dense
                        type="date"
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="formObra.fecha_inicio_real"
                        label="Fecha Inicio Real"
                        outlined
                        dense
                        type="date"
                      />
                    </div>
                    <div class="col-12 col-md-5">
                      <q-input
                        v-model="formObra.fecha_fin_real"
                        label="Fecha Fin Real"
                        outlined
                        dense
                        type="date"
                      />
                    </div>
                  </div>
                </q-tab-panel>

                <!-- Tab Financiero -->
                <q-tab-panel name="financiero">
                  <div class="row q-gutter-md">
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model.number="formObra.valor_contrato"
                        label="Valor del Contrato"
                        outlined
                        dense
                        type="number"
                        step="0.01"
                        min="0"
                      />
                    </div>
                    <div class="col-12 col-md-5">
                      <q-select
                        v-model="formObra.moneda"
                        :options="monedaOptions"
                        label="Moneda"
                        outlined
                        dense
                        emit-value
                        map-options
                      />
                    </div>
                  </div>
                </q-tab-panel>

                <!-- Tab Inventario -->
                <q-tab-panel name="inventario">
                  <div class="row q-gutter-md">
                    <div class="col-12 col-md-6">
                      <q-toggle
                        v-model="formObra.requiere_devolucion_sobrantes"
                        label="Requiere Devolución de Sobrantes"
                      />
                    </div>
                    <div class="col-12 col-md-5">
                      <q-input
                        v-model.number="formObra.dias_limite_devolucion"
                        label="Días Límite para Devolución"
                        outlined
                        dense
                        type="number"
                        min="1"
                        max="365"
                      />
                    </div>
                  </div>
                </q-tab-panel>
              </q-tab-panels>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar"
              @click="guardarObra"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Almacenes Dialog -->
      <q-dialog v-model="showAlmacenesDialog" persistent>
        <q-card style="min-width: 1000px; max-width: 1200px">
          <q-card-section class="row items-center">
            <div class="text-h6">Almacenes de {{ obraSeleccionada?.nombre_obra }}</div>
            <q-space />
            <q-btn
              color="primary"
              icon="add"
              label="Nuevo Almacén"
              @click="abrirFormularioAlmacen"
              class="q-mr-sm"
            />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <!-- Almacenes Table -->
            <q-table
              :rows="almacenesObra"
              :columns="columnsAlmacenes"
              :loading="isLoading"
              row-key="id_almacen"
              flat
              bordered
            >
              <template v-slot:body-cell-tiene_seguridad="props">
                <q-td :props="props">
                  <q-icon
                    :name="props.value ? 'security' : 'lock_open'"
                    :color="props.value ? 'green' : 'red'"
                  />
                </q-td>
              </template>

              <template v-slot:body-cell-tiene_techo="props">
                <q-td :props="props">
                  <q-icon
                    :name="props.value ? 'roofing' : 'outdoor_grill'"
                    :color="props.value ? 'blue' : 'orange'"
                  />
                </q-td>
              </template>

              <template v-slot:body-cell-activo="props">
                <q-td :props="props">
                  <q-badge
                    :color="props.value ? 'green' : 'red'"
                    :label="props.value ? 'Activo' : 'Inactivo'"
                  />
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
                    @click="editarAlmacen(props.row as AlmacenObra)"
                  >
                    <q-tooltip>Editar</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    round
                    icon="delete"
                    color="negative"
                    size="sm"
                    @click="eliminarAlmacen(props.row as AlmacenObra)"
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

      <!-- Create/Edit Almacen Dialog -->
      <q-dialog v-model="showCreateAlmacenDialog" persistent>
        <q-card style="min-width: 600px; max-width: 800px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoAlmacen ? 'Editar' : 'Nuevo' }} Almacén</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarAlmacen">
              <div class="row q-gutter-md">
                <div class="col-12">
                  <q-input
                    v-model="formAlmacen.nombre_almacen"
                    label="Nombre del Almacén *"
                    outlined
                    dense
                    :rules="[val => !!val || 'El nombre es requerido']"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formAlmacen.descripcion"
                    label="Descripción"
                    outlined
                    type="textarea"
                    rows="2"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formAlmacen.direccion"
                    label="Dirección"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formAlmacen.responsable"
                    label="Responsable"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-5">
                  <q-input
                    v-model="formAlmacen.telefono"
                    label="Teléfono"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model.number="formAlmacen.capacidad_m3"
                    label="Capacidad (m³)"
                    outlined
                    dense
                    type="number"
                    step="0.01"
                    min="0"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-4">
                  <q-toggle
                    v-model="formAlmacen.tiene_seguridad"
                    label="Tiene Seguridad"
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-toggle
                    v-model="formAlmacen.tiene_techo"
                    label="Tiene Techo"
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-toggle
                    v-model="formAlmacen.activo"
                    label="Activo"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formAlmacen.observaciones"
                    label="Observaciones"
                    outlined
                    type="textarea"
                    rows="2"
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
              @click="guardarAlmacen"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Change Estado Dialog -->
      <q-dialog v-model="showCambiarEstadoDialog" persistent>
        <q-card style="min-width: 400px">
          <q-card-section class="row items-center">
            <div class="text-h6">Cambiar Estado de Obra</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <p>Obra: <strong>{{ obraSeleccionada?.nombre_obra }}</strong></p>
            <p>Estado actual: <q-badge :color="getEstadoColor(obraSeleccionada?.estado)" :label="getEstadoLabel(obraSeleccionada?.estado)" /></p>

            <q-select
              v-model="nuevoEstado"
              :options="estadoOptions"
              label="Nuevo Estado"
              outlined
              dense
              emit-value
              map-options
            />
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Cambiar"
              @click="confirmarCambioEstado"
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
  useObraStore,
  type Obra,
  type ObraCreate,
  type AlmacenObra,
  type AlmacenObraCreate,
  type EstadoObra,
  ESTADOS_OBRA
} from '../stores/obras'

const $q = useQuasar()
const obraStore = useObraStore()

// Reactive data
const obras = ref<Obra[]>([])
const almacenesObra = ref<AlmacenObra[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const showCreateObraDialog = ref(false)
const showAlmacenesDialog = ref(false)
const showCreateAlmacenDialog = ref(false)
const showCambiarEstadoDialog = ref(false)
const editandoObra = ref(false)
const editandoAlmacen = ref(false)
const obraSeleccionada = ref<Obra | null>(null)
const tabActual = ref('general')
const nuevoEstado = ref<EstadoObra>('PLANIFICACION')

// Filters
const filtros = ref({
  busqueda: '',
  estado: null as EstadoObra | null,
  cliente: null as number | null,
  activo: null as boolean | null
})

const estadoOptions = ESTADOS_OBRA.map(estado => ({
  label: getEstadoLabel(estado),
  value: estado
}))

const activoOptions = [
  { label: 'Activo', value: true },
  { label: 'Inactivo', value: false }
]

const monedaOptions = [
  { label: 'Peso Chileno (CLP)', value: 'CLP' },
  { label: 'Dólar (USD)', value: 'USD' },
  { label: 'Euro (EUR)', value: 'EUR' }
]

// Pagination
const paginacion = ref({
  sortBy: 'id_obra',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formObra = ref<ObraCreate & { id_obra?: number }>({
  codigo_obra: '',
  nombre_obra: '',
  descripcion: '',
  id_cliente: 0,
  direccion_obra: '',
  ciudad: '',
  codigo_postal: '',
  supervisor_obra: '',
  contacto_obra: '',
  telefono_obra: '',
  fecha_inicio_programada: '',
  fecha_fin_programada: '',
  fecha_inicio_real: '',
  fecha_fin_real: '',
  valor_contrato: undefined,
  moneda: 'CLP',
  requiere_devolucion_sobrantes: true,
  dias_limite_devolucion: 30,
  estado: 'PLANIFICACION',
  activo: true
})

const formAlmacen = ref<AlmacenObraCreate & { id_almacen?: number }>({
  id_obra: 0,
  nombre_almacen: '',
  descripcion: '',
  direccion: '',
  responsable: '',
  telefono: '',
  tiene_seguridad: false,
  tiene_techo: true,
  capacidad_m3: undefined,
  observaciones: '',
  activo: true
})

// Computed options for selects
const clientesOptions = computed(() => {
  return obraStore.clientes.map(cliente => ({
    label: cliente.nombre_cliente,
    value: cliente.id_cliente
  }))
})

// Table columns for obras
const columnsObras = [
  {
    name: 'codigo_obra',
    required: true,
    label: 'Código',
    align: 'left' as const,
    field: 'codigo_obra',
    sortable: true
  },
  {
    name: 'nombre_obra',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_obra',
    sortable: true
  },
  {
    name: 'estado',
    label: 'Estado',
    align: 'center' as const,
    field: 'estado',
    sortable: true
  },
  {
    name: 'fecha_fin_programada',
    label: 'Fecha Fin',
    align: 'center' as const,
    field: 'fecha_fin_programada',
    sortable: true
  },
  {
    name: 'valor_contrato',
    label: 'Valor',
    align: 'right' as const,
    field: 'valor_contrato',
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

// Table columns for almacenes
const columnsAlmacenes = [
  {
    name: 'nombre_almacen',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_almacen'
  },
  {
    name: 'responsable',
    label: 'Responsable',
    align: 'left' as const,
    field: 'responsable'
  },
  {
    name: 'tiene_seguridad',
    label: 'Seguridad',
    align: 'center' as const,
    field: 'tiene_seguridad'
  },
  {
    name: 'tiene_techo',
    label: 'Techo',
    align: 'center' as const,
    field: 'tiene_techo'
  },
  {
    name: 'activo',
    label: 'Estado',
    align: 'center' as const,
    field: 'activo'
  },
  {
    name: 'actions',
    label: 'Acciones',
    align: 'center' as const,
    field: 'actions'
  }
]

// Methods
const onRequestObras = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarObras()
}

const cargarObras = async () => {
  try {
    isLoading.value = true
    const params: any = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    if (filtros.value.estado) params.estado = filtros.value.estado
    if (filtros.value.activo !== null) params.activo = filtros.value.activo
    if (filtros.value.cliente) params.cliente_id = filtros.value.cliente

    let response = await obraStore.obtenerObras(params)

    // Filtrar por búsqueda en el frontend
    if (filtros.value.busqueda && filtros.value.busqueda.trim()) {
      const busqueda = filtros.value.busqueda.toLowerCase().trim()
      response = response.filter((obra: any) =>
        obra.codigo_obra.toLowerCase().includes(busqueda) ||
        obra.nombre_obra.toLowerCase().includes(busqueda) ||
        (obra.cliente?.nombre_cliente && obra.cliente.nombre_cliente.toLowerCase().includes(busqueda))
      )
    }

    obras.value = response

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar obras',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const buscarObras = async () => {
  paginacion.value.page = 1
  await cargarObras()
}

const abrirFormularioObra = () => {
  resetFormObra()
  showCreateObraDialog.value = true
}

const editarObra = (obra: Obra) => {
  editandoObra.value = true
  formObra.value = {
    ...obra,
    fecha_inicio_programada: obra.fecha_inicio_programada ? formatDateForInput(obra.fecha_inicio_programada) : '',
    fecha_fin_programada: obra.fecha_fin_programada ? formatDateForInput(obra.fecha_fin_programada) : '',
    fecha_inicio_real: obra.fecha_inicio_real ? formatDateForInput(obra.fecha_inicio_real) : '',
    fecha_fin_real: obra.fecha_fin_real ? formatDateForInput(obra.fecha_fin_real) : ''
  }
  showCreateObraDialog.value = true
}

const guardarObra = async () => {
  try {
    isGuardando.value = true

    if (editandoObra.value && formObra.value.id_obra) {
      await obraStore.actualizarObra(formObra.value.id_obra, formObra.value)
      $q.notify({
        type: 'positive',
        message: 'Obra actualizada correctamente'
      })
    } else {
      await obraStore.crearObra(formObra.value)
      $q.notify({
        type: 'positive',
        message: 'Obra creada correctamente'
      })
    }

    showCreateObraDialog.value = false
    resetFormObra()
    await cargarObras()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar obra',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoObra = async (obra: Obra) => {
  try {
    if (obra.activo) {
      await obraStore.eliminarObra(obra.id_obra, false)
      $q.notify({
        type: 'positive',
        message: 'Obra desactivada'
      })
    } else {
      await obraStore.activarObra(obra.id_obra)
      $q.notify({
        type: 'positive',
        message: 'Obra activada'
      })
    }

    await cargarObras()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de obra',
      caption: error.message
    })
  }
}

const eliminarObra = async (obra: Obra) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de eliminar la obra "${obra.nombre_obra}"?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await obraStore.eliminarObra(obra.id_obra, true)
      $q.notify({
        type: 'positive',
        message: 'Obra eliminada correctamente'
      })
      await cargarObras()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar obra',
        caption: error.message
      })
    }
  })
}

const cambiarEstado = (obra: Obra) => {
  obraSeleccionada.value = obra
  nuevoEstado.value = obra.estado as EstadoObra
  showCambiarEstadoDialog.value = true
}

const confirmarCambioEstado = async () => {
  try {
    if (!obraSeleccionada.value) return

    isGuardando.value = true
    await obraStore.cambiarEstadoObra(obraSeleccionada.value.id_obra, nuevoEstado.value)

    $q.notify({
      type: 'positive',
      message: 'Estado de obra cambiado correctamente'
    })

    showCambiarEstadoDialog.value = false
    await cargarObras()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de obra',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const resetFormObra = () => {
  editandoObra.value = false
  tabActual.value = 'general'
  formObra.value = {
    codigo_obra: '',
    nombre_obra: '',
    descripcion: '',
    id_cliente: 0,
    direccion_obra: '',
    ciudad: '',
    codigo_postal: '',
    supervisor_obra: '',
    contacto_obra: '',
    telefono_obra: '',
    fecha_inicio_programada: '',
    fecha_fin_programada: '',
    fecha_inicio_real: '',
    fecha_fin_real: '',
    valor_contrato: undefined,
    moneda: 'CLP',
    requiere_devolucion_sobrantes: true,
    dias_limite_devolucion: 30,
    estado: 'PLANIFICACION',
    activo: true
  }
}

// Almacenes methods
const verAlmacenes = async (obra: Obra) => {
  obraSeleccionada.value = obra
  await cargarAlmacenes(obra.id_obra)
  showAlmacenesDialog.value = true
}

const cargarAlmacenes = async (obraId: number) => {
  try {
    isLoading.value = true
    const response = await obraStore.obtenerAlmacenesPorObra(obraId)
    almacenesObra.value = response
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar almacenes',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const abrirFormularioAlmacen = () => {
  resetFormAlmacen()
  if (obraSeleccionada.value) {
    formAlmacen.value.id_obra = obraSeleccionada.value.id_obra
  }
  showCreateAlmacenDialog.value = true
}

const editarAlmacen = (almacen: AlmacenObra) => {
  editandoAlmacen.value = true
  formAlmacen.value = { ...almacen }
  showCreateAlmacenDialog.value = true
}

const guardarAlmacen = async () => {
  try {
    isGuardando.value = true

    if (editandoAlmacen.value && formAlmacen.value.id_almacen) {
      await obraStore.actualizarAlmacenObra(formAlmacen.value.id_almacen, formAlmacen.value)
      $q.notify({
        type: 'positive',
        message: 'Almacén actualizado correctamente'
      })
    } else {
      await obraStore.crearAlmacenObra(formAlmacen.value)
      $q.notify({
        type: 'positive',
        message: 'Almacén creado correctamente'
      })
    }

    showCreateAlmacenDialog.value = false
    resetFormAlmacen()
    if (obraSeleccionada.value) {
      await cargarAlmacenes(obraSeleccionada.value.id_obra)
    }

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar almacén',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const eliminarAlmacen = async (almacen: AlmacenObra) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de eliminar el almacén "${almacen.nombre_almacen}"?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await obraStore.eliminarAlmacenObra(almacen.id_almacen)
      $q.notify({
        type: 'positive',
        message: 'Almacén eliminado correctamente'
      })
      if (obraSeleccionada.value) {
        await cargarAlmacenes(obraSeleccionada.value.id_obra)
      }
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar almacén',
        caption: error.message
      })
    }
  })
}

const resetFormAlmacen = () => {
  editandoAlmacen.value = false
  formAlmacen.value = {
    id_obra: obraSeleccionada.value?.id_obra || 0,
    nombre_almacen: '',
    descripcion: '',
    direccion: '',
    responsable: '',
    telefono: '',
    tiene_seguridad: false,
    tiene_techo: true,
    capacidad_m3: undefined,
    observaciones: '',
    activo: true
  }
}

// Helper functions
function getEstadoColor(estado?: string): string {
  switch (estado) {
    case 'PLANIFICACION': return 'blue'
    case 'EN_EJECUCION': return 'green'
    case 'SUSPENDIDA': return 'orange'
    case 'FINALIZADA': return 'purple'
    case 'CANCELADA': return 'red'
    default: return 'grey'
  }
}

function getEstadoLabel(estado?: string): string {
  switch (estado) {
    case 'PLANIFICACION': return 'Planificación'
    case 'EN_EJECUCION': return 'En Ejecución'
    case 'SUSPENDIDA': return 'Suspendida'
    case 'FINALIZADA': return 'Finalizada'
    case 'CANCELADA': return 'Cancelada'
    default: return estado || 'Sin Estado'
  }
}

const formatCurrency = (value?: number, currency = 'CLP') => {
  if (!value) return '-'
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: currency
  }).format(value)
}

const formatDate = (dateString?: string) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('es-CL')
}

const formatDateForInput = (dateString: string) => {
  return dateString.split('T')[0]
}

const isObraRetrasada = (obra: Obra): boolean => {
  if (!obra.fecha_fin_programada || obra.estado === 'FINALIZADA') return false
  const fechaFin = new Date(obra.fecha_fin_programada)
  const hoy = new Date()
  return fechaFin < hoy && obra.estado === 'EN_EJECUCION'
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    obraStore.obtenerClientes(),
    cargarObras()
  ])
})
</script>