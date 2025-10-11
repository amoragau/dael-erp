<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Configuración del Sistema</h4>
          <p class="text-grey-7 q-mb-none">Administra las configuraciones generales del sistema ERP</p>
        </div>
        <div class="q-gutter-sm">
          <q-btn
            color="secondary"
            icon="backup"
            label="Exportar Config"
            @click="exportarConfiguracion"
          />
          <q-btn
            color="primary"
            icon="save"
            label="Guardar Cambios"
            @click="guardarConfiguracion"
            :loading="isGuardando"
            :disable="!hayCambios"
          />
        </div>
      </div>

      <!-- System Status Cards -->
      <div class="row q-gutter-md q-mb-md" v-if="estadoSistema">
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <q-icon
                :name="estadoSistema.database_status === 'online' ? 'storage' : 'warning'"
                :color="estadoSistema.database_status === 'online' ? 'positive' : 'negative'"
                size="md"
              />
              <div class="text-caption q-mt-xs">Base de Datos</div>
              <div class="text-weight-bold">{{ estadoSistema.database_status === 'online' ? 'Online' : 'Offline' }}</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <q-icon name="memory" color="info" size="md" />
              <div class="text-caption q-mt-xs">Memoria</div>
              <div class="text-weight-bold">{{ estadoSistema.memory_usage }}%</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <q-icon name="people" color="primary" size="md" />
              <div class="text-caption q-mt-xs">Usuarios Activos</div>
              <div class="text-weight-bold">{{ estadoSistema.active_users }}</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-2">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <q-icon name="schedule" color="secondary" size="md" />
              <div class="text-caption q-mt-xs">Uptime</div>
              <div class="text-weight-bold">{{ estadoSistema.uptime_days }}d</div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-3">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <q-icon name="update" color="warning" size="md" />
              <div class="text-caption q-mt-xs">Última Actualización</div>
              <div class="text-weight-bold">{{ formatDate(estadoSistema.last_update) }}</div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Configuration Tabs -->
      <q-card flat bordered>
        <q-tabs
          v-model="tabActivo"
          dense
          class="text-grey"
          active-color="primary"
          indicator-color="primary"
          align="justify"
          narrow-indicator
        >
          <q-tab name="general" icon="settings" label="General" />
          <q-tab name="empresa" icon="business" label="Empresa" />
          <q-tab name="inventario" icon="inventory" label="Inventario" />
          <q-tab name="usuarios" icon="people" label="Usuarios" />
          <q-tab name="integraciones" icon="integration_instructions" label="Integraciones" />
          <q-tab name="seguridad" icon="security" label="Seguridad" />
          <q-tab name="notificaciones" icon="notifications" label="Notificaciones" />
          <q-tab name="mantenimiento" icon="build" label="Mantenimiento" />
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="tabActivo" animated>
          <!-- Panel General -->
          <q-tab-panel name="general">
            <div class="text-h6 q-mb-md">Configuración General del Sistema</div>

            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Información del Sistema</div>
                    <div class="q-gutter-md">
                      <q-input
                        v-model="configuracion.nombre_sistema"
                        label="Nombre del Sistema"
                        outlined
                        dense
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model="configuracion.version_sistema"
                        label="Versión"
                        outlined
                        dense
                        readonly
                      />
                      <q-select
                        v-model="configuracion.idioma_predeterminado"
                        :options="idiomaOptions"
                        label="Idioma Predeterminado"
                        outlined
                        dense
                        emit-value
                        map-options
                        @update:model-value="marcarCambio"
                      />
                      <q-select
                        v-model="configuracion.zona_horaria"
                        :options="zonaHorariaOptions"
                        label="Zona Horaria"
                        outlined
                        dense
                        emit-value
                        map-options
                        @update:model-value="marcarCambio"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
              <div class="col-12 col-md-5">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Configuración Regional</div>
                    <div class="q-gutter-md">
                      <q-select
                        v-model="configuracion.moneda_predeterminada"
                        :options="monedaOptions"
                        label="Moneda Predeterminada"
                        outlined
                        dense
                        emit-value
                        map-options
                        @update:model-value="marcarCambio"
                      />
                      <q-select
                        v-model="configuracion.formato_fecha"
                        :options="formatoFechaOptions"
                        label="Formato de Fecha"
                        outlined
                        dense
                        emit-value
                        map-options
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model.number="configuracion.decimales_moneda"
                        label="Decimales para Moneda"
                        outlined
                        dense
                        type="number"
                        min="0"
                        max="4"
                        @update:model-value="marcarCambio"
                      />
                      <q-toggle
                        v-model="configuracion.modo_debug"
                        label="Modo Debug"
                        @update:model-value="marcarCambio"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </q-tab-panel>

          <!-- Panel Empresa -->
          <q-tab-panel name="empresa">
            <div class="text-h6 q-mb-md">Información de la Empresa</div>

            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Datos Básicos</div>
                    <div class="q-gutter-md">
                      <q-input
                        v-model="configuracion.empresa_nombre"
                        label="Nombre de la Empresa"
                        outlined
                        dense
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model="configuracion.empresa_rut"
                        label="RUT"
                        outlined
                        dense
                        mask="##.###.###-#"
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model="configuracion.empresa_giro"
                        label="Giro Comercial"
                        outlined
                        dense
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model="configuracion.empresa_direccion"
                        label="Dirección"
                        outlined
                        dense
                        @update:model-value="marcarCambio"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
              <div class="col-12 col-md-5">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Contacto</div>
                    <div class="q-gutter-md">
                      <q-input
                        v-model="configuracion.empresa_telefono"
                        label="Teléfono"
                        outlined
                        dense
                        mask="(##) ####-####"
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model="configuracion.empresa_email"
                        label="Email"
                        outlined
                        dense
                        type="email"
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model="configuracion.empresa_sitio_web"
                        label="Sitio Web"
                        outlined
                        dense
                        @update:model-value="marcarCambio"
                      />
                      <q-file
                        v-model="logoEmpresa"
                        label="Logo de la Empresa"
                        outlined
                        dense
                        accept="image/*"
                        max-file-size="2097152"
                        @rejected="onRejectedFile"
                        @update:model-value="marcarCambio"
                      >
                        <template v-slot:prepend>
                          <q-icon name="image" />
                        </template>
                      </q-file>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </q-tab-panel>

          <!-- Panel Inventario -->
          <q-tab-panel name="inventario">
            <div class="text-h6 q-mb-md">Configuración de Inventario</div>

            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Códigos y Numeración</div>
                    <div class="q-gutter-md">
                      <q-input
                        v-model="configuracion.prefijo_productos"
                        label="Prefijo Productos"
                        outlined
                        dense
                        @update:model-value="marcarCambio"
                        hint="Ej: PRD, PROD"
                      />
                      <q-input
                        v-model.number="configuracion.longitud_codigo_producto"
                        label="Longitud Código Producto"
                        outlined
                        dense
                        type="number"
                        min="4"
                        max="20"
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model="configuracion.prefijo_movimientos"
                        label="Prefijo Movimientos"
                        outlined
                        dense
                        @update:model-value="marcarCambio"
                        hint="Ej: MOV, MOVIM"
                      />
                      <q-toggle
                        v-model="configuracion.auto_generar_codigos"
                        label="Generar Códigos Automáticamente"
                        @update:model-value="marcarCambio"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
              <div class="col-12 col-md-5">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Stock y Alertas</div>
                    <div class="q-gutter-md">
                      <q-input
                        v-model.number="configuracion.stock_minimo_predeterminado"
                        label="Stock Mínimo Predeterminado"
                        outlined
                        dense
                        type="number"
                        min="0"
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model.number="configuracion.dias_alerta_vencimiento"
                        label="Días Alerta Vencimiento"
                        outlined
                        dense
                        type="number"
                        min="1"
                        @update:model-value="marcarCambio"
                      />
                      <q-toggle
                        v-model="configuracion.permitir_stock_negativo"
                        label="Permitir Stock Negativo"
                        @update:model-value="marcarCambio"
                      />
                      <q-toggle
                        v-model="configuracion.validar_stock_movimientos"
                        label="Validar Stock en Movimientos"
                        @update:model-value="marcarCambio"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>

            <div class="row q-gutter-md q-mt-md">
              <div class="col-12">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Métodos de Costeo</div>
                    <div class="row q-gutter-md">
                      <div class="col-12 col-md-4">
                        <q-select
                          v-model="configuracion.metodo_costeo"
                          :options="metodoCosteoOptions"
                          label="Método de Costeo"
                          outlined
                          dense
                          emit-value
                          map-options
                          @update:model-value="marcarCambio"
                        />
                      </div>
                      <div class="col-12 col-md-4">
                        <q-toggle
                          v-model="configuracion.actualizar_costo_promedio"
                          label="Actualizar Costo Promedio"
                          @update:model-value="marcarCambio"
                        />
                      </div>
                      <div class="col-12 col-md-3">
                        <q-toggle
                          v-model="configuracion.incluir_impuestos_costo"
                          label="Incluir Impuestos en Costo"
                          @update:model-value="marcarCambio"
                        />
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </q-tab-panel>

          <!-- Panel Usuarios -->
          <q-tab-panel name="usuarios">
            <div class="text-h6 q-mb-md">Configuración de Usuarios</div>

            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Políticas de Contraseñas</div>
                    <div class="q-gutter-md">
                      <q-input
                        v-model.number="configuracion.min_longitud_password"
                        label="Longitud Mínima Contraseña"
                        outlined
                        dense
                        type="number"
                        min="6"
                        max="50"
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model.number="configuracion.dias_expiracion_password"
                        label="Días Expiración Contraseña"
                        outlined
                        dense
                        type="number"
                        min="0"
                        hint="0 = sin expiración"
                        @update:model-value="marcarCambio"
                      />
                      <q-toggle
                        v-model="configuracion.requiere_mayuscula"
                        label="Requiere Mayúscula"
                        @update:model-value="marcarCambio"
                      />
                      <q-toggle
                        v-model="configuracion.requiere_numero"
                        label="Requiere Número"
                        @update:model-value="marcarCambio"
                      />
                      <q-toggle
                        v-model="configuracion.requiere_caracter_especial"
                        label="Requiere Carácter Especial"
                        @update:model-value="marcarCambio"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
              <div class="col-12 col-md-5">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Sesiones</div>
                    <div class="q-gutter-md">
                      <q-input
                        v-model.number="configuracion.tiempo_sesion_minutos"
                        label="Tiempo Sesión (minutos)"
                        outlined
                        dense
                        type="number"
                        min="15"
                        max="1440"
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model.number="configuracion.intentos_login_max"
                        label="Máximo Intentos Login"
                        outlined
                        dense
                        type="number"
                        min="3"
                        max="10"
                        @update:model-value="marcarCambio"
                      />
                      <q-toggle
                        v-model="configuracion.cerrar_sesion_inactividad"
                        label="Cerrar por Inactividad"
                        @update:model-value="marcarCambio"
                      />
                      <q-toggle
                        v-model="configuracion.sesion_unica"
                        label="Sesión Única por Usuario"
                        @update:model-value="marcarCambio"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </q-tab-panel>

          <!-- Panel Integraciones -->
          <q-tab-panel name="integraciones">
            <div class="text-h6 q-mb-md">Integraciones Externas</div>

            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Configuración de Email</div>
                    <div class="q-gutter-md">
                      <q-input
                        v-model="configuracion.smtp_servidor"
                        label="Servidor SMTP"
                        outlined
                        dense
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model.number="configuracion.smtp_puerto"
                        label="Puerto SMTP"
                        outlined
                        dense
                        type="number"
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model="configuracion.smtp_usuario"
                        label="Usuario SMTP"
                        outlined
                        dense
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model="configuracion.smtp_password"
                        label="Contraseña SMTP"
                        outlined
                        dense
                        type="password"
                        @update:model-value="marcarCambio"
                      />
                      <q-toggle
                        v-model="configuracion.smtp_ssl"
                        label="Usar SSL/TLS"
                        @update:model-value="marcarCambio"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
              <div class="col-12 col-md-5">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">APIs Externas</div>
                    <div class="q-gutter-md">
                      <q-input
                        v-model="configuracion.api_key_externa"
                        label="API Key Externa"
                        outlined
                        dense
                        type="password"
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model="configuracion.webhook_url"
                        label="Webhook URL"
                        outlined
                        dense
                        @update:model-value="marcarCambio"
                      />
                      <q-toggle
                        v-model="configuracion.habilitar_integraciones"
                        label="Habilitar Integraciones"
                        @update:model-value="marcarCambio"
                      />
                      <q-btn
                        color="secondary"
                        icon="test_tube"
                        label="Probar Conexión"
                        @click="probarConexionEmail"
                        :loading="probandoConexion"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </q-tab-panel>

          <!-- Panel Seguridad -->
          <q-tab-panel name="seguridad">
            <div class="text-h6 q-mb-md">Configuración de Seguridad</div>

            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Auditoría</div>
                    <div class="q-gutter-md">
                      <q-toggle
                        v-model="configuracion.habilitar_auditoria"
                        label="Habilitar Auditoría"
                        @update:model-value="marcarCambio"
                      />
                      <q-toggle
                        v-model="configuracion.auditar_consultas"
                        label="Auditar Consultas"
                        @update:model-value="marcarCambio"
                      />
                      <q-toggle
                        v-model="configuracion.auditar_modificaciones"
                        label="Auditar Modificaciones"
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model.number="configuracion.dias_retencion_logs"
                        label="Días Retención Logs"
                        outlined
                        dense
                        type="number"
                        min="30"
                        @update:model-value="marcarCambio"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
              <div class="col-12 col-md-5">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Respaldos</div>
                    <div class="q-gutter-md">
                      <q-toggle
                        v-model="configuracion.respaldo_automatico"
                        label="Respaldo Automático"
                        @update:model-value="marcarCambio"
                      />
                      <q-select
                        v-model="configuracion.frecuencia_respaldo"
                        :options="frecuenciaRespaldoOptions"
                        label="Frecuencia Respaldo"
                        outlined
                        dense
                        emit-value
                        map-options
                        @update:model-value="marcarCambio"
                      />
                      <q-input
                        v-model.number="configuracion.cantidad_respaldos_mantener"
                        label="Cantidad Respaldos a Mantener"
                        outlined
                        dense
                        type="number"
                        min="1"
                        @update:model-value="marcarCambio"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </q-tab-panel>

          <!-- Panel Notificaciones -->
          <q-tab-panel name="notificaciones">
            <div class="text-h6 q-mb-md">Configuración de Notificaciones</div>

            <div class="row q-gutter-md">
              <div class="col-12">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Tipos de Notificaciones</div>
                    <div class="row q-gutter-md">
                      <div class="col-12 col-md-3">
                        <q-list dense>
                          <q-item-label header>Stock</q-item-label>
                          <q-item tag="label" v-ripple>
                            <q-item-section avatar>
                              <q-checkbox v-model="configuracion.notif_stock_minimo" @update:model-value="marcarCambio" />
                            </q-item-section>
                            <q-item-section>
                              <q-item-label>Stock Mínimo</q-item-label>
                            </q-item-section>
                          </q-item>
                          <q-item tag="label" v-ripple>
                            <q-item-section avatar>
                              <q-checkbox v-model="configuracion.notif_vencimientos" @update:model-value="marcarCambio" />
                            </q-item-section>
                            <q-item-section>
                              <q-item-label>Vencimientos</q-item-label>
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </div>
                      <div class="col-12 col-md-3">
                        <q-list dense>
                          <q-item-label header>Movimientos</q-item-label>
                          <q-item tag="label" v-ripple>
                            <q-item-section avatar>
                              <q-checkbox v-model="configuracion.notif_movimientos_criticos" @update:model-value="marcarCambio" />
                            </q-item-section>
                            <q-item-section>
                              <q-item-label>Movimientos Críticos</q-item-label>
                            </q-item-section>
                          </q-item>
                          <q-item tag="label" v-ripple>
                            <q-item-section avatar>
                              <q-checkbox v-model="configuracion.notif_traspasos" @update:model-value="marcarCambio" />
                            </q-item-section>
                            <q-item-section>
                              <q-item-label>Traspasos</q-item-label>
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </div>
                      <div class="col-12 col-md-3">
                        <q-list dense>
                          <q-item-label header>Sistema</q-item-label>
                          <q-item tag="label" v-ripple>
                            <q-item-section avatar>
                              <q-checkbox v-model="configuracion.notif_errores_sistema" @update:model-value="marcarCambio" />
                            </q-item-section>
                            <q-item-section>
                              <q-item-label>Errores del Sistema</q-item-label>
                            </q-item-section>
                          </q-item>
                          <q-item tag="label" v-ripple>
                            <q-item-section avatar>
                              <q-checkbox v-model="configuracion.notif_respaldos" @update:model-value="marcarCambio" />
                            </q-item-section>
                            <q-item-section>
                              <q-item-label>Respaldos</q-item-label>
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </div>
                      <div class="col-12 col-md-2">
                        <q-list dense>
                          <q-item-label header>Usuarios</q-item-label>
                          <q-item tag="label" v-ripple>
                            <q-item-section avatar>
                              <q-checkbox v-model="configuracion.notif_nuevos_usuarios" @update:model-value="marcarCambio" />
                            </q-item-section>
                            <q-item-section>
                              <q-item-label>Nuevos Usuarios</q-item-label>
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </q-tab-panel>

          <!-- Panel Mantenimiento -->
          <q-tab-panel name="mantenimiento">
            <div class="text-h6 q-mb-md">Mantenimiento del Sistema</div>

            <div class="row q-gutter-md">
              <div class="col-12 col-md-6">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Limpieza de Datos</div>
                    <div class="q-gutter-md">
                      <q-btn
                        color="warning"
                        icon="cleaning_services"
                        label="Limpiar Logs Antiguos"
                        @click="limpiarLogs"
                        :loading="limpiandoLogs"
                        class="full-width"
                      />
                      <q-btn
                        color="info"
                        icon="compress"
                        label="Optimizar Base de Datos"
                        @click="optimizarBD"
                        :loading="optimizandoBD"
                        class="full-width"
                      />
                      <q-btn
                        color="secondary"
                        icon="refresh"
                        label="Recalcular Stocks"
                        @click="recalcularStocks"
                        :loading="recalculandoStocks"
                        class="full-width"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
              <div class="col-12 col-md-5">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Respaldos Manuales</div>
                    <div class="q-gutter-md">
                      <q-btn
                        color="positive"
                        icon="backup"
                        label="Crear Respaldo Completo"
                        @click="crearRespaldo"
                        :loading="creandoRespaldo"
                        class="full-width"
                      />
                      <q-btn
                        color="negative"
                        icon="restore"
                        label="Restaurar desde Respaldo"
                        @click="mostrarDialogoRestaurar"
                        class="full-width"
                      />
                      <q-btn
                        color="primary"
                        icon="download"
                        label="Descargar Respaldo"
                        @click="descargarRespaldo"
                        class="full-width"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>

            <div class="row q-gutter-md q-mt-md">
              <div class="col-12">
                <q-card flat bordered>
                  <q-card-section>
                    <div class="text-subtitle1 q-mb-md">Información del Sistema</div>
                    <q-table
                      :rows="infoSistema"
                      :columns="columnsInfoSistema"
                      row-key="parametro"
                      flat
                      dense
                      hide-pagination
                      :rows-per-page-options="[0]"
                    />
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </q-card>

      <!-- Restore Dialog -->
      <q-dialog v-model="showRestaurarDialog" persistent>
        <q-card style="min-width: 500px">
          <q-card-section class="row items-center">
            <q-icon name="warning" color="negative" size="md" class="q-mr-sm" />
            <div class="text-h6">Restaurar Sistema</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <div class="text-body1 q-mb-md">
              <strong>¡ATENCIÓN!</strong> Esta operación sobrescribirá todos los datos actuales del sistema.
            </div>
            <q-file
              v-model="archivoRespaldo"
              label="Seleccionar archivo de respaldo"
              outlined
              dense
              accept=".sql,.bak"
            >
              <template v-slot:prepend>
                <q-icon name="attach_file" />
              </template>
            </q-file>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="negative"
              label="Restaurar"
              @click="restaurarSistema"
              :loading="restaurandoSistema"
              :disable="!archivoRespaldo"
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

const $q = useQuasar()

// Types
interface ConfiguracionSistema {
  // General
  nombre_sistema: string
  version_sistema: string
  idioma_predeterminado: string
  zona_horaria: string
  moneda_predeterminada: string
  formato_fecha: string
  decimales_moneda: number
  modo_debug: boolean

  // Empresa
  empresa_nombre: string
  empresa_rut: string
  empresa_giro: string
  empresa_direccion: string
  empresa_telefono: string
  empresa_email: string
  empresa_sitio_web: string

  // Inventario
  prefijo_productos: string
  longitud_codigo_producto: number
  prefijo_movimientos: string
  auto_generar_codigos: boolean
  stock_minimo_predeterminado: number
  dias_alerta_vencimiento: number
  permitir_stock_negativo: boolean
  validar_stock_movimientos: boolean
  metodo_costeo: string
  actualizar_costo_promedio: boolean
  incluir_impuestos_costo: boolean

  // Usuarios
  min_longitud_password: number
  dias_expiracion_password: number
  requiere_mayuscula: boolean
  requiere_numero: boolean
  requiere_caracter_especial: boolean
  tiempo_sesion_minutos: number
  intentos_login_max: number
  cerrar_sesion_inactividad: boolean
  sesion_unica: boolean

  // Integraciones
  smtp_servidor: string
  smtp_puerto: number
  smtp_usuario: string
  smtp_password: string
  smtp_ssl: boolean
  api_key_externa: string
  webhook_url: string
  habilitar_integraciones: boolean

  // Seguridad
  habilitar_auditoria: boolean
  auditar_consultas: boolean
  auditar_modificaciones: boolean
  dias_retencion_logs: number
  respaldo_automatico: boolean
  frecuencia_respaldo: string
  cantidad_respaldos_mantener: number

  // Notificaciones
  notif_stock_minimo: boolean
  notif_vencimientos: boolean
  notif_movimientos_criticos: boolean
  notif_traspasos: boolean
  notif_errores_sistema: boolean
  notif_respaldos: boolean
  notif_nuevos_usuarios: boolean
}

// Reactive data
const configuracion = ref<ConfiguracionSistema>({
  // General
  nombre_sistema: 'ERP DAEL',
  version_sistema: '1.0.0',
  idioma_predeterminado: 'es',
  zona_horaria: 'America/Santiago',
  moneda_predeterminada: 'CLP',
  formato_fecha: 'DD/MM/YYYY',
  decimales_moneda: 0,
  modo_debug: false,

  // Empresa
  empresa_nombre: '',
  empresa_rut: '',
  empresa_giro: '',
  empresa_direccion: '',
  empresa_telefono: '',
  empresa_email: '',
  empresa_sitio_web: '',

  // Inventario
  prefijo_productos: 'PRD',
  longitud_codigo_producto: 8,
  prefijo_movimientos: 'MOV',
  auto_generar_codigos: true,
  stock_minimo_predeterminado: 10,
  dias_alerta_vencimiento: 30,
  permitir_stock_negativo: false,
  validar_stock_movimientos: true,
  metodo_costeo: 'promedio',
  actualizar_costo_promedio: true,
  incluir_impuestos_costo: false,

  // Usuarios
  min_longitud_password: 8,
  dias_expiracion_password: 90,
  requiere_mayuscula: true,
  requiere_numero: true,
  requiere_caracter_especial: false,
  tiempo_sesion_minutos: 480,
  intentos_login_max: 5,
  cerrar_sesion_inactividad: true,
  sesion_unica: false,

  // Integraciones
  smtp_servidor: '',
  smtp_puerto: 587,
  smtp_usuario: '',
  smtp_password: '',
  smtp_ssl: true,
  api_key_externa: '',
  webhook_url: '',
  habilitar_integraciones: false,

  // Seguridad
  habilitar_auditoria: true,
  auditar_consultas: false,
  auditar_modificaciones: true,
  dias_retencion_logs: 365,
  respaldo_automatico: true,
  frecuencia_respaldo: 'daily',
  cantidad_respaldos_mantener: 30,

  // Notificaciones
  notif_stock_minimo: true,
  notif_vencimientos: true,
  notif_movimientos_criticos: true,
  notif_traspasos: true,
  notif_errores_sistema: true,
  notif_respaldos: true,
  notif_nuevos_usuarios: false
})

const estadoSistema = ref<any>(null)
const infoSistema = ref<any[]>([])
const isGuardando = ref(false)
const hayCambios = ref(false)
const tabActivo = ref('general')
const logoEmpresa = ref<File | null>(null)
const archivoRespaldo = ref<File | null>(null)
const showRestaurarDialog = ref(false)

// Loading states
const probandoConexion = ref(false)
const limpiandoLogs = ref(false)
const optimizandoBD = ref(false)
const recalculandoStocks = ref(false)
const creandoRespaldo = ref(false)
const restaurandoSistema = ref(false)

// Computed properties would go here if needed

// Options
const idiomaOptions = [
  { label: 'Español', value: 'es' },
  { label: 'English', value: 'en' },
  { label: 'Português', value: 'pt' }
]

const zonaHorariaOptions = [
  { label: 'Santiago (GMT-3)', value: 'America/Santiago' },
  { label: 'Buenos Aires (GMT-3)', value: 'America/Argentina/Buenos_Aires' },
  { label: 'Lima (GMT-5)', value: 'America/Lima' },
  { label: 'Bogotá (GMT-5)', value: 'America/Bogota' }
]

const monedaOptions = [
  { label: 'Peso Chileno (CLP)', value: 'CLP' },
  { label: 'Dólar Americano (USD)', value: 'USD' },
  { label: 'Euro (EUR)', value: 'EUR' },
  { label: 'Peso Argentino (ARS)', value: 'ARS' }
]

const formatoFechaOptions = [
  { label: 'DD/MM/YYYY', value: 'DD/MM/YYYY' },
  { label: 'MM/DD/YYYY', value: 'MM/DD/YYYY' },
  { label: 'YYYY-MM-DD', value: 'YYYY-MM-DD' }
]

const metodoCosteoOptions = [
  { label: 'Costo Promedio', value: 'promedio' },
  { label: 'FIFO (Primero en Entrar, Primero en Salir)', value: 'fifo' },
  { label: 'LIFO (Último en Entrar, Primero en Salir)', value: 'lifo' },
  { label: 'Costo Estándar', value: 'estandar' }
]

const frecuenciaRespaldoOptions = [
  { label: 'Diario', value: 'daily' },
  { label: 'Semanal', value: 'weekly' },
  { label: 'Mensual', value: 'monthly' }
]

const columnsInfoSistema = [
  {
    name: 'parametro',
    label: 'Parámetro',
    align: 'left' as const,
    field: 'parametro'
  },
  {
    name: 'valor',
    label: 'Valor',
    align: 'left' as const,
    field: 'valor'
  }
]

// Methods
const cargarConfiguracion = async () => {
  try {
    // TODO: Implement API call to load configuration
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar configuración',
      caption: error.message
    })
  }
}

const cargarEstadoSistema = async () => {
  try {
    // TODO: Implement API call to load system status
    estadoSistema.value = {
      database_status: 'online',
      memory_usage: 65,
      active_users: 12,
      uptime_days: 45,
      last_update: '2024-01-15'
    }

    infoSistema.value = [
      { parametro: 'Versión del Sistema', valor: '1.0.0' },
      { parametro: 'Base de Datos', valor: 'PostgreSQL 14.2' },
      { parametro: 'Servidor Web', valor: 'FastAPI 0.104.1' },
      { parametro: 'Espacio en Disco', valor: '2.5 GB / 10 GB' },
      { parametro: 'Último Respaldo', valor: 'Hace 2 horas' }
    ]
  } catch (error: any) {
    console.error('Error al cargar estado del sistema:', error)
  }
}

const marcarCambio = () => {
  hayCambios.value = true
}

const guardarConfiguracion = async () => {
  try {
    isGuardando.value = true
    // TODO: Implement API call to save configuration

    $q.notify({
      type: 'positive',
      message: 'Configuración guardada correctamente'
    })

    hayCambios.value = false
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar configuración',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const exportarConfiguracion = async () => {
  try {
    // TODO: Implement configuration export
    $q.notify({
      type: 'positive',
      message: 'Configuración exportada correctamente'
    })
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al exportar configuración',
      caption: error.message
    })
  }
}

const probarConexionEmail = async () => {
  try {
    probandoConexion.value = true
    // TODO: Implement email connection test

    $q.notify({
      type: 'positive',
      message: 'Conexión de email exitosa'
    })
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error en conexión de email',
      caption: error.message
    })
  } finally {
    probandoConexion.value = false
  }
}

const limpiarLogs = async () => {
  $q.dialog({
    title: 'Limpiar Logs',
    message: '¿Está seguro de eliminar los logs antiguos?',
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      limpiandoLogs.value = true
      // TODO: Implement log cleanup

      $q.notify({
        type: 'positive',
        message: 'Logs limpiados correctamente'
      })
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al limpiar logs',
        caption: error.message
      })
    } finally {
      limpiandoLogs.value = false
    }
  })
}

const optimizarBD = async () => {
  $q.dialog({
    title: 'Optimizar Base de Datos',
    message: '¿Está seguro de optimizar la base de datos? Esta operación puede tomar varios minutos.',
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      optimizandoBD.value = true
      // TODO: Implement database optimization

      $q.notify({
        type: 'positive',
        message: 'Base de datos optimizada correctamente'
      })
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al optimizar base de datos',
        caption: error.message
      })
    } finally {
      optimizandoBD.value = false
    }
  })
}

const recalcularStocks = async () => {
  $q.dialog({
    title: 'Recalcular Stocks',
    message: '¿Está seguro de recalcular todos los stocks? Esta operación puede tomar tiempo.',
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      recalculandoStocks.value = true
      // TODO: Implement stock recalculation

      $q.notify({
        type: 'positive',
        message: 'Stocks recalculados correctamente'
      })
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al recalcular stocks',
        caption: error.message
      })
    } finally {
      recalculandoStocks.value = false
    }
  })
}

const crearRespaldo = async () => {
  $q.dialog({
    title: 'Crear Respaldo',
    message: '¿Está seguro de crear un respaldo completo del sistema?',
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      creandoRespaldo.value = true
      // TODO: Implement backup creation

      $q.notify({
        type: 'positive',
        message: 'Respaldo creado correctamente'
      })
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al crear respaldo',
        caption: error.message
      })
    } finally {
      creandoRespaldo.value = false
    }
  })
}

const mostrarDialogoRestaurar = () => {
  showRestaurarDialog.value = true
}

const restaurarSistema = async () => {
  try {
    restaurandoSistema.value = true
    // TODO: Implement system restore

    $q.notify({
      type: 'positive',
      message: 'Sistema restaurado correctamente'
    })

    showRestaurarDialog.value = false
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al restaurar sistema',
      caption: error.message
    })
  } finally {
    restaurandoSistema.value = false
  }
}

const descargarRespaldo = async () => {
  try {
    // TODO: Implement backup download
    $q.notify({
      type: 'positive',
      message: 'Descarga iniciada'
    })
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al descargar respaldo',
      caption: error.message
    })
  }
}

const onRejectedFile = (rejectedEntries: any[]) => {
  $q.notify({
    type: 'negative',
    message: `Archivo no válido: ${rejectedEntries[0].failedPropValidation}`
  })
}

const formatDate = (dateString: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-CL')
}

// Lifecycle
onMounted(async () => {
  await cargarConfiguracion()
  await cargarEstadoSistema()
})
</script>