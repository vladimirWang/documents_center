import { Box, Button, Card, Heading, Text } from '@chakra-ui/react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getApiErrorMessage } from '../api/auth'
import { createClient } from '../api/clients'
import ClientForm from '../components/ClientForm'

export default function ClientCreatePage() {
  const navigate = useNavigate()
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')
  const [errorMsg, setErrorMsg] = useState('')

  const handleSubmit = async (payload: Parameters<typeof createClient>[0]) => {
    setSubmitting(true)
    setMessage('')
    setErrorMsg('')

    try {
      const result = await createClient(payload)
      setMessage(result.message)
      navigate('/clients')
    } catch (err) {
      setErrorMsg(getApiErrorMessage(err, '创建顾客失败'))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Box>
      <Button variant="ghost" mb={4} onClick={() => navigate('/clients')}>
        ← 返回列表
      </Button>

      <Heading size="lg" mb={2}>
        新建顾客
      </Heading>
      <Text color="gray.600" mb={8}>
        名称为必填项
      </Text>

      <Card.Root maxW="3xl">
        <Card.Body>
          <ClientForm submitLabel="创建顾客" loading={submitting} onSubmit={handleSubmit} />
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
