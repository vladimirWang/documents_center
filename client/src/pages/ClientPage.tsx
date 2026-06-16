import {
  Badge,
  Box,
  Button,
  Card,
  Heading,
  HStack,
  Spinner,
  Table,
  Text,
} from '@chakra-ui/react'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { getApiErrorMessage } from '../api/auth'
import {
  deleteClient,
  updateClient,
  type ClientItem,
  type ClientStatus,
} from '../api/clients'
import ClientForm from '../components/ClientForm'
import { useClients } from '../hooks/useClients'

const formatDate = (value: string) => {
  return new Date(value).toLocaleString('zh-CN')
}

const statusLabel: Record<ClientStatus, string> = {
  active: '活跃',
  inactive: '停用',
}

export default function ClientPage() {
  const { data: clients, isLoading, error, mutate } = useClients()
  const [editingClient, setEditingClient] = useState<ClientItem | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [deletingId, setDeletingId] = useState<number | null>(null)
  const [message, setMessage] = useState('')
  const [errorMsg, setErrorMsg] = useState('')

  const handleUpdate = async (payload: Parameters<typeof updateClient>[1]) => {
    if (!editingClient) return

    setSubmitting(true)
    setMessage('')
    setErrorMsg('')

    try {
      const result = await updateClient(editingClient.id, payload)
      setMessage(result.message)
      setEditingClient(null)
      await mutate()
    } catch (err) {
      setErrorMsg(getApiErrorMessage(err, '更新顾客失败'))
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async (clientId: number) => {
    if (!window.confirm('确定要删除该顾客吗？')) return

    setDeletingId(clientId)
    setMessage('')
    setErrorMsg('')

    try {
      const result = await deleteClient(clientId)
      setMessage(result.message)
      if (editingClient?.id === clientId) setEditingClient(null)
      await mutate()
    } catch (err) {
      setErrorMsg(getApiErrorMessage(err, '删除顾客失败'))
    } finally {
      setDeletingId(null)
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
        加载顾客列表失败，请确认后端 /client/ 接口已实现
      </Text>
    )
  }

  return (
    <Box>
      <HStack justify="space-between" mb={8}>
        <Box>
          <Heading size="lg" mb={2}>
            顾客管理
          </Heading>
          <Text color="gray.600">共 {clients?.length ?? 0} 位顾客</Text>
        </Box>
        <Button asChild colorPalette="blue">
          <Link to="/clients/new">新建顾客</Link>
        </Button>
      </HStack>

      {editingClient && (
        <Card.Root mb={8}>
          <Card.Body>
            <Heading size="sm" mb={4}>
              编辑顾客
            </Heading>
            <ClientForm
              key={editingClient.id}
              initialValues={{
                name: editingClient.name,
                phone: editingClient.phone,
                email: editingClient.email,
                status: editingClient.status,
                notes: editingClient.notes,
              }}
              submitLabel="保存修改"
              loading={submitting}
              onSubmit={handleUpdate}
            />
            <Button variant="outline" mt={4} onClick={() => setEditingClient(null)}>
              取消编辑
            </Button>
          </Card.Body>
        </Card.Root>
      )}

      {(message || errorMsg) && (
        <Box mb={4}>
          {message && (
            <Text color="green.600" fontSize="sm">
              {message}
            </Text>
          )}
          {errorMsg && (
            <Text color="red.500" fontSize="sm">
              {errorMsg}
            </Text>
          )}
        </Box>
      )}

      <Card.Root>
        <Card.Body p={0}>
          {Array.isArray(clients) && clients.length > 0 ? (
            <Table.Root size="sm">
              <Table.Header>
                <Table.Row>
                  <Table.ColumnHeader>名称</Table.ColumnHeader>
                  <Table.ColumnHeader>电话</Table.ColumnHeader>
                  <Table.ColumnHeader>邮箱</Table.ColumnHeader>
                  <Table.ColumnHeader>状态</Table.ColumnHeader>
                  <Table.ColumnHeader>备注</Table.ColumnHeader>
                  <Table.ColumnHeader>创建时间</Table.ColumnHeader>
                  <Table.ColumnHeader>操作</Table.ColumnHeader>
                </Table.Row>
              </Table.Header>
              <Table.Body>
                {clients.map((client) => (
                  <Table.Row key={client.id}>
                    <Table.Cell>
                      <Text fontWeight="medium">{client.name}</Text>
                    </Table.Cell>
                    <Table.Cell>{client.phone || '-'}</Table.Cell>
                    <Table.Cell>{client.email || '-'}</Table.Cell>
                    <Table.Cell>
                      <Badge colorPalette={client.status === 'active' ? 'green' : 'gray'}>
                        {statusLabel[client.status]}
                      </Badge>
                    </Table.Cell>
                    <Table.Cell>
                      <Text fontSize="sm" color="gray.600" maxW="200px" truncate>
                        {client.notes || '-'}
                      </Text>
                    </Table.Cell>
                    <Table.Cell>{formatDate(client.created_at)}</Table.Cell>
                    <Table.Cell>
                      <HStack gap={2}>
                        <Button
                          size="xs"
                          colorPalette="blue"
                          variant="outline"
                          onClick={() => {
                            setEditingClient(client)
                            setMessage('')
                            setErrorMsg('')
                          }}
                        >
                          编辑
                        </Button>
                        <Button
                          size="xs"
                          colorPalette="red"
                          variant="outline"
                          loading={deletingId === client.id}
                          onClick={() => handleDelete(client.id)}
                        >
                          删除
                        </Button>
                      </HStack>
                    </Table.Cell>
                  </Table.Row>
                ))}
              </Table.Body>
            </Table.Root>
          ) : (
            <Text textAlign="center" color="gray.500" py={10}>
              暂无顾客，请先创建
            </Text>
          )}
        </Card.Body>
      </Card.Root>
    </Box>
  )
}
