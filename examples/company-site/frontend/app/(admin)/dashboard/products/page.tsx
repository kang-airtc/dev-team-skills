'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'

import AdminShell from '@/components/admin/AdminShell'
import { Category, listCategories } from '@/services/categories'
import { deleteProduct, listProducts, Product } from '@/services/products'

export default function ProductsAdmin() {
  const [items, setItems] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)

  const fetchAll = () => {
    setLoading(true)
    Promise.all([
      listProducts({ include_unpublished: true, limit: 200 }),
      listCategories(),
    ])
      .then(([p, cats]) => {
        setItems(p.items)
        setCategories(cats)
      })
      .catch(() => {
        setItems([])
        setCategories([])
      })
      .finally(() => setLoading(false))
  }

  useEffect(fetchAll, [])

  const remove = async (id: number) => {
    if (!confirm('确认删除该产品？')) return
    try {
      await deleteProduct(id)
      fetchAll()
    } catch (err) {
      alert(err instanceof Error ? err.message : '删除失败')
    }
  }

  const categoryName = (id: number | null) =>
    id == null ? '—' : categories.find((c) => c.id === id)?.name || '—'

  return (
    <AdminShell
      title="产品管理"
      description="管理所有产品的发布、推荐、上下架与详情。"
      actions={
        <Link
          href="/dashboard/products/new"
          className="inline-flex h-10 items-center px-5 rounded-full bg-ink text-white text-sm font-medium hover:bg-neutral-800 transition-colors cursor-pointer"
        >
          + 新建产品
        </Link>
      }
    >
      <div className="rounded-2xl bg-white border border-line overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-surface-alt text-ink-muted text-xs uppercase tracking-wider">
            <tr>
              <th className="text-left px-5 py-3">名称</th>
              <th className="text-left px-5 py-3">分类</th>
              <th className="text-left px-5 py-3">价格</th>
              <th className="text-left px-5 py-3 w-32">状态</th>
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
                  暂无产品。点击右上角新建。
                </td>
              </tr>
            ) : (
              items.map((p) => (
                <tr key={p.id} className="border-t border-line">
                  <td className="px-5 py-3">
                    <div className="font-medium text-ink">{p.name}</div>
                    <div className="text-xs text-ink-muted">/{p.slug}</div>
                  </td>
                  <td className="px-5 py-3 text-ink-muted">
                    {categoryName(p.category_id)}
                  </td>
                  <td className="px-5 py-3 text-ink-muted">
                    {p.price != null ? `¥${Number(p.price).toLocaleString()}` : '—'}
                  </td>
                  <td className="px-5 py-3">
                    <div className="flex gap-1.5 flex-wrap">
                      <Tag tone={p.is_published ? 'green' : 'gray'}>
                        {p.is_published ? '已上架' : '草稿'}
                      </Tag>
                      {p.is_featured && <Tag tone="dark">推荐</Tag>}
                    </div>
                  </td>
                  <td className="px-5 py-3 text-right">
                    <Link
                      href={`/dashboard/products/${p.id}`}
                      className="text-ink hover:underline cursor-pointer mr-4"
                    >
                      编辑
                    </Link>
                    <button
                      onClick={() => remove(p.id)}
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

function Tag({
  children,
  tone,
}: {
  children: React.ReactNode
  tone: 'green' | 'gray' | 'dark'
}) {
  const cls =
    tone === 'green'
      ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
      : tone === 'dark'
        ? 'bg-ink text-white border-ink'
        : 'bg-surface-alt text-ink-muted border-line'
  return (
    <span className={`inline-flex items-center text-xs px-2 py-0.5 rounded-full border ${cls}`}>
      {children}
    </span>
  )
}
