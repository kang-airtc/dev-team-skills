'use client'

import { useRouter } from 'next/navigation'
import { FormEvent, useEffect, useState } from 'react'

import ImageUploader from '@/components/admin/ImageUploader'
import { createNews, getNews, News, NewsInput, updateNews } from '@/services/news'

interface FormState {
  title: string
  slug: string
  summary: string
  cover_image: string
  content: string
  author: string
  is_published: boolean
  published_at: string
}

const empty: FormState = {
  title: '',
  slug: '',
  summary: '',
  cover_image: '',
  content: '',
  author: '',
  is_published: true,
  published_at: '',
}

function fromNews(n: News): FormState {
  return {
    title: n.title,
    slug: n.slug,
    summary: n.summary || '',
    cover_image: n.cover_image || '',
    content: n.content || '',
    author: n.author || '',
    is_published: n.is_published,
    published_at: n.published_at ? n.published_at.slice(0, 16) : '',
  }
}

export default function NewsForm({ id }: { id?: number }) {
  const router = useRouter()
  const [form, setForm] = useState<FormState>(empty)
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    getNews(id)
      .then((n) => setForm(fromNews(n)))
      .catch((e) => setError(e instanceof Error ? e.message : '加载失败'))
      .finally(() => setLoading(false))
  }, [id])

  const update = <K extends keyof FormState>(k: K, v: FormState[K]) =>
    setForm((s) => ({ ...s, [k]: v }))

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    if (!form.title.trim() || !form.slug.trim() || !form.content.trim()) {
      setError('标题、slug、正文必填')
      return
    }
    const payload: NewsInput = {
      title: form.title.trim(),
      slug: form.slug.trim(),
      summary: form.summary.trim() || null,
      cover_image: form.cover_image.trim() || null,
      content: form.content,
      author: form.author.trim() || null,
      is_published: form.is_published,
      published_at: form.published_at ? new Date(form.published_at).toISOString() : null,
    }
    setSubmitting(true)
    try {
      if (id) await updateNews(id, payload)
      else await createNews(payload)
      router.push('/dashboard/news')
    } catch (err) {
      setError(err instanceof Error ? err.message : '提交失败')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <div className="text-sm text-ink-muted">加载中…</div>

  return (
    <form onSubmit={submit} className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 space-y-4">
        <div className="rounded-2xl bg-white border border-line p-6 space-y-4">
          <Field label="标题 *">
            <input className={input} value={form.title} onChange={(e) => update('title', e.target.value)} />
          </Field>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Field label="Slug *">
              <input className={input} value={form.slug} onChange={(e) => update('slug', e.target.value)} placeholder="phone-pro-16-launch" />
            </Field>
            <Field label="作者">
              <input className={input} value={form.author} onChange={(e) => update('author', e.target.value)} />
            </Field>
          </div>
          <Field label="摘要">
            <textarea className={`${input} h-auto py-3`} rows={2} value={form.summary} onChange={(e) => update('summary', e.target.value)} />
          </Field>
          <Field label="封面图">
            <ImageUploader
              value={form.cover_image}
              onChange={(url) => update('cover_image', url)}
            />
          </Field>
          <Field label="正文 *">
            <textarea className={`${input} h-auto py-3`} rows={14} value={form.content} onChange={(e) => update('content', e.target.value)} />
          </Field>
        </div>
      </div>

      <div className="space-y-4">
        <div className="rounded-2xl bg-white border border-line p-6 space-y-4">
          <div className="text-sm font-semibold text-ink">发布</div>
          <label className="flex items-center justify-between cursor-pointer">
            <span className="text-sm text-ink">已发布</span>
            <button
              type="button"
              onClick={() => update('is_published', !form.is_published)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 cursor-pointer ${
                form.is_published ? 'bg-ink' : 'bg-line'
              }`}
            >
              <span
                className={`inline-block h-5 w-5 transform rounded-full bg-white shadow transition-transform duration-200 ${
                  form.is_published ? 'translate-x-5' : 'translate-x-0.5'
                }`}
              />
            </button>
          </label>
          <Field label="发布时间">
            <input
              type="datetime-local"
              className={input}
              value={form.published_at}
              onChange={(e) => update('published_at', e.target.value)}
            />
          </Field>
        </div>

        {error && (
          <div className="rounded-xl bg-red-50 border border-red-200 p-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <div className="flex gap-2">
          <button
            type="submit"
            disabled={submitting}
            className="flex-1 inline-flex h-11 items-center justify-center px-5 rounded-full bg-ink text-white text-sm font-medium hover:bg-neutral-800 transition-colors cursor-pointer disabled:opacity-50"
          >
            {submitting ? '保存中…' : id ? '保存修改' : '发布新闻'}
          </button>
          <button
            type="button"
            onClick={() => router.push('/dashboard/news')}
            className="inline-flex h-11 items-center px-5 rounded-full bg-surface-alt text-sm hover:bg-neutral-200 transition-colors cursor-pointer"
          >
            取消
          </button>
        </div>
      </div>
    </form>
  )
}

const input =
  'w-full h-10 px-3 rounded-xl bg-surface-alt border border-line text-sm focus:outline-none focus:border-ink focus:bg-white transition-colors'

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block">
      <div className="text-xs font-medium text-ink-muted mb-1.5 uppercase tracking-wider">
        {label}
      </div>
      {children}
    </label>
  )
}
