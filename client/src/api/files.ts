import apiClient from './client'
import type { ApiResponse } from './auth'

export interface FileItem {
  id: number
  md5: string
  original_filename: string
  filepath: string
  filesize: number
  filetype: string
  created_at: string
  updated_at: string
}

export interface UploadFileResult {
  filepath: string
}

export const fetchFiles = async () => {
  const { data } = await apiClient.get<ApiResponse<FileItem[]>>('/file/')
  return data.data
}

export const uploadFile = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)

  const { data } = await apiClient.post<ApiResponse<UploadFileResult>>('/file/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}
