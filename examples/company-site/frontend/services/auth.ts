import { httpPost, httpGet } from '@/utils/request'

export interface User {
  id: number
  username: string
  email: string
  full_name: string | null
  is_active: boolean
  is_superuser: boolean
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  full_name?: string
}

export type RegisterResponse = User

export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  const result = await httpPost<LoginResponse>('/users/login', data)
  localStorage.setItem('access_token', result.access_token)
  localStorage.setItem('refresh_token', result.refresh_token)
  return result
}

export const register = async (data: RegisterRequest): Promise<RegisterResponse> => {
  return httpPost<RegisterResponse>('/users/register', data)
}

export const getCurrentUser = async (): Promise<User> => {
  return httpGet<User>('/users/me')
}

export const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  if (typeof window !== 'undefined') {
    window.location.href = '/login'
  }
}

export const isAuthenticated = (): boolean => {
  if (typeof window === 'undefined') return false
  return !!localStorage.getItem('access_token')
}
