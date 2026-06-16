import {
  Button,
  Field,
  HStack,
  Input,
  NativeSelect,
  Stack,
  Text,
  Textarea,
} from '@chakra-ui/react'
import { useState } from 'react'
import type { ClientStatus, CreateClientPayload } from '../api/clients'

interface ClientFormProps {
  initialValues?: CreateClientPayload
  submitLabel: string
  loading?: boolean
  onSubmit: (payload: CreateClientPayload) => Promise<void>
}

const defaultValues: CreateClientPayload = {
  name: '',
  phone: '',
  email: '',
  status: 'active',
  notes: '',
}

export default function ClientForm({
  initialValues = defaultValues,
  submitLabel,
  loading = false,
  onSubmit,
}: ClientFormProps) {
  const [form, setForm] = useState<CreateClientPayload>(initialValues)
  const [errorMsg, setErrorMsg] = useState('')

  const handleSubmit = async () => {
    if (!form.name.trim()) {
      setErrorMsg('请填写顾客名称')
      return
    }

    setErrorMsg('')
    await onSubmit({
      name: form.name.trim(),
      phone: form.phone?.trim() ?? '',
      email: form.email?.trim() ?? '',
      status: form.status ?? 'active',
      notes: form.notes?.trim() ?? '',
    })
  }

  return (
    <Stack gap={4}>
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
              onChange={(e) => setForm({ ...form, status: e.target.value as ClientStatus })}
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
      <Button colorPalette="blue" loading={loading} onClick={handleSubmit} maxW="xs">
        {submitLabel}
      </Button>
      {errorMsg && (
        <Text color="red.500" fontSize="sm">
          {errorMsg}
        </Text>
      )}
    </Stack>
  )
}
