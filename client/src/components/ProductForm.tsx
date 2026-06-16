import {
  Button,
  Field,
  HStack,
  Input,
  Stack,
  Text,
  Textarea,
} from '@chakra-ui/react'
import { useState } from 'react'
import type { ProductFormPayload } from '../api/products'

interface ProductFormProps {
  initialValues?: ProductFormPayload
  submitLabel: string
  loading?: boolean
  onSubmit: (payload: ProductFormPayload) => Promise<void>
}

const defaultValues: ProductFormPayload = {
  name: '',
  description: '',
  price: 0,
}

export default function ProductForm({
  initialValues = defaultValues,
  submitLabel,
  loading = false,
  onSubmit,
}: ProductFormProps) {
  const [form, setForm] = useState<ProductFormPayload>(initialValues)
  const [errorMsg, setErrorMsg] = useState('')

  const handleSubmit = async () => {
    if (!form.name.trim()) {
      setErrorMsg('请填写产品名称')
      return
    }
    if (!form.price || form.price <= 0) {
      setErrorMsg('请填写大于 0 的价格')
      return
    }

    setErrorMsg('')
    await onSubmit({
      name: form.name.trim(),
      description: form.description?.trim() ?? '',
      price: form.price,
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
            placeholder="产品名称"
            maxLength={30}
          />
        </Field.Root>
        <Field.Root required maxW="xs">
          <Field.Label>价格</Field.Label>
          <Input
            type="number"
            min={0}
            step={0.01}
            value={form.price || ''}
            onChange={(e) => setForm({ ...form, price: Number(e.target.value) })}
            placeholder="产品价格"
          />
        </Field.Root>
      </HStack>
      <Field.Root maxW="xl">
        <Field.Label>描述</Field.Label>
        <Textarea
          value={form.description ?? ''}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          placeholder="产品描述（选填）"
          maxLength={255}
          rows={4}
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
