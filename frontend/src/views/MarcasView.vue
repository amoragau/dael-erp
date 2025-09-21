<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Gestión de Marcas</h4>
          <p class="text-grey-7 q-mb-none">Administra fabricantes y sus datos de contacto técnico</p>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nueva Marca"
          @click="abrirFormularioMarca"
        />
      </div>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-gutter-md items-center">
            <q-input
              v-model="filtros.busqueda"
              placeholder="Buscar por nombre, país o contacto..."
              outlined
              dense
              clearable
              style="min-width: 350px"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
            <q-input
              v-model="filtros.pais"
              placeholder="Filtrar por país..."
              outlined
              dense
              clearable
              style="min-width: 200px"
            >
              <template v-slot:prepend>
                <q-icon name="flag" />
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
            <q-btn
              color="primary"
              icon="search"
              label="Buscar"
              @click="buscarMarcas"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Marcas Table -->
      <q-table
        :rows="marcasFiltradas"
        :columns="columnsMarcas"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_marca"
        flat
        bordered
        @request="onRequestMarcas"
      >
        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'green' : 'red'"
              :label="props.value ? 'Activa' : 'Inactiva'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-sitio_web="props">
          <q-td :props="props">
            <a
              v-if="props.value"
              :href="formatearUrl(props.value)"
              target="_blank"
              rel="noopener noreferrer"
              class="text-primary"
            >
              {{ props.value }}
              <q-icon name="open_in_new" size="xs" class="q-ml-xs" />
            </a>
            <span v-else class="text-grey-5">-</span>
          </q-td>
        </template>

        <template v-slot:body-cell-contacto_tecnico="props">
          <q-td :props="props">
            <div v-if="props.value" class="column">
              <span>{{ props.value }}</span>
              <q-btn
                v-if="esEmail(props.value)"
                flat
                dense
                size="sm"
                icon="email"
                color="primary"
                @click="enviarEmail(props.value)"
                class="q-mt-xs"
              >
                <q-tooltip>Enviar email</q-tooltip>
              </q-btn>
            </div>
            <span v-else class="text-grey-5">-</span>
          </q-td>
        </template>

        <template v-slot:body-cell-fecha_creacion="props">
          <q-td :props="props">
            {{ formatearFecha(props.value) }}
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
              @click="editarMarca(props.row as Marca)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'negative' : 'positive'"
              size="sm"
              @click="toggleEstadoMarca(props.row as Marca)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="delete"
              color="negative"
              size="sm"
              @click="eliminarMarca(props.row as Marca)"
            >
              <q-tooltip>Eliminar</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Marca Dialog -->
      <q-dialog v-model="showCreateMarcaDialog" persistent>
        <q-card style="min-width: 700px; max-width: 900px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoMarca ? 'Editar' : 'Nueva' }} Marca</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarMarca">
              <div class="row q-gutter-md">
                <div class="col-12 col-md-7">
                  <q-input
                    v-model="formMarca.nombre_marca"
                    label="Nombre de la Marca *"
                    outlined
                    dense
                    maxlength="100"
                    :rules="[val => !!val || 'El nombre es requerido']"
                    hint="Ej: Honeywell, Siemens, Johnson Controls"
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formMarca.pais_origen"
                    label="País de Origen"
                    outlined
                    dense
                    maxlength="50"
                    hint="Ej: Estados Unidos, Alemania"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formMarca.descripcion"
                    label="Descripción"
                    outlined
                    type="textarea"
                    rows="3"
                    hint="Información general sobre el fabricante"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formMarca.sitio_web"
                    label="Sitio Web"
                    outlined
                    dense
                    maxlength="200"
                    hint="Ej: www.honeywell.com"
                    :rules="[validarUrl]"
                  >
                    <template v-slot:prepend>
                      <q-icon name="language" />
                    </template>
                  </q-input>
                </div>
                <div class="col-12 col-md-5">
                  <q-input
                    v-model="formMarca.contacto_tecnico"
                    label="Contacto Técnico"
                    outlined
                    dense
                    maxlength="200"
                    hint="Email o teléfono de soporte técnico"
                    :rules="[validarContacto]"
                  >
                    <template v-slot:prepend>
                      <q-icon name="support_agent" />
                    </template>
                  </q-input>
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-toggle
                    v-model="formMarca.activo"
                    label="Activa"
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
              @click="guardarMarca"
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
                label="Total Marcas"
                color="primary"
                icon="business"
              />
            </div>
            <div class="col">
              <q-stat
                :value="estadisticas.activas"
                label="Activas"
                color="positive"
                icon="check_circle"
              />
            </div>
            <div class="col">
              <q-stat
                :value="estadisticas.inactivas"
                label="Inactivas"
                color="negative"
                icon="cancel"
              />
            </div>
            <div class="col">
              <q-stat
                :value="marcasConSitioWeb"
                label="Con Sitio Web"
                color="info"
                icon="language"
              />
            </div>
            <div class="col">
              <q-stat
                :value="marcasConContacto"
                label="Con Contacto"
                color="accent"
                icon="support_agent"
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
  useMarcaStore,
  type Marca,
  type MarcaCreate
} from '../stores/marcas'

const $q = useQuasar()
const marcaStore = useMarcaStore()

// Reactive data
const marcas = ref<Marca[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const showCreateMarcaDialog = ref(false)
const editandoMarca = ref(false)
const estadisticas = ref<{
  total: number
  activas: number
  inactivas: number
} | null>(null)

// Filters
const filtros = ref({
  busqueda: '',
  pais: '',
  estado: null as boolean | null
})

const estadoOptions = [
  { label: 'Activa', value: true },
  { label: 'Inactiva', value: false }
]

// Pagination
const paginacion = ref({
  sortBy: 'nombre_marca',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formMarca = ref<MarcaCreate & { id_marca?: number }>({
  nombre_marca: '',
  descripcion: '',
  pais_origen: '',
  sitio_web: '',
  contacto_tecnico: '',
  activo: true
})

// Computed
const marcasFiltradas = computed(() => {
  let resultado = [...marcas.value]

  // Filtrar por búsqueda
  if (filtros.value.busqueda && filtros.value.busqueda.trim()) {
    const busqueda = filtros.value.busqueda.toLowerCase().trim()
    resultado = resultado.filter(marca =>
      marca.nombre_marca.toLowerCase().includes(busqueda) ||
      (marca.pais_origen && marca.pais_origen.toLowerCase().includes(busqueda)) ||
      (marca.contacto_tecnico && marca.contacto_tecnico.toLowerCase().includes(busqueda)) ||
      (marca.descripcion && marca.descripcion.toLowerCase().includes(busqueda))
    )
  }

  // Filtrar por país
  if (filtros.value.pais && filtros.value.pais.trim()) {
    const pais = filtros.value.pais.toLowerCase().trim()
    resultado = resultado.filter(marca =>
      marca.pais_origen && marca.pais_origen.toLowerCase().includes(pais)
    )
  }

  // Filtrar por estado
  if (filtros.value.estado !== null) {
    resultado = resultado.filter(marca => marca.activo === filtros.value.estado)
  }

  return resultado
})

const marcasConSitioWeb = computed(() => {
  return marcas.value.filter(m => m.sitio_web && m.sitio_web.trim()).length
})

const marcasConContacto = computed(() => {
  return marcas.value.filter(m => m.contacto_tecnico && m.contacto_tecnico.trim()).length
})

// Table columns
const columnsMarcas = [
  {
    name: 'nombre_marca',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_marca',
    sortable: true
  },
  {
    name: 'pais_origen',
    label: 'País',
    align: 'left' as const,
    field: 'pais_origen',
    sortable: true
  },
  {
    name: 'sitio_web',
    label: 'Sitio Web',
    align: 'left' as const,
    field: 'sitio_web'
  },
  {
    name: 'contacto_tecnico',
    label: 'Contacto Técnico',
    align: 'left' as const,
    field: 'contacto_tecnico'
  },
  {
    name: 'fecha_creacion',
    label: 'Fecha Creación',
    align: 'center' as const,
    field: 'fecha_creacion',
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
const onRequestMarcas = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarMarcas()
}

const cargarMarcas = async () => {
  try {
    isLoading.value = true
    const params = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    const response = await marcaStore.obtenerMarcas(params)
    marcas.value = response

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar marcas',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const cargarEstadisticas = async () => {
  try {
    estadisticas.value = await marcaStore.obtenerEstadisticas()
  } catch (error: any) {
    console.error('Error al cargar estadísticas:', error)
  }
}

const buscarMarcas = async () => {
  paginacion.value.page = 1
  await cargarMarcas()
}

const abrirFormularioMarca = () => {
  resetFormMarca()
  showCreateMarcaDialog.value = true
}

const editarMarca = (marca: Marca) => {
  editandoMarca.value = true
  formMarca.value = { ...marca }
  showCreateMarcaDialog.value = true
}

const guardarMarca = async () => {
  try {
    isGuardando.value = true

    if (editandoMarca.value && formMarca.value.id_marca) {
      await marcaStore.actualizarMarca(formMarca.value.id_marca, formMarca.value)
      $q.notify({
        type: 'positive',
        message: 'Marca actualizada correctamente'
      })
    } else {
      await marcaStore.crearMarca(formMarca.value)
      $q.notify({
        type: 'positive',
        message: 'Marca creada correctamente'
      })
    }

    showCreateMarcaDialog.value = false
    resetFormMarca()
    await cargarMarcas()
    await cargarEstadisticas()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar marca',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoMarca = async (marca: Marca) => {
  try {
    await marcaStore.toggleEstadoMarca(marca.id_marca)

    const nuevoEstado = !marca.activo
    $q.notify({
      type: 'positive',
      message: `Marca ${nuevoEstado ? 'activada' : 'desactivada'}`
    })

    await cargarMarcas()
    await cargarEstadisticas()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de marca',
      caption: error.message
    })
  }
}

const eliminarMarca = async (marca: Marca) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de eliminar la marca "${marca.nombre_marca}"? Esta acción la marcará como inactiva.`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await marcaStore.eliminarMarca(marca.id_marca)
      $q.notify({
        type: 'positive',
        message: 'Marca eliminada correctamente'
      })
      await cargarMarcas()
      await cargarEstadisticas()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar marca',
        caption: error.message
      })
    }
  })
}

const resetFormMarca = () => {
  editandoMarca.value = false
  formMarca.value = {
    nombre_marca: '',
    descripcion: '',
    pais_origen: '',
    sitio_web: '',
    contacto_tecnico: '',
    activo: true
  }
}

// Helper methods
const formatearUrl = (url: string): string => {
  if (!url) return ''
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  return `https://${url}`
}

const formatearFecha = (fecha: string): string => {
  if (!fecha) return '-'
  return new Date(fecha).toLocaleDateString('es-ES')
}

const esEmail = (contacto: string): boolean => {
  if (!contacto) return false
  return contacto.includes('@') && contacto.includes('.')
}

const enviarEmail = (email: string) => {
  window.open(`mailto:${email}`, '_blank')
}

// Validation methods
const validarUrl = (val: string): boolean | string => {
  if (!val) return true
  const urlPattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/
  return urlPattern.test(val) || 'Formato de URL inválido'
}

const validarContacto = (val: string): boolean | string => {
  if (!val) return true

  // Validar email
  if (val.includes('@')) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailPattern.test(val) || 'Formato de email inválido'
  }

  // Validar teléfono (formato básico)
  if (/^\+?\d[\d\s\-\(\)]{7,}$/.test(val)) {
    return true
  }

  return 'Formato de contacto inválido (email o teléfono)'
}

// Lifecycle
onMounted(async () => {
  await cargarMarcas()
  await cargarEstadisticas()
})
</script>