import useSWR from 'swr'
import { fetchProduct, fetchProducts } from '../api/products'

export const useProducts = () => {
  return useSWR('products', fetchProducts)
}

export const useProduct = (productId?: string) => {
  return useSWR(productId ? ['product', productId] : null, () =>
    fetchProduct(Number(productId)),
  )
}
