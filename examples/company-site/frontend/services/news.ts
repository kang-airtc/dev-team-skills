import { httpDelete, httpGet, httpPost, httpPut } from '@/utils/request'

export interface News {
  id: number
  title: string
  slug: string
  summary: string | null
  cover_image: string | null
  content: string
  author: string | null
  is_published: boolean
  published_at: string | null
  created_at: string
  updated_at: string
}

export interface NewsListResult {
  items: News[]
  total: number
}

export interface NewsInput {
  title: string
  slug: string
  summary?: string | null
  cover_image?: string | null
  content: string
  author?: string | null
  is_published?: boolean
  published_at?: string | null
}

export interface NewsListParams {
  include_unpublished?: boolean
  limit?: number
  offset?: number
}

export const listNews = (params?: NewsListParams) =>
  httpGet<NewsListResult>('/news', params)

export const getNewsBySlug = (slug: string) => httpGet<News>(`/news/slug/${slug}`)

export const getNews = (id: number) => httpGet<News>(`/news/${id}`)

export const createNews = (data: NewsInput) => httpPost<News>('/news', data)

export const updateNews = (id: number, data: Partial<NewsInput>) =>
  httpPut<News>(`/news/${id}`, data)

export const deleteNews = (id: number) =>
  httpDelete<{ id: number }>(`/news/${id}`)
