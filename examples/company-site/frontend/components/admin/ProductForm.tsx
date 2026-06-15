'use client'

import { useRouter } from 'next/navigation'
import { FormEvent, useEffect, useState } from 'react'

import GalleryUploader from '@/components/admin/GalleryUploader'
import ImageUploader from '@/components/admin/ImageUploader'
import { Category, listCategories } from '@/services/categories'
import {
  createProduct,
  getProduct,
  Product,
  ProductInput,
  updateProduct,
} from '@/services/products'

interface FormState {
  name: string
  slug: string
  category_id: string
  tagline: string
  summary: string
  description: string
  cover_image: string
  gallery: string
  specs: string
  price: string
  is_featured: boolean
  is_published: boolean
  sort_order: string
}

const empty: FormState = {
  name: '',
  slug: '',
  category_id: '',
  tagline: '',
  summary: '',
  description: '',
  cover_image: '',
  gallery: '',
  specs: '',
  price: '',
  is_featured: false,
  is_published: true,
  sort_order: '0',
}

function fromProduct(p: Product): FormState {
  return {
    name: p.name,
    slug: p.slug,
    category_id: p.category_id != null ? String(p.category_id) : '',
    tagline: p.tagline || '',
    summary: p.summary || '',
    description: p.description || '',
    cover_image: p.cover_image || '',
    gallery: p.gallery || '',
    specs: p.specs || '',
    price: p.price != null ? String(p.price) : '',
    is_featured: p.is_featured,
    is_published: p.is_published,
    sort_order: String(p.sort_order ?? 0),
  }
}

export default function ProductForm({ id }: { id?: number }) {
  const router = useRouter()
  const [form, setForm] = useState<FormState>(empty)
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    listCategories().then(setCategories).catch(() => {})
    if (id) {
      setLoading(true)
      getProduct(id)
        .then((p) => setForm(fromProduct(p)))
        .catch((e) => setError(e instanceof Error ? e.message : '加载失败'))
        .finally(() => setLoading(false))
    }
  }, [id])

  const update = <K extends keyof FormState>(key: K, value: FormState[K]) =>
    setForm((s) => ({ ...s, [key]: value }))

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    if (!form.name.trim() || !form.slug.trim()) {
      setError('名称与 slug 必填')
      return
    }
    const payload: ProductInput = {
      name: form.name.trim(),
      slug: form.slug.trim(),
      category_id: form.category_id ? Number(form.category_id) : null,
      tagline: form.tagline.trim() || null,
      summary: form.summary.trim() || null,
      description: form.description || null,
      cover_image: form.cover_image.trim() || null,
      gallery: form.gallery.trim() || null,
      specs: form.specs.trim() || null,
      price: form.price ? Number(form.price) : null,
      is_featured: form.is_featured,
      is_published: form.is_published,
      sort_order: Number(form.sort_order) || 0,
    }
    setSubmitting(true)
    try {
      if (id) await updateProduct(id, payload)
      else await createProduct(payload)
      router.push('/dashboard/products')
    } catch (err) {
      setError(err instanceof Error ? err.message : '提交失败')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return <div className="text-sm text-ink-muted">加载中…</div>
  }

  return (
    <form onSubmit={submit} className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="lg:col-span-2 space-y-4">
        <Card title="基础信息">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Field label="名称 *">
              <input className={input} value={form.name} onChange={(e) => update('name', e.target.value)} />
            </Field>
            <Field label="Slug *">
              <input className={input} value={form.slug} onChange={(e) => update('slug', e.target.value)} placeholder="book-pro-15" />
            </Field>
            <Field label="分类">
              <select
                className={input}
                value={form.category_id}
                onChange={(e) => update('category_id', e.target.value)}
              >
                <option value="">未分类</option>
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </Field>
            <Field label="价格（元）">
              <input
                type="number"
                step="0.01"
                className={input}
                value={form.price}
                onChange={(e) => update('price', e.target.value)}
              />
            </Field>
          </div>

          <Field label="标语（一句话）">
            <input className={input} value={form.tagline} onChange={(e) => update('tagline', e.target.value)} placeholder="轻盈，至极。" />
          </Field>
          <Field label="简介（列表页摘要）">
            <textarea className={`${input} h-auto py-3`} rows={2} value={form.summary} onChange={(e) => update('summary', e.target.value)} />
          </Field>
          <Field label="详情正文">
            <textarea className={`${input} h-auto py-3`} rows={8} value={form.description} onChange={(e) => update('description', e.target.value)} />
          </Field>
        </Card>

        <Card title="媒体">
          <Field label="封面图">
            <ImageUploader
              value={form.cover_image}
              onChange={(url) => update('cover_image', url)}
            />
          </Field>
          <Field label="图集">
            <GalleryUploader
              value={form.gallery}
              onChange={(json) => update('gallery', json)}
            />
          </Field>
          <Field label="规格参数（JSON 对象，例如 {&quot;芯片&quot;: &quot;A18&quot;}）">
            <textarea
              className={`${input} h-auto py-3 font-mono`}
              rows={5}
              value={form.specs}
              onChange={(e) => update('specs', e.target.value)}
            />
          </Field>
        </Card>
      </div>

      <div className="space-y-4">
        <Card title="发布">
          <Toggle
            label="已上架"
            checked={form.is_published}
            onChange={(v) => update('is_published', v)}
          />
          <Toggle
            label="设为推荐（首页 Featured）"
            checked={form.is_featured}
            onChange={(v) => update('is_featured', v)}
          />
          <Field label="排序（小的在前）">
            <input
              type="number"
              className={input}
              value={form.sort_order}
              onChange={(e) => update('sort_order', e.target.value)}
            />
          </Field>
        </Card>

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
            {submitting ? '保存中…' : id ? '保存修改' : '创建产品'}
          </button>
          <button
            type="button"
            onClick={() => router.push('/dashboard/products')}
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

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-2xl bg-white border border-line p-6 space-y-4">
      <div className="text-sm font-semibold text-ink">{title}</div>
      {children}
    </div>
  )
}

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

function Toggle({
  label,
  checked,
  onChange,
}: {
  label: string
  checked: boolean
  onChange: (v: boolean) => void
}) {
  return (
    <label className="flex items-center justify-between cursor-pointer py-1">
      <span className="text-sm text-ink">{label}</span>
      <button
        type="button"
        onClick={() => onChange(!checked)}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors duration-200 cursor-pointer ${
          checked ? 'bg-ink' : 'bg-line'
        }`}
      >
        <span
          className={`inline-block h-5 w-5 transform rounded-full bg-white shadow transition-transform duration-200 ${
            checked ? 'translate-x-5' : 'translate-x-0.5'
          }`}
        />
      </button>
    </label>
  )
}
