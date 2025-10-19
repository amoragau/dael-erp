<template>
  <q-page class="q-pa-lg">
    <!-- Page Header -->
    <div class="page-header">
      <div class="row items-center q-mb-sm">
        <q-icon name="account_circle" size="32px" color="primary" class="q-mr-md" />
        <h4 class="q-my-none text-h4 text-weight-light">Mi <span class="text-weight-bold text-primary">Perfil</span></h4>
      </div>
      <p class="text-body2 text-grey-6 q-mb-none">Gestiona tu información personal y configuración de cuenta</p>
    </div>

    <div class="row q-gutter-lg">
      <!-- Profile Information Card -->
      <div class="col-12 col-md-8">
        <q-card class="shadow-light">
          <q-card-section class="bg-blue-1">
            <div class="text-h6 text-primary">
              <q-icon name="person" class="q-mr-sm" />
              Información Personal
            </div>
            <div class="text-caption text-grey-6">Actualiza tus datos personales</div>
          </q-card-section>

          <q-card-section>
            <q-form @submit.prevent="updateProfile" class="q-gutter-md">
              <!-- Basic Information -->
              <div class="row q-gutter-md">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="profileForm.nombre_completo"
                    label="Nombre Completo *"
                    outlined
                    dense
                    :rules="[val => !!val || 'El nombre es requerido']"
                    :readonly="!editMode"
                  >
                    <template v-slot:prepend>
                      <q-icon name="badge" color="primary" />
                    </template>
                  </q-input>
                </div>

                <div class="col-12 col-md-6">
                  <q-input
                    v-model="profileForm.username"
                    label="Usuario *"
                    outlined
                    dense
                    :rules="[val => !!val || 'El usuario es requerido']"
                    :readonly="!editMode"
                    hint="Nombre de usuario para iniciar sesión"
                  >
                    <template v-slot:prepend>
                      <q-icon name="alternate_email" color="primary" />
                    </template>
                  </q-input>
                </div>
              </div>

              <div class="row q-gutter-md">
                <div class="col-12 col-md-6">
                  <q-input
                    v-model="profileForm.email"
                    label="Correo Electrónico *"
                    type="email"
                    outlined
                    dense
                    :rules="[val => !!val || 'El email es requerido',
                            val => /.+@.+\..+/.test(val) || 'Email debe ser válido']"
                    :readonly="!editMode"
                  >
                    <template v-slot:prepend>
                      <q-icon name="email" color="primary" />
                    </template>
                  </q-input>
                </div>

                <div class="col-12 col-md-6">
                  <q-select
                    v-model="profileForm.id_rol"
                    :options="rolesOptions"
                    label="Rol del Usuario"
                    outlined
                    dense
                    emit-value
                    map-options
                    disable
                    hint="Contacta al administrador para cambiar rol"
                  >
                    <template v-slot:prepend>
                      <q-icon name="security" color="primary" />
                    </template>
                  </q-select>
                </div>
              </div>

              <!-- Password Change Section -->
              <q-expansion-item
                v-if="editMode"
                icon="lock"
                label="Cambiar Contraseña"
                class="q-mt-md"
                header-class="text-primary"
              >
                <div class="q-pa-md bg-grey-1 rounded-borders">
                  <div class="row q-gutter-md">
                    <div class="col-12">
                      <q-input
                        v-model="passwordForm.current_password"
                        label="Contraseña Actual *"
                        type="password"
                        outlined
                        dense
                        :rules="[val => !val || val.length >= 1 || 'Contraseña actual requerida']"
                      >
                        <template v-slot:prepend>
                          <q-icon name="key" color="grey-6" />
                        </template>
                      </q-input>
                    </div>

                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="passwordForm.new_password"
                        label="Nueva Contraseña"
                        type="password"
                        outlined
                        dense
                        :rules="[val => !val || val.length >= 6 || 'Mínimo 6 caracteres']"
                      >
                        <template v-slot:prepend>
                          <q-icon name="lock_outline" color="grey-6" />
                        </template>
                      </q-input>
                    </div>

                    <div class="col-12 col-md-6">
                      <q-input
                        v-model="passwordForm.confirm_password"
                        label="Confirmar Contraseña"
                        type="password"
                        outlined
                        dense
                        :rules="[val => !val || val === passwordForm.new_password || 'Las contraseñas no coinciden']"
                      >
                        <template v-slot:prepend>
                          <q-icon name="lock_outline" color="grey-6" />
                        </template>
                      </q-input>
                    </div>
                  </div>
                </div>
              </q-expansion-item>

              <!-- Action Buttons -->
              <div class="row q-gutter-sm q-mt-lg">
                <q-btn
                  v-if="!editMode"
                  @click="enableEditMode"
                  color="primary"
                  unelevated
                  icon="edit"
                  label="Editar Perfil"
                  class="rounded-borders"
                />

                <template v-else>
                  <q-btn
                    type="submit"
                    color="primary"
                    unelevated
                    icon="save"
                    label="Guardar Cambios"
                    :loading="loading"
                    class="rounded-borders"
                  />

                  <q-btn
                    @click="cancelEdit"
                    color="grey-6"
                    unelevated
                    icon="cancel"
                    label="Cancelar"
                    class="rounded-borders"
                  />
                </template>
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </div>

      <!-- Account Information Sidebar -->
      <div class="col-12 col-md-4">
        <div class="column q-gutter-md">
          <!-- Account Status Card -->
          <q-card class="shadow-light">
            <q-card-section class="bg-green-1">
              <div class="text-h6 text-green-8">
                <q-icon name="verified_user" class="q-mr-sm" />
                Estado de la Cuenta
              </div>
            </q-card-section>

            <q-card-section>
              <div class="column q-gutter-sm">
                <div class="row items-center justify-between">
                  <span class="text-body2">Estado:</span>
                  <q-badge
                    :color="authStore.user?.activo ? 'green' : 'red'"
                    :label="authStore.user?.activo ? 'Activa' : 'Inactiva'"
                    class="status-badge"
                  />
                </div>

                <div class="row items-center justify-between">
                  <span class="text-body2">Usuario ID:</span>
                  <span class="text-weight-medium">#{{ authStore.user?.id_usuario }}</span>
                </div>

                <div class="row items-center justify-between">
                  <span class="text-body2">Rol:</span>
                  <span class="text-weight-medium">{{ getRoleName(authStore.user?.id_rol) }}</span>
                </div>

                <q-separator class="q-my-sm" />

                <div class="column q-gutter-xs">
                  <span class="text-body2 text-grey-6">Fecha de Registro:</span>
                  <span class="text-caption">{{ formatDate(authStore.user?.fecha_creacion) }}</span>
                </div>

                <div class="column q-gutter-xs">
                  <span class="text-body2 text-grey-6">Último Acceso:</span>
                  <span class="text-caption">{{ formatDate(authStore.user?.ultimo_acceso) || 'Primera vez' }}</span>
                </div>

                <div class="column q-gutter-xs">
                  <span class="text-body2 text-grey-6">Última Modificación:</span>
                  <span class="text-caption">{{ formatDate(authStore.user?.fecha_modificacion) }}</span>
                </div>
              </div>
            </q-card-section>
          </q-card>

          <!-- Quick Actions Card -->
          <q-card class="shadow-light">
            <q-card-section class="bg-blue-1">
              <div class="text-h6 text-primary">
                <q-icon name="flash_on" class="q-mr-sm" />
                Acciones Rápidas
              </div>
            </q-card-section>

            <q-card-section>
              <div class="column q-gutter-sm">
                <q-btn
                  @click="downloadProfile"
                  flat
                  icon="download"
                  label="Descargar Datos"
                  class="justify-start"
                  color="primary"
                />

                <q-btn
                  @click="refreshSession"
                  flat
                  icon="refresh"
                  label="Actualizar Sesión"
                  class="justify-start"
                  color="primary"
                />

                <q-separator class="q-my-sm" />

                <q-btn
                  @click="logout"
                  flat
                  icon="logout"
                  label="Cerrar Sesión"
                  class="justify-start"
                  color="negative"
                />
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from '../stores/auth'
import type { User, Role } from '../types'

// Stores and router
const authStore = useAuthStore()
const router = useRouter()
const $q = useQuasar()

// State
const editMode = ref(false)
const loading = ref(false)
const roles = ref<Role[]>([])

// Forms
const profileForm = reactive<Partial<User>>({
  nombre_completo: '',
  username: '',
  email: '',
  id_rol: 1
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

// Computed
const rolesOptions = computed(() =>
  roles.value.map(role => ({
    label: role.nombre_rol,
    value: role.id_rol
  }))
)

// Methods
const loadUserData = () => {
  if (authStore.user) {
    Object.assign(profileForm, {
      nombre_completo: authStore.user.nombre_completo,
      username: authStore.user.username,
      email: authStore.user.email,
      id_rol: authStore.user.id_rol
    })
  }
}

const loadRoles = async () => {
  try {
    // For now, use static roles based on your system
    roles.value = [
      { id_rol: 1, nombre_rol: 'Administrador', descripcion: 'Acceso completo al sistema', activo: true },
      { id_rol: 2, nombre_rol: 'Supervisor', descripcion: 'Permisos de supervisión', activo: true },
      { id_rol: 3, nombre_rol: 'Usuario', descripcion: 'Usuario estándar', activo: true }
    ]
  } catch (error) {
    console.error('Error loading roles:', error)
  }
}

const enableEditMode = () => {
  editMode.value = true
  loadUserData()
}

const cancelEdit = () => {
  editMode.value = false
  loadUserData()
  // Reset password form
  Object.assign(passwordForm, {
    current_password: '',
    new_password: '',
    confirm_password: ''
  })
}

const updateProfile = async () => {
  loading.value = true

  try {
    // Prepare update data
    const updateData: any = {
      nombre_completo: profileForm.nombre_completo,
      username: profileForm.username,
      email: profileForm.email
    }

    // Add password if provided
    if (passwordForm.new_password) {
      updateData.password = passwordForm.new_password
      updateData.current_password = passwordForm.current_password
    }

    // Call API to update profile
    const success = await authStore.updateProfile(updateData)

    if (success) {
      $q.notify({
        type: 'positive',
        message: 'Perfil actualizado correctamente',
        position: 'top-right'
      })

      editMode.value = false
      // Reset password form
      Object.assign(passwordForm, {
        current_password: '',
        new_password: '',
        confirm_password: ''
      })
    } else {
      $q.notify({
        type: 'negative',
        message: 'Error al actualizar el perfil',
        position: 'top-right'
      })
    }
  } catch (error) {
    console.error('Profile update error:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al actualizar el perfil',
      position: 'top-right'
    })
  } finally {
    loading.value = false
  }
}

const getRoleName = (roleId?: number) => {
  const role = roles.value.find(r => r.id_rol === roleId)
  return role?.nombre_rol || 'Desconocido'
}

const formatDate = (dateString?: string | null) => {
  if (!dateString) return null

  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    return 'Fecha inválida'
  }
}

const downloadProfile = () => {
  // Create a simple data export
  const userData = {
    ...authStore.user,
    exported_at: new Date().toISOString()
  }

  const dataStr = JSON.stringify(userData, null, 2)
  const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr)

  const exportFileDefaultName = `mi_perfil_${new Date().toISOString().split('T')[0]}.json`

  const linkElement = document.createElement('a')
  linkElement.setAttribute('href', dataUri)
  linkElement.setAttribute('download', exportFileDefaultName)
  linkElement.click()

  $q.notify({
    type: 'positive',
    message: 'Datos del perfil descargados',
    position: 'top-right'
  })
}

const refreshSession = async () => {
  try {
    const isValid = await authStore.checkAuth()
    if (isValid) {
      loadUserData()
      $q.notify({
        type: 'positive',
        message: 'Sesión actualizada correctamente',
        position: 'top-right'
      })
    } else {
      $q.notify({
        type: 'negative',
        message: 'Error al actualizar la sesión',
        position: 'top-right'
      })
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Error al actualizar la sesión',
      position: 'top-right'
    })
  }
}

const logout = () => {
  $q.dialog({
    title: 'Cerrar Sesión',
    message: '¿Estás seguro de que deseas cerrar sesión?',
    cancel: true,
    persistent: true,
    color: 'primary'
  }).onOk(() => {
    authStore.logout()
    router.push({ name: 'login' })
  })
}

// Lifecycle
onMounted(() => {
  loadUserData()
  loadRoles()
})
</script>

<style scoped>
.page-header {
  background: linear-gradient(135deg, var(--primary-50) 0%, var(--grey-50) 100%);
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
}

.status-badge {
  padding: 4px 12px !important;
  border-radius: 20px !important;
  font-weight: 600 !important;
  font-size: 0.75rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
}
</style>