import { Box, Button, Card, Heading, Text } from '@chakra-ui/react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getApiErrorMessage } from '../api/auth'
import { createProduct } from '../api/products'
import ProductForm from '../components/ProductForm'

export default function ProductCreatePage() {
  const navigate = useNavigate()
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')
  const [errorMsg, setErrorMsg] = useState('')

  const handleSubmit = async (payload: Parameters<typeof createProduct>[0]) => {
    setSubmitting(true)
    setMessage('')
    setErrorMsg('')

    try {
      const result = await createProduct(payload)
      setMessage(result.message)
      navigate('/products')
    } catch (err) {
      setErrorMsg(getApiErrorMessage(err, '创建产品失败'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Box>
      <Button variant="ghost" mb={4} onClick={() => navigate('/products')}>
        ← 返回列表
      </Button>

      <Heading size="lg" mb={2}>
        新建产品
      </Heading>
      <Text color="gray.600" mb={8}>
        名称和价格为必填项
      </Text>

      <Card.Root maxW="xl">
        <Card.Body>
          <ProductForm submitLabel="创建产品" loading={submitting} onSubmit={handleSubmit} />
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
