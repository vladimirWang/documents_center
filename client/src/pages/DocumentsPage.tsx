import {
  Badge,
  Box,
  Card,
  Heading,
  HStack,
  Spinner,
  Stack,
  Text,
} from '@chakra-ui/react'
import { useNavigate } from 'react-router-dom'
import type { DocumentType } from '../api/documents'
import { useDocuments } from '../hooks/useDocuments'

const typeLabels: Record<DocumentType, string> = {
  pdf: 'PDF',
  doc: '文档',
  sheet: '表格',
  image: '图片',
  note: '笔记',
}

const typeColors: Record<DocumentType, string> = {
  pdf: 'red',
  doc: 'blue',
  sheet: 'green',
  image: 'purple',
  note: 'orange',
}

export default function DocumentsPage() {
  const navigate = useNavigate()
  const { data: documents, isLoading, error } = useDocuments()

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
        加载文档列表失败
      </Text>
    )
  }

  return (
    <Box>
      <Heading size="lg" mb={2}>
        我的文档
      </Heading>
      <Text color="gray.600" mb={8}>
        共 {documents?.length ?? 0} 个文档
      </Text>

      <Stack gap={4}>
        {documents?.map((doc) => (
          <Card.Root
            key={doc.id}
            cursor="pointer"
            _hover={{ shadow: 'md' }}
            onClick={() => navigate(`/documents/${doc.id}`)}
          >
            <Card.Body>
              <HStack justify="space-between" align="start" gap={4}>
                <Box flex={1}>
                  <HStack mb={2} gap={3}>
                    <Heading size="sm">{doc.title}</Heading>
                    <Badge colorPalette={typeColors[doc.type]}>{typeLabels[doc.type]}</Badge>
                  </HStack>
                  <Text fontSize="sm" color="gray.600" mb={1}>
                    {doc.summary}
                  </Text>
                  <Text fontSize="xs" color="gray.500">
                    更新于 {doc.updatedAt}
                  </Text>
                </Box>
              </HStack>
            </Card.Body>
          </Card.Root>
        ))}
      </Stack>
    </Box>
  )
}
