<template>
  <!-- Login layout (no header/drawer) -->
  <q-layout v-if="$route.meta.layout === 'blank'" view="lHh Lpr lFf">
    <q-page-container>
      <RouterView />
    </q-page-container>
  </q-layout>

  <!-- Main layout (with header and drawer) -->
  <q-layout v-else view="lHh Lpr lFf" class="bg-grey-1">
    <q-header elevated class="bg-white text-primary shadow-2">
      <q-toolbar class="q-py-sm">
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
          class="q-mr-sm"
          color="primary"
        />

        <div class="row items-center q-mr-md">
          <q-icon name="business" size="28px" color="primary" class="q-mr-sm" />
          <q-toolbar-title class="text-h5 text-weight-light text-primary">
            ERP <span class="text-weight-bold">DAEL</span>
          </q-toolbar-title>
        </div>

        <q-space />

        <!-- User menu -->
        <q-btn-dropdown
          v-if="authStore.isAuthenticated"
          flat
          no-caps
          class="q-px-md q-py-xs"
          color="primary"
        >
          <template v-slot:label>
            <div class="row items-center no-wrap">
              <q-avatar size="32px" color="primary" text-color="white" class="q-mr-sm">
                <q-icon name="person" />
              </q-avatar>
              <div class="text-left">
                <div class="text-weight-medium">{{ authStore.userName }}</div>
                <div class="text-caption text-grey-6">{{ authStore.user?.email || 'Usuario' }}</div>
              </div>
            </div>
          </template>

          <q-list style="min-width: 200px">
            <q-item clickable v-close-popup @click="goToProfile">
              <q-item-section avatar>
                <q-icon name="account_circle" color="primary" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Mi Perfil</q-item-label>
                <q-item-label caption>Ver información personal</q-item-label>
              </q-item-section>
            </q-item>

            <q-item clickable v-close-popup @click="goToSettings">
              <q-item-section avatar>
                <q-icon name="settings" color="primary" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Configuración</q-item-label>
                <q-item-label caption>Preferencias del sistema</q-item-label>
              </q-item-section>
            </q-item>

            <q-separator class="q-my-sm" />

            <q-item clickable v-close-popup @click="logout">
              <q-item-section avatar>
                <q-icon name="logout" color="negative" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Cerrar Sesión</q-item-label>
                <q-item-label caption>Salir del sistema</q-item-label>
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
      :width="280"
      class="bg-white"
    >
      <div class="q-pa-md bg-blue-1">
        <div class="text-h6 text-primary text-weight-light">Navegación</div>
        <div class="text-caption text-grey-6">Sistema de gestión empresarial</div>
      </div>

      <q-list class="q-pa-md">
        <!-- Dashboard -->
        <q-item
          clickable
          :to="{ name: 'dashboard' }"
          exact
          class="rounded-borders q-mb-xs"
          active-class="bg-blue-1 text-primary"
        >
          <q-item-section avatar class="min-width-none">
            <q-icon name="dashboard" size="20px" />
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-weight-medium">Dashboard</q-item-label>
            <q-item-label caption>Panel principal</q-item-label>
          </q-item-section>
        </q-item>

        <!-- Inicio -->
        <q-item
          clickable
          :to="{ name: 'home' }"
          exact
          class="rounded-borders q-mb-xs"
          active-class="bg-blue-1 text-primary"
        >
          <q-item-section avatar class="min-width-none">
            <q-icon name="home" size="20px" />
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-weight-medium">Inicio</q-item-label>
            <q-item-label caption>Página principal</q-item-label>
          </q-item-section>
        </q-item>

        <q-separator class="q-my-md" />

        <!-- Compras -->
        <q-expansion-item
          icon="shopping_cart"
          label="Compras"
          header-class="text-primary text-weight-medium"
          expand-icon-class="text-primary"
          default-opened
          class="rounded-borders"
        >
          <template v-slot:header>
            <q-item-section avatar class="min-width-none">
              <q-icon name="shopping_cart" color="primary" size="20px" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-weight-medium text-primary">Compras</q-item-label>
              <q-item-label caption class="text-grey-6">Gestión de adquisiciones</q-item-label>
            </q-item-section>
          </template>

          <div class="q-ml-md q-mt-sm">
            <q-item
              clickable
              :to="{ name: 'documentos' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="receipt_long" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Documentos</q-item-label>
                <q-item-label caption>Documentos de compra</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :to="{ name: 'ordenes-compra' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="local_mall" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Órdenes de Compra</q-item-label>
                <q-item-label caption>Gestión de OC</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :to="{ name: 'aprobaciones' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="check_circle" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Aprobaciones</q-item-label>
                <q-item-label caption>Autorizar órdenes</q-item-label>
              </q-item-section>
            </q-item>
          </div>
        </q-expansion-item>
          
        <!-- Inventario -->
        <q-expansion-item
          icon="inventory"
          label="Inventario"
          header-class="text-primary text-weight-medium"
          expand-icon-class="text-primary"
          default-opened
          class="rounded-borders"
        >
          <template v-slot:header>
            <q-item-section avatar class="min-width-none">
              <q-icon name="inventory" color="primary" size="20px" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-weight-medium text-primary">Inventario</q-item-label>
              <q-item-label caption class="text-grey-6">Control de stock y productos</q-item-label>
            </q-item-section>
          </template>

          <div class="q-ml-md q-mt-sm">
            <q-item
              clickable
              :to="{ name: 'productos' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="inventory_2" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Productos</q-item-label>
                <q-item-label caption>Catálogo de productos</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :to="{ name: 'ajustes-inventario' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="tune" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Ajustes</q-item-label>
                <q-item-label caption>Ajustes de inventario</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :to="{ name: 'movimientos' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="compare_arrows" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Movimientos</q-item-label>
                <q-item-label caption>Historial de movimientos</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :to="{ name: 'traspasos' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="swap_horiz" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Traspasos</q-item-label>
                <q-item-label caption>Traspasos entre bodegas</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :to="{ name: 'stock-bodega' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="warehouse" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Stock por Bodega</q-item-label>
                <q-item-label caption>Inventario por ubicación</q-item-label>
              </q-item-section>
            </q-item>
          </div>
        </q-expansion-item>

        <!-- Obras -->
        <q-expansion-item
          icon="construction"
          label="Obras"
          header-class="text-primary text-weight-medium"
          expand-icon-class="text-primary"
          class="rounded-borders"
        >
          <template v-slot:header>
            <q-item-section avatar class="min-width-none">
              <q-icon name="construction" color="primary" size="20px" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-weight-medium text-primary">Obras</q-item-label>
              <q-item-label caption class="text-grey-6">Gestión de proyectos</q-item-label>
            </q-item-section>
          </template>

          <div class="q-ml-md q-mt-sm">
            <q-item
              clickable
              :to="{ name: 'obras' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="engineering" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Obras</q-item-label>
                <q-item-label caption>Gestión de obras</q-item-label>
              </q-item-section>
            </q-item>
          </div>
        </q-expansion-item>

        <!-- Configuración -->
        <q-expansion-item
          icon="settings"
          label="Configuración"
          header-class="text-primary text-weight-medium"
          expand-icon-class="text-primary"
          class="rounded-borders"
        >
          <template v-slot:header>
            <q-item-section avatar class="min-width-none">
              <q-icon name="settings" color="primary" size="20px" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-weight-medium text-primary">Configuración</q-item-label>
              <q-item-label caption class="text-grey-6">Maestros y configuración</q-item-label>
            </q-item-section>
          </template>

          <div class="q-ml-md q-mt-sm">
            <q-item
              clickable
              :to="{ name: 'bodegas' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="warehouse" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Bodegas</q-item-label>
                <q-item-label caption>Configurar bodegas</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :to="{ name: 'proveedores' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="business" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Proveedores</q-item-label>
                <q-item-label caption>Gestión de proveedores</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :to="{ name: 'clientes' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="people" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Clientes</q-item-label>
                <q-item-label caption>Gestión de clientes</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :to="{ name: 'categorias' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="category" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Categorías</q-item-label>
                <q-item-label caption>Categorías de productos</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :to="{ name: 'marcas' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="branding_watermark" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Marcas</q-item-label>
                <q-item-label caption>Marcas de productos</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :to="{ name: 'tipos-producto' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="label" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Tipos de Producto</q-item-label>
                <q-item-label caption>Tipos de productos</q-item-label>
              </q-item-section>
            </q-item>

            <q-item
              clickable
              :to="{ name: 'centros-costo' }"
              class="rounded-borders q-mb-xs"
              active-class="bg-blue-1 text-primary"
            >
              <q-item-section avatar class="min-width-none">
                <q-icon name="account_balance" size="18px" />
              </q-item-section>
              <q-item-section>
                <q-item-label>Centros de Costo</q-item-label>
                <q-item-label caption>Gestión de centros de costo</q-item-label>
              </q-item-section>
            </q-item>
          </div>
        </q-expansion-item>

        <q-separator class="q-my-md" />

        <!-- Admin section -->
        <template v-if="authStore.isAdmin">
          <q-item
            clickable
            :to="{ name: 'users' }"
            exact
            class="rounded-borders q-mb-xs"
            active-class="bg-blue-1 text-primary"
          >
            <q-item-section avatar class="min-width-none">
              <q-icon name="admin_panel_settings" size="20px" />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-weight-medium">Administración</q-item-label>
              <q-item-label caption>Gestión de usuarios</q-item-label>
            </q-item-section>
          </q-item>

          <q-separator class="q-my-md" />
        </template>

        <!-- About -->
        <q-item
          clickable
          :to="{ name: 'about' }"
          exact
          class="rounded-borders"
          active-class="bg-blue-1 text-primary"
        >
          <q-item-section avatar class="min-width-none">
            <q-icon name="info" size="20px" />
          </q-item-section>
          <q-item-section>
            <q-item-label class="text-weight-medium">Acerca de</q-item-label>
            <q-item-label caption>Información del sistema</q-item-label>
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
import { ref, onMounted } from 'vue'
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
  router.push({ name: 'perfil' })
}

const goToSettings = () => {
  router.push({ name: 'configuracion' })
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

// Load theme on mount
onMounted(() => {
  try {
    const savedPrefs = localStorage.getItem('userPreferences')
    if (savedPrefs) {
      const preferences = JSON.parse(savedPrefs)
      if (preferences.theme === 'dark') {
        document.body.classList.add('dark')
      } else {
        document.body.classList.remove('dark')
      }
    }
  } catch (error) {
    console.error('Error loading theme:', error)
  }
})
</script>