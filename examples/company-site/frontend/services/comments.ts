import { httpDelete, httpGet, httpPost, httpPut } from '@/utils/request'

export type CommentTargetType = 'product' | 'news'

export interface Comment {
  id: number
  target_type: CommentTargetType
  target_id: number
  user_id: number | null
  nickname: string
  content: string
  is_approved: boolean
  created_at: string
}

export interface CommentListResult {
  items: Comment[]
  total: number
}

export interface CommentInput {
  target_type: CommentTargetType
  target_id: number
  nickname: string
  content: string
}

export interface CommentListParams {
  target_type?: CommentTargetType
  target_id?: number
  limit?: number
  offset?: number
}

export const listComments = (params?: CommentListParams) =>
  httpGet<CommentListResult>('/comments', params)

export const createComment = (data: CommentInput) =>
  httpPost<Comment>('/comments', data)

// 后台
export const listCommentsAdmin = (params?: CommentListParams & { approved_only?: boolean }) =>
  httpGet<CommentListResult>('/comments/admin', params)

export const updateComment = (id: number, data: { is_approved?: boolean }) =>
  httpPut<Comment>(`/comments/${id}`, data)

export const deleteComment = (id: number) =>
  httpDelete<{ id: number }>(`/comments/${id}`)
