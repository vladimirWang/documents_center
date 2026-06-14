import {
  Box,
  Button,
  Card,
  Center,
  Field,
  Heading,
  Input,
  Stack,
  Text,
} from '@chakra-ui/react'
import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { login } from '../api/auth'
import { getToken } from '../api/client'

export default function LoginPage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('mike')
  const [password, setPassword] = useState('123456')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  if (getToken()) {
    return <Navigate to="/" replace />
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await login({ username, password })
      navigate('/', { replace: true })
    } catch {
      setError('登录失败，请检查用户名和密码')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Center minH="100vh" bg="gray.50" px={4}>
      <Card.Root maxW="md" w="full" shadow="lg">
        <Card.Body p={8}>
          <Stack gap={6}>
            <Box textAlign="center">
              <Heading size="lg" mb={2}>
                文档中心
              </Heading>
              <Text color="gray.600">登录以访问你的文档</Text>
            </Box>

            <form onSubmit={handleSubmit}>
              <Stack gap={4}>
                <Field.Root required>
                  <Field.Label>用户名</Field.Label>
                  <Input
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="请输入用户名"
                  />
                </Field.Root>

                <Field.Root required>
                  <Field.Label>密码</Field.Label>
                  <Input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="请输入密码"
                  />
                </Field.Root>

                {error && (
                  <Text color="red.500" fontSize="sm">
                    {error}
                  </Text>
                )}

                <Button type="submit" colorPalette="blue" loading={loading} w="full">
                  登录
                </Button>
              </Stack>
            </form>
          </Stack>
        </Card.Body>
      </Card.Root>
    </Center>
  )
}
