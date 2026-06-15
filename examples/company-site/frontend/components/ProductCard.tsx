import Link from 'next/link'

import { Product } from '@/services/products'
import { toAbsoluteUrl } from '@/services/uploads'

interface Props {
  product: Product
  variant?: 'default' | 'feature'
}

/**
 * 「上图下文」卡片：保证文字清晰、视觉一致。
 * - 图片在上方占 60%，object-cover 自适应裁切
 * - 文字在白色面板上，深色字保证对比度
 */
export default function ProductCard({ product, variant = 'default' }: Props) {
  const isFeature = variant === 'feature'

  return (
    <Link
      href={`/products/${product.slug}`}
      className="group block overflow-hidden rounded-3xl bg-white border border-line cursor-pointer transition-all duration-300 ease-smooth hover:shadow-lift hover:border-neutral-300"
    >
      <div
        className={`relative w-full overflow-hidden bg-surface-alt ${
          isFeature ? 'aspect-[16/10]' : 'aspect-[4/3]'
        }`}
      >
        {product.cover_image ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={toAbsoluteUrl(product.cover_image)}
            alt={product.name}
            className="w-full h-full object-cover transition-transform duration-500 ease-smooth group-hover:scale-[1.03]"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-neutral-100 via-white to-neutral-200" />
        )}
      </div>

      <div className={`p-6 md:p-7 ${isFeature ? 'md:p-8' : ''}`}>
        {product.tagline && (
          <div className="text-xs font-medium uppercase tracking-wider text-ink-muted mb-2">
            {product.tagline}
          </div>
        )}
        <h3
          className={`font-semibold tracking-tight text-ink leading-tight ${
            isFeature ? 'text-2xl md:text-3xl' : 'text-xl'
          }`}
        >
          {product.name}
        </h3>
        {product.summary && (
          <p className="mt-2 text-sm text-ink-muted leading-relaxed line-clamp-2">
            {product.summary}
          </p>
        )}

        <div className="mt-5 flex items-center justify-between">
          {product.price != null ? (
            <div className="text-sm text-ink">
              <span className="text-ink-muted">起售 </span>
              <span className="font-semibold">
                ¥{Number(product.price).toLocaleString()}
              </span>
            </div>
          ) : (
            <span className="text-sm text-ink-muted">了解详情</span>
          )}
          <span className="inline-flex items-center text-sm font-medium text-ink transition-transform duration-200 group-hover:translate-x-1">
            查看
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              className="ml-1"
            >
              <path
                d="M5 12h14M13 5l7 7-7 7"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </span>
        </div>
      </div>
    </Link>
  )
}
