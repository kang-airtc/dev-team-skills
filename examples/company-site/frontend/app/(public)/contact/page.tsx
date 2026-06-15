'use client'

import { useState } from 'react'

export default function ContactPage() {
  const [form, setForm] = useState({ name: '', email: '', subject: '', body: '' })
  const [status, setStatus] = useState<'idle' | 'sending' | 'sent' | 'error'>('idle')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setStatus('sending')
    try {
      // 第 12 章接通：const { submitMessage } = await import('@/services/api')
      // await submitMessage(form)
      await new Promise((r) => setTimeout(r, 600))
      setStatus('sent')
      setForm({ name: '', email: '', subject: '', body: '' })
    } catch {
      setStatus('error')
    }
  }

  return (
    <div>
      <section className="pt-24 md:pt-32 pb-12 bg-gradient-to-b from-surface-alt to-white">
        <div className="max-w-4xl mx-auto px-6 md:px-8">
          <div className="text-sm font-medium text-ink-muted uppercase tracking-wider mb-4">
            Contact
          </div>
          <h1 className="text-5xl md:text-7xl font-semibold tracking-tightest text-ink leading-[1.02]">
            我们在听。
          </h1>
          <p className="mt-6 text-lg text-ink-muted max-w-2xl">
            售前咨询、售后服务、合作机会——告诉我们，我们会在 1 个工作日内回复。
          </p>
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-5xl mx-auto px-6 md:px-8 grid grid-cols-1 md:grid-cols-3 gap-10">
          <div className="space-y-6 md:col-span-1">
            {[
              { label: '客服邮箱', value: 'support@example.com' },
              { label: '商务合作', value: 'partner@example.com' },
              { label: '工作时间', value: '周一至周五 9:00 – 18:00' },
            ].map((it) => (
              <div key={it.label}>
                <div className="text-xs uppercase tracking-wider text-ink-muted mb-1">
                  {it.label}
                </div>
                <div className="text-sm text-ink">{it.value}</div>
              </div>
            ))}
          </div>

          <form
            onSubmit={handleSubmit}
            className="md:col-span-2 rounded-3xl bg-surface-alt p-8 md:p-10 space-y-4"
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                name="name"
                value={form.name}
                onChange={handleChange}
                placeholder="您的姓名"
                required
                className="h-11 px-4 rounded-xl bg-white border border-line text-sm focus:outline-none focus:border-ink transition-colors"
              />
              <input
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                placeholder="邮箱"
                required
                className="h-11 px-4 rounded-xl bg-white border border-line text-sm focus:outline-none focus:border-ink transition-colors"
              />
            </div>
            <input
              name="subject"
              value={form.subject}
              onChange={handleChange}
              placeholder="主题"
              required
              className="w-full h-11 px-4 rounded-xl bg-white border border-line text-sm focus:outline-none focus:border-ink transition-colors"
            />
            <textarea
              name="body"
              value={form.body}
              onChange={handleChange}
              rows={6}
              placeholder="详细描述您的问题或需求"
              required
              className="w-full px-4 py-3 rounded-xl bg-white border border-line text-sm focus:outline-none focus:border-ink transition-colors resize-none"
            />
            <button
              type="submit"
              disabled={status === 'sending'}
              className="inline-flex h-11 items-center px-6 rounded-full bg-ink text-white text-sm font-medium hover:bg-neutral-800 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {status === 'sending' ? '提交中…' : '提交'}
            </button>
            {status === 'sent' && (
              <p className="text-emerald-600 text-sm">已收到，谢谢您的留言。</p>
            )}
            {status === 'error' && (
              <p className="text-red-600 text-sm">提交失败，请稍后重试。</p>
            )}
          </form>
        </div>
      </section>
    </div>
  )
}
