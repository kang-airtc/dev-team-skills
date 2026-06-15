import { httpGet, httpPost } from '@/utils/request'

// 业务接口占位（第 12 章按需补充）
export interface Product {
  id: number
  slug: string
  title: string
  summary: string
  cover_url?: string
}

export interface NewsArticle {
  id: number
  slug: string
  title: string
  excerpt: string
  published_at: string
}

export interface ContactMessage {
  name: string
  email: string
  subject: string
  body: string
}

export const listProducts = () => httpGet<Product[]>('/products')
export const listNews = () => httpGet<NewsArticle[]>('/news')
export const submitMessage = (data: ContactMessage) =>
  httpPost<{ id: number }>('/messages', data)
