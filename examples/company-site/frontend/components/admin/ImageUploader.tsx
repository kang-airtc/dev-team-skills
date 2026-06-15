'use client'

import { ChangeEvent, useRef, useState } from 'react'

import { toAbsoluteUrl, uploadImage } from '@/services/uploads'

interface Props {
  /** 当前图片 URL（可以是 /uploads/... 相对路径，或外链） */
  value: string
  onChange: (url: string) => void
  /** 显示比例，默认 16:10 */
  aspect?: string
  className?: string
}

/**
 * 图片上传 + 预览 + URL 手动输入三合一。
 */
export default function ImageUploader({
  value,
  onChange,
  aspect = 'aspect-[16/10]',
  className = '',
}: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleFile = async (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    e.target.value = '' // 允许选择相同文件
    if (!file) return
    setError(null)
    setUploading(true)
    try {
      const result = await uploadImage(file)
      onChange(result.url)
    } catch (err) {
      setError(err instanceof Error ? err.message : '上传失败')
    } finally {
      setUploading(false)
    }
  }

  const previewSrc = value ? toAbsoluteUrl(value) : ''

  return (
    <div className={className}>
      <div
        className={`relative w-full ${aspect} rounded-2xl overflow-hidden bg-surface-alt border border-line group`}
      >
        {previewSrc ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={previewSrc}
            alt="封面预览"
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-ink-muted text-sm">
            暂无图片
          </div>
        )}

        {uploading && (
          <div className="absolute inset-0 bg-white/70 flex items-center justify-center text-sm text-ink">
            上传中…
          </div>
        )}
      </div>

      <div className="mt-3 flex flex-wrap items-center gap-2">
        <button
          type="button"
          onClick={() => inputRef.current?.click()}
          disabled={uploading}
          className="inline-flex h-9 items-center px-4 rounded-full bg-ink text-white text-sm font-medium hover:bg-neutral-800 transition-colors cursor-pointer disabled:opacity-50"
        >
          {value ? '替换图片' : '上传图片'}
        </button>
        {value && (
          <button
            type="button"
            onClick={() => onChange('')}
            className="inline-flex h-9 items-center px-4 rounded-full bg-surface-alt text-sm hover:bg-neutral-200 transition-colors cursor-pointer"
          >
            清除
          </button>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp,image/gif"
          onChange={handleFile}
          className="hidden"
        />
      </div>

      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="或粘贴图片 URL（http://… 或 /uploads/…）"
        className="mt-3 w-full h-10 px-3 rounded-xl bg-surface-alt border border-line text-sm focus:outline-none focus:border-ink focus:bg-white transition-colors"
      />

      {error && <div className="mt-2 text-xs text-red-600">{error}</div>}
    </div>
  )
}
