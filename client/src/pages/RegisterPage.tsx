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
import { Link as RouterLink, Navigate, useNavigate } from 'react-router-dom'
import { getApiErrorMessage, register } from '../api/auth'
import { getToken } from '../api/client'

export default function RegisterPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  if (getToken()) {
    return <Navigate to="/" replace />
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (password !== confirmPassword) {
      setError('两次输入的密码不一致')
      return
    }

    if (password.length < 6 || password.length > 8) {
      setError('密码长度需在 6-8 位之间')
      return
    }

    setLoading(true)

    try {
      await register({ email, password })
      navigate('/login', { replace: true, state: { registeredEmail: email } })
    } catch (err) {
      setError(getApiErrorMessage(err, '注册失败，请稍后重试'))
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
                注册账号
              </Heading>
              <Text color="gray.600">创建账号以访问文档中心</Text>
            </Box>

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
                    placeholder="6-8 位密码"
                  />
                  <Field.HelperText>密码长度为 6-8 位</Field.HelperText>
                </Field.Root>

                <Field.Root required>
                  <Field.Label>确认密码</Field.Label>
                  <Input
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="请再次输入密码"
                  />
                </Field.Root>

                {error && (
                  <Text color="red.500" fontSize="sm">
                    {error}
                  </Text>
                )}

                <Button type="submit" colorPalette="blue" loading={loading} w="full">
                  注册
                </Button>
              </Stack>
            </form>

            <Text textAlign="center" fontSize="sm" color="gray.600">
              已有账号？{' '}
              <Link asChild color="blue.600">
                <RouterLink to="/login">去登录</RouterLink>
              </Link>
            </Text>
          </Stack>
        </Card.Body>
      </Card.Root>
    </Center>
  )
}
