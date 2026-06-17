import {
  Badge,
  Box,
  Button,
  Card,
  Heading,
  HStack,
  SimpleGrid,
  Spinner,
  Text,
} from '@chakra-ui/react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useProduct } from '../hooks/useProducts'

const formatDate = (value?: string) => {
  if (!value) return '-'
  return new Date(value).toLocaleString('zh-CN')
}

const formatPrice = (price: number) => `¥${price.toFixed(2)}`

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: product, isLoading, error } = useProduct(id)

  if (isLoading) {
    return (
      <Box textAlign="center" py={20}>
        <Spinner size="lg" color="blue.500" />
      </Box>
    )
  }

  if (error || !product) {
    return (
      <Box textAlign="center" py={20}>
        <Text color="red.500" mb={4}>
          产品不存在或加载失败
        </Text>
        <Button colorPalette="blue" onClick={() => navigate('/products')}>
          返回列表
        </Button>
      </Box>
    )
  }

  return (
    <Box>
      <Button variant="ghost" mb={4} onClick={() => navigate('/products')}>
        ← 返回列表
      </Button>

      <Card.Root>
        <Card.Body p={8}>
          <HStack mb={6} gap={3} flexWrap="wrap">
            <Heading size="lg">{product.name}</Heading>
            <Badge colorPalette={product.vectorized ? 'green' : 'gray'}>
              {product.vectorized ? '已向量化' : '未向量化'}
            </Badge>
          </HStack>

          <SimpleGrid columns={{ base: 1, md: 2 }} gap={6} mb={8}>
            <Box>
              <Text fontSize="sm" color="gray.500" mb={1}>
                价格
              </Text>
              <Text fontWeight="medium">{formatPrice(product.price)}</Text>
            </Box>
            <Box>
              <Text fontSize="sm" color="gray.500" mb={1}>
                库存
              </Text>
              <Text fontWeight="medium">{product.balance ?? 0}</Text>
            </Box>
            <Box>
              <Text fontSize="sm" color="gray.500" mb={1}>
                创建时间
              </Text>
              <Text>{formatDate(product.created_at)}</Text>
            </Box>
            <Box>
              <Text fontSize="sm" color="gray.500" mb={1}>
                更新时间
              </Text>
              <Text>{formatDate(product.updated_at)}</Text>
            </Box>
          </SimpleGrid>

          <Box mb={8}>
            <Text fontSize="sm" color="gray.500" mb={2}>
              描述
            </Text>
            <Text color="gray.700" lineHeight="tall" whiteSpace="pre-wrap">
              {product.description || '暂无描述'}
            </Text>
          </Box>

          <HStack gap={3}>
            <Button asChild colorPalette="blue">
              <Link to={`/products/${product.id}/edit`}>编辑</Link>
            </Button>
            <Button asChild variant="outline">
              <Link to={`/products/${product.id}/balance`}>修改库存</Link>
            </Button>
          </HStack>
        </Card.Body>
      </Card.Root>
    </Box>
  )
}
