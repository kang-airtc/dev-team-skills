import '@/styles/globals.css'
import React from 'react'

export const metadata = {
  title: '某某科技 — 重新定义个人科技',
  description: '高端个人电子产品：手机、平板、笔记本与配件。',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body className="bg-white text-ink antialiased">{children}</body>
    </html>
  )
}
