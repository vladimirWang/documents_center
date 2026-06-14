import {
  Badge,
  Box,
  Card,
  Heading,
  HStack,
  Input,
  Spinner,
  Stack,
  Table,
  Text,
} from '@chakra-ui/react'
import { useRef, useState } from 'react'
import { getApiErrorMessage } from '../api/auth'
import { uploadFile } from '../api/files'
import { useFiles } from '../hooks/useFiles'

const formatFileSize = (size: number) => {
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / 1024 / 1024).toFixed(1)} MB`
}

const formatDate = (value: string) => {
  return new Date(value).toLocaleString('zh-CN')
}

export default function FilesPage() {
  const inputRef = useRef<HTMLInputElement>(null)
  const { data: files, isLoading, error, mutate } = useFiles()
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')
  const [errorMsg, setErrorMsg] = useState('')

  const handleUpload = async (selectedFile: File | undefined) => {
    if (!selectedFile) return

    setUploading(true)
    setMessage('')
    setErrorMsg('')

    try {
      const result = await uploadFile(selectedFile)
      setMessage(result.message)
      await mutate()
    } catch (err) {
      setErrorMsg(getApiErrorMessage(err, '文件上传失败'))
    } finally {
      setUploading(false)
      if (inputRef.current) {
        inputRef.current.value = ''
      }
    }
  }

  if (isLoading) {
    return (
      <Box textAlign="center" py={20}>
        <Spinner size="lg" color="blue.500" />
      </Box>
    )
  }

  if (error) {
    return (
      <Text color="red.500" textAlign="center" py={20}>
        加载文件列表失败
      </Text>
    )
  }

  return (
    <Box>
      <Heading size="lg" mb={2}>
        我的文件
      </Heading>
      <Text color="gray.600" mb={8}>
        共 {files?.length ?? 0} 个文件
      </Text>

      <Card.Root mb={8}>
        <Card.Body>
          <Stack gap={4}>
            <Heading size="sm">上传文件</Heading>
            <HStack gap={4} align="center" flexWrap="wrap">
              <Input
                ref={inputRef}
                type="file"
                maxW="sm"
                onChange={(e) => handleUpload(e.target.files?.[0])}
              />
            </HStack>
            {uploading && (
              <HStack gap={2}>
                <Spinner size="sm" />
                <Text fontSize="sm" color="gray.600">
                  上传中...
                </Text>
              </HStack>
            )}
            {message && (
              <Text color="green.600" fontSize="sm">
                {message}
              </Text>
            )}
            {errorMsg && (
              <Text color="red.500" fontSize="sm">
                {errorMsg}
              </Text>
            )}
          </Stack>
        </Card.Body>
      </Card.Root>

      <Card.Root>
        <Card.Body p={0}>
          <Table.Root size="sm">
            <Table.Header>
              <Table.Row>
                <Table.ColumnHeader>文件名</Table.ColumnHeader>
                <Table.ColumnHeader>类型</Table.ColumnHeader>
                <Table.ColumnHeader>大小</Table.ColumnHeader>
                <Table.ColumnHeader>MD5</Table.ColumnHeader>
                <Table.ColumnHeader>上传时间</Table.ColumnHeader>
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {files?.map((file) => (
                <Table.Row key={file.id}>
                  <Table.Cell>
                    <Text fontWeight="medium">{file.original_filename}</Text>
                    <Text fontSize="xs" color="gray.500">
                      {file.filepath}
                    </Text>
                  </Table.Cell>
                  <Table.Cell>
                    <Badge colorPalette="blue">{file.filetype || '未知'}</Badge>
                  </Table.Cell>
                  <Table.Cell>{formatFileSize(file.filesize)}</Table.Cell>
                  <Table.Cell>
                    <Text fontSize="xs" fontFamily="mono">
                      {file.md5.slice(0, 8)}...
                    </Text>
                  </Table.Cell>
                  <Table.Cell>{formatDate(file.created_at)}</Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table.Root>

          {!files?.length && (
            <Text textAlign="center" color="gray.500" py={10}>
              暂无文件，请先上传
            </Text>
          )}
        </Card.Body>
      </Card.Root>
    </Box>
  )
}
