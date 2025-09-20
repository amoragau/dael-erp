export interface User {
  id_usuario: number
  username: string
  email: string
  nombre_completo: string
  id_rol: number
  activo: boolean
  ultimo_acceso?: string | null
  fecha_creacion: string
  fecha_modificacion: string
}

export interface Product {
  id: number
  codigo: string
  nombre: string
  descripcion?: string
  precio: number
  stock: number
  categoria_id: number
  marca_id?: number
  unidad_medida_id: number
  created_at: string
  updated_at: string
}

export interface Category {
  id: number
  nombre: string
  descripcion?: string
  created_at: string
  updated_at: string
}

export interface Brand {
  id: number
  nombre: string
  descripcion?: string
  created_at: string
  updated_at: string
}

export interface Role {
  id_rol: number
  nombre_rol: string
  descripcion?: string
  activo: boolean
}

export interface UserCreate {
  username: string
  email: string
  nombre_completo: string
  password: string
  id_rol: number
  activo?: boolean
}

export interface UserUpdate {
  username?: string
  email?: string
  nombre_completo?: string
  password?: string
  id_rol?: number
  activo?: boolean
}

export interface ApiError {
  detail: string
  status_code: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  per_page: number
  pages: number
}