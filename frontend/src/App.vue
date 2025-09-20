<template>
  <!-- Login layout (no header/drawer) -->
  <q-layout v-if="$route.meta.layout === 'blank'" view="lHh Lpr lFf">
    <q-page-container>
      <RouterView />
    </q-page-container>
  </q-layout>

  <!-- Main layout (with header and drawer) -->
  <q-layout v-else view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          ERP DAEL
        </q-toolbar-title>

        <!-- User menu -->
        <q-btn-dropdown
          v-if="authStore.isAuthenticated"
          flat
          icon="account_circle"
          :label="authStore.userName"
        >
          <q-list>
            <q-item clickable v-close-popup @click="goToProfile">
              <q-item-section avatar>
                <q-icon name="person" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Perfil</q-item-label>
              </q-item-section>
            </q-item>

            <q-item clickable v-close-popup @click="goToSettings">
              <q-item-section avatar>
                <q-icon name="settings" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Configuración</q-item-label>
              </q-item-section>
            </q-item>

            <q-separator />

            <q-item clickable v-close-popup @click="logout">
              <q-item-section avatar>
                <q-icon name="logout" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Cerrar Sesión</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-if="authStore.isAuthenticated"
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label header>
          Navegación
        </q-item-label>

        <q-item clickable :to="{ name: 'dashboard' }" exact>
          <q-item-section avatar>
            <q-icon name="dashboard" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Dashboard</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable :to="{ name: 'home' }" exact>
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Inicio</q-item-label>
          </q-item-section>
        </q-item>

        <q-expansion-item
          icon="inventory"
          label="Inventario"
          default-opened
        >
          <q-item clickable :inset-level="1" :to="{ name: 'productos' }">
            <q-item-section avatar>
              <q-icon name="category" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Productos</q-item-label>
            </q-item-section>
          </q-item>

          <q-item clickable :inset-level="1" :to="{ name: 'categorias' }">
            <q-item-section avatar>
              <q-icon name="label" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Categorías</q-item-label>
            </q-item-section>
          </q-item>

          <q-item clickable :inset-level="1" :to="{ name: 'bodegas' }">
            <q-item-section avatar>
              <q-icon name="warehouse" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Bodegas</q-item-label>
            </q-item-section>
          </q-item>
        </q-expansion-item>

        <q-expansion-item
          icon="construction"
          label="Obras y Proyectos"
        >
          <q-item clickable :inset-level="1" :to="{ name: 'obras' }">
            <q-item-section avatar>
              <q-icon name="engineering" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Obras</q-item-label>
            </q-item-section>
          </q-item>
        </q-expansion-item>

        <q-expansion-item
          icon="settings"
          label="Configuraciones"
        >
          <q-item clickable :inset-level="1" :to="{ name: 'proveedores' }">
            <q-item-section avatar>
              <q-icon name="business" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Proveedores</q-item-label>
            </q-item-section>
          </q-item>

          <q-item clickable :inset-level="1">
            <q-item-section avatar>
              <q-icon name="people" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Clientes</q-item-label>
            </q-item-section>
          </q-item>

        </q-expansion-item>

        <!-- Admin only section -->
        <template v-if="authStore.isAdmin">
          <q-separator class="q-my-md" />

          <q-item-label header>
            Administración
          </q-item-label>

          <q-item clickable :to="{ name: 'users' }" exact>
            <q-item-section avatar>
              <q-icon name="people" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Usuarios</q-item-label>
            </q-item-section>
          </q-item>
        </template>

        <q-item clickable :to="{ name: 'about' }" exact>
          <q-item-section avatar>
            <q-icon name="info" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Acerca de</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <RouterView />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterView } from 'vue-router'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const $q = useQuasar()
const authStore = useAuthStore()

const leftDrawerOpen = ref(false)

const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

const goToProfile = () => {
  // TODO: Navigate to profile page
  $q.notify({
    message: 'Función de perfil pendiente de implementar',
    type: 'info'
  })
}

const goToSettings = () => {
  // TODO: Navigate to settings page
  $q.notify({
    message: 'Función de configuración pendiente de implementar',
    type: 'info'
  })
}

const logout = () => {
  $q.dialog({
    title: 'Confirmar',
    message: '¿Estás seguro de que quieres cerrar sesión?',
    cancel: true,
    persistent: true
  }).onOk(() => {
    authStore.logout()
    $q.notify({
      message: 'Sesión cerrada exitosamente',
      type: 'positive'
    })
    router.push({ name: 'login' })
  })
}
</script>