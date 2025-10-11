<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Documentos de Compra</h4>
          <p class="text-grey-7 q-mb-none">Gestión manual de documentos de compra</p>
        </div>
        <div class="q-gutter-sm">
          <q-btn
            color="secondary"
            icon="upload_file"
            label="Importar XML"
            @click="abrirDialogoImportarXML"
          />
          <q-btn
            color="primary"
            icon="add"
            label="Nuevo Documento"
            @click="abrirFormularioDocumento"
          />
        </div>
      </div>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-gutter-md items-center">
            <q-input
              v-model="filtros.busqueda"
              placeholder="Buscar por número de documento, UUID..."
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
              v-model="filtros.tipoDocumento"
              :options="tiposDocumentoOptions"
              label="Tipo de Documento"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 150px"
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
              style="min-width: 120px"
            />
            <q-btn
              color="primary"
              icon="search"
              label="Buscar"
              @click="buscarDocumentos"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Documents Table -->
      <q-table
        :rows="documentosFiltrados"
        :columns="columnsDocumentos"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_documento"
        flat
        bordered
        @request="onRequestDocumentos"
      >
        <template v-slot:body-cell-tipo_documento="props">
          <q-td :props="props">
            <q-badge
              :color="getTipoDocumentoColor(props.value)"
              :label="props.value"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-estado="props">
          <q-td :props="props">
            <q-badge
              :color="getEstadoColor(props.value)"
              :label="props.value"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-validado="props">
          <q-td :props="props">
            <q-icon
              :name="props.value ? 'verified' : 'warning'"
              :color="props.value ? 'green' : 'orange'"
              size="sm"
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

        <template v-slot:body-cell-fecha_documento="props">
          <q-td :props="props">
            {{ formatDate(props.value) }}
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
                @click="verDocumento(props.row)"
                dense
                round
              >
                <q-tooltip>Ver detalle</q-tooltip>
              </q-btn>
              <q-btn
                size="sm"
                color="green"
                icon="edit"
                @click="editarDocumento(props.row)"
                dense
                round
              >
                <q-tooltip>Editar</q-tooltip>
              </q-btn>
              <q-btn
                size="sm"
                color="red"
                icon="delete"
                @click="eliminarDocumento(props.row)"
                dense
                round
              >
                <q-tooltip>Eliminar</q-tooltip>
              </q-btn>
            </div>
          </q-td>
        </template>
      </q-table>

      <!-- Dialog para crear/editar documento -->
      <q-dialog v-model="mostrarFormularioDocumento" persistent>
        <q-card style="min-width: 1200px; max-width: 1400px; max-height: 90vh">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">{{ modoEdicion ? 'Editar' : 'Nuevo' }} Documento de Compra</div>
            <q-space />
            <q-btn icon="close" flat round dense @click="cerrarFormularioDocumento" />
          </q-card-section>

          <q-card-section class="q-pt-none" style="max-height: calc(90vh - 120px);">
            <q-form @submit="guardarDocumento">
              <div class="row" style="height: calc(90vh - 160px);">
                <div class="col-3">
                  <q-tabs
                    v-model="tabActivoDocumento"
                    vertical
                    class="text-primary full-height"
                  >
                    <q-tab name="basica" icon="info" label="Información Básica" />
                    <q-tab name="pago" icon="payment" label="Formas de Pago" />
                    <q-tab name="montos" icon="attach_money" label="Montos" />
                    <q-tab name="detalles" icon="list" label="Detalles del Documento" />
                    <q-tab name="adicional" icon="description" label="Información Adicional" />
                  </q-tabs>
                </div>
                <div class="col-9">
                  <q-tab-panels
                    v-model="tabActivoDocumento"
                    animated
                    class="full-height"
                    style="overflow-y: auto;"
                  >
                    <!-- Panel Información Básica -->
                    <q-tab-panel name="basica">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="info" class="q-mr-sm" />
                        Información Básica
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-md-8 col-sm-12 col-xs-12">
                          <q-select
                            v-model="formularioDocumento.id_proveedor"
                            :options="proveedoresOptions"
                            label="Proveedor *"
                            outlined
                            dense
                            emit-value
                            map-options
                            use-input
                            input-debounce="300"
                            @filter="filtrarProveedores"
                            :rules="[val => !!val || 'Proveedor es requerido']"
                            hint="Busca y selecciona el proveedor emisor del documento"
                            clearable
                            option-value="value"
                            option-label="label"
                          >
                            <template v-slot:no-option>
                              <q-item>
                                <q-item-section class="text-grey">
                                  Escriba para buscar proveedores
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

                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-select
                            v-model="formularioDocumento.tipo_documento"
                            :options="tiposDocumentoOptions"
                            label="Tipo de Documento *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'Tipo de documento es requerido']"
                          />
                        </div>

                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-input
                            v-model="formularioDocumento.numero_documento"
                            label="Número de Documento *"
                            outlined
                            dense
                            :rules="[val => !!val || 'Número de documento es requerido']"
                          />
                        </div>

                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-input
                            v-model="formularioDocumento.fecha_documento"
                            type="date"
                            label="Fecha de Documento *"
                            outlined
                            dense
                            :rules="[val => !!val || 'Fecha de documento es requerida']"
                          />
                        </div>
                      </div>

                      <!-- Relación con Orden de Compra -->
                      <q-separator class="q-my-md" />
                      <div class="text-h6 q-mb-md">
                        <q-icon name="assignment" class="q-mr-sm" />
                        Relación con Orden de Compra (Opcional)
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-md-8 col-sm-12 col-xs-12">
                          <q-select
                            v-model="formularioDocumento.id_orden_compra"
                            :options="ordenesCompraOptions"
                            label="Orden de Compra"
                            outlined
                            dense
                            clearable
                            emit-value
                            map-options
                            use-input
                            input-debounce="300"
                            @filter="filtrarOrdenesCompra"
                            hint="Opcional: Selecciona una orden de compra para pre-llenar datos"
                          >
                            <template v-slot:option="scope">
                              <q-item v-bind="scope.itemProps">
                                <q-item-section>
                                  <q-item-label>{{ scope.opt.label }}</q-item-label>
                                  <q-item-label caption>{{ scope.opt.proveedor }} - {{ formatCurrency(scope.opt.total) }}</q-item-label>
                                </q-item-section>
                              </q-item>
                            </template>
                          </q-select>
                        </div>
                      </div>
                    </q-tab-panel>


                    <!-- Panel Formas de Pago -->
                    <q-tab-panel name="pago">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="payment" class="q-mr-sm" />
                        Formas de Pago
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-select
                            v-model="formularioDocumento.forma_pago"
                            :options="formasPagoOptions"
                            label="Forma de Pago *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'Forma de pago es requerida']"
                          />
                        </div>

                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-input
                            v-model.number="formularioDocumento.plazo_pago"
                            type="number"
                            label="Plazo de Pago (días)"
                            outlined
                            dense
                            min="0"
                            hint="Días para el pago del documento"
                          />
                        </div>

                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-input
                            v-model="formularioDocumento.fecha_vencimiento"
                            type="date"
                            label="Fecha de Vencimiento"
                            outlined
                            dense
                            hint="Fecha límite para el pago"
                          />
                        </div>

                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-input
                            v-model="formularioDocumento.referencia_pago"
                            label="Referencia de Pago"
                            outlined
                            dense
                            hint="Número de cheque, transferencia, etc."
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Montos -->
                    <q-tab-panel name="montos">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="attach_money" class="q-mr-sm" />
                        Montos
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-md-3 col-sm-6 col-xs-12">
                          <q-input
                            v-model.number="formularioDocumento.subtotal"
                            type="number"
                            label="Subtotal *"
                            outlined
                            dense
                            step="0.01"
                            min="0"
                            prefix="$"
                            :rules="[val => val >= 0 || 'El subtotal debe ser mayor o igual a 0']"
                            @input="calcularTotal"
                          />
                        </div>

                        <div class="col-md-3 col-sm-6 col-xs-12">
                          <q-input
                            v-model.number="formularioDocumento.impuestos"
                            type="number"
                            label="Impuestos"
                            outlined
                            dense
                            step="0.01"
                            min="0"
                            prefix="$"
                            @input="calcularTotal"
                          />
                        </div>

                        <div class="col-md-3 col-sm-6 col-xs-12">
                          <q-input
                            v-model.number="formularioDocumento.descuentos"
                            type="number"
                            label="Descuentos"
                            outlined
                            dense
                            step="0.01"
                            min="0"
                            prefix="$"
                            @input="calcularTotal"
                          />
                        </div>

                        <div class="col-md-3 col-sm-6 col-xs-12">
                          <q-input
                            v-model.number="formularioDocumento.total"
                            type="number"
                            label="Total *"
                            outlined
                            dense
                            step="0.01"
                            min="0"
                            prefix="$"
                            :rules="[val => val > 0 || 'El total debe ser mayor a 0']"
                            readonly
                            class="bg-grey-1"
                          />
                        </div>

                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-select
                            v-model="formularioDocumento.moneda"
                            :options="monedasOptions"
                            label="Moneda *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'Moneda es requerida']"
                          />
                        </div>

                        <div class="col-md-6 col-sm-12 col-xs-12">
                          <q-input
                            v-model.number="formularioDocumento.tipo_cambio"
                            type="number"
                            label="Tipo de Cambio"
                            outlined
                            dense
                            step="0.0001"
                            min="0"
                            hint="1 para moneda nacional"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Detalles del Documento -->
                    <q-tab-panel name="detalles">
                      <div class="row items-center q-mb-md">
                        <div class="text-h6 q-mr-auto">
                          <q-icon name="list" class="q-mr-sm" />
                          Detalles del Documento *
                        </div>
                        <q-btn
                          color="primary"
                          icon="add"
                          label="Agregar Línea"
                          @click="agregarDetalle"
                          dense
                          outline
                          class="q-ml-md"
                        />
                      </div>

                      <div class="col-12" v-if="!formularioDocumento.detalles || formularioDocumento.detalles.length === 0">
                        <q-banner class="bg-orange-1 text-orange-8">
                          <template v-slot:avatar>
                            <q-icon name="warning" color="orange" />
                          </template>
                          El documento debe tener al menos una línea de detalle
                        </q-banner>
                      </div>

                      <div class="col-12" v-for="(detalle, index) in (formularioDocumento.detalles || [])" :key="index">
                        <q-card flat bordered>
                          <q-card-section>
                            <div class="row q-gutter-sm items-start" style="align-items: flex-start;">
                              <div class="col-4">
                                <q-input
                                  v-model="detalle.descripcion"
                                  label="Descripción *"
                                  outlined
                                  dense
                                  hide-bottom-space
                                  :rules="[val => !!val || 'Descripción es requerida']"
                                />
                        </div>

                              <div class="col-1">
                                <q-input
                                  v-model.number="detalle.cantidad"
                                  type="number"
                                  label="Cantidad *"
                                  outlined
                                  dense
                                  hide-bottom-space
                                  step="0.01"
                                  min="0"
                                  :rules="[val => val > 0 || 'Cantidad debe ser mayor a 0']"
                                  @input="calcularLineaTotal(index)"
                                />
                        </div>

                              <div class="col-2">
                                <q-input
                                  v-model.number="detalle.precio_unitario"
                                  type="number"
                                  label="Precio Unit. *"
                                  outlined
                                  dense
                                  hide-bottom-space
                                  step="0.01"
                                  min="0"
                                  prefix="$"
                                  :rules="[val => val >= 0 || 'Precio debe ser mayor o igual a 0']"
                                  @input="calcularLineaTotal(index)"
                                />
                              </div>

                              <div class="col-2">
                                <q-input
                                  v-model.number="detalle.descuento_linea"
                                  type="number"
                                  label="Descuento"
                                  outlined
                                  dense
                                  hide-bottom-space
                                  step="0.01"
                                  min="0"
                                  prefix="$"
                                  @input="calcularLineaTotal(index)"
                                />
                              </div>

                              <div class="col-2">
                                <q-input
                                  v-model.number="detalle.total_linea"
                                  type="number"
                                  label="Total Línea"
                                  outlined
                                  dense
                                  hide-bottom-space
                                  prefix="$"
                                  readonly
                                  class="bg-grey-1"
                                />
                              </div>

                              <div class="col-auto" style="display: flex; align-items: center; height: 40px;">
                                <q-btn
                                  color="red"
                                  icon="delete"
                                  @click="eliminarDetalle(index)"
                                  dense
                                  round
                                  size="md"
                                >
                                  <q-tooltip>Eliminar línea</q-tooltip>
                                </q-btn>
                              </div>
                            </div>
                          </q-card-section>
                        </q-card>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Información Adicional -->
                    <q-tab-panel name="adicional">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="description" class="q-mr-sm" />
                        Información Adicional
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12">
                          <q-input
                            v-model="formularioDocumento.observaciones"
                            label="Observaciones"
                            type="textarea"
                            outlined
                            rows="3"
                            hint="Información adicional del documento"
                          />
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
                  @click="cerrarFormularioDocumento"
                />
                <q-btn
                  :label="modoEdicion ? 'Actualizar' : 'Crear Documento'"
                  color="primary"
                  type="submit"
                  :loading="guardandoDocumento"
                  :disable="!formularioDocumentoValido"
                />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- Dialog para ver detalle del documento -->
      <q-dialog
        v-model="mostrarDetalle"
        persistent
        maximized
        transition-show="slide-up"
        transition-hide="slide-down"
      >
        <q-card class="dialog-card" v-if="documentoSeleccionado">
          <q-toolbar class="bg-primary text-white">
            <q-toolbar-title>
              Documento {{ documentoSeleccionado.numero_documento }}
            </q-toolbar-title>
            <q-btn flat round dense icon="close" @click="cerrarDetalle" />
          </q-toolbar>

          <q-card-section class="q-pa-md scroll">
            <!-- Información del documento -->
            <div class="row q-gutter-md q-mb-lg">
              <div class="col-12">
                <h6 class="q-ma-none q-mb-md">Información del Documento</h6>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Tipo de Documento" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      <q-badge
                        :color="getTipoDocumentoColor(documentoSeleccionado.tipo_documento)"
                        :label="documentoSeleccionado.tipo_documento"
                      />
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Número" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ documentoSeleccionado.numero_documento }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Estado" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      <q-badge
                        :color="getEstadoColor(documentoSeleccionado.estado)"
                        :label="documentoSeleccionado.estado"
                      />
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Validado" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      <q-icon
                        :name="documentoSeleccionado.validado ? 'verified' : 'warning'"
                        :color="documentoSeleccionado.validado ? 'green' : 'orange'"
                        size="sm"
                      />
                      {{ documentoSeleccionado.validado ? 'Sí' : 'No' }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Fecha Documento" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ formatDate(documentoSeleccionado.fecha_documento) }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Total" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline text-weight-bold text-primary" tabindex="-1">
                      {{ formatCurrency(documentoSeleccionado.total) }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Moneda" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ documentoSeleccionado.moneda }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
              </div>
            </div>

            <!-- Información fiscal -->
            <div class="row q-gutter-md q-mb-lg" v-if="documentoSeleccionado.uuid_fiscal || documentoSeleccionado.rut_emisor">
              <div class="col-12">
                <h6 class="q-ma-none q-mb-md">Información Fiscal</h6>
              </div>

              <div class="col-md-6 col-sm-12 col-xs-12" v-if="documentoSeleccionado.serie">
                <q-field label="Serie" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ documentoSeleccionado.serie }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-6 col-sm-12 col-xs-12" v-if="documentoSeleccionado.folio">
                <q-field label="Folio" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ documentoSeleccionado.folio }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-4 col-sm-6 col-xs-12" v-if="documentoSeleccionado.uuid_fiscal">
                <q-field label="UUID Fiscal" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ documentoSeleccionado.uuid_fiscal }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-4 col-sm-6 col-xs-12" v-if="documentoSeleccionado.rut_emisor">
                <q-field label="RUT Emisor" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ documentoSeleccionado.rut_emisor }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-4 col-sm-6 col-xs-12" v-if="documentoSeleccionado.rut_receptor">
                <q-field label="RUT Receptor" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ documentoSeleccionado.rut_receptor }}
                    </div>
                  </template>
                </q-field>
              </div>

              <!-- Montos -->
              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Subtotal" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ formatCurrency(documentoSeleccionado.subtotal) }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Impuestos" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ formatCurrency(documentoSeleccionado.impuestos) }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Descuentos" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ formatCurrency(documentoSeleccionado.descuentos) }}
                    </div>
                  </template>
                </q-field>
              </div>

              <div class="col-md-3 col-sm-6 col-xs-12">
                <q-field label="Tipo de Cambio" stack-label outlined readonly dense>
                  <template v-slot:control>
                    <div class="self-center full-width no-outline" tabindex="-1">
                      {{ documentoSeleccionado.tipo_cambio }}
                    </div>
                  </template>
                </q-field>
              </div>
            </div>

            <!-- Errores de procesamiento -->
            <div class="row q-gutter-md q-mb-lg" v-if="documentoSeleccionado.errores_procesamiento">
              <div class="col-12">
                <h6 class="q-ma-none q-mb-md">Errores de Procesamiento</h6>
                <q-banner class="bg-red-1 text-red-8">
                  <template v-slot:avatar>
                    <q-icon name="error" color="red" />
                  </template>
                  {{ documentoSeleccionado.errores_procesamiento }}
                </q-banner>
              </div>
            </div>

            <!-- Observaciones -->
            <div class="row q-gutter-md" v-if="documentoSeleccionado.observaciones">
              <div class="col-12">
                <h6 class="q-ma-none q-mb-md">Observaciones</h6>
                <q-card flat bordered>
                  <q-card-section>
                    {{ documentoSeleccionado.observaciones }}
                  </q-card-section>
                </q-card>
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
                label="Editar"
                color="primary"
                @click="editarDocumentoDesdeDetalle"
              />
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>

      <!-- Dialog para importar XML -->
      <q-dialog v-model="mostrarDialogoImportarXML" persistent>
        <q-card style="min-width: 600px; max-width: 800px">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Importar Documento desde XML</div>
            <q-space />
            <q-btn icon="close" flat round dense @click="cerrarDialogoImportarXML" />
          </q-card-section>

          <q-card-section>
            <div class="text-body1 q-mb-md">
              Seleccione un archivo XML válido para importar automáticamente un documento de compra.
              El sistema extraerá la información fiscal y los datos del documento.
            </div>

            <q-stepper
              v-model="pasoImportacion"
              color="primary"
              animated
            >
              <q-step
                :name="1"
                title="Seleccionar Archivo"
                icon="upload_file"
                :done="pasoImportacion > 1"
              >
                <div class="q-gutter-md">
                  <q-file
                    v-model="archivoXML"
                    label="Archivo XML"
                    outlined
                    accept=".xml"
                    max-file-size="5242880"
                    @rejected="onArchivoRechazado"
                    @update:model-value="onArchivoSeleccionado"
                  >
                    <template v-slot:prepend>
                      <q-icon name="attach_file" />
                    </template>
                    <template v-slot:hint>
                      Archivo XML válido (máximo 5MB)
                    </template>
                  </q-file>

                  <div v-if="archivoXML" class="q-mt-md">
                    <q-card flat bordered class="bg-grey-1">
                      <q-card-section>
                        <div class="text-subtitle2">Archivo seleccionado:</div>
                        <div class="text-body2">{{ archivoXML.name }}</div>
                        <div class="text-caption">Tamaño: {{ formatFileSize(archivoXML.size) }}</div>
                      </q-card-section>
                    </q-card>
                  </div>
                </div>
              </q-step>

              <q-step
                :name="2"
                title="Procesamiento"
                icon="settings"
                :done="pasoImportacion > 2"
              >
                <div v-if="procesandoXML" class="text-center q-pa-lg">
                  <q-spinner color="primary" size="3em" />
                  <div class="q-mt-md">Procesando archivo XML...</div>
                </div>

                <div v-else-if="errorProcesamiento" class="q-pa-md">
                  <q-banner class="bg-negative text-white">
                    <template v-slot:avatar>
                      <q-icon name="error" />
                    </template>
                    {{ errorProcesamiento }}
                  </q-banner>
                </div>

                <div v-else-if="datosExtraidos" class="q-gutter-md">
                  <div class="text-subtitle1 q-mb-md">Datos extraídos del XML:</div>

                  <q-card flat bordered>
                    <q-card-section>
                      <div class="row q-gutter-md">
                        <div class="col-6">
                          <q-field label="Tipo Documento" stack-label outlined readonly dense>
                            <template v-slot:control>
                              <div class="self-center full-width no-outline" tabindex="-1">
                                {{ datosExtraidos.tipo_documento }}
                              </div>
                            </template>
                          </q-field>
                        </div>
                        <div class="col-5">
                          <q-field label="Número" stack-label outlined readonly dense>
                            <template v-slot:control>
                              <div class="self-center full-width no-outline" tabindex="-1">
                                {{ datosExtraidos.numero_documento }}
                              </div>
                            </template>
                          </q-field>
                        </div>
                        <div class="col-6">
                          <q-field label="RUT Emisor" stack-label outlined readonly dense>
                            <template v-slot:control>
                              <div class="self-center full-width no-outline" tabindex="-1">
                                {{ datosExtraidos.rut_emisor }}
                              </div>
                            </template>
                          </q-field>
                        </div>
                        <div class="col-5">
                          <q-field label="Fecha" stack-label outlined readonly dense>
                            <template v-slot:control>
                              <div class="self-center full-width no-outline" tabindex="-1">
                                {{ formatDate(datosExtraidos.fecha_documento) }}
                              </div>
                            </template>
                          </q-field>
                        </div>
                        <div class="col-6">
                          <q-field label="Total" stack-label outlined readonly dense>
                            <template v-slot:control>
                              <div class="self-center full-width no-outline text-weight-bold text-primary" tabindex="-1">
                                {{ formatCurrency(datosExtraidos.total) }}
                              </div>
                            </template>
                          </q-field>
                        </div>
                        <div class="col-5">
                          <q-field label="UUID Fiscal" stack-label outlined readonly dense>
                            <template v-slot:control>
                              <div class="self-center full-width no-outline text-caption" tabindex="-1">
                                {{ datosExtraidos.uuid_fiscal }}
                              </div>
                            </template>
                          </q-field>
                        </div>
                      </div>
                    </q-card-section>
                  </q-card>

                  <q-card flat bordered>
                    <q-card-section>
                      <div class="text-subtitle2 q-mb-sm">Configuración de Importación:</div>
                      <div class="q-gutter-md">
                        <q-select
                          v-model="configuracionImportacion.id_proveedor"
                          :options="proveedoresEncontrados"
                          label="Seleccionar Proveedor"
                          outlined
                          dense
                          emit-value
                          map-options
                          hint="Proveedor encontrado por RUT o crear nuevo"
                        />
                        <q-toggle
                          v-model="configuracionImportacion.validar_automaticamente"
                          label="Validar automáticamente después de importar"
                        />
                        <q-toggle
                          v-model="configuracionImportacion.importar_detalles"
                          label="Importar líneas de detalle del documento"
                        />
                      </div>
                    </q-card-section>
                  </q-card>
                </div>
              </q-step>

              <q-step
                :name="3"
                title="Confirmación"
                icon="check"
              >
                <div v-if="importandoDocumento" class="text-center q-pa-lg">
                  <q-spinner color="primary" size="3em" />
                  <div class="q-mt-md">Importando documento al sistema...</div>
                </div>

                <div v-else class="q-pa-md">
                  <q-banner class="bg-positive text-white q-mb-md">
                    <template v-slot:avatar>
                      <q-icon name="check_circle" />
                    </template>
                    Documento importado exitosamente
                  </q-banner>

                  <div class="text-body1">
                    El documento ha sido importado y está disponible en la lista de documentos.
                  </div>
                </div>
              </q-step>
            </q-stepper>
          </q-card-section>

          <q-card-actions align="right" class="q-pa-md">
            <q-btn
              flat
              label="Cancelar"
              @click="cerrarDialogoImportarXML"
              :disable="procesandoXML || importandoDocumento"
            />
            <q-btn
              v-if="pasoImportacion === 1"
              color="primary"
              label="Procesar XML"
              @click="procesarArchivoXML"
              :disable="!archivoXML"
              :loading="procesandoXML"
            />
            <q-btn
              v-if="pasoImportacion === 2 && datosExtraidos && !errorProcesamiento"
              color="positive"
              label="Importar Documento"
              @click="importarDocumento"
              :loading="importandoDocumento"
            />
            <q-btn
              v-if="pasoImportacion === 3"
              color="primary"
              label="Finalizar"
              @click="cerrarDialogoImportarXML"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useQuasar } from 'quasar'
import { useDocumentoStore, type DocumentoCompra, type DocumentoCompraDetalle } from '@/stores/documentos'

const $q = useQuasar()
const documentoStore = useDocumentoStore()

// Estado reactivo
const mostrarFormularioDocumento = ref(false)
const mostrarDetalle = ref(false)
const documentoSeleccionado = ref<DocumentoCompra | null>(null)
const modoEdicion = ref(false)
const guardandoDocumento = ref(false)
const tabActivoDocumento = ref('basica')

// Estado para importación XML
const mostrarDialogoImportarXML = ref(false)
const archivoXML = ref<File | null>(null)
const pasoImportacion = ref(1)
const procesandoXML = ref(false)
const importandoDocumento = ref(false)
const errorProcesamiento = ref('')
const datosExtraidos = ref<any>(null)
const proveedoresEncontrados = ref([])
const configuracionImportacion = ref({
  id_proveedor: null,
  validar_automaticamente: true,
  importar_detalles: true
})

// Filtros
const filtros = reactive({
  busqueda: '',
  ordenCompra: null,
  tipoDocumento: null,
  estado: null
})

// Paginación
const paginacion = ref({
  sortBy: 'fecha_documento',
  descending: true,
  page: 1,
  rowsPerPage: 10,
  rowsNumber: 0
})

// Formulario de documento
const formularioDocumentoInicial: Partial<DocumentoCompra> = {
  id_proveedor: null,
  id_orden_compra: null,
  tipo_documento: null,
  numero_documento: '',
  fecha_documento: '',
  forma_pago: null,
  plazo_pago: 0,
  fecha_vencimiento: '',
  referencia_pago: '',
  subtotal: 0,
  impuestos: 0,
  descuentos: 0,
  total: 0,
  moneda: 'CLP',
  tipo_cambio: 1,
  observaciones: '',
  activo: true,
  detalles: [] as DocumentoCompraDetalle[]
}

const formularioDocumento = reactive({ ...formularioDocumentoInicial })


// Computed
const isLoading = computed(() => documentoStore.isLoading)

const documentosFiltrados = computed(() => {
  let docs = documentoStore.documentos

  if (filtros.busqueda) {
    docs = docs.filter(doc =>
      doc.numero_documento?.toLowerCase().includes(filtros.busqueda.toLowerCase()) ||
      doc.uuid_fiscal?.toLowerCase().includes(filtros.busqueda.toLowerCase())
    )
  }

  if (filtros.ordenCompra) {
    docs = docs.filter(doc => doc.id_orden_compra === filtros.ordenCompra)
  }

  if (filtros.tipoDocumento) {
    docs = docs.filter(doc => doc.tipo_documento === filtros.tipoDocumento)
  }

  if (filtros.estado) {
    docs = docs.filter(doc => doc.estado === filtros.estado)
  }

  return docs
})

const ordenesCompraOptions = ref([])
const proveedoresOptions = ref([])

const filtrarProveedores = async (val: string, update: Function) => {
  if (val.length < 2) {
    update(() => {
      proveedoresOptions.value = []
    })
    return
  }

  try {
    const proveedores = await documentoStore.buscarProveedores(val)
    update(() => {
      proveedoresOptions.value = proveedores.map(proveedor => {
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
    })
  } catch (error) {
    console.error('Error buscando proveedores:', error)
    update(() => {
      proveedoresOptions.value = []
    })
  }
}

const filtrarOrdenesCompra = async (val: string, update: Function) => {
  if (val.length < 2) {
    update(() => {
      ordenesCompraOptions.value = []
    })
    return
  }

  try {
    const ordenes = await documentoStore.buscarOrdenesCompra(val)
    update(() => {
      ordenesCompraOptions.value = ordenes.map(orden => ({
        label: `${orden.numero_orden} - ${orden.proveedor?.razon_social || 'Sin proveedor'}`,
        value: orden.id_orden_compra,
        proveedor: orden.proveedor?.razon_social || 'Sin proveedor',
        total: orden.total
      }))
    })
  } catch (error) {
    console.error('Error buscando órdenes de compra:', error)
    update(() => {
      ordenesCompraOptions.value = []
    })
  }
}

const tiposDocumentoOptions = [
  { label: 'Factura', value: 'FACTURA' },
  { label: 'Factura Exenta', value: 'FACTURA_EXENTA' },
  { label: 'Boleta', value: 'BOLETA' },
  { label: 'Nota de Crédito', value: 'NOTA_CREDITO' },
  { label: 'Nota de Débito', value: 'NOTA_DEBITO' },
  { label: 'Guía de Despacho', value: 'GUIA_DESPACHO' },
  { label: 'Otro', value: 'OTRO' }
]

const estadosOptions = [
  { label: 'Pendiente', value: 'PENDIENTE' },
  { label: 'Validado', value: 'VALIDADO' },
  { label: 'Disponible Bodega', value: 'DISPONIBLE_BODEGA' },
  { label: 'Ingresado Bodega', value: 'INGRESADO_BODEGA' },
  { label: 'Anulado', value: 'ANULADO' }
]

const formularioDocumentoValido = computed(() => {
  return formularioDocumento.id_proveedor &&
         formularioDocumento.tipo_documento &&
         formularioDocumento.numero_documento &&
         formularioDocumento.fecha_documento &&
         formularioDocumento.forma_pago &&
         formularioDocumento.subtotal >= 0 &&
         formularioDocumento.total > 0 &&
         formularioDocumento.moneda &&
         formularioDocumento.detalles &&
         formularioDocumento.detalles.length > 0 &&
         formularioDocumento.detalles.every(detalle =>
           detalle.descripcion &&
           detalle.cantidad > 0 &&
           detalle.precio_unitario >= 0
         )
})

const monedasOptions = [
  { label: 'Peso Chileno (CLP)', value: 'CLP' },
  { label: 'Dólar Americano (USD)', value: 'USD' },
  { label: 'Euro (EUR)', value: 'EUR' },
  { label: 'Unidad de Fomento (UF)', value: 'UF' }
]

const formasPagoOptions = [
  { label: 'Contado', value: 'CONTADO' },
  { label: 'Crédito', value: 'CREDITO' },
  { label: 'Cheque', value: 'CHEQUE' },
  { label: 'Transferencia', value: 'TRANSFERENCIA' },
  { label: 'Tarjeta de Crédito', value: 'TARJETA_CREDITO' },
  { label: 'Tarjeta de Débito', value: 'TARJETA_DEBITO' },
  { label: 'Otro', value: 'OTRO' }
]

// Columnas de la tabla
const columnsDocumentos = [
  {
    name: 'tipo_documento',
    label: 'Tipo',
    align: 'left',
    field: 'tipo_documento',
    sortable: true
  },
  {
    name: 'numero_documento',
    label: 'Número',
    align: 'left',
    field: 'numero_documento',
    sortable: true
  },
  {
    name: 'proveedor',
    label: 'Proveedor',
    align: 'left',
    field: 'proveedor',
    sortable: true
  },
  {
    name: 'fecha_documento',
    label: 'Fecha',
    align: 'center',
    field: 'fecha_documento',
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
    name: 'validado',
    label: 'Validado',
    align: 'center',
    field: 'validado',
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

// Métodos
const cargarDatos = async () => {
  try {
    await documentoStore.obtenerDocumentos()
  } catch (error) {
    console.error('Error cargando datos:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al cargar los datos'
    })
  }
}

const buscarDocumentos = async () => {
  try {
    const params: any = {}

    if (filtros.tipoDocumento) params.tipo_documento = filtros.tipoDocumento
    if (filtros.estado) params.estado = filtros.estado

    if (filtros.busqueda) {
      await documentoStore.buscarDocumentos(filtros.busqueda, params)
    } else {
      await documentoStore.obtenerDocumentos(params)
    }
  } catch (error) {
    console.error('Error buscando documentos:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al buscar documentos'
    })
  }
}

const onRequestDocumentos = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await buscarDocumentos()
}

const abrirFormularioDocumento = () => {
  modoEdicion.value = false
  Object.assign(formularioDocumento, {
    ...formularioDocumentoInicial,
    detalles: []
  })
  mostrarFormularioDocumento.value = true
}

const cerrarFormularioDocumento = () => {
  mostrarFormularioDocumento.value = false
  modoEdicion.value = false
  Object.assign(formularioDocumento, {
    ...formularioDocumentoInicial,
    detalles: []
  })
}

const calcularTotal = () => {
  const subtotal = formularioDocumento.subtotal || 0
  const impuestos = formularioDocumento.impuestos || 0
  const descuentos = formularioDocumento.descuentos || 0
  formularioDocumento.total = subtotal + impuestos - descuentos
}

// Funciones para manejar detalles
const agregarDetalle = () => {
  const nuevoDetalle: DocumentoCompraDetalle = {
    descripcion: '',
    cantidad: 1,
    precio_unitario: 0,
    descuento_linea: 0,
    subtotal_linea: 0,
    impuesto_linea: 0,
    total_linea: 0,
    numero_linea: formularioDocumento.detalles?.length + 1 || 1
  }
  if (!formularioDocumento.detalles) {
    formularioDocumento.detalles = []
  }
  formularioDocumento.detalles.push(nuevoDetalle)
}

const eliminarDetalle = (index: number) => {
  if (formularioDocumento.detalles) {
    formularioDocumento.detalles.splice(index, 1)
    // Recalcular números de línea
    formularioDocumento.detalles.forEach((detalle, idx) => {
      detalle.numero_linea = idx + 1
    })
    calcularTotalesDocumento()
  }
}

const calcularLineaTotal = (index: number) => {
  if (formularioDocumento.detalles && formularioDocumento.detalles[index]) {
    const detalle = formularioDocumento.detalles[index]
    const cantidad = detalle.cantidad || 0
    const precioUnitario = detalle.precio_unitario || 0
    const descuento = detalle.descuento_linea || 0

    detalle.subtotal_linea = cantidad * precioUnitario
    detalle.total_linea = detalle.subtotal_linea - descuento

    calcularTotalesDocumento()
  }
}

const calcularTotalesDocumento = () => {
  if (formularioDocumento.detalles) {
    const subtotal = formularioDocumento.detalles.reduce((sum, detalle) => sum + (detalle.subtotal_linea || 0), 0)
    const descuentos = formularioDocumento.detalles.reduce((sum, detalle) => sum + (detalle.descuento_linea || 0), 0)

    formularioDocumento.subtotal = subtotal
    formularioDocumento.descuentos = descuentos
    calcularTotal()
  }
}

const guardarDocumento = async () => {
  try {
    guardandoDocumento.value = true

    if (modoEdicion.value && documentoSeleccionado.value) {
      await documentoStore.actualizarDocumento(
        documentoSeleccionado.value.id_documento,
        formularioDocumento
      )
      $q.notify({
        type: 'positive',
        message: 'Documento actualizado exitosamente'
      })
    } else {
      await documentoStore.crearDocumento(formularioDocumento)
      $q.notify({
        type: 'positive',
        message: 'Documento creado exitosamente'
      })
    }

    cerrarFormularioDocumento()
    await cargarDatos()
  } catch (error) {
    console.error('Error guardando documento:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al guardar el documento'
    })
  } finally {
    guardandoDocumento.value = false
  }
}

const verDocumento = async (documento: DocumentoCompra) => {
  try {
    const documentoCompleto = await documentoStore.obtenerDocumento(documento.id_documento)
    documentoSeleccionado.value = documentoCompleto
    mostrarDetalle.value = true
  } catch (error) {
    console.error('Error cargando detalle del documento:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al cargar el detalle del documento'
    })
  }
}

const cerrarDetalle = () => {
  mostrarDetalle.value = false
  documentoSeleccionado.value = null
}

const editarDocumento = (documento: DocumentoCompra) => {
  modoEdicion.value = true
  documentoSeleccionado.value = documento

  Object.assign(formularioDocumento, {
    id_proveedor: documento.id_proveedor,
    id_orden_compra: documento.id_orden_compra || null,
    tipo_documento: documento.tipo_documento,
    numero_documento: documento.numero_documento,
    fecha_documento: documento.fecha_documento,
    forma_pago: documento.forma_pago || null,
    plazo_pago: documento.plazo_pago || 0,
    fecha_vencimiento: documento.fecha_vencimiento || '',
    referencia_pago: documento.referencia_pago || '',
    subtotal: documento.subtotal || 0,
    impuestos: documento.impuestos || 0,
    descuentos: documento.descuentos || 0,
    total: documento.total || 0,
    moneda: documento.moneda || 'CLP',
    tipo_cambio: documento.tipo_cambio || 1,
    observaciones: documento.observaciones || '',
    activo: documento.activo,
    detalles: documento.detalles || []
  })

  mostrarFormularioDocumento.value = true
}

const editarDocumentoDesdeDetalle = () => {
  cerrarDetalle()
  if (documentoSeleccionado.value) {
    editarDocumento(documentoSeleccionado.value)
  }
}


const eliminarDocumento = async (documento: DocumentoCompra) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de que desea eliminar el documento ${documento.numero_documento}?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await documentoStore.eliminarDocumento(documento.id_documento)
      $q.notify({
        type: 'positive',
        message: 'Documento eliminado exitosamente'
      })
      await cargarDatos()
    } catch (error) {
      console.error('Error eliminando documento:', error)
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar el documento'
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

const formatFileSize = (bytes: number): string => {
  if (!bytes) return ''
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
}

const getTipoDocumentoColor = (tipo: string): string => {
  const colores: { [key: string]: string } = {
    'FACTURA': 'blue',
    'FACTURA_EXENTA': 'cyan',
    'NOTA_CREDITO': 'green',
    'NOTA_DEBITO': 'orange',
    'GUIA_DESPACHO': 'purple',
    'BOLETA': 'teal',
    'OTRO': 'grey'
  }
  return colores[tipo] || 'grey'
}

const getEstadoColor = (estado: string): string => {
  const colores: { [key: string]: string } = {
    'PENDIENTE': 'orange',
    'VALIDADO': 'green',
    'DISPONIBLE_BODEGA': 'blue',
    'INGRESADO_BODEGA': 'purple',
    'ANULADO': 'red'
  }
  return colores[estado] || 'grey'
}

// Funciones para importación XML
const abrirDialogoImportarXML = () => {
  resetImportacionXML()
  mostrarDialogoImportarXML.value = true
}

const cerrarDialogoImportarXML = () => {
  mostrarDialogoImportarXML.value = false
  resetImportacionXML()
}

const resetImportacionXML = () => {
  archivoXML.value = null
  pasoImportacion.value = 1
  procesandoXML.value = false
  importandoDocumento.value = false
  errorProcesamiento.value = ''
  datosExtraidos.value = null
  proveedoresEncontrados.value = []
  configuracionImportacion.value = {
    id_proveedor: null,
    validar_automaticamente: true,
    importar_detalles: true
  }
}

const onArchivoSeleccionado = (archivo: File | null) => {
  if (archivo) {
    // Resetear estado de procesamiento
    errorProcesamiento.value = ''
    datosExtraidos.value = null
  }
}

const onArchivoRechazado = (rejectedEntries: any[]) => {
  $q.notify({
    type: 'negative',
    message: `Archivo no válido: ${rejectedEntries[0].failedPropValidation}`,
    caption: 'Seleccione un archivo XML válido menor a 5MB'
  })
}

const procesarArchivoXML = async () => {
  if (!archivoXML.value) return

  try {
    procesandoXML.value = true
    errorProcesamiento.value = ''

    // Crear FormData para enviar el archivo
    const formData = new FormData()
    formData.append('archivo_xml', archivoXML.value)

    // Llamar al store para procesar el XML
    const resultado = await documentoStore.procesarArchivoXML(formData)

    if (resultado.success) {
      datosExtraidos.value = resultado.datos

      // Buscar proveedores por RUT
      if (resultado.datos.rut_emisor) {
        await buscarProveedoresPorRUT(resultado.datos.rut_emisor)
      }

      pasoImportacion.value = 2

      $q.notify({
        type: 'positive',
        message: 'Archivo XML procesado exitosamente',
        caption: 'Se extrajeron los datos del documento'
      })
    } else {
      errorProcesamiento.value = resultado.error || 'Error procesando el archivo XML'
    }
  } catch (error: any) {
    console.error('Error procesando XML:', error)
    errorProcesamiento.value = error.message || 'Error inesperado procesando el archivo'
  } finally {
    procesandoXML.value = false
  }
}

const buscarProveedoresPorRUT = async (rut: string) => {
  try {
    const proveedores = await documentoStore.buscarProveedoresPorRUT(rut)

    proveedoresEncontrados.value = proveedores.map(proveedor => {
      const proveedorRfc = proveedor.rfc || proveedor.rut_proveedor || proveedor.rut || 'Sin RUT'
      return {
        label: `${proveedor.razon_social} - ${proveedorRfc}`,
        value: proveedor.id_proveedor,
        rut: proveedorRfc,
        rfc: proveedorRfc,
        razon_social: proveedor.razon_social,
        email: proveedor.email,
        telefono: proveedor.telefono,
        proveedor: proveedor
      }
    })

    // Si encontramos un proveedor exacto, seleccionarlo automáticamente
    if (proveedores.length === 1) {
      configuracionImportacion.value.id_proveedor = proveedores[0].id_proveedor
    }

    // Si no hay proveedores, agregar opción para crear nuevo
    if (proveedores.length === 0) {
      proveedoresEncontrados.value.push({
        label: `Crear nuevo proveedor - ${rut}`,
        value: 'nuevo',
        rut: rut,
        rfc: rut,
        razon_social: datosExtraidos.value.nombre_emisor || 'Nuevo Proveedor'
      })
    }
  } catch (error) {
    console.error('Error buscando proveedores:', error)
  }
}

const importarDocumento = async () => {
  if (!datosExtraidos.value) return

  try {
    importandoDocumento.value = true

    // Preparar datos para importación
    const datosImportacion = {
      ...datosExtraidos.value,
      id_proveedor: configuracionImportacion.value.id_proveedor,
      validar_automaticamente: configuracionImportacion.value.validar_automaticamente,
      importar_detalles: configuracionImportacion.value.importar_detalles,
      archivo_xml_original: archivoXML.value?.name
    }

    // Llamar al store para importar el documento
    const resultado = await documentoStore.importarDocumentoDesdeXML(datosImportacion)

    if (resultado.success) {
      pasoImportacion.value = 3

      $q.notify({
        type: 'positive',
        message: 'Documento importado exitosamente',
        caption: `Documento ${resultado.documento.numero_documento} creado`
      })

      // Recargar la lista de documentos
      await cargarDatos()
    } else {
      throw new Error(resultado.error || 'Error importando el documento')
    }
  } catch (error: any) {
    console.error('Error importando documento:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al importar el documento',
      caption: error.message
    })
  } finally {
    importandoDocumento.value = false
  }
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

.stat-card {
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}
</style>