<template>
  <q-page class="flex flex-center bg-grey-2">
    <q-card class="q-pa-lg">
      <q-card-section class="text-center">
        <div class="text-h4 text-primary q-mb-md">ERP DAEL</div>
        <div class="text-h6 q-mb-lg">Iniciar Sesión</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="handleLogin">
          <q-input
            v-model="username"
            label="Usuario"
            outlined
            class="q-mb-md"
          />

          <q-input
            v-model="password"
            label="Contraseña"
            type="password"
            outlined
            class="q-mb-md"
          />

          <q-btn
            type="submit"
            label="Iniciar Sesión"
            color="primary"
            class="full-width"
          />
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
// @ts-ignore
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('admin')
const password = ref('admin123')

const handleLogin = () => {
  // Simple mock login
  if (username.value === 'admin' && password.value === 'admin123') {
    router.push('/')
  } else {
    alert('Credenciales incorrectas')
  }
}
</script>