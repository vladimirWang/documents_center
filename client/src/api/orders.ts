import apiClient from './client'
import type { ApiResponse } from './auth'

export interface OrderLinePayload {
  product_id: number
  quantity: number
  price: number
}

export interface OrderCreatePayload {
  items: OrderLinePayload[]
  remark?: string
}

export interface OrderLineItem {
  product_id: number
  quantity: number
  price: number
}

export interface OrderItem {
  id: number
  total_price: number
  remark: string | null
  items: OrderLineItem[]
  created_at: string
  updated_at: string
}

export const fetchOrders = async () => {
  const { data } = await apiClient.get<ApiResponse<{ orders: OrderItem[] }>>('/order/')
  return data.data?.orders ?? []
}

export const fetchOrder = async (orderId: number) => {
  const { data } = await apiClient.get<ApiResponse<{ order: OrderItem }>>(`/order/${orderId}`)
  if (data.code !== 200) {
    throw new Error(data.message)
  }
  return data.data?.order
}

export const createOrder = async (payload: OrderCreatePayload) => {
  const { data } = await apiClient.post<ApiResponse<{ order: OrderItem }>>('/order/', payload)
  if (data.code !== 200) {
    throw new Error(data.message)
  }
  return data
}
