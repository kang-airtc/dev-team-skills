'use client'

import { ChangeEvent, useRef, useState } from 'react'

import { toAbsoluteUrl, uploadImages } from '@/services/uploads'

interface Props {
  /** value 是 JSON 字符串（数组），与表单字段保持一致 */
  value: string
  onChange: (jsonValue: string) => void
}

function parseList(value: string): string[] {
  if (!value) return []
  try {
    const v = JSON.parse(value)
    return Array.isArray(v) ? v.filter((x) => typeof x === 'string') : []
  } catch {
    return []
  }
}

/**
 * 多图集上传器：维护一个 URL 数组，序列化为 JSON 字符串存入表单。
 */
export default function GalleryUploader({ value, onChange }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const list = parseList(value)

  const update = (next: string[]) => {
    onChange(JSON.stringify(next))
  }

  const handleFiles = async (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    e.target.value = ''
    if (!files || files.length === 0) return
    setError(null)
    setUploading(true)
    try {
      const urls = await uploadImages(Array.from(files))
      update([...list, ...urls])
    } catch (err) {
      setError(err instanceof Error ? err.message : '上传失败')
    } finally {
      setUploading(false)
    }
  }

  const removeAt = (i: number) => update(list.filter((_, idx) => idx !== i))
  const move = (i: number, dir: -1 | 1) => {
    const j = i + dir
    if (j < 0 || j >= list.length) return
    const next = [...list]
    ;[next[i], next[j]] = [next[j], next[i]]
    update(next)
  }

  return (
    <div>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {list.map((url, i) => (
          <div
            key={`${url}-${i}`}
            className="relative group aspect-[4/3] rounded-xl overflow-hidden bg-surface-alt border border-line"
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={toAbsoluteUrl(url)}
              alt=""
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-ink/0 group-hover:bg-ink/40 transition-colors duration-200 flex items-end justify-between p-2 opacity-0 group-hover:opacity-100">
              <div className="flex gap-1">
                <button
                  type="button"
                  onClick={() => move(i, -1)}
                  disabled={i === 0}
                  className="h-7 w-7 rounded-full bg-white/90 text-ink text-xs disabled:opacity-40 cursor-pointer"
                  title="上移"
                >
                  ←
                </button>
                <button
                  type="button"
                  onClick={() => move(i, 1)}
                  disabled={i === list.length - 1}
                  className="h-7 w-7 rounded-full bg-white/90 text-ink text-xs disabled:opacity-40 cursor-pointer"
                  title="下移"
                >
                  →
                </button>
              </div>
              <button
                type="button"
                onClick={() => removeAt(i)}
                className="h-7 px-3 rounded-full bg-white/90 text-red-600 text-xs cursor-pointer"
              >
                删除
              </button>
            </div>
          </div>
        ))}

        <button
          type="button"
          onClick={() => inputRef.current?.click()}
          disabled={uploading}
          className="aspect-[4/3] rounded-xl border-2 border-dashed border-line bg-surface-alt text-ink-muted text-sm hover:border-ink hover:text-ink transition-colors cursor-pointer disabled:opacity-50 flex flex-col items-center justify-center"
        >
          <div className="text-2xl mb-1">+</div>
          <div>{uploading ? '上传中…' : '添加图片'}</div>
        </button>
      </div>

      <input
        ref={inputRef}
        type="file"
        multiple
        accept="image/jpeg,image/png,image/webp,image/gif"
        onChange={handleFiles}
        className="hidden"
      />

      {error && <div className="mt-2 text-xs text-red-600">{error}</div>}
    </div>
  )
}
