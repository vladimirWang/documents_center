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

export const getApiErrorMessage = (error: unknown, fallback: string) => {
  if (!isAxiosError(error)) return fallback
  const detail = error.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail) && detail.length > 0) {
    return detail.map((item) => item.msg).join('；')
  }
  return fallback
}

export const login = async (payload: LoginPayload) => {
  const { data } = await apiClient.post<{ token: string }>('/user/login', payload)
  setToken(data.token)
  return data
}

export const register = async (payload: RegisterPayload) => {
  const { data } = await apiClient.post<{ success: boolean; data: RegisterPayload }>(
    '/user/register',
    payload,
  )
  return data
}

export const fetchUserInfo = async () => {
  const { data } = await apiClient.get<UserInfo>('/user/user_info')
  return data
}
