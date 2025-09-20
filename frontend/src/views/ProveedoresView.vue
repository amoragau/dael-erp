<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Gestión de Proveedores</h4>
          <p class="text-grey-7 q-mb-none">Administra los proveedores del sistema</p>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nuevo Proveedor"
          @click="abrirFormularioProveedor"
        />
      </div>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-gutter-md items-center">
            <q-input
              v-model="filtros.busqueda"
              placeholder="Buscar por nombre, código o RUT..."
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
            <q-btn
              color="primary"
              icon="search"
              label="Buscar"
              @click="buscarProveedores"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Providers Table -->
      <q-table
        :rows="proveedores"
        :columns="columnsProveedores"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_proveedor"
        flat
        bordered
        @request="onRequestProveedores"
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
              @click="editarProveedor(props.row as Proveedor)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'negative' : 'positive'"
              size="sm"
              @click="toggleEstadoProveedor(props.row as Proveedor)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="store"
              color="info"
              size="sm"
              @click="verSucursales(props.row as Proveedor)"
            >
              <q-tooltip>Ver Sucursales</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="delete"
              color="negative"
              size="sm"
              @click="eliminarProveedor(props.row as Proveedor)"
            >
              <q-tooltip>Eliminar</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Proveedor Dialog -->
      <q-dialog v-model="showCreateProveedorDialog" persistent>
        <q-card style="min-width: 600px; max-width: 800px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoProveedor ? 'Editar' : 'Nuevo' }} Proveedor</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarProveedor">
              <div class="row q-gutter-md">
                <div class="col-12 col-md-5">
                  <q-input
                    v-model="formProveedor.codigo_proveedor"
                    label="Código *"
                    outlined
                    dense
                    :rules="[val => !!val || 'El código es requerido']"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formProveedor.nombre_proveedor"
                    label="Nombre *"
                    outlined
                    dense
                    :rules="[val => !!val || 'El nombre es requerido']"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-5">
                  <q-input
                    v-model="formProveedor.razon_social"
                    label="Razón Social"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formProveedor.rfc"
                    label="RUT"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formProveedor.direccion"
                    label="Dirección"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-5">
                  <q-input
                    v-model="formProveedor.telefono"
                    label="Teléfono"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formProveedor.email"
                    label="Email"
                    type="email"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-5">
                  <q-input
                    v-model="formProveedor.contacto"
                    label="Contacto"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formProveedor.telefono_contacto"
                    label="Teléfono Contacto"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-5">
                  <q-input
                    v-model="formProveedor.email_contacto"
                    label="Email Contacto"
                    type="email"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-toggle
                    v-model="formProveedor.activo"
                    label="Activo"
                  />
                </div>
              </div>

              <div class="q-mt-md">
                <q-input
                  v-model="formProveedor.observaciones"
                  label="Observaciones"
                  outlined
                  type="textarea"
                  rows="3"
                />
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar"
              @click="guardarProveedor"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Sucursales Dialog -->
      <q-dialog v-model="showSucursalesDialog" persistent>
        <q-card style="min-width: 1000px; max-width: 1200px">
          <q-card-section class="row items-center">
            <div class="text-h6">Sucursales de {{ proveedorSeleccionado?.nombre_proveedor }}</div>
            <q-space />
            <q-btn
              color="primary"
              icon="add"
              label="Nueva Sucursal"
              @click="abrirFormularioSucursal"
              class="q-mr-sm"
            />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <!-- Sucursales Table -->
            <q-table
              :rows="sucursales"
              :columns="columnsSucursales"
              :loading="isLoading"
              row-key="id_sucursal"
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

              <template v-slot:body-cell-es_sucursal_principal="props">
                <q-td :props="props">
                  <q-badge
                    :color="props.value ? 'blue' : 'grey'"
                    :label="props.value ? 'Principal' : 'Secundaria'"
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
                    @click="editarSucursal(props.row as SucursalProveedor)"
                  >
                    <q-tooltip>Editar</q-tooltip>
                  </q-btn>
                  <q-btn
                    v-if="!props.row.es_sucursal_principal"
                    flat
                    round
                    icon="star"
                    color="warning"
                    size="sm"
                    @click="establecerPrincipal(props.row as SucursalProveedor)"
                  >
                    <q-tooltip>Establecer como Principal</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    round
                    :icon="props.row.activo ? 'block' : 'check_circle'"
                    :color="props.row.activo ? 'negative' : 'positive'"
                    size="sm"
                    @click="toggleEstadoSucursal(props.row as SucursalProveedor)"
                  >
                    <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    round
                    icon="delete"
                    color="negative"
                    size="sm"
                    @click="eliminarSucursal(props.row as SucursalProveedor)"
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

      <!-- Create/Edit Sucursal Dialog -->
      <q-dialog v-model="showCreateSucursalDialog" persistent>
        <q-card style="min-width: 600px; max-width: 800px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoSucursal ? 'Editar' : 'Nueva' }} Sucursal</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarSucursal">
              <div class="row q-gutter-md">
                <div class="col-12 col-md-5">
                  <q-input
                    v-model="formSucursal.codigo_sucursal"
                    label="Código *"
                    outlined
                    dense
                    :rules="[val => !!val || 'El código es requerido']"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formSucursal.nombre_sucursal"
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
                    v-model="formSucursal.direccion"
                    label="Dirección"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formSucursal.ciudad"
                    label="Ciudad"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formSucursal.estado"
                    label="Estado/Región"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-input
                    v-model="formSucursal.codigo_postal"
                    label="Código Postal"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formSucursal.pais"
                    label="País"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formSucursal.telefono"
                    label="Teléfono"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-input
                    v-model="formSucursal.email"
                    label="Email"
                    type="email"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formSucursal.contacto"
                    label="Contacto"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formSucursal.telefono_contacto"
                    label="Teléfono Contacto"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-input
                    v-model="formSucursal.email_contacto"
                    label="Email Contacto"
                    type="email"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-6">
                  <q-toggle
                    v-model="formSucursal.es_sucursal_principal"
                    label="Sucursal Principal"
                  />
                </div>
                <div class="col-12 col-md-5">
                  <q-toggle
                    v-model="formSucursal.activo"
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
              @click="guardarSucursal"
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
  useProveedorStore,
  type Proveedor,
  type ProveedorCreate,
  type SucursalProveedor,
  type SucursalProveedorCreate
} from '../stores/proveedores'

const $q = useQuasar()
const proveedorStore = useProveedorStore()

// Reactive data
const proveedores = ref<Proveedor[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const showCreateProveedorDialog = ref(false)
const editandoProveedor = ref(false)
const showSucursalesDialog = ref(false)
const showCreateSucursalDialog = ref(false)
const editandoSucursal = ref(false)
const proveedorSeleccionado = ref<Proveedor | null>(null)
const sucursales = ref<SucursalProveedor[]>([])

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
  sortBy: 'id_proveedor',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formProveedor = ref<ProveedorCreate & { id_proveedor?: number }>({
  codigo_proveedor: '',
  nombre_proveedor: '',
  razon_social: '',
  rfc: '',
  direccion: '',
  telefono: '',
  email: '',
  contacto: '',
  telefono_contacto: '',
  email_contacto: '',
  observaciones: '',
  activo: true
})

const formSucursal = ref<SucursalProveedorCreate & { id_sucursal?: number }>({
  id_proveedor: 0,
  codigo_sucursal: '',
  nombre_sucursal: '',
  direccion: '',
  ciudad: '',
  estado: '',
  codigo_postal: '',
  pais: '',
  telefono: '',
  email: '',
  contacto: '',
  telefono_contacto: '',
  email_contacto: '',
  es_sucursal_principal: false,
  activo: true
})

// Table columns
const columnsProveedores = [
  {
    name: 'codigo_proveedor',
    required: true,
    label: 'Código',
    align: 'left' as const,
    field: 'codigo_proveedor',
    sortable: true
  },
  {
    name: 'nombre_proveedor',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_proveedor',
    sortable: true
  },
  {
    name: 'razon_social',
    label: 'Razón Social',
    align: 'left' as const,
    field: 'razon_social'
  },
  {
    name: 'rfc',
    label: 'RUT',
    align: 'left' as const,
    field: 'rfc'
  },
  {
    name: 'telefono',
    label: 'Teléfono',
    align: 'left' as const,
    field: 'telefono'
  },
  {
    name: 'email',
    label: 'Email',
    align: 'left' as const,
    field: 'email'
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

// Table columns for sucursales
const columnsSucursales = [
  {
    name: 'codigo_sucursal',
    required: true,
    label: 'Código',
    align: 'left' as const,
    field: 'codigo_sucursal',
    sortable: true
  },
  {
    name: 'nombre_sucursal',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_sucursal',
    sortable: true
  },
  {
    name: 'ciudad',
    label: 'Ciudad',
    align: 'left' as const,
    field: 'ciudad'
  },
  {
    name: 'telefono',
    label: 'Teléfono',
    align: 'left' as const,
    field: 'telefono'
  },
  {
    name: 'email',
    label: 'Email',
    align: 'left' as const,
    field: 'email'
  },
  {
    name: 'es_sucursal_principal',
    label: 'Tipo',
    align: 'center' as const,
    field: 'es_sucursal_principal',
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
const onRequestProveedores = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarProveedores()
}

const cargarProveedores = async () => {
  try {
    isLoading.value = true
    const params: any = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    if (filtros.value.estado !== null) {
      params.activo = filtros.value.estado
      console.log('Filtro aplicado - estado:', filtros.value.estado, 'params.activo:', params.activo)
    } else {
      console.log('Sin filtro de estado aplicado')
    }

    console.log('Parámetros enviados:', params)
    const response = await proveedorStore.obtenerProveedores(params)
    console.log('Respuesta del servidor:', response)

    // Filtrar por búsqueda en el frontend si hay texto de búsqueda
    let proveedoresFiltered = response
    if (filtros.value.busqueda && filtros.value.busqueda.trim()) {
      const busqueda = filtros.value.busqueda.toLowerCase().trim()
      proveedoresFiltered = response.filter((proveedor: any) =>
        proveedor.codigo_proveedor.toLowerCase().includes(busqueda) ||
        proveedor.nombre_proveedor.toLowerCase().includes(busqueda) ||
        (proveedor.rfc && proveedor.rfc.toLowerCase().includes(busqueda)) ||
        (proveedor.razon_social && proveedor.razon_social.toLowerCase().includes(busqueda))
      )
      console.log('Filtro de búsqueda aplicado:', busqueda, 'Resultados:', proveedoresFiltered.length)
    }

    proveedores.value = proveedoresFiltered

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar proveedores',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const buscarProveedores = async () => {
  paginacion.value.page = 1
  await cargarProveedores()
}

const abrirFormularioProveedor = () => {
  resetFormProveedor()
  showCreateProveedorDialog.value = true
}

const editarProveedor = (proveedor: Proveedor) => {
  editandoProveedor.value = true
  formProveedor.value = { ...proveedor }
  showCreateProveedorDialog.value = true
}

const guardarProveedor = async () => {
  try {
    isGuardando.value = true

    if (editandoProveedor.value && formProveedor.value.id_proveedor) {
      await proveedorStore.actualizarProveedor(formProveedor.value.id_proveedor, formProveedor.value)
      $q.notify({
        type: 'positive',
        message: 'Proveedor actualizado correctamente'
      })
    } else {
      await proveedorStore.crearProveedor(formProveedor.value)
      $q.notify({
        type: 'positive',
        message: 'Proveedor creado correctamente'
      })
    }

    showCreateProveedorDialog.value = false
    resetFormProveedor()
    await cargarProveedores()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar proveedor',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoProveedor = async (proveedor: Proveedor) => {
  try {
    if (proveedor.activo) {
      await proveedorStore.eliminarProveedor(proveedor.id_proveedor, false)
      $q.notify({
        type: 'positive',
        message: 'Proveedor desactivado'
      })
    } else {
      await proveedorStore.activarProveedor(proveedor.id_proveedor)
      $q.notify({
        type: 'positive',
        message: 'Proveedor activado'
      })
    }

    await cargarProveedores()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de proveedor',
      caption: error.message
    })
  }
}

const eliminarProveedor = async (proveedor: Proveedor) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de eliminar el proveedor "${proveedor.nombre_proveedor}"?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await proveedorStore.eliminarProveedor(proveedor.id_proveedor, true)
      $q.notify({
        type: 'positive',
        message: 'Proveedor eliminado correctamente'
      })
      await cargarProveedores()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar proveedor',
        caption: error.message
      })
    }
  })
}

const resetFormProveedor = () => {
  editandoProveedor.value = false
  formProveedor.value = {
    codigo_proveedor: '',
    nombre_proveedor: '',
    razon_social: '',
    rfc: '',
    direccion: '',
    telefono: '',
    email: '',
    contacto: '',
    telefono_contacto: '',
    email_contacto: '',
    observaciones: '',
    activo: true
  }
}

// Sucursales methods
const verSucursales = async (proveedor: Proveedor) => {
  proveedorSeleccionado.value = proveedor
  await cargarSucursales(proveedor.id_proveedor)
  showSucursalesDialog.value = true
}

const cargarSucursales = async (proveedorId: number) => {
  try {
    isLoading.value = true
    const response = await proveedorStore.obtenerSucursalesPorProveedor(proveedorId)
    sucursales.value = response
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar sucursales',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const abrirFormularioSucursal = () => {
  resetFormSucursal()
  if (proveedorSeleccionado.value) {
    formSucursal.value.id_proveedor = proveedorSeleccionado.value.id_proveedor
  }
  showCreateSucursalDialog.value = true
}

const editarSucursal = (sucursal: SucursalProveedor) => {
  editandoSucursal.value = true
  formSucursal.value = { ...sucursal }
  showCreateSucursalDialog.value = true
}

const guardarSucursal = async () => {
  try {
    isGuardando.value = true

    if (editandoSucursal.value && formSucursal.value.id_sucursal) {
      await proveedorStore.actualizarSucursal(formSucursal.value.id_sucursal, formSucursal.value)
      $q.notify({
        type: 'positive',
        message: 'Sucursal actualizada correctamente'
      })
    } else {
      await proveedorStore.crearSucursal(formSucursal.value)
      $q.notify({
        type: 'positive',
        message: 'Sucursal creada correctamente'
      })
    }

    showCreateSucursalDialog.value = false
    resetFormSucursal()
    if (proveedorSeleccionado.value) {
      await cargarSucursales(proveedorSeleccionado.value.id_proveedor)
    }

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar sucursal',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoSucursal = async (sucursal: SucursalProveedor) => {
  try {
    if (sucursal.activo) {
      await proveedorStore.eliminarSucursal(sucursal.id_sucursal, false)
      $q.notify({
        type: 'positive',
        message: 'Sucursal desactivada'
      })
    } else {
      await proveedorStore.activarSucursal(sucursal.id_sucursal)
      $q.notify({
        type: 'positive',
        message: 'Sucursal activada'
      })
    }

    if (proveedorSeleccionado.value) {
      await cargarSucursales(proveedorSeleccionado.value.id_proveedor)
    }

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de sucursal',
      caption: error.message
    })
  }
}

const eliminarSucursal = async (sucursal: SucursalProveedor) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿ Está seguro de eliminar la sucursal "${sucursal.nombre_sucursal}"?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await proveedorStore.eliminarSucursal(sucursal.id_sucursal, true)
      $q.notify({
        type: 'positive',
        message: 'Sucursal eliminada correctamente'
      })
      if (proveedorSeleccionado.value) {
        await cargarSucursales(proveedorSeleccionado.value.id_proveedor)
      }
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar sucursal',
        caption: error.message
      })
    }
  })
}

const establecerPrincipal = async (sucursal: SucursalProveedor) => {
  try {
    await proveedorStore.establecerSucursalPrincipal(sucursal.id_sucursal)
    $q.notify({
      type: 'positive',
      message: 'Sucursal establecida como principal'
    })
    if (proveedorSeleccionado.value) {
      await cargarSucursales(proveedorSeleccionado.value.id_proveedor)
    }
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al establecer sucursal principal',
      caption: error.message
    })
  }
}

const resetFormSucursal = () => {
  editandoSucursal.value = false
  formSucursal.value = {
    id_proveedor: proveedorSeleccionado.value?.id_proveedor || 0,
    codigo_sucursal: '',
    nombre_sucursal: '',
    direccion: '',
    ciudad: '',
    estado: '',
    codigo_postal: '',
    pais: '',
    telefono: '',
    email: '',
    contacto: '',
    telefono_contacto: '',
    email_contacto: '',
    es_sucursal_principal: false,
    activo: true
  }
}

// Lifecycle
onMounted(() => {
  cargarProveedores()
})
</script>