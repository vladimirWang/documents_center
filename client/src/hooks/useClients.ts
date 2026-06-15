import useSWR from 'swr'
import { fetchClients } from '../api/clients'

export const useClients = () => {
  return useSWR('clients', fetchClients)
}
