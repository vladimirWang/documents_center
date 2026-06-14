import {
  Badge,
  Box,
  Button,
  Card,
  Heading,
  HStack,
  Spinner,
  Text,
} from '@chakra-ui/react'
import { useNavigate, useParams } from 'react-router-dom'
import type { DocumentType } from '../api/documents'
import { useDocument } from '../hooks/useDocuments'

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

export default function DocumentDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: document, isLoading, error } = useDocument(id)

  if (isLoading) {
    return (
      <Box textAlign="center" py={20}>
        <Spinner size="lg" color="blue.500" />
      </Box>
    )
  }

  if (error || !document) {
    return (
      <Box textAlign="center" py={20}>
        <Text color="red.500" mb={4}>
          文档不存在或加载失败
        </Text>
        <Button colorPalette="blue" onClick={() => navigate('/documents')}>
          返回列表
        </Button>
      </Box>
    )
  }

  return (
    <Box>
      <Button variant="ghost" mb={4} onClick={() => navigate('/documents')}>
        ← 返回列表
      </Button>

      <Card.Root>
        <Card.Body p={8}>
          <HStack mb={4} gap={3}>
            <Heading size="lg">{document.title}</Heading>
            <Badge colorPalette={typeColors[document.type]}>
              {typeLabels[document.type]}
            </Badge>
          </HStack>
          <Text fontSize="sm" color="gray.500" mb={6}>
            更新于 {document.updatedAt}
          </Text>
          <Text color="gray.700" lineHeight="tall" whiteSpace="pre-wrap">
            {document.content}
          </Text>
        </Card.Body>
      </Card.Root>
    </Box>
  )
}
