'use client'

import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'next/navigation'

import Container from '@/components/Container'
import ProductCard from '@/components/ProductCard'
import { Category, listCategories } from '@/services/categories'
import { listProducts, Product } from '@/services/products'

export default function ProductsPage() {
  const params = useSearchParams()
  const categoryFromUrl = params?.get('category') || null

  const [categories, setCategories] = useState<Category[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [activeSlug, setActiveSlug] = useState<string | null>(categoryFromUrl)

  useEffect(() => {
    listCategories()
      .then(setCategories)
      .catch(() => {})
  }, [])

  const activeCategory = useMemo(
    () => categories.find((c) => c.slug === activeSlug) || null,
    [categories, activeSlug],
  )

  useEffect(() => {
    setLoading(true)
    listProducts({
      category_id: activeCategory?.id,
      limit: 60,
    })
      .then((r) => setProducts(r.items))
      .catch(() => setProducts([]))
      .finally(() => setLoading(false))
  }, [activeCategory])

  useEffect(() => {
    setActiveSlug(categoryFromUrl)
  }, [categoryFromUrl])

  return (
    <div>
      <section className="pt-24 md:pt-32 pb-12 bg-gradient-to-b from-surface-alt to-white">
        <Container>
          <div className="text-sm font-medium text-ink-muted uppercase tracking-wider mb-4">
            Products
          </div>
          <h1 className="text-5xl md:text-7xl font-semibold tracking-tightest text-ink leading-[1.02]">
            为你而造的全系产品
          </h1>
          <p className="mt-6 text-lg text-ink-muted max-w-2xl">
            从随身的手机到桌面的笔记本，每一件都恪守同一种品质。
          </p>
        </Container>
      </section>

      <section className="py-12">
        <Container>
          <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pb-2">
            <FilterChip
              label="全部"
              active={!activeSlug}
              onClick={() => setActiveSlug(null)}
            />
            {categories.map((c) => (
              <FilterChip
                key={c.id}
                label={c.name}
                active={activeSlug === c.slug}
                onClick={() => setActiveSlug(c.slug)}
              />
            ))}
          </div>

          <div className="mt-10">
            {loading ? (
              <SkeletonGrid />
            ) : products.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {products.map((p) => (
                  <ProductCard key={p.id} product={p} />
                ))}
              </div>
            ) : (
              <div className="rounded-2xl border border-dashed border-line p-16 text-center text-ink-muted text-sm">
                {activeCategory
                  ? `「${activeCategory.name}」分类下暂无产品。`
                  : '暂无产品。请在后台添加。'}
              </div>
            )}
          </div>
        </Container>
      </section>
    </div>
  )
}

function FilterChip({
  label,
  active,
  onClick,
}: {
  label: string
  active: boolean
  onClick: () => void
}) {
  return (
    <button
      onClick={onClick}
      className={`shrink-0 inline-flex h-9 items-center px-4 rounded-full text-sm font-medium transition-colors duration-200 cursor-pointer ${
        active
          ? 'bg-ink text-white'
          : 'bg-surface-alt text-ink hover:bg-neutral-200'
      }`}
    >
      {label}
    </button>
  )
}

function SkeletonGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[0, 1, 2, 3, 4, 5].map((i) => (
        <div
          key={i}
          className="h-[360px] rounded-3xl bg-surface-alt animate-pulse"
        />
      ))}
    </div>
  )
}
