'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { login } from '@/services/auth'

export default function LoginPage() {
  const router = useRouter()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    if (!form.username || !form.password) {
      setError('请输入用户名和密码')
      return
    }
    setLoading(true)
    try {
      await login(form)
      router.push('/dashboard')
    } catch (err) {
      const msg = err instanceof Error ? err.message : '登录失败'
      if (msg.includes('用户名或密码错误') || msg.includes('401')) {
        setError('用户名或密码错误')
      } else if (msg.includes('禁用') || msg.includes('403')) {
        setError('账号已被禁用')
      } else {
        setError('登录失败，请稍后重试')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-surface-alt px-4 py-12">
      <div className="max-w-md w-full">
        <a href="/" className="flex items-center justify-center mb-8 cursor-pointer">
          <span className="text-xl font-semibold tracking-tight text-ink">某某科技</span>
        </a>

        <div className="bg-white rounded-3xl shadow-soft border border-line p-8 md:p-10">
          <h1 className="text-2xl font-semibold tracking-tight text-ink mb-1">欢迎回来</h1>
          <p className="text-sm text-ink-muted mb-8">登录后台管理控制台</p>

          <form className="space-y-4" onSubmit={handleSubmit} noValidate>
            {error && (
              <div className="rounded-xl bg-red-50 border border-red-200 p-3 text-sm text-red-700">
                {error}
              </div>
            )}

            <div>
              <label className="block text-xs font-medium text-ink-muted mb-2 uppercase tracking-wider">
                用户名
              </label>
              <input
                name="username"
                value={form.username}
                onChange={handleChange}
                disabled={loading}
                className="w-full h-11 px-4 rounded-xl bg-surface-alt border border-line text-sm focus:outline-none focus:border-ink focus:bg-white transition-colors"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-ink-muted mb-2 uppercase tracking-wider">
                密码
              </label>
              <input
                name="password"
                type="password"
                value={form.password}
                onChange={handleChange}
                disabled={loading}
                className="w-full h-11 px-4 rounded-xl bg-surface-alt border border-line text-sm focus:outline-none focus:border-ink focus:bg-white transition-colors"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full h-11 rounded-full bg-ink text-white text-sm font-medium hover:bg-neutral-800 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? '登录中…' : '登录'}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-ink-muted">
            没有账号？{' '}
            <a href="/register" className="text-ink font-medium hover:underline cursor-pointer">
              立即注册
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
