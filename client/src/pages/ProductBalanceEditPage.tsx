import { Box, Button, Card, Heading, HStack, Spinner, Text } from '@chakra-ui/react'
import { useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { getApiErrorMessage } from '../api/auth'
import { updateProductBalance } from '../api/products'
import ProductBalanceForm from '../components/ProductBalanceForm'
import { useProduct } from '../hooks/useProducts'

export default function ProductBalanceEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: product, isLoading, error } = useProduct(id)
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')
  const [errorMsg, setErrorMsg] = useState('')

  const handleSubmit = async (payload: Parameters<typeof updateProductBalance>[1]) => {
    if (!id) return

    setSubmitting(true)
    setMessage('')
    setErrorMsg('')

    try {
      const result = await updateProductBalance(Number(id), payload)
      setMessage(result.message)
      navigate('/products')
    } catch (err) {
      setErrorMsg(getApiErrorMessage(err, '更新库存失败'))
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

      <Heading size="lg" mb={2}>
        修改库存
      </Heading>
      <Text color="gray.600" mb={2}>
        产品：{product.name}
      </Text>
      <Text color="gray.600" mb={8}>
        当前库存：{product.balance ?? 0}
      </Text>

      <HStack gap={3} mb={6}>
        <Button asChild size="sm" variant="outline">
          <Link to={`/products/${product.id}/edit`}>编辑产品信息</Link>
        </Button>
      </HStack>

      <Card.Root maxW="xl">
        <Card.Body>
          <ProductBalanceForm
            key={product.id}
            initialBalance={product.balance ?? 0}
            submitLabel="保存库存"
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
