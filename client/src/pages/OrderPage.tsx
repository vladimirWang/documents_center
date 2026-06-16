import {
  Box,
  Button,
  Card,
  Field,
  Heading,
  HStack,
  IconButton,
  Input,
  NativeSelect,
  Spinner,
  Stack,
  Table,
  Text,
  Textarea,
} from '@chakra-ui/react'
import { useMemo, useState } from 'react'
import { getApiErrorMessage } from '../api/auth'
import { createOrder, type OrderCreatePayload, type OrderLinePayload } from '../api/orders'
import { useOrders } from '../hooks/useOrders'
import { useProducts } from '../hooks/useProducts'

const emptyLine = (): OrderLinePayload => ({
  product_id: 0,
  quantity: 1,
  price: 0,
})

const emptyForm = (): OrderCreatePayload => ({
  items: [emptyLine()],
  remark: '',
})

const formatDate = (value: string) => {
  return new Date(value).toLocaleString('zh-CN')
}

const formatMoney = (value: number) => {
  return `¥${value.toFixed(2)}`
}

export default function OrderPage() {
  const { data: orders, isLoading, error, mutate } = useOrders()
  const { data: products } = useProducts()
  const [form, setForm] = useState<OrderCreatePayload>(emptyForm())
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')
  const [errorMsg, setErrorMsg] = useState('')

  const productMap = useMemo(() => {
    return new Map((products ?? []).map((product) => [product.id, product.name]))
  }, [products])

  const estimatedTotal = useMemo(() => {
    return form.items.reduce((sum, item) => sum + item.quantity * item.price, 0)
  }, [form.items])

  const resetForm = () => {
    setForm(emptyForm())
  }

  const updateLine = (index: number, patch: Partial<OrderLinePayload>) => {
    setForm((prev) => ({
      ...prev,
      items: prev.items.map((item, i) => (i === index ? { ...item, ...patch } : item)),
    }))
  }

  const handleProductChange = (index: number, productId: number) => {
    const product = products?.find((item) => item.id === productId)
    updateLine(index, {
      product_id: productId,
      price: product?.price ?? 0,
    })
  }

  const addLine = () => {
    setForm((prev) => ({
      ...prev,
      items: [...prev.items, emptyLine()],
    }))
  }

  const removeLine = (index: number) => {
    setForm((prev) => ({
      ...prev,
      items: prev.items.length > 1 ? prev.items.filter((_, i) => i !== index) : prev.items,
    }))
  }

  const handleSubmit = async () => {
    const validItems = form.items.filter((item) => item.product_id > 0)
    if (!validItems.length) {
      setErrorMsg('请至少添加一条有效的产品明细')
      return
    }

    if (validItems.some((item) => item.quantity <= 0 || item.price <= 0)) {
      setErrorMsg('数量和单价必须大于 0')
      return
    }

    setSubmitting(true)
    setMessage('')
    setErrorMsg('')

    try {
      const result = await createOrder({
        items: validItems,
        remark: form.remark?.trim() || '',
      })
      setMessage(result.message || '订单创建成功')
      resetForm()
      await mutate()
    } catch (err) {
      setErrorMsg(getApiErrorMessage(err, '创建订单失败'))
    } finally {
      setSubmitting(false)
    }
  }

  const renderItemSummary = (items: OrderLinePayload[]) => {
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
      <Heading size="lg" mb={2}>
        订单管理
      </Heading>
      <Text color="gray.600" mb={8}>
        共 {orders?.length ?? 0} 笔订单
      </Text>

      <Card.Root mb={8}>
        <Card.Body>
          <Stack gap={4}>
            <Heading size="sm">新增订单</Heading>

            <Stack gap={3}>
              {form.items.map((item, index) => (
                <HStack key={index} gap={3} align="end" flexWrap="wrap">
                  <Field.Root required minW="220px">
                    <Field.Label>产品</Field.Label>
                    <NativeSelect.Root>
                      <NativeSelect.Field
                        value={item.product_id || ''}
                        onChange={(e) => handleProductChange(index, Number(e.target.value))}
                      >
                        <option value="">请选择产品</option>
                        {(products ?? []).map((product) => (
                          <option key={product.id} value={product.id}>
                            {product.name}
                          </option>
                        ))}
                      </NativeSelect.Field>
                    </NativeSelect.Root>
                  </Field.Root>

                  <Field.Root required maxW="120px">
                    <Field.Label>数量</Field.Label>
                    <Input
                      type="number"
                      min={1}
                      value={item.quantity}
                      onChange={(e) => updateLine(index, { quantity: Number(e.target.value) })}
                    />
                  </Field.Root>

                  <Field.Root required maxW="140px">
                    <Field.Label>单价</Field.Label>
                    <Input
                      type="number"
                      min={0.01}
                      step={0.01}
                      value={item.price}
                      onChange={(e) => updateLine(index, { price: Number(e.target.value) })}
                    />
                  </Field.Root>

                  <IconButton
                    aria-label="删除明细"
                    variant="outline"
                    colorPalette="red"
                    onClick={() => removeLine(index)}
                    disabled={form.items.length === 1}
                  >
                    删
                  </IconButton>
                </HStack>
              ))}
            </Stack>

            <Button alignSelf="start" variant="outline" onClick={addLine}>
              添加明细
            </Button>

            <Field.Root>
              <Field.Label>备注</Field.Label>
              <Textarea
                value={form.remark}
                onChange={(e) => setForm({ ...form, remark: e.target.value })}
                placeholder="订单备注"
                rows={2}
              />
            </Field.Root>

            <Text fontSize="sm" color="gray.600">
              预估总价：{formatMoney(estimatedTotal)}
            </Text>

            <HStack gap={3}>
              <Button colorPalette="blue" loading={submitting} onClick={handleSubmit}>
                创建订单
              </Button>
              <Button variant="outline" onClick={resetForm}>
                重置
              </Button>
            </HStack>

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
