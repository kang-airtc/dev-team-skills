'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useEffect, useRef, useState } from 'react'

import { getCurrentUser, User } from '@/services/auth'

import Logo from './Logo'

function isAdmin(user: User | null): boolean {
  if (!user) return false
  return user.is_superuser || user.username === 'admin'
}

function logoutAndReload() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  window.location.reload()
}

const NAV_ITEMS = [
  { href: '/', label: '首页' },
  { href: '/products', label: '产品' },
  { href: '/news', label: '新闻' },
  { href: '/about', label: '关于' },
  { href: '/contact', label: '联系' },
]

export default function Navbar() {
  const pathname = usePathname()
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)
  const [user, setUser] = useState<User | null>(null)
  const [menuOpen, setMenuOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  // 拉当前用户（路由变化后也重拉，以防登录/退出后状态不同步）
  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null
    if (!token) {
      setUser(null)
      return
    }
    getCurrentUser()
      .then(setUser)
      .catch(() => setUser(null))
  }, [pathname])

  // 点击外部关闭下拉菜单
  useEffect(() => {
    if (!menuOpen) return
    const onClick = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false)
      }
    }
    document.addEventListener('mousedown', onClick)
    return () => document.removeEventListener('mousedown', onClick)
  }, [menuOpen])

  return (
    <header
      className={`sticky top-0 z-50 transition-colors duration-300 ease-smooth ${
        scrolled
          ? 'bg-white/80 backdrop-blur-md border-b border-line'
          : 'bg-white/0 border-b border-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 md:px-8 h-16 flex items-center justify-between">
        <Link
          href="/"
          className="flex items-center cursor-pointer transition-opacity hover:opacity-80"
        >
          <Logo />
        </Link>

        <nav className="hidden md:flex items-center gap-8">
          {NAV_ITEMS.map((item) => {
            const active =
              item.href === '/' ? pathname === '/' : pathname?.startsWith(item.href)
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`text-[14px] font-medium transition-colors duration-200 cursor-pointer ${
                  active ? 'text-ink' : 'text-ink-muted hover:text-ink'
                }`}
              >
                {item.label}
              </Link>
            )
          })}
        </nav>

        <div className="hidden md:flex items-center gap-3">
          {user ? (
            <div className="relative" ref={menuRef}>
              <button
                onClick={() => setMenuOpen((v) => !v)}
                className="flex items-center gap-2 cursor-pointer group"
                aria-label="用户菜单"
              >
                <span className="hidden lg:inline text-[14px] font-medium text-ink-muted group-hover:text-ink transition-colors">
                  {user.username}
                </span>
                <span className="flex items-center justify-center h-9 w-9 rounded-full bg-ink text-white text-[13px] font-semibold transition-transform group-hover:scale-105">
                  {(user.username || '?').charAt(0).toUpperCase()}
                </span>
              </button>

              {menuOpen && (
                <div className="absolute right-0 mt-2 w-52 rounded-2xl bg-white border border-line shadow-lift overflow-hidden">
                  <div className="px-4 py-3 border-b border-line">
                    <div className="text-sm font-semibold text-ink">{user.username}</div>
                    <div className="text-xs text-ink-muted truncate">{user.email}</div>
                  </div>
                  {isAdmin(user) && (
                    <Link
                      href="/dashboard"
                      onClick={() => setMenuOpen(false)}
                      className="block px-4 py-2.5 text-sm text-ink hover:bg-surface-alt transition-colors cursor-pointer"
                    >
                      后台管理
                    </Link>
                  )}
                  <button
                    onClick={logoutAndReload}
                    className="block w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-surface-alt transition-colors cursor-pointer"
                  >
                    退出登录
                  </button>
                </div>
              )}
            </div>
          ) : (
            <>
              <Link
                href="/login"
                className="text-[14px] font-medium text-ink-muted hover:text-ink transition-colors cursor-pointer"
              >
                登录
              </Link>
              <Link
                href="/register"
                className="inline-flex h-9 items-center px-4 rounded-full bg-ink text-white text-[14px] font-medium hover:bg-neutral-800 transition-colors cursor-pointer"
              >
                注册
              </Link>
            </>
          )}
        </div>

        <button
          aria-label="菜单"
          onClick={() => setOpen((v) => !v)}
          className="md:hidden inline-flex h-10 w-10 items-center justify-center rounded-full hover:bg-surface-alt cursor-pointer"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
            {open ? (
              <path d="M6 6l12 12M18 6L6 18" strokeLinecap="round" />
            ) : (
              <>
                <path d="M4 7h16" strokeLinecap="round" />
                <path d="M4 17h16" strokeLinecap="round" />
              </>
            )}
          </svg>
        </button>
      </div>

      {open && (
        <div className="md:hidden border-t border-line bg-white">
          <div className="max-w-7xl mx-auto px-6 py-4 flex flex-col gap-3">
            {NAV_ITEMS.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className="text-[15px] py-1.5 text-ink hover:text-ink-muted"
              >
                {item.label}
              </Link>
            ))}
            <div className="flex flex-col gap-2 pt-3 border-t border-line">
              {user ? (
                <>
                  <div className="text-xs text-ink-muted">
                    已登录为 <span className="text-ink font-medium">{user.username}</span>
                  </div>
                  {isAdmin(user) && (
                    <Link
                      href="/dashboard"
                      onClick={() => setOpen(false)}
                      className="text-[14px] py-2 text-ink"
                    >
                      后台管理
                    </Link>
                  )}
                  <button
                    onClick={logoutAndReload}
                    className="text-left text-[14px] py-2 text-red-600"
                  >
                    退出登录
                  </button>
                </>
              ) : (
                <div className="flex gap-3">
                  <Link href="/login" className="text-[14px] py-2 text-ink-muted">
                    登录
                  </Link>
                  <Link
                    href="/register"
                    className="inline-flex h-9 items-center px-4 rounded-full bg-ink text-white text-[14px]"
                  >
                    注册
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </header>
  )
}
