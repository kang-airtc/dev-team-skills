'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'

import Container from '@/components/Container'
import NewsCard from '@/components/NewsCard'
import ProductCard from '@/components/ProductCard'
import SectionHeader from '@/components/SectionHeader'
import { listNews, News } from '@/services/news'
import { listProducts, Product } from '@/services/products'

export default function HomePage() {
  const [featured, setFeatured] = useState<Product[]>([])
  const [latest, setLatest] = useState<Product[]>([])
  const [news, setNews] = useState<News[]>([])

  useEffect(() => {
    listProducts({ is_featured: true, limit: 4 })
      .then((r) => setFeatured(r.items))
      .catch(() => {})
    listProducts({ limit: 6 })
      .then((r) => setLatest(r.items))
      .catch(() => {})
    listNews({ limit: 3 })
      .then((r) => setNews(r.items))
      .catch(() => {})
  }, [])

  return (
    <div>
      {/* Hero */}
      <section className="relative pt-20 md:pt-28 pb-20 md:pb-32 overflow-hidden">
        <div className="absolute inset-0 -z-10 bg-gradient-to-b from-surface-alt via-white to-white" />
        <Container>
          <div className="text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white border border-line text-xs font-medium text-ink-muted mb-8">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              全新系列 · 即刻上市
            </div>
            <h1 className="text-5xl md:text-7xl font-semibold tracking-tightest text-ink leading-[1.02]">
              重新定义
              <br />
              个人科技体验
            </h1>
            <p className="mt-6 text-lg md:text-xl text-ink-muted leading-relaxed max-w-2xl mx-auto">
              手机、平板、笔记本与配件。
              <br className="hidden md:block" />
              更轻、更快，也更懂你。
            </p>
            <div className="mt-10 flex items-center justify-center gap-3">
              <Link
                href="/products"
                className="inline-flex h-12 items-center px-8 rounded-full bg-ink text-white text-[15px] font-medium hover:bg-neutral-800 transition-colors cursor-pointer"
              >
                探索产品
              </Link>
              <Link
                href="/about"
                className="inline-flex h-12 items-center px-8 rounded-full text-ink text-[15px] font-medium hover:bg-surface-alt transition-colors cursor-pointer"
              >
                了解品牌 →
              </Link>
            </div>
          </div>
        </Container>

        {/* Hero visual */}
        <Container className="mt-16 md:mt-20">
          <div className="relative h-[360px] md:h-[520px] rounded-3xl bg-gradient-to-br from-neutral-100 via-white to-neutral-200 overflow-hidden border border-line">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-72 h-72 md:w-96 md:h-96 rounded-full bg-gradient-to-br from-white to-neutral-200 shadow-lift opacity-90" />
            </div>
            <div className="absolute bottom-8 left-8 md:bottom-12 md:left-12">
              <div className="text-xs uppercase tracking-wider text-ink-muted mb-2">
                Pro 系列
              </div>
              <div className="text-2xl md:text-3xl font-semibold tracking-tight text-ink">
                轻盈，至极。
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* Featured bento */}
      <section className="py-20 md:py-28">
        <Container>
          <SectionHeader
            eyebrow="Featured"
            title="精选系列"
            description="为不同场景而生，为每一份细节而精雕细琢。"
          />
          {featured.length > 0 ? (
            <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-6">
              {featured.map((p, i) => (
                <ProductCard key={p.id} product={p} variant={i < 2 ? 'feature' : 'default'} />
              ))}
            </div>
          ) : (
            <EmptyHint text="后台添加产品并标记为「推荐」后将显示在此。" />
          )}
        </Container>
      </section>

      {/* Categories */}
      <section className="py-16 bg-surface-alt">
        <Container>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { name: '手机', slug: 'phone' },
              { name: '平板', slug: 'tablet' },
              { name: '笔记本', slug: 'laptop' },
              { name: '配件', slug: 'accessory' },
            ].map((c) => (
              <Link
                key={c.slug}
                href={`/products?category=${c.slug}`}
                className="group flex flex-col items-center justify-center h-40 rounded-2xl bg-white border border-line cursor-pointer transition-all duration-300 ease-smooth hover:shadow-soft hover:-translate-y-0.5"
              >
                <div className="w-12 h-12 rounded-2xl bg-surface-alt mb-3 flex items-center justify-center text-ink group-hover:bg-ink group-hover:text-white transition-colors">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6">
                    <rect x="6" y="3" width="12" height="18" rx="2" />
                    <circle cx="12" cy="17.5" r="0.6" fill="currentColor" />
                  </svg>
                </div>
                <div className="text-sm font-medium text-ink">{c.name}</div>
                <div className="text-xs text-ink-muted mt-1">查看全部 →</div>
              </Link>
            ))}
          </div>
        </Container>
      </section>

      {/* Latest products */}
      {latest.length > 0 && (
        <section className="py-20 md:py-28">
          <Container>
            <div className="flex items-end justify-between flex-wrap gap-4">
              <SectionHeader eyebrow="Catalog" title="最新上架" />
              <Link
                href="/products"
                className="text-sm font-medium text-ink hover:text-ink-muted transition-colors cursor-pointer"
              >
                浏览全部 →
              </Link>
            </div>
            <div className="mt-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {latest.map((p) => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          </Container>
        </section>
      )}

      {/* News */}
      <section className="py-20 md:py-28 bg-surface-alt">
        <Container>
          <div className="flex items-end justify-between flex-wrap gap-4">
            <SectionHeader eyebrow="Newsroom" title="最新动态" />
            <Link
              href="/news"
              className="text-sm font-medium text-ink hover:text-ink-muted transition-colors cursor-pointer"
            >
              全部新闻 →
            </Link>
          </div>
          {news.length > 0 ? (
            <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-6">
              {news.map((n) => (
                <NewsCard key={n.id} news={n} />
              ))}
            </div>
          ) : (
            <EmptyHint text="后台发布新闻后将显示在此。" />
          )}
        </Container>
      </section>

      {/* CTA */}
      <section className="py-24">
        <Container>
          <div className="rounded-3xl bg-ink text-white px-8 md:px-16 py-16 md:py-24 text-center">
            <h3 className="text-3xl md:text-5xl font-semibold tracking-tightest leading-[1.05]">
              你的下一台设备，
              <br />
              已经在路上。
            </h3>
            <p className="mt-4 text-base md:text-lg text-neutral-300 max-w-xl mx-auto">
              加入我们，一起塑造更轻盈、更直觉的科技日常。
            </p>
            <div className="mt-10">
              <Link
                href="/contact"
                className="inline-flex h-12 items-center px-8 rounded-full bg-white text-ink text-[15px] font-medium hover:bg-neutral-200 transition-colors cursor-pointer"
              >
                联系我们
              </Link>
            </div>
          </div>
        </Container>
      </section>
    </div>
  )
}

function EmptyHint({ text }: { text: string }) {
  return (
    <div className="mt-12 rounded-2xl border border-dashed border-line p-12 text-center text-ink-muted text-sm">
      {text}
    </div>
  )
}
