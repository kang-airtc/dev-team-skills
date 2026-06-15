'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'

import CommentSection from '@/components/CommentSection'
import Container from '@/components/Container'
import { getProductBySlug, Product } from '@/services/products'
import { toAbsoluteUrl } from '@/services/uploads'

interface PageProps {
  params: { slug: string }
}

function parseJSON<T>(s: string | null | undefined, fallback: T): T {
  if (!s) return fallback
  try {
    return JSON.parse(s) as T
  } catch {
    return fallback
  }
}

export default function ProductDetailPage({ params }: PageProps) {
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    getProductBySlug(params.slug)
      .then(setProduct)
      .catch((e) => setError(e instanceof Error ? e.message : '加载失败'))
      .finally(() => setLoading(false))
  }, [params.slug])

  if (loading) {
    return (
      <Container className="py-32">
        <div className="h-[420px] rounded-3xl bg-surface-alt animate-pulse" />
      </Container>
    )
  }

  if (error || !product) {
    return (
      <Container className="py-32 text-center">
        <h1 className="text-3xl font-semibold text-ink mb-4">未找到该产品</h1>
        <p className="text-ink-muted mb-8">{error || '产品可能已下架。'}</p>
        <Link
          href="/products"
          className="inline-flex h-11 items-center px-6 rounded-full bg-ink text-white text-sm hover:bg-neutral-800 transition-colors cursor-pointer"
        >
          返回产品列表
        </Link>
      </Container>
    )
  }

  const gallery = parseJSON<string[]>(product.gallery, [])
  const specs = parseJSON<Record<string, string>>(product.specs, {})

  return (
    <div>
      <section className="pt-20 md:pt-28 pb-12 bg-gradient-to-b from-surface-alt to-white">
        <Container>
          <div className="text-xs uppercase tracking-wider text-ink-muted mb-4">
            <Link href="/products" className="hover:text-ink transition-colors cursor-pointer">
              产品
            </Link>
            <span className="mx-2">/</span>
            {product.name}
          </div>
          {product.tagline && (
            <div className="text-sm font-medium text-ink-muted mb-3">{product.tagline}</div>
          )}
          <h1 className="text-5xl md:text-7xl font-semibold tracking-tightest text-ink leading-[1.02]">
            {product.name}
          </h1>
          {product.summary && (
            <p className="mt-6 text-lg md:text-xl text-ink-muted leading-relaxed max-w-3xl">
              {product.summary}
            </p>
          )}
          {product.price != null && (
            <div className="mt-6 text-xl text-ink">
              <span className="text-ink-muted text-base">起售 </span>
              <span className="font-semibold">
                ¥{Number(product.price).toLocaleString()}
              </span>
            </div>
          )}
        </Container>
      </section>

      <section className="pb-12">
        <Container>
          <div className="rounded-3xl bg-surface-alt overflow-hidden h-[360px] md:h-[560px] flex items-center justify-center">
            {product.cover_image ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                src={toAbsoluteUrl(product.cover_image)}
                alt={product.name}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-72 h-72 md:w-96 md:h-96 rounded-full bg-gradient-to-br from-white to-neutral-200 shadow-lift" />
            )}
          </div>

          {gallery.length > 0 && (
            <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
              {gallery.map((src, i) => (
                <div
                  key={i}
                  className="aspect-square rounded-2xl bg-surface-alt overflow-hidden"
                >
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={toAbsoluteUrl(src)} alt={`${product.name} ${i + 1}`} className="w-full h-full object-cover" />
                </div>
              ))}
            </div>
          )}
        </Container>
      </section>

      {product.description && (
        <section className="py-16">
          <Container size="narrow">
            <div className="prose prose-neutral max-w-none">
              <p className="text-base md:text-lg text-ink leading-relaxed whitespace-pre-wrap">
                {product.description}
              </p>
            </div>
          </Container>
        </section>
      )}

      {Object.keys(specs).length > 0 && (
        <section className="py-16 bg-surface-alt">
          <Container size="narrow">
            <h2 className="text-3xl md:text-4xl font-semibold tracking-tightest text-ink mb-8">
              规格参数
            </h2>
            <dl className="rounded-2xl bg-white border border-line divide-y divide-line">
              {Object.entries(specs).map(([k, v]) => (
                <div key={k} className="flex items-start justify-between gap-6 px-6 py-4">
                  <dt className="text-sm text-ink-muted">{k}</dt>
                  <dd className="text-sm text-ink text-right max-w-[60%]">{v}</dd>
                </div>
              ))}
            </dl>
          </Container>
        </section>
      )}

      <section className="py-16">
        <Container size="narrow">
          <CommentSection targetType="product" targetId={product.id} />
        </Container>
      </section>
    </div>
  )
}
