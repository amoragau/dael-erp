<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-xl">
        <div>
          <div class="row items-center q-mb-sm">
            <q-icon name="people" size="32px" color="primary" class="q-mr-md" />
            <div>
              <h4 class="q-my-none text-h4 text-weight-light">Información Comercial de <span class="text-weight-bold text-primary">Clientes</span></h4>
              <p class="text-grey-6 q-mb-none text-body2">Gestión integral de clientes con datos fiscales y condiciones comerciales</p>
            </div>
          </div>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nuevo Cliente"
          @click="abrirFormularioCliente"
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
                v-model="filtros.tipo"
                :options="tipoClienteOptions"
                label="Tipo Cliente"
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
                @click="buscarClientes"
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

      <!-- Clients Table -->
      <q-table
        :rows="clientes"
        :columns="columnsClientes"
        :loading="isLoading"
        :pagination="paginacion"
        row-key="id_cliente"
        flat
        bordered
        @request="onRequestClientes"
      >
        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'green' : 'red'"
              :label="props.value ? 'Activo' : 'Inactivo'"
            />
          </q-td>
        </template>
        <template v-slot:body-cell-tipo_cliente="props">
          <q-td :props="props">
            <q-badge
              :color="getTipoClienteColor(props.value)"
              :label="formatTipoCliente(props.value)"
              text-color="white"
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
              ${{ Number(props.value).toLocaleString() }}
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
              @click="verDetalleCliente(props.row as Cliente)"
            >
              <q-tooltip>Ver Detalles</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="edit"
              color="primary"
              size="sm"
              @click="editarCliente(props.row as Cliente)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'negative' : 'positive'"
              size="sm"
              @click="toggleEstadoCliente(props.row as Cliente)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit Cliente Dialog -->
      <q-dialog v-model="showCreateClienteDialog" persistent>
        <q-card style="min-width: 1200px; max-width: 1400px; max-height: 90vh">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">{{ editandoCliente ? 'Editar' : 'Nuevo' }} Cliente</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section class="q-pt-none" style="max-height: calc(90vh - 120px);">
            <q-form @submit="guardarCliente">
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
                            v-model="formCliente.codigo_cliente"
                            label="Código *"
                            outlined
                            dense
                            maxlength="20"
                            :rules="[val => !!val || 'El código es requerido']"
                            hint="Código único del cliente"
                          />
                        </div>
                        <div class="col-12 col-md-7">
                          <q-input
                            v-model="formCliente.nombre_cliente"
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
                            v-model="formCliente.razon_social"
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
                          <q-select
                            v-model="formCliente.tipo_cliente"
                            :options="tipoClienteOptions"
                            label="Tipo Cliente *"
                            outlined
                            dense
                            emit-value
                            map-options
                            :rules="[val => !!val || 'El tipo es requerido']"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formCliente.telefono_principal"
                            label="Teléfono Principal"
                            outlined
                            dense
                            mask="(###) ###-####"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-6">
                          <q-input
                            v-model="formCliente.email_principal"
                            label="Email Corporativo"
                            type="email"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formCliente.sitio_web"
                            label="Sitio Web"
                            outlined
                            dense
                            hint="ej: www.empresa.com"
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formCliente.direccion_comercial"
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
                            v-model="formCliente.activo"
                            label="Cliente Activo"
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
                            v-model="formCliente.rut"
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
                            v-model="formCliente.giro_comercial"
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
                            v-model="formCliente.direccion_fiscal"
                            label="Dirección Fiscal"
                            outlined
                            dense
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formCliente.ciudad_fiscal"
                            label="Ciudad"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-4">
                          <q-input
                            v-model="formCliente.estado_fiscal"
                            label="Estado/Región"
                            outlined
                            dense
                          />
                        </div>
                        <div class="col-12 col-md-3">
                          <q-input
                            v-model="formCliente.codigo_postal_fiscal"
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
                            v-model="formCliente.pais_fiscal"
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
                            v-model.number="formCliente.dias_credito"
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
                            v-model.number="formCliente.limite_credito"
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
                            v-model="formCliente.moneda_preferida"
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
                            v-model.number="formCliente.descuento_comercial"
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
                            v-model="formCliente.condiciones_pago"
                            label="Condiciones de Pago"
                            outlined
                            dense
                            hint="ej: 30 días, Contado, etc."
                          />
                        </div>
                      </div>

                      <div class="row q-gutter-md q-mt-sm">
                        <div class="col-12">
                          <q-input
                            v-model="formCliente.observaciones"
                            label="Observaciones Generales"
                            outlined
                            type="textarea"
                            rows="3"
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
                            v-model="formCliente.contacto_principal"
                            label="Nombre del Contacto"
                            outlined
                            dense
                            maxlength="200"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formCliente.puesto_contacto"
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
                            v-model="formCliente.telefono_contacto"
                            label="Teléfono Directo"
                            outlined
                            dense
                            mask="(###) ###-####"
                          />
                        </div>
                        <div class="col-12 col-md-5">
                          <q-input
                            v-model="formCliente.email_contacto"
                            label="Email Directo"
                            type="email"
                            outlined
                            dense
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
              label="Guardar Cliente"
              @click="guardarCliente"
              :loading="isGuardando"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Client Detail Dialog -->
      <q-dialog v-model="showDetalleDialog" persistent>
        <q-card style="min-width: 800px; max-width: 1000px">
          <q-card-section class="row items-center">
            <div class="text-h6">Detalles del Cliente</div>
            <q-space />
            <q-btn icon="close" flat round dense v-close-popup />
          </q-card-section>

          <q-card-section v-if="clienteDetalle">
            <div class="row q-col-gutter-md">
              <!-- Información Básica -->
              <div class="col-12 col-md-6">
                <q-list bordered separator>
                  <q-item-label header>Información Comercial</q-item-label>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Código</q-item-label>
                      <q-item-label>{{ clienteDetalle.codigo_cliente }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Nombre Comercial</q-item-label>
                      <q-item-label>{{ clienteDetalle.nombre_cliente }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>RUT</q-item-label>
                      <q-item-label>{{ clienteDetalle.rut || '-' }}</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Tipo Cliente</q-item-label>
                      <q-item-label>{{ formatTipoCliente(clienteDetalle.tipo_cliente) }}</q-item-label>
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
                          :color="diasCreditoDetalle > 0 ? 'blue' : 'grey'"
                          :label="diasCreditoDetalle > 0 ? `${diasCreditoDetalle} días` : 'Contado'"
                        />
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Límite de Crédito</q-item-label>
                      <q-item-label>
                        <span v-if="clienteDetalle.limite_credito && clienteDetalle.limite_credito > 0">
                          ${{ Number(clienteDetalle.limite_credito).toLocaleString() }}
                        </span>
                        <span v-else>Sin límite</span>
                      </q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Descuento Comercial</q-item-label>
                      <q-item-label>{{ clienteDetalle.descuento_comercial || 0 }}%</q-item-label>
                    </q-item-section>
                  </q-item>
                  <q-item>
                    <q-item-section>
                      <q-item-label caption>Moneda Preferida</q-item-label>
                      <q-item-label>{{ clienteDetalle.moneda_preferida || 'CLP' }}</q-item-label>
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
                            <q-item v-if="clienteDetalle.contacto_principal">
                              <q-item-section>
                                <q-item-label caption>Nombre</q-item-label>
                                <q-item-label>{{ clienteDetalle.contacto_principal }}</q-item-label>
                              </q-item-section>
                            </q-item>
                            <q-item v-if="clienteDetalle.puesto_contacto">
                              <q-item-section>
                                <q-item-label caption>Puesto</q-item-label>
                                <q-item-label>{{ clienteDetalle.puesto_contacto }}</q-item-label>
                              </q-item-section>
                            </q-item>
                          </q-list>
                        </div>
                        <div class="col-12 col-md-6">
                          <q-list dense>
                            <q-item v-if="clienteDetalle.telefono_contacto">
                              <q-item-section>
                                <q-item-label caption>Teléfono</q-item-label>
                                <q-item-label>{{ clienteDetalle.telefono_contacto }}</q-item-label>
                              </q-item-section>
                            </q-item>
                            <q-item v-if="clienteDetalle.email_contacto">
                              <q-item-section>
                                <q-item-label caption>Email</q-item-label>
                                <q-item-label>{{ clienteDetalle.email_contacto }}</q-item-label>
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
              v-if="clienteDetalle"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useClienteStore, type Cliente, type ClienteCreate, type ClienteUpdate } from '@/stores/clientes'

// Composables
const $q = useQuasar()
const clienteStore = useClienteStore()

// Reactive data
const clientes = computed(() => clienteStore.clientes)
const isLoading = computed(() => clienteStore.isLoading)
const isGuardando = ref(false)
const showCreateClienteDialog = ref(false)
const editandoCliente = ref(false)
const showDetalleDialog = ref(false)
const clienteDetalle = ref<Cliente | null>(null)
const diasCreditoDetalle = computed(() => clienteDetalle.value?.dias_credito ?? 0)
const tabActivo = ref('basica')

// Filters
const filtros = ref({
  busqueda: '',
  estado: null as boolean | null,
  tipo: null as string | null
})

const estadoOptions = [
  { label: 'Activo', value: true },
  { label: 'Inactivo', value: false }
]

const tipoClienteOptions = [
  { label: 'Gobierno', value: 'gobierno' },
  { label: 'Privado', value: 'privado' },
  { label: 'Constructora', value: 'constructora' },
  { label: 'Distribuidor', value: 'distribuidor' }
]

const monedaOptions = [
  { label: 'CLP - Peso Chileno', value: 'CLP' },
  { label: 'USD - Dólar Americano', value: 'USD' },
  { label: 'EUR - Euro', value: 'EUR' }
]

// Pagination
const paginacion = ref({
  sortBy: 'id_cliente',
  descending: false,
  page: 1,
  rowsPerPage: 25,
  rowsNumber: 0
})

// Forms
const formCliente = ref<ClienteCreate & { id_cliente?: number }>({
  codigo_cliente: '',
  nombre_cliente: '',
  razon_social: '',
  tipo_cliente: 'privado',
  rut: '',
  giro_comercial: '',
  direccion_fiscal: '',
  ciudad_fiscal: '',
  estado_fiscal: '',
  codigo_postal_fiscal: '',
  pais_fiscal: 'Chile',
  direccion_comercial: '',
  ciudad_comercial: '',
  estado_comercial: '',
  codigo_postal_comercial: '',
  pais_comercial: 'Chile',
  telefono_principal: '',
  email_principal: '',
  sitio_web: '',
  contacto_principal: '',
  telefono_contacto: '',
  email_contacto: '',
  puesto_contacto: '',
  condiciones_pago: '',
  dias_credito: 30,
  limite_credito: 0,
  descuento_comercial: 0,
  moneda_preferida: 'CLP',
  observaciones: '',
  activo: true
})

// Table columns
const columnsClientes = [
  {
    name: 'codigo_cliente',
    required: true,
    label: 'Código',
    align: 'left' as const,
    field: 'codigo_cliente',
    sortable: true
  },
  {
    name: 'nombre_cliente',
    required: true,
    label: 'Nombre',
    align: 'left' as const,
    field: 'nombre_cliente',
    sortable: true
  },
  {
    name: 'rut',
    label: 'RUT',
    align: 'left' as const,
    field: 'rut'
  },
  {
    name: 'tipo_cliente',
    label: 'Tipo',
    align: 'center' as const,
    field: 'tipo_cliente',
    sortable: true
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

// Methods
const onRequestClientes = async (props: any) => {
  const { page, rowsPerPage, sortBy, descending } = props.pagination

  paginacion.value.page = page
  paginacion.value.rowsPerPage = rowsPerPage
  paginacion.value.sortBy = sortBy
  paginacion.value.descending = descending

  await cargarClientes()
}

const cargarClientes = async () => {
  try {
    const params: any = {
      skip: (paginacion.value.page - 1) * paginacion.value.rowsPerPage,
      limit: paginacion.value.rowsPerPage
    }

    if (filtros.value.estado !== null) {
      params.activo = filtros.value.estado
    }

    await clienteStore.obtenerClientes(params)

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar clientes',
      caption: error.message
    })
  }
}

const buscarClientes = async () => {
  paginacion.value.page = 1
  await cargarClientes()
}

const limpiarFiltros = () => {
  filtros.value.busqueda = ''
  filtros.value.estado = null
  filtros.value.tipo = null
  buscarClientes()
}

const abrirFormularioCliente = () => {
  resetFormCliente()
  showCreateClienteDialog.value = true
}

const editarCliente = (cliente: Cliente) => {
  editandoCliente.value = true
  formCliente.value = { ...cliente }
  showCreateClienteDialog.value = true
}

const verDetalleCliente = async (cliente: Cliente) => {
  try {
    clienteDetalle.value = await clienteStore.obtenerCliente(cliente.id_cliente)
    showDetalleDialog.value = true
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cargar detalles del cliente',
      caption: error.message
    })
  }
}

const editarDesdeDetalle = () => {
  if (clienteDetalle.value) {
    showDetalleDialog.value = false
    editarCliente(clienteDetalle.value)
  }
}

const guardarCliente = async () => {
  try {
    isGuardando.value = true

    if (editandoCliente.value && formCliente.value.id_cliente) {
      await clienteStore.actualizarCliente(formCliente.value.id_cliente, formCliente.value)
      $q.notify({
        type: 'positive',
        message: 'Cliente actualizado correctamente'
      })
    } else {
      await clienteStore.crearCliente(formCliente.value)
      $q.notify({
        type: 'positive',
        message: 'Cliente creado correctamente'
      })
    }

    showCreateClienteDialog.value = false
    resetFormCliente()
    await cargarClientes()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al guardar cliente',
      caption: error.message
    })
  } finally {
    isGuardando.value = false
  }
}

const toggleEstadoCliente = async (cliente: Cliente) => {
  try {
    if (cliente.activo) {
      await clienteStore.eliminarCliente(cliente.id_cliente, false)
      $q.notify({
        type: 'positive',
        message: 'Cliente desactivado'
      })
    } else {
      await clienteStore.activarCliente(cliente.id_cliente)
      $q.notify({
        type: 'positive',
        message: 'Cliente activado'
      })
    }

    await cargarClientes()

  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: 'Error al cambiar estado de cliente',
      caption: error.message
    })
  }
}

const resetFormCliente = () => {
  editandoCliente.value = false
  tabActivo.value = 'basica'
  formCliente.value = {
    codigo_cliente: '',
    nombre_cliente: '',
    razon_social: '',
    tipo_cliente: 'privado',
    rut: '',
    giro_comercial: '',
    direccion_fiscal: '',
    ciudad_fiscal: '',
    estado_fiscal: '',
    codigo_postal_fiscal: '',
    pais_fiscal: 'Chile',
    direccion_comercial: '',
    ciudad_comercial: '',
    estado_comercial: '',
    codigo_postal_comercial: '',
    pais_comercial: 'Chile',
    telefono_principal: '',
    email_principal: '',
    sitio_web: '',
    contacto_principal: '',
    telefono_contacto: '',
    email_contacto: '',
    puesto_contacto: '',
    condiciones_pago: '',
    dias_credito: 30,
    limite_credito: 0,
    descuento_comercial: 0,
    moneda_preferida: 'CLP',
    observaciones: '',
    activo: true
  }
}

// Utility functions
const formatTipoCliente = (tipo: string) => {
  const tipos: Record<string, string> = {
    gobierno: 'Gobierno',
    privado: 'Privado',
    constructora: 'Constructora',
    distribuidor: 'Distribuidor'
  }
  return tipos[tipo] || tipo
}

const getTipoClienteColor = (tipo: string) => {
  const colores: Record<string, string> = {
    gobierno: 'warning',
    privado: 'primary',
    constructora: 'positive',
    distribuidor: 'info'
  }
  return colores[tipo] || 'primary'
}

// Lifecycle
onMounted(() => {
  cargarClientes()
})
</script>
