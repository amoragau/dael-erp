<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Movimientos de Inventario</h4>
          <p class="text-grey-7 q-mb-none">Control integral de movimientos con autorización y trazabilidad</p>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nuevo Movimiento"
          @click="abrirFormularioMovimiento"
        />
      </div>

      <!-- Stats Cards -->
      <div class="row q-gutter-md q-mb-md" v-if="estadisticas">
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-primary">{{ estadisticas.total_movimientos }}</div>
              <div class="text-caption">Total Movimientos</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-warning">{{ estadisticas.pendientes }}</div>
              <div class="text-caption">Pendientes</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-info">{{ estadisticas.autorizados }}</div>
              <div class="text-caption">Autorizados</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-positive">{{ estadisticas.procesados }}</div>
              <div class="text-caption">Procesados</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-3">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-secondary">${{ Number(estadisticas.valor_total).toLocaleString() }}</div>
              <div class="text-caption">Valor Total</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-gutter-md items-center">
            <q-input
              v-model="filtros.busqueda"
              placeholder="Buscar por número, motivo..."
              outlined
              dense
              clearable
              style="min-width: 250px"
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
              v-model="filtros.tipo_movimiento"
              :options="tiposMovimientoOptions"
              label="Tipo Movimiento"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 200px"
            />
            <q-input
              v-model="filtros.fecha_desde"
              label="Desde"
              outlined
              dense
              type="date"
              style="min-width: 150px"
            />
            <q-input
              v-model="filtros.fecha_hasta"
              label="Hasta"
              outlined
              dense
              type="date"
              style="min-width: 150px"
            />
            <q-btn
              color="primary"
              icon="search"
              label="Filtrar"
              @click="aplicarFiltros"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Movements Table -->
      <q-table
        :rows="movimientos"
        :columns="columnsMovimientos"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_movimiento"
        flat
        bordered
        @request="onRequestMovimientos"
      >
        <template v-slot:body-cell-numero_movimiento="props">
          <q-td :props="props">
            <div class="text-weight-medium">{{ props.value }}</div>
          </q-td>
        </template>

        <template v-slot:body-cell-tipo_movimiento="props">
          <q-td :props="props">
            <q-badge
              :color="getTipoMovimientoColor(props.row.tipo_movimiento)"
              :label="getTipoMovimientoLabel(props.row.tipo_movimiento)"
              :icon="getTipoMovimientoIcon(props.row.tipo_movimiento)"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-estado="props">
          <q-td :props="props">
            <q-badge
              :color="getEstadoColor(props.value)"
              :label="getEstadoLabel(props.value)"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-valor_total="props">
          <q-td :props="props">
            <div class="text-right text-weight-medium">
              ${{ Number(props.value).toLocaleString() }}
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-requiere_autorizacion="props">
          <q-td :props="props">
            <q-icon
              v-if="props.value"
              name="verified_user"
              color="warning"
              size="sm"
            >
              <q-tooltip>Requiere Autorización</q-tooltip>
            </q-icon>
          </q-td>
        </template>

        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn
              flat
              round
              icon="visibility"
              color="info"
              size="sm"
              @click="verDetalleMovimiento(props.row)"
            >
              <q-tooltip>Ver Detalles</q-tooltip>
            </q-btn>
            <q-btn
              v-if="props.row.estado === 'pendiente'"
              flat
              round
              icon="edit"
              color="primary"
              size="sm"
              @click="editarMovimiento(props.row)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              v-if="props.row.estado === 'pendiente' && props.row.requiere_autorizacion"
              flat
              round
              icon="verified_user"
              color="warning"
              size="sm"
              @click="autorizarMovimiento(props.row)"
            >
              <q-tooltip>Autorizar</q-tooltip>
            </q-btn>
            <q-btn
              v-if="props.row.estado === 'autorizado' || (props.row.estado === 'pendiente' && !props.row.requiere_autorizacion)"
              flat
              round
              icon="play_arrow"
              color="positive"
              size="sm"
              @click="procesarMovimiento(props.row)"
            >
              <q-tooltip>Procesar</q-tooltip>
            </q-btn>
            <q-btn
              v-if="props.row.estado === 'pendiente' || props.row.estado === 'autorizado'"
              flat
              round
              icon="cancel"
              color="negative"
              size="sm"
              @click="cancelarMovimiento(props.row)"
            >
              <q-tooltip>Cancelar</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Movement Dialog -->
      <q-dialog v-model="showCreateMovimientoDialog" persistent>
        <q-card style="min-width: 1200px; max-width: 1400px; max-height: 90vh">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">{{ editandoMovimiento ? 'Editar' : 'Nuevo' }} Movimiento</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section class="q-pt-none" style="max-height: calc(90vh - 120px);">
            <q-form @submit="guardarMovimiento">
              <div class="row" style="height: calc(90vh - 160px);">
                <div class="col-3">
                  <q-tabs
                    v-model="tabActivo"
                    vertical
                    class="text-primary full-height"
                  >
                    <q-tab name="cabecera" icon="description" label="Información General" />
                    <q-tab name="detalles" icon="list" label="Productos" />
                    <q-tab name="documento" icon="attach_file" label="Documento Soporte" />
                    <q-tab name="autorizacion" icon="verified_user" label="Autorización" />
                  </q-tabs>
                </div>
                <div class="col-9">
                  <q-tab-panels
                    v-model="tabActivo"
                    animated
                    class="full-height"
                    style="overflow-y: auto;"
                  >
                    <!-- Panel Información General -->
                    <q-tab-panel name="cabecera">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="description" class="q-mr-sm" />
                        Información General del Movimiento
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-4">
                          <q-select
                            v-model="formMovimiento.id_tipo_movimiento"
                            :options="tiposMovimientoOptions"
                            label="Tipo de Movimiento *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'El tipo de movimiento es requerido']"
                            @update:model-value="onTipoMovimientoChange"
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formMovimiento.fecha_movimiento"
                            label="Fecha Movimiento *"
                            outlined
                            dense
                            type="date"
                            :rules="[val => !!val || 'La fecha es requerida']"
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-badge
                            v-if="tipoMovimientoSeleccionado"
                            :color="getTipoMovimientoColor(tipoMovimientoSeleccionado)"
                            :label="tipoMovimientoSeleccionado.nombre_tipo"
                            class="q-pa-sm"
                          />
                        </div>
                      </div>

                      <!-- Transferencias: Bodegas -->
                      <div v-if="tipoMovimientoSeleccionado?.codigo_tipo === 'TRA'" class="q-mt-md">
                        <div class="text-subtitle1 q-mb-sm">Ubicaciones de Transferencia</div>
                        <q-separator class="q-mb-md" />

                        <div class="row q-gutter-md">
                          <div class="col-12 col-md-6">
                            <q-select
                              v-model="formMovimiento.id_bodega_origen"
                              :options="bodegasOptions"
                              label="Bodega Origen *"
                              outlined
                              dense
                              emit-value
                              map-options
                              :rules="[val => !!val || 'La bodega origen es requerida']"
                            />
                          </div>
                          <div class="col-12 col-md-5">
                            <q-select
                              v-model="formMovimiento.id_bodega_destino"
                              :options="bodegasOptions"
                              label="Bodega Destino *"
                              outlined
                              dense
                              emit-value
                              map-options
                              :rules="[val => !!val || 'La bodega destino es requerida']"
                            />
                          </div>
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12">
                          <q-input
                            v-model="formMovimiento.motivo"
                            label="Motivo *"
                            outlined
                            dense
                            :rules="[val => !!val || 'El motivo es requerido']"
                            hint="Razón del movimiento"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formMovimiento.observaciones"
                            label="Observaciones"
                            outlined
                            type="textarea"
                            rows="3"
                            hint="Comentarios adicionales"
                          />
                        </div>
                      </div>

                      <div v-if="tipoMovimientoSeleccionado?.requiere_autorizacion" class="q-mt-md">
                        <q-banner class="bg-warning text-dark">
                          <q-icon name="warning" class="q-mr-sm" />
                          Este tipo de movimiento requiere autorización antes de ser procesado
                        </q-banner>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Productos -->
                    <q-tab-panel name="detalles">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="list" class="q-mr-sm" />
                        Productos del Movimiento
                      </div>

                      <div class="row items-center justify-between q-mb-md">
                        <div class="text-subtitle2">Detalle de Productos</div>
                        <q-btn
                          color="primary"
                          icon="add"
                          label="Agregar Producto"
                          size="sm"
                          @click="abrirFormularioDetalle"
                        />
                      </div>

                      <q-table
                        :rows="detallesMovimiento"
                        :columns="columnsDetalles"
                        :loading="isLoadingDetalles"
                        row-key="id_detalle"
                        flat
                        bordered
                        dense
                      >
                        <template v-slot:body-cell-producto="props">
                          <q-td :props="props">
                            <div class="text-weight-medium">{{ getProductoNombre(props.row.id_producto) }}</div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-cantidad="props">
                          <q-td :props="props">
                            <div class="text-center text-weight-medium">
                              {{ Number(props.value).toLocaleString() }}
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-costo_unitario="props">
                          <q-td :props="props">
                            <div class="text-right">
                              ${{ Number(props.value).toLocaleString() }}
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-costo_total="props">
                          <q-td :props="props">
                            <div class="text-right text-weight-medium">
                              ${{ Number(props.value).toLocaleString() }}
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-ubicaciones="props">
                          <q-td :props="props">
                            <div v-if="props.row.ubicacion_origen || props.row.ubicacion_destino">
                              <div v-if="props.row.ubicacion_origen" class="text-caption">
                                Origen: {{ getUbicacionNombre(props.row.ubicacion_origen) }}
                              </div>
                              <div v-if="props.row.ubicacion_destino" class="text-caption">
                                Destino: {{ getUbicacionNombre(props.row.ubicacion_destino) }}
                              </div>
                            </div>
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
                              @click="editarDetalle(props.row)"
                            >
                              <q-tooltip>Editar</q-tooltip>
                            </q-btn>
                            <q-btn
                              flat
                              round
                              icon="delete"
                              color="negative"
                              size="sm"
                              @click="eliminarDetalle(props.row)"
                            >
                              <q-tooltip>Eliminar</q-tooltip>
                            </q-btn>
                          </q-td>
                        </template>
                      </q-table>

                      <div v-if="detallesMovimiento.length > 0" class="q-mt-md">
                        <q-separator />
                        <div class="row justify-end q-mt-sm">
                          <div class="text-h6">
                            Total: ${{ calcularTotalMovimiento().toLocaleString() }}
                          </div>
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Documento -->
                    <q-tab-panel name="documento">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="attach_file" class="q-mr-sm" />
                        Documento Soporte
                      </div>

                      <div class="text-subtitle2 q-mb-md">Respaldo Legal del Movimiento</div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-4">
                          <q-select
                            v-model="formDocumento.tipo_documento"
                            :options="tipoDocumentoOptions"
                            label="Tipo Documento"
                            outlined
                            dense
                            emit-value
                            map-options
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formDocumento.numero_documento"
                            label="Número Documento"
                            outlined
                            dense
                            hint="Número de factura, remisión, etc."
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model="formDocumento.fecha_documento"
                            label="Fecha Documento"
                            outlined
                            dense
                            type="date"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formDocumento.proveedor_cliente"
                            label="Proveedor/Cliente"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formDocumento.rut_proveedor_cliente"
                            label="RUT"
                            outlined
                            dense
                            mask="##.###.###-#"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model.number="formDocumento.monto_total"
                            label="Monto Total"
                            outlined
                            dense
                            type="number"
                            step="0.01"
                            prefix="$"
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-select
                            v-model="formDocumento.moneda"
                            :options="monedaOptions"
                            label="Moneda"
                            outlined
                            dense
                            emit-value
                            map-options
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formDocumento.observaciones"
                            label="Observaciones del Documento"
                            outlined
                            type="textarea"
                            rows="3"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-file
                            v-model="archivoDocumento"
                            label="Archivo Digital"
                            outlined
                            dense
                            accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
                            max-file-size="10485760"
                            @rejected="onRejectedFile"
                          >
                            <template v-slot:prepend>
                              <q-icon name="attach_file" />
                            </template>
                          </q-file>
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Autorización -->
                    <q-tab-panel name="autorizacion">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="verified_user" class="q-mr-sm" />
                        Control de Autorización
                      </div>

                      <q-card flat bordered v-if="!tipoMovimientoSeleccionado?.requiere_autorizacion">
                        <q-card-section class="text-center text-grey-6">
                          <q-icon name="info" size="md" class="q-mb-sm" />
                          <div>Este tipo de movimiento no requiere autorización</div>
                        </q-card-section>
                      </q-card>

                      <div v-else>
                        <q-banner class="bg-warning text-dark q-mb-md">
                          <q-icon name="warning" class="q-mr-sm" />
                          Este movimiento requiere autorización de un usuario con permisos
                        </q-banner>

                        <div class="text-subtitle1 q-mb-sm">Información de Autorización</div>
                        <q-separator class="q-mb-md" />

                        <div v-if="formMovimiento.id_movimiento && movimientoDetalle">
                          <div class="row q-gutter-md">
                            <div class="col-12 col-md-6">
                              <q-list bordered separator>
                                <q-item>
                                  <q-item-section>
                                    <q-item-label caption>Estado Actual</q-item-label>
                                    <q-item-label>
                                      <q-badge
                                        :color="getEstadoColor(movimientoDetalle.estado)"
                                        :label="getEstadoLabel(movimientoDetalle.estado)"
                                      />
                                    </q-item-label>
                                  </q-item-section>
                                </q-item>
                                <q-item v-if="movimientoDetalle.usuario_autoriza">
                                  <q-item-section>
                                    <q-item-label caption>Autorizado por</q-item-label>
                                    <q-item-label>{{ movimientoDetalle.usuario_autoriza.nombre }}</q-item-label>
                                  </q-item-section>
                                </q-item>
                                <q-item v-if="movimientoDetalle.fecha_autorizacion">
                                  <q-item-section>
                                    <q-item-label caption>Fecha Autorización</q-item-label>
                                    <q-item-label>{{ formatDateTime(movimientoDetalle.fecha_autorizacion) }}</q-item-label>
                                  </q-item-section>
                                </q-item>
                              </q-list>
                            </div>
                          </div>
                        </div>

                        <div v-else class="text-grey-6">
                          <q-icon name="info" class="q-mr-sm" />
                          Guarde el movimiento primero para gestionar la autorización
                        </div>
                      </div>
                    </q-tab-panel>
                  </q-tab-panels>
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right" class="q-pa-md">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar Movimiento"
              @click="guardarMovimiento"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Movement Detail Dialog -->
      <q-dialog v-model="showDetalleDialog" persistent>
        <q-card style="min-width: 800px; max-width: 1000px">
          <q-card-section class="row items-center">
            <div class="text-h6">Detalle del Movimiento</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section v-if="movimientoDetalle">
            <div class="row q-col-gutter-md">
              <!-- Información General -->
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Información General</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Número</q-item-label>
                      <q-item-label>{{ movimientoDetalle.numero_movimiento }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Tipo</q-item-label>
                      <q-item-label>
                        <q-badge
                          :color="getTipoMovimientoColor(movimientoDetalle.tipo_movimiento)"
                          :label="getTipoMovimientoLabel(movimientoDetalle.tipo_movimiento)"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Estado</q-item-label>
                      <q-item-label>
                        <q-badge
                          :color="getEstadoColor(movimientoDetalle.estado)"
                          :label="getEstadoLabel(movimientoDetalle.estado)"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Fecha</q-item-label>
                      <q-item-label>{{ formatDate(movimientoDetalle.fecha_movimiento) }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>

              <!-- Valores -->
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Valores</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Productos</q-item-label>
                      <q-item-label>{{ movimientoDetalle.cantidad_productos }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Valor Total</q-item-label>
                      <q-item-label class="text-weight-medium">
                        ${{ Number(movimientoDetalle.valor_total).toLocaleString() }}
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Motivo</q-item-label>
                      <q-item-label>{{ movimientoDetalle.motivo }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>

              <!-- Productos -->
              <div class="col-12">
                <q-expansion-item
                  icon="list"
                  label="Productos del Movimiento"
                  class="q-mt-md"
                >
                  <q-card flat bordered>
                    <q-card-section>
                      <q-table
                        :rows="movimientoDetalle.detalles || []"
                        :columns="columnsDetallesView"
                        row-key="id_detalle"
                        flat
                        dense
                      />
                    </q-card-section>
                  </q-card>
                </q-expansion-item>
              </div>
            </div>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cerrar" v-close-popup />
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
  useMovimientoStore,
  type MovimientoInventario,
  type MovimientoInventarioCreate,
  type MovimientoDetalle,
  type DocumentoMovimiento,
  type TipoMovimiento
} from '../stores/movimientos'

const $q = useQuasar()
const movimientoStore = useMovimientoStore()

// Reactive data
const movimientos = ref<MovimientoInventario[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const isLoadingDetalles = ref(false)
const showCreateMovimientoDialog = ref(false)
const showDetalleDialog = ref(false)
const editandoMovimiento = ref(false)
const movimientoDetalle = ref<MovimientoInventario | null>(null)
const detallesMovimiento = ref<MovimientoDetalle[]>([])
const estadisticas = ref<any>(null)
const tabActivo = ref('cabecera')
const archivoDocumento = ref<File | null>(null)

// Filters
const filtros = ref({
  busqueda: '',
  estado: null as string | null,
  tipo_movimiento: null as number | null,
  fecha_desde: '',
  fecha_hasta: ''
})

// Options
const estadoOptions = [
  { label: 'Pendiente', value: 'pendiente' },
  { label: 'Autorizado', value: 'autorizado' },
  { label: 'Procesado', value: 'procesado' },
  { label: 'Cancelado', value: 'cancelado' }
]

const tipoDocumentoOptions = [
  { label: 'Factura', value: 'factura' },
  { label: 'Remisión', value: 'remision' },
  { label: 'Orden de Compra', value: 'orden_compra' },
  { label: 'Guía de Despacho', value: 'guia_despacho' },
  { label: 'Nota de Crédito', value: 'nota_credito' },
  { label: 'Nota de Débito', value: 'nota_debito' },
  { label: 'Otro', value: 'otro' }
]

const monedaOptions = [
  { label: 'CLP - Peso Chileno', value: 'CLP' },
  { label: 'USD - Dólar Americano', value: 'USD' },
  { label: 'EUR - Euro', value: 'EUR' }
]

// Pagination
const paginacion = ref({
  sortBy: 'id_movimiento',
  descending: true,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formMovimiento = ref<MovimientoInventarioCreate & { id_movimiento?: number }>({
  id_tipo_movimiento: 0,
  fecha_movimiento: new Date().toISOString().split('T')[0],
  motivo: '',
  observaciones: '',
  id_documento: undefined,
  id_bodega_origen: undefined,
  id_bodega_destino: undefined,
  activo: true
})

const formDocumento = ref<any>({
  tipo_documento: 'factura',
  numero_documento: '',
  fecha_documento: '',
  proveedor_cliente: '',
  rut_proveedor_cliente: '',
  monto_total: undefined,
  moneda: 'CLP',
  observaciones: '',
  activo: true
})

// Computed
const tiposMovimientoOptions = computed(() => {
  return movimientoStore.tiposMovimiento.map(tipo => ({
    label: `${tipo.codigo_tipo} - ${tipo.nombre_tipo}`,
    value: tipo.id_tipo_movimiento,
    description: tipo.descripcion
  }))
})

const tipoMovimientoSeleccionado = computed(() => {
  return movimientoStore.tiposMovimiento.find(
    tipo => tipo.id_tipo_movimiento === formMovimiento.value.id_tipo_movimiento
  )
})

const bodegasOptions = computed(() => {
  // This would come from a bodegas store
  return []
})

// Table columns
const columnsMovimientos = [
  {
    name: 'numero_movimiento',
    required: true,
    label: 'Número',
    align: 'left' as const,
    field: 'numero_movimiento',
    sortable: true
  },
  {
    name: 'tipo_movimiento',
    label: 'Tipo',
    align: 'center' as const,
    field: 'tipo_movimiento',
    sortable: true
  },
  {
    name: 'fecha_movimiento',
    label: 'Fecha',
    align: 'center' as const,
    field: 'fecha_movimiento',
    sortable: true,
    format: (val: string) => formatDate(val)
  },
  {
    name: 'motivo',
    label: 'Motivo',
    align: 'left' as const,
    field: 'motivo'
  },
  {
    name: 'estado',
    label: 'Estado',
    align: 'center' as const,
    field: 'estado',
    sortable: true
  },
  {
    name: 'cantidad_productos',
    label: 'Productos',
    align: 'center' as const,
    field: 'cantidad_productos',
    sortable: true
  },
  {
    name: 'valor_total',
    label: 'Valor Total',
    align: 'right' as const,
    field: 'valor_total',
    sortable: true
  },
  {
    name: 'requiere_autorizacion',
    label: 'Auth',
    align: 'center' as const,
    field: 'requiere_autorizacion'
  },
  {
    name: 'actions',
    label: 'Acciones',
    align: 'center' as const,
    field: 'actions'
  }
]

const columnsDetalles = [
  {
    name: 'producto',
    required: true,
    label: 'Producto',
    align: 'left' as const,
    field: 'id_producto'
  },
  {
    name: 'cantidad',
    label: 'Cantidad',
    align: 'center' as const,
    field: 'cantidad'
  },
  {
    name: 'costo_unitario',
    label: 'Costo Unit.',
    align: 'right' as const,
    field: 'costo_unitario'
  },
  {
    name: 'costo_total',
    label: 'Total',
    align: 'right' as const,
    field: 'costo_total'
  },
  {
    name: 'ubicaciones',
    label: 'Ubicaciones',
    align: 'left' as const,
    field: 'ubicaciones'
  },
  {
    name: 'actions',
    label: 'Acciones',
    align: 'center' as const,
    field: 'actions'
  }
]

const columnsDetallesView = [
  {
    name: 'producto',
    required: true,
    label: 'Producto',
    align: 'left' as const,
    field: (row: MovimientoDetalle) => getProductoNombre(row.id_producto)
  },
  {
    name: 'cantidad',
    label: 'Cantidad',
    align: 'center' as const,
    field: 'cantidad',
    format: (val: number) => Number(val).toLocaleString()
  },
  {
    name: 'costo_unitario',
    label: 'Costo Unit.',
    align: 'right' as const,
    field: 'costo_unitario',
    format: (val: number) => `$${Number(val).toLocaleString()}`
  },
  {
    name: 'costo_total',
    label: 'Total',
    align: 'right' as const,
    field: 'costo_total',
    format: (val: number) => `$${Number(val).toLocaleString()}`
  }
]

// Methods
const onRequestMovimientos = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarMovimientos()
}

const cargarMovimientos = async () => {
  try {
    isLoading.value = true
    const params: any = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    if (filtros.value.estado) params.estado = filtros.value.estado
    if (filtros.value.tipo_movimiento) params.tipo_movimiento = filtros.value.tipo_movimiento
    if (filtros.value.fecha_desde) params.fecha_desde = filtros.value.fecha_desde
    if (filtros.value.fecha_hasta) params.fecha_hasta = filtros.value.fecha_hasta

    const response = await movimientoStore.obtenerMovimientosInventario(params)
    movimientos.value = response

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar movimientos',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const cargarEstadisticas = async () => {
  try {
    const params: any = {}
    if (filtros.value.fecha_desde) params.fecha_desde = filtros.value.fecha_desde
    if (filtros.value.fecha_hasta) params.fecha_hasta = filtros.value.fecha_hasta

    estadisticas.value = await movimientoStore.obtenerEstadisticasMovimientos(params)
  } catch (error: any) {
    console.error('Error al cargar estadísticas:', error)
  }
}

const aplicarFiltros = async () => {
  paginacion.value.page = 1
  await cargarMovimientos()
  await cargarEstadisticas()
}

const abrirFormularioMovimiento = () => {
  resetFormMovimiento()
  showCreateMovimientoDialog.value = true
}

const editarMovimiento = (movimiento: MovimientoInventario) => {
  editandoMovimiento.value = true
  formMovimiento.value = { ...movimiento }
  showCreateMovimientoDialog.value = true
}

const guardarMovimiento = async () => {
  try {
    isGuardando.value = true

    if (editandoMovimiento.value && formMovimiento.value.id_movimiento) {
      await movimientoStore.actualizarMovimientoInventario(formMovimiento.value.id_movimiento, formMovimiento.value)
      $q.notify({
        type: 'positive',
        message: 'Movimiento actualizado correctamente'
      })
    } else {
      await movimientoStore.crearMovimientoInventario(formMovimiento.value)
      $q.notify({
        type: 'positive',
        message: 'Movimiento creado correctamente'
      })
    }

    showCreateMovimientoDialog.value = false
    resetFormMovimiento()
    await cargarMovimientos()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar movimiento',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const verDetalleMovimiento = async (movimiento: MovimientoInventario) => {
  try {
    movimientoDetalle.value = await movimientoStore.obtenerMovimientoInventario(movimiento.id_movimiento)
    showDetalleDialog.value = true
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar detalles del movimiento',
      caption: error.message
    })
  }
}

const autorizarMovimiento = async (movimiento: MovimientoInventario) => {
  $q.dialog({
    title: 'Autorizar Movimiento',
    message: `¿Está seguro de autorizar el movimiento ${movimiento.numero_movimiento}?`,
    prompt: {
      model: '',
      type: 'textarea',
      label: 'Observaciones de autorización (opcional)'
    },
    cancel: true,
    persistent: true
  }).onOk(async (observaciones) => {
    try {
      await movimientoStore.autorizarMovimiento(movimiento.id_movimiento, observaciones)
      $q.notify({
        type: 'positive',
        message: 'Movimiento autorizado correctamente'
      })
      await cargarMovimientos()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al autorizar movimiento',
        caption: error.message
      })
    }
  })
}

const procesarMovimiento = async (movimiento: MovimientoInventario) => {
  $q.dialog({
    title: 'Procesar Movimiento',
    message: `¿Está seguro de procesar el movimiento ${movimiento.numero_movimiento}? Esta acción afectará el inventario y no se puede deshacer.`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await movimientoStore.procesarMovimiento(movimiento.id_movimiento)
      $q.notify({
        type: 'positive',
        message: 'Movimiento procesado correctamente'
      })
      await cargarMovimientos()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al procesar movimiento',
        caption: error.message
      })
    }
  })
}

const cancelarMovimiento = async (movimiento: MovimientoInventario) => {
  $q.dialog({
    title: 'Cancelar Movimiento',
    message: `¿Está seguro de cancelar el movimiento ${movimiento.numero_movimiento}?`,
    prompt: {
      model: '',
      type: 'text',
      label: 'Motivo de cancelación *',
      isValid: val => !!val
    },
    cancel: true,
    persistent: true
  }).onOk(async (motivo) => {
    try {
      await movimientoStore.cancelarMovimiento(movimiento.id_movimiento, motivo)
      $q.notify({
        type: 'positive',
        message: 'Movimiento cancelado correctamente'
      })
      await cargarMovimientos()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al cancelar movimiento',
        caption: error.message
      })
    }
  })
}

const resetFormMovimiento = () => {
  editandoMovimiento.value = false
  tabActivo.value = 'cabecera'
  formMovimiento.value = {
    id_tipo_movimiento: 0,
    fecha_movimiento: new Date().toISOString().split('T')[0],
    motivo: '',
    observaciones: '',
    id_documento: undefined,
    id_bodega_origen: undefined,
    id_bodega_destino: undefined,
    activo: true
  }
  formDocumento.value = {
    tipo_documento: 'factura',
    numero_documento: '',
    fecha_documento: '',
    proveedor_cliente: '',
    rut_proveedor_cliente: '',
    monto_total: undefined,
    moneda: 'CLP',
    observaciones: '',
    activo: true
  }
  detallesMovimiento.value = []
}

const onTipoMovimientoChange = (tipoId: number) => {
  const tipo = movimientoStore.tiposMovimiento.find(t => t.id_tipo_movimiento === tipoId)
  if (tipo?.codigo_tipo !== 'TRA') {
    formMovimiento.value.id_bodega_origen = undefined
    formMovimiento.value.id_bodega_destino = undefined
  }
}

const abrirFormularioDetalle = () => {
  // TODO: Implement detail form
}

const editarDetalle = (detalle: MovimientoDetalle) => {
  // TODO: Implement detail editing
}

const eliminarDetalle = (detalle: MovimientoDetalle) => {
  // TODO: Implement detail deletion
}

const calcularTotalMovimiento = (): number => {
  return detallesMovimiento.value.reduce((total, detalle) => total + detalle.costo_total, 0)
}

const onRejectedFile = (rejectedEntries: any[]) => {
  $q.notify({
    type: 'negative',
    message: `Archivo no válido: ${rejectedEntries[0].failedPropValidation}`
  })
}

// Helper methods
const getTipoMovimientoColor = (tipo: TipoMovimiento): string => {
  if (!tipo) return 'grey'

  const colorMap: { [key: string]: string } = {
    'ENT': 'positive',
    'SAL': 'negative',
    'DSO': 'orange',
    'DVO': 'positive',
    'USO': 'info',
    'AJU': 'warning',
    'TRA': 'blue',
    'DEV': 'positive',
    'MER': 'deep-orange',
    'DAÑ': 'red',
    'PER': 'brown'
  }

  return colorMap[tipo.codigo_tipo] || 'grey'
}

const getTipoMovimientoLabel = (tipo: TipoMovimiento): string => {
  return tipo ? `${tipo.codigo_tipo} - ${tipo.nombre_tipo}` : '-'
}

const getTipoMovimientoIcon = (tipo: TipoMovimiento): string => {
  if (!tipo) return 'help'

  const iconMap: { [key: string]: string } = {
    'ENT': 'input',
    'SAL': 'output',
    'DSO': 'local_shipping',
    'DVO': 'keyboard_return',
    'USO': 'build',
    'AJU': 'tune',
    'TRA': 'swap_horiz',
    'DEV': 'undo',
    'MER': 'trending_down',
    'DAÑ': 'report_problem',
    'PER': 'error'
  }

  return iconMap[tipo.codigo_tipo] || 'help'
}

const getEstadoColor = (estado: string): string => {
  const colorMap: { [key: string]: string } = {
    'pendiente': 'warning',
    'autorizado': 'info',
    'procesado': 'positive',
    'cancelado': 'negative'
  }

  return colorMap[estado] || 'grey'
}

const getEstadoLabel = (estado: string): string => {
  const labelMap: { [key: string]: string } = {
    'pendiente': 'Pendiente',
    'autorizado': 'Autorizado',
    'procesado': 'Procesado',
    'cancelado': 'Cancelado'
  }

  return labelMap[estado] || estado
}

const getProductoNombre = (productoId: number): string => {
  // TODO: Get from products store
  return `Producto ${productoId}`
}

const getUbicacionNombre = (ubicacion: any): string => {
  // TODO: Get from locations
  return ubicacion ? 'Ubicación' : '-'
}

const formatDate = (dateString: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-CL')
}

const formatDateTime = (dateString: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('es-CL')
}

// Lifecycle
onMounted(async () => {
  await movimientoStore.obtenerTiposMovimiento({ activo: true })
  await cargarMovimientos()
  await cargarEstadisticas()
})
</script>