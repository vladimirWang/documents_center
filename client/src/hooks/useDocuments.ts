import useSWR from 'swr'
import { fetchDocumentById, fetchDocuments } from '../api/documents'

export const useDocuments = () => {
  return useSWR('documents', fetchDocuments)
}

export const useDocument = (id: string | undefined) => {
  return useSWR(id ? ['document', id] : null, () => fetchDocumentById(id!))
}
