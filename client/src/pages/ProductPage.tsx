import {
  Badge,
  Box,
  Button,
  Card,
  Heading,
  HStack,
  Spinner,
  Table,
  Text,
} from '@chakra-ui/react'
import { Link } from 'react-router-dom'
import { useProducts } from '../hooks/useProducts'

const formatDate = (value?: string) => {
  if (!value) return '-'
  return new Date(value).toLocaleString('zh-CN')
}

const formatPrice = (price: number) => `¥${price.toFixed(2)}`

export default function ProductPage() {
  const { data: products, isLoading, error } = useProducts()

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
        加载产品列表失败
      </Text>
    )
  }

  return (
    <Box>
      <HStack justify="space-between" mb={8}>
        <Box>
          <Heading size="lg" mb={2}>
            产品管理
          </Heading>
          <Text color="gray.600">共 {products?.length ?? 0} 个产品</Text>
        </Box>
        <Button asChild colorPalette="blue">
          <Link to="/products/new">新建产品</Link>
        </Button>
      </HStack>

      <Card.Root>
        <Card.Body p={0}>
          <Table.Root size="sm">
            <Table.Header>
              <Table.Row>
                <Table.ColumnHeader>名称</Table.ColumnHeader>
                <Table.ColumnHeader>描述</Table.ColumnHeader>
                <Table.ColumnHeader>价格</Table.ColumnHeader>
                <Table.ColumnHeader>库存</Table.ColumnHeader>
                <Table.ColumnHeader>向量化</Table.ColumnHeader>
                <Table.ColumnHeader>更新时间</Table.ColumnHeader>
                <Table.ColumnHeader>操作</Table.ColumnHeader>
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {products?.map((product) => (
                <Table.Row key={product.id}>
                  <Table.Cell>
                    <Text
                      asChild
                      fontWeight="medium"
                      color="blue.600"
                      _hover={{ textDecoration: 'underline' }}
                    >
                      <Link to={`/products/${product.id}`}>{product.name}</Link>
                    </Text>
                  </Table.Cell>
                  <Table.Cell>
                    <Text fontSize="sm" color="gray.600" maxW="320px" truncate>
                      {product.description || '-'}
                    </Text>
                  </Table.Cell>
                  <Table.Cell>{formatPrice(product.price)}</Table.Cell>
                  <Table.Cell>{product.balance ?? 0}</Table.Cell>
                  <Table.Cell>
                    <Badge colorPalette={product.vectorized ? 'green' : 'gray'}>
                      {product.vectorized ? '已向量化' : '未向量化'}
                    </Badge>
                  </Table.Cell>
                  <Table.Cell>{formatDate(product.updated_at)}</Table.Cell>
                  <Table.Cell>
                    <HStack gap={2}>
                      <Button asChild size="xs" variant="outline">
                        <Link to={`/products/${product.id}`}>详情</Link>
                      </Button>
                      <Button asChild size="xs" variant="outline" colorPalette="blue">
                        <Link to={`/products/${product.id}/edit`}>编辑</Link>
                      </Button>
                      <Button asChild size="xs" variant="outline">
                        <Link to={`/products/${product.id}/balance`}>库存</Link>
                      </Button>
                    </HStack>
                  </Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table.Root>

          {!products?.length && (
            <Text textAlign="center" color="gray.500" py={10}>
              暂无产品，请先创建
            </Text>
          )}
        </Card.Body>
      </Card.Root>
    </Box>
  )
}
