import { defineStore } from 'pinia'
import { ref, computed, readonly } from 'vue'
import type { User } from '../types'
import { useApiStore } from './api'

interface LoginCredentials {
  username: string
  password: string
}

interface LoginResponse {
  usuario: User
  token: string | null
  mensaje: string
}

export const useAuthStore = defineStore('auth', () => {
  const apiStore = useApiStore()

  // State
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const userName = computed(() => user.value?.nombre_completo || user.value?.username || 'Usuario')
  const isAdmin = computed(() => user.value?.id_rol === 1)

  // Actions
  const login = async (credentials: LoginCredentials): Promise<boolean> => {
    isLoading.value = true
    error.value = null

    try {
      // Real API authentication using your endpoints
      const response = await apiStore.post('/usuarios/login', {
        username: credentials.username,
        password: credentials.password
      })

      if (!response.success) {
        throw new Error(response.error || 'Error en login')
      }

      const loginData: LoginResponse = response.data

      // Store user info
      user.value = loginData.usuario

      // For now, create a simple token since your API doesn't use JWT yet
      const simpleToken = `user-${loginData.usuario.id_usuario}-${Date.now()}`
      token.value = simpleToken

      // Persist token and user in localStorage
      localStorage.setItem('token', simpleToken)
      localStorage.setItem('user', JSON.stringify(loginData.usuario))

      // Set default authorization header (for future JWT implementation)
      apiStore.apiClient.defaults.headers.common['Authorization'] = `Bearer ${simpleToken}`

      return true
    } catch (err: any) {
      console.error('Login error:', err)

      // Handle different types of errors
      if (err.response) {
        // Server responded with error status
        error.value = err.response.data?.detail || `Error ${err.response.status}: ${err.response.statusText}`
      } else if (err.request) {
        // Network error - server not responding
        error.value = 'No se puede conectar con el servidor. Verifica que el backend esté ejecutándose.'
      } else {
        // Other error
        error.value = err.message || 'Error inesperado durante el login'
      }
      return false
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    error.value = null

    // Clear localStorage
    localStorage.removeItem('token')
    localStorage.removeItem('user')

    // Remove authorization header
    delete apiStore.apiClient.defaults.headers.common['Authorization']
  }

  const checkAuth = async (): Promise<boolean> => {
    if (!token.value) {
      return false
    }

    try {
      // For now, just verify if user data exists in localStorage
      // since your API doesn't have JWT token verification yet
      const storedUser = localStorage.getItem('user')
      if (storedUser && token.value) {
        user.value = JSON.parse(storedUser)
        // Set token in headers for future JWT implementation
        apiStore.apiClient.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
        return true
      } else {
        logout()
        return false
      }
    } catch (err: any) {
      console.error('Auth check failed:', err)
      // Token is invalid, clear everything
      logout()
      return false
    }
  }

  const updateProfile = async (userData: Partial<User>): Promise<boolean> => {
    try {
      const response = await apiStore.put('/auth/profile', userData)
      if (!response.success) {
        throw new Error(response.error || 'Error al actualizar perfil')
      }
      user.value = response.data
      return true
    } catch (err) {
      error.value = 'Error al actualizar perfil'
      return false
    }
  }

  // Initialize auth state on store creation
  if (token.value) {
    checkAuth()
  }

  return {
    // State
    token: readonly(token),
    user: readonly(user),
    isLoading: readonly(isLoading),
    error: readonly(error),

    // Getters
    isAuthenticated,
    userName,
    isAdmin,

    // Actions
    login,
    logout,
    checkAuth,
    updateProfile
  }
})