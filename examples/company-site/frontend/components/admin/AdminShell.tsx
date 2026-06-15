'use client'

import Link from 'next/link'
import { useRouter, usePathname } from 'next/navigation'
import { ReactNode, useEffect, useState } from 'react'

import { getCurrentUser, isAuthenticated, logout, User } from '@/services/auth'

const NAV = [
  { href: '/dashboard', label: '概览', match: (p: string) => p === '/dashboard' },
  { href: '/dashboard/products', label: '产品', match: (p: string) => p.startsWith('/dashboard/products') },
  { href: '/dashboard/categories', label: '分类', match: (p: string) => p.startsWith('/dashboard/categories') },
  { href: '/dashboard/news', label: '新闻', match: (p: string) => p.startsWith('/dashboard/news') },
  { href: '/dashboard/comments', label: '评论', match: (p: string) => p.startsWith('/dashboard/comments') },
]

interface Props {
  children: ReactNode
  title: string
  description?: string
  actions?: ReactNode
}

export default function AdminShell({ children, title, description, actions }: Props) {
  const router = useRouter()
  const pathname = usePathname() || ''
  const [user, setUser] = useState<User | null>(null)
  const [ready, setReady] = useState(false)

  useEffect(() => {
    if (!isAuthenticated()) {
      router.replace('/login')
      return
    }
    getCurrentUser()
      .then((u) => {
        setUser(u)
        setReady(true)
      })
      .catch(() => router.replace('/login'))
  }, [router])

  if (!ready) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-surface-alt">
        <div className="text-sm text-ink-muted">加载中…</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex bg-surface-alt">
      <aside className="hidden md:flex w-60 bg-white border-r border-line flex-col">
        <div className="h-16 flex items-center px-6 border-b border-line">
          <span className="text-lg font-semibold tracking-tight text-ink">某某科技</span>
          <span className="ml-2 text-xs px-2 py-0.5 rounded-full bg-surface-alt text-ink-muted">
            Admin
          </span>
        </div>

        <nav className="flex-1 p-3">
          {NAV.map((item) => {
            const active = item.match(pathname)
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`block px-4 py-2.5 rounded-xl text-sm transition-colors duration-200 cursor-pointer mb-1 ${
                  active
                    ? 'bg-ink text-white'
                    : 'text-ink hover:bg-surface-alt'
                }`}
              >
                {item.label}
              </Link>
            )
          })}
        </nav>

        <div className="p-4 border-t border-line">
          <div className="text-sm font-medium text-ink truncate">
            {user?.full_name || user?.username}
          </div>
          <div className="text-xs text-ink-muted truncate mb-3">{user?.email}</div>
          <div className="flex gap-2">
            <Link
              href="/"
              className="flex-1 inline-flex h-8 items-center justify-center px-3 rounded-full bg-surface-alt text-xs text-ink hover:bg-neutral-200 transition-colors cursor-pointer"
            >
              访问站点
            </Link>
            <button
              onClick={logout}
              className="flex-1 inline-flex h-8 items-center justify-center px-3 rounded-full bg-surface-alt text-xs text-ink hover:bg-neutral-200 transition-colors cursor-pointer"
            >
              退出
            </button>
          </div>
        </div>
      </aside>

      <main className="flex-1 min-w-0">
        <div className="border-b border-line bg-white">
          <div className="px-6 md:px-10 py-6 flex items-center justify-between gap-4">
            <div className="min-w-0">
              <h1 className="text-2xl font-semibold tracking-tight text-ink truncate">
                {title}
              </h1>
              {description && (
                <p className="text-sm text-ink-muted mt-1">{description}</p>
              )}
            </div>
            {actions && <div className="shrink-0">{actions}</div>}
          </div>
        </div>
        <div className="p-6 md:p-10">{children}</div>
      </main>
    </div>
  )
}
