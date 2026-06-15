import { API_BASE } from 'config'

import request from '@/utils/request'

export interface UploadResult {
  url: string
  size: number
  mime: string
}

/**
 * 单文件上传。返回 **绝对 URL**（已拼上 host），可直接用于 <img src>。
 *
 * 用配置好的 axios 实例发送，自动带 Authorization 与 401 自动刷新。
 * 不要硬写 Content-Type —— 浏览器会自动加上 multipart/form-data 的 boundary。
 */
export async function uploadImage(file: File): Promise<UploadResult> {
  const fd = new FormData()
  fd.append('file', file)
  const data = (await request.post('/uploads', fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })) as UploadResult
  return { ...data, url: toAbsoluteUrl(data.url) }
}

/** 多文件上传 */
export async function uploadImages(files: File[]): Promise<string[]> {
  const fd = new FormData()
  files.forEach((f) => fd.append('files', f))
  const data = (await request.post('/uploads/multi', fd, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })) as { urls: string[] }
  return (data.urls || []).map(toAbsoluteUrl)
}

/**
 * 把 /uploads/... 这种相对路径补全成完整 URL（host 来自 API_BASE）。
 * 已经是绝对 URL（http/https）的不动。
 */
export function toAbsoluteUrl(url: string): string {
  if (!url) return url
  if (/^https?:\/\//i.test(url)) return url
  // API_BASE 一般是 http://localhost:8000/api，需要去掉 /api
  const apiOrigin = API_BASE.replace(/\/api\/?$/, '')
  return apiOrigin + (url.startsWith('/') ? url : `/${url}`)
}
