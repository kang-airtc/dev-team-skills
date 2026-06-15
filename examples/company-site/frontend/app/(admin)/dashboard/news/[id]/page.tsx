'use client'

import AdminShell from '@/components/admin/AdminShell'
import NewsForm from '@/components/admin/NewsForm'

interface Props {
  params: { id: string }
}

export default function EditNewsPage({ params }: Props) {
  const id = Number(params.id)
  return (
    <AdminShell title="编辑新闻" description={`新闻 ID: ${id}`}>
      <NewsForm id={id} />
    </AdminShell>
  )
}
