import apiClient from './client'
import type { ApiResponse } from './auth'

export interface ProductItem {
  id: number
  name: string
  description: string
  price: number
  created_at?: string
  updated_at?: string
}

export interface ProductFormPayload {
  name: string
  description?: string
  price: number
}

export const fetchProducts = async () => {
  const { data } = await apiClient.get<ApiResponse<{ products: ProductItem[] }>>('/product/')
  return data.data?.products ?? []
}

export const fetchProduct = async (productId: number) => {
  const { data } = await apiClient.get<ApiResponse<{ product: ProductItem }>>(`/product/${productId}`)
  if (data.code !== 200 || !data.data?.product) {
    throw new Error(data.message || '产品不存在')
  }
  return data.data.product
}

export const createProduct = async (payload: ProductFormPayload) => {
  const { data } = await apiClient.post<ApiResponse<{ product: ProductItem }>>('/product/', payload)
  if (data.code !== 200) {
    throw new Error(data.message)
  }
  return data
}

export const updateProduct = async (productId: number, payload: ProductFormPayload) => {
  const { data } = await apiClient.put<ApiResponse<{ product: ProductItem }>>(
    `/product/${productId}`,
    payload,
  )
  if (data.code !== 200) {
    throw new Error(data.message)
  }
  return data
}
