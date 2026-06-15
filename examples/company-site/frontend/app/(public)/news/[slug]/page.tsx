'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'

import CommentSection from '@/components/CommentSection'
import Container from '@/components/Container'
import { getNewsBySlug, News } from '@/services/news'
import { toAbsoluteUrl } from '@/services/uploads'

interface PageProps {
  params: { slug: string }
}

function formatDate(s: string | null) {
  if (!s) return ''
  const d = new Date(s)
  return `${d.getFullYear()} 年 ${d.getMonth() + 1} 月 ${d.getDate()} 日`
}

export default function NewsDetailPage({ params }: PageProps) {
  const [news, setNews] = useState<News | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    getNewsBySlug(params.slug)
      .then(setNews)
      .catch((e) => setError(e instanceof Error ? e.message : '加载失败'))
      .finally(() => setLoading(false))
  }, [params.slug])

  if (loading) {
    return (
      <Container className="py-32" size="narrow">
        <div className="h-12 bg-surface-alt animate-pulse rounded mb-8" />
        <div className="h-72 bg-surface-alt animate-pulse rounded-2xl" />
      </Container>
    )
  }

  if (error || !news) {
    return (
      <Container className="py-32 text-center">
        <h1 className="text-3xl font-semibold text-ink mb-4">未找到该新闻</h1>
        <p className="text-ink-muted mb-8">{error || '可能已下架。'}</p>
        <Link
          href="/news"
          className="inline-flex h-11 items-center px-6 rounded-full bg-ink text-white text-sm hover:bg-neutral-800 transition-colors cursor-pointer"
        >
          返回新闻列表
        </Link>
      </Container>
    )
  }

  return (
    <article>
      <section className="pt-24 md:pt-32 pb-10">
        <Container size="narrow">
          <Link
            href="/news"
            className="inline-flex items-center text-xs uppercase tracking-wider text-ink-muted hover:text-ink transition-colors cursor-pointer mb-6"
          >
            ← 返回新闻
          </Link>
          <div className="text-xs uppercase tracking-wider text-ink-muted mb-4">
            {formatDate(news.published_at || news.created_at)}
            {news.author && <span className="mx-2">·</span>}
            {news.author}
          </div>
          <h1 className="text-4xl md:text-6xl font-semibold tracking-tightest text-ink leading-[1.05]">
            {news.title}
          </h1>
          {news.summary && (
            <p className="mt-6 text-lg md:text-xl text-ink-muted leading-relaxed">
              {news.summary}
            </p>
          )}
        </Container>
      </section>

      {news.cover_image && (
        <section className="pb-12">
          <Container>
            <div className="rounded-3xl overflow-hidden bg-surface-alt h-[300px] md:h-[480px]">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={toAbsoluteUrl(news.cover_image)} alt={news.title} className="w-full h-full object-cover" />
            </div>
          </Container>
        </section>
      )}

      <section className="pb-16">
        <Container size="narrow">
          <div className="text-base md:text-lg text-ink leading-[1.8] whitespace-pre-wrap">
            {news.content}
          </div>
        </Container>
      </section>

      <section className="pb-24">
        <Container size="narrow">
          <CommentSection targetType="news" targetId={news.id} />
        </Container>
      </section>
    </article>
  )
}
