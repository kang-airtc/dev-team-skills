'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'

import AdminShell from '@/components/admin/AdminShell'
import { listCategories } from '@/services/categories'
import { listComments } from '@/services/comments'
import { listNews } from '@/services/news'
import { listProducts } from '@/services/products'

interface Counts {
  products: number
  news: number
  comments: number
  categories: number
}

export default function DashboardPage() {
  const [counts, setCounts] = useState<Counts>({
    products: 0,
    news: 0,
    comments: 0,
    categories: 0,
  })

  useEffect(() => {
    Promise.all([
      listProducts({ limit: 1, include_unpublished: true }).catch(() => ({ total: 0 })),
      listNews({ limit: 1, include_unpublished: true }).catch(() => ({ total: 0 })),
      listComments({ limit: 1 }).catch(() => ({ total: 0 })),
      listCategories().then((arr) => ({ total: arr.length })).catch(() => ({ total: 0 })),
    ]).then(([p, n, c, cat]) => {
      setCounts({
        products: p.total ?? 0,
        news: n.total ?? 0,
        comments: c.total ?? 0,
        categories: cat.total ?? 0,
      })
    })
  }, [])

  const cards = [
    { label: '产品', count: counts.products, href: '/dashboard/products' },
    { label: '分类', count: counts.categories, href: '/dashboard/categories' },
    { label: '新闻', count: counts.news, href: '/dashboard/news' },
    { label: '评论', count: counts.comments, href: '/dashboard/comments' },
  ]

  return (
    <AdminShell title="概览" description="快速查看站点内容总量与入口。">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {cards.map((c) => (
          <Link
            key={c.label}
            href={c.href}
            className="block rounded-2xl bg-white border border-line p-6 hover:shadow-soft transition-all duration-200 cursor-pointer"
          >
            <div className="text-xs uppercase tracking-wider text-ink-muted mb-2">
              {c.label}
            </div>
            <div className="text-3xl font-semibold tracking-tight text-ink">
              {c.count}
            </div>
            <div className="text-xs text-ink-muted mt-3">前往管理 →</div>
          </Link>
        ))}
      </div>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-2xl bg-white border border-line p-6">
          <div className="text-sm font-semibold text-ink mb-3">快速操作</div>
          <div className="space-y-2">
            <Link
              href="/dashboard/products/new"
              className="block px-4 py-3 rounded-xl bg-surface-alt hover:bg-neutral-200 text-sm transition-colors cursor-pointer"
            >
              + 新建产品
            </Link>
            <Link
              href="/dashboard/news/new"
              className="block px-4 py-3 rounded-xl bg-surface-alt hover:bg-neutral-200 text-sm transition-colors cursor-pointer"
            >
              + 发布新闻
            </Link>
            <Link
              href="/dashboard/categories"
              className="block px-4 py-3 rounded-xl bg-surface-alt hover:bg-neutral-200 text-sm transition-colors cursor-pointer"
            >
              管理产品分类
            </Link>
          </div>
        </div>

        <div className="rounded-2xl bg-white border border-line p-6">
          <div className="text-sm font-semibold text-ink mb-3">使用提示</div>
          <ul className="space-y-2 text-sm text-ink-muted leading-relaxed">
            <li>· 创建产品前先添加产品分类，便于公开站筛选。</li>
            <li>· 把产品标记为「推荐」即会出现在首页 Featured 区。</li>
            <li>· 评论默认直接发布，可在评论页隐藏或删除违规内容。</li>
          </ul>
        </div>
      </div>
    </AdminShell>
  )
}
