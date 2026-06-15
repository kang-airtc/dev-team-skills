'use client'

import AdminShell from '@/components/admin/AdminShell'
import ProductForm from '@/components/admin/ProductForm'

interface Props {
  params: { id: string }
}

export default function EditProductPage({ params }: Props) {
  const id = Number(params.id)
  return (
    <AdminShell title="编辑产品" description={`产品 ID: ${id}`}>
      <ProductForm id={id} />
    </AdminShell>
  )
}
