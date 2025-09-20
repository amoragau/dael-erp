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
  }

  // Check if route requires guest (unauthenticated) user
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }

  next()
})

export default router