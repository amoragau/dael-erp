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
      <q-dialog
        v-model="mostrarFormularioDocumento"
        persistent
        maximized
        transition-show="slide-up"
        transition-hide="slide-down"
      >
        <q-card class="dialog-card">
          <q-toolbar class="bg-primary text-white">
            <q-toolbar-title>
              {{ modoEdicion ? 'Editar Documento' : 'Nuevo Documento de Compra' }}
            </q-toolbar-title>
            <q-btn flat round dense icon="close" @click="cerrarFormularioDocumento" />
          </q-toolbar>

          <q-card-section class="q-pa-md">
            <q-form @submit="guardarDocumento" class="q-gutter-md">
              <!-- Información básica -->
              <div class="row q-gutter-md">
                <div class="col-12">
                  <h6 class="q-ma-none q-mb-md">Información Básica</h6>
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

                <div class="col-md-6 col-sm-12 col-xs-12">
                  <q-input
                    v-model="formularioDocumento.serie"
                    label="Serie"
                    outlined
                    dense
                    hint="Opcional"
                  />
                </div>

                <div class="col-md-6 col-sm-12 col-xs-12">
                  <q-input
                    v-model="formularioDocumento.folio"
                    label="Folio"
                    outlined
                    dense
                    hint="Opcional"
                  />
                </div>
              </div>

              <!-- Relación con Orden de Compra -->
              <div class="row q-gutter-md">
                <div class="col-12">
                  <q-separator class="q-my-md" />
                  <h6 class="q-ma-none q-mb-md">Relación con Orden de Compra (Opcional)</h6>
                </div>

                <div class="col-12">
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

              <!-- Información fiscal -->
              <div class="row q-gutter-md">
                <div class="col-12">
                  <q-separator class="q-my-md" />
                  <h6 class="q-ma-none q-mb-md">Información Fiscal</h6>
                </div>

                <div class="col-md-6 col-sm-12 col-xs-12">
                  <q-input
                    v-model="formularioDocumento.uuid_fiscal"
                    label="UUID Fiscal"
                    outlined
                    dense
                    hint="Timbre electrónico único"
                  />
                </div>

                <div class="col-md-6 col-sm-12 col-xs-12">
                  <q-input
                    v-model="formularioDocumento.rut_emisor"
                    label="RUT Emisor"
                    outlined
                    dense
                    mask="##.###.###-#"
                    hint="RUT del emisor"
                  />
                </div>

                <div class="col-md-6 col-sm-12 col-xs-12">
                  <q-input
                    v-model="formularioDocumento.rut_receptor"
                    label="RUT Receptor"
                    outlined
                    dense
                    mask="##.###.###-#"
                    hint="RUT del receptor"
                  />
                </div>

                <div class="col-md-6 col-sm-12 col-xs-12">
                  <q-input
                    v-model="formularioDocumento.contenido_xml"
                    label="Contenido XML"
                    type="textarea"
                    outlined
                    rows="3"
                    hint="Opcional: XML del documento electrónico"
                  />
                </div>
              </div>

              <!-- Montos -->
              <div class="row q-gutter-md">
                <div class="col-12">
                  <q-separator class="q-my-md" />
                  <h6 class="q-ma-none q-mb-md">Montos</h6>
                </div>

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

              <!-- Detalles del Documento -->
              <div class="row q-gutter-md">
                <div class="col-12">
                  <q-separator class="q-my-md" />
                  <div class="row items-center justify-between">
                    <h6 class="q-ma-none">Detalles del Documento *</h6>
                    <q-btn
                      color="primary"
                      icon="add"
                      label="Agregar Línea"
                      @click="agregarDetalle"
                      dense
                      outline
                    />
                  </div>
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
                      <div class="row q-gutter-md items-center">
                        <div class="col-md-4 col-sm-12 col-xs-12">
                          <q-input
                            v-model="detalle.descripcion"
                            label="Descripción *"
                            outlined
                            dense
                            :rules="[val => !!val || 'Descripción es requerida']"
                          />
                        </div>

                        <div class="col-md-2 col-sm-6 col-xs-12">
                          <q-input
                            v-model.number="detalle.cantidad"
                            type="number"
                            label="Cantidad *"
                            outlined
                            dense
                            step="0.01"
                            min="0"
                            :rules="[val => val > 0 || 'Cantidad debe ser mayor a 0']"
                            @input="calcularLineaTotal(index)"
                          />
                        </div>

                        <div class="col-md-2 col-sm-6 col-xs-12">
                          <q-input
                            v-model.number="detalle.precio_unitario"
                            type="number"
                            label="Precio Unit. *"
                            outlined
                            dense
                            step="0.01"
                            min="0"
                            prefix="$"
                            :rules="[val => val >= 0 || 'Precio debe ser mayor o igual a 0']"
                            @input="calcularLineaTotal(index)"
                          />
                        </div>

                        <div class="col-md-2 col-sm-6 col-xs-12">
                          <q-input
                            v-model.number="detalle.descuento_linea"
                            type="number"
                            label="Descuento"
                            outlined
                            dense
                            step="0.01"
                            min="0"
                            prefix="$"
                            @input="calcularLineaTotal(index)"
                          />
                        </div>

                        <div class="col-md-2 col-sm-6 col-xs-12">
                          <q-input
                            v-model.number="detalle.total_linea"
                            type="number"
                            label="Total Línea"
                            outlined
                            dense
                            prefix="$"
                            readonly
                            class="bg-grey-1"
                          />
                        </div>

                        <div class="col-auto">
                          <q-btn
                            color="red"
                            icon="delete"
                            @click="eliminarDetalle(index)"
                            dense
                            round
                          >
                            <q-tooltip>Eliminar línea</q-tooltip>
                          </q-btn>
                        </div>
                      </div>
                    </q-card-section>
                  </q-card>
                </div>
              </div>

              <!-- Observaciones -->
              <div class="row q-gutter-md">
                <div class="col-12">
                  <q-separator class="q-my-md" />
                  <h6 class="q-ma-none q-mb-md">Información Adicional</h6>
                </div>

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
  id_orden_compra: null,
  tipo_documento: null,
  numero_documento: '',
  fecha_documento: '',
  serie: '',
  folio: '',
  uuid_fiscal: '',
  rut_emisor: '',
  rut_receptor: '',
  subtotal: 0,
  impuestos: 0,
  descuentos: 0,
  total: 0,
  moneda: 'CLP',
  tipo_cambio: 1,
  contenido_xml: '',
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
  return formularioDocumento.tipo_documento &&
         formularioDocumento.numero_documento &&
         formularioDocumento.fecha_documento &&
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
    id_orden_compra: documento.id_orden_compra || null,
    tipo_documento: documento.tipo_documento,
    numero_documento: documento.numero_documento,
    fecha_documento: documento.fecha_documento,
    serie: documento.serie || '',
    folio: documento.folio || '',
    uuid_fiscal: documento.uuid_fiscal || '',
    rut_emisor: documento.rut_emisor || '',
    rut_receptor: documento.rut_receptor || '',
    subtotal: documento.subtotal || 0,
    impuestos: documento.impuestos || 0,
    descuentos: documento.descuentos || 0,
    total: documento.total || 0,
    moneda: documento.moneda || 'CLP',
    tipo_cambio: documento.tipo_cambio || 1,
    contenido_xml: documento.contenido_xml || '',
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