import { Box, Container, Flex, Heading, HStack, Link, Text } from '@chakra-ui/react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { clearToken } from '../api/client'
import { useAuth } from '../hooks/useAuth'

const navItems = [
  { to: '/', label: '首页' },
  { to: '/documents', label: '我的文档' },
]

export default function Layout() {
  const navigate = useNavigate()
  const { user } = useAuth()

  const handleLogout = () => {
    clearToken()
    navigate('/login')
  }

  return (
    <Box minH="100vh" bg="gray.50">
      <Box as="header" bg="white" borderBottomWidth="1px" borderColor="gray.200" shadow="sm">
        <Container maxW="6xl" py={4}>
          <Flex align="center" justify="space-between" gap={4}>
            <Heading size="md" color="blue.600">
              文档中心
            </Heading>
            <HStack gap={6}>
              {navItems.map((item) => (
                <Link
                  key={item.to}
                  asChild
                  fontWeight="medium"
                  color="gray.700"
                  _hover={{ color: 'blue.600' }}
                >
                  <NavLink
                    to={item.to}
                    style={({ isActive }) => ({
                      color: isActive ? '#2B6CB0' : undefined,
                    })}
                  >
                    {item.label}
                  </NavLink>
                </Link>
              ))}
              {user && (
                <Text fontSize="sm" color="gray.600">
                  {user.username}
                </Text>
              )}
              <Link
                as="button"
                fontSize="sm"
                color="red.500"
                onClick={handleLogout}
                _hover={{ textDecoration: 'underline' }}
              >
                退出登录
              </Link>
            </HStack>
          </Flex>
        </Container>
      </Box>
      <Container maxW="6xl" py={8}>
        <Outlet />
      </Container>
    </Box>
  )
}
