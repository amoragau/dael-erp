<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Traspasos entre Bodegas</h4>
          <p class="text-grey-7 q-mb-none">Control de transferencias de productos entre bodegas</p>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nuevo Traspaso"
          @click="abrirFormularioTraspaso"
        />
      </div>

      <!-- Stats Cards -->
      <div class="row q-gutter-md q-mb-md" v-if="estadisticas">
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-primary">{{ estadisticas.total_traspasos }}</div>
              <div class="text-caption">Total Traspasos</div>
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
              <div class="text-h6 text-info">{{ estadisticas.en_transito }}</div>
              <div class="text-caption">En Tránsito</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-positive">{{ estadisticas.completados }}</div>
              <div class="text-caption">Completados</div>
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
              v-model="filtros.id_bodega_origen"
              :options="bodegasOptions"
              label="Bodega Origen"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 180px"
            />
            <q-select
              v-model="filtros.id_bodega_destino"
              :options="bodegasOptions"
              label="Bodega Destino"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 180px"
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

      <!-- Transfers Table -->
      <q-table
        :rows="traspasos"
        :columns="columnsTraspasos"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_traspaso"
        flat
        bordered
        @request="onRequestTraspasos"
      >
        <template v-slot:body-cell-numero_traspaso="props">
          <q-td :props="props">
            <div class="text-weight-medium">{{ props.value }}</div>
          </q-td>
        </template>

        <template v-slot:body-cell-estado="props">
          <q-td :props="props">
            <q-badge
              :color="getEstadoColor(props.value)"
              :label="getEstadoLabel(props.value)"
              :icon="getEstadoIcon(props.value)"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-bodega_origen="props">
          <q-td :props="props">
            <div class="text-weight-medium">{{ getBodegaNombre(props.row.id_bodega_origen) }}</div>
            <div class="text-caption text-grey-6">{{ getBodegaCodigo(props.row.id_bodega_origen) }}</div>
          </q-td>
        </template>

        <template v-slot:body-cell-bodega_destino="props">
          <q-td :props="props">
            <div class="text-weight-medium">{{ getBodegaNombre(props.row.id_bodega_destino) }}</div>
            <div class="text-caption text-grey-6">{{ getBodegaCodigo(props.row.id_bodega_destino) }}</div>
          </q-td>
        </template>

        <template v-slot:body-cell-valor_total="props">
          <q-td :props="props">
            <div class="text-right text-weight-medium">
              ${{ Number(props.value).toLocaleString() }}
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-cantidad_productos="props">
          <q-td :props="props">
            <div class="text-center">{{ props.value }}</div>
          </q-td>
        </template>

        <template v-slot:body-cell-progreso="props">
          <q-td :props="props">
            <div class="row items-center q-gutter-sm">
              <q-linear-progress
                :value="props.row.porcentaje_completado / 100"
                color="primary"
                size="8px"
                style="min-width: 60px"
              />
              <span class="text-caption">{{ props.row.porcentaje_completado }}%</span>
            </div>
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
              @click="verDetalleTraspaso(props.row)"
            >
              <q-tooltip>Ver Detalles</q-tooltip>
            </q-btn>
            <q-btn
              v-if="props.row.estado === 'borrador'"
              flat
              round
              icon="edit"
              color="primary"
              size="sm"
              @click="editarTraspaso(props.row)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              v-if="props.row.estado === 'borrador'"
              flat
              round
              icon="send"
              color="warning"
              size="sm"
              @click="enviarTraspaso(props.row)"
            >
              <q-tooltip>Enviar</q-tooltip>
            </q-btn>
            <q-btn
              v-if="props.row.estado === 'enviado'"
              flat
              round
              icon="local_shipping"
              color="info"
              size="sm"
              @click="marcarEnTransito(props.row)"
            >
              <q-tooltip>Marcar en Tránsito</q-tooltip>
            </q-btn>
            <q-btn
              v-if="props.row.estado === 'en_transito'"
              flat
              round
              icon="inventory"
              color="positive"
              size="sm"
              @click="recibirTraspaso(props.row)"
            >
              <q-tooltip>Recibir</q-tooltip>
            </q-btn>
            <q-btn
              v-if="['borrador', 'enviado'].includes(props.row.estado)"
              flat
              round
              icon="cancel"
              color="negative"
              size="sm"
              @click="cancelarTraspaso(props.row)"
            >
              <q-tooltip>Cancelar</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Transfer Dialog -->
      <q-dialog v-model="showCreateTraspasoDialog" persistent>
        <q-card style="min-width: 1200px; max-width: 1400px; max-height: 90vh">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">{{ editandoTraspaso ? 'Editar' : 'Nuevo' }} Traspaso</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section class="q-pt-none" style="max-height: calc(90vh - 120px);">
            <q-form @submit="guardarTraspaso">
              <div class="row" style="height: calc(90vh - 160px);">
                <div class="col-3">
                  <q-tabs
                    v-model="tabActivo"
                    vertical
                    class="text-primary full-height"
                  >
                    <q-tab name="general" icon="description" label="Información General" />
                    <q-tab name="productos" icon="list" label="Productos a Traspasar" />
                    <q-tab name="transporte" icon="local_shipping" label="Transporte" />
                    <q-tab name="seguimiento" icon="timeline" label="Seguimiento" />
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
                    <q-tab-panel name="general">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="description" class="q-mr-sm" />
                        Información General del Traspaso
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formTraspaso.fecha_traspaso"
                            label="Fecha Traspaso *"
                            outlined
                            dense
                            type="date"
                            :rules="[val => !!val || 'La fecha es requerida']"
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formTraspaso.fecha_estimada_llegada"
                            label="Fecha Estimada Llegada"
                            outlined
                            dense
                            type="date"
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-select
                            v-model="formTraspaso.prioridad"
                            :options="prioridadOptions"
                            label="Prioridad"
                            outlined
                            dense
                            emit-value
                            map-options
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12 col-md-6">
                          <q-select
                            v-model="formTraspaso.id_bodega_origen"
                            :options="bodegasOptions"
                            label="Bodega Origen *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'La bodega origen es requerida']"
                            @update:model-value="onBodegaOrigenChange"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-select
                            v-model="formTraspaso.id_bodega_destino"
                            :options="bodegasDestinoOptions"
                            label="Bodega Destino *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'La bodega destino es requerida']"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12">
                          <q-input
                            v-model="formTraspaso.motivo"
                            label="Motivo del Traspaso *"
                            outlined
                            dense
                            :rules="[val => !!val || 'El motivo es requerido']"
                            hint="Razón del traspaso"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formTraspaso.observaciones"
                            label="Observaciones"
                            outlined
                            type="textarea"
                            rows="3"
                            hint="Comentarios adicionales"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formTraspaso.numero_documento_referencia"
                            label="Número Documento Referencia"
                            outlined
                            dense
                            hint="Orden de trabajo, solicitud, etc."
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formTraspaso.solicitante"
                            label="Solicitante"
                            outlined
                            dense
                            hint="Persona que solicita el traspaso"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Productos -->
                    <q-tab-panel name="productos">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="list" class="q-mr-sm" />
                        Productos a Traspasar
                      </div>

                      <div class="row items-center justify-between q-mb-md">
                        <div class="text-subtitle2">Detalle de Productos</div>
                        <q-btn
                          color="primary"
                          icon="add"
                          label="Agregar Producto"
                          size="sm"
                          @click="abrirFormularioDetalleTraspaso"
                          :disable="!formTraspaso.id_bodega_origen"
                        />
                      </div>

                      <q-banner v-if="!formTraspaso.id_bodega_origen" class="bg-warning text-dark q-mb-md">
                        <q-icon name="warning" class="q-mr-sm" />
                        Seleccione una bodega origen para agregar productos
                      </q-banner>

                      <q-table
                        :rows="detallesTraspaso"
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
                            <div class="text-caption text-grey-6">{{ getProductoCodigo(props.row.id_producto) }}</div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-stock_disponible="props">
                          <q-td :props="props">
                            <div class="text-center">{{ Number(props.value).toLocaleString() }}</div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-cantidad_solicitada="props">
                          <q-td :props="props">
                            <div class="text-center text-weight-medium">{{ Number(props.value).toLocaleString() }}</div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-cantidad_enviada="props">
                          <q-td :props="props">
                            <div class="text-center" :class="props.value < props.row.cantidad_solicitada ? 'text-warning' : 'text-positive'">
                              {{ Number(props.value).toLocaleString() }}
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-cantidad_recibida="props">
                          <q-td :props="props">
                            <div class="text-center" :class="props.value < props.row.cantidad_enviada ? 'text-warning' : 'text-positive'">
                              {{ Number(props.value).toLocaleString() }}
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-costo_unitario="props">
                          <q-td :props="props">
                            <div class="text-right">${{ Number(props.value).toLocaleString() }}</div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-valor_total="props">
                          <q-td :props="props">
                            <div class="text-right text-weight-medium">
                              ${{ Number(props.value).toLocaleString() }}
                            </div>
                          </q-td>
                        </template>

                        <template v-slot:body-cell-estado_producto="props">
                          <q-td :props="props">
                            <q-badge
                              :color="getEstadoProductoColor(props.value)"
                              :label="getEstadoProductoLabel(props.value)"
                            />
                          </q-td>
                        </template>

                        <template v-slot:body-cell-actions="props">
                          <q-td :props="props">
                            <q-btn
                              v-if="formTraspaso.estado === 'borrador'"
                              flat
                              round
                              icon="edit"
                              color="primary"
                              size="sm"
                              @click="editarDetalleTraspaso(props.row)"
                            >
                              <q-tooltip>Editar</q-tooltip>
                            </q-btn>
                            <q-btn
                              v-if="formTraspaso.estado === 'borrador'"
                              flat
                              round
                              icon="delete"
                              color="negative"
                              size="sm"
                              @click="eliminarDetalleTraspaso(props.row)"
                            >
                              <q-tooltip>Eliminar</q-tooltip>
                            </q-btn>
                          </q-td>
                        </template>
                      </q-table>

                      <div v-if="detallesTraspaso.length > 0" class="q-mt-md">
                        <q-separator />
                        <div class="row justify-end q-mt-sm">
                          <div class="text-h6">
                            Total: ${{ calcularTotalTraspaso().toLocaleString() }}
                          </div>
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Transporte -->
                    <q-tab-panel name="transporte">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="local_shipping" class="q-mr-sm" />
                        Información de Transporte
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-4">
                          <q-select
                            v-model="formTraspaso.tipo_transporte"
                            :options="tipoTransporteOptions"
                            label="Tipo de Transporte"
                            outlined
                            dense
                            emit-value
                            map-options
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formTraspaso.transportista"
                            label="Transportista/Empresa"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model="formTraspaso.patente_vehiculo"
                            label="Patente Vehículo"
                            outlined
                            dense
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formTraspaso.conductor"
                            label="Conductor"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formTraspaso.telefono_conductor"
                            label="Teléfono Conductor"
                            outlined
                            dense
                            mask="(##) ####-####"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12">
                          <q-input
                            v-model="formTraspaso.observaciones_transporte"
                            label="Observaciones de Transporte"
                            outlined
                            type="textarea"
                            rows="3"
                            hint="Instrucciones especiales para el transporte"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formTraspaso.numero_guia_despacho"
                            label="Número Guía de Despacho"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formTraspaso.fecha_despacho"
                            label="Fecha Despacho"
                            outlined
                            dense
                            type="datetime-local"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Seguimiento -->
                    <q-tab-panel name="seguimiento">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="timeline" class="q-mr-sm" />
                        Seguimiento del Traspaso
                      </div>

                      <div v-if="formTraspaso.id_traspaso">
                        <q-timeline>
                          <q-timeline-entry
                            :title="'Traspaso Creado'"
                            :subtitle="formatDateTime(traspasoDetalle?.fecha_creacion)"
                            icon="create"
                            color="primary"
                          >
                            <div>Usuario: {{ traspasoDetalle?.usuario_crea?.nombre }}</div>
                          </q-timeline-entry>

                          <q-timeline-entry
                            v-if="traspasoDetalle?.fecha_envio"
                            :title="'Traspaso Enviado'"
                            :subtitle="formatDateTime(traspasoDetalle.fecha_envio)"
                            icon="send"
                            color="warning"
                          >
                            <div>Usuario: {{ traspasoDetalle.usuario_envia?.nombre }}</div>
                          </q-timeline-entry>

                          <q-timeline-entry
                            v-if="traspasoDetalle?.fecha_despacho"
                            :title="'En Tránsito'"
                            :subtitle="formatDateTime(traspasoDetalle.fecha_despacho)"
                            icon="local_shipping"
                            color="info"
                          >
                            <div>Guía: {{ traspasoDetalle.numero_guia_despacho }}</div>
                            <div v-if="traspasoDetalle.transportista">Transportista: {{ traspasoDetalle.transportista }}</div>
                          </q-timeline-entry>

                          <q-timeline-entry
                            v-if="traspasoDetalle?.fecha_recepcion"
                            :title="'Recibido'"
                            :subtitle="formatDateTime(traspasoDetalle.fecha_recepcion)"
                            icon="inventory"
                            color="positive"
                          >
                            <div>Usuario: {{ traspasoDetalle.usuario_recibe?.nombre }}</div>
                          </q-timeline-entry>

                          <q-timeline-entry
                            v-if="traspasoDetalle?.estado === 'cancelado'"
                            :title="'Cancelado'"
                            :subtitle="formatDateTime(traspasoDetalle.fecha_cancelacion)"
                            icon="cancel"
                            color="negative"
                          >
                            <div>Motivo: {{ traspasoDetalle.motivo_cancelacion }}</div>
                          </q-timeline-entry>
                        </q-timeline>

                        <div v-if="traspasoDetalle?.estado === 'completado'" class="q-mt-md">
                          <q-card flat bordered class="bg-positive text-white">
                            <q-card-section class="text-center">
                              <q-icon name="check_circle" size="lg" class="q-mb-sm" />
                              <div class="text-h6">Traspaso Completado</div>
                              <div>Todos los productos han sido recibidos exitosamente</div>
                            </q-card-section>
                          </q-card>
                        </div>
                      </div>

                      <div v-else class="text-grey-6">
                        <q-icon name="info" class="q-mr-sm" />
                        Guarde el traspaso primero para ver el seguimiento
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
              label="Guardar Traspaso"
              @click="guardarTraspaso"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Transfer Detail Dialog -->
      <q-dialog v-model="showDetalleDialog" persistent>
        <q-card style="min-width: 1000px; max-width: 1200px">
          <q-card-section class="row items-center">
            <div class="text-h6">Detalle del Traspaso</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section v-if="traspasoDetalle">
            <div class="row q-col-gutter-md">
              <!-- Información General -->
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Información General</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Número</q-item-label>
                      <q-item-label>{{ traspasoDetalle.numero_traspaso }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Estado</q-item-label>
                      <q-item-label>
                        <q-badge
                          :color="getEstadoColor(traspasoDetalle.estado)"
                          :label="getEstadoLabel(traspasoDetalle.estado)"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Bodega Origen</q-item-label>
                      <q-item-label>{{ getBodegaNombre(traspasoDetalle.id_bodega_origen) }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Bodega Destino</q-item-label>
                      <q-item-label>{{ getBodegaNombre(traspasoDetalle.id_bodega_destino) }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Fecha</q-item-label>
                      <q-item-label>{{ formatDate(traspasoDetalle.fecha_traspaso) }}</q-item-label>
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
                      <q-item-label>{{ traspasoDetalle.cantidad_productos }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Valor Total</q-item-label>
                      <q-item-label class="text-weight-medium">
                        ${{ Number(traspasoDetalle.valor_total).toLocaleString() }}
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Progreso</q-item-label>
                      <q-item-label>
                        <q-linear-progress
                          :value="traspasoDetalle.porcentaje_completado / 100"
                          color="primary"
                          size="12px"
                        />
                        <div class="text-caption q-mt-xs">{{ traspasoDetalle.porcentaje_completado }}% completado</div>
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Motivo</q-item-label>
                      <q-item-label>{{ traspasoDetalle.motivo }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>

              <!-- Productos -->
              <div class="col-12">
                <q-expansion-item
                  icon="list"
                  label="Productos del Traspaso"
                  class="q-mt-md"
                >
                  <q-card flat bordered>
                    <q-card-section>
                      <q-table
                        :rows="traspasoDetalle.detalles || []"
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

const $q = useQuasar()

// Types
interface Traspaso {
  id_traspaso: number
  numero_traspaso: string
  id_bodega_origen: number
  id_bodega_destino: number
  fecha_traspaso: string
  fecha_estimada_llegada?: string
  prioridad: string
  motivo: string
  observaciones?: string
  numero_documento_referencia?: string
  solicitante?: string
  estado: string
  cantidad_productos: number
  valor_total: number
  porcentaje_completado: number
  tipo_transporte?: string
  transportista?: string
  patente_vehiculo?: string
  conductor?: string
  telefono_conductor?: string
  observaciones_transporte?: string
  numero_guia_despacho?: string
  fecha_despacho?: string
  fecha_creacion: string
  usuario_crea?: { nombre: string }
  fecha_envio?: string
  usuario_envia?: { nombre: string }
  fecha_recepcion?: string
  usuario_recibe?: { nombre: string }
  fecha_cancelacion?: string
  motivo_cancelacion?: string
  detalles?: DetalleTraspaso[]
}

interface TraspasoCreate {
  id_bodega_origen: number
  id_bodega_destino: number
  fecha_traspaso: string
  fecha_estimada_llegada?: string
  prioridad: string
  motivo: string
  observaciones?: string
  numero_documento_referencia?: string
  solicitante?: string
  tipo_transporte?: string
  transportista?: string
  patente_vehiculo?: string
  conductor?: string
  telefono_conductor?: string
  observaciones_transporte?: string
  numero_guia_despacho?: string
  fecha_despacho?: string
  activo: boolean
}

interface DetalleTraspaso {
  id_detalle?: number
  id_traspaso?: number
  id_producto: number
  stock_disponible: number
  cantidad_solicitada: number
  cantidad_enviada: number
  cantidad_recibida: number
  costo_unitario: number
  valor_total: number
  estado_producto: string
  observaciones_detalle?: string
}

// Reactive data
const traspasos = ref<Traspaso[]>([])
const detallesTraspaso = ref<DetalleTraspaso[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const isLoadingDetalles = ref(false)
const showCreateTraspasoDialog = ref(false)
const showDetalleDialog = ref(false)
const editandoTraspaso = ref(false)
const traspasoDetalle = ref<Traspaso | null>(null)
const estadisticas = ref<any>(null)
const tabActivo = ref('general')

// Filters
const filtros = ref({
  busqueda: '',
  estado: null as string | null,
  id_bodega_origen: null as number | null,
  id_bodega_destino: null as number | null,
  fecha_desde: '',
  fecha_hasta: ''
})

// Options
const estadoOptions = [
  { label: 'Borrador', value: 'borrador' },
  { label: 'Enviado', value: 'enviado' },
  { label: 'En Tránsito', value: 'en_transito' },
  { label: 'Recibido', value: 'recibido' },
  { label: 'Completado', value: 'completado' },
  { label: 'Cancelado', value: 'cancelado' }
]

const prioridadOptions = [
  { label: 'Baja', value: 'baja' },
  { label: 'Normal', value: 'normal' },
  { label: 'Alta', value: 'alta' },
  { label: 'Urgente', value: 'urgente' }
]

const tipoTransporteOptions = [
  { label: 'Interno', value: 'interno' },
  { label: 'Externo', value: 'externo' },
  { label: 'Propio', value: 'propio' },
  { label: 'Tercerizado', value: 'tercerizado' }
]

const bodegasOptions = ref([])

// Pagination
const paginacion = ref({
  sortBy: 'id_traspaso',
  descending: true,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formTraspaso = ref<TraspasoCreate & { id_traspaso?: number; estado?: string }>({
  id_bodega_origen: 0,
  id_bodega_destino: 0,
  fecha_traspaso: new Date().toISOString().split('T')[0],
  fecha_estimada_llegada: '',
  prioridad: 'normal',
  motivo: '',
  observaciones: '',
  numero_documento_referencia: '',
  solicitante: '',
  tipo_transporte: 'interno',
  transportista: '',
  patente_vehiculo: '',
  conductor: '',
  telefono_conductor: '',
  observaciones_transporte: '',
  numero_guia_despacho: '',
  fecha_despacho: '',
  activo: true
})

// Computed
const bodegasDestinoOptions = computed(() => {
  return bodegasOptions.value.filter((bodega: any) => bodega.value !== formTraspaso.value.id_bodega_origen)
})

// Table columns
const columnsTraspasos = [
  {
    name: 'numero_traspaso',
    required: true,
    label: 'Número',
    align: 'left' as const,
    field: 'numero_traspaso',
    sortable: true
  },
  {
    name: 'bodega_origen',
    label: 'Origen',
    align: 'left' as const,
    field: 'id_bodega_origen',
    sortable: true
  },
  {
    name: 'bodega_destino',
    label: 'Destino',
    align: 'left' as const,
    field: 'id_bodega_destino',
    sortable: true
  },
  {
    name: 'fecha_traspaso',
    label: 'Fecha',
    align: 'center' as const,
    field: 'fecha_traspaso',
    sortable: true,
    format: (val: string) => formatDate(val)
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
    name: 'progreso',
    label: 'Progreso',
    align: 'center' as const,
    field: 'porcentaje_completado'
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
    name: 'stock_disponible',
    label: 'Stock Disp.',
    align: 'center' as const,
    field: 'stock_disponible'
  },
  {
    name: 'cantidad_solicitada',
    label: 'Cant. Solicitada',
    align: 'center' as const,
    field: 'cantidad_solicitada'
  },
  {
    name: 'cantidad_enviada',
    label: 'Cant. Enviada',
    align: 'center' as const,
    field: 'cantidad_enviada'
  },
  {
    name: 'cantidad_recibida',
    label: 'Cant. Recibida',
    align: 'center' as const,
    field: 'cantidad_recibida'
  },
  {
    name: 'costo_unitario',
    label: 'Costo Unit.',
    align: 'right' as const,
    field: 'costo_unitario'
  },
  {
    name: 'valor_total',
    label: 'Valor Total',
    align: 'right' as const,
    field: 'valor_total'
  },
  {
    name: 'estado_producto',
    label: 'Estado',
    align: 'center' as const,
    field: 'estado_producto'
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
    field: (row: DetalleTraspaso) => getProductoNombre(row.id_producto)
  },
  {
    name: 'cantidad_solicitada',
    label: 'Solicitada',
    align: 'center' as const,
    field: 'cantidad_solicitada',
    format: (val: number) => Number(val).toLocaleString()
  },
  {
    name: 'cantidad_enviada',
    label: 'Enviada',
    align: 'center' as const,
    field: 'cantidad_enviada',
    format: (val: number) => Number(val).toLocaleString()
  },
  {
    name: 'cantidad_recibida',
    label: 'Recibida',
    align: 'center' as const,
    field: 'cantidad_recibida',
    format: (val: number) => Number(val).toLocaleString()
  },
  {
    name: 'valor_total',
    label: 'Valor Total',
    align: 'right' as const,
    field: 'valor_total',
    format: (val: number) => `$${Number(val).toLocaleString()}`
  }
]

// Methods
const onRequestTraspasos = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarTraspasos()
}

const cargarTraspasos = async () => {
  try {
    isLoading.value = true
    // TODO: Implement API call
    traspasos.value = []
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar traspasos',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const cargarEstadisticas = async () => {
  try {
    // TODO: Implement API call
    estadisticas.value = {
      total_traspasos: 0,
      pendientes: 0,
      en_transito: 0,
      completados: 0,
      valor_total: 0
    }
  } catch (error: any) {
    console.error('Error al cargar estadísticas:', error)
  }
}

const aplicarFiltros = async () => {
  paginacion.value.page = 1
  await cargarTraspasos()
  await cargarEstadisticas()
}

const abrirFormularioTraspaso = () => {
  resetFormTraspaso()
  showCreateTraspasoDialog.value = true
}

const editarTraspaso = (traspaso: Traspaso) => {
  editandoTraspaso.value = true
  formTraspaso.value = { ...traspaso }
  showCreateTraspasoDialog.value = true
}

const guardarTraspaso = async () => {
  try {
    isGuardando.value = true

    if (editandoTraspaso.value && formTraspaso.value.id_traspaso) {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Traspaso actualizado correctamente'
      })
    } else {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Traspaso creado correctamente'
      })
    }

    showCreateTraspasoDialog.value = false
    resetFormTraspaso()
    await cargarTraspasos()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar traspaso',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const verDetalleTraspaso = async (traspaso: Traspaso) => {
  try {
    // TODO: Implement API call
    traspasoDetalle.value = traspaso
    showDetalleDialog.value = true
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar detalles del traspaso',
      caption: error.message
    })
  }
}

const enviarTraspaso = async (traspaso: Traspaso) => {
  $q.dialog({
    title: 'Enviar Traspaso',
    message: `¿Está seguro de enviar el traspaso ${traspaso.numero_traspaso}?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Traspaso enviado correctamente'
      })
      await cargarTraspasos()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al enviar traspaso',
        caption: error.message
      })
    }
  })
}

const marcarEnTransito = async (traspaso: Traspaso) => {
  $q.dialog({
    title: 'Marcar en Tránsito',
    message: `¿Confirma que el traspaso ${traspaso.numero_traspaso} está en tránsito?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Traspaso marcado en tránsito'
      })
      await cargarTraspasos()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al marcar en tránsito',
        caption: error.message
      })
    }
  })
}

const recibirTraspaso = async (traspaso: Traspaso) => {
  $q.dialog({
    title: 'Recibir Traspaso',
    message: `¿Confirma la recepción del traspaso ${traspaso.numero_traspaso}?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Traspaso recibido correctamente'
      })
      await cargarTraspasos()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al recibir traspaso',
        caption: error.message
      })
    }
  })
}

const cancelarTraspaso = async (traspaso: Traspaso) => {
  $q.dialog({
    title: 'Cancelar Traspaso',
    message: `¿Está seguro de cancelar el traspaso ${traspaso.numero_traspaso}?`,
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
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Traspaso cancelado correctamente'
      })
      await cargarTraspasos()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al cancelar traspaso',
        caption: error.message
      })
    }
  })
}

const resetFormTraspaso = () => {
  editandoTraspaso.value = false
  tabActivo.value = 'general'
  formTraspaso.value = {
    id_bodega_origen: 0,
    id_bodega_destino: 0,
    fecha_traspaso: new Date().toISOString().split('T')[0],
    fecha_estimada_llegada: '',
    prioridad: 'normal',
    motivo: '',
    observaciones: '',
    numero_documento_referencia: '',
    solicitante: '',
    tipo_transporte: 'interno',
    transportista: '',
    patente_vehiculo: '',
    conductor: '',
    telefono_conductor: '',
    observaciones_transporte: '',
    numero_guia_despacho: '',
    fecha_despacho: '',
    activo: true
  }
  detallesTraspaso.value = []
}

const onBodegaOrigenChange = (bodegaId: number) => {
  if (formTraspaso.value.id_bodega_destino === bodegaId) {
    formTraspaso.value.id_bodega_destino = 0
  }
}

const abrirFormularioDetalleTraspaso = () => {
  // TODO: Implement detail form
}

const editarDetalleTraspaso = (detalle: DetalleTraspaso) => {
  // TODO: Implement detail editing
}

const eliminarDetalleTraspaso = (detalle: DetalleTraspaso) => {
  // TODO: Implement detail deletion
}

const calcularTotalTraspaso = (): number => {
  return detallesTraspaso.value.reduce((total, detalle) => total + detalle.valor_total, 0)
}

// Helper methods
const getEstadoColor = (estado: string): string => {
  const colorMap: { [key: string]: string } = {
    'borrador': 'grey',
    'enviado': 'warning',
    'en_transito': 'info',
    'recibido': 'positive',
    'completado': 'positive',
    'cancelado': 'negative'
  }

  return colorMap[estado] || 'grey'
}

const getEstadoLabel = (estado: string): string => {
  const labelMap: { [key: string]: string } = {
    'borrador': 'Borrador',
    'enviado': 'Enviado',
    'en_transito': 'En Tránsito',
    'recibido': 'Recibido',
    'completado': 'Completado',
    'cancelado': 'Cancelado'
  }

  return labelMap[estado] || estado
}

const getEstadoIcon = (estado: string): string => {
  const iconMap: { [key: string]: string } = {
    'borrador': 'edit',
    'enviado': 'send',
    'en_transito': 'local_shipping',
    'recibido': 'inventory',
    'completado': 'check_circle',
    'cancelado': 'cancel'
  }

  return iconMap[estado] || 'help'
}

const getEstadoProductoColor = (estado: string): string => {
  const colorMap: { [key: string]: string } = {
    'pendiente': 'grey',
    'enviado': 'warning',
    'recibido': 'positive',
    'faltante': 'negative',
    'sobrante': 'info'
  }

  return colorMap[estado] || 'grey'
}

const getEstadoProductoLabel = (estado: string): string => {
  const labelMap: { [key: string]: string } = {
    'pendiente': 'Pendiente',
    'enviado': 'Enviado',
    'recibido': 'Recibido',
    'faltante': 'Faltante',
    'sobrante': 'Sobrante'
  }

  return labelMap[estado] || estado
}

const getProductoNombre = (productoId: number): string => {
  // TODO: Get from products store
  return `Producto ${productoId}`
}

const getProductoCodigo = (productoId: number): string => {
  // TODO: Get from products store
  return `PRD-${productoId}`
}

const getBodegaNombre = (bodegaId: number): string => {
  // TODO: Get from bodegas store
  return `Bodega ${bodegaId}`
}

const getBodegaCodigo = (bodegaId: number): string => {
  // TODO: Get from bodegas store
  return `BOD-${bodegaId}`
}

const formatDate = (dateString: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-CL')
}

const formatDateTime = (dateString?: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('es-CL')
}

// Lifecycle
onMounted(async () => {
  await cargarTraspasos()
  await cargarEstadisticas()
})
</script>