import useSWR from 'swr'
import { fetchOrder, fetchOrders } from '../api/orders'

export const useOrders = () => {
  return useSWR('orders', fetchOrders)
}

export const useOrder = (orderId?: string) => {
  return useSWR(orderId ? ['order', orderId] : null, () => fetchOrder(Number(orderId)))
}
