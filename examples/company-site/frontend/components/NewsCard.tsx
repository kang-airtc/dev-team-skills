import Link from 'next/link'

import { News } from '@/services/news'
import { toAbsoluteUrl } from '@/services/uploads'

function formatDate(s: string | null) {
  if (!s) return ''
  const d = new Date(s)
  return `${d.getFullYear()}/${String(d.getMonth() + 1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}`
}

export default function NewsCard({ news }: { news: News }) {
  return (
    <Link
      href={`/news/${news.slug}`}
      className="group block overflow-hidden rounded-2xl bg-white border border-line cursor-pointer transition-all duration-300 ease-smooth hover:shadow-lift hover:border-neutral-300"
    >
      <div className="aspect-[16/10] bg-surface-alt overflow-hidden">
        {news.cover_image ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={toAbsoluteUrl(news.cover_image)}
            alt={news.title}
            className="w-full h-full object-cover transition-transform duration-500 ease-smooth group-hover:scale-[1.03]"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-neutral-100 to-neutral-200" />
        )}
      </div>
      <div className="p-6">
        <div className="text-xs text-ink-muted mb-3 uppercase tracking-wider">
          {formatDate(news.published_at || news.created_at)}
          {news.author && <span className="mx-2">·</span>}
          {news.author}
        </div>
        <h3 className="text-lg font-semibold text-ink leading-tight group-hover:text-neutral-700 transition-colors line-clamp-2">
          {news.title}
        </h3>
        {news.summary && (
          <p className="mt-2 text-sm text-ink-muted leading-relaxed line-clamp-2">
            {news.summary}
          </p>
        )}
      </div>
    </Link>
  )
}
