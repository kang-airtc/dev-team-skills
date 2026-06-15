import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios'
import { API_BASE } from 'config'

export interface ApiResponse<T = unknown> {
  code: number
  msg: string
  data: T | null
}

const request = axios.create({
  baseURL: API_BASE,
  timeout: 60000,
  headers: { 'Content-Type': 'application/json' },
})

// 请求拦截器：自动带上 access_token
request.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    return config
  },
  (error) => Promise.reject(error),
)

// 响应拦截器：统一处理 code 与 401 自动刷新
request.interceptors.response.use(
  (response: AxiosResponse) => {
    const data = response.data as ApiResponse
    if (data && typeof data.code === 'number') {
      if (data.code === 1104 || data.code === 1105) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        if (typeof window !== 'undefined') window.location.href = '/login'
        return Promise.reject(new Error(data.msg || '认证失败'))
      }
      if (data.code !== 0) {
        return Promise.reject(new Error(data.msg || '请求失败'))
      }
      return data.data
    }
    return response.data
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean }
    const isAuthEndpoint =
      originalRequest?.url?.includes('/login') ||
      originalRequest?.url?.includes('/register') ||
      originalRequest?.url?.includes('/refresh')

    if (error.response?.status === 401 && !isAuthEndpoint && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) throw new Error('No refresh token')

        const response = await axios.post(
          `${API_BASE}/users/refresh`,
          {},
          { headers: { Authorization: `Bearer ${refreshToken}` } },
        )
        const { access_token, refresh_token } = response.data.data
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', refresh_token)

        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access_token}`
        }
        return request(originalRequest)
      } catch (e) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        if (typeof window !== 'undefined') window.location.href = '/login'
        return Promise.reject(e)
      }
    }

    const backend = error.response?.data as ApiResponse | { detail?: string } | undefined
    let msg = error.message
    if (backend && 'msg' in backend) msg = (backend as ApiResponse).msg || msg
    else if (backend && 'detail' in backend) msg = (backend as { detail?: string }).detail || msg
    return Promise.reject(new Error(msg))
  },
)

export const httpGet = <T = unknown>(url: string, params?: any): Promise<T> =>
  request.get(url, { params }) as Promise<T>

export const httpPost = <T = unknown>(url: string, data?: any): Promise<T> =>
  request.post(url, data) as Promise<T>

export const httpPut = <T = unknown>(url: string, data?: any): Promise<T> =>
  request.put(url, data) as Promise<T>

export const httpDelete = <T = unknown>(url: string, params?: any): Promise<T> =>
  request.delete(url, { params }) as Promise<T>

export const httpPatch = <T = unknown>(url: string, data?: any): Promise<T> =>
  request.patch(url, data) as Promise<T>

export default request
