<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-xl">
        <div>
          <div class="row items-center q-mb-sm">
            <q-icon name="label" size="32px" color="primary" class="q-mr-md" />
            <div>
              <h4 class="q-my-none text-h4 text-weight-light">Tipos de <span class="text-weight-bold text-primary">Productos</span></h4>
              <p class="text-grey-6 q-mb-none text-body2">Clasificación de productos por tipo y características</p>
            </div>
          </div>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nuevo Tipo"
          @click="abrirFormularioTipo"
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
            <div class="col-12 col-md-3">
              <q-select
                v-model="filtros.subcategoria"
                :options="subcategoriasOptions"
                label="Subcategoría"
                outlined
                dense
                clearable
                emit-value
                map-options
                option-value="value"
                option-label="label"
              />
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
            <div class="col-12 col-md-3 row q-gutter-sm justify-end items-center">
              <q-btn color="primary" icon="search" label="Buscar" @click="buscarTipos" unelevated no-caps />
              <q-btn color="grey-6" icon="clear" label="Limpiar" @click="limpiarFiltros" flat no-caps />
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Tipos de Producto Table -->
      <q-table
        :rows="tiposFiltrados"
        :columns="columnsTipos"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_tipo_producto"
        flat
        bordered
        @request="onRequestTipos"
      >
        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'green' : 'red'"
              :label="props.value ? 'Activo' : 'Inactivo'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-subcategoria="props">
          <q-td :props="props">
            <div class="column">
              <span class="text-weight-medium">{{ getSubcategoriaNombre(props.row.id_subcategoria) }}</span>
              <span class="text-caption text-grey-6">{{ getCategoriaNombre(props.row.id_subcategoria) }}</span>
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
              @click="editarTipo(props.row as TipoProducto)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'negative' : 'positive'"
              size="sm"
              @click="toggleEstadoTipo(props.row as TipoProducto)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="delete"
              color="negative"
              size="sm"
              @click="eliminarTipo(props.row as TipoProducto)"
            >
              <q-tooltip>Eliminar</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Tipo Dialog -->
      <q-dialog v-model="showCreateTipoDialog" persistent>
        <q-card style="min-width: 600px; max-width: 800px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoTipo ? 'Editar' : 'Nuevo' }} Tipo de Producto</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarTipo">
              <div class="row q-gutter-md">
                <div class="col-12">
                  <q-select
                    v-model="formTipo.id_subcategoria"
                    :options="subcategoriasOptions"
                    label="Subcategoría *"
                    outlined
                    dense
                    emit-value
                    map-options
                    option-value="value"
                    option-label="label"
                    :rules="[val => !!val || 'La subcategoría es requerida']"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formTipo.codigo_tipo"
                    label="Código *"
                    outlined
                    dense
                    maxlength="10"
                    :rules="[val => !!val || 'El código es requerido']"
                    hint="Ej: ION, UPR, etc."
                  />
                </div>
                <div class="col-12 col-md-7">
                  <q-input
                    v-model="formTipo.nombre_tipo"
                    label="Nombre *"
                    outlined
                    dense
                    maxlength="100"
                    :rules="[val => !!val || 'El nombre es requerido']"
                    hint="Ej: Detector Iónico, Rociador Upright"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formTipo.descripcion"
                    label="Descripción"
                    outlined
                    type="textarea"
                    rows="3"
                    hint="Especificaciones técnicas del tipo de producto"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-toggle
                    v-model="formTipo.activo"
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
              @click="guardarTipo"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Estadísticas -->
      <q-card flat bordered class="q-mt-md" v-if="estadisticas">
        <q-card-section>
          <div class="text-h6 q-mb-md">Estadísticas</div>
          <div class="row q-gutter-md">
            <div class="col">
              <q-stat
                :value="estadisticas.total"
                label="Total"
                color="primary"
                icon="inventory_2"
              />
            </div>
            <div class="col">
              <q-stat
                :value="estadisticas.activos"
                label="Activos"
                color="positive"
                icon="check_circle"
              />
            </div>
            <div class="col">
              <q-stat
                :value="estadisticas.inactivos"
                label="Inactivos"
                color="negative"
                icon="cancel"
              />
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import {
  useTipoProductoStore,
  type TipoProducto,
  type TipoProductoCreate
} from '../stores/tiposProducto'
import {
  useCategoriaStore,
  type Subcategoria
} from '../stores/categorias'

const $q = useQuasar()
const tipoProductoStore = useTipoProductoStore()
const categoriaStore = useCategoriaStore()

// Reactive data
const tiposProducto = ref<TipoProducto[]>([])
const subcategorias = ref<Subcategoria[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const showCreateTipoDialog = ref(false)
const editandoTipo = ref(false)
const estadisticas = ref<{
  total: number
  activos: number
  inactivos: number
} | null>(null)

// Filters
const filtros = ref({
  busqueda: '',
  subcategoria: null as number | null,
  estado: null as boolean | null
})

const estadoOptions = [
  { label: 'Activo', value: true },
  { label: 'Inactivo', value: false }
]

// Pagination
const paginacion = ref({
  sortBy: 'id_tipo_producto',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formTipo = ref<TipoProductoCreate & { id_tipo_producto?: number }>({
  id_subcategoria: 0,
  codigo_tipo: '',
  nombre_tipo: '',
  descripcion: '',
  activo: true
})

// Computed
const subcategoriasOptions = computed(() => {
  return subcategorias.value.map(sub => ({
    label: `${sub.codigo_subcategoria} - ${sub.nombre_subcategoria} (${sub.categoria?.nombre_categoria || ''})`,
    value: sub.id_subcategoria
  }))
})

const tiposFiltrados = computed(() => {
  let resultado = [...tiposProducto.value]

  // Filtrar por búsqueda
  if (filtros.value.busqueda && filtros.value.busqueda.trim()) {
    const busqueda = filtros.value.busqueda.toLowerCase().trim()
    resultado = resultado.filter(tipo =>
      tipo.codigo_tipo.toLowerCase().includes(busqueda) ||
      tipo.nombre_tipo.toLowerCase().includes(busqueda) ||
      (tipo.descripcion && tipo.descripcion.toLowerCase().includes(busqueda))
    )
  }

  // Filtrar por subcategoría
  if (filtros.value.subcategoria !== null) {
    resultado = resultado.filter(tipo => tipo.id_subcategoria === filtros.value.subcategoria)
  }

  // Filtrar por estado
  if (filtros.value.estado !== null) {
    resultado = resultado.filter(tipo => tipo.activo === filtros.value.estado)
  }

  return resultado
})

// Table columns
const columnsTipos = [
  {
    name: 'codigo_tipo',
    required: true,
    label: 'Código',
    align: 'left' as const,
    field: 'codigo_tipo',
    sortable: true
  },
  {
    name: 'nombre_tipo',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_tipo',
    sortable: true
  },
  {
    name: 'subcategoria',
    label: 'Subcategoría',
    align: 'left' as const,
    field: 'id_subcategoria'
  },
  {
    name: 'descripcion',
    label: 'Descripción',
    align: 'left' as const,
    field: 'descripcion'
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
const onRequestTipos = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarTipos()
}

const cargarTipos = async () => {
  try {
    isLoading.value = true
    const params = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    const response = await tipoProductoStore.obtenerTiposProducto(params)
    tiposProducto.value = response

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar tipos de producto',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const cargarSubcategorias = async () => {
  try {
    const response = await categoriaStore.obtenerSubcategorias()
    subcategorias.value = response
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar subcategorías',
      caption: error.message
    })
  }
}

const cargarEstadisticas = async () => {
  try {
    estadisticas.value = await tipoProductoStore.obtenerEstadisticas()
  } catch (error: any) {
    console.error('Error al cargar estadísticas:', error)
  }
}

const buscarTipos = async () => {
  paginacion.value.page = 1
  await cargarTipos()
}

const limpiarFiltros = () => {
  filtros.value.busqueda = ''
  filtros.value.subcategoria = null
  filtros.value.estado = null
  buscarTipos()
}

const abrirFormularioTipo = () => {
  resetFormTipo()
  showCreateTipoDialog.value = true
}

const editarTipo = (tipo: TipoProducto) => {
  editandoTipo.value = true
  formTipo.value = { ...tipo }
  showCreateTipoDialog.value = true
}

const guardarTipo = async () => {
  try {
    isGuardando.value = true

    if (editandoTipo.value && formTipo.value.id_tipo_producto) {
      await tipoProductoStore.actualizarTipoProducto(formTipo.value.id_tipo_producto, formTipo.value)
      $q.notify({
        type: 'positive',
        message: 'Tipo de producto actualizado correctamente'
      })
    } else {
      await tipoProductoStore.crearTipoProducto(formTipo.value)
      $q.notify({
        type: 'positive',
        message: 'Tipo de producto creado correctamente'
      })
    }

    showCreateTipoDialog.value = false
    resetFormTipo()
    await cargarTipos()
    await cargarEstadisticas()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar tipo de producto',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoTipo = async (tipo: TipoProducto) => {
  try {
    if (tipo.activo) {
      // Desactivar (eliminar con soft delete)
      await tipoProductoStore.eliminarTipoProducto(tipo.id_tipo_producto, false)
      $q.notify({
        type: 'positive',
        message: 'Tipo de producto desactivado'
      })
    } else {
      // Activar
      await tipoProductoStore.activarTipoProducto(tipo.id_tipo_producto)
      $q.notify({
        type: 'positive',
        message: 'Tipo de producto activado'
      })
    }

    await cargarTipos()
    await cargarEstadisticas()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado del tipo de producto',
      caption: error.message
    })
  }
}

const eliminarTipo = async (tipo: TipoProducto) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de eliminar el tipo de producto "${tipo.nombre_tipo}"? Esta acción lo marcará como inactivo.`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await tipoProductoStore.eliminarTipoProducto(tipo.id_tipo_producto, false)
      $q.notify({
        type: 'positive',
        message: 'Tipo de producto eliminado correctamente'
      })
      await cargarTipos()
      await cargarEstadisticas()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar tipo de producto',
        caption: error.message
      })
    }
  })
}

const resetFormTipo = () => {
  editandoTipo.value = false
  formTipo.value = {
    id_subcategoria: 0,
    codigo_tipo: '',
    nombre_tipo: '',
    descripcion: '',
    activo: true
  }
}

// Helper methods
const getSubcategoriaNombre = (subcategoriaId: number): string => {
  const subcategoria = subcategorias.value.find(s => s.id_subcategoria === subcategoriaId)
  return subcategoria ? `${subcategoria.codigo_subcategoria} - ${subcategoria.nombre_subcategoria}` : 'N/A'
}

const getCategoriaNombre = (subcategoriaId: number): string => {
  const subcategoria = subcategorias.value.find(s => s.id_subcategoria === subcategoriaId)
  return subcategoria?.categoria?.nombre_categoria || 'N/A'
}

// Lifecycle
onMounted(async () => {
  await cargarSubcategorias()
  await cargarTipos()
  await cargarEstadisticas()
})
</script>