import apiClient from './client'
import type { ApiResponse } from './auth'

export type ClientStatus = 'active' | 'inactive'

export interface ClientItem {
  id: number
  name: string
  phone: string
  email: string
  status: ClientStatus
  notes: string
  created_at: string
  updated_at: string
}

export interface CreateClientPayload {
  name: string
  phone: string
  email: string
  status?: ClientStatus
  notes?: string
}

export interface UpdateClientPayload {
  name?: string
  phone?: string
  email?: string
  status?: ClientStatus
  notes?: string
}

export const fetchClients = async () => {
  const { data } = await apiClient.get<ApiResponse<ClientItem[]>>('/client/')
  return data.data
}

export const createClient = async (payload: CreateClientPayload) => {
  const { data } = await apiClient.post<ApiResponse<ClientItem>>('/client/', payload)
  if (data.code !== 200) {
    throw new Error(data.message)
  }
  return data
}

export const updateClient = async (clientId: number, payload: UpdateClientPayload) => {
  const { data } = await apiClient.put<ApiResponse<ClientItem>>(`/client/${clientId}`, payload)
  if (data.code !== 200) {
    throw new Error(data.message)
  }
  return data
}

export const deleteClient = async (clientId: number) => {
  const { data } = await apiClient.delete<ApiResponse<null>>(`/client/${clientId}`)
  if (data.code !== 200) {
    throw new Error(data.message)
  }
  return data
}
