import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, Role, UserCreate, UserUpdate } from '../types'
import { useApiStore } from './api'

export const useUsersStore = defineStore('users', () => {
  const apiStore = useApiStore()

  // State
  const users = ref<User[]>([])
  const roles = ref<Role[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const getUserById = computed(() => (id: number) => {
    return users.value.find(user => user.id_usuario === id)
  })

  const activeUsers = computed(() => {
    return users.value.filter(user => user.activo)
  })

  const activeRoles = computed(() => {
    return roles.value.filter(role => role.activo)
  })

  // Actions
  const fetchUsers = async (): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      const response = await apiStore.get('/usuarios/')
      users.value = response.data
    } catch (err: any) {
      console.error('Error fetching users:', err)
      error.value = err.response?.data?.detail || 'Error al cargar usuarios'
    } finally {
      isLoading.value = false
    }
  }

  const fetchRoles = async (): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      const response = await apiStore.get('/roles/')
      roles.value = response.data
    } catch (err: any) {
      console.error('Error fetching roles:', err)
      error.value = err.response?.data?.detail || 'Error al cargar roles'
    } finally {
      isLoading.value = false
    }
  }

  const createUser = async (userData: UserCreate): Promise<User | null> => {
    isLoading.value = true
    error.value = null

    try {
      const response = await apiStore.post('/usuarios/', userData)
      const newUser = response.data
      users.value.push(newUser)
      return newUser
    } catch (err: any) {
      console.error('Error creating user:', err)
      console.error('Error response:', err.response?.data)
      console.error('Request data:', userData)
      error.value = err.response?.data?.detail || err.response?.data || 'Error al crear usuario'
      return null
    } finally {
      isLoading.value = false
    }
  }

  const updateUser = async (id: number, userData: UserUpdate): Promise<User | null> => {
    isLoading.value = true
    error.value = null

    try {
      const response = await apiStore.put(`/usuarios/${id}`, userData)
      const updatedUser = response.data

      const index = users.value.findIndex(user => user.id_usuario === id)
      if (index !== -1) {
        users.value[index] = updatedUser
      }

      return updatedUser
    } catch (err: any) {
      console.error('Error updating user:', err)
      error.value = err.response?.data?.detail || 'Error al actualizar usuario'
      return null
    } finally {
      isLoading.value = false
    }
  }

  const deleteUser = async (id: number): Promise<boolean> => {
    isLoading.value = true
    error.value = null

    try {
      await apiStore.delete(`/usuarios/${id}`)
      users.value = users.value.filter(user => user.id_usuario !== id)
      return true
    } catch (err: any) {
      console.error('Error deleting user:', err)
      error.value = err.response?.data?.detail || 'Error al eliminar usuario'
      return false
    } finally {
      isLoading.value = false
    }
  }

  const toggleUserStatus = async (id: number): Promise<boolean> => {
    const user = getUserById.value(id)
    if (!user) return false

    return await updateUser(id, { activo: !user.activo }) !== null
  }

  const changeUserPassword = async (id: number, newPassword: string): Promise<boolean> => {
    return await updateUser(id, { password: newPassword }) !== null
  }

  const getRoleName = (roleId: number): string => {
    const role = roles.value.find(r => r.id_rol === roleId)
    return role?.nombre_rol || 'Rol desconocido'
  }

  return {
    // State
    users,
    roles,
    isLoading,
    error,

    // Getters
    getUserById,
    activeUsers,
    activeRoles,

    // Actions
    fetchUsers,
    fetchRoles,
    createUser,
    updateUser,
    deleteUser,
    toggleUserStatus,
    changeUserPassword,
    getRoleName
  }
})