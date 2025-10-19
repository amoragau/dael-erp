<template>
  <q-page class="q-pa-lg">
    <!-- Page Header -->
    <div class="page-header">
      <div class="row items-center q-mb-sm">
        <q-icon name="settings" size="32px" color="primary" class="q-mr-md" />
        <h4 class="q-my-none text-h4 text-weight-light">Centro de <span class="text-weight-bold text-primary">Configuración</span></h4>
      </div>
      <p class="text-body2 text-grey-6 q-mb-none">Personaliza tu experiencia en el sistema</p>
    </div>

    <!-- Personal Preferences Card -->
    <div class="row justify-center">
      <div class="col-12 col-md-8 col-lg-6">
        <q-card class="shadow-light">
          <q-card-section class="bg-blue-1">
            <div class="text-h6 text-primary">
              <q-icon name="person_outline" class="q-mr-sm" />
              Preferencias Personales
            </div>
            <div class="text-caption text-grey-6">Configura tu experiencia personal en el sistema</div>
          </q-card-section>

          <q-card-section>
            <q-form @submit.prevent="guardarPreferencias" class="q-gutter-md">
              <!-- Theme and Display -->
              <div class="text-subtitle2 text-primary q-mb-sm">
                <q-icon name="palette" class="q-mr-xs" />
                Apariencia
              </div>

              <div class="row q-gutter-md">
                <div class="col-12">
                  <q-select
                    v-model="preferences.theme"
                    :options="themeOptions"
                    label="Tema del Sistema"
                    outlined
                    dense
                    emit-value
                    map-options
                  >
                    <template v-slot:prepend>
                      <q-icon name="brush" color="primary" />
                    </template>
                  </q-select>
                </div>
              </div>

              <!-- Notifications -->
              <q-separator class="q-my-md" />

              <div class="text-subtitle2 text-primary q-mb-sm">
                <q-icon name="notifications" class="q-mr-xs" />
                Notificaciones
              </div>

              <div class="column q-gutter-sm">
                <q-toggle
                  v-model="preferences.emailNotifications"
                  label="Notificaciones por correo electrónico"
                  color="primary"
                />
                <q-toggle
                  v-model="preferences.pushNotifications"
                  label="Notificaciones push"
                  color="primary"
                />
                <q-toggle
                  v-model="preferences.soundNotifications"
                  label="Sonidos de notificación"
                  color="primary"
                />
                <q-toggle
                  v-model="preferences.alertasInventario"
                  label="Alertas de inventario bajo"
                  color="primary"
                />
              </div>

              <!-- Dashboard -->
              <q-separator class="q-my-md" />

              <div class="text-subtitle2 text-primary q-mb-sm">
                <q-icon name="dashboard" class="q-mr-xs" />
                Dashboard
              </div>

              <div class="row q-gutter-md">
                <div class="col-12 col-md-6">
                  <q-select
                    v-model="preferences.defaultView"
                    :options="defaultViewOptions"
                    label="Vista Inicial"
                    outlined
                    dense
                    emit-value
                    map-options
                    hint="Página que se muestra al iniciar sesión"
                  >
                    <template v-slot:prepend>
                      <q-icon name="home" color="primary" />
                    </template>
                  </q-select>
                </div>

                <div class="col-12 col-md-6">
                  <q-input
                    v-model.number="preferences.itemsPerPage"
                    label="Elementos por página"
                    type="number"
                    outlined
                    dense
                    min="10"
                    max="100"
                    step="10"
                    hint="Número de registros en tablas"
                  >
                    <template v-slot:prepend>
                      <q-icon name="view_list" color="primary" />
                    </template>
                  </q-input>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="row q-gutter-sm q-mt-lg">
                <q-btn
                  type="submit"
                  color="primary"
                  unelevated
                  icon="save"
                  label="Guardar Preferencias"
                  :loading="loading"
                  class="rounded-borders"
                />

                <q-btn
                  @click="resetPreferences"
                  color="grey-6"
                  unelevated
                  icon="restart_alt"
                  label="Restaurar Predeterminados"
                  class="rounded-borders"
                />
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useQuasar } from 'quasar'

// Stores and composables
const $q = useQuasar()

// State
const loading = ref(false)

// User Preferences
const preferences = reactive({
  // Appearance
  theme: 'light',

  // Notifications
  emailNotifications: true,
  pushNotifications: true,
  soundNotifications: false,
  alertasInventario: true,

  // Dashboard
  defaultView: 'dashboard',
  itemsPerPage: 20
})

// Options
const themeOptions = [
  { label: 'Claro', value: 'light' },
  { label: 'Oscuro', value: 'dark' }
]

const defaultViewOptions = [
  { label: 'Dashboard', value: 'dashboard' },
  { label: 'Productos', value: 'productos' },
  { label: 'Inventario', value: 'stock-bodega' },
  { label: 'Órdenes de Compra', value: 'ordenes-compra' }
]

// Methods
const loadPreferences = () => {
  try {
    const savedPrefs = localStorage.getItem('userPreferences')
    if (savedPrefs) {
      Object.assign(preferences, JSON.parse(savedPrefs))
    }
  } catch (error) {
    console.error('Error loading preferences:', error)
  }
}

const guardarPreferencias = async () => {
  loading.value = true

  try {
    // Save to localStorage
    localStorage.setItem('userPreferences', JSON.stringify(preferences))

    // Apply theme changes immediately
    if (preferences.theme === 'dark') {
      document.body.classList.add('dark')
    } else {
      document.body.classList.remove('dark')
    }

    $q.notify({
      type: 'positive',
      message: 'Preferencias guardadas correctamente',
      position: 'top-right'
    })
  } catch (error) {
    console.error('Error saving preferences:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al guardar las preferencias',
      position: 'top-right'
    })
  } finally {
    loading.value = false
  }
}

const resetPreferences = () => {
  $q.dialog({
    title: 'Restaurar Configuración',
    message: '¿Estás seguro de que deseas restaurar todas las preferencias a los valores predeterminados?',
    cancel: true,
    persistent: true,
    color: 'primary'
  }).onOk(() => {
    Object.assign(preferences, {
      theme: 'light',
      emailNotifications: true,
      pushNotifications: true,
      soundNotifications: false,
      alertasInventario: true,
      defaultView: 'dashboard',
      itemsPerPage: 20
    })

    localStorage.removeItem('userPreferences')

    $q.notify({
      type: 'info',
      message: 'Preferencias restauradas a valores predeterminados',
      position: 'top-right'
    })
  })
}

// Lifecycle
onMounted(() => {
  loadPreferences()
})
</script>

<style scoped>
.page-header {
  background: linear-gradient(135deg, var(--primary-50) 0%, var(--grey-50) 100%);
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
}

.status-badge {
  padding: 4px 12px !important;
  border-radius: 20px !important;
  font-weight: 600 !important;
  font-size: 0.75rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
}
</style>