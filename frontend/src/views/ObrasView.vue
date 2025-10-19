<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-xl">
        <div>
          <div class="row items-center q-mb-sm">
            <q-icon name="engineering" size="32px" color="primary" class="q-mr-md" />
            <div>
              <h4 class="q-my-none text-h4 text-weight-light">Gestión de <span class="text-weight-bold text-primary">Obras</span></h4>
              <p class="text-grey-6 q-mb-none text-body2">Gestión integral de obras con control financiero y almacenes de proyecto</p>
            </div>
          </div>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nueva Obra"
          @click="abrirFormularioObra"
          unelevated
          class="q-px-lg q-py-sm"
          no-caps
        />
      </div>

      <!-- Filters -->
      <q-card flat class="q-mb-lg shadow-light">
        <q-card-section class="q-pa-lg">
          <div class="text-h6 text-weight-medium q-mb-md text-grey-8">
            <q-icon name="filter_list" class="q-mr-sm" />
            Filtros de búsqueda
          </div>
          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-3">
              <q-input
                v-model="filtros.busqueda"
                placeholder="Buscar por código, nombre..."
                outlined
                dense
                clearable
              >
                <template v-slot:prepend>
                  <q-icon name="search" color="grey-5" />
                </template>
              </q-input>
            </div>
            <div class="col-12 col-md-2">
              <q-select
                v-model="filtros.estado"
                :options="estadoObrasOptions"
                label="Estado"
                outlined
                dense
                clearable
                emit-value
                map-options
              />
            </div>
            <div class="col-12 col-md-3">
              <q-select
                v-model="filtros.cliente_id"
                :options="clienteOptions"
                label="Cliente"
                outlined
                dense
                clearable
                emit-value
                map-options
              />
            </div>
            <div class="col-12 col-md-2">
              <q-select
                v-model="filtros.activo"
                :options="activoOptions"
                label="Estado General"
                outlined
                dense
                clearable
                emit-value
                map-options
              />
            </div>
            <div class="col-12 col-md-2 row q-gutter-sm justify-end items-center">
              <q-btn color="primary" icon="search" label="Buscar" @click="buscarObras" unelevated no-caps />
              <q-btn color="grey-6" icon="clear" label="Limpiar" @click="limpiarFiltros" flat no-caps />
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Works Table -->
      <q-table
        :rows="obras"
        :columns="columnsObras"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_obra"
        flat
        bordered
        @request="onRequestObras"
      >
        <template v-slot:body-cell-estado="props">
          <q-td :props="props">
            <q-badge
              :color="getEstadoColor(props.value)"
              :label="formatEstado(props.value)"
              text-color="white"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'green' : 'red'"
              :label="props.value ? 'Activa' : 'Inactiva'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-valor_contrato="props">
          <q-td :props="props">
            <span class="text-weight-medium">
              {{ formatCurrency(props.value) }}
            </span>
          </q-td>
        </template>

        <template v-slot:body-cell-almacen="props">
          <q-td :props="props">
            <q-badge
              v-if="props.row.almacen_obra"
              color="green"
              icon="warehouse"
              label="Configurado"
            />
            <q-badge
              v-else
              color="orange"
              icon="warning"
              label="Sin almacén"
            />
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
              @click="verDetalleObra(props.row as Obra)"
            >
              <q-tooltip>Ver Detalles</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="edit"
              color="primary"
              size="sm"
              @click="editarObra(props.row as Obra)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="warehouse"
              color="info"
              size="sm"
              @click="gestionarAlmacen(props.row as Obra)"
              :disable="!props.row.activo"
            >
              <q-tooltip>Gestionar Almacén</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'negative' : 'positive'"
              size="sm"
              @click="toggleEstadoObra(props.row as Obra)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Obra Dialog -->
      <q-dialog v-model="showCreateObraDialog" persistent>
        <q-card style="min-width: 1200px; max-width: 1400px; max-height: 90vh">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">{{ editandoObra ? 'Editar' : 'Nueva' }} Obra</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section class="q-pt-none" style="max-height: calc(90vh - 120px);">
            <q-form @submit="guardarObra">
              <div class="row" style="height: calc(90vh - 160px);">
                <div class="col-3">
                  <q-tabs
                    v-model="tabActivo"
                    vertical
                    class="text-primary full-height"
                  >
                    <q-tab name="basica" icon="business" label="Información Básica" />
                    <q-tab name="ubicacion" icon="location_on" label="Ubicación y Personal" />
                    <q-tab name="fechas" icon="calendar_today" label="Fechas" />
                    <q-tab name="financiero" icon="attach_money" label="Financiero" />
                    <q-tab name="inventario" icon="inventory" label="Inventario" />
                  </q-tabs>
                </div>
                <div class="col-9">
                  <q-tab-panels
                    v-model="tabActivo"
                    animated
                    class="full-height"
                    style="overflow-y: auto;"
                  >
                    <!-- Panel Información Básica -->
                    <q-tab-panel name="basica">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="business" class="q-mr-sm" />
                        Información Básica
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formObra.codigo_obra"
                            label="Código *"
                            outlined
                            dense
                            maxlength="20"
                            :rules="[val => !!val || 'El código es requerido']"
                            hint="Código único de la obra"
                          />
                        </div>
                        <div class="col-12 col-md-7">
                          <q-select
                            v-model="formObra.id_cliente"
                            :options="clienteOptions"
                            label="Cliente *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'El cliente es requerido']"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formObra.nombre_obra"
                            label="Nombre de la Obra *"
                            outlined
                            dense
                            maxlength="200"
                            :rules="[val => !!val || 'El nombre es requerido']"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formObra.descripcion"
                            label="Descripción"
                            outlined
                            dense
                            type="textarea"
                            rows="3"
                            hint="Descripción detallada del proyecto"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-6">
                          <q-select
                            v-model="formObra.estado"
                            :options="estadoObrasOptions"
                            label="Estado *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'El estado es requerido']"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-toggle
                            v-model="formObra.activo"
                            label="Obra Activa"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Ubicación y Personal -->
                    <q-tab-panel name="ubicacion">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="location_on" class="q-mr-sm" />
                        Ubicación y Personal
                      </div>

                      <!-- Ubicación Física -->
                      <div class="text-subtitle1 q-mb-sm">Ubicación Física</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12">
                          <q-input
                            v-model="formObra.direccion"
                            label="Dirección"
                            outlined
                            dense
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formObra.ciudad"
                            label="Ciudad"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formObra.codigo_postal"
                            label="Código Postal"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model="formObra.pais"
                            label="País"
                            outlined
                            dense
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formObra.coordenadas_gps"
                            label="Coordenadas GPS"
                            outlined
                            dense
                            hint="Formato: latitud, longitud (ej: -33.4489, -70.6693)"
                          />
                        </div>
                      </div>

                      <!-- Personal de Obra -->
                      <div class="text-subtitle1 q-mb-sm q-mt-lg">Personal de Obra</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formObra.supervisor_obra"
                            label="Supervisor de Obra"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formObra.telefono_supervisor"
                            label="Teléfono Supervisor"
                            outlined
                            dense
                            mask="(###) ###-####"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formObra.email_supervisor"
                            label="Email Supervisor"
                            type="email"
                            outlined
                            dense
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formObra.contacto_obra"
                            label="Contacto en Obra"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formObra.telefono_contacto"
                            label="Teléfono Contacto"
                            outlined
                            dense
                            mask="(###) ###-####"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formObra.email_contacto"
                            label="Email Contacto"
                            type="email"
                            outlined
                            dense
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Fechas -->
                    <q-tab-panel name="fechas">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="calendar_today" class="q-mr-sm" />
                        Fechas del Proyecto
                      </div>

                      <!-- Fechas Programadas -->
                      <div class="text-subtitle1 q-mb-sm">Fechas Programadas</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formObra.fecha_inicio_programada"
                            label="Fecha Inicio Programada"
                            outlined
                            dense
                            type="date"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formObra.fecha_fin_programada"
                            label="Fecha Fin Programada"
                            outlined
                            dense
                            type="date"
                          />
                        </div>
                      </div>

                      <!-- Fechas Reales -->
                      <div class="text-subtitle1 q-mb-sm q-mt-lg">Fechas Reales</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formObra.fecha_inicio_real"
                            label="Fecha Inicio Real"
                            outlined
                            dense
                            type="date"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formObra.fecha_fin_real"
                            label="Fecha Fin Real"
                            outlined
                            dense
                            type="date"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Financiero -->
                    <q-tab-panel name="financiero">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="attach_money" class="q-mr-sm" />
                        Control Financiero
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model.number="formObra.valor_contrato"
                            label="Valor del Contrato"
                            outlined
                            dense
                            type="number"
                            step="0.01"
                            min="0"
                            prefix="$"
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-select
                            v-model="formObra.moneda"
                            :options="monedaOptions"
                            label="Moneda"
                            outlined
                            dense
                            emit-value
                            map-options
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model.number="formObra.porcentaje_merma_permitida"
                            label="% Merma Permitida"
                            outlined
                            dense
                            type="number"
                            step="0.01"
                            min="0"
                            max="100"
                            suffix="%"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Inventario -->
                    <q-tab-panel name="inventario">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="inventory" class="q-mr-sm" />
                        Políticas de Inventario
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-toggle
                            v-model="formObra.requiere_devolucion_sobrantes"
                            label="Requiere Devolución de Sobrantes"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model.number="formObra.dias_limite_devolucion"
                            label="Días Límite para Devolución"
                            outlined
                            dense
                            type="number"
                            min="1"
                            max="365"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formObra.observaciones"
                            label="Observaciones Generales"
                            outlined
                            type="textarea"
                            rows="4"
                          />
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
              label="Guardar Obra"
              @click="guardarObra"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Work Detail Dialog -->
      <q-dialog v-model="showDetalleDialog" persistent>
        <q-card style="min-width: 800px; max-width: 1000px">
          <q-card-section class="row items-center">
            <div class="text-h6">Detalles de la Obra</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section v-if="obraDetalle">
            <div class="row q-col-gutter-md">
              <!-- Información Básica -->
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Información del Proyecto</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Código</q-item-label>
                      <q-item-label>{{ obraDetalle.codigo_obra }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Nombre</q-item-label>
                      <q-item-label>{{ obraDetalle.nombre_obra }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Cliente</q-item-label>
                      <q-item-label>{{ obraDetalle.cliente?.nombre_cliente || '-' }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Estado</q-item-label>
                      <q-item-label>
                        <q-badge
                          :color="getEstadoColor(obraDetalle?.estado ?? 'planificacion')"
                          :label="formatEstado(obraDetalle?.estado ?? 'planificacion')"
                          text-color="white"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>

              <!-- Información Financiera -->
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Control Financiero</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Valor Contrato</q-item-label>
                      <q-item-label>
                        {{ formatCurrency(obraDetalle.valor_contrato) }}
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Moneda</q-item-label>
                      <q-item-label>{{ obraDetalle.moneda || 'CLP' }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>% Merma Permitida</q-item-label>
                      <q-item-label>{{ obraDetalle.porcentaje_merma_permitida || 0 }}%</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Almacén</q-item-label>
                      <q-item-label>
                        <q-badge
                          v-if="obraDetalle.almacen_obra"
                          color="green"
                          label="Configurado"
                        />
                        <q-badge
                          v-else
                          color="orange"
                          label="Sin almacén"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>

              <!-- Fechas y Ubicación -->
              <div class="col-12">
                <q-expansion-item
                  icon="calendar_today"
                  label="Fechas y Ubicación"
                  class="q-mt-md"
                >
                  <q-card flat bordered>
                    <q-card-section>
                      <div class="row q-col-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-list dense>
                            <q-item v-if="obraDetalle.fecha_inicio_programada">
                              <q-item-section>
                                <q-item-label caption>Inicio Programado</q-item-label>
                                <q-item-label>{{ formatDate(obraDetalle.fecha_inicio_programada) }}</q-item-label>
                              </q-item-section>
                            </q-item>
                            <q-item v-if="obraDetalle.fecha_fin_programada">
                              <q-item-section>
                                <q-item-label caption>Fin Programado</q-item-label>
                                <q-item-label>{{ formatDate(obraDetalle.fecha_fin_programada) }}</q-item-label>
                              </q-item-section>
                            </q-item>
                            <q-item v-if="obraDetalle.direccion">
                              <q-item-section>
                                <q-item-label caption>Dirección</q-item-label>
                                <q-item-label>{{ obraDetalle.direccion }}</q-item-label>
                              </q-item-section>
                            </q-item>
                          </q-list>
                        </div>
                        <div class="col-12 col-md-6">
                          <q-list dense>
                            <q-item v-if="obraDetalle.supervisor_obra">
                              <q-item-section>
                                <q-item-label caption>Supervisor</q-item-label>
                                <q-item-label>{{ obraDetalle.supervisor_obra }}</q-item-label>
                              </q-item-section>
                            </q-item>
                            <q-item v-if="obraDetalle.telefono_supervisor">
                              <q-item-section>
                                <q-item-label caption>Teléfono Supervisor</q-item-label>
                                <q-item-label>{{ obraDetalle.telefono_supervisor }}</q-item-label>
                              </q-item-section>
                            </q-item>
                            <q-item v-if="obraDetalle.ciudad">
                              <q-item-section>
                                <q-item-label caption>Ciudad</q-item-label>
                                <q-item-label>{{ obraDetalle.ciudad }}</q-item-label>
                              </q-item-section>
                            </q-item>
                          </q-list>
                        </div>
                      </div>
                    </q-card-section>
                  </q-card>
                </q-expansion-item>
              </div>
            </div>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cerrar" v-close-popup />
            <q-btn
              color="primary"
              label="Editar"
              @click="editarDesdeDetalle"
              v-if="obraDetalle"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Warehouse Management Dialog -->
      <q-dialog v-model="showWarehouseModal" persistent>
        <q-card style="min-width: 700px; max-width: 90vw">
          <q-card-section class="row items-center">
            <div class="text-h6">Gestión de Almacén de Obra</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarAlmacen" class="q-gutter-md">
              <q-input
                v-model="almacenForm.ubicacion_almacen"
                label="Ubicación del Almacén *"
                outlined
                :rules="[val => !!val || 'Campo requerido']"
              />

              <q-input
                v-model="almacenForm.direccion_almacen"
                label="Dirección del Almacén"
                outlined
              />

              <h6>Responsable del Almacén</h6>
              <div class="row q-gutter-md">
                <div class="col">
                  <q-input
                    v-model="almacenForm.responsable_almacen"
                    label="Responsable"
                    outlined
                  />
                </div>
                <div class="col">
                  <q-input
                    v-model="almacenForm.telefono_responsable"
                    label="Teléfono"
                    outlined
                    placeholder="+56 9 1234 5678"
                  />
                </div>
              </div>

              <q-input
                v-model="almacenForm.email_responsable"
                label="Email Responsable"
                outlined
                type="email"
              />

              <h6>Condiciones del Almacén</h6>
              <div class="row q-gutter-md">
                <div class="col">
                  <q-toggle
                    v-model="almacenForm.tiene_techo"
                    label="Tiene Techo"
                  />
                </div>
                <div class="col">
                  <q-toggle
                    v-model="almacenForm.tiene_seguridad"
                    label="Tiene Seguridad"
                  />
                </div>
                <div class="col">
                  <q-input
                    v-model.number="almacenForm.capacidad_m3"
                    label="Capacidad (m³)"
                    outlined
                    type="number"
                    min="0"
                  />
                </div>
              </div>

              <q-input
                v-model="almacenForm.condiciones_especiales"
                label="Condiciones Especiales"
                outlined
                type="textarea"
                rows="3"
              />

              <q-input
                v-model="almacenForm.observaciones"
                label="Observaciones"
                outlined
                type="textarea"
                rows="3"
              />

              <q-card-actions align="right">
                <q-btn flat label="Cancelar" v-close-popup @click="cancelarAlmacen" />
                <q-btn
                  color="primary"
                  label="Guardar"
                  type="submit"
                  :loading="saving"
                />
              </q-card-actions>
            </q-form>
          </q-card-section>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import {
  useObraStore,
  type Obra,
  type ObraCreate,
  type ObraUpdate,
  type AlmacenObra,
  type AlmacenObraCreate,
  type AlmacenObraUpdate
} from '@/stores/obras'
import { useClienteStore, type Cliente } from '@/stores/clientes'

// Composables
const $q = useQuasar()
const obraStore = useObraStore()
const clienteStore = useClienteStore()

// Reactive data
const obras = computed(() => obraStore.obras)
const isLoading = computed(() => obraStore.isLoading)
const clientesDisponibles = computed(() => clienteStore.clientes.filter(c => c.activo))
const isGuardando = ref(false)
const showCreateObraDialog = ref(false)
const showWarehouseModal = ref(false)
const showDetalleDialog = ref(false)
const editandoObra = ref(false)
const editingAlmacen = ref<AlmacenObra | null>(null)
const currentObraForWarehouse = ref<Obra | null>(null)
const obraDetalle = ref<Obra | null>(null)
const saving = ref(false)
const tabActivo = ref('basica')

// Filters
const filtros = ref({
  busqueda: '',
  estado: null as string | null,
  cliente_id: null as number | null,
  activo: null as boolean | null
})

const estadoObrasOptions = [
  { label: 'Planificación', value: 'planificacion' },
  { label: 'Ejecución', value: 'ejecucion' },
  { label: 'Suspendida', value: 'suspendida' },
  { label: 'Finalizada', value: 'finalizada' },
  { label: 'Cancelada', value: 'cancelada' }
]

const activoOptions = [
  { label: 'Activas', value: true },
  { label: 'Inactivas', value: false }
]

const monedaOptions = [
  { label: 'CLP - Peso Chileno', value: 'CLP' },
  { label: 'USD - Dólar Americano', value: 'USD' },
  { label: 'EUR - Euro', value: 'EUR' }
]

// Pagination
const paginacion = ref({
  sortBy: 'id_obra',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formObra = ref<ObraCreate & { id_obra?: number }>({
  codigo_obra: '',
  nombre_obra: '',
  descripcion: '',
  id_cliente: 0,
  direccion: '',
  ciudad: '',
  codigo_postal: '',
  pais: 'Chile',
  coordenadas_gps: '',
  supervisor_obra: '',
  telefono_supervisor: '',
  email_supervisor: '',
  contacto_obra: '',
  telefono_contacto: '',
  email_contacto: '',
  fecha_inicio_programada: '',
  fecha_fin_programada: '',
  fecha_inicio_real: '',
  fecha_fin_real: '',
  estado: 'planificacion',
  valor_contrato: 0,
  moneda: 'CLP',
  porcentaje_merma_permitida: 0,
  requiere_devolucion_sobrantes: true,
  dias_limite_devolucion: 30,
  observaciones: '',
  activo: true
})

const almacenForm = ref<AlmacenObraCreate>({
  id_obra: 0,
  ubicacion_almacen: '',
  direccion_almacen: '',
  responsable_almacen: '',
  telefono_responsable: '',
  email_responsable: '',
  tiene_techo: false,
  tiene_seguridad: false,
  capacidad_m3: 0,
  condiciones_especiales: '',
  observaciones: '',
  activo: true
})

// Table columns
const columnsObras = [
  {
    name: 'codigo_obra',
    required: true,
    label: 'Código',
    align: 'left' as const,
    field: 'codigo_obra',
    sortable: true
  },
  {
    name: 'nombre_obra',
    required: true,
    label: 'Obra',
    align: 'left' as const,
    field: 'nombre_obra',
    sortable: true
  },
  {
    name: 'estado',
    label: 'Estado',
    align: 'center' as const,
    field: 'estado',
    sortable: true
  },
  {
    name: 'valor_contrato',
    label: 'Valor',
    align: 'right' as const,
    field: 'valor_contrato',
    sortable: true
  },
  {
    name: 'almacen',
    label: 'Almacén',
    align: 'center' as const,
    field: 'almacen'
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

// Options
const clienteOptions = computed(() =>
  clientesDisponibles.value.map(cliente => ({
    label: cliente.nombre_cliente,
    value: cliente.id_cliente
  }))
)

// Methods
const onRequestObras = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarObras()
}

const cargarObras = async () => {
  try {
    const params: any = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    if (filtros.value.activo !== null) {
      params.activo = filtros.value.activo
    }

    await obraStore.obtenerObras(params)

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar obras',
      caption: error.message
    })
  }
}

const cargarClientes = async () => {
  try {
    await clienteStore.obtenerClientes({ activo: true })
  } catch (error) {
    console.error('Error al cargar clientes:', error)
  }
}

const buscarObras = async () => {
  paginacion.value.page = 1
  await cargarObras()
}

const limpiarFiltros = () => {
  filtros.value.busqueda = ''
  filtros.value.estado = null
  filtros.value.cliente_id = null
  filtros.value.activo = null
  buscarObras()
}

const abrirFormularioObra = () => {
  resetFormObra()
  showCreateObraDialog.value = true
}

const editarObra = (obra: Obra) => {
  editandoObra.value = true
  formObra.value = { ...obra }
  showCreateObraDialog.value = true
}

const verDetalleObra = async (obra: Obra) => {
  try {
    obraDetalle.value = await obraStore.obtenerObra(obra.id_obra)
    showDetalleDialog.value = true
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar detalles de la obra',
      caption: error.message
    })
  }
}

const editarDesdeDetalle = () => {
  if (obraDetalle.value) {
    showDetalleDialog.value = false
    editarObra(obraDetalle.value)
  }
}

const gestionarAlmacen = async (obra: Obra) => {
  currentObraForWarehouse.value = obra

  try {
    const almacenExistente = await obraStore.obtenerAlmacenObra(obra.id_obra)

    if (almacenExistente) {
      editingAlmacen.value = almacenExistente
      Object.assign(almacenForm.value, {
        ...almacenExistente,
        direccion_almacen: almacenExistente.direccion_almacen || '',
        responsable_almacen: almacenExistente.responsable_almacen || '',
        telefono_responsable: almacenExistente.telefono_responsable || '',
        email_responsable: almacenExistente.email_responsable || '',
        capacidad_m3: almacenExistente.capacidad_m3 || 0,
        condiciones_especiales: almacenExistente.condiciones_especiales || '',
        observaciones: almacenExistente.observaciones || ''
      })
    } else {
      editingAlmacen.value = null
      almacenForm.value.id_obra = obra.id_obra
    }

    showWarehouseModal.value = true
  } catch (error) {
    console.error('Error al cargar almacén:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al cargar información del almacén'
    })
  }
}

const guardarObra = async () => {
  try {
    isGuardando.value = true

    if (editandoObra.value && formObra.value.id_obra) {
      await obraStore.actualizarObra(formObra.value.id_obra, formObra.value)
      $q.notify({
        type: 'positive',
        message: 'Obra actualizada correctamente'
      })
    } else {
      await obraStore.crearObra(formObra.value)
      $q.notify({
        type: 'positive',
        message: 'Obra creada correctamente'
      })
    }

    showCreateObraDialog.value = false
    resetFormObra()
    await cargarObras()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar obra',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const guardarAlmacen = async () => {
  try {
    saving.value = true

    if (editingAlmacen.value) {
      const updateData: AlmacenObraUpdate = { ...almacenForm.value }
      await obraStore.actualizarAlmacenObra(editingAlmacen.value.id_almacen_obra, updateData)
      $q.notify({
        type: 'positive',
        message: 'Almacén actualizado correctamente'
      })
    } else {
      await obraStore.crearAlmacenObra(almacenForm.value)
      $q.notify({
        type: 'positive',
        message: 'Almacén creado correctamente'
      })
    }

    showWarehouseModal.value = false
    await cargarObras()
  } catch (error: any) {
    console.error('Error al guardar almacén:', error)
    $q.notify({
      type: 'negative',
      message: error.message || 'Error al guardar el almacén'
    })
  } finally {
    saving.value = false
  }
}

const cancelarAlmacen = () => {
  editingAlmacen.value = null
  currentObraForWarehouse.value = null

  Object.assign(almacenForm.value, {
    id_obra: 0,
    ubicacion_almacen: '',
    direccion_almacen: '',
    responsable_almacen: '',
    telefono_responsable: '',
    email_responsable: '',
    tiene_techo: false,
    tiene_seguridad: false,
    capacidad_m3: 0,
    condiciones_especiales: '',
    observaciones: '',
    activo: true
  })
}

const toggleEstadoObra = async (obra: Obra) => {
  try {
    if (obra.activo) {
      await obraStore.eliminarObra(obra.id_obra, false)
      $q.notify({
        type: 'positive',
        message: 'Obra desactivada'
      })
    } else {
      await obraStore.activarObra(obra.id_obra)
      $q.notify({
        type: 'positive',
        message: 'Obra activada'
      })
    }

    await cargarObras()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de obra',
      caption: error.message
    })
  }
}

const resetFormObra = () => {
  editandoObra.value = false
  tabActivo.value = 'basica'
  formObra.value = {
    codigo_obra: '',
    nombre_obra: '',
    descripcion: '',
    id_cliente: 0,
    direccion: '',
    ciudad: '',
    codigo_postal: '',
    pais: 'Chile',
    coordenadas_gps: '',
    supervisor_obra: '',
    telefono_supervisor: '',
    email_supervisor: '',
    contacto_obra: '',
    telefono_contacto: '',
    email_contacto: '',
    fecha_inicio_programada: '',
    fecha_fin_programada: '',
    fecha_inicio_real: '',
    fecha_fin_real: '',
    estado: 'planificacion',
    valor_contrato: 0,
    moneda: 'CLP',
    porcentaje_merma_permitida: 0,
    requiere_devolucion_sobrantes: true,
    dias_limite_devolucion: 30,
    observaciones: '',
    activo: true
  }
}

// Utility functions
const formatEstado = (estado: string) => {
  const estados: Record<string, string> = {
    planificacion: 'Planificación',
    ejecucion: 'Ejecución',
    suspendida: 'Suspendida',
    finalizada: 'Finalizada',
    cancelada: 'Cancelada'
  }
  return estados[estado] || estado
}

const getEstadoColor = (estado: string) => {
  const colores: Record<string, string> = {
    planificacion: 'info',
    ejecucion: 'primary',
    suspendida: 'warning',
    finalizada: 'positive',
    cancelada: 'negative'
  }
  return colores[estado] || 'info'
}

const formatDate = (dateString: string) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('es-CL')
}

const formatCurrency = (amount: number | undefined) => {
  if (!amount) return 'No especificado'
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP'
  }).format(amount)
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    cargarObras(),
    cargarClientes()
  ])
})
</script>