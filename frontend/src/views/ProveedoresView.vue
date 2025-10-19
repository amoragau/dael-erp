<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-xl">
        <div>
          <div class="row items-center q-mb-sm">
            <q-icon name="business" size="32px" color="primary" class="q-mr-md" />
            <div>
              <h4 class="q-my-none text-h4 text-weight-light">Información Comercial de <span class="text-weight-bold text-primary">Proveedores</span></h4>
              <p class="text-grey-6 q-mb-none text-body2">Gestión integral de proveedores con datos fiscales y condiciones comerciales</p>
            </div>
          </div>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nuevo Proveedor"
          @click="abrirFormularioProveedor"
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
                placeholder="Buscar por nombre, código o RUT..."
                outlined
                dense
                clearable
              >
                <template v-slot:prepend>
                  <q-icon name="search" color="grey-5" />
                </template>
              </q-input>
            </div>
            <div class="col-12 col-md-3">
              <q-select
                v-model="filtros.estado"
                :options="estadoOptions"
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
                v-model="filtros.clasificacion"
                :options="clasificacionOptions"
                label="Clasificación"
                outlined
                dense
                clearable
                emit-value
                map-options
              />
            </div>
            <div class="col-12 col-md-3 row q-gutter-sm justify-end items-center">
              <q-btn
                color="primary"
                icon="search"
                label="Buscar"
                @click="buscarProveedores"
                unelevated
                no-caps
              />
              <q-btn
                color="grey-6"
                icon="clear"
                label="Limpiar"
                @click="limpiarFiltros"
                flat
                no-caps
              />
            </div>
          </div>
        </q-card-section>
      </q-card>

      <!-- Providers Table -->
      <q-table
        :rows="proveedores"
        :columns="columnsProveedores"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_proveedor"
        flat
        bordered
        @request="onRequestProveedores"
      >
        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'green' : 'red'"
              :label="props.value ? 'Activo' : 'Inactivo'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-dias_credito="props">
          <q-td :props="props">
            <q-badge
              :color="props.value > 0 ? 'blue' : 'grey'"
              :label="props.value > 0 ? `${props.value} días` : 'Contado'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-limite_credito="props">
          <q-td :props="props">
            <span v-if="props.value && props.value > 0" class="text-weight-medium">
              {{ formatCurrency(props.value) }}
            </span>
            <span v-else class="text-grey-5">Sin límite</span>
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
              @click="verDetalleProveedor(props.row as Proveedor)"
            >
              <q-tooltip>Ver Detalles</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="edit"
              color="primary"
              size="sm"
              @click="editarProveedor(props.row as Proveedor)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'negative' : 'positive'"
              size="sm"
              @click="toggleEstadoProveedor(props.row as Proveedor)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="store"
              color="info"
              size="sm"
              @click="verSucursales(props.row as Proveedor)"
            >
              <q-tooltip>Ver Sucursales</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Proveedor Dialog -->
      <q-dialog v-model="showCreateProveedorDialog" persistent>
        <q-card style="min-width: 1200px; max-width: 1400px; max-height: 90vh">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">{{ editandoProveedor ? 'Editar' : 'Nuevo' }} Proveedor</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section class="q-pt-none" style="max-height: calc(90vh - 120px);">
            <q-form @submit="guardarProveedor">
              <div class="row" style="height: calc(90vh - 160px);">
                <div class="col-3">
                  <q-tabs
                    v-model="tabActivo"
                    vertical
                    class="text-primary full-height"
                  >
                    <q-tab name="basica" icon="business" label="Información Básica" />
                    <q-tab name="fiscal" icon="receipt" label="Datos Fiscales" />
                    <q-tab name="comercial" icon="handshake" label="Condiciones Comerciales" />
                    <q-tab name="contacto" icon="contacts" label="Contacto Principal" />
                    <q-tab name="entrega" icon="local_shipping" label="Información de Entrega" />
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
                            v-model="formProveedor.codigo_proveedor"
                            label="Código *"
                            outlined
                            dense
                            maxlength="20"
                            :rules="[val => !!val || 'El código es requerido']"
                            hint="Código único del proveedor"
                          />
                        </div>
                        <div class="col-12 col-md-7">
                          <q-input
                            v-model="formProveedor.nombre_proveedor"
                            label="Nombre Comercial *"
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
                            v-model="formProveedor.razon_social"
                            label="Razón Social"
                            outlined
                            dense
                            maxlength="300"
                            hint="Nombre legal de la empresa"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formProveedor.telefono"
                            label="Teléfono Principal"
                            outlined
                            dense
                            mask="(###) ###-####"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formProveedor.email"
                            label="Email Corporativo"
                            type="email"
                            outlined
                            dense
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formProveedor.sitio_web"
                            label="Sitio Web"
                            outlined
                            dense
                            hint="ej: www.empresa.com"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-select
                            v-model="formProveedor.clasificacion"
                            :options="clasificacionOptions"
                            label="Clasificación"
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
                            v-model="formProveedor.direccion"
                            label="Dirección Principal"
                            outlined
                            dense
                            hint="Dirección de oficinas principales"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-md">
                        <div class="col-12">
                          <q-toggle
                            v-model="formProveedor.activo"
                            label="Proveedor Activo"
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Datos Fiscales -->
                    <q-tab-panel name="fiscal">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="receipt" class="q-mr-sm" />
                        Datos Fiscales
                      </div>

                      <!-- Identificación Tributaria -->
                      <div class="text-subtitle1 q-mb-sm">Identificación Tributaria</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formProveedor.rfc"
                            label="RUT"
                            outlined
                            dense
                            maxlength="12"
                            hint="Rol Único Tributario (ej: 12.345.678-9)"
                            mask="##.###.###-#"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formProveedor.giro_comercial"
                            label="Giro Comercial"
                            outlined
                            dense
                            hint="Actividad comercial principal"
                          />
                        </div>
                      </div>

                      <!-- Domicilio Fiscal -->
                      <div class="text-subtitle1 q-mb-sm q-mt-lg">Domicilio Fiscal</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12">
                          <q-input
                            v-model="formProveedor.direccion_fiscal"
                            label="Dirección Fiscal"
                            outlined
                            dense
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formProveedor.ciudad_fiscal"
                            label="Ciudad"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formProveedor.estado_fiscal"
                            label="Estado/Región"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model="formProveedor.codigo_postal_fiscal"
                            label="Código Postal"
                            outlined
                            dense
                            mask="#####"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formProveedor.pais_fiscal"
                            label="País"
                            outlined
                            dense
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Condiciones Comerciales -->
                    <q-tab-panel name="comercial">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="handshake" class="q-mr-sm" />
                        Condiciones Comerciales
                      </div>

                      <!-- Términos de Crédito -->
                      <div class="text-subtitle1 q-mb-sm">Términos de Crédito</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model.number="formProveedor.dias_credito"
                            label="Días de Crédito *"
                            outlined
                            dense
                            type="number"
                            min="0"
                            max="365"
                            :rules="[val => val >= 0 || 'Debe ser mayor o igual a 0']"
                            hint="0 = Contado"
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model.number="formProveedor.limite_credito"
                            label="Límite de Crédito"
                            outlined
                            dense
                            type="number"
                            step="0.01"
                            min="0"
                            prefix="$"
                            hint="Dejar vacío = Sin límite"
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-select
                            v-model="formProveedor.moneda_preferida"
                            :options="monedaOptions"
                            label="Moneda Preferida"
                            outlined
                            dense
                            emit-value
                            map-options
                          />
                        </div>
                      </div>

                      <!-- Descuentos -->
                      <div class="text-subtitle1 q-mb-sm q-mt-lg">Descuentos</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model.number="formProveedor.descuento_comercial"
                            label="Descuento Comercial (%)"
                            outlined
                            dense
                            type="number"
                            step="0.01"
                            min="0"
                            max="100"
                            suffix="%"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model.number="formProveedor.descuento_pronto_pago"
                            label="Descuento Pronto Pago (%)"
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

                      <!-- Formas de Pago -->
                      <div class="text-subtitle1 q-mb-sm q-mt-lg">Formas de Pago</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-select
                            v-model="formProveedor.forma_pago_preferida"
                            :options="formaPagoOptions"
                            label="Forma de Pago Preferida"
                            outlined
                            dense
                            emit-value
                            map-options
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-select
                            v-model="formProveedor.metodo_pago_preferido"
                            :options="metodoPagoOptions"
                            label="Método de Pago Preferido"
                            outlined
                            dense
                            emit-value
                            map-options
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Contacto Principal -->
                    <q-tab-panel name="contacto">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="contacts" class="q-mr-sm" />
                        Contacto Principal
                      </div>

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formProveedor.contacto_principal"
                            label="Nombre del Contacto"
                            outlined
                            dense
                            maxlength="200"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formProveedor.puesto_contacto"
                            label="Puesto/Cargo"
                            outlined
                            dense
                            maxlength="100"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formProveedor.telefono_contacto_principal"
                            label="Teléfono Directo"
                            outlined
                            dense
                            mask="(###) ###-####"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formProveedor.email_contacto_principal"
                            label="Email Directo"
                            type="email"
                            outlined
                            dense
                          />
                        </div>
                      </div>
                    </q-tab-panel>

                    <!-- Panel Información de Entrega -->
                    <q-tab-panel name="entrega">
                      <div class="text-h6 q-mb-md">
                        <q-icon name="local_shipping" class="q-mr-sm" />
                        Información de Entrega
                      </div>

                      <!-- Dirección de Entrega -->
                      <div class="text-subtitle1 q-mb-sm">Dirección de Entrega</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12">
                          <q-input
                            v-model="formProveedor.direccion_entrega"
                            label="Dirección de Entrega"
                            outlined
                            dense
                            hint="Si es diferente a la dirección principal"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formProveedor.ciudad_entrega"
                            label="Ciudad"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formProveedor.estado_entrega"
                            label="Estado/Región"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model="formProveedor.codigo_postal_entrega"
                            label="Código Postal"
                            outlined
                            dense
                            mask="#####"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formProveedor.pais_entrega"
                            label="País"
                            outlined
                            dense
                          />
                        </div>
                      </div>

                      <!-- Contacto de Recepción -->
                      <div class="text-subtitle1 q-mb-sm q-mt-lg">Contacto de Recepción</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formProveedor.contacto_recepcion"
                            label="Responsable de Recepción"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formProveedor.telefono_recepcion"
                            label="Teléfono de Recepción"
                            outlined
                            dense
                            mask="(###) ###-####"
                          />
                        </div>
                      </div>

                      <!-- Instrucciones -->
                      <div class="text-subtitle1 q-mb-sm q-mt-lg">Instrucciones Especiales</div>
                      <q-separator class="q-mb-md" />

                      <div class="row q-gutter-md">
                        <div class="col-12">
                          <q-input
                            v-model="formProveedor.horario_entrega"
                            label="Horario de Entrega"
                            outlined
                            dense
                            hint="ej: Lunes a Viernes 8:00 - 17:00"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formProveedor.instrucciones_entrega"
                            label="Instrucciones de Entrega"
                            outlined
                            type="textarea"
                            rows="4"
                            hint="Indicaciones especiales para entregas"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formProveedor.observaciones"
                            label="Observaciones Generales"
                            outlined
                            type="textarea"
                            rows="3"
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
              label="Guardar Proveedor"
              @click="guardarProveedor"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Provider Detail Dialog -->
      <q-dialog v-model="showDetalleDialog" persistent>
        <q-card style="min-width: 800px; max-width: 1000px">
          <q-card-section class="row items-center">
            <div class="text-h6">Detalles del Proveedor</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section v-if="proveedorDetalle">
            <div class="row q-col-gutter-md">
              <!-- Información Básica -->
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Información Comercial</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Código</q-item-label>
                      <q-item-label>{{ proveedorDetalle.codigo_proveedor }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Nombre Comercial</q-item-label>
                      <q-item-label>{{ proveedorDetalle.nombre_proveedor }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>RUT</q-item-label>
                      <q-item-label>{{ proveedorDetalle.rfc || '-' }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Clasificación</q-item-label>
                      <q-item-label>{{ proveedorDetalle.clasificacion || '-' }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>

              <!-- Condiciones Comerciales -->
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Condiciones Comerciales</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Días de Crédito</q-item-label>
                      <q-item-label>
                        <q-badge
                          :color="proveedorDetalle.dias_credito > 0 ? 'blue' : 'grey'"
                          :label="proveedorDetalle.dias_credito > 0 ? `${proveedorDetalle.dias_credito} días` : 'Contado'"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Límite de Crédito</q-item-label>
                      <q-item-label>
                        <span v-if="proveedorDetalle.limite_credito && proveedorDetalle.limite_credito > 0">
                          {{ formatCurrency(proveedorDetalle.limite_credito) }}
                        </span>
                        <span v-else>Sin límite</span>
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Descuento Comercial</q-item-label>
                      <q-item-label>{{ proveedorDetalle.descuento_comercial || 0 }}%</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Moneda Preferida</q-item-label>
                      <q-item-label>{{ proveedorDetalle.moneda_preferida || 'CLP' }}</q-item-label>
                    </q-item-section>
                  </q-item>
                </q-list>
              </div>

              <!-- Contacto Principal -->
              <div class="col-12">
                <q-expansion-item
                  icon="contacts"
                  label="Contacto Principal"
                  class="q-mt-md"
                >
                  <q-card flat bordered>
                    <q-card-section>
                      <div class="row q-col-gutter-md">
                        <div class="col-12 col-md-6">
                          <q-list dense>
                            <q-item v-if="proveedorDetalle.contacto_principal">
                              <q-item-section>
                                <q-item-label caption>Nombre</q-item-label>
                                <q-item-label>{{ proveedorDetalle.contacto_principal }}</q-item-label>
                              </q-item-section>
                            </q-item>
                            <q-item v-if="proveedorDetalle.puesto_contacto">
                              <q-item-section>
                                <q-item-label caption>Puesto</q-item-label>
                                <q-item-label>{{ proveedorDetalle.puesto_contacto }}</q-item-label>
                              </q-item-section>
                            </q-item>
                          </q-list>
                        </div>
                        <div class="col-12 col-md-6">
                          <q-list dense>
                            <q-item v-if="proveedorDetalle.telefono_contacto_principal">
                              <q-item-section>
                                <q-item-label caption>Teléfono</q-item-label>
                                <q-item-label>{{ proveedorDetalle.telefono_contacto_principal }}</q-item-label>
                              </q-item-section>
                            </q-item>
                            <q-item v-if="proveedorDetalle.email_contacto_principal">
                              <q-item-section>
                                <q-item-label caption>Email</q-item-label>
                                <q-item-label>{{ proveedorDetalle.email_contacto_principal }}</q-item-label>
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
              v-if="proveedorDetalle"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Sucursales Dialog -->
      <q-dialog v-model="showSucursalesDialog" persistent>
        <q-card style="min-width: 1000px; max-width: 1200px">
          <q-card-section class="row items-center">
            <div class="text-h6">Sucursales de {{ proveedorSeleccionado?.nombre_proveedor }}</div>
            <q-space />
            <q-btn
              color="primary"
              icon="add"
              label="Nueva Sucursal"
              @click="abrirFormularioSucursal"
              class="q-mr-sm"
            />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <!-- Sucursales Table -->
            <q-table
              :rows="sucursales"
              :columns="columnsSucursales"
              :loading="isLoading"
              row-key="id_sucursal"
              flat
              bordered
            >
              <template v-slot:body-cell-activo="props">
                <q-td :props="props">
                  <q-badge
                    :color="props.value ? 'green' : 'red'"
                    :label="props.value ? 'Activo' : 'Inactivo'"
                  />
                </q-td>
              </template>

              <template v-slot:body-cell-es_sucursal_principal="props">
                <q-td :props="props">
                  <q-badge
                    :color="props.value ? 'blue' : 'grey'"
                    :label="props.value ? 'Principal' : 'Secundaria'"
                  />
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
                    @click="editarSucursal(props.row as SucursalProveedor)"
                  >
                    <q-tooltip>Editar</q-tooltip>
                  </q-btn>
                  <q-btn
                    v-if="!props.row.es_sucursal_principal"
                    flat
                    round
                    icon="star"
                    color="warning"
                    size="sm"
                    @click="establecerPrincipal(props.row as SucursalProveedor)"
                  >
                    <q-tooltip>Establecer como Principal</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    round
                    :icon="props.row.activo ? 'block' : 'check_circle'"
                    :color="props.row.activo ? 'negative' : 'positive'"
                    size="sm"
                    @click="toggleEstadoSucursal(props.row as SucursalProveedor)"
                  >
                    <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
                  </q-btn>
                  <q-btn
                    flat
                    round
                    icon="delete"
                    color="negative"
                    size="sm"
                    @click="eliminarSucursal(props.row as SucursalProveedor)"
                  >
                    <q-tooltip>Eliminar</q-tooltip>
                  </q-btn>
                </q-td>
              </template>
            </q-table>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cerrar" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Create/Edit Sucursal Dialog -->
      <q-dialog v-model="showCreateSucursalDialog" persistent>
        <q-card style="min-width: 600px; max-width: 800px">
          <q-card-section class="row items-center">
            <div class="text-h6">{{ editandoSucursal ? 'Editar' : 'Nueva' }} Sucursal</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section>
            <q-form @submit="guardarSucursal">
              <div class="row q-gutter-md">
                <div class="col-12 col-md-5">
                  <q-input
                    v-model="formSucursal.codigo_sucursal"
                    label="Código *"
                    outlined
                    dense
                    :rules="[val => !!val || 'El código es requerido']"
                  />
                </div>
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="formSucursal.nombre_sucursal"
                    label="Nombre *"
                    outlined
                    dense
                    :rules="[val => !!val || 'El nombre es requerido']"
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12">
                  <q-input
                    v-model="formSucursal.direccion"
                    label="Dirección"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formSucursal.ciudad"
                    label="Ciudad"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formSucursal.estado"
                    label="Estado/Región"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-input
                    v-model="formSucursal.codigo_postal"
                    label="Código Postal"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formSucursal.pais"
                    label="País"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formSucursal.telefono"
                    label="Teléfono"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-input
                    v-model="formSucursal.email"
                    label="Email"
                    type="email"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formSucursal.contacto"
                    label="Contacto"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-4">
                  <q-input
                    v-model="formSucursal.telefono_contacto"
                    label="Teléfono Contacto"
                    outlined
                    dense
                  />
                </div>
                <div class="col-12 col-md-3">
                  <q-input
                    v-model="formSucursal.email_contacto"
                    label="Email Contacto"
                    type="email"
                    outlined
                    dense
                  />
                </div>
              </div>

              <div class="row q-gutter-md q-mt-sm">
                <div class="col-12 col-md-6">
                  <q-toggle
                    v-model="formSucursal.es_sucursal_principal"
                    label="Sucursal Principal"
                  />
                </div>
                <div class="col-12 col-md-5">
                  <q-toggle
                    v-model="formSucursal.activo"
                    label="Activo"
                  />
                </div>
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Cancelar" v-close-popup />
            <q-btn
              color="primary"
              label="Guardar"
              @click="guardarSucursal"
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
  useProveedorStore,
  type Proveedor,
  type ProveedorCreate,
  type SucursalProveedor,
  type SucursalProveedorCreate
} from '../stores/proveedores'
import { formatCurrency } from '@/utils/formatters'

const $q = useQuasar()
const proveedorStore = useProveedorStore()

// Reactive data
const proveedores = ref<Proveedor[]>([])
const isLoading = ref(false)
const isGuardando = ref(false)
const showCreateProveedorDialog = ref(false)
const editandoProveedor = ref(false)
const showDetalleDialog = ref(false)
const proveedorDetalle = ref<Proveedor | null>(null)
const showSucursalesDialog = ref(false)
const showCreateSucursalDialog = ref(false)
const editandoSucursal = ref(false)
const proveedorSeleccionado = ref<Proveedor | null>(null)
const sucursales = ref<SucursalProveedor[]>([])
const tabActivo = ref('basica')

// Filters
const filtros = ref({
  busqueda: '',
  estado: null as boolean | null,
  clasificacion: null as string | null
})

const estadoOptions = [
  { label: 'Activo', value: true },
  { label: 'Inactivo', value: false }
]

const clasificacionOptions = [
  { label: 'Nacional', value: 'nacional' },
  { label: 'Internacional', value: 'internacional' },
  { label: 'Local', value: 'local' },
  { label: 'Estratégico', value: 'estrategico' },
  { label: 'Eventual', value: 'eventual' }
]

const monedaOptions = [
  { label: 'CLP - Peso Chileno', value: 'CLP' },
  { label: 'USD - Dólar Americano', value: 'USD' },
  { label: 'EUR - Euro', value: 'EUR' }
]

const formaPagoOptions = [
  { label: 'Efectivo', value: 'efectivo' },
  { label: 'Transferencia', value: 'transferencia' },
  { label: 'Cheque', value: 'cheque' },
  { label: 'Tarjeta de Crédito', value: 'tarjeta_credito' }
]

const metodoPagoOptions = [
  { label: 'Contado', value: 'contado' },
  { label: 'Crédito', value: 'credito' },
  { label: 'Parcialidades', value: 'parcialidades' }
]

// Pagination
const paginacion = ref({
  sortBy: 'id_proveedor',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formProveedor = ref<ProveedorCreate & { id_proveedor?: number }>({
  codigo_proveedor: '',
  nombre_proveedor: '',
  razon_social: '',

  // Datos fiscales
  rfc: '',
  giro_comercial: '',
  direccion_fiscal: '',
  ciudad_fiscal: '',
  estado_fiscal: '',
  codigo_postal_fiscal: '',
  pais_fiscal: '',

  // Información de contacto
  direccion: '',
  telefono: '',
  email: '',
  sitio_web: '',

  // Contacto principal
  contacto_principal: '',
  telefono_contacto_principal: '',
  email_contacto_principal: '',
  puesto_contacto: '',

  // Condiciones comerciales
  dias_credito: 0,
  limite_credito: undefined,
  descuento_comercial: undefined,
  descuento_pronto_pago: undefined,
  moneda_preferida: 'CLP',
  forma_pago_preferida: '',
  metodo_pago_preferido: '',

  // Información de entrega
  direccion_entrega: '',
  ciudad_entrega: '',
  estado_entrega: '',
  codigo_postal_entrega: '',
  pais_entrega: '',
  instrucciones_entrega: '',
  horario_entrega: '',
  contacto_recepcion: '',
  telefono_recepcion: '',

  // Información adicional
  observaciones: '',
  clasificacion: '',
  activo: true
})

const formSucursal = ref<SucursalProveedorCreate & { id_sucursal?: number }>({
  id_proveedor: 0,
  codigo_sucursal: '',
  nombre_sucursal: '',
  direccion: '',
  ciudad: '',
  estado: '',
  codigo_postal: '',
  pais: '',
  telefono: '',
  email: '',
  contacto: '',
  telefono_contacto: '',
  email_contacto: '',
  es_sucursal_principal: false,
  activo: true
})

// Table columns
const columnsProveedores = [
  {
    name: 'codigo_proveedor',
    required: true,
    label: 'Código',
    align: 'left' as const,
    field: 'codigo_proveedor',
    sortable: true
  },
  {
    name: 'nombre_proveedor',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_proveedor',
    sortable: true
  },
  {
    name: 'rut',
    label: 'RUT',
    align: 'left' as const,
    field: 'rfc'
  },
  {
    name: 'dias_credito',
    label: 'Crédito',
    align: 'center' as const,
    field: 'dias_credito',
    sortable: true
  },
  {
    name: 'limite_credito',
    label: 'Límite',
    align: 'right' as const,
    field: 'limite_credito',
    sortable: true
  },
  {
    name: 'contacto_principal',
    label: 'Contacto',
    align: 'left' as const,
    field: 'contacto_principal'
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

// Table columns for sucursales
const columnsSucursales = [
  {
    name: 'codigo_sucursal',
    required: true,
    label: 'Código',
    align: 'left' as const,
    field: 'codigo_sucursal',
    sortable: true
  },
  {
    name: 'nombre_sucursal',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_sucursal',
    sortable: true
  },
  {
    name: 'ciudad',
    label: 'Ciudad',
    align: 'left' as const,
    field: 'ciudad'
  },
  {
    name: 'telefono',
    label: 'Teléfono',
    align: 'left' as const,
    field: 'telefono'
  },
  {
    name: 'email',
    label: 'Email',
    align: 'left' as const,
    field: 'email'
  },
  {
    name: 'es_sucursal_principal',
    label: 'Tipo',
    align: 'center' as const,
    field: 'es_sucursal_principal',
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
const onRequestProveedores = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarProveedores()
}

const cargarProveedores = async () => {
  try {
    isLoading.value = true
    const params: any = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    if (filtros.value.estado !== null) {
      params.activo = filtros.value.estado
    }

    const response = await proveedorStore.obtenerProveedores(params)

    // Filtrar por búsqueda en el frontend si hay texto de búsqueda
    let proveedoresFiltered = response
    if (filtros.value.busqueda && filtros.value.busqueda.trim()) {
      const busqueda = filtros.value.busqueda.toLowerCase().trim()
      proveedoresFiltered = response.filter((proveedor: any) =>
        proveedor.codigo_proveedor.toLowerCase().includes(busqueda) ||
        proveedor.nombre_proveedor.toLowerCase().includes(busqueda) ||
        (proveedor.rfc && proveedor.rfc.toLowerCase().includes(busqueda)) ||
        (proveedor.razon_social && proveedor.razon_social.toLowerCase().includes(busqueda))
      )
    }

    // Filtrar por clasificación
    if (filtros.value.clasificacion) {
      proveedoresFiltered = proveedoresFiltered.filter((proveedor: any) =>
        proveedor.clasificacion === filtros.value.clasificacion
      )
    }

    proveedores.value = proveedoresFiltered

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar proveedores',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const buscarProveedores = async () => {
  paginacion.value.page = 1
  await cargarProveedores()
}

const limpiarFiltros = () => {
  filtros.value.busqueda = ''
  filtros.value.estado = null
  filtros.value.clasificacion = null
  buscarProveedores()
}

const abrirFormularioProveedor = () => {
  resetFormProveedor()
  showCreateProveedorDialog.value = true
}

const editarProveedor = (proveedor: Proveedor) => {
  editandoProveedor.value = true
  formProveedor.value = { ...proveedor }
  showCreateProveedorDialog.value = true
}

const verDetalleProveedor = async (proveedor: Proveedor) => {
  try {
    proveedorDetalle.value = await proveedorStore.obtenerProveedor(proveedor.id_proveedor)
    showDetalleDialog.value = true
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar detalles del proveedor',
      caption: error.message
    })
  }
}

const editarDesdeDetalle = () => {
  if (proveedorDetalle.value) {
    showDetalleDialog.value = false
    editarProveedor(proveedorDetalle.value)
  }
}

const guardarProveedor = async () => {
  try {
    isGuardando.value = true

    if (editandoProveedor.value && formProveedor.value.id_proveedor) {
      await proveedorStore.actualizarProveedor(formProveedor.value.id_proveedor, formProveedor.value)
      $q.notify({
        type: 'positive',
        message: 'Proveedor actualizado correctamente'
      })
    } else {
      await proveedorStore.crearProveedor(formProveedor.value)
      $q.notify({
        type: 'positive',
        message: 'Proveedor creado correctamente'
      })
    }

    showCreateProveedorDialog.value = false
    resetFormProveedor()
    await cargarProveedores()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar proveedor',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoProveedor = async (proveedor: Proveedor) => {
  try {
    if (proveedor.activo) {
      await proveedorStore.eliminarProveedor(proveedor.id_proveedor, false)
      $q.notify({
        type: 'positive',
        message: 'Proveedor desactivado'
      })
    } else {
      await proveedorStore.activarProveedor(proveedor.id_proveedor)
      $q.notify({
        type: 'positive',
        message: 'Proveedor activado'
      })
    }

    await cargarProveedores()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de proveedor',
      caption: error.message
    })
  }
}

const resetFormProveedor = () => {
  editandoProveedor.value = false
  tabActivo.value = 'basica'
  formProveedor.value = {
    codigo_proveedor: '',
    nombre_proveedor: '',
    razon_social: '',

    // Datos fiscales
    rfc: '',
    giro_comercial: '',
    direccion_fiscal: '',
    ciudad_fiscal: '',
    estado_fiscal: '',
    codigo_postal_fiscal: '',
    pais_fiscal: '',

    // Información de contacto
    direccion: '',
    telefono: '',
    email: '',
    sitio_web: '',

    // Contacto principal
    contacto_principal: '',
    telefono_contacto_principal: '',
    email_contacto_principal: '',
    puesto_contacto: '',

    // Condiciones comerciales
    dias_credito: 0,
    limite_credito: undefined,
    descuento_comercial: undefined,
    descuento_pronto_pago: undefined,
    moneda_preferida: 'CLP',
    forma_pago_preferida: '',
    metodo_pago_preferido: '',

    // Información de entrega
    direccion_entrega: '',
    ciudad_entrega: '',
    estado_entrega: '',
    codigo_postal_entrega: '',
    pais_entrega: '',
    instrucciones_entrega: '',
    horario_entrega: '',
    contacto_recepcion: '',
    telefono_recepcion: '',

    // Información adicional
    observaciones: '',
    clasificacion: '',
    activo: true
  }
}

// Sucursales methods
const verSucursales = async (proveedor: Proveedor) => {
  proveedorSeleccionado.value = proveedor
  await cargarSucursales(proveedor.id_proveedor)
  showSucursalesDialog.value = true
}

const cargarSucursales = async (proveedorId: number) => {
  try {
    isLoading.value = true
    const response = await proveedorStore.obtenerSucursalesPorProveedor(proveedorId)
    sucursales.value = response
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar sucursales',
      caption: error.message
    })
  } finally {
    isLoading.value = false
  }
}

const abrirFormularioSucursal = () => {
  resetFormSucursal()
  if (proveedorSeleccionado.value) {
    formSucursal.value.id_proveedor = proveedorSeleccionado.value.id_proveedor
  }
  showCreateSucursalDialog.value = true
}

const editarSucursal = (sucursal: SucursalProveedor) => {
  editandoSucursal.value = true
  formSucursal.value = { ...sucursal }
  showCreateSucursalDialog.value = true
}

const guardarSucursal = async () => {
  try {
    isGuardando.value = true

    if (editandoSucursal.value && formSucursal.value.id_sucursal) {
      await proveedorStore.actualizarSucursal(formSucursal.value.id_sucursal, formSucursal.value)
      $q.notify({
        type: 'positive',
        message: 'Sucursal actualizada correctamente'
      })
    } else {
      await proveedorStore.crearSucursal(formSucursal.value)
      $q.notify({
        type: 'positive',
        message: 'Sucursal creada correctamente'
      })
    }

    showCreateSucursalDialog.value = false
    resetFormSucursal()
    if (proveedorSeleccionado.value) {
      await cargarSucursales(proveedorSeleccionado.value.id_proveedor)
    }

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar sucursal',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoSucursal = async (sucursal: SucursalProveedor) => {
  try {
    if (sucursal.activo) {
      await proveedorStore.eliminarSucursal(sucursal.id_sucursal, false)
      $q.notify({
        type: 'positive',
        message: 'Sucursal desactivada'
      })
    } else {
      await proveedorStore.activarSucursal(sucursal.id_sucursal)
      $q.notify({
        type: 'positive',
        message: 'Sucursal activada'
      })
    }

    if (proveedorSeleccionado.value) {
      await cargarSucursales(proveedorSeleccionado.value.id_proveedor)
    }

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de sucursal',
      caption: error.message
    })
  }
}

const eliminarSucursal = async (sucursal: SucursalProveedor) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Está seguro de eliminar la sucursal "${sucursal.nombre_sucursal}"?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    try {
      await proveedorStore.eliminarSucursal(sucursal.id_sucursal, true)
      $q.notify({
        type: 'positive',
        message: 'Sucursal eliminada correctamente'
      })
      if (proveedorSeleccionado.value) {
        await cargarSucursales(proveedorSeleccionado.value.id_proveedor)
      }
    } catch (error: any) {
      $q.notify({
        type: 'negative',
        message: 'Error al eliminar sucursal',
        caption: error.message
      })
    }
  })
}

const establecerPrincipal = async (sucursal: SucursalProveedor) => {
  try {
    await proveedorStore.establecerSucursalPrincipal(sucursal.id_sucursal)
    $q.notify({
      type: 'positive',
      message: 'Sucursal establecida como principal'
    })
    if (proveedorSeleccionado.value) {
      await cargarSucursales(proveedorSeleccionado.value.id_proveedor)
    }
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al establecer sucursal principal',
      caption: error.message
    })
  }
}

const resetFormSucursal = () => {
  editandoSucursal.value = false
  formSucursal.value = {
    id_proveedor: proveedorSeleccionado.value?.id_proveedor || 0,
    codigo_sucursal: '',
    nombre_sucursal: '',
    direccion: '',
    ciudad: '',
    estado: '',
    codigo_postal: '',
    pais: '',
    telefono: '',
    email: '',
    contacto: '',
    telefono_contacto: '',
    email_contacto: '',
    es_sucursal_principal: false,
    activo: true
  }
}

// Lifecycle
onMounted(() => {
  cargarProveedores()
})
</script>