<template>
  <q-page class="flex flex-center">
    <div class="text-center">
      <h1 class="text-h2 q-mb-md">Bienvenido a ERP DAEL</h1>
      <p class="text-h6 q-mb-lg">Sistema de gestión empresarial</p>

      <div class="row q-gutter-md justify-center">
        <q-btn
          color="primary"
          label="Dashboard"
          icon="dashboard"
          @click="$router.push('/dashboard')"
          size="lg"
          class="q-ma-sm"
        />

        <q-btn
          color="secondary"
          label="Acerca de"
          icon="info"
          @click="$router.push('/about')"
          size="lg"
          class="q-ma-sm"
        />
      </div>

      <q-card class="q-mt-lg q-pa-md bg-blue-1" style="max-width: 500px">
        <q-card-section>
          <div class="text-h6 text-primary q-mb-sm">
            <q-icon name="info" class="q-mr-sm" />
            Sistema ERP
          </div>
          <p class="text-body2">
            Gestiona tu inventario, clientes, proveedores y más desde una plataforma centralizada.
          </p>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
// Simple home page component
</script>