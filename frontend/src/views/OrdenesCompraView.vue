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
      <q-dialog v-model="mostrarFormulario" persistent>
        <q-card style="min-width: 1200px; max-width: 1400px; max-height: 90vh">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">{{ modoEdicion ? 'Editar' : 'Nueva' }} Orden de Compra</div>
            <q-space />
            <q-btn icon="close" flat round dense @click="cerrarFormulario" />
          </q-card-section>

          <q-card-section class="q-pt-none" style="max-height: calc(90vh - 120px);">
            <q-form @submit="guardarOrdenCompra">
              <div class="row" style="height: calc(90vh - 160px);">
                <div class="col-3">
                  <q-tabs
                    v-model="tabActivoOrden"
                    vertical
                    class="text-primary full-height"
                  >
                    <q-tab name="general" icon="info" label="Información General" />
                    <q-tab name="condiciones" icon="assignment" label="Condiciones" />
                    <q-tab name="productos" icon="inventory" label="Productos" />
                    <q-tab name="resumen" icon="summarize" label="Resumen" />
                  </q-tabs>
                </div>
                <div class="col-9">
                  <q-tab-panels
                    v-model="tabActivoOrden"
                    animated
                    class="full-height"
                    style="overflow-y: auto;"
                  >
                    <!-- Panel Información General -->
                    <q-tab-panel name="general">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="info" class="q-mr-sm" />
                        Información General
                      </div>

                      <div class="row q-gutter-md">
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
                                  <q-item-label>{{ scope.opt.razon_social }}</q-item-label>
                                  <q-item-label caption>RUT: {{ scope.opt.rfc }}</q-item-label>
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
                            label="Moneda *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'Moneda es requerida']"
                          />
                        </div>

                        <div class="col-md-3 col-sm-6 col-xs-12">
                          <q-input
                            v-model.number="formulario.tipo_cambio"
                            type="number"
                            label="Tipo de Cambio"
                            outlined
                            dense
                            step="0.0001"
                            min="0"
                            hint="1 para moneda nacional"
                          />
                        </div>

                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-input
                            v-model="formulario.observaciones"
                            label="Observaciones"
                            type="textarea"
                            outlined
                            dense
                            rows="3"
                            hint="Observaciones generales de la orden"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Condiciones -->
                    <q-tab-panel name="condiciones">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="assignment" class="q-mr-sm" />
                        Condiciones de Pago y Entrega
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-input
                            v-model="formulario.condiciones_pago"
                            label="Condiciones de Pago"
                            outlined
                            dense
                            hint="Ej: 30 días fecha factura, Contado, etc."
                          />
                        </div>


                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-input
                            v-model="formulario.lugar_entrega"
                            label="Lugar de Entrega"
                            outlined
                            dense
                            hint="Dirección completa de entrega"
                          />
                        </div>

                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-input
                            v-model="formulario.contacto_proveedor"
                            label="Contacto del Proveedor"
                            outlined
                            dense
                            hint="Persona de contacto en el proveedor"
                          />
                        </div>

                        <div class="col-12">
                          <q-separator class="q-my-md" />
                          <div class="text-h6 q-mb-md">
                            <q-icon name="local_shipping" class="q-mr-sm" />
                            Información de Envío
                          </div>
                        </div>

                        <div class="col-md-4 col-sm-6 col-xs-12">
                          <q-input
                            v-model.number="formulario.plazo_entrega"
                            type="number"
                            label="Plazo de Entrega (días)"
                            outlined
                            dense
                            min="1"
                            hint="Días hábiles para la entrega"
                          />
                        </div>

                        <div class="col-md-4 col-sm-6 col-xs-12">
                          <q-select
                            v-model="formulario.prioridad"
                            :options="prioridadOptions"
                            label="Prioridad"
                            outlined
                            dense
                            emit-value
                            map-options
                          />
                        </div>

                        <div class="col-md-4 col-sm-6 col-xs-12">
                          <q-select
                            v-model="formulario.metodo_envio"
                            :options="metodosEnvioOptions"
                            label="Método de Envío"
                            outlined
                            dense
                            emit-value
                            map-options
                          />
                        </div>

                        <div class="col-12">
                          <q-input
                            v-model="formulario.terminos_condiciones"
                            label="Términos y Condiciones Específicos"
                            type="textarea"
                            outlined
                            dense
                            rows="4"
                            hint="Condiciones particulares para esta orden"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Productos -->
                    <q-tab-panel name="productos">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="inventory" class="q-mr-sm" />
                        Productos
                      </div>

                      <!-- Botón para agregar productos -->
                      <div class="row q-mb-md">
                        <q-btn
                          color="primary"
                          icon="add"
                          label="Agregar Producto"
                          @click="abrirSelectorProducto"
                        />
                      </div>

                      <!-- Tabla de productos -->
                      <q-table
                        :rows="formulario.detalles"
                        :columns="columnsDetalles"
                        row-key="numero_linea"
                        flat
                        bordered
                        :hide-bottom="formulario.detalles.length === 0"
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
                              min="1"
                              step="1"
                              dense
                              outlined
                              style="min-width: 80px"
                              @update:model-value="calcularTotalLinea(props.row)"
                              hide-bottom-space
                            />
                          </q-td>
                        </template>

                        <template v-slot:body-cell-precio_unitario="props">
                          <q-td :props="props">
                            <q-input
                              v-model.number="props.row.precio_unitario"
                              type="number"
                              min="0"
                              step="0.01"
                              dense
                              outlined
                              style="min-width: 100px"
                              @update:model-value="calcularTotalLinea(props.row)"
                              hide-bottom-space
                            />
                          </q-td>
                        </template>

                        <template v-slot:body-cell-descuento_porcentaje="props">
                          <q-td :props="props">
                            <q-input
                              v-model.number="props.row.descuento_porcentaje"
                              type="number"
                              min="0"
                              max="100"
                              step="0.01"
                              dense
                              outlined
                              style="min-width: 80px"
                              @update:model-value="calcularTotalLinea(props.row)"
                              hide-bottom-space
                            />
                          </q-td>
                        </template>

                        <template v-slot:body-cell-impuesto_porcentaje="props">
                          <q-td :props="props">
                            <q-input
                              v-model.number="props.row.impuesto_porcentaje"
                              type="number"
                              min="0"
                              max="100"
                              step="0.01"
                              dense
                              outlined
                              style="min-width: 80px"
                              @update:model-value="calcularTotalLinea(props.row)"
                              hide-bottom-space
                            />
                          </q-td>
                        </template>

                        <template v-slot:body-cell-total_linea="props">
                          <q-td :props="props">
                            <span class="text-weight-bold">
                              {{ formatCurrency(props.row.total_linea || 0) }}
                            </span>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-acciones="props">
                          <q-td :props="props">
                            <div class="row items-center justify-center q-gutter-xs">
                              <q-btn
                                size="sm"
                                color="red"
                                icon="delete"
                                @click="eliminarDetalle(props.rowIndex)"
                                dense
                                round
                                style="height: 32px; width: 32px;"
                              >
                                <q-tooltip>Eliminar</q-tooltip>
                              </q-btn>
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:no-data>
                          <div class="full-width row flex-center q-gutter-sm">
                            <q-icon size="2em" name="inventory" />
                            <span>
                              No hay productos agregados. Haga clic en "Agregar Producto" para comenzar.
                            </span>
                          </div>
                        </template>
                      </q-table>

                      <!-- Información adicional de productos -->
                      <div class="row q-mt-md" v-if="formulario.detalles.length > 0">
                        <div class="col-12">
                          <q-expansion-item
                            icon="info"
                            label="Especificaciones y Observaciones"
                            dense
                          >
                            <div class="q-pa-md">
                              <div class="row q-gutter-md">
                                <div class="col-12">
                                  <q-input
                                    v-model="especificacionesGenerales"
                                    label="Especificaciones Generales"
                                    type="textarea"
                                    outlined
                                    dense
                                    rows="3"
                                    hint="Aplicar a todos los productos"
                                  />
                                </div>
                                <div class="col-12">
                                  <q-input
                                    v-model="observacionesGenerales"
                                    label="Observaciones Generales"
                                    type="textarea"
                                    outlined
                                    dense
                                    rows="3"
                                    hint="Notas adicionales para todos los productos"
                                  />
                                </div>
                              </div>
                            </div>
                          </q-expansion-item>
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Resumen -->
                    <q-tab-panel name="resumen">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="summarize" class="q-mr-sm" />
                        Resumen de la Orden
                      </div>

                      <div class="row q-gutter-md">
                        <!-- Información general -->
                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-card flat bordered>
                            <q-card-section>
                              <div class="text-h6 q-mb-md">
                                <q-icon name="info" class="q-mr-sm" />
                                Información General
                              </div>

                              <div class="row q-gutter-sm">
                                <div class="col-12">
                                  <q-field label="Proveedor" stack-label outlined readonly dense>
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline" tabindex="-1">
                                        <div>{{ proveedorSeleccionado?.label || 'No seleccionado' }}</div>
                                        <div class="text-caption text-grey-6" v-if="proveedorSeleccionado?.rfc">
                                          RUT: {{ proveedorSeleccionado.rfc }}
                                        </div>
                                      </div>
                                    </template>
                                  </q-field>
                                </div>

                                <div class="col-6">
                                  <q-field label="Fecha de Orden" stack-label outlined readonly dense>
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline" tabindex="-1">
                                        {{ formatDate(formulario.fecha_orden) }}
                                      </div>
                                    </template>
                                  </q-field>
                                </div>

                                <div class="col-6">
                                  <q-field label="Fecha Requerida" stack-label outlined readonly dense>
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline" tabindex="-1">
                                        {{ formatDate(formulario.fecha_requerida) }}
                                      </div>
                                    </template>
                                  </q-field>
                                </div>

                                <div class="col-6">
                                  <q-field label="Moneda" stack-label outlined readonly dense>
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline" tabindex="-1">
                                        {{ formulario.moneda }}
                                      </div>
                                    </template>
                                  </q-field>
                                </div>

                                <div class="col-6">
                                  <q-field label="Tipo de Cambio" stack-label outlined readonly dense>
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline" tabindex="-1">
                                        {{ formulario.tipo_cambio }}
                                      </div>
                                    </template>
                                  </q-field>
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </div>

                        <!-- Totales -->
                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-card flat bordered>
                            <q-card-section>
                              <div class="text-h6 q-mb-md">
                                <q-icon name="calculate" class="q-mr-sm" />
                                Totales
                              </div>

                              <div class="row q-gutter-sm">
                                <div class="col-6">
                                  <q-field label="Subtotal" stack-label outlined readonly dense>
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline text-right" tabindex="-1">
                                        {{ formatCurrency(totales.subtotal) }}
                                      </div>
                                    </template>
                                  </q-field>
                                </div>

                                <div class="col-6">
                                  <q-field label="Descuentos" stack-label outlined readonly dense>
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline text-right text-red" tabindex="-1">
                                        {{ formatCurrency(totales.descuentos) }}
                                      </div>
                                    </template>
                                  </q-field>
                                </div>

                                <div class="col-6">
                                  <q-field label="Impuestos (IVA)" stack-label outlined readonly dense>
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline text-right" tabindex="-1">
                                        {{ formatCurrency(totales.impuestos) }}
                                      </div>
                                    </template>
                                  </q-field>
                                </div>

                                <div class="col-6">
                                  <q-field label="Total General" stack-label outlined readonly dense class="bg-primary text-white">
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline text-right text-weight-bold text-white" tabindex="-1">
                                        {{ formatCurrency(totales.total) }}
                                      </div>
                                    </template>
                                  </q-field>
                                </div>

                                <div class="col-12">
                                  <q-field label="Cantidad de Items" stack-label outlined readonly dense>
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline text-center" tabindex="-1">
                                        {{ formulario.detalles.length }} productos
                                      </div>
                                    </template>
                                  </q-field>
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </div>

                        <!-- Resumen de productos -->
                        <div class="col-12" v-if="formulario.detalles.length > 0">
                          <q-card flat bordered>
                            <q-card-section>
                              <div class="text-h6 q-mb-md">
                                <q-icon name="inventory" class="q-mr-sm" />
                                Resumen de Productos
                              </div>

                              <q-table
                                :rows="formulario.detalles"
                                :columns="columnsResumen"
                                row-key="numero_linea"
                                flat
                                bordered
                                dense
                                :hide-bottom="true"
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
                                    {{ formatCurrency(props.row.precio_unitario || 0) }}
                                  </q-td>
                                </template>

                                <template v-slot:body-cell-total_linea="props">
                                  <q-td :props="props">
                                    <span class="text-weight-bold">
                                      {{ formatCurrency(props.row.total_linea || 0) }}
                                    </span>
                                  </q-td>
                                </template>
                              </q-table>
                            </q-card-section>
                          </q-card>
                        </div>

                        <!-- Condiciones -->
                        <div class="col-12">
                          <q-card flat bordered>
                            <q-card-section>
                              <div class="text-h6 q-mb-md">
                                <q-icon name="assignment" class="q-mr-sm" />
                                Condiciones y Observaciones
                              </div>

                              <div class="row q-gutter-md">
                                <div class="col-md-4 col-sm-6 col-xs-12">
                                  <q-field label="Condiciones de Pago" stack-label outlined readonly dense>
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline" tabindex="-1">
                                        {{ formulario.condiciones_pago || 'No especificado' }}
                                      </div>
                                    </template>
                                  </q-field>
                                </div>


                                <div class="col-md-4 col-sm-6 col-xs-12">
                                  <q-field label="Lugar de Entrega" stack-label outlined readonly dense>
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline" tabindex="-1">
                                        {{ formulario.lugar_entrega || 'No especificado' }}
                                      </div>
                                    </template>
                                  </q-field>
                                </div>

                                <div class="col-12" v-if="formulario.observaciones">
                                  <q-field label="Observaciones" stack-label outlined readonly dense>
                                    <template v-slot:control>
                                      <div class="self-center full-width no-outline" tabindex="-1">
                                        {{ formulario.observaciones }}
                                      </div>
                                    </template>
                                  </q-field>
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </div>

                        <!-- Validación -->
                        <div class="col-12">
                          <q-card flat bordered :class="formularioValido ? 'bg-green-1' : 'bg-red-1'">
                            <q-card-section>
                              <div class="text-h6 q-mb-md">
                                <q-icon
                                  :name="formularioValido ? 'check_circle' : 'error'"
                                  :color="formularioValido ? 'green' : 'red'"
                                  class="q-mr-sm"
                                />
                                Estado de Validación
                              </div>

                              <div class="row">
                                <div class="col-12">
                                  <q-list dense>
                                    <q-item>
                                      <q-item-section avatar>
                                        <q-icon
                                          :name="formulario.id_proveedor ? 'check_circle' : 'error'"
                                          :color="formulario.id_proveedor ? 'green' : 'red'"
                                        />
                                      </q-item-section>
                                      <q-item-section>
                                        <q-item-label>Proveedor seleccionado</q-item-label>
                                      </q-item-section>
                                    </q-item>

                                    <q-item>
                                      <q-item-section avatar>
                                        <q-icon
                                          :name="formulario.fecha_orden ? 'check_circle' : 'error'"
                                          :color="formulario.fecha_orden ? 'green' : 'red'"
                                        />
                                      </q-item-section>
                                      <q-item-section>
                                        <q-item-label>Fecha de orden definida</q-item-label>
                                      </q-item-section>
                                    </q-item>

                                    <q-item>
                                      <q-item-section avatar>
                                        <q-icon
                                          :name="formulario.fecha_requerida ? 'check_circle' : 'error'"
                                          :color="formulario.fecha_requerida ? 'green' : 'red'"
                                        />
                                      </q-item-section>
                                      <q-item-section>
                                        <q-item-label>Fecha requerida definida</q-item-label>
                                      </q-item-section>
                                    </q-item>

                                    <q-item>
                                      <q-item-section avatar>
                                        <q-icon
                                          :name="formulario.detalles.length > 0 ? 'check_circle' : 'error'"
                                          :color="formulario.detalles.length > 0 ? 'green' : 'red'"
                                        />
                                      </q-item-section>
                                      <q-item-section>
                                        <q-item-label>Al menos un producto agregado</q-item-label>
                                      </q-item-section>
                                    </q-item>
                                  </q-list>
                                </div>
                              </div>

                              <div class="row q-mt-md" v-if="!formularioValido">
                                <div class="col-12">
                                  <q-banner inline-actions class="text-white bg-red">
                                    <q-icon name="warning" />
                                    La orden no puede ser guardada hasta completar todos los campos requeridos.
                                  </q-banner>
                                </div>
                              </div>
                            </q-card-section>
                          </q-card>
                        </div>
                      </div>
                    </q-tab-panel>
                  </q-tab-panels>
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
                  label="Crear Orden"
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
import { useLogStore } from '@/stores/logs'
import { useAuthStore } from '@/stores/auth'

const $q = useQuasar()
const ordenCompraStore = useOrdenCompraStore()
const logStore = useLogStore()
const authStore = useAuthStore()

// Estado reactivo
const mostrarFormulario = ref(false)
const tabActivoOrden = ref('general')
const mostrarSelectorProducto = ref(false)
const mostrarDetalle = ref(false)
const modoEdicion = ref(false)
const guardando = ref(false)
const cargandoProductos = ref(false)
const busquedaProducto = ref('')
const busquedaProveedor = ref('')
const productoSeleccionado = ref([])
const ordenSeleccionada = ref<OrdenCompra | null>(null)
const especificacionesGenerales = ref('')
const observacionesGenerales = ref('')

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
  estado: 'CREADA',
  subtotal: 0,
  impuestos: 0,
  descuentos: 0,
  total: 0,
  moneda: 'CLP',
  tipo_cambio: 1,
  condiciones_pago: '',
  lugar_entrega: '',
  contacto_proveedor: '',
  plazo_entrega: null,
  prioridad: 'NORMAL',
  metodo_envio: '',
  terminos_condiciones: '',
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
  ordenCompraStore.proveedores.map(proveedor => {
    const rfc = proveedor.rfc || proveedor.rut_proveedor || proveedor.rut || 'Sin RUT'
    return {
      label: `${proveedor.razon_social} - ${rfc}`,
      value: proveedor.id_proveedor,
      rut: rfc,
      rfc: rfc,
      razon_social: proveedor.razon_social,
      email: proveedor.email,
      telefono: proveedor.telefono,
      // Agregar datos completos del proveedor para referencia
      proveedor: proveedor
    }
  })
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

const prioridadOptions = [
  { label: 'Baja', value: 'BAJA' },
  { label: 'Normal', value: 'NORMAL' },
  { label: 'Alta', value: 'ALTA' },
  { label: 'Urgente', value: 'URGENTE' }
]

const metodosEnvioOptions = [
  { label: 'Retiro en tienda', value: 'RETIRO_TIENDA' },
  { label: 'Despacho domicilio', value: 'DESPACHO_DOMICILIO' },
  { label: 'Transporte propio', value: 'TRANSPORTE_PROPIO' },
  { label: 'Courier', value: 'COURIER' },
  { label: 'Flete terrestre', value: 'FLETE_TERRESTRE' },
  { label: 'Otro', value: 'OTRO' }
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

const proveedorSeleccionado = computed(() => {
  if (!formulario.id_proveedor) return null
  return proveedoresOptions.value.find(p => p.value === formulario.id_proveedor)
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

// Columnas para resumen
const columnsResumen = [
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
      estado: 'CREADA',
      subtotal: formulario.subtotal,
      impuestos: formulario.impuestos,
      descuentos: formulario.descuentos,
      total: formulario.total,
      moneda: formulario.moneda,
      tipo_cambio: formulario.tipo_cambio,
      condiciones_pago: formulario.condiciones_pago,
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

const onProveedorChange = (proveedorId: number | null) => {
  if (!proveedorId) {
    formulario.contacto_proveedor = ''
    return
  }

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
    'CREADA': () => aprobar(orden),
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
    const usuarioId = authStore.user?.id_usuario || 1

    await ordenCompraStore.aprobarOrdenCompra(orden.id_orden_compra, usuarioId)

    // Registrar log de aprobación
    await logStore.logAprobacion(orden.id_orden_compra, usuarioId, 'Orden aprobada desde módulo de órdenes de compra')

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


const enviar = async (orden: OrdenCompra) => {
  try {
    const usuarioId = authStore.user?.id_usuario || 1

    await ordenCompraStore.enviarOrdenCompra(orden.id_orden_compra, usuarioId)

    // Registrar log de envío
    await logStore.logEnvio(orden.id_orden_compra, usuarioId, 'Orden enviada al proveedor')

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
    const usuarioId = authStore.user?.id_usuario || 1

    await ordenCompraStore.cerrarOrdenCompra(orden.id_orden_compra)

    // Registrar log de cierre
    await logStore.logCierre(orden.id_orden_compra, usuarioId, 'Orden cerrada - proceso completado')

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
    'CREADA': 'grey',
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
  return ['CREADA'].includes(orden.estado)
}

const puedeEliminar = (orden: OrdenCompra): boolean => {
  return ['CREADA'].includes(orden.estado)
}

const puedeEjecutarAccion = (orden: OrdenCompra): boolean => {
  return ['CREADA', 'APROBADA', 'ENVIADA'].includes(orden.estado)
}

const getAccionColor = (estado: string): string => {
  const colores: { [key: string]: string } = {
    'CREADA': 'blue',
    'APROBADA': 'purple',
    'ENVIADA': 'teal'
  }
  return colores[estado] || 'grey'
}

const getAccionIcon = (estado: string): string => {
  const iconos: { [key: string]: string } = {
    'CREADA': 'check',
    'APROBADA': 'send',
    'ENVIADA': 'done_all'
  }
  return iconos[estado] || 'more_horiz'
}

const getAccionTooltip = (estado: string): string => {
  const tooltips: { [key: string]: string } = {
    'CREADA': 'Aprobar',
    'APROBADA': 'Enviar',
    'ENVIADA': 'Cerrar'
  }
  return tooltips[estado] || 'Acción'
}

const getAccionLabel = (estado: string): string => {
  const labels: { [key: string]: string } = {
    'CREADA': 'Aprobar',
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
        proveedor.razon_social.toLowerCase().includes(needle) ||
        (proveedor.rut && proveedor.rut.toLowerCase().includes(needle)) ||
        (proveedor.email && proveedor.email.toLowerCase().includes(needle))
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