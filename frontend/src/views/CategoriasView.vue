<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Gestión de Categorías</h4>
          <p class="text-grey-7 q-mb-none">Administra las categorías y subcategorías del sistema</p>
        </div>
        <div class="q-gutter-sm">
          <q-btn
            color="secondary"
            icon="category"
            label="Nueva Subcategoría"
            @click="showCreateSubcategoriaDialog = true"
          />
          <q-btn
            color="primary"
            icon="add"
            label="Nueva Categoría"
            @click="showCreateCategoriaDialog = true"
          />
        </div>
      </div>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-gutter-md items-center">
            <q-input
              v-model="filtros.busqueda"
              placeholder="Buscar por nombre o código..."
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
              style="min-width: 150px"
            />
            <q-btn
              color="primary"
              icon="search"
              label="Buscar"
              @click="buscarCategorias"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Categories Table -->
      <q-table
        :rows="categorias"
        :columns="columnsCategorias"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_categoria"
        flat
        bordered
        @request="onRequestCategorias"
      >
        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'green' : 'red'"
              :label="props.value ? 'Activo' : 'Inactivo'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-subcategorias="props">
          <q-td :props="props">
            <q-btn
              flat
              dense
              color="secondary"
              :label="`Ver (${getSubcategoriasCount(props.row.id_categoria)})`"
              @click="verSubcategorias(props.row as Categoria)"
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
              @click="editarCategoria(props.row)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'negative' : 'positive'"
              size="sm"
              @click="toggleEstadoCategoria(props.row)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="delete"
              color="negative"
              size="sm"
              @click="eliminarCategoria(props.row)"
            >
              <q-tooltip>Eliminar</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Subcategorias Dialog -->
      <q-dialog v-model="showSubcategoriasDialog" maximized>
        <q-card>
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Subcategorías de: {{ categoriaSeleccionada?.nombre }}</div>
            <q-space />
            <q-btn
              color="primary"
              icon="add"
              label="Nueva Subcategoría"
              @click="showCreateSubcategoriaDialog = true"
            />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-table
              :rows="subcategorias"
              :columns="columnsSubcategorias"
              :loading="isLoadingSubcategorias"
              row-key="id_subcategoria"
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

              <template v-slot:body-cell-actions="props">
                <q-td :props="props">
                  <q-btn
                    flat
                    round
                    icon="edit"
                    color="primary"
                    size="sm"
                    @click="editarSubcategoria(props.row)"
                  >
                    <q-tooltip>Editar</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    round
                    :icon="props.row.activo ? 'block' : 'check_circle'"
                    :color="props.row.activo ? 'negative' : 'positive'"
                    size="sm"
                    @click="toggleEstadoSubcategoria(props.row)"
                  >
                    <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    round
                    icon="delete"
                    color="negative"
                    size="sm"
                    @click="eliminarSubcategoria(props.row)"
                  >
                    <q-tooltip>Eliminar</q-tooltip>
                  </q-btn>
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- Create/Edit Categoria Dialog -->
      <q-dialog v-model="showCreateCategoriaDialog" persistent>
        <q-card style="min-width: 400px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoCategoria ? 'Editar' : 'Nueva' }} Categoría</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarCategoria">
              <q-input
                v-model="formCategoria.codigo"
                label="Código *"
                outlined
                dense
                :rules="[val => !!val || 'El código es requerido']"
              />
              <q-input
                v-model="formCategoria.nombre"
                label="Nombre *"
                outlined
                dense
                class="q-mt-md"
                :rules="[val => !!val || 'El nombre es requerido']"
              />
              <q-input
                v-model="formCategoria.descripcion"
                label="Descripción"
                outlined
                type="textarea"
                rows="3"
                class="q-mt-md"
              />
              <q-toggle
                v-model="formCategoria.activo"
                label="Activo"
                class="q-mt-md"
              />
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar"
              @click="guardarCategoria"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Create/Edit Subcategoria Dialog -->
      <q-dialog v-model="showCreateSubcategoriaDialog" persistent>
        <q-card style="min-width: 400px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoSubcategoria ? 'Editar' : 'Nueva' }} Subcategoría</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarSubcategoria">
              <q-select
                v-model="formSubcategoria.id_categoria"
                :options="categoriasOptions"
                label="Categoría *"
                outlined
                dense
                option-value="value"
                option-label="label"
                emit-value
                map-options
                :rules="[(val: any) => !!val || 'La categoría es requerida']"
              />
              <q-input
                v-model="formSubcategoria.codigo_subcategoria"
                label="Código *"
                outlined
                dense
                class="q-mt-md"
                :rules="[val => !!val || 'El código es requerido']"
              />
              <q-input
                v-model="formSubcategoria.nombre_subcategoria"
                label="Nombre *"
                outlined
                dense
                class="q-mt-md"
                :rules="[val => !!val || 'El nombre es requerido']"
              />
              <q-input
                v-model="formSubcategoria.descripcion"
                label="Descripción"
                outlined
                type="textarea"
                rows="3"
                class="q-mt-md"
              />
              <q-toggle
                v-model="formSubcategoria.activo"
                label="Activo"
                class="q-mt-md"
              />
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar"
              @click="guardarSubcategoria"
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
import { useCategoriaStore, type Categoria, type Subcategoria, type CategoriaCreate, type SubcategoriaCreate } from '../stores/categorias'

const $q = useQuasar()
const categoriaStore = useCategoriaStore()

// Reactive data
const categorias = ref<Categoria[]>([])
const subcategorias = ref<Subcategoria[]>([])
const isLoading = ref(false)
const isLoadingSubcategorias = ref(false)
const isGuardando = ref(false)
const showCreateCategoriaDialog = ref(false)
const showCreateSubcategoriaDialog = ref(false)
const showSubcategoriasDialog = ref(false)
const editandoCategoria = ref(false)
const editandoSubcategoria = ref(false)
const categoriaSeleccionada = ref<Categoria | null>(null)

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
  sortBy: 'id_categoria',
  descending: false,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
})

// Forms
const formCategoria = ref<CategoriaCreate & { id_categoria?: number }>({
  codigo: '',
  nombre: '',
  descripcion: '',
  activo: true
})

const formSubcategoria = ref<Omit<SubcategoriaCreate, 'id_categoria'> & { id_categoria: number | null; id_subcategoria?: number }>({
  id_categoria: null as number | null,
  codigo_subcategoria: '',
  nombre_subcategoria: '',
  descripcion: '',
  activo: true
})

// Table columns
const columnsCategorias = [
  {
    name: 'codigo',
    required: true,
    label: 'Código',
    align: 'left' as const,
    field: 'codigo',
    sortable: true
  },
  {
    name: 'nombre',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre',
    sortable: true
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
    name: 'subcategorias',
    label: 'Subcategorías',
    align: 'center' as const,
    field: 'subcategorias'
  },
  {
    name: 'actions',
    label: 'Acciones',
    align: 'center' as const,
    field: 'actions'
  }
]

const columnsSubcategorias = [
  {
    name: 'codigo_subcategoria',
    required: true,
    label: 'Código',
    align: 'left' as const,
    field: 'codigo_subcategoria',
    sortable: true
  },
  {
    name: 'nombre_subcategoria',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_subcategoria',
    sortable: true
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

// Computed
const categoriasOptions = computed(() => {
  return categorias.value
    .filter(cat => cat.activo)
    .map(cat => ({
      value: cat.id_categoria,
      label: `${cat.codigo} - ${cat.nombre}`
    }))
})

// Methods
const onRequestCategorias = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarCategorias()
}

const cargarCategorias = async () => {
  try {
    isLoading.value = true
    const params: any = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    if (filtros.value.estado !== null) {
      params.activo = filtros.value.estado
    }

    const response = await categoriaStore.obtenerCategorias(params)
    categorias.value = response

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar categorías',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const buscarCategorias = async () => {
  paginacion.value.page = 1
  await cargarCategorias()
}

const verSubcategorias = async (categoria: Categoria) => {
  try {
    categoriaSeleccionada.value = categoria
    isLoadingSubcategorias.value = true
    showSubcategoriasDialog.value = true

    const response = await categoriaStore.obtenerSubcategoriasPorCategoria(categoria.id_categoria)
    subcategorias.value = response

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar subcategorías',
      caption: error.message
    })
  } finally {
    isLoadingSubcategorias.value = false
  }
}

const getSubcategoriasCount = (idCategoria: number) => {
  // En una implementación real, esto vendría del backend
  return 0
}

const editarCategoria = (categoria: Categoria) => {
  editandoCategoria.value = true
  formCategoria.value = { ...categoria }
  showCreateCategoriaDialog.value = true
}

const editarSubcategoria = (subcategoria: Subcategoria) => {
  editandoSubcategoria.value = true
  formSubcategoria.value = { ...subcategoria }
  showCreateSubcategoriaDialog.value = true
}

const guardarCategoria = async () => {
  try {
    isGuardando.value = true

    if (editandoCategoria.value && formCategoria.value.id_categoria) {
      await categoriaStore.actualizarCategoria(formCategoria.value.id_categoria, formCategoria.value)
      $q.notify({
        type: 'positive',
        message: 'Categoría actualizada correctamente'
      })
    } else {
      await categoriaStore.crearCategoria(formCategoria.value)
      $q.notify({
        type: 'positive',
        message: 'Categoría creada correctamente'
      })
    }

    showCreateCategoriaDialog.value = false
    resetFormCategoria()
    await cargarCategorias()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar categoría',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const guardarSubcategoria = async () => {
  try {
    isGuardando.value = true

    if (editandoSubcategoria.value && formSubcategoria.value.id_subcategoria) {
      await categoriaStore.actualizarSubcategoria(formSubcategoria.value.id_subcategoria, formSubcategoria.value)
      $q.notify({
        type: 'positive',
        message: 'Subcategoría actualizada correctamente'
      })
    } else if (formSubcategoria.value.id_categoria) {
      await categoriaStore.crearSubcategoria({
        id_categoria: formSubcategoria.value.id_categoria,
        codigo_subcategoria: formSubcategoria.value.codigo_subcategoria,
        nombre_subcategoria: formSubcategoria.value.nombre_subcategoria,
        descripcion: formSubcategoria.value.descripcion,
        activo: formSubcategoria.value.activo
      })
      $q.notify({
        type: 'positive',
        message: 'Subcategoría creada correctamente'
      })
    }

    showCreateSubcategoriaDialog.value = false
    resetFormSubcategoria()

    if (showSubcategoriasDialog.value && categoriaSeleccionada.value) {
      await verSubcategorias(categoriaSeleccionada.value)
    }

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar subcategoría',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoCategoria = async (categoria: Categoria) => {
  try {
    if (categoria.activo) {
      await categoriaStore.eliminarCategoria(categoria.id_categoria, false)
      $q.notify({
        type: 'positive',
        message: 'Categoría desactivada'
      })
    } else {
      await categoriaStore.activarCategoria(categoria.id_categoria)
      $q.notify({
        type: 'positive',
        message: 'Categoría activada'
      })
    }

    await cargarCategorias()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de categoría',
      caption: error.message
    })
  }
}

const toggleEstadoSubcategoria = async (subcategoria: Subcategoria) => {
  try {
    if (subcategoria.activo) {
      await categoriaStore.eliminarSubcategoria(subcategoria.id_subcategoria, false)
      $q.notify({
        type: 'positive',
        message: 'Subcategoría desactivada'
      })
    } else {
      await categoriaStore.activarSubcategoria(subcategoria.id_subcategoria)
      $q.notify({
        type: 'positive',
        message: 'Subcategoría activada'
      })
    }

    if (categoriaSeleccionada.value) {
      await verSubcategorias(categoriaSeleccionada.value)
    }

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de subcategoría',
      caption: error.message
    })
  }
}

const eliminarCategoria = async (categoria: Categoria) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de eliminar la categoría "${categoria.nombre}"?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await categoriaStore.eliminarCategoria(categoria.id_categoria, true)
      $q.notify({
        type: 'positive',
        message: 'Categoría eliminada correctamente'
      })
      await cargarCategorias()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar categoría',
        caption: error.message
      })
    }
  })
}

const eliminarSubcategoria = async (subcategoria: Subcategoria) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de eliminar la subcategoría "${subcategoria.nombre_subcategoria}"?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await categoriaStore.eliminarSubcategoria(subcategoria.id_subcategoria, true)
      $q.notify({
        type: 'positive',
        message: 'Subcategoría eliminada correctamente'
      })

      if (categoriaSeleccionada.value) {
        await verSubcategorias(categoriaSeleccionada.value)
      }
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar subcategoría',
        caption: error.message
      })
    }
  })
}

const resetFormCategoria = () => {
  editandoCategoria.value = false
  formCategoria.value = {
    codigo: '',
    nombre: '',
    descripcion: '',
    activo: true
  }
}

const resetFormSubcategoria = () => {
  editandoSubcategoria.value = false
  formSubcategoria.value = {
    id_categoria: categoriaSeleccionada.value?.id_categoria || null,
    codigo_subcategoria: '',
    nombre_subcategoria: '',
    descripcion: '',
    activo: true
  }
}

// Lifecycle
onMounted(() => {
  cargarCategorias()
})
</script>