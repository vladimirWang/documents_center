import { isAxiosError } from 'axios'
import apiClient, { setToken } from './client'

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  email: string
  password: string
}

export interface UserInfo {
  user_id: number
  username: string
  exp?: number
}

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export const getApiErrorMessage = (error: unknown, fallback: string) => {
  if (error instanceof Error && error.message) return error.message
  if (!isAxiosError(error)) return fallback
  const responseData = error.response?.data as { message?: string; detail?: unknown } | undefined
  if (typeof responseData?.message === 'string') return responseData.message
  const detail = responseData?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail) && detail.length > 0) {
    return detail.map((item) => item.msg).join('；')
  }
  return fallback
}

export const login = async (payload: LoginPayload) => {
  const { data } = await apiClient.post<ApiResponse<string>>('/user/login', payload)
  setToken(data.data)
  return data
}

export const register = async (payload: RegisterPayload) => {
  const { data } = await apiClient.post<ApiResponse<RegisterPayload>>('/user/register', payload)
  return data
}

export const fetchUserInfo = async () => {
  const { data } = await apiClient.get<UserInfo>('/user/user_info')
  return data
}
