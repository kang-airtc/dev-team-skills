'use client'

import { useEffect, useState } from 'react'

import Container from '@/components/Container'
import NewsCard from '@/components/NewsCard'
import { listNews, News } from '@/services/news'

export default function NewsListPage() {
  const [items, setItems] = useState<News[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    listNews({ limit: 60 })
      .then((r) => setItems(r.items))
      .catch(() => setItems([]))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div>
      <section className="pt-24 md:pt-32 pb-12 bg-gradient-to-b from-surface-alt to-white">
        <Container>
          <div className="text-sm font-medium text-ink-muted uppercase tracking-wider mb-4">
            Newsroom
          </div>
          <h1 className="text-5xl md:text-7xl font-semibold tracking-tightest text-ink leading-[1.02]">
            最新动态
          </h1>
          <p className="mt-6 text-lg text-ink-muted max-w-2xl">
            产品发布、品牌故事与公司动向，一网打尽。
          </p>
        </Container>
      </section>

      <section className="py-12 pb-24">
        <Container>
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[0, 1, 2, 3, 4, 5].map((i) => (
                <div
                  key={i}
                  className="h-[360px] rounded-2xl bg-surface-alt animate-pulse"
                />
              ))}
            </div>
          ) : items.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {items.map((n) => (
                <NewsCard key={n.id} news={n} />
              ))}
            </div>
          ) : (
            <div className="rounded-2xl border border-dashed border-line p-16 text-center text-ink-muted text-sm">
              暂无新闻。请在后台发布。
            </div>
          )}
        </Container>
      </section>
    </div>
  )
}
