<template>
  <q-page class="flex flex-center">
    <div class="text-center">
      <h1 class="text-h3 q-mb-md">Acerca de ERP DAEL</h1>
      <p class="text-body1 q-mb-lg">
        Este es un sistema ERP desarrollado con Vue 3, TypeScript, Pinia, Vue Router, Axios y Quasar.
      </p>

      <q-list bordered separator>
        <q-item>
          <q-item-section avatar>
            <q-icon color="primary" name="check_circle" />
          </q-item-section>
          <q-item-section>Vue 3 con Composition API</q-item-section>
        </q-item>

        <q-item>
          <q-item-section avatar>
            <q-icon color="primary" name="check_circle" />
          </q-item-section>
          <q-item-section>TypeScript para tipado estático</q-item-section>
        </q-item>

        <q-item>
          <q-item-section avatar>
            <q-icon color="primary" name="check_circle" />
          </q-item-section>
          <q-item-section>Pinia para manejo de estado</q-item-section>
        </q-item>

        <q-item>
          <q-item-section avatar>
            <q-icon color="primary" name="check_circle" />
          </q-item-section>
          <q-item-section>Vue Router para navegación</q-item-section>
        </q-item>

        <q-item>
          <q-item-section avatar>
            <q-icon color="primary" name="check_circle" />
          </q-item-section>
          <q-item-section>Axios para peticiones HTTP</q-item-section>
        </q-item>

        <q-item>
          <q-item-section avatar>
            <q-icon color="primary" name="check_circle" />
          </q-item-section>
          <q-item-section>Quasar Framework para UI</q-item-section>
        </q-item>
      </q-list>

      <q-btn
        color="primary"
        label="Volver al inicio"
        @click="$router.push('/')"
        class="q-mt-lg"
      />
    </div>
  </q-page>
</template>

<script setup lang="ts">
// No setup code needed for this component
</script>