'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'

import AdminShell from '@/components/admin/AdminShell'
import { deleteNews, listNews, News } from '@/services/news'

function fmt(s: string | null) {
  if (!s) return '—'
  const d = new Date(s)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

export default function NewsAdmin() {
  const [items, setItems] = useState<News[]>([])
  const [loading, setLoading] = useState(true)

  const fetchAll = () => {
    setLoading(true)
    listNews({ include_unpublished: true, limit: 200 })
      .then((r) => setItems(r.items))
      .catch(() => setItems([]))
      .finally(() => setLoading(false))
  }

  useEffect(fetchAll, [])

  const remove = async (id: number) => {
    if (!confirm('确认删除该新闻？')) return
    try {
      await deleteNews(id)
      fetchAll()
    } catch (err) {
      alert(err instanceof Error ? err.message : '删除失败')
    }
  }

  return (
    <AdminShell
      title="新闻管理"
      description="管理新闻发布、上下线与正文。"
      actions={
        <Link
          href="/dashboard/news/new"
          className="inline-flex h-10 items-center px-5 rounded-full bg-ink text-white text-sm font-medium hover:bg-neutral-800 transition-colors cursor-pointer"
        >
          + 发布新闻
        </Link>
      }
    >
      <div className="rounded-2xl bg-white border border-line overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-surface-alt text-ink-muted text-xs uppercase tracking-wider">
            <tr>
              <th className="text-left px-5 py-3">标题</th>
              <th className="text-left px-5 py-3 w-40">作者</th>
              <th className="text-left px-5 py-3 w-32">发布时间</th>
              <th className="text-left px-5 py-3 w-24">状态</th>
              <th className="text-right px-5 py-3 w-40">操作</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={5} className="px-5 py-10 text-center text-ink-muted">
                  加载中…
                </td>
              </tr>
            ) : items.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-5 py-10 text-center text-ink-muted">
                  暂无新闻
                </td>
              </tr>
            ) : (
              items.map((n) => (
                <tr key={n.id} className="border-t border-line">
                  <td className="px-5 py-3">
                    <div className="font-medium text-ink">{n.title}</div>
                    <div className="text-xs text-ink-muted">/{n.slug}</div>
                  </td>
                  <td className="px-5 py-3 text-ink-muted">{n.author || '—'}</td>
                  <td className="px-5 py-3 text-ink-muted">{fmt(n.published_at)}</td>
                  <td className="px-5 py-3">
                    <span
                      className={`inline-flex items-center text-xs px-2 py-0.5 rounded-full border ${
                        n.is_published
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                          : 'bg-surface-alt text-ink-muted border-line'
                      }`}
                    >
                      {n.is_published ? '已发布' : '草稿'}
                    </span>
                  </td>
                  <td className="px-5 py-3 text-right">
                    <Link
                      href={`/dashboard/news/${n.id}`}
                      className="text-ink hover:underline cursor-pointer mr-4"
                    >
                      编辑
                    </Link>
                    <button
                      onClick={() => remove(n.id)}
                      className="text-red-600 hover:underline cursor-pointer"
                    >
                      删除
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </AdminShell>
  )
}
