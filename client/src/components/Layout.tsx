import { Box, Flex, Heading, Link, Stack, Text } from '@chakra-ui/react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { clearToken } from '../api/client'
import { useAuth } from '../hooks/useAuth'

const navItems = [
  { to: '/', label: '首页' },
  { to: '/documents', label: '我的文档' },
  { to: '/files', label: '我的文件' },
  { to: '/clients', label: '客户管理' },
  { to: '/products', label: '产品管理' },
  { to: '/orders', label: '订单管理' },
]

export default function Layout() {
  const navigate = useNavigate()
  const { user } = useAuth()

  const handleLogout = () => {
    clearToken()
    navigate('/login')
  }

  return (
    <Flex minH="100vh" bg="gray.50">
      <Box
        as="aside"
        w="240px"
        flexShrink={0}
        bg="white"
        borderRightWidth="1px"
        borderColor="gray.200"
        display="flex"
        flexDirection="column"
      >
        <Box px={5} py={6} borderBottomWidth="1px" borderColor="gray.100">
          <Heading size="md" color="blue.600">
            文档中心
          </Heading>
        </Box>

        <Stack as="nav" gap={1} px={3} py={4} flex="1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              style={{ textDecoration: 'none' }}
            >
              {({ isActive }) => (
                <Box
                  px={3}
                  py={2.5}
                  rounded="md"
                  fontWeight="medium"
                  color={isActive ? 'blue.600' : 'gray.700'}
                  bg={isActive ? 'blue.50' : 'transparent'}
                  _hover={{
                    bg: isActive ? 'blue.50' : 'gray.100',
                    color: 'blue.600',
                  }}
                >
                  {item.label}
                </Box>
              )}
            </NavLink>
          ))}
        </Stack>

        <Box px={5} py={4} borderTopWidth="1px" borderColor="gray.100">
          {user && (
            <Text fontSize="sm" color="gray.600" mb={2} truncate>
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
        </Box>
      </Box>

      <Box as="main" flex="1" minW={0} p={8}>
        <Outlet />
      </Box>
    </Flex>
  )
}
