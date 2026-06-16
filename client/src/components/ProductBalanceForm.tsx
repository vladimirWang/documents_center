import { Button, Field, Input, Stack, Text } from '@chakra-ui/react'
import { useState } from 'react'
import type { ProductBalancePayload } from '../api/products'

interface ProductBalanceFormProps {
  initialBalance: number
  submitLabel: string
  loading?: boolean
  onSubmit: (payload: ProductBalancePayload) => Promise<void>
}

export default function ProductBalanceForm({
  initialBalance,
  submitLabel,
  loading = false,
  onSubmit,
}: ProductBalanceFormProps) {
  const [balance, setBalance] = useState(initialBalance)
  const [errorMsg, setErrorMsg] = useState('')

  const handleSubmit = async () => {
    if (!Number.isInteger(balance) || balance < 0) {
      setErrorMsg('库存必须是不小于 0 的整数')
      return
    }

    setErrorMsg('')
    await onSubmit({ balance })
  }

  return (
    <Stack gap={4}>
      <Field.Root required maxW="xs">
        <Field.Label>库存数量</Field.Label>
        <Input
          type="number"
          min={0}
          step={1}
          value={balance}
          onChange={(e) => setBalance(Number(e.target.value))}
          placeholder="请输入库存数量"
        />
        <Field.HelperText>修改后立即生效，用于控制可售数量</Field.HelperText>
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
