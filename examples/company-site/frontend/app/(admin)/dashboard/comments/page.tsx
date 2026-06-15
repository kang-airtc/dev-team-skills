'use client'

import { useEffect, useState } from 'react'

import AdminShell from '@/components/admin/AdminShell'
import {
  Comment,
  deleteComment,
  listCommentsAdmin,
  updateComment,
} from '@/services/comments'

function fmt(s: string) {
  const d = new Date(s)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

type FilterType = 'all' | 'product' | 'news'

export default function CommentsAdmin() {
  const [items, setItems] = useState<Comment[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<FilterType>('all')

  const fetchAll = () => {
    setLoading(true)
    listCommentsAdmin({
      target_type: filter === 'all' ? undefined : filter,
      approved_only: false,
      limit: 200,
    })
      .then((r) => setItems(r.items))
      .catch(() => setItems([]))
      .finally(() => setLoading(false))
  }

  useEffect(fetchAll, [filter])

  const toggle = async (c: Comment) => {
    try {
      await updateComment(c.id, { is_approved: !c.is_approved })
      fetchAll()
    } catch (err) {
      alert(err instanceof Error ? err.message : '操作失败')
    }
  }

  const remove = async (id: number) => {
    if (!confirm('确认删除该评论？')) return
    try {
      await deleteComment(id)
      fetchAll()
    } catch (err) {
      alert(err instanceof Error ? err.message : '删除失败')
    }
  }

  return (
    <AdminShell title="评论管理" description="管理产品与新闻下的评论，必要时可隐藏或删除。">
      <div className="flex gap-2 mb-6">
        {(
          [
            { v: 'all' as FilterType, label: '全部' },
            { v: 'product' as FilterType, label: '产品评论' },
            { v: 'news' as FilterType, label: '新闻评论' },
          ]
        ).map((t) => (
          <button
            key={t.v}
            onClick={() => setFilter(t.v)}
            className={`h-9 px-4 rounded-full text-sm font-medium transition-colors duration-200 cursor-pointer ${
              filter === t.v
                ? 'bg-ink text-white'
                : 'bg-white border border-line text-ink hover:bg-surface-alt'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="rounded-2xl bg-white border border-line overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-surface-alt text-ink-muted text-xs uppercase tracking-wider">
            <tr>
              <th className="text-left px-5 py-3 w-32">类型</th>
              <th className="text-left px-5 py-3 w-32">昵称</th>
              <th className="text-left px-5 py-3">内容</th>
              <th className="text-left px-5 py-3 w-40">时间</th>
              <th className="text-left px-5 py-3 w-24">状态</th>
              <th className="text-right px-5 py-3 w-40">操作</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} className="px-5 py-10 text-center text-ink-muted">
                  加载中…
                </td>
              </tr>
            ) : items.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-5 py-10 text-center text-ink-muted">
                  暂无评论
                </td>
              </tr>
            ) : (
              items.map((c) => (
                <tr key={c.id} className="border-t border-line align-top">
                  <td className="px-5 py-3 text-ink-muted">
                    {c.target_type === 'product' ? '产品' : '新闻'} #{c.target_id}
                  </td>
                  <td className="px-5 py-3 text-ink">{c.nickname}</td>
                  <td className="px-5 py-3 text-ink whitespace-pre-wrap">{c.content}</td>
                  <td className="px-5 py-3 text-ink-muted">{fmt(c.created_at)}</td>
                  <td className="px-5 py-3">
                    <span
                      className={`inline-flex items-center text-xs px-2 py-0.5 rounded-full border ${
                        c.is_approved
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                          : 'bg-surface-alt text-ink-muted border-line'
                      }`}
                    >
                      {c.is_approved ? '已显示' : '已隐藏'}
                    </span>
                  </td>
                  <td className="px-5 py-3 text-right">
                    <button
                      onClick={() => toggle(c)}
                      className="text-ink hover:underline cursor-pointer mr-4"
                    >
                      {c.is_approved ? '隐藏' : '显示'}
                    </button>
                    <button
                      onClick={() => remove(c.id)}
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
