import {
  Box,
  Button,
  Card,
  Center,
  Field,
  Heading,
  Input,
  Link,
  Stack,
  Text,
} from '@chakra-ui/react'
import { useState } from 'react'
import { Link as RouterLink, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { getApiErrorMessage, login } from '../api/auth'
import { getToken } from '../api/client'

export default function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const registeredEmail = (location.state as { registeredEmail?: string } | null)?.registeredEmail
  const [email, setEmail] = useState(registeredEmail ?? '413114463@qq.com')
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
      await login({ email, password })
      navigate('/', { replace: true })
    } catch (err) {
      setError(getApiErrorMessage(err, '登录失败，请检查邮箱和密码'))
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

            {registeredEmail && (
              <Text color="green.600" fontSize="sm" textAlign="center">
                注册成功，请使用邮箱登录
              </Text>
            )}

            <form onSubmit={handleSubmit}>
              <Stack gap={4}>
                <Field.Root required>
                  <Field.Label>邮箱</Field.Label>
                  <Input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="请输入邮箱"
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

            <Text textAlign="center" fontSize="sm" color="gray.600">
              还没有账号？{' '}
              <Link asChild color="blue.600">
                <RouterLink to="/register">去注册</RouterLink>
              </Link>
            </Text>
          </Stack>
        </Card.Body>
      </Card.Root>
    </Center>
  )
}
