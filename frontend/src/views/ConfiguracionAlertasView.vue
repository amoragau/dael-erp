<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-xl">
        <div>
          <div class="row items-center q-mb-sm">
            <q-icon name="notifications" size="32px" color="primary" class="q-mr-md" />
            <div>
              <h4 class="q-my-none text-h4 text-weight-light">Configuración de <span class="text-weight-bold text-primary">Alertas</span></h4>
              <p class="text-grey-6 q-mb-none text-body2">Gestiona las reglas de alertas automáticas del sistema</p>
            </div>
          </div>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nueva Alerta"
          @click="abrirFormularioAlerta"
          unelevated
          class="q-px-lg q-py-sm"
          no-caps
        />
      </div>

      <!-- Stats Cards -->
      <div class="row q-gutter-md q-mb-md" v-if="estadisticas">
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-primary">{{ estadisticas.total_alertas }}</div>
              <div class="text-caption">Total Alertas</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-positive">{{ estadisticas.activas }}</div>
              <div class="text-caption">Activas</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-warning">{{ estadisticas.criticas }}</div>
              <div class="text-caption">Críticas</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-info">{{ estadisticas.disparadas_hoy }}</div>
              <div class="text-caption">Disparadas Hoy</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-3">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <div class="text-h6 text-secondary">{{ estadisticas.productos_monitoreados }}</div>
              <div class="text-caption">Productos Monitoreados</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Alert Categories -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="text-h6 q-mb-md">Categorías de Alertas</div>
          <div class="row q-gutter-md">
            <q-btn-toggle
              v-model="categoriaSeleccionada"
              toggle-color="primary"
              :options="categoriasAlerta"
              @update:model-value="filtrarPorCategoria"
            />
          </div>
        </q-card-section>
      </q-card>

      <!-- Filters -->
      <q-card flat bordered class="q-mb-md">
        <q-card-section>
          <div class="row q-gutter-md items-center">
            <q-input
              v-model="filtros.busqueda"
              placeholder="Buscar por nombre, descripción..."
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
              v-model="filtros.prioridad"
              :options="prioridadOptions"
              label="Prioridad"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 150px"
            />
            <q-select
              v-model="filtros.tipo_condicion"
              :options="tipoCondicionOptions"
              label="Tipo Condición"
              outlined
              dense
              clearable
              emit-value
              map-options
              style="min-width: 180px"
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

      <!-- Alerts Table -->
      <q-table
        :rows="alertas"
        :columns="columnsAlertas"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_alerta"
        flat
        bordered
        @request="onRequestAlertas"
      >
        <template v-slot:body-cell-nombre_alerta="props">
          <q-td :props="props">
            <div class="text-weight-medium">{{ props.value }}</div>
            <div class="text-caption text-grey-6">{{ props.row.descripcion }}</div>
          </q-td>
        </template>

        <template v-slot:body-cell-categoria="props">
          <q-td :props="props">
            <q-badge
              :color="getCategoriaColor(props.value)"
              :label="getCategoriaLabel(props.value)"
              :icon="getCategoriaIcon(props.value)"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-prioridad="props">
          <q-td :props="props">
            <q-badge
              :color="getPrioridadColor(props.value)"
              :label="getPrioridadLabel(props.value)"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-condicion="props">
          <q-td :props="props">
            <div class="text-caption">
              <strong>{{ getTipoCondicionLabel(props.row.tipo_condicion) }}</strong>
            </div>
            <div class="text-body2">{{ formatCondicion(props.row) }}</div>
          </q-td>
        </template>

        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-toggle
              :model-value="props.value"
              @update:model-value="toggleEstadoAlerta(props.row)"
              color="positive"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-ultima_ejecucion="props">
          <q-td :props="props">
            <div v-if="props.value">{{ formatDateTime(props.value) }}</div>
            <span v-else class="text-grey-5">Nunca</span>
          </q-td>
        </template>

        <template v-slot:body-cell-disparos_recientes="props">
          <q-td :props="props">
            <div class="text-center">
              <q-badge
                :color="props.value > 0 ? 'warning' : 'grey'"
                :label="props.value"
              />
            </div>
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
              @click="editarAlerta(props.row)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="visibility"
              color="info"
              size="sm"
              @click="verDetalleAlerta(props.row)"
            >
              <q-tooltip>Ver Detalles</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="play_arrow"
              color="positive"
              size="sm"
              @click="ejecutarAlerta(props.row)"
            >
              <q-tooltip>Ejecutar Ahora</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="history"
              color="secondary"
              size="sm"
              @click="verHistorialAlerta(props.row)"
            >
              <q-tooltip>Ver Historial</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="delete"
              color="negative"
              size="sm"
              @click="eliminarAlerta(props.row)"
            >
              <q-tooltip>Eliminar</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Alert Dialog -->
      <q-dialog v-model="showCreateAlertaDialog" persistent>
        <q-card style="min-width: 1000px; max-width: 1200px; max-height: 90vh">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">{{ editandoAlerta ? 'Editar' : 'Nueva' }} Alerta</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section class="q-pt-none" style="max-height: calc(90vh - 120px);">
            <q-form @submit="guardarAlerta">
              <div class="row" style="height: calc(90vh - 160px);">
                <div class="col-3">
                  <q-tabs
                    v-model="tabActivo"
                    vertical
                    class="text-primary full-height"
                  >
                    <q-tab name="general" icon="settings" label="General" />
                    <q-tab name="condiciones" icon="rule" label="Condiciones" />
                    <q-tab name="acciones" icon="notifications" label="Acciones" />
                    <q-tab name="programacion" icon="schedule" label="Programación" />
                  </q-tabs>
                </div>
                <div class="col-9">
                  <q-tab-panels
                    v-model="tabActivo"
                    animated
                    class="full-height"
                    style="overflow-y: auto;"
                  >
                    <!-- Panel General -->
                    <q-tab-panel name="general">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="settings" class="q-mr-sm" />
                        Información General
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formAlerta.nombre_alerta"
                            label="Nombre de la Alerta *"
                            outlined
                            dense
                            :rules="[val => !!val || 'El nombre es requerido']"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-select
                            v-model="formAlerta.categoria"
                            :options="categoriaAlertaOptions"
                            label="Categoría *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'La categoría es requerida']"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12">
                          <q-input
                            v-model="formAlerta.descripcion"
                            label="Descripción"
                            outlined
                            type="textarea"
                            rows="3"
                            hint="Descripción detallada de la alerta"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12 col-md-4">
                          <q-select
                            v-model="formAlerta.prioridad"
                            :options="prioridadOptions"
                            label="Prioridad *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'La prioridad es requerida']"
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-toggle
                            v-model="formAlerta.activo"
                            label="Alerta Activa"
                            left-label
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-toggle
                            v-model="formAlerta.enviar_email"
                            label="Enviar Email"
                            left-label
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formAlerta.email_destino"
                            label="Email Destino"
                            outlined
                            dense
                            type="email"
                            :disable="!formAlerta.enviar_email"
                            hint="Separar múltiples emails con comas"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model.number="formAlerta.limite_disparos_dia"
                            label="Límite Disparos por Día"
                            outlined
                            dense
                            type="number"
                            min="1"
                            hint="Máximo de alertas por día"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Condiciones -->
                    <q-tab-panel name="condiciones">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="rule" class="q-mr-sm" />
                        Condiciones de Disparo
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-select
                            v-model="formAlerta.tipo_condicion"
                            :options="tipoCondicionOptions"
                            label="Tipo de Condición *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'El tipo de condición es requerido']"
                            @update:model-value="onTipoCondicionChange"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-select
                            v-model="formAlerta.operador"
                            :options="operadorOptions"
                            label="Operador *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'El operador es requerido']"
                          />
                        </div>
                      </div>

                      <!-- Stock Mínimo -->
                      <div v-if="formAlerta.tipo_condicion === 'stock_minimo'" class="q-mt-md">
                        <q-banner class="bg-info text-white q-mb-md">
                          <q-icon name="info" class="q-mr-sm" />
                          Esta alerta se disparará cuando el stock de un producto esté por debajo del stock mínimo configurado
                        </q-banner>

                        <div class="row q-gutter-md">
                          <div class="col-12 col-md-6">
                            <q-select
                              v-model="formAlerta.id_producto"
                              :options="productosOptions"
                              label="Producto Específico"
                              outlined
                              dense
                              clearable
                              emit-value
                              map-options
                              hint="Dejar vacío para todos los productos"
                            />
                          </div>
                          <div class="col-12 col-md-5">
                            <q-select
                              v-model="formAlerta.id_bodega"
                              :options="bodegasOptions"
                              label="Bodega Específica"
                              outlined
                              dense
                              clearable
                              emit-value
                              map-options
                              hint="Dejar vacío para todas las bodegas"
                            />
                          </div>
                        </div>
                      </div>

                      <!-- Stock Máximo -->
                      <div v-if="formAlerta.tipo_condicion === 'stock_maximo'" class="q-mt-md">
                        <q-banner class="bg-warning text-dark q-mb-md">
                          <q-icon name="warning" class="q-mr-sm" />
                          Esta alerta se disparará cuando el stock de un producto supere el valor configurado
                        </q-banner>

                        <div class="row q-gutter-md">
                          <div class="col-12 col-md-4">
                            <q-input
                              v-model.number="formAlerta.valor_referencia"
                              label="Cantidad Máxima *"
                              outlined
                              dense
                              type="number"
                              min="0"
                              :rules="[val => val >= 0 || 'Debe ser mayor o igual a 0']"
                            />
                          </div>
                          <div class="col-12 col-md-4">
                            <q-select
                              v-model="formAlerta.id_producto"
                              :options="productosOptions"
                              label="Producto Específico"
                              outlined
                              dense
                              clearable
                              emit-value
                              map-options
                            />
                          </div>
                          <div class="col-12 col-md-3">
                            <q-select
                              v-model="formAlerta.id_bodega"
                              :options="bodegasOptions"
                              label="Bodega"
                              outlined
                              dense
                              clearable
                              emit-value
                              map-options
                            />
                          </div>
                        </div>
                      </div>

                      <!-- Vencimiento -->
                      <div v-if="formAlerta.tipo_condicion === 'vencimiento'" class="q-mt-md">
                        <q-banner class="bg-negative text-white q-mb-md">
                          <q-icon name="schedule" class="q-mr-sm" />
                          Esta alerta se disparará cuando productos estén próximos a vencer
                        </q-banner>

                        <div class="row q-gutter-md">
                          <div class="col-12 col-md-4">
                            <q-input
                              v-model.number="formAlerta.dias_anticipacion"
                              label="Días de Anticipación *"
                              outlined
                              dense
                              type="number"
                              min="1"
                              :rules="[val => val > 0 || 'Debe ser mayor a 0']"
                              hint="Días antes del vencimiento"
                            />
                          </div>
                          <div class="col-12 col-md-4">
                            <q-select
                              v-model="formAlerta.id_producto"
                              :options="productosOptions"
                              label="Producto Específico"
                              outlined
                              dense
                              clearable
                              emit-value
                              map-options
                            />
                          </div>
                          <div class="col-12 col-md-3">
                            <q-select
                              v-model="formAlerta.id_bodega"
                              :options="bodegasOptions"
                              label="Bodega"
                              outlined
                              dense
                              clearable
                              emit-value
                              map-options
                            />
                          </div>
                        </div>
                      </div>

                      <!-- Movimientos Sospechosos -->
                      <div v-if="formAlerta.tipo_condicion === 'movimientos_sospechosos'" class="q-mt-md">
                        <q-banner class="bg-deep-orange text-white q-mb-md">
                          <q-icon name="security" class="q-mr-sm" />
                          Esta alerta detectará patrones anómalos en los movimientos de inventario
                        </q-banner>

                        <div class="row q-gutter-md">
                          <div class="col-12 col-md-4">
                            <q-input
                              v-model.number="formAlerta.valor_referencia"
                              label="Cantidad Umbral *"
                              outlined
                              dense
                              type="number"
                              min="1"
                              :rules="[val => val > 0 || 'Debe ser mayor a 0']"
                              hint="Cantidad que considera sospechosa"
                            />
                          </div>
                          <div class="col-12 col-md-4">
                            <q-input
                              v-model.number="formAlerta.periodo_evaluacion"
                              label="Período (horas) *"
                              outlined
                              dense
                              type="number"
                              min="1"
                              :rules="[val => val > 0 || 'Debe ser mayor a 0']"
                              hint="Ventana de tiempo a evaluar"
                            />
                          </div>
                          <div class="col-12 col-md-3">
                            <q-select
                              v-model="formAlerta.id_bodega"
                              :options="bodegasOptions"
                              label="Bodega"
                              outlined
                              dense
                              clearable
                              emit-value
                              map-options
                            />
                          </div>
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Acciones -->
                    <q-tab-panel name="acciones">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="notifications" class="q-mr-sm" />
                        Acciones al Dispararse
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12">
                          <q-input
                            v-model="formAlerta.mensaje_alerta"
                            label="Mensaje de la Alerta *"
                            outlined
                            type="textarea"
                            rows="3"
                            :rules="[val => !!val || 'El mensaje es requerido']"
                            hint="Mensaje que se mostrará cuando se dispare la alerta"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12 col-md-6">
                          <q-card flat bordered>
                            <q-card-section>
                              <div class="text-subtitle1 q-mb-sm">Notificaciones</div>
                              <q-list>
                                <q-item tag="label" v-ripple>
                                  <q-item-section avatar>
                                    <q-checkbox v-model="formAlerta.mostrar_popup" />
                                  </q-item-section>
                                  <q-item-section>
                                    <q-item-label>Mostrar Popup en Sistema</q-item-label>
                                    <q-item-label caption>Ventana emergente en la interfaz</q-item-label>
                                  </q-item-section>
                                </q-item>
                                <q-item tag="label" v-ripple>
                                  <q-item-section avatar>
                                    <q-checkbox v-model="formAlerta.enviar_email" />
                                  </q-item-section>
                                  <q-item-section>
                                    <q-item-label>Enviar Email</q-item-label>
                                    <q-item-label caption>Notificación por correo electrónico</q-item-label>
                                  </q-item-section>
                                </q-item>
                                <q-item tag="label" v-ripple>
                                  <q-item-section avatar>
                                    <q-checkbox v-model="formAlerta.registrar_log" />
                                  </q-item-section>
                                  <q-item-section>
                                    <q-item-label>Registrar en Log</q-item-label>
                                    <q-item-label caption>Guardar en historial del sistema</q-item-label>
                                  </q-item-section>
                                </q-item>
                              </q-list>
                            </q-card-section>
                          </q-card>
                        </div>
                        <div class="col-12 col-md-5">
                          <q-card flat bordered>
                            <q-card-section>
                              <div class="text-subtitle1 q-mb-sm">Acciones Automáticas</div>
                              <q-list>
                                <q-item tag="label" v-ripple>
                                  <q-item-section avatar>
                                    <q-checkbox v-model="formAlerta.crear_tarea" />
                                  </q-item-section>
                                  <q-item-section>
                                    <q-item-label>Crear Tarea</q-item-label>
                                    <q-item-label caption>Generar tarea automática</q-item-label>
                                  </q-item-section>
                                </q-item>
                                <q-item tag="label" v-ripple>
                                  <q-item-section avatar>
                                    <q-checkbox v-model="formAlerta.bloquear_producto" />
                                  </q-item-section>
                                  <q-item-section>
                                    <q-item-label>Bloquear Producto</q-item-label>
                                    <q-item-label caption>Impedir movimientos del producto</q-item-label>
                                  </q-item-section>
                                </q-item>
                              </q-list>
                            </q-card-section>
                          </q-card>
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12">
                          <q-input
                            v-model="formAlerta.webhook_url"
                            label="Webhook URL"
                            outlined
                            dense
                            hint="URL para integración con sistemas externos"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Programación -->
                    <q-tab-panel name="programacion">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="schedule" class="q-mr-sm" />
                        Programación de Ejecución
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-select
                            v-model="formAlerta.frecuencia_evaluacion"
                            :options="frecuenciaOptions"
                            label="Frecuencia de Evaluación *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'La frecuencia es requerida']"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formAlerta.hora_ejecucion"
                            label="Hora de Ejecución"
                            outlined
                            dense
                            type="time"
                            hint="Para alertas diarias"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formAlerta.fecha_inicio"
                            label="Fecha de Inicio"
                            outlined
                            dense
                            type="date"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formAlerta.fecha_fin"
                            label="Fecha de Fin"
                            outlined
                            dense
                            type="date"
                            hint="Dejar vacío para indefinido"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12">
                          <q-card flat bordered class="bg-grey-1">
                            <q-card-section>
                              <div class="text-subtitle1 q-mb-sm">Días de Ejecución</div>
                              <div class="row q-gutter-sm">
                                <q-checkbox v-model="formAlerta.lunes" label="Lunes" />
                                <q-checkbox v-model="formAlerta.martes" label="Martes" />
                                <q-checkbox v-model="formAlerta.miercoles" label="Miércoles" />
                                <q-checkbox v-model="formAlerta.jueves" label="Jueves" />
                                <q-checkbox v-model="formAlerta.viernes" label="Viernes" />
                                <q-checkbox v-model="formAlerta.sabado" label="Sábado" />
                                <q-checkbox v-model="formAlerta.domingo" label="Domingo" />
                              </div>
                            </q-card-section>
                          </q-card>
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
              label="Guardar Alerta"
              @click="guardarAlerta"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Alert Detail Dialog -->
      <q-dialog v-model="showDetalleDialog" persistent>
        <q-card style="min-width: 800px; max-width: 1000px">
          <q-card-section class="row items-center">
            <div class="text-h6">Detalle de la Alerta</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section v-if="alertaDetalle">
            <div class="row q-col-gutter-md">
              <!-- Información General -->
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Información General</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Nombre</q-item-label>
                      <q-item-label>{{ alertaDetalle.nombre_alerta }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Categoría</q-item-label>
                      <q-item-label>
                        <q-badge
                          :color="getCategoriaColor(alertaDetalle.categoria)"
                          :label="getCategoriaLabel(alertaDetalle.categoria)"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Prioridad</q-item-label>
                      <q-item-label>
                        <q-badge
                          :color="getPrioridadColor(alertaDetalle.prioridad)"
                          :label="getPrioridadLabel(alertaDetalle.prioridad)"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Estado</q-item-label>
                      <q-item-label>
                        <q-badge
                          :color="alertaDetalle.activo ? 'positive' : 'negative'"
                          :label="alertaDetalle.activo ? 'Activa' : 'Inactiva'"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>

              <!-- Estadísticas -->
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Estadísticas</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Última Ejecución</q-item-label>
                      <q-item-label>{{ alertaDetalle.ultima_ejecucion ? formatDateTime(alertaDetalle.ultima_ejecucion) : 'Nunca' }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Total Disparos</q-item-label>
                      <q-item-label>{{ alertaDetalle.total_disparos || 0 }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Disparos Esta Semana</q-item-label>
                      <q-item-label>{{ alertaDetalle.disparos_semana || 0 }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Promedio Mensual</q-item-label>
                      <q-item-label>{{ alertaDetalle.promedio_mensual || 0 }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>

              <!-- Condición -->
              <div class="col-12">
                <q-expansion-item
                  icon="rule"
                  label="Condición Configurada"
                  class="q-mt-md"
                >
                  <q-card flat bordered>
                    <q-card-section>
                      <div class="text-body1">{{ formatCondicion(alertaDetalle) }}</div>
                      <div class="text-caption text-grey-6 q-mt-sm">{{ alertaDetalle.descripcion }}</div>
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

      <!-- Alert History Dialog -->
      <q-dialog v-model="showHistorialDialog" persistent>
        <q-card style="min-width: 900px; max-width: 1100px">
          <q-card-section class="row items-center">
            <div class="text-h6">Historial de Alertas</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-table
              :rows="historialAlertas"
              :columns="columnsHistorial"
              :loading="isLoadingHistorial"
              row-key="id_log"
              flat
              bordered
              dense
            >
              <template v-slot:body-cell-fecha_disparo="props">
                <q-td :props="props">
                  {{ formatDateTime(props.value) }}
                </q-td>
              </template>

              <template v-slot:body-cell-nivel="props">
                <q-td :props="props">
                  <q-badge
                    :color="getPrioridadColor(props.value)"
                    :label="getPrioridadLabel(props.value)"
                  />
                </q-td>
              </template>

              <template v-slot:body-cell-mensaje="props">
                <q-td :props="props">
                  <div class="text-body2">{{ props.value }}</div>
                </q-td>
              </template>
            </q-table>
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
interface ConfiguracionAlerta {
  id_alerta: number
  nombre_alerta: string
  descripcion?: string
  categoria: string
  tipo_condicion: string
  operador: string
  valor_referencia?: number
  dias_anticipacion?: number
  periodo_evaluacion?: number
  id_producto?: number
  id_bodega?: number
  prioridad: string
  mensaje_alerta: string
  activo: boolean
  frecuencia_evaluacion: string
  hora_ejecucion?: string
  fecha_inicio?: string
  fecha_fin?: string
  lunes: boolean
  martes: boolean
  miercoles: boolean
  jueves: boolean
  viernes: boolean
  sabado: boolean
  domingo: boolean
  enviar_email: boolean
  email_destino?: string
  mostrar_popup: boolean
  registrar_log: boolean
  crear_tarea: boolean
  bloquear_producto: boolean
  webhook_url?: string
  limite_disparos_dia?: number
  ultima_ejecucion?: string
  disparos_recientes: number
  total_disparos?: number
  disparos_semana?: number
  promedio_mensual?: number
}

interface ConfiguracionAlertaCreate {
  nombre_alerta: string
  descripcion?: string
  categoria: string
  tipo_condicion: string
  operador: string
  valor_referencia?: number
  dias_anticipacion?: number
  periodo_evaluacion?: number
  id_producto?: number
  id_bodega?: number
  prioridad: string
  mensaje_alerta: string
  activo: boolean
  frecuencia_evaluacion: string
  hora_ejecucion?: string
  fecha_inicio?: string
  fecha_fin?: string
  lunes: boolean
  martes: boolean
  miercoles: boolean
  jueves: boolean
  viernes: boolean
  sabado: boolean
  domingo: boolean
  enviar_email: boolean
  email_destino?: string
  mostrar_popup: boolean
  registrar_log: boolean
  crear_tarea: boolean
  bloquear_producto: boolean
  webhook_url?: string
  limite_disparos_dia?: number
}

// Reactive data
const alertas = ref<ConfiguracionAlerta[]>([])
const historialAlertas = ref<any[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const isLoadingHistorial = ref(false)
const showCreateAlertaDialog = ref(false)
const showDetalleDialog = ref(false)
const showHistorialDialog = ref(false)
const editandoAlerta = ref(false)
const alertaDetalle = ref<ConfiguracionAlerta | null>(null)
const estadisticas = ref<any>(null)
const tabActivo = ref('general')
const categoriaSeleccionada = ref('all')

// Filters
const filtros = ref({
  busqueda: '',
  estado: null as boolean | null,
  prioridad: null as string | null,
  tipo_condicion: null as string | null
})

// Options
const estadoOptions = [
  { label: 'Activa', value: true },
  { label: 'Inactiva', value: false }
]

const prioridadOptions = [
  { label: 'Baja', value: 'baja' },
  { label: 'Media', value: 'media' },
  { label: 'Alta', value: 'alta' },
  { label: 'Crítica', value: 'critica' }
]

const categoriaAlertaOptions = [
  { label: 'Stock', value: 'stock' },
  { label: 'Vencimientos', value: 'vencimientos' },
  { label: 'Seguridad', value: 'seguridad' },
  { label: 'Operacional', value: 'operacional' },
  { label: 'Financiera', value: 'financiera' }
]

const categoriasAlerta = [
  { label: 'Todas', value: 'all' },
  { label: 'Stock', value: 'stock' },
  { label: 'Vencimientos', value: 'vencimientos' },
  { label: 'Seguridad', value: 'seguridad' },
  { label: 'Operacional', value: 'operacional' },
  { label: 'Financiera', value: 'financiera' }
]

const tipoCondicionOptions = [
  { label: 'Stock Mínimo', value: 'stock_minimo' },
  { label: 'Stock Máximo', value: 'stock_maximo' },
  { label: 'Productos por Vencer', value: 'vencimiento' },
  { label: 'Movimientos Sospechosos', value: 'movimientos_sospechosos' },
  { label: 'Costo Elevado', value: 'costo_elevado' }
]

const operadorOptions = [
  { label: 'Menor que', value: 'menor_que' },
  { label: 'Menor o igual', value: 'menor_igual' },
  { label: 'Mayor que', value: 'mayor_que' },
  { label: 'Mayor o igual', value: 'mayor_igual' },
  { label: 'Igual a', value: 'igual' },
  { label: 'Diferente de', value: 'diferente' }
]

const frecuenciaOptions = [
  { label: 'Cada 15 minutos', value: '15_minutos' },
  { label: 'Cada 30 minutos', value: '30_minutos' },
  { label: 'Cada hora', value: 'hourly' },
  { label: 'Diario', value: 'daily' },
  { label: 'Semanal', value: 'weekly' },
  { label: 'Mensual', value: 'monthly' }
]

const productosOptions = ref([])
const bodegasOptions = ref([])

// Pagination
const paginacion = ref({
  sortBy: 'id_alerta',
  descending: true,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formAlerta = ref<ConfiguracionAlertaCreate & { id_alerta?: number }>({
  nombre_alerta: '',
  descripcion: '',
  categoria: 'stock',
  tipo_condicion: 'stock_minimo',
  operador: 'menor_que',
  valor_referencia: undefined,
  dias_anticipacion: undefined,
  periodo_evaluacion: undefined,
  id_producto: undefined,
  id_bodega: undefined,
  prioridad: 'media',
  mensaje_alerta: '',
  activo: true,
  frecuencia_evaluacion: 'daily',
  hora_ejecucion: '09:00',
  fecha_inicio: '',
  fecha_fin: '',
  lunes: true,
  martes: true,
  miercoles: true,
  jueves: true,
  viernes: true,
  sabado: false,
  domingo: false,
  enviar_email: false,
  email_destino: '',
  mostrar_popup: true,
  registrar_log: true,
  crear_tarea: false,
  bloquear_producto: false,
  webhook_url: '',
  limite_disparos_dia: 10
})

// Table columns
const columnsAlertas = [
  {
    name: 'nombre_alerta',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_alerta',
    sortable: true
  },
  {
    name: 'categoria',
    label: 'Categoría',
    align: 'center' as const,
    field: 'categoria',
    sortable: true
  },
  {
    name: 'prioridad',
    label: 'Prioridad',
    align: 'center' as const,
    field: 'prioridad',
    sortable: true
  },
  {
    name: 'condicion',
    label: 'Condición',
    align: 'left' as const,
    field: 'tipo_condicion'
  },
  {
    name: 'activo',
    label: 'Estado',
    align: 'center' as const,
    field: 'activo',
    sortable: true
  },
  {
    name: 'ultima_ejecucion',
    label: 'Última Ejecución',
    align: 'center' as const,
    field: 'ultima_ejecucion',
    sortable: true
  },
  {
    name: 'disparos_recientes',
    label: 'Disparos (7d)',
    align: 'center' as const,
    field: 'disparos_recientes',
    sortable: true
  },
  {
    name: 'actions',
    label: 'Acciones',
    align: 'center' as const,
    field: 'actions'
  }
]

const columnsHistorial = [
  {
    name: 'fecha_disparo',
    label: 'Fecha',
    align: 'left' as const,
    field: 'fecha_disparo',
    sortable: true
  },
  {
    name: 'nivel',
    label: 'Nivel',
    align: 'center' as const,
    field: 'nivel'
  },
  {
    name: 'mensaje',
    label: 'Mensaje',
    align: 'left' as const,
    field: 'mensaje'
  },
  {
    name: 'valor_detectado',
    label: 'Valor',
    align: 'center' as const,
    field: 'valor_detectado'
  }
]

// Methods
const onRequestAlertas = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarAlertas()
}

const cargarAlertas = async () => {
  try {
    isLoading.value = true
    // TODO: Implement API call
    alertas.value = []
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar alertas',
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
      total_alertas: 0,
      activas: 0,
      criticas: 0,
      disparadas_hoy: 0,
      productos_monitoreados: 0
    }
  } catch (error: any) {
    console.error('Error al cargar estadísticas:', error)
  }
}

const aplicarFiltros = async () => {
  paginacion.value.page = 1
  await cargarAlertas()
}

const filtrarPorCategoria = async (categoria: string) => {
  if (categoria === 'all') {
    filtros.value.tipo_condicion = null
  } else {
    // Filter by category logic
  }
  await aplicarFiltros()
}

const abrirFormularioAlerta = () => {
  resetFormAlerta()
  showCreateAlertaDialog.value = true
}

const editarAlerta = (alerta: ConfiguracionAlerta) => {
  editandoAlerta.value = true
  formAlerta.value = { ...alerta }
  showCreateAlertaDialog.value = true
}

const guardarAlerta = async () => {
  try {
    isGuardando.value = true

    if (editandoAlerta.value && formAlerta.value.id_alerta) {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Alerta actualizada correctamente'
      })
    } else {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Alerta creada correctamente'
      })
    }

    showCreateAlertaDialog.value = false
    resetFormAlerta()
    await cargarAlertas()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar alerta',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const verDetalleAlerta = async (alerta: ConfiguracionAlerta) => {
  try {
    // TODO: Implement API call
    alertaDetalle.value = alerta
    showDetalleDialog.value = true
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar detalles de la alerta',
      caption: error.message
    })
  }
}

const verHistorialAlerta = async (alerta: ConfiguracionAlerta) => {
  try {
    isLoadingHistorial.value = true
    // TODO: Implement API call
    historialAlertas.value = []
    showHistorialDialog.value = true
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar historial',
      caption: error.message
    })
  } finally {
    isLoadingHistorial.value = false
  }
}

const ejecutarAlerta = async (alerta: ConfiguracionAlerta) => {
  $q.dialog({
    title: 'Ejecutar Alerta',
    message: `¿Está seguro de ejecutar manualmente la alerta "${alerta.nombre_alerta}"?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Alerta ejecutada correctamente'
      })
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al ejecutar alerta',
        caption: error.message
      })
    }
  })
}

const toggleEstadoAlerta = async (alerta: ConfiguracionAlerta) => {
  try {
    // TODO: Implement API call
    $q.notify({
      type: 'positive',
      message: `Alerta ${alerta.activo ? 'desactivada' : 'activada'} correctamente`
    })
    await cargarAlertas()
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de alerta',
      caption: error.message
    })
  }
}

const eliminarAlerta = async (alerta: ConfiguracionAlerta) => {
  $q.dialog({
    title: 'Eliminar Alerta',
    message: `¿Está seguro de eliminar la alerta "${alerta.nombre_alerta}"?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      // TODO: Implement API call
      $q.notify({
        type: 'positive',
        message: 'Alerta eliminada correctamente'
      })
      await cargarAlertas()
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar alerta',
        caption: error.message
      })
    }
  })
}

const resetFormAlerta = () => {
  editandoAlerta.value = false
  tabActivo.value = 'general'
  formAlerta.value = {
    nombre_alerta: '',
    descripcion: '',
    categoria: 'stock',
    tipo_condicion: 'stock_minimo',
    operador: 'menor_que',
    valor_referencia: undefined,
    dias_anticipacion: undefined,
    periodo_evaluacion: undefined,
    id_producto: undefined,
    id_bodega: undefined,
    prioridad: 'media',
    mensaje_alerta: '',
    activo: true,
    frecuencia_evaluacion: 'daily',
    hora_ejecucion: '09:00',
    fecha_inicio: '',
    fecha_fin: '',
    lunes: true,
    martes: true,
    miercoles: true,
    jueves: true,
    viernes: true,
    sabado: false,
    domingo: false,
    enviar_email: false,
    email_destino: '',
    mostrar_popup: true,
    registrar_log: true,
    crear_tarea: false,
    bloquear_producto: false,
    webhook_url: '',
    limite_disparos_dia: 10
  }
}

const onTipoCondicionChange = (tipo: string) => {
  // Reset specific fields when condition type changes
  formAlerta.value.valor_referencia = undefined
  formAlerta.value.dias_anticipacion = undefined
  formAlerta.value.periodo_evaluacion = undefined
}

// Helper methods
const getCategoriaColor = (categoria: string): string => {
  const colorMap: { [key: string]: string } = {
    'stock': 'primary',
    'vencimientos': 'warning',
    'seguridad': 'negative',
    'operacional': 'info',
    'financiera': 'secondary'
  }

  return colorMap[categoria] || 'grey'
}

const getCategoriaLabel = (categoria: string): string => {
  const labelMap: { [key: string]: string } = {
    'stock': 'Stock',
    'vencimientos': 'Vencimientos',
    'seguridad': 'Seguridad',
    'operacional': 'Operacional',
    'financiera': 'Financiera'
  }

  return labelMap[categoria] || categoria
}

const getCategoriaIcon = (categoria: string): string => {
  const iconMap: { [key: string]: string } = {
    'stock': 'inventory',
    'vencimientos': 'schedule',
    'seguridad': 'security',
    'operacional': 'settings',
    'financiera': 'attach_money'
  }

  return iconMap[categoria] || 'help'
}

const getPrioridadColor = (prioridad: string): string => {
  const colorMap: { [key: string]: string } = {
    'baja': 'positive',
    'media': 'info',
    'alta': 'warning',
    'critica': 'negative'
  }

  return colorMap[prioridad] || 'grey'
}

const getPrioridadLabel = (prioridad: string): string => {
  const labelMap: { [key: string]: string } = {
    'baja': 'Baja',
    'media': 'Media',
    'alta': 'Alta',
    'critica': 'Crítica'
  }

  return labelMap[prioridad] || prioridad
}

const getTipoCondicionLabel = (tipo: string): string => {
  const labelMap: { [key: string]: string } = {
    'stock_minimo': 'Stock Mínimo',
    'stock_maximo': 'Stock Máximo',
    'vencimiento': 'Vencimiento',
    'movimientos_sospechosos': 'Movimientos Sospechosos',
    'costo_elevado': 'Costo Elevado'
  }

  return labelMap[tipo] || tipo
}

const formatCondicion = (alerta: ConfiguracionAlerta): string => {
  switch (alerta.tipo_condicion) {
    case 'stock_minimo':
      return 'Stock por debajo del mínimo configurado'
    case 'stock_maximo':
      return `Stock mayor a ${alerta.valor_referencia} unidades`
    case 'vencimiento':
      return `Productos que vencen en ${alerta.dias_anticipacion} días`
    case 'movimientos_sospechosos':
      return `Movimientos > ${alerta.valor_referencia} en ${alerta.periodo_evaluacion}h`
    default:
      return 'Condición personalizada'
  }
}

const formatDateTime = (dateString: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('es-CL')
}

// Lifecycle
onMounted(async () => {
  await cargarAlertas()
  await cargarEstadisticas()
})
</script>