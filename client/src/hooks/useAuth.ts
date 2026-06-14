import useSWR from 'swr'
import { fetchUserInfo } from '../api/auth'
import { getToken } from '../api/client'

export const useAuth = () => {
  const token = getToken()

  const { data, error, isLoading, mutate } = useSWR(
    token ? '/user/user_info' : null,
    fetchUserInfo,
    { revalidateOnFocus: false },
  )

  return {
    user: data,
    isAuthenticated: Boolean(token && data),
    isLoading: Boolean(token && isLoading),
    error,
    mutate,
  }
}
