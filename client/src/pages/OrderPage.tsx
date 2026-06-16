import {
  Box,
  Button,
  Card,
  Heading,
  HStack,
  Spinner,
  Table,
  Text,
} from '@chakra-ui/react'
import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import type { OrderLineItem } from '../api/orders'
import { useOrders } from '../hooks/useOrders'
import { useProducts } from '../hooks/useProducts'

const formatDate = (value: string) => {
  return new Date(value).toLocaleString('zh-CN')
}

const formatMoney = (value: number) => {
  return `¥${value.toFixed(2)}`
}

export default function OrderPage() {
  const { data: orders, isLoading, error } = useOrders()
  const { data: products } = useProducts()

  const productMap = useMemo(() => {
    return new Map((products ?? []).map((product) => [product.id, product.name]))
  }, [products])

  const renderItemSummary = (items: OrderLineItem[]) => {
    return items
      .map((item) => {
        const name = productMap.get(item.product_id) ?? `产品#${item.product_id}`
        return `${name} x${item.quantity}`
      })
      .join('；')
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
        加载订单列表失败，请确认后端 /order/ 接口已实现
      </Text>
    )
  }

  return (
    <Box>
      <HStack justify="space-between" mb={8}>
        <Box>
          <Heading size="lg" mb={2}>
            订单管理
          </Heading>
          <Text color="gray.600">共 {orders?.length ?? 0} 笔订单</Text>
        </Box>
        <Button asChild colorPalette="blue">
          <Link to="/orders/new">新建订单</Link>
        </Button>
      </HStack>

      <Card.Root>
        <Card.Body p={0}>
          {Array.isArray(orders) && orders.length > 0 ? (
            <Table.Root size="sm">
              <Table.Header>
                <Table.Row>
                  <Table.ColumnHeader>订单 ID</Table.ColumnHeader>
                  <Table.ColumnHeader>明细</Table.ColumnHeader>
                  <Table.ColumnHeader>总价</Table.ColumnHeader>
                  <Table.ColumnHeader>备注</Table.ColumnHeader>
                  <Table.ColumnHeader>创建时间</Table.ColumnHeader>
                </Table.Row>
              </Table.Header>
              <Table.Body>
                {orders.map((order) => (
                  <Table.Row key={order.id}>
                    <Table.Cell>
                      <Text fontWeight="medium">#{order.id}</Text>
                    </Table.Cell>
                    <Table.Cell>
                      <Text fontSize="sm" color="gray.700" maxW="360px">
                        {renderItemSummary(order.items)}
                      </Text>
                    </Table.Cell>
                    <Table.Cell>{formatMoney(order.total_price)}</Table.Cell>
                    <Table.Cell>
                      <Text fontSize="sm" color="gray.600" maxW="200px" truncate>
                        {order.remark || '-'}
                      </Text>
                    </Table.Cell>
                    <Table.Cell>{formatDate(order.created_at)}</Table.Cell>
                  </Table.Row>
                ))}
              </Table.Body>
            </Table.Root>
          ) : (
            <Text textAlign="center" color="gray.500" py={10}>
              暂无订单，请先创建
            </Text>
          )}
        </Card.Body>
      </Card.Root>
    </Box>
  )
}
