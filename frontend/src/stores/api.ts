import { defineStore } from 'pinia'
import axios, { type AxiosInstance } from 'axios'

export interface ApiResponse {
  success: boolean
  data?: any
  message?: string
  error?: string
}

export const useApiStore = defineStore('api', () => {
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

  const apiClient: AxiosInstance = axios.create({
    baseURL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  })

  apiClient.interceptors.request.use(
    (config) => {
      console.log('Request:', config)
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  apiClient.interceptors.response.use(
    (response) => {
      console.log('Response:', response)
      return response
    },
    (error) => {
      console.error('API Error:', error)
      return Promise.reject(error)
    }
  )

  const testConnection = async (): Promise<ApiResponse> => {
    try {
      const response = await apiClient.get('/health')
      return {
        success: true,
        data: response.data,
        message: 'Conexión exitosa'
      }
    } catch (error: any) {
      return {
        success: false,
        error: error.message || 'Error de conexión',
        message: 'No se pudo conectar al servidor'
      }
    }
  }

  const get = async (url: string): Promise<ApiResponse> => {
    try {
      const response = await apiClient.get(url)
      return {
        success: true,
        data: response.data
      }
    } catch (error: any) {
      return {
        success: false,
        error: error.message
      }
    }
  }

  const post = async (url: string, data: any): Promise<ApiResponse> => {
    try {
      const response = await apiClient.post(url, data)
      return {
        success: true,
        data: response.data
      }
    } catch (error: any) {
      return {
        success: false,
        error: error.message
      }
    }
  }

  const put = async (url: string, data: any): Promise<ApiResponse> => {
    try {
      const response = await apiClient.put(url, data)
      return {
        success: true,
        data: response.data
      }
    } catch (error: any) {
      return {
        success: false,
        error: error.message
      }
    }
  }

  const del = async (url: string): Promise<ApiResponse> => {
    try {
      const response = await apiClient.delete(url)
      return {
        success: true,
        data: response.data
      }
    } catch (error: any) {
      return {
        success: false,
        error: error.message
      }
    }
  }

  const patch = async (url: string, data?: any): Promise<ApiResponse> => {
    try {
      const response = await apiClient.patch(url, data)
      return {
        success: true,
        data: response.data
      }
    } catch (error: any) {
      return {
        success: false,
        error: error.message
      }
    }
  }

  const uploadFile = async (url: string, formData: FormData): Promise<ApiResponse> => {
    try {
      const response = await apiClient.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return {
        success: true,
        data: response.data
      }
    } catch (error: any) {
      return {
        success: false,
        error: error.message
      }
    }
  }

  const downloadFile = async (url: string): Promise<Blob> => {
    try {
      const response = await apiClient.get(url, {
        responseType: 'blob'
      })
      return response.data
    } catch (error: any) {
      console.error('Error downloading file:', error)
      throw error
    }
  }

  return {
    apiClient,
    testConnection,
    get,
    post,
    put,
    patch,
    delete: del,
    uploadFile,
    downloadFile
  }
})