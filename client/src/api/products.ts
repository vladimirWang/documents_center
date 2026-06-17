import apiClient from './client'
import type { ApiResponse } from './auth'

export interface ProductItem {
  id: number
  name: string
  description: string
  price: number
  balance: number
  vectorized: boolean
  created_at?: string
  updated_at?: string
}

export interface ProductBalancePayload {
  balance: number
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

export const updateProductBalance = async (
  productId: number,
  payload: ProductBalancePayload,
) => {
  const { data } = await apiClient.put<ApiResponse<{ product: ProductItem }>>(
    `/product/${productId}/balance`,
    null,
    { params: payload },
  )
  if (data.code !== 200) {
    throw new Error(data.message)
  }
  return data
}
