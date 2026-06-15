'use client'

import { FormEvent, useEffect, useState } from 'react'

import {
  Comment,
  CommentTargetType,
  createComment,
  listComments,
} from '@/services/comments'

interface Props {
  targetType: CommentTargetType
  targetId: number
}

function formatTime(s: string) {
  const d = new Date(s)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(
    d.getDate(),
  ).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(
    2,
    '0',
  )}`
}

export default function CommentSection({ targetType, targetId }: Props) {
  const [items, setItems] = useState<Comment[]>([])
  const [loading, setLoading] = useState(true)
  const [nickname, setNickname] = useState('')
  const [content, setContent] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchList = () => {
    setLoading(true)
    listComments({ target_type: targetType, target_id: targetId, limit: 100 })
      .then((r) => setItems(r.items))
      .catch(() => setItems([]))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    fetchList()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [targetType, targetId])

  const submit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    if (!nickname.trim() || !content.trim()) {
      setError('昵称与评论内容不能为空')
      return
    }
    try {
      setSubmitting(true)
      await createComment({
        target_type: targetType,
        target_id: targetId,
        nickname: nickname.trim(),
        content: content.trim(),
      })
      setContent('')
      fetchList()
    } catch (err) {
      setError(err instanceof Error ? err.message : '提交失败')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="mt-16 border-t border-line pt-12">
      <h3 className="text-2xl font-semibold tracking-tight text-ink">
        评论 <span className="text-ink-muted text-base font-normal">({items.length})</span>
      </h3>

      <form onSubmit={submit} className="mt-6 rounded-2xl bg-surface-alt p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3">
          <input
            type="text"
            value={nickname}
            onChange={(e) => setNickname(e.target.value)}
            placeholder="昵称"
            maxLength={80}
            className="md:col-span-1 h-11 px-4 rounded-xl bg-white border border-line text-sm focus:outline-none focus:border-ink transition-colors"
          />
        </div>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="留下你的看法..."
          rows={3}
          maxLength={2000}
          className="w-full px-4 py-3 rounded-xl bg-white border border-line text-sm focus:outline-none focus:border-ink transition-colors resize-none"
        />
        {error && <div className="mt-2 text-sm text-red-600">{error}</div>}
        <div className="mt-3 flex justify-end">
          <button
            type="submit"
            disabled={submitting}
            className="inline-flex h-10 items-center px-6 rounded-full bg-ink text-white text-sm font-medium hover:bg-neutral-800 transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {submitting ? '提交中…' : '发表评论'}
          </button>
        </div>
      </form>

      <div className="mt-8 space-y-6">
        {loading ? (
          <div className="text-sm text-ink-muted">加载中…</div>
        ) : items.length === 0 ? (
          <div className="text-sm text-ink-muted">还没有评论，来抢沙发。</div>
        ) : (
          items.map((c) => (
            <div key={c.id} className="flex gap-4">
              <div className="shrink-0 w-10 h-10 rounded-full bg-surface-alt flex items-center justify-center text-sm font-medium text-ink">
                {c.nickname.slice(0, 1).toUpperCase()}
              </div>
              <div className="flex-1">
                <div className="flex items-baseline gap-3">
                  <div className="text-sm font-medium text-ink">{c.nickname}</div>
                  <div className="text-xs text-ink-muted">{formatTime(c.created_at)}</div>
                </div>
                <p className="mt-1 text-sm text-ink leading-relaxed whitespace-pre-wrap">
                  {c.content}
                </p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
