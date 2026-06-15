'use client'

import AdminShell from '@/components/admin/AdminShell'
import NewsForm from '@/components/admin/NewsForm'

export default function NewNewsPage() {
  return (
    <AdminShell title="发布新闻" description="撰写并发布一条新闻。">
      <NewsForm />
    </AdminShell>
  )
}
