<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Gestión de Productos</h4>
          <p class="text-grey-7 q-mb-none">Administra el catálogo de productos del sistema</p>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nuevo Producto"
          @click="abrirFormularioProducto"
        />
      </div>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-gutter-md items-center">
            <q-input
              v-model="filtros.busqueda"
              placeholder="Buscar por SKU, nombre o descripción..."
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
              v-model="filtros.marca"
              :options="marcasOptions"
              label="Marca"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 150px"
            />
            <q-select
              v-model="filtros.tipo"
              :options="tiposOptions"
              label="Tipo"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 150px"
            />
            <q-select
              v-model="filtros.estado"
              :options="estadoOptions"
              label="Estado"
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
              @click="buscarProductos"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Products Table -->
      <q-table
        :rows="productos"
        :columns="columnsProductos"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_producto"
        flat
        bordered
        @request="onRequestProductos"
      >
        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'green' : 'red'"
              :label="props.value ? 'Activo' : 'Inactivo'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-stock_disponible="props">
          <q-td :props="props">
            <q-badge
              :color="getStockColor(props.row)"
              :label="props.value || 0"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-precio_venta="props">
          <q-td :props="props">
            {{ formatCurrency(props.value) }}
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
              @click="editarProducto(props.row as Producto)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="inventory"
              color="info"
              size="sm"
              @click="verInventario(props.row as Producto)"
            >
              <q-tooltip>Ver Inventario</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'negative' : 'positive'"
              size="sm"
              @click="toggleEstadoProducto(props.row as Producto)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="delete"
              color="negative"
              size="sm"
              @click="eliminarProducto(props.row as Producto)"
            >
              <q-tooltip>Eliminar</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Producto Dialog -->
      <q-dialog v-model="showCreateProductoDialog" persistent maximized>
        <q-card>
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoProducto ? 'Editar' : 'Nuevo' }} Producto</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-form @submit="guardarProducto">
              <q-tabs v-model="tabActual" dense class="text-grey" active-color="primary" indicator-color="primary" align="justify">
                <q-tab name="general" label="Información General" />
                <q-tab name="especificaciones" label="Especificaciones Técnicas" />
                <q-tab name="contraincendios" label="Sistemas Contraincendios" />
                <q-tab name="certificaciones" label="Certificaciones" />
                <q-tab name="inventario" label="Inventario" />
              </q-tabs>

              <q-separator />

              <q-tab-panels v-model="tabActual" animated>
                <!-- Tab General -->
                <q-tab-panel name="general">
                  <div class="row q-gutter-md">
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model="formProducto.sku"
                        label="SKU *"
                        outlined
                        dense
                        :rules="[val => !!val || 'El SKU es requerido']"
                      />
                    </div>
                    <div class="col-12 col-md-8">
                      <q-input
                        v-model="formProducto.nombre_producto"
                        label="Nombre del Producto *"
                        outlined
                        dense
                        :rules="[val => !!val || 'El nombre es requerido']"
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12">
                      <q-input
                        v-model="formProducto.descripcion_corta"
                        label="Descripción Corta"
                        outlined
                        dense
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12">
                      <q-input
                        v-model="formProducto.descripcion_detallada"
                        label="Descripción Detallada"
                        outlined
                        type="textarea"
                        rows="3"
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-4">
                      <q-select
                        v-model="formProducto.id_marca"
                        :options="marcasOptions"
                        label="Marca"
                        outlined
                        dense
                        emit-value
                        map-options
                        clearable
                      />
                    </div>
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model="formProducto.modelo"
                        label="Modelo"
                        outlined
                        dense
                      />
                    </div>
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model="formProducto.numero_parte"
                        label="Número de Parte"
                        outlined
                        dense
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-6">
                      <q-select
                        v-model="formProducto.id_tipo_producto"
                        :options="tiposOptions"
                        label="Tipo de Producto *"
                        outlined
                        dense
                        emit-value
                        map-options
                        :rules="[val => !!val || 'El tipo es requerido']"
                      />
                    </div>
                    <div class="col-12 col-md-5">
                      <q-select
                        v-model="formProducto.id_unidad_medida"
                        :options="unidadesOptions"
                        label="Unidad de Medida *"
                        outlined
                        dense
                        emit-value
                        map-options
                        :rules="[val => !!val || 'La unidad es requerida']"
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-6">
                      <q-toggle
                        v-model="formProducto.activo"
                        label="Activo"
                      />
                    </div>
                  </div>
                </q-tab-panel>

                <!-- Tab Especificaciones -->
                <q-tab-panel name="especificaciones">
                  <div class="row q-gutter-md">
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model.number="formProducto.peso_kg"
                        label="Peso (kg)"
                        outlined
                        dense
                        type="number"
                        step="0.01"
                      />
                    </div>
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model.number="formProducto.dimensiones_largo_cm"
                        label="Largo (cm)"
                        outlined
                        dense
                        type="number"
                        step="0.1"
                      />
                    </div>
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model.number="formProducto.dimensiones_ancho_cm"
                        label="Ancho (cm)"
                        outlined
                        dense
                        type="number"
                        step="0.1"
                      />
                    </div>
                    <div class="col-12 col-md-2">
                      <q-input
                        v-model.number="formProducto.dimensiones_alto_cm"
                        label="Alto (cm)"
                        outlined
                        dense
                        type="number"
                        step="0.1"
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="formProducto.material_principal"
                        label="Material Principal"
                        outlined
                        dense
                      />
                    </div>
                    <div class="col-12 col-md-5">
                      <q-input
                        v-model="formProducto.color"
                        label="Color"
                        outlined
                        dense
                      />
                    </div>
                  </div>
                </q-tab-panel>

                <!-- Tab Contraincendios -->
                <q-tab-panel name="contraincendios">
                  <div class="row q-gutter-md">
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model.number="formProducto.presion_trabajo_bar"
                        label="Presión de Trabajo (bar)"
                        outlined
                        dense
                        type="number"
                        step="0.1"
                      />
                    </div>
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model.number="formProducto.presion_maxima_bar"
                        label="Presión Máxima (bar)"
                        outlined
                        dense
                        type="number"
                        step="0.1"
                      />
                    </div>
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model.number="formProducto.factor_k"
                        label="Factor K"
                        outlined
                        dense
                        type="number"
                        step="0.01"
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model.number="formProducto.temperatura_min_celsius"
                        label="Temp. Mínima (°C)"
                        outlined
                        dense
                        type="number"
                      />
                    </div>
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model.number="formProducto.temperatura_max_celsius"
                        label="Temp. Máxima (°C)"
                        outlined
                        dense
                        type="number"
                      />
                    </div>
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model.number="formProducto.temperatura_activacion_celsius"
                        label="Temp. Activación (°C)"
                        outlined
                        dense
                        type="number"
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="formProducto.conexion_entrada"
                        label="Conexión de Entrada"
                        outlined
                        dense
                      />
                    </div>
                    <div class="col-12 col-md-5">
                      <q-input
                        v-model="formProducto.conexion_salida"
                        label="Conexión de Salida"
                        outlined
                        dense
                      />
                    </div>
                  </div>
                </q-tab-panel>

                <!-- Tab Certificaciones -->
                <q-tab-panel name="certificaciones">
                  <div class="row q-gutter-md">
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model="formProducto.certificacion_ul"
                        label="Certificación UL"
                        outlined
                        dense
                      />
                    </div>
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model="formProducto.certificacion_fm"
                        label="Certificación FM"
                        outlined
                        dense
                      />
                    </div>
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model="formProducto.certificacion_vds"
                        label="Certificación VDS"
                        outlined
                        dense
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model="formProducto.certificacion_lpcb"
                        label="Certificación LPCB"
                        outlined
                        dense
                      />
                    </div>
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model="formProducto.norma_nfpa"
                        label="Norma NFPA"
                        outlined
                        dense
                      />
                    </div>
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model="formProducto.norma_en"
                        label="Norma EN"
                        outlined
                        dense
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="formProducto.norma_iso"
                        label="Norma ISO"
                        outlined
                        dense
                      />
                    </div>
                  </div>
                </q-tab-panel>

                <!-- Tab Inventario -->
                <q-tab-panel name="inventario">
                  <div class="row q-gutter-md">
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model.number="formProducto.stock_minimo"
                        label="Stock Mínimo *"
                        outlined
                        dense
                        type="number"
                        :rules="[val => val >= 0 || 'Debe ser mayor o igual a 0']"
                      />
                    </div>
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model.number="formProducto.stock_maximo"
                        label="Stock Máximo *"
                        outlined
                        dense
                        type="number"
                        :rules="[val => val >= 0 || 'Debe ser mayor o igual a 0']"
                      />
                    </div>
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model.number="formProducto.punto_reorden"
                        label="Punto de Reorden *"
                        outlined
                        dense
                        type="number"
                        :rules="[val => val >= 0 || 'Debe ser mayor o igual a 0']"
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model.number="formProducto.costo_promedio"
                        label="Costo Promedio"
                        outlined
                        dense
                        type="number"
                        step="0.01"
                      />
                    </div>
                    <div class="col-12 col-md-4">
                      <q-input
                        v-model.number="formProducto.precio_venta"
                        label="Precio de Venta"
                        outlined
                        dense
                        type="number"
                        step="0.01"
                      />
                    </div>
                    <div class="col-12 col-md-3">
                      <q-input
                        v-model.number="formProducto.dias_vida_util"
                        label="Días de Vida Útil"
                        outlined
                        dense
                        type="number"
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="formProducto.ubicacion_principal"
                        label="Ubicación Principal"
                        outlined
                        dense
                      />
                    </div>
                  </div>

                  <div class="row q-gutter-md q-mt-sm">
                    <div class="col-12 col-md-6">
                      <q-toggle
                        v-model="formProducto.requiere_lote"
                        label="Requiere Control de Lotes"
                      />
                    </div>
                    <div class="col-12 col-md-5">
                      <q-toggle
                        v-model="formProducto.requiere_numero_serie"
                        label="Requiere Número de Serie"
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
              @click="guardarProducto"
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
  useProductoStore,
  type Producto,
  type ProductoCreate,
  type Marca,
  type TipoProducto,
  type UnidadMedida
} from '../stores/productos'

const $q = useQuasar()
const productoStore = useProductoStore()

// Reactive data
const productos = ref<Producto[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const showCreateProductoDialog = ref(false)
const editandoProducto = ref(false)
const tabActual = ref('general')

// Filters
const filtros = ref({
  busqueda: '',
  marca: null as number | null,
  tipo: null as number | null,
  estado: null as boolean | null
})

const estadoOptions = [
  { label: 'Activo', value: true },
  { label: 'Inactivo', value: false }
]

// Pagination
const paginacion = ref({
  sortBy: 'id_producto',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formProducto = ref<ProductoCreate & { id_producto?: number }>({
  sku: '',
  nombre_producto: '',
  descripcion_corta: '',
  descripcion_detallada: '',
  id_marca: undefined,
  modelo: '',
  numero_parte: '',
  id_tipo_producto: 0,
  id_unidad_medida: 0,
  peso_kg: undefined,
  dimensiones_largo_cm: undefined,
  dimensiones_ancho_cm: undefined,
  dimensiones_alto_cm: undefined,
  material_principal: '',
  color: '',
  presion_trabajo_bar: undefined,
  presion_maxima_bar: undefined,
  temperatura_min_celsius: undefined,
  temperatura_max_celsius: undefined,
  temperatura_activacion_celsius: undefined,
  factor_k: undefined,
  conexion_entrada: '',
  conexion_salida: '',
  certificacion_ul: '',
  certificacion_fm: '',
  certificacion_vds: '',
  certificacion_lpcb: '',
  norma_nfpa: '',
  norma_en: '',
  norma_iso: '',
  stock_minimo: 0,
  stock_maximo: 0,
  punto_reorden: 0,
  costo_promedio: undefined,
  precio_venta: undefined,
  ubicacion_principal: '',
  requiere_lote: false,
  requiere_numero_serie: false,
  dias_vida_util: undefined,
  activo: true
})

// Computed options for selects
const marcasOptions = computed(() => {
  return productoStore.marcas.map(marca => ({
    label: marca.nombre_marca,
    value: marca.id_marca
  }))
})

const tiposOptions = computed(() => {
  return productoStore.tiposProducto.map(tipo => ({
    label: tipo.nombre_tipo,
    value: tipo.id_tipo_producto
  }))
})

const unidadesOptions = computed(() => {
  return productoStore.unidadesMedida.map(unidad => ({
    label: unidad.nombre_unidad,
    value: unidad.id_unidad
  }))
})

// Table columns
const columnsProductos = [
  {
    name: 'sku',
    required: true,
    label: 'SKU',
    align: 'left' as const,
    field: 'sku',
    sortable: true
  },
  {
    name: 'nombre_producto',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_producto',
    sortable: true
  },
  {
    name: 'descripcion_corta',
    label: 'Descripción',
    align: 'left' as const,
    field: 'descripcion_corta'
  },
  {
    name: 'stock_disponible',
    label: 'Stock',
    align: 'center' as const,
    field: 'stock_disponible',
    sortable: true
  },
  {
    name: 'precio_venta',
    label: 'Precio',
    align: 'right' as const,
    field: 'precio_venta',
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
const onRequestProductos = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarProductos()
}

const cargarProductos = async () => {
  try {
    isLoading.value = true
    const params: any = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    if (filtros.value.estado !== null) {
      params.activo = filtros.value.estado
    }
    if (filtros.value.marca !== null) {
      params.marca_id = filtros.value.marca
    }
    if (filtros.value.tipo !== null) {
      params.tipo_id = filtros.value.tipo
    }

    let response = await productoStore.obtenerProductos(params)

    // Filtrar por búsqueda en el frontend si hay texto de búsqueda
    if (filtros.value.busqueda && filtros.value.busqueda.trim()) {
      const busqueda = filtros.value.busqueda.toLowerCase().trim()
      response = response.filter((producto: any) =>
        producto.sku.toLowerCase().includes(busqueda) ||
        producto.nombre_producto.toLowerCase().includes(busqueda) ||
        (producto.descripcion_corta && producto.descripcion_corta.toLowerCase().includes(busqueda))
      )
    }

    productos.value = response

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar productos',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const buscarProductos = async () => {
  paginacion.value.page = 1
  await cargarProductos()
}

const abrirFormularioProducto = () => {
  resetFormProducto()
  showCreateProductoDialog.value = true
}

const editarProducto = (producto: Producto) => {
  editandoProducto.value = true
  formProducto.value = { ...producto }
  showCreateProductoDialog.value = true
}

const guardarProducto = async () => {
  try {
    isGuardando.value = true

    if (editandoProducto.value && formProducto.value.id_producto) {
      await productoStore.actualizarProducto(formProducto.value.id_producto, formProducto.value)
      $q.notify({
        type: 'positive',
        message: 'Producto actualizado correctamente'
      })
    } else {
      await productoStore.crearProducto(formProducto.value)
      $q.notify({
        type: 'positive',
        message: 'Producto creado correctamente'
      })
    }

    showCreateProductoDialog.value = false
    resetFormProducto()
    await cargarProductos()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar producto',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoProducto = async (producto: Producto) => {
  try {
    if (producto.activo) {
      await productoStore.eliminarProducto(producto.id_producto, false)
      $q.notify({
        type: 'positive',
        message: 'Producto desactivado'
      })
    } else {
      await productoStore.activarProducto(producto.id_producto)
      $q.notify({
        type: 'positive',
        message: 'Producto activado'
      })
    }

    await cargarProductos()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de producto',
      caption: error.message
    })
  }
}

const eliminarProducto = async (producto: Producto) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de eliminar el producto "${producto.nombre_producto}"?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await productoStore.eliminarProducto(producto.id_producto, true)
      $q.notify({
        type: 'positive',
        message: 'Producto eliminado correctamente'
      })
      await cargarProductos()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar producto',
        caption: error.message
      })
    }
  })
}

const verInventario = (producto: Producto) => {
  $q.notify({
    type: 'info',
    message: `Ver inventario de ${producto.nombre_producto}`,
    caption: 'Funcionalidad en desarrollo'
  })
}

const resetFormProducto = () => {
  editandoProducto.value = false
  tabActual.value = 'general'
  formProducto.value = {
    sku: '',
    nombre_producto: '',
    descripcion_corta: '',
    descripcion_detallada: '',
    id_marca: undefined,
    modelo: '',
    numero_parte: '',
    id_tipo_producto: 0,
    id_unidad_medida: 0,
    peso_kg: undefined,
    dimensiones_largo_cm: undefined,
    dimensiones_ancho_cm: undefined,
    dimensiones_alto_cm: undefined,
    material_principal: '',
    color: '',
    presion_trabajo_bar: undefined,
    presion_maxima_bar: undefined,
    temperatura_min_celsius: undefined,
    temperatura_max_celsius: undefined,
    temperatura_activacion_celsius: undefined,
    factor_k: undefined,
    conexion_entrada: '',
    conexion_salida: '',
    certificacion_ul: '',
    certificacion_fm: '',
    certificacion_vds: '',
    certificacion_lpcb: '',
    norma_nfpa: '',
    norma_en: '',
    norma_iso: '',
    stock_minimo: 0,
    stock_maximo: 0,
    punto_reorden: 0,
    costo_promedio: undefined,
    precio_venta: undefined,
    ubicacion_principal: '',
    requiere_lote: false,
    requiere_numero_serie: false,
    dias_vida_util: undefined,
    activo: true
  }
}

const getStockColor = (producto: Producto) => {
  const stock = producto.stock_disponible || 0
  if (stock <= producto.stock_minimo) return 'red'
  if (stock <= producto.punto_reorden) return 'orange'
  return 'green'
}

const formatCurrency = (value?: number) => {
  if (!value) return '-'
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP'
  }).format(value)
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    productoStore.obtenerMarcas(),
    productoStore.obtenerTiposProducto(),
    productoStore.obtenerUnidadesMedida(),
    cargarProductos()
  ])
})
</script>