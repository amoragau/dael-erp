<template>
  <q-page padding>
    <div class="q-pa-md">
      <!-- Header -->
      <div class="row items-center justify-between q-mb-md">
        <div>
          <h4 class="q-my-none">Gestión de Usuarios</h4>
          <p class="text-grey-7 q-mb-none">Administra los usuarios del sistema</p>
        </div>
        <q-btn
          color="primary"
          icon="add"
          label="Nuevo Usuario"
          @click="showCreateDialog = true"
        />
      </div>

      <!-- Users Table -->
      <q-table
        :rows="usersStore.users"
        :columns="columns"
        :loading="usersStore.isLoading"
        :pagination="{ rowsPerPage: 10 }"
        row-key="id_usuario"
        flat
        bordered
      >
        <template v-slot:body-cell-activo="props">
          <q-td :props="props">
            <q-badge
              :color="props.value ? 'green' : 'red'"
              :label="props.value ? 'Activo' : 'Inactivo'"
            />
          </q-td>
        </template>

        <template v-slot:body-cell-rol="props">
          <q-td :props="props">
            {{ usersStore.getRoleName(props.row.id_rol) }}
          </q-td>
        </template>

        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn
              flat
              round
              icon="edit"
              color="primary"
              size="sm"
              @click="editUser(props.row)"
            >
              <q-tooltip>Editar</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              :icon="props.row.activo ? 'block' : 'check_circle'"
              :color="props.row.activo ? 'orange' : 'green'"
              size="sm"
              @click="toggleUserStatus(props.row)"
            >
              <q-tooltip>{{ props.row.activo ? 'Desactivar' : 'Activar' }}</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="lock_reset"
              color="purple"
              size="sm"
              @click="showPasswordDialog(props.row)"
            >
              <q-tooltip>Cambiar Contraseña</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              icon="delete"
              color="red"
              size="sm"
              @click="confirmDelete(props.row)"
            >
              <q-tooltip>Eliminar</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>

      <!-- Create/Edit User Dialog -->
      <q-dialog v-model="showCreateDialog" persistent>
        <q-card style="min-width: 500px">
          <q-card-section>
            <div class="text-h6">{{ editingUser ? 'Editar Usuario' : 'Nuevo Usuario' }}</div>
          </q-card-section>

          <q-card-section>
            <q-form @submit="submitUser" class="q-gutter-md">
              <q-input
                v-model="userForm.username"
                label="Nombre de Usuario"
                :rules="[val => !!val || 'Campo requerido']"
                outlined
              />

              <q-input
                v-model="userForm.email"
                label="Email"
                type="email"
                :rules="[val => !!val || 'Campo requerido']"
                outlined
              />

              <q-input
                v-model="userForm.nombre_completo"
                label="Nombre Completo"
                :rules="[val => !!val || 'Campo requerido']"
                outlined
              />

              <q-input
                v-if="!editingUser"
                v-model="userForm.password"
                label="Contraseña"
                type="password"
                :rules="[val => !!val || 'Campo requerido']"
                outlined
              />

              <q-select
                v-model="userForm.id_rol"
                :options="roleOptions"
                option-value="id_rol"
                option-label="nombre_rol"
                emit-value
                map-options
                label="Rol"
                :rules="[val => !!val || 'Campo requerido']"
                outlined
              />

              <q-toggle
                v-model="userForm.activo"
                label="Usuario Activo"
              />
            </q-form>
          </q-card-section>

          <q-card-actions align="right" class="text-primary">
            <q-btn flat label="Cancelar" @click="closeDialog" />
            <q-btn
              flat
              label="Guardar"
              @click="submitUser"
              :loading="usersStore.isLoading"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Change Password Dialog -->
      <q-dialog v-model="showPasswordChangeDialog" persistent>
        <q-card style="min-width: 400px">
          <q-card-section>
            <div class="text-h6">Cambiar Contraseña</div>
            <p class="text-grey-7">{{ selectedUser?.nombre_completo }}</p>
          </q-card-section>

          <q-card-section>
            <q-input
              v-model="newPassword"
              label="Nueva Contraseña"
              type="password"
              :rules="[val => !!val || 'Campo requerido', val => val.length >= 8 || 'Mínimo 8 caracteres']"
              outlined
            />

            <q-input
              v-model="confirmPassword"
              label="Confirmar Contraseña"
              type="password"
              :rules="[val => !!val || 'Campo requerido', val => val === newPassword || 'Las contraseñas no coinciden']"
              outlined
              class="q-mt-md"
            />
          </q-card-section>

          <q-card-actions align="right" class="text-primary">
            <q-btn flat label="Cancelar" @click="closePasswordDialog" />
            <q-btn
              flat
              label="Cambiar"
              @click="changePassword"
              :loading="usersStore.isLoading"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useUsersStore } from '../stores/users'
import type { User, UserCreate, UserUpdate } from '../types'

type TableColumn = {
  name: string;
  required: boolean;
  label: string;
  align: 'left' | 'center' | 'right';
  field: string | ((row: any) => any);
  sortable?: boolean;
  format?: (val: any, row?: any) => string;
}

const $q = useQuasar()
const usersStore = useUsersStore()

// Reactive state
const showCreateDialog = ref(false)
const showPasswordChangeDialog = ref(false)
const editingUser = ref<User | null>(null)
const selectedUser = ref<User | null>(null)
const newPassword = ref('')
const confirmPassword = ref('')

// Form data
const userForm = reactive<UserCreate & { activo: boolean }>({
  username: '',
  email: '',
  nombre_completo: '',
  password: '',
  id_rol: 0,
  activo: true
})

// Table columns
const columns: TableColumn[] = [
  {
    name: 'username',
    required: true,
    label: 'Usuario',
    align: 'left',
    field: 'username',
    sortable: true
  },
  {
    name: 'nombre_completo',
    required: true,
    label: 'Nombre Completo',
    align: 'left',
    field: 'nombre_completo',
    sortable: true
  },
  {
    name: 'email',
    required: true,
    label: 'Email',
    align: 'left',
    field: 'email',
    sortable: true
  },
  {
    name: 'rol',
    required: true,
    label: 'Rol',
    align: 'left',
    field: 'id_rol',
    sortable: true
  },
  {
    name: 'activo',
    required: true,
    label: 'Estado',
    align: 'center',
    field: 'activo',
    sortable: true
  },
  {
    name: 'ultimo_acceso',
    required: false,
    label: 'Último Acceso',
    align: 'left',
    field: 'ultimo_acceso',
    sortable: true,
    format: (val: string | null) => val ? new Date(val).toLocaleString() : 'Nunca'
  },
  {
    name: 'actions',
    required: true,
    label: 'Acciones',
    align: 'center',
    field: 'actions'
  }
]

// Computed
const roleOptions = computed(() => usersStore.activeRoles)

// Methods
const loadData = async () => {
  await Promise.all([
    usersStore.fetchUsers(),
    usersStore.fetchRoles()
  ])
}

const resetForm = () => {
  userForm.username = ''
  userForm.email = ''
  userForm.nombre_completo = ''
  userForm.password = ''
  userForm.id_rol = usersStore.activeRoles.length > 0 ? usersStore.activeRoles[0].id_rol : 1
  userForm.activo = true
}

const closeDialog = () => {
  showCreateDialog.value = false
  editingUser.value = null
  resetForm()
}

const closePasswordDialog = () => {
  showPasswordChangeDialog.value = false
  selectedUser.value = null
  newPassword.value = ''
  confirmPassword.value = ''
}

const editUser = (user: User) => {
  editingUser.value = user
  userForm.username = user.username
  userForm.email = user.email
  userForm.nombre_completo = user.nombre_completo
  userForm.id_rol = user.id_rol
  userForm.activo = user.activo
  showCreateDialog.value = true
}

const submitUser = async () => {
  // Validate form data before sending
  if (!userForm.username || !userForm.email || !userForm.nombre_completo || !userForm.id_rol) {
    $q.notify({
      type: 'negative',
      message: 'Todos los campos obligatorios deben estar completos'
    })
    return
  }

  if (!editingUser.value && (!userForm.password || userForm.password.length < 8)) {
    $q.notify({
      type: 'negative',
      message: 'La contraseña debe tener al menos 8 caracteres'
    })
    return
  }

  try {
    if (editingUser.value) {
      // Update existing user
      const updateData: UserUpdate = {
        username: userForm.username,
        email: userForm.email,
        nombre_completo: userForm.nombre_completo,
        id_rol: userForm.id_rol,
        activo: userForm.activo
      }

      const success = await usersStore.updateUser(editingUser.value.id_usuario, updateData)

      if (success) {
        $q.notify({
          type: 'positive',
          message: 'Usuario actualizado exitosamente'
        })
        closeDialog()
      }
    } else {
      // Create new user - ensure data is properly formatted
      const userData = {
        username: userForm.username.trim(),
        email: userForm.email.trim(),
        nombre_completo: userForm.nombre_completo.trim(),
        password: userForm.password,
        id_rol: Number(userForm.id_rol),
        activo: userForm.activo
      }

      console.log('Sending user data:', userData)
      const success = await usersStore.createUser(userData)

      if (success) {
        $q.notify({
          type: 'positive',
          message: 'Usuario creado exitosamente'
        })
        closeDialog()
      }
    }
  } catch (error) {
    console.error('Submit error:', error)
    $q.notify({
      type: 'negative',
      message: usersStore.error || 'Error al procesar la solicitud'
    })
  }
}

const toggleUserStatus = async (user: User) => {
  const action = user.activo ? 'desactivar' : 'activar'

  $q.dialog({
    title: 'Confirmar',
    message: `¿Estás seguro de que quieres ${action} a ${user.nombre_completo}?`,
    cancel: true,
    persistent: true
  }).onOk(async () => {
    const success = await usersStore.toggleUserStatus(user.id_usuario)

    if (success) {
      $q.notify({
        type: 'positive',
        message: `Usuario ${action === 'activar' ? 'activado' : 'desactivado'} exitosamente`
      })
    } else {
      $q.notify({
        type: 'negative',
        message: usersStore.error || `Error al ${action} usuario`
      })
    }
  })
}

const showPasswordDialog = (user: User) => {
  selectedUser.value = user
  showPasswordChangeDialog.value = true
}

const changePassword = async () => {
  if (!selectedUser.value || newPassword.value !== confirmPassword.value) {
    $q.notify({
      type: 'negative',
      message: 'Las contraseñas no coinciden'
    })
    return
  }

  if (newPassword.value.length < 8) {
    $q.notify({
      type: 'negative',
      message: 'La contraseña debe tener al menos 8 caracteres'
    })
    return
  }

  const success = await usersStore.changeUserPassword(selectedUser.value.id_usuario, newPassword.value)

  if (success) {
    $q.notify({
      type: 'positive',
      message: 'Contraseña cambiada exitosamente'
    })
    closePasswordDialog()
  } else {
    $q.notify({
      type: 'negative',
      message: usersStore.error || 'Error al cambiar contraseña'
    })
  }
}

const confirmDelete = (user: User) => {
  $q.dialog({
    title: 'Confirmar eliminación',
    message: `¿Estás seguro de que quieres eliminar a ${user.nombre_completo}? Esta acción no se puede deshacer.`,
    cancel: true,
    persistent: true,
    ok: {
      color: 'negative',
      label: 'Eliminar'
    }
  }).onOk(async () => {
    const success = await usersStore.deleteUser(user.id_usuario)

    if (success) {
      $q.notify({
        type: 'positive',
        message: 'Usuario eliminado exitosamente'
      })
    } else {
      $q.notify({
        type: 'negative',
        message: usersStore.error || 'Error al eliminar usuario'
      })
    }
  })
}

// Lifecycle
onMounted(() => {
  loadData()
})
</script>