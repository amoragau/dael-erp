<template>
  <q-page class="flex flex-center bg-grey-2">
    <div class="login-container">
      <q-card class="login-card q-pa-lg">
        <q-card-section class="text-center">
          <div class="text-h4 text-primary q-mb-md">ERP DAEL</div>
          <div class="text-h6 q-mb-lg">Iniciar Sesión</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="handleLogin" class="q-gutter-md">
            <q-input
              v-model="username"
              label="Usuario"
              outlined
              dense
              :rules="[val => !!val || 'Usuario es requerido']"
              :disable="authStore.isLoading"
            >
              <template v-slot:prepend>
                <q-icon name="person" />
              </template>
            </q-input>

            <q-input
              v-model="password"
              label="Contraseña"
              type="password"
              outlined
              dense
              :rules="[val => !!val || 'Contraseña es requerida']"
              :disable="authStore.isLoading"
            >
              <template v-slot:prepend>
                <q-icon name="lock" />
              </template>
            </q-input>

            <div class="row q-mt-md">
              <q-checkbox
                v-model="rememberMe"
                label="Recordarme"
                :disable="authStore.isLoading"
              />
            </div>

            <div v-if="authStore.error" class="text-negative q-mt-md">
              <q-icon name="error" class="q-mr-sm" />
              {{ authStore.error }}
            </div>

            <q-btn
              type="submit"
              label="Iniciar Sesión"
              color="primary"
              class="full-width q-mt-lg"
              :loading="authStore.isLoading"
              :disable="!isFormValid"
            />
          </q-form>
        </q-card-section>

        <q-card-section class="text-center">
          <div class="text-caption text-grey-6">
            ¿Olvidaste tu contraseña?
            <a href="#" class="text-primary">Recuperar</a>
          </div>
        </q-card-section>
      </q-card>

      <!-- Backend connection info -->
      <q-card class="demo-card q-mt-md q-pa-md bg-blue-1">
        <q-card-section>
          <div class="text-subtitle2 text-primary q-mb-sm">
            <q-icon name="info" class="q-mr-sm" />
            Información de conexión:
          </div>
          <div class="text-body2">
            <strong>Backend:</strong> {{ apiBaseUrl }}<br>
            <strong>Nota:</strong> Asegúrate de que el backend esté ejecutándose
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
// @ts-ignore
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Form data
const username = ref('')
const password = ref('')
const rememberMe = ref(false)

// Computed
const isFormValid = computed(() =>
  username.value.length > 0 && password.value.length > 0
)

// Methods
const handleLogin = async () => {
  if (!isFormValid.value) return

  const success = await authStore.login({
    username: username.value,
    password: password.value
  })

  if (success) {
    $q.notify({
      type: 'positive',
      message: `¡Bienvenido, ${authStore.userName}!`,
      position: 'top'
    })

    // Redirect to home or intended route
    const redirectTo = router.currentRoute.value.query.redirect as string || '/'
    router.push(redirectTo)
  } else {
    $q.notify({
      type: 'negative',
      message: authStore.error || 'Error al iniciar sesión',
      position: 'top'
    })
  }
}

// Auto-fill demo credentials
const fillDemoCredentials = () => {
  username.value = 'admin'
  password.value = 'admin123'
}
</script>

<style scoped>
.login-container {
  width: 100%;
  max-width: 400px;
}

.login-card {
  width: 100%;
  min-height: 400px;
}

.demo-card {
  width: 100%;
}

@media (max-width: 600px) {
  .login-container {
    padding: 16px;
  }
}
</style>