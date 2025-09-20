<template>
  <q-page class="flex flex-center">
    <div class="text-center">
      <div class="text-h1 text-grey-5">404</div>
      <div class="text-h4 q-mb-md">Página no encontrada</div>
      <p class="text-body1 q-mb-lg">
        La página que buscas no existe o ha sido movida.
      </p>
      <q-btn
        color="primary"
        label="Volver al inicio"
        @click="$router.push('/')"
      />
    </div>
  </q-page>
</template>

<script setup lang="ts">
// No setup code needed for this component
</script>