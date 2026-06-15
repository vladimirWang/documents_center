import {
  Badge,
  Box,
  Button,
  Card,
  Field,
  Heading,
  HStack,
  Input,
  NativeSelect,
  Spinner,
  Stack,
  Table,
  Text,
  Textarea,
} from '@chakra-ui/react'
import { useState } from 'react'
import { getApiErrorMessage } from '../api/auth'
import {
  createClient,
  deleteClient,
  updateClient,
  type ClientItem,
  type ClientStatus,
  type CreateClientPayload,
} from '../api/clients'
import { useClients } from '../hooks/useClients'

const emptyForm: CreateClientPayload = {
  name: '',
  phone: '',
  email: '',
  status: 'active',
  notes: '',
}

const formatDate = (value: string) => {
  return new Date(value).toLocaleString('zh-CN')
}

const statusLabel: Record<ClientStatus, string> = {
  active: '活跃',
  inactive: '停用',
}

export default function ClientPage() {
  const { data: clients, isLoading, error, mutate } = useClients()
  const [form, setForm] = useState<CreateClientPayload>(emptyForm)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [submitting, setSubmitting] = useState(false)
  const [deletingId, setDeletingId] = useState<number | null>(null)
  const [message, setMessage] = useState('')
  const [errorMsg, setErrorMsg] = useState('')

  const resetForm = () => {
    setForm(emptyForm)
    setEditingId(null)
  }

  const fillForm = (client: ClientItem) => {
    setEditingId(client.id)
    setForm({
      name: client.name,
      phone: client.phone,
      email: client.email,
      status: client.status,
      notes: client.notes,
    })
    setMessage('')
    setErrorMsg('')
  }

  const handleSubmit = async () => {
    if (!form.name.trim()) {
      setErrorMsg('请填写顾客名称')
      return
    }

    setSubmitting(true)
    setMessage('')
    setErrorMsg('')

    try {
      if (editingId) {
        const result = await updateClient(editingId, form)
        setMessage(result.message)
      } else {
        const result = await createClient(form)
        setMessage(result.message)
      }
      resetForm()
      await mutate()
    } catch (err) {
      setErrorMsg(getApiErrorMessage(err, editingId ? '更新顾客失败' : '创建顾客失败'))
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
      if (editingId === clientId) resetForm()
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
      <Heading size="lg" mb={2}>
        顾客管理
      </Heading>
      <Text color="gray.600" mb={8}>
        共 {clients?.length ?? 0} 位顾客
      </Text>

      <Card.Root mb={8}>
        <Card.Body>
          <Stack gap={4}>
            <Heading size="sm">{editingId ? '编辑顾客' : '新增顾客'}</Heading>
            <HStack gap={4} align="start" flexWrap="wrap">
              <Field.Root required maxW="xs">
                <Field.Label>名称</Field.Label>
                <Input
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="顾客名称"
                />
              </Field.Root>
              <Field.Root maxW="xs">
                <Field.Label>电话</Field.Label>
                <Input
                  value={form.phone}
                  onChange={(e) => setForm({ ...form, phone: e.target.value })}
                  placeholder="联系电话"
                />
              </Field.Root>
              <Field.Root maxW="xs">
                <Field.Label>邮箱</Field.Label>
                <Input
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  placeholder="邮箱地址"
                />
              </Field.Root>
              <Field.Root maxW="xs">
                <Field.Label>状态</Field.Label>
                <NativeSelect.Root>
                  <NativeSelect.Field
                    value={form.status}
                    onChange={(e) =>
                      setForm({ ...form, status: e.target.value as ClientStatus })
                    }
                  >
                    <option value="active">活跃</option>
                    <option value="inactive">停用</option>
                  </NativeSelect.Field>
                </NativeSelect.Root>
              </Field.Root>
            </HStack>
            <Field.Root>
              <Field.Label>备注</Field.Label>
              <Textarea
                value={form.notes}
                onChange={(e) => setForm({ ...form, notes: e.target.value })}
                placeholder="备注信息"
                rows={2}
              />
            </Field.Root>
            <HStack gap={3}>
              <Button colorPalette="blue" loading={submitting} onClick={handleSubmit}>
                {editingId ? '保存修改' : '添加顾客'}
              </Button>
              {editingId && (
                <Button variant="outline" onClick={resetForm}>
                  取消编辑
                </Button>
              )}
            </HStack>
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
          </Stack>
        </Card.Body>
      </Card.Root>

      <Card.Root>
        <Card.Body p={0}>
          {
            Array.isArray(clients) ? <Table.Root size="sm">
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
                        onClick={() => fillForm(client)}
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
          </Table.Root>: null
          }

          {!clients?.length && (
            <Text textAlign="center" color="gray.500" py={10}>
              暂无顾客，请先添加
            </Text>
          )}
        </Card.Body>
      </Card.Root>
    </Box>
  )
}
