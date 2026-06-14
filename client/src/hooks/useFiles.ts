import useSWR from 'swr'
import { fetchFiles } from '../api/files'

export const useFiles = () => {
  return useSWR('files', fetchFiles)
}
