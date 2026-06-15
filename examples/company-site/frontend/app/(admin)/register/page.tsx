'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { register } from '@/services/auth'

export default function RegisterPage() {
  const router = useRouter()
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    full_name: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    if (!form.username || !form.email || !form.password) {
      setError('请填写必填项')
      return
    }
    setLoading(true)
    try {
      await register(form)
      router.push('/login')
    } catch (err) {
      const msg = err instanceof Error ? err.message : '注册失败'
      setError(msg)
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
          <h1 className="text-2xl font-semibold tracking-tight text-ink mb-1">创建账号</h1>
          <p className="text-sm text-ink-muted mb-8">注册后即可登录后台管理</p>

          <form className="space-y-4" onSubmit={handleSubmit} noValidate>
            {error && (
              <div className="rounded-xl bg-red-50 border border-red-200 p-3 text-sm text-red-700">
                {error}
              </div>
            )}

            {[
              { name: 'username', label: '用户名 *', type: 'text' },
              { name: 'email', label: '邮箱 *', type: 'email' },
              { name: 'password', label: '密码 *（至少 6 位）', type: 'password' },
              { name: 'full_name', label: '姓名（可选）', type: 'text' },
            ].map((f) => (
              <div key={f.name}>
                <label className="block text-xs font-medium text-ink-muted mb-2 uppercase tracking-wider">
                  {f.label}
                </label>
                <input
                  name={f.name}
                  type={f.type}
                  value={form[f.name as keyof typeof form]}
                  onChange={handleChange}
                  disabled={loading}
                  className="w-full h-11 px-4 rounded-xl bg-surface-alt border border-line text-sm focus:outline-none focus:border-ink focus:bg-white transition-colors"
                />
              </div>
            ))}

            <button
              type="submit"
              disabled={loading}
              className="w-full h-11 rounded-full bg-ink text-white text-sm font-medium hover:bg-neutral-800 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? '提交中…' : '注册'}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-ink-muted">
            已有账号？{' '}
            <a href="/login" className="text-ink font-medium hover:underline cursor-pointer">
              去登录
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
