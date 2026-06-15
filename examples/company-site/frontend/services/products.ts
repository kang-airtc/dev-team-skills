import { httpDelete, httpGet, httpPost, httpPut } from '@/utils/request'

export interface Product {
  id: number
  name: string
  slug: string
  category_id: number | null
  tagline: string | null
  summary: string | null
  description: string | null
  cover_image: string | null
  gallery: string | null
  specs: string | null
  price: string | number | null
  is_featured: boolean
  is_published: boolean
  sort_order: number
  created_at: string
  updated_at: string
}

export interface ProductListResult {
  items: Product[]
  total: number
}

export interface ProductInput {
  name: string
  slug: string
  category_id?: number | null
  tagline?: string | null
  summary?: string | null
  description?: string | null
  cover_image?: string | null
  gallery?: string | null
  specs?: string | null
  price?: number | null
  is_featured?: boolean
  is_published?: boolean
  sort_order?: number
}

export interface ProductListParams {
  category_id?: number
  is_featured?: boolean
  include_unpublished?: boolean
  limit?: number
  offset?: number
}

export const listProducts = (params?: ProductListParams) =>
  httpGet<ProductListResult>('/products', params)

export const getProductBySlug = (slug: string) =>
  httpGet<Product>(`/products/slug/${slug}`)

export const getProduct = (id: number) => httpGet<Product>(`/products/${id}`)

export const createProduct = (data: ProductInput) => httpPost<Product>('/products', data)

export const updateProduct = (id: number, data: Partial<ProductInput>) =>
  httpPut<Product>(`/products/${id}`, data)

export const deleteProduct = (id: number) =>
  httpDelete<{ id: number }>(`/products/${id}`)
