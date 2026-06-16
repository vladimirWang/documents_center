import { Box, Button, Card, Heading, Spinner, Text } from '@chakra-ui/react'
import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getApiErrorMessage } from '../api/auth'
import { updateProduct } from '../api/products'
import ProductForm from '../components/ProductForm'
import { useProduct } from '../hooks/useProducts'

export default function ProductEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: product, isLoading, error } = useProduct(id)
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')
  const [errorMsg, setErrorMsg] = useState('')

  const handleSubmit = async (payload: Parameters<typeof updateProduct>[1]) => {
    if (!id) return

    setSubmitting(true)
    setMessage('')
    setErrorMsg('')

    try {
      const result = await updateProduct(Number(id), payload)
      setMessage(result.message)
      navigate('/products')
    } catch (err) {
      setErrorMsg(getApiErrorMessage(err, '更新产品失败'))
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
        编辑产品
      </Heading>
      <Text color="gray.600" mb={8}>
        名称和价格为必填项
      </Text>

      <Card.Root maxW="xl">
        <Card.Body>
          <ProductForm
            key={product.id}
            initialValues={{
              name: product.name,
              description: product.description,
              price: product.price,
            }}
            submitLabel="保存修改"
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
