import { httpDelete, httpGet, httpPost, httpPut } from '@/utils/request'

export interface Category {
  id: number
  name: string
  slug: string
  description: string | null
  sort_order: number
  created_at: string
  updated_at: string
}

export interface CategoryInput {
  name: string
  slug: string
  description?: string | null
  sort_order?: number
}

export const listCategories = () => httpGet<Category[]>('/categories')
export const createCategory = (data: CategoryInput) => httpPost<Category>('/categories', data)
export const updateCategory = (id: number, data: Partial<CategoryInput>) =>
  httpPut<Category>(`/categories/${id}`, data)
export const deleteCategory = (id: number) => httpDelete<{ id: number }>(`/categories/${id}`)
