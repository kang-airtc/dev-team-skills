import Link from 'next/link'

import Logo from './Logo'

const COLUMNS = [
  {
    title: '产品',
    links: [
      { href: '/products?category=phone', label: '手机' },
      { href: '/products?category=tablet', label: '平板' },
      { href: '/products?category=laptop', label: '笔记本' },
      { href: '/products?category=accessory', label: '配件' },
    ],
  },
  {
    title: '关于',
    links: [
      { href: '/about', label: '公司故事' },
      { href: '/news', label: '最新动态' },
      { href: '/contact', label: '联系我们' },
    ],
  },
  {
    title: '支持',
    links: [
      { href: '/contact', label: '客户服务' },
      { href: '/contact', label: '售后政策' },
      { href: '/contact', label: '问题反馈' },
    ],
  },
]

export default function Footer() {
  return (
    <footer className="border-t border-line bg-white">
      <div className="max-w-7xl mx-auto px-6 md:px-8 py-16 grid grid-cols-2 md:grid-cols-5 gap-10">
        <div className="col-span-2">
          <Logo />
          <p className="mt-4 text-sm text-ink-muted leading-relaxed max-w-sm">
            （示例品牌占位，随书学习用。）
            我们用极致的工艺与简洁的设计，让每一件产品成为生活的延伸。
          </p>
        </div>
        {COLUMNS.map((col) => (
          <div key={col.title}>
            <div className="text-sm font-semibold text-ink mb-4">{col.title}</div>
            <ul className="space-y-3">
              {col.links.map((l) => (
                <li key={l.label}>
                  <Link
                    href={l.href}
                    className="text-sm text-ink-muted hover:text-ink transition-colors cursor-pointer"
                  >
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div className="border-t border-line">
        <div className="max-w-7xl mx-auto px-6 md:px-8 py-6 flex flex-col md:flex-row items-center justify-between gap-3 text-xs text-ink-muted">
          <div>© {new Date().getFullYear()} 某某科技 · 示例骨架，仅供学习</div>
          <div className="flex items-center gap-5">
            <Link href="/about" className="hover:text-ink transition-colors">隐私政策</Link>
            <Link href="/about" className="hover:text-ink transition-colors">使用条款</Link>
            <Link href="/contact" className="hover:text-ink transition-colors">联系我们</Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
