import { Box, Button, Card, Heading, Spinner, Text } from '@chakra-ui/react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getApiErrorMessage } from '../api/auth'
import { createOrder } from '../api/orders'
import OrderForm from '../components/OrderForm'
import { useProducts } from '../hooks/useProducts'

export default function OrderCreatePage() {
  const navigate = useNavigate()
  const { data: products, isLoading, error } = useProducts()
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')
  const [errorMsg, setErrorMsg] = useState('')

  const handleSubmit = async (payload: Parameters<typeof createOrder>[0]) => {
    setSubmitting(true)
    setMessage('')
    setErrorMsg('')

    try {
      const result = await createOrder(payload)
      setMessage(result.message)
      navigate('/orders')
    } catch (err) {
      setErrorMsg(getApiErrorMessage(err, '创建订单失败'))
    } finally {
      setSubmitting(false)
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
        加载产品列表失败，无法创建订单
      </Text>
    )
  }

  return (
    <Box>
      <Button variant="ghost" mb={4} onClick={() => navigate('/orders')}>
        ← 返回列表
      </Button>

      <Heading size="lg" mb={2}>
        新建订单
      </Heading>
      <Text color="gray.600" mb={8}>
        请至少添加一条产品明细
      </Text>

      <Card.Root maxW="4xl">
        <Card.Body>
          <OrderForm
            products={products ?? []}
            submitLabel="创建订单"
            loading={submitting}
            onSubmit={handleSubmit}
          />
          {message && (
            <Text color="green.600" fontSize="sm" mt={4}>
              {message}
            </Text>
          )}
          {errorMsg && (
            <Text color="red.500" fontSize="sm" mt={4}>
              {errorMsg}
            </Text>
          )}
        </Card.Body>
      </Card.Root>
    </Box>
  )
}
