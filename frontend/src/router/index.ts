import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: {
        requiresGuest: true,
        layout: 'blank'
      }
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/usuarios',
      name: 'users',
      component: () => import('../views/UsersView.vue'),
      meta: {
        requiresAuth: true,
        requiresAdmin: true
      }
    },
    {
      path: '/categorias',
      name: 'categorias',
      component: () => import('../views/CategoriasView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/proveedores',
      name: 'proveedores',
      component: () => import('../views/ProveedoresView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/productos',
      name: 'productos',
      component: () => import('../views/ProductosView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/bodegas',
      name: 'bodegas',
      component: () => import('../views/BodegasView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/clientes',
      name: 'clientes',
      component: () => import('../views/ClientesView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/obras',
      name: 'obras',
      component: () => import('../views/ObrasView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/tipos-producto',
      name: 'tipos-producto',
      component: () => import('../views/TiposProductoView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/marcas',
      name: 'marcas',
      component: () => import('../views/MarcasView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/movimientos',
      name: 'movimientos',
      component: () => import('../views/MovimientosView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/ordenes-compra',
      name: 'ordenes-compra',
      component: () => import('../views/OrdenesCompraView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/aprobaciones',
      name: 'aprobaciones',
      component: () => import('../views/AprobacionesView.vue'),
      meta: {
        requiresAuth: true,
        requiresApprovalPermission: true
      }
    },
    {
      path: '/documentos',
      name: 'documentos',
      component: () => import('../views/DocumentosView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/stock-bodega',
      name: 'stock-bodega',
      component: () => import('../views/StockBodegaView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/ajustes-inventario',
      name: 'ajustes-inventario',
      component: () => import('../views/AjustesInventarioView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/traspasos',
      name: 'traspasos',
      component: () => import('../views/TraspasosView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/configuracion-alertas',
      name: 'configuracion-alertas',
      component: () => import('../views/ConfiguracionAlertasView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/configuracion-sistema',
      name: 'configuracion-sistema',
      component: () => import('../views/ConfiguracionSistemaView.vue'),
      meta: {
        requiresAuth: true,
        requiresAdmin: true
      }
    },
    {
      path: '/perfil',
      name: 'perfil',
      component: () => import('../views/PerfilView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/configuracion',
      name: 'configuracion',
      component: () => import('../views/ConfiguracionView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/centros-costo',
      name: 'centros-costo',
      component: () => import('../views/CentrosCostoView.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue')
    }
  ]
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  // Import store inside the guard to avoid circular dependency
  const { useAuthStore } = await import('../stores/auth')
  const authStore = useAuthStore()

  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      // Check if user has valid token
      const isValid = await authStore.checkAuth()

      if (!isValid) {
        // Redirect to login with return URL
        next({
          name: 'login',
          query: { redirect: to.fullPath }
        })
        return
      }
    }

    // Check if route requires admin role (assuming role ID 1 is administrator)
    if (to.meta.requiresAdmin && authStore.user?.id_rol !== 1) {
      // Redirect to dashboard if user is not admin
      next({ name: 'dashboard' })
      return
    }

    // Check if route requires approval permission
    if (to.meta.requiresApprovalPermission) {
      // TODO: Implementar sistema completo de permisos
      // Por ahora, solo permitir a administradores y usuarios con rol específico
      const canApprove = authStore.user?.id_rol === 1 || // Admin
                        authStore.user?.id_rol === 2    // Manager/Supervisor

      if (!canApprove) {
        next({ name: 'dashboard' })
        return
      }
    }
  }

  // Check if route requires guest (unauthenticated) user
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }

  next()
})

export default router