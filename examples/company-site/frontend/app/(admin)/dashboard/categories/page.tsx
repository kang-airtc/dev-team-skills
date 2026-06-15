'use client'

import { FormEvent, useEffect, useState } from 'react'

import AdminShell from '@/components/admin/AdminShell'
import {
  Category,
  createCategory,
  deleteCategory,
  listCategories,
  updateCategory,
} from '@/services/categories'

interface FormState {
  id: number | null
  name: string
  slug: string
  description: string
  sort_order: number
}

const empty: FormState = { id: null, name: '', slug: '', description: '', sort_order: 0 }

export default function CategoriesAdmin() {
  const [items, setItems] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState<FormState>(empty)
  const [error, setError] = useState<string | null>(null)
  const [submitting, setSubmitting] = useState(false)

  const fetchAll = () => {
    setLoading(true)
    listCategories()
      .then(setItems)
      .catch(() => setItems([]))
      .finally(() => setLoading(false))
  }

  useEffect(fetchAll, [])

  const startEdit = (c: Category) => {
    setForm({
      id: c.id,
      name: c.name,
      slug: c.slug,
      description: c.description || '',
      sort_order: c.sort_order,
    })
  }
  const reset = () => setForm(empty)

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    if (!form.name.trim() || !form.slug.trim()) {
      setError('名称与 slug 必填')
      return
    }
    setSubmitting(true)
    try {
      const payload = {
        name: form.name.trim(),
        slug: form.slug.trim(),
        description: form.description.trim() || null,
        sort_order: Number(form.sort_order) || 0,
      }
      if (form.id) await updateCategory(form.id, payload)
      else await createCategory(payload)
      reset()
      fetchAll()
    } catch (err) {
      setError(err instanceof Error ? err.message : '提交失败')
    } finally {
      setSubmitting(false)
    }
  }

  const remove = async (id: number) => {
    if (!confirm('确认删除该分类？')) return
    try {
      await deleteCategory(id)
      fetchAll()
    } catch (err) {
      alert(err instanceof Error ? err.message : '删除失败')
    }
  }

  return (
    <AdminShell title="产品分类" description="管理产品分类（手机 / 平板 / 笔记本 / 配件）。">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <form
          onSubmit={submit}
          className="lg:col-span-1 rounded-2xl bg-white border border-line p-6 space-y-4 h-fit"
        >
          <div className="text-sm font-semibold text-ink">
            {form.id ? '编辑分类' : '新建分类'}
          </div>
          {error && (
            <div className="rounded-xl bg-red-50 border border-red-200 p-3 text-sm text-red-700">
              {error}
            </div>
          )}
          <Field label="名称">
            <input
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              className={inputCls}
              placeholder="手机"
            />
          </Field>
          <Field label="Slug（URL 标识）">
            <input
              value={form.slug}
              onChange={(e) => setForm({ ...form, slug: e.target.value })}
              className={inputCls}
              placeholder="phone"
            />
          </Field>
          <Field label="描述">
            <textarea
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              rows={3}
              className={`${inputCls} h-auto py-3`}
            />
          </Field>
          <Field label="排序（小的在前）">
            <input
              type="number"
              value={form.sort_order}
              onChange={(e) => setForm({ ...form, sort_order: Number(e.target.value) })}
              className={inputCls}
            />
          </Field>
          <div className="flex gap-2 pt-2">
            <button
              type="submit"
              disabled={submitting}
              className="inline-flex h-10 items-center px-5 rounded-full bg-ink text-white text-sm font-medium hover:bg-neutral-800 transition-colors cursor-pointer disabled:opacity-50"
            >
              {form.id ? '保存修改' : '新建'}
            </button>
            {form.id && (
              <button
                type="button"
                onClick={reset}
                className="inline-flex h-10 items-center px-5 rounded-full bg-surface-alt text-sm hover:bg-neutral-200 cursor-pointer"
              >
                取消
              </button>
            )}
          </div>
        </form>

        <div className="lg:col-span-2 rounded-2xl bg-white border border-line overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-surface-alt text-ink-muted text-xs uppercase tracking-wider">
              <tr>
                <th className="text-left px-5 py-3">名称</th>
                <th className="text-left px-5 py-3">Slug</th>
                <th className="text-left px-5 py-3 w-20">排序</th>
                <th className="text-right px-5 py-3 w-32">操作</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={4} className="px-5 py-10 text-center text-ink-muted">
                    加载中…
                  </td>
                </tr>
              ) : items.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-5 py-10 text-center text-ink-muted">
                    暂无分类
                  </td>
                </tr>
              ) : (
                items.map((c) => (
                  <tr key={c.id} className="border-t border-line">
                    <td className="px-5 py-3 font-medium text-ink">{c.name}</td>
                    <td className="px-5 py-3 text-ink-muted">{c.slug}</td>
                    <td className="px-5 py-3 text-ink-muted">{c.sort_order}</td>
                    <td className="px-5 py-3 text-right">
                      <button
                        onClick={() => startEdit(c)}
                        className="text-ink hover:underline cursor-pointer mr-4"
                      >
                        编辑
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
      </div>
    </AdminShell>
  )
}

const inputCls =
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
