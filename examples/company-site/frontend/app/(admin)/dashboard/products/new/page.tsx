'use client'

import AdminShell from '@/components/admin/AdminShell'
import ProductForm from '@/components/admin/ProductForm'

export default function NewProductPage() {
  return (
    <AdminShell title="新建产品" description="填写产品信息后保存即可发布。">
      <ProductForm />
    </AdminShell>
  )
}
