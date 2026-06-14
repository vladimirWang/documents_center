import apiClient, { setToken } from './client'

export interface LoginPayload {
  username: string
  password: string
}

export interface UserInfo {
  user_id: number
  username: string
  exp?: number
}

export const login = async (payload: LoginPayload) => {
  const { data } = await apiClient.post<{ token: string }>('/user/login', payload)
  setToken(data.token)
  return data
}

export const fetchUserInfo = async () => {
  const { data } = await apiClient.get<UserInfo>('/user/user_info')
  return data
}
