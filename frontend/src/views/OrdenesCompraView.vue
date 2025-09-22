<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Órdenes de Compra</h4>
          <p class="text-grey-7 q-mb-none">Gestión integral de órdenes de compra</p>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nueva Orden"
          @click="abrirFormularioOrdenCompra"
        />
      </div>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-gutter-md items-center">
            <q-input
              v-model="filtros.busqueda"
              placeholder="Buscar por número de orden..."
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
              v-model="filtros.proveedor"
              :options="proveedoresOptions"
              label="Proveedor"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 200px"
            />
            <q-select
              v-model="filtros.estado"
              :options="estadosOptions"
              label="Estado"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 150px"
            />
            <q-input
              v-model="filtros.fechaDesde"
              type="date"
              label="Fecha desde"
              outlined
              dense
              clearable
              style="min-width: 150px"
            />
            <q-input
              v-model="filtros.fechaHasta"
              type="date"
              label="Fecha hasta"
              outlined
              dense
              clearable
              style="min-width: 150px"
            />
            <q-btn
              color="primary"
              icon="search"
              label="Buscar"
              @click="buscarOrdenesCompra"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Orders Table -->
      <q-table
        :rows="ordenesCompraFiltradas"
        :columns="columnsOrdenesCompra"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_orden_compra"
        flat
        bordered
        @request="onRequestOrdenesCompra"
      >
        <template v-slot:body-cell-estado="props">
          <q-td :props="props">
            <q-badge
              :color="getEstadoColor(props.value)"
              :label="props.value"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-total="props">
          <q-td :props="props">
            <span class="text-weight-bold">
              {{ formatCurrency(props.value) }}
            </span>
          </q-td>
        </template>

        <template v-slot:body-cell-fecha_orden="props">
          <q-td :props="props">
            {{ formatDate(props.value) }}
          </q-td>
        </template>

        <template v-slot:body-cell-fecha_requerida="props">
          <q-td :props="props">
            <span
              :class="getDateClass(props.value)"
            >
              {{ formatDate(props.value) }}
            </span>
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

        <template v-slot:body-cell-acciones="props">
          <q-td :props="props">
            <div class="q-gutter-sm">
              <q-btn
                size="sm"
                color="blue"
                icon="visibility"
                @click="verOrdenCompra(props.row)"
                dense
                round
              >
                <q-tooltip>Ver detalle</q-tooltip>
              </q-btn>
              <q-btn
                size="sm"
                color="green"
                icon="edit"
                @click="editarOrdenCompra(props.row)"
                dense
                round
                :disable="!puedeEditar(props.row)"
              >
                <q-tooltip>Editar</q-tooltip>
              </q-btn>
              <q-btn
                size="sm"
                color="orange"
                icon="file_copy"
                @click="duplicarOrdenCompra(props.row)"
                dense
                round
              >
                <q-tooltip>Duplicar</q-tooltip>
              </q-btn>
              <q-btn
                size="sm"
                :color="getAccionColor(props.row.estado)"
                :icon="getAccionIcon(props.row.estado)"
                @click="ejecutarAccion(props.row)"
                dense
                round
                :disable="!puedeEjecutarAccion(props.row)"
              >
                <q-tooltip>{{ getAccionTooltip(props.row.estado) }}</q-tooltip>
              </q-btn>
              <q-btn
                size="sm"
                color="red"
                icon="delete"
                @click="eliminarOrdenCompra(props.row)"
                dense
                round
                :disable="!puedeEliminar(props.row)"
              >
                <q-tooltip>Eliminar</q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </template>
      </q-table>

      <!-- Dialog para formulario de orden de compra -->
      <q-dialog
        v-model="mostrarFormulario"
        persistent
        maximized
        transition-show="slide-up"
        transition-hide="slide-down"
      >
        <q-card class="dialog-card">
          <q-toolbar class="bg-primary text-white">
            <q-toolbar-title>
              {{ modoEdicion ? 'Editar Orden de Compra' : 'Nueva Orden de Compra' }}
            </q-toolbar-title>
            <q-btn flat round dense icon="close" @click="cerrarFormulario" />
          </q-toolbar>

          <q-card-section class="q-pa-md scroll" style="max-height: calc(100vh - 100px)">
            <q-form @submit="guardarOrdenCompra" class="q-gutter-md">
              <!-- Información general -->
              <div class="row q-gutter-md">
                <div class="col-12">
                  <h6 class="q-ma-none q-mb-md">Información General</h6>
                </div>

                <div class="col-md-3 col-sm-6 col-xs-12">
                  <q-input
                    v-model="formulario.numero_orden"
                    label="Número de Orden"
                    outlined
                    dense
                    readonly
                    hint="Se genera automáticamente"
                  />
                </div>

                <div class="col-md-3 col-sm-6 col-xs-12">
                  <q-select
                    v-model="formulario.id_proveedor"
                    :options="proveedoresFiltrados"
                    label="Proveedor *"
                    outlined
                    dense
                    emit-value
                    map-options
                    use-input
                    clearable
                    input-debounce="300"
                    :rules="[val => !!val || 'Proveedor es requerido']"
                    @update:model-value="onProveedorChange"
                    @filter="filtrarProveedores"
                    @clear="limpiarFiltroProveedores"
                    option-value="value"
                    option-label="label"
                  >
                    <template v-slot:no-option>
                      <q-item>
                        <q-item-section class="text-grey">
                          {{ busquedaProveedor ? 'No se encontraron proveedores' : 'Escriba para buscar proveedores' }}
                        </q-item-section>
                      </q-item>
                    </template>
                    <template v-slot:option="scope">
                      <q-item v-bind="scope.itemProps">
                        <q-item-section>
                          <q-item-label>{{ scope.opt.label }}</q-item-label>
                          <q-item-label caption v-if="scope.opt.rut">{{ scope.opt.rut }}</q-item-label>
                        </q-item-section>
                      </q-item>
                    </template>
                  </q-select>
                </div>

                <div class="col-md-3 col-sm-6 col-xs-12">
                  <q-input
                    v-model="formulario.fecha_orden"
                    type="date"
                    label="Fecha de Orden *"
                    outlined
                    dense
                    :rules="[val => !!val || 'Fecha de orden es requerida']"
                  />
                </div>

                <div class="col-md-3 col-sm-6 col-xs-12">
                  <q-input
                    v-model="formulario.fecha_requerida"
                    type="date"
                    label="Fecha Requerida *"
                    outlined
                    dense
                    :rules="[val => !!val || 'Fecha requerida es requerida']"
                  />
                </div>

                <div class="col-md-3 col-sm-6 col-xs-12">
                  <q-input
                    v-model="formulario.fecha_prometida"
                    type="date"
                    label="Fecha Prometida"
                    outlined
                    dense
                  />
                </div>

                <div class="col-md-3 col-sm-6 col-xs-12">
                  <q-select
                    v-model="formulario.moneda"
                    :options="monedasOptions"
                    label="Moneda"
                    outlined
                    dense
                    emit-value
                    map-options
                  />
                </div>

                <div class="col-md-3 col-sm-6 col-xs-12">
                  <q-input
                    v-model.number="formulario.tipo_cambio"
                    type="number"
                    label="Tipo de Cambio"
                    outlined
                    dense
                    step="0.01"
                    min="0"
                  />
                </div>

                <div class="col-md-3 col-sm-6 col-xs-12">
                  <q-input
                    v-model="formulario.contacto_proveedor"
                    label="Contacto Proveedor"
                    outlined
                    dense
                  />
                </div>

                <div class="col-md-6 col-sm-12 col-xs-12">
                  <q-input
                    v-model="formulario.condiciones_pago"
                    label="Condiciones de Pago"
                    outlined
                    dense
                  />
                </div>

                <div class="col-md-6 col-sm-12 col-xs-12">
                  <q-input
                    v-model="formulario.terminos_entrega"
                    label="Términos de Entrega"
                    outlined
                    dense
                  />
                </div>

                <div class="col-12">
                  <q-input
                    v-model="formulario.lugar_entrega"
                    label="Lugar de Entrega"
                    outlined
                    dense
                  />
                </div>

                <div class="col-12">
                  <q-input
                    v-model="formulario.observaciones"
                    label="Observaciones"
                    type="textarea"
                    outlined
                    rows="3"
                  />
                </div>
              </div>

              <!-- Detalles de productos -->
              <q-separator class="q-my-lg" />

              <div class="row q-gutter-md">
                <div class="col-12">
                  <div class="row items-center justify-between">
                    <h6 class="q-ma-none">Detalle de Productos</h6>
                    <q-btn
                      color="primary"
                      icon="add"
                      label="Agregar Producto"
                      @click="abrirSelectorProducto"
                      size="sm"
                    />
                  </div>
                </div>

                <div class="col-12" v-if="formulario.detalles.length > 0">
                  <q-table
                    :rows="formulario.detalles"
                    :columns="columnsDetalles"
                    row-key="numero_linea"
                    flat
                    bordered
                    separator="cell"
                    dense
                  >
                    <template v-slot:body-cell-producto="props">
                      <q-td :props="props">
                        <div>
                          <div class="text-weight-bold">{{ props.row.producto?.sku }}</div>
                          <div class="text-caption">{{ props.row.producto?.nombre_producto }}</div>
                        </div>
                      </q-td>
                    </template>

                    <template v-slot:body-cell-cantidad_solicitada="props">
                      <q-td :props="props">
                        <q-input
                          v-model.number="props.row.cantidad_solicitada"
                          type="number"
                          dense
                          min="0.01"
                          step="0.01"
                          @update:model-value="calcularTotalLinea(props.row)"
                        />
                      </q-td>
                    </template>

                    <template v-slot:body-cell-precio_unitario="props">
                      <q-td :props="props">
                        <q-input
                          v-model.number="props.row.precio_unitario"
                          type="number"
                          dense
                          min="0.01"
                          step="0.01"
                          @update:model-value="calcularTotalLinea(props.row)"
                        />
                      </q-td>
                    </template>

                    <template v-slot:body-cell-descuento_porcentaje="props">
                      <q-td :props="props">
                        <q-input
                          v-model.number="props.row.descuento_porcentaje"
                          type="number"
                          dense
                          min="0"
                          max="100"
                          step="0.01"
                          @update:model-value="calcularTotalLinea(props.row)"
                        />
                      </q-td>
                    </template>

                    <template v-slot:body-cell-impuesto_porcentaje="props">
                      <q-td :props="props">
                        <q-input
                          v-model.number="props.row.impuesto_porcentaje"
                          type="number"
                          dense
                          min="0"
                          max="100"
                          step="0.01"
                          @update:model-value="calcularTotalLinea(props.row)"
                        />
                      </q-td>
                    </template>

                    <template v-slot:body-cell-total_linea="props">
                      <q-td :props="props">
                        <span class="text-weight-bold">
                          {{ formatCurrency(props.row.total_linea) }}
                        </span>
                      </q-td>
                    </template>

                    <template v-slot:body-cell-acciones="props">
                      <q-td :props="props">
                        <q-btn
                          size="sm"
                          color="red"
                          icon="delete"
                          @click="eliminarDetalle(props.rowIndex)"
                          dense
                          round
                        >
                          <q-tooltip>Eliminar</q-tooltip>
                        </q-btn>
                      </q-td>
                    </template>
                  </q-table>
                </div>

                <div class="col-12" v-else>
                  <q-card flat bordered class="text-center q-pa-lg">
                    <q-icon name="shopping_cart" size="3rem" color="grey-5" />
                    <div class="text-h6 text-grey-7 q-mt-md">No hay productos agregados</div>
                    <div class="text-grey-6">Haz clic en "Agregar Producto" para comenzar</div>
                  </q-card>
                </div>
              </div>

              <!-- Totales -->
              <q-separator class="q-my-lg" />

              <div class="row justify-end">
                <div class="col-md-4 col-sm-6 col-xs-12">
                  <q-card flat bordered>
                    <q-card-section>
                      <div class="text-h6 q-mb-md">Resumen</div>
                      <div class="row justify-between q-mb-sm">
                        <span>Subtotal:</span>
                        <span class="text-weight-bold">{{ formatCurrency(totales.subtotal) }}</span>
                      </div>
                      <div class="row justify-between q-mb-sm">
                        <span>Descuentos:</span>
                        <span class="text-weight-bold text-red">-{{ formatCurrency(totales.descuentos) }}</span>
                      </div>
                      <div class="row justify-between q-mb-sm">
                        <span>Impuestos:</span>
                        <span class="text-weight-bold">{{ formatCurrency(totales.impuestos) }}</span>
                      </div>
                      <q-separator class="q-my-sm" />
                      <div class="row justify-between">
                        <span class="text-h6">Total:</span>
                        <span class="text-h6 text-weight-bold text-primary">{{ formatCurrency(totales.total) }}</span>
                      </div>
                    </q-card-section>
                  </q-card>
                </div>
              </div>

              <!-- Botones -->
              <div class="row justify-end q-gutter-md q-mt-lg">
                <q-btn
                  label="Cancelar"
                  color="grey"
                  flat
                  @click="cerrarFormulario"
                />
                <q-btn
                  label="Guardar Borrador"
                  color="orange"
                  @click="guardarBorrador"
                  :loading="guardando"
                />
                <q-btn
                  label="Guardar y Aprobar"
                  color="primary"
                  type="submit"
                  :loading="guardando"
                  :disable="!formularioValido"
                />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- Dialog para selector de productos -->
      <q-dialog
        v-model="mostrarSelectorProducto"
        persistent
        maximized
        transition-show="slide-up"
        transition-hide="slide-down"
      >
        <q-card class="dialog-card">
          <q-toolbar class="bg-primary text-white">
            <q-toolbar-title>Seleccionar Producto</q-toolbar-title>
            <q-btn flat round dense icon="close" @click="cerrarSelectorProducto" />
          </q-toolbar>

          <q-card-section class="q-pa-md">
            <div class="row q-gutter-md q-mb-md">
              <q-input
                v-model="busquedaProducto"
                placeholder="Buscar por SKU o nombre..."
                outlined
                dense
                clearable
                style="min-width: 300px"
                @keyup.enter="buscarProductos"
              >
                <template v-slot:prepend>
                  <q-icon name="search" />
                </template>
              </q-input>
              <q-btn
                color="primary"
                icon="search"
                label="Buscar"
                @click="buscarProductos"
              />
            </div>

            <q-table
              :rows="productosDisponibles"
              :columns="columnsProductos"
              :loading="cargandoProductos"
              row-key="id_producto"
              flat
              bordered
              selection="single"
              v-model:selected="productoSeleccionado"
            >
              <template v-slot:body-cell-stock_actual="props">
                <q-td :props="props">
                  <q-badge
                    :color="props.value > 0 ? 'green' : 'red'"
                    :label="props.value || 0"
                  />
                </q-td>
              </template>

              <template v-slot:body-cell-precio_venta="props">
                <q-td :props="props">
                  {{ formatCurrency(props.value || 0) }}
                </q-td>
              </template>

              <template v-slot:body-cell-costo_promedio="props">
                <q-td :props="props">
                  {{ formatCurrency(props.value || 0) }}
                </q-td>
              </template>
            </q-table>

            <div class="row justify-end q-gutter-md q-mt-lg">
              <q-btn
                label="Cancelar"
                color="grey"
                flat
                @click="cerrarSelectorProducto"
              />
              <q-btn
                label="Agregar Producto"
                color="primary"
                @click="agregarProductoSeleccionado"
                :disable="productoSeleccionado.length === 0"
              />
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- Dialog para ver detalle de orden -->
      <q-dialog
        v-model="mostrarDetalle"
        persistent
        maximized
        transition-show="slide-up"
        transition-hide="slide-down"
      >
        <q-card class="dialog-card" v-if="ordenSeleccionada">
          <q-toolbar class="bg-primary text-white">
            <q-toolbar-title>
              Orden de Compra {{ ordenSeleccionada.numero_orden }}
            </q-toolbar-title>
            <q-btn flat round dense icon="close" @click="cerrarDetalle" />
          </q-toolbar>

          <q-card-section class="q-pa-md scroll">
            <!-- Información de la orden -->
            <div class="row q-gutter-md q-mb-lg">
              <div class="col-12">
                <h6 class="q-ma-none q-mb-md">Información de la Orden</h6>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Número de Orden" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ ordenSeleccionada.numero_orden }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Proveedor" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ ordenSeleccionada.proveedor?.razon_social }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Estado" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      <q-badge
                        :color="getEstadoColor(ordenSeleccionada.estado)"
                        :label="ordenSeleccionada.estado"
                      />
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Fecha de Orden" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ formatDate(ordenSeleccionada.fecha_orden) }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Fecha Requerida" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ formatDate(ordenSeleccionada.fecha_requerida) }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Total" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline text-weight-bold text-primary" tabindex="-1">
                      {{ formatCurrency(ordenSeleccionada.total) }}
                    </div>
                  </template>
                </q-field>
              </div>
            </div>

            <!-- Detalles de productos -->
            <div class="row q-gutter-md">
              <div class="col-12">
                <h6 class="q-ma-none q-mb-md">Detalle de Productos</h6>
              </div>

              <div class="col-12">
                <q-table
                  :rows="ordenSeleccionada.detalles || []"
                  :columns="columnsDetallesVer"
                  row-key="id_detalle_oc"
                  flat
                  bordered
                  separator="cell"
                  dense
                >
                  <template v-slot:body-cell-producto="props">
                    <q-td :props="props">
                      <div>
                        <div class="text-weight-bold">{{ props.row.producto?.sku }}</div>
                        <div class="text-caption">{{ props.row.producto?.nombre_producto }}</div>
                      </div>
                    </q-td>
                  </template>

                  <template v-slot:body-cell-precio_unitario="props">
                    <q-td :props="props">
                      {{ formatCurrency(props.value) }}
                    </q-td>
                  </template>

                  <template v-slot:body-cell-subtotal_linea="props">
                    <q-td :props="props">
                      {{ formatCurrency(props.value) }}
                    </q-td>
                  </template>

                  <template v-slot:body-cell-total_linea="props">
                    <q-td :props="props">
                      <span class="text-weight-bold">
                        {{ formatCurrency(props.value) }}
                      </span>
                    </q-td>
                  </template>
                </q-table>
              </div>
            </div>

            <!-- Botones de acción -->
            <div class="row justify-end q-gutter-md q-mt-lg">
              <q-btn
                label="Cerrar"
                color="grey"
                flat
                @click="cerrarDetalle"
              />
              <q-btn
                v-if="puedeEditar(ordenSeleccionada)"
                label="Editar"
                color="primary"
                @click="editarOrdenCompraDesdeDetalle"
              />
              <q-btn
                v-if="puedeEjecutarAccion(ordenSeleccionada)"
                :label="getAccionLabel(ordenSeleccionada.estado)"
                :color="getAccionColor(ordenSeleccionada.estado)"
                @click="ejecutarAccion(ordenSeleccionada)"
              />
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useQuasar } from 'quasar'
import { useOrdenCompraStore, type OrdenCompra, type OrdenCompraCreate, type OrdenCompraDetalle, type OrdenCompraDetalleCreate } from '@/stores/ordenesCompra'

const $q = useQuasar()
const ordenCompraStore = useOrdenCompraStore()

// Estado reactivo
const mostrarFormulario = ref(false)
const mostrarSelectorProducto = ref(false)
const mostrarDetalle = ref(false)
const modoEdicion = ref(false)
const guardando = ref(false)
const cargandoProductos = ref(false)
const busquedaProducto = ref('')
const busquedaProveedor = ref('')
const productoSeleccionado = ref([])
const ordenSeleccionada = ref<OrdenCompra | null>(null)

// Filtros
const filtros = reactive({
  busqueda: '',
  proveedor: null,
  estado: null,
  fechaDesde: '',
  fechaHasta: ''
})

// Paginación
const paginacion = ref({
  sortBy: 'fecha_orden',
  descending: true,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
})

// Formulario
const formularioInicial = {
  numero_orden: '',
  id_proveedor: null,
  fecha_orden: new Date().toISOString().split('T')[0],
  fecha_requerida: '',
  fecha_prometida: '',
  estado: 'BORRADOR',
  subtotal: 0,
  impuestos: 0,
  descuentos: 0,
  total: 0,
  moneda: 'CLP',
  tipo_cambio: 1,
  condiciones_pago: '',
  terminos_entrega: '',
  lugar_entrega: '',
  contacto_proveedor: '',
  observaciones: '',
  activo: true,
  detalles: [] as OrdenCompraDetalleCreate[]
}

const formulario = reactive({ ...formularioInicial })

// Computed
const isLoading = computed(() => ordenCompraStore.isLoading)

const ordenesCompraFiltradas = computed(() => {
  let ordenes = ordenCompraStore.ordenesCompra

  if (filtros.busqueda) {
    ordenes = ordenes.filter(orden =>
      orden.numero_orden.toLowerCase().includes(filtros.busqueda.toLowerCase())
    )
  }

  if (filtros.proveedor) {
    ordenes = ordenes.filter(orden => orden.id_proveedor === filtros.proveedor)
  }

  if (filtros.estado) {
    ordenes = ordenes.filter(orden => orden.estado === filtros.estado)
  }

  return ordenes
})

const proveedoresOptions = computed(() =>
  ordenCompraStore.proveedores.map(proveedor => ({
    label: proveedor.razon_social,
    value: proveedor.id_proveedor,
    rut: proveedor.rut_proveedor,
    email: proveedor.email,
    telefono: proveedor.telefono
  }))
)

const proveedoresFiltrados = ref(proveedoresOptions.value)

const estadosOptions = computed(() =>
  ordenCompraStore.estadosOrdenCompra.map(estado => ({
    label: estado.nombre_estado,
    value: estado.estado
  }))
)

const monedasOptions = [
  { label: 'Peso Chileno (CLP)', value: 'CLP' },
  { label: 'Dólar Americano (USD)', value: 'USD' },
  { label: 'Euro (EUR)', value: 'EUR' }
]

const productosDisponibles = computed(() => ordenCompraStore.productos)

const totales = computed(() => {
  const subtotal = formulario.detalles.reduce((sum, detalle) => sum + (detalle.subtotal_linea || 0), 0)
  const descuentos = formulario.detalles.reduce((sum, detalle) => sum + (detalle.descuento_monto || 0), 0)
  const impuestos = formulario.detalles.reduce((sum, detalle) => sum + (detalle.impuesto_monto || 0), 0)
  const total = subtotal - descuentos + impuestos

  formulario.subtotal = subtotal
  formulario.descuentos = descuentos
  formulario.impuestos = impuestos
  formulario.total = total

  return { subtotal, descuentos, impuestos, total }
})

const formularioValido = computed(() => {
  return formulario.id_proveedor &&
         formulario.fecha_orden &&
         formulario.fecha_requerida &&
         formulario.detalles.length > 0
})

// Columnas de la tabla principal
const columnsOrdenesCompra = [
  {
    name: 'numero_orden',
    label: 'Número',
    align: 'left',
    field: 'numero_orden',
    sortable: true
  },
  {
    name: 'proveedor',
    label: 'Proveedor',
    align: 'left',
    field: (row: OrdenCompra) => row.proveedor?.razon_social,
    sortable: true
  },
  {
    name: 'fecha_orden',
    label: 'Fecha Orden',
    align: 'center',
    field: 'fecha_orden',
    sortable: true
  },
  {
    name: 'fecha_requerida',
    label: 'Fecha Requerida',
    align: 'center',
    field: 'fecha_requerida',
    sortable: true
  },
  {
    name: 'estado',
    label: 'Estado',
    align: 'center',
    field: 'estado',
    sortable: true
  },
  {
    name: 'total',
    label: 'Total',
    align: 'right',
    field: 'total',
    sortable: true
  },
  {
    name: 'activo',
    label: 'Estado',
    align: 'center',
    field: 'activo',
    sortable: true
  },
  {
    name: 'acciones',
    label: 'Acciones',
    align: 'center',
    field: 'acciones',
    sortable: false
  }
]

// Columnas para detalles en formulario
const columnsDetalles = [
  {
    name: 'producto',
    label: 'Producto',
    align: 'left',
    field: 'producto'
  },
  {
    name: 'cantidad_solicitada',
    label: 'Cantidad',
    align: 'center',
    field: 'cantidad_solicitada'
  },
  {
    name: 'precio_unitario',
    label: 'Precio Unit.',
    align: 'right',
    field: 'precio_unitario'
  },
  {
    name: 'descuento_porcentaje',
    label: 'Desc. %',
    align: 'center',
    field: 'descuento_porcentaje'
  },
  {
    name: 'impuesto_porcentaje',
    label: 'IVA %',
    align: 'center',
    field: 'impuesto_porcentaje'
  },
  {
    name: 'total_linea',
    label: 'Total',
    align: 'right',
    field: 'total_linea'
  },
  {
    name: 'acciones',
    label: 'Acciones',
    align: 'center',
    field: 'acciones'
  }
]

// Columnas para ver detalles
const columnsDetallesVer = [
  {
    name: 'numero_linea',
    label: 'Línea',
    align: 'center',
    field: 'numero_linea'
  },
  {
    name: 'producto',
    label: 'Producto',
    align: 'left',
    field: 'producto'
  },
  {
    name: 'cantidad_solicitada',
    label: 'Cant. Solicitada',
    align: 'center',
    field: 'cantidad_solicitada'
  },
  {
    name: 'cantidad_recibida',
    label: 'Cant. Recibida',
    align: 'center',
    field: 'cantidad_recibida'
  },
  {
    name: 'precio_unitario',
    label: 'Precio Unit.',
    align: 'right',
    field: 'precio_unitario'
  },
  {
    name: 'descuento_porcentaje',
    label: 'Desc. %',
    align: 'center',
    field: 'descuento_porcentaje'
  },
  {
    name: 'impuesto_porcentaje',
    label: 'IVA %',
    align: 'center',
    field: 'impuesto_porcentaje'
  },
  {
    name: 'subtotal_linea',
    label: 'Subtotal',
    align: 'right',
    field: 'subtotal_linea'
  },
  {
    name: 'total_linea',
    label: 'Total',
    align: 'right',
    field: 'total_linea'
  }
]

// Columnas para selector de productos
const columnsProductos = [
  {
    name: 'sku',
    label: 'SKU',
    align: 'left',
    field: 'sku',
    sortable: true
  },
  {
    name: 'nombre_producto',
    label: 'Nombre',
    align: 'left',
    field: 'nombre_producto',
    sortable: true
  },
  {
    name: 'descripcion_corta',
    label: 'Descripción',
    align: 'left',
    field: 'descripcion_corta'
  },
  {
    name: 'stock_actual',
    label: 'Stock',
    align: 'center',
    field: 'stock_actual'
  },
  {
    name: 'precio_venta',
    label: 'Precio Venta',
    align: 'right',
    field: 'precio_venta'
  },
  {
    name: 'costo_promedio',
    label: 'Costo Promedio',
    align: 'right',
    field: 'costo_promedio'
  }
]

// Métodos
const cargarDatos = async () => {
  try {
    await Promise.all([
      ordenCompraStore.obtenerOrdenesCompra(),
      ordenCompraStore.obtenerEstadosOrdenCompra(),
      ordenCompraStore.obtenerProveedores()
    ])
    // Actualizar lista filtrada de proveedores después de cargar datos
    proveedoresFiltrados.value = proveedoresOptions.value
  } catch (error) {
    console.error('Error cargando datos:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al cargar los datos'
    })
  }
}

const buscarOrdenesCompra = async () => {
  try {
    const params: any = {}

    if (filtros.proveedor) params.proveedor_id = filtros.proveedor
    if (filtros.estado) params.estado = filtros.estado
    if (filtros.fechaDesde) params.fecha_desde = filtros.fechaDesde
    if (filtros.fechaHasta) params.fecha_hasta = filtros.fechaHasta

    if (filtros.busqueda) {
      await ordenCompraStore.buscarOrdenesCompra(filtros.busqueda, params)
    } else {
      await ordenCompraStore.obtenerOrdenesCompra(params)
    }
  } catch (error) {
    console.error('Error buscando órdenes de compra:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al buscar órdenes de compra'
    })
  }
}

const onRequestOrdenesCompra = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await buscarOrdenesCompra()
}

const abrirFormularioOrdenCompra = () => {
  Object.assign(formulario, formularioInicial)
  formulario.detalles = []
  modoEdicion.value = false
  mostrarFormulario.value = true
}

const editarOrdenCompra = async (orden: OrdenCompra) => {
  try {
    const ordenCompleta = await ordenCompraStore.obtenerOrdenCompra(orden.id_orden_compra)
    const detalles = await ordenCompraStore.obtenerDetallesOrdenCompra(orden.id_orden_compra)

    Object.assign(formulario, {
      ...ordenCompleta,
      detalles: detalles.map(detalle => ({
        numero_linea: detalle.numero_linea,
        id_producto: detalle.id_producto,
        cantidad_solicitada: detalle.cantidad_solicitada,
        precio_unitario: detalle.precio_unitario,
        descuento_porcentaje: detalle.descuento_porcentaje || 0,
        descuento_monto: detalle.descuento_monto || 0,
        impuesto_porcentaje: detalle.impuesto_porcentaje || 19,
        impuesto_monto: detalle.impuesto_monto || 0,
        subtotal_linea: detalle.subtotal_linea,
        total_linea: detalle.total_linea,
        especificaciones: detalle.especificaciones,
        observaciones: detalle.observaciones,
        fecha_requerida: detalle.fecha_requerida,
        fecha_prometida: detalle.fecha_prometida,
        activo: detalle.activo,
        producto: detalle.producto
      }))
    })

    modoEdicion.value = true
    mostrarFormulario.value = true
  } catch (error) {
    console.error('Error cargando orden para editar:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al cargar la orden de compra'
    })
  }
}

const cerrarFormulario = () => {
  mostrarFormulario.value = false
  Object.assign(formulario, formularioInicial)
  formulario.detalles = []
}

const guardarOrdenCompra = async () => {
  try {
    guardando.value = true

    const ordenData: OrdenCompraCreate = {
      numero_orden: formulario.numero_orden,
      id_proveedor: formulario.id_proveedor!,
      fecha_orden: formulario.fecha_orden,
      fecha_requerida: formulario.fecha_requerida,
      fecha_prometida: formulario.fecha_prometida,
      estado: 'PENDIENTE',
      subtotal: formulario.subtotal,
      impuestos: formulario.impuestos,
      descuentos: formulario.descuentos,
      total: formulario.total,
      moneda: formulario.moneda,
      tipo_cambio: formulario.tipo_cambio,
      condiciones_pago: formulario.condiciones_pago,
      terminos_entrega: formulario.terminos_entrega,
      lugar_entrega: formulario.lugar_entrega,
      contacto_proveedor: formulario.contacto_proveedor,
      observaciones: formulario.observaciones,
      activo: true,
      detalles: formulario.detalles
    }

    if (modoEdicion.value) {
      await ordenCompraStore.actualizarOrdenCompra(formulario.id_orden_compra!, ordenData)
    } else {
      await ordenCompraStore.crearOrdenCompra(ordenData)
    }

    $q.notify({
      type: 'positive',
      message: `Orden de compra ${modoEdicion.value ? 'actualizada' : 'creada'} exitosamente`
    })

    cerrarFormulario()
    await cargarDatos()
  } catch (error) {
    console.error('Error guardando orden de compra:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al guardar la orden de compra'
    })
  } finally {
    guardando.value = false
  }
}

const guardarBorrador = async () => {
  try {
    guardando.value = true

    const ordenData: OrdenCompraCreate = {
      numero_orden: formulario.numero_orden,
      id_proveedor: formulario.id_proveedor!,
      fecha_orden: formulario.fecha_orden,
      fecha_requerida: formulario.fecha_requerida,
      fecha_prometida: formulario.fecha_prometida,
      estado: 'BORRADOR',
      subtotal: formulario.subtotal,
      impuestos: formulario.impuestos,
      descuentos: formulario.descuentos,
      total: formulario.total,
      moneda: formulario.moneda,
      tipo_cambio: formulario.tipo_cambio,
      condiciones_pago: formulario.condiciones_pago,
      terminos_entrega: formulario.terminos_entrega,
      lugar_entrega: formulario.lugar_entrega,
      contacto_proveedor: formulario.contacto_proveedor,
      observaciones: formulario.observaciones,
      activo: true,
      detalles: formulario.detalles
    }

    if (modoEdicion.value) {
      await ordenCompraStore.actualizarOrdenCompra(formulario.id_orden_compra!, ordenData)
    } else {
      await ordenCompraStore.crearOrdenCompra(ordenData)
    }

    $q.notify({
      type: 'positive',
      message: 'Borrador guardado exitosamente'
    })

    cerrarFormulario()
    await cargarDatos()
  } catch (error) {
    console.error('Error guardando borrador:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al guardar el borrador'
    })
  } finally {
    guardando.value = false
  }
}

const abrirSelectorProducto = async () => {
  try {
    await ordenCompraStore.obtenerProductos({ activo: true })
    mostrarSelectorProducto.value = true
  } catch (error) {
    console.error('Error cargando productos:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al cargar productos'
    })
  }
}

const cerrarSelectorProducto = () => {
  mostrarSelectorProducto.value = false
  productoSeleccionado.value = []
  busquedaProducto.value = ''
}

const buscarProductos = async () => {
  try {
    cargandoProductos.value = true
    await ordenCompraStore.obtenerProductos({
      activo: true,
      busqueda: busquedaProducto.value
    })
  } catch (error) {
    console.error('Error buscando productos:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al buscar productos'
    })
  } finally {
    cargandoProductos.value = false
  }
}

const agregarProductoSeleccionado = () => {
  if (productoSeleccionado.value.length === 0) return

  const producto = productoSeleccionado.value[0]
  const numeroLinea = Math.max(0, ...formulario.detalles.map(d => d.numero_linea)) + 1

  const nuevoDetalle: OrdenCompraDetalleCreate = {
    numero_linea: numeroLinea,
    id_producto: producto.id_producto,
    cantidad_solicitada: 1,
    precio_unitario: producto.costo_promedio || 0,
    descuento_porcentaje: 0,
    descuento_monto: 0,
    impuesto_porcentaje: 19,
    impuesto_monto: 0,
    subtotal_linea: 0,
    total_linea: 0,
    especificaciones: '',
    observaciones: '',
    activo: true,
    producto: producto
  }

  calcularTotalLinea(nuevoDetalle)
  formulario.detalles.push(nuevoDetalle)

  cerrarSelectorProducto()
}

const calcularTotalLinea = (detalle: any) => {
  const cantidad = detalle.cantidad_solicitada || 0
  const precio = detalle.precio_unitario || 0
  const descuentoPct = detalle.descuento_porcentaje || 0
  const impuestoPct = detalle.impuesto_porcentaje || 19

  const subtotal = cantidad * precio
  const descuentoMonto = (subtotal * descuentoPct) / 100
  const base = subtotal - descuentoMonto
  const impuestoMonto = (base * impuestoPct) / 100

  detalle.subtotal_linea = subtotal
  detalle.descuento_monto = descuentoMonto
  detalle.impuesto_monto = impuestoMonto
  detalle.total_linea = base + impuestoMonto
}

const eliminarDetalle = (index: number) => {
  formulario.detalles.splice(index, 1)
}

const onProveedorChange = (proveedorId: number) => {
  const proveedor = ordenCompraStore.proveedores.find(p => p.id_proveedor === proveedorId)
  if (proveedor) {
    formulario.contacto_proveedor = proveedor.nombre_contacto || ''
  }
}

const verOrdenCompra = async (orden: OrdenCompra) => {
  try {
    const ordenCompleta = await ordenCompraStore.obtenerOrdenCompra(orden.id_orden_compra)
    const detalles = await ordenCompraStore.obtenerDetallesOrdenCompra(orden.id_orden_compra)

    ordenSeleccionada.value = {
      ...ordenCompleta,
      detalles
    }

    mostrarDetalle.value = true
  } catch (error) {
    console.error('Error cargando detalle de orden:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al cargar el detalle de la orden'
    })
  }
}

const cerrarDetalle = () => {
  mostrarDetalle.value = false
  ordenSeleccionada.value = null
}

const editarOrdenCompraDesdeDetalle = () => {
  cerrarDetalle()
  if (ordenSeleccionada.value) {
    editarOrdenCompra(ordenSeleccionada.value)
  }
}

const duplicarOrdenCompra = async (orden: OrdenCompra) => {
  try {
    await ordenCompraStore.duplicarOrdenCompra(orden.id_orden_compra)
    $q.notify({
      type: 'positive',
      message: 'Orden de compra duplicada exitosamente'
    })
    await cargarDatos()
  } catch (error) {
    console.error('Error duplicando orden:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al duplicar la orden de compra'
    })
  }
}

const ejecutarAccion = async (orden: OrdenCompra) => {
  const accionesMap: { [key: string]: () => Promise<void> } = {
    'BORRADOR': () => aprobar(orden),
    'PENDIENTE': () => autorizar(orden),
    'APROBADA': () => enviar(orden),
    'ENVIADA': () => cerrar(orden)
  }

  const accion = accionesMap[orden.estado]
  if (accion) {
    await accion()
  }
}

const aprobar = async (orden: OrdenCompra) => {
  try {
    await ordenCompraStore.aprobarOrdenCompra(orden.id_orden_compra, 1) // TODO: usar ID del usuario actual
    $q.notify({
      type: 'positive',
      message: 'Orden de compra aprobada exitosamente'
    })
    await cargarDatos()
  } catch (error) {
    console.error('Error aprobando orden:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al aprobar la orden de compra'
    })
  }
}

const autorizar = async (orden: OrdenCompra) => {
  try {
    await ordenCompraStore.autorizarOrdenCompra(orden.id_orden_compra, 1) // TODO: usar ID del usuario actual
    $q.notify({
      type: 'positive',
      message: 'Orden de compra autorizada exitosamente'
    })
    await cargarDatos()
  } catch (error) {
    console.error('Error autorizando orden:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al autorizar la orden de compra'
    })
  }
}

const enviar = async (orden: OrdenCompra) => {
  try {
    await ordenCompraStore.enviarOrdenCompra(orden.id_orden_compra, 1) // TODO: usar ID del usuario actual
    $q.notify({
      type: 'positive',
      message: 'Orden de compra enviada exitosamente'
    })
    await cargarDatos()
  } catch (error) {
    console.error('Error enviando orden:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al enviar la orden de compra'
    })
  }
}

const cerrar = async (orden: OrdenCompra) => {
  try {
    await ordenCompraStore.cerrarOrdenCompra(orden.id_orden_compra)
    $q.notify({
      type: 'positive',
      message: 'Orden de compra cerrada exitosamente'
    })
    await cargarDatos()
  } catch (error) {
    console.error('Error cerrando orden:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al cerrar la orden de compra'
    })
  }
}

const eliminarOrdenCompra = async (orden: OrdenCompra) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de que desea eliminar la orden de compra ${orden.numero_orden}?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await ordenCompraStore.eliminarOrdenCompra(orden.id_orden_compra)
      $q.notify({
        type: 'positive',
        message: 'Orden de compra eliminada exitosamente'
      })
      await cargarDatos()
    } catch (error) {
      console.error('Error eliminando orden:', error)
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar la orden de compra'
      })
    }
  })
}

// Funciones de utilidad
const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP'
  }).format(value || 0)
}

const formatDate = (date: string): string => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('es-CL')
}

const getEstadoColor = (estado: string): string => {
  const colores: { [key: string]: string } = {
    'BORRADOR': 'grey',
    'PENDIENTE': 'orange',
    'APROBADA': 'blue',
    'ENVIADA': 'purple',
    'RECIBIDA': 'green',
    'FACTURADA': 'teal',
    'CONCILIADA': 'indigo',
    'PAGADA': 'positive',
    'CERRADA': 'dark',
    'CANCELADA': 'negative'
  }
  return colores[estado] || 'grey'
}

const getDateClass = (fecha: string): string => {
  if (!fecha) return ''

  const today = new Date()
  const dateToCheck = new Date(fecha)
  const diffTime = dateToCheck.getTime() - today.getTime()
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays < 0) return 'text-red text-weight-bold' // Vencida
  if (diffDays <= 3) return 'text-orange text-weight-bold' // Por vencer
  return '' // Normal
}

const puedeEditar = (orden: OrdenCompra): boolean => {
  return ['BORRADOR', 'PENDIENTE'].includes(orden.estado)
}

const puedeEliminar = (orden: OrdenCompra): boolean => {
  return ['BORRADOR', 'PENDIENTE'].includes(orden.estado)
}

const puedeEjecutarAccion = (orden: OrdenCompra): boolean => {
  return ['BORRADOR', 'PENDIENTE', 'APROBADA', 'ENVIADA'].includes(orden.estado)
}

const getAccionColor = (estado: string): string => {
  const colores: { [key: string]: string } = {
    'BORRADOR': 'blue',
    'PENDIENTE': 'green',
    'APROBADA': 'purple',
    'ENVIADA': 'teal'
  }
  return colores[estado] || 'grey'
}

const getAccionIcon = (estado: string): string => {
  const iconos: { [key: string]: string } = {
    'BORRADOR': 'check',
    'PENDIENTE': 'verified',
    'APROBADA': 'send',
    'ENVIADA': 'done_all'
  }
  return iconos[estado] || 'more_horiz'
}

const getAccionTooltip = (estado: string): string => {
  const tooltips: { [key: string]: string } = {
    'BORRADOR': 'Aprobar',
    'PENDIENTE': 'Autorizar',
    'APROBADA': 'Enviar',
    'ENVIADA': 'Cerrar'
  }
  return tooltips[estado] || 'Acción'
}

const getAccionLabel = (estado: string): string => {
  const labels: { [key: string]: string } = {
    'BORRADOR': 'Aprobar',
    'PENDIENTE': 'Autorizar',
    'APROBADA': 'Enviar',
    'ENVIADA': 'Cerrar'
  }
  return labels[estado] || 'Acción'
}

// Funciones de autocompletado de proveedores
const filtrarProveedores = (val: string, update: (fn: () => void) => void) => {
  busquedaProveedor.value = val

  update(() => {
    if (val === '') {
      proveedoresFiltrados.value = proveedoresOptions.value
    } else {
      const needle = val.toLowerCase()
      proveedoresFiltrados.value = proveedoresOptions.value.filter(proveedor =>
        proveedor.label.toLowerCase().includes(needle) ||
        (proveedor.rut && proveedor.rut.toLowerCase().includes(needle))
      )
    }
  })
}

const limpiarFiltroProveedores = () => {
  busquedaProveedor.value = ''
  proveedoresFiltrados.value = proveedoresOptions.value
}

// Lifecycle
onMounted(() => {
  cargarDatos()
})
</script>

<style scoped>
.dialog-card {
  min-height: 50vh;
}

.scroll {
  overflow-y: auto;
}
</style>