import {
  Button,
  Field,
  HStack,
  IconButton,
  Input,
  NativeSelect,
  Stack,
  Text,
  Textarea,
} from '@chakra-ui/react'
import { useMemo, useState } from 'react'
import type { OrderCreatePayload, OrderLinePayload } from '../api/orders'
import type { ProductItem } from '../api/products'

interface OrderFormProps {
  products: ProductItem[]
  submitLabel: string
  loading?: boolean
  onSubmit: (payload: OrderCreatePayload) => Promise<void>
}

const emptyLine = (): OrderLinePayload => ({
  product_id: 0,
  quantity: 1,
  price: 0,
})

const defaultValues: OrderCreatePayload = {
  items: [emptyLine()],
  remark: '',
}

const formatMoney = (value: number) => `¥${value.toFixed(2)}`

export default function OrderForm({
  products,
  submitLabel,
  loading = false,
  onSubmit,
}: OrderFormProps) {
  const [form, setForm] = useState<OrderCreatePayload>(defaultValues)
  const [errorMsg, setErrorMsg] = useState('')

  const estimatedTotal = useMemo(() => {
    return form.items.reduce((sum, item) => sum + item.quantity * item.price, 0)
  }, [form.items])

  const updateLine = (index: number, patch: Partial<OrderLinePayload>) => {
    setForm((prev) => ({
      ...prev,
      items: prev.items.map((item, i) => (i === index ? { ...item, ...patch } : item)),
    }))
  }

  const handleProductChange = (index: number, productId: number) => {
    const product = products.find((item) => item.id === productId)
    updateLine(index, {
      product_id: productId,
      price: product?.price ?? 0,
    })
  }

  const addLine = () => {
    setForm((prev) => ({
      ...prev,
      items: [...prev.items, emptyLine()],
    }))
  }

  const removeLine = (index: number) => {
    setForm((prev) => ({
      ...prev,
      items: prev.items.length > 1 ? prev.items.filter((_, i) => i !== index) : prev.items,
    }))
  }

  const handleSubmit = async () => {
    const validItems = form.items.filter((item) => item.product_id > 0)
    if (!validItems.length) {
      setErrorMsg('请至少添加一条有效的产品明细')
      return
    }

    if (validItems.some((item) => item.quantity <= 0 || item.price <= 0)) {
      setErrorMsg('数量和单价必须大于 0')
      return
    }

    setErrorMsg('')
    await onSubmit({
      items: validItems,
      remark: form.remark?.trim() || '',
    })
  }

  return (
    <Stack gap={4}>
      <Stack gap={3}>
        {form.items.map((item, index) => (
          <HStack key={index} gap={3} align="end" flexWrap="wrap">
            <Field.Root required minW="220px">
              <Field.Label>产品</Field.Label>
              <NativeSelect.Root>
                <NativeSelect.Field
                  value={item.product_id || ''}
                  onChange={(e) => handleProductChange(index, Number(e.target.value))}
                >
                  <option value="">请选择产品</option>
                  {products.map((product) => (
                    <option key={product.id} value={product.id}>
                      {product.name}
                    </option>
                  ))}
                </NativeSelect.Field>
              </NativeSelect.Root>
            </Field.Root>

            <Field.Root required maxW="120px">
              <Field.Label>数量</Field.Label>
              <Input
                type="number"
                min={1}
                value={item.quantity}
                onChange={(e) => updateLine(index, { quantity: Number(e.target.value) })}
              />
            </Field.Root>

            <Field.Root required maxW="140px">
              <Field.Label>单价</Field.Label>
              <Input
                type="number"
                min={0.01}
                step={0.01}
                value={item.price}
                onChange={(e) => updateLine(index, { price: Number(e.target.value) })}
              />
            </Field.Root>

            <IconButton
              aria-label="删除明细"
              variant="outline"
              colorPalette="red"
              onClick={() => removeLine(index)}
              disabled={form.items.length === 1}
            >
              删
            </IconButton>
          </HStack>
        ))}
      </Stack>

      <Button alignSelf="start" variant="outline" onClick={addLine}>
        添加明细
      </Button>

      <Field.Root>
        <Field.Label>备注</Field.Label>
        <Textarea
          value={form.remark}
          onChange={(e) => setForm({ ...form, remark: e.target.value })}
          placeholder="订单备注"
          rows={2}
        />
      </Field.Root>

      <Text fontSize="sm" color="gray.600">
        预估总价：{formatMoney(estimatedTotal)}
      </Text>

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
