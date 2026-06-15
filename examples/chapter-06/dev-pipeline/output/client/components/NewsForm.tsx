"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createNews, updateNews } from "@/services/news";

interface NewsFormData {
  title: string;
  slug: string;
  summary: string;
  cover_image: string;
  content: string;
  is_published: boolean;
}

interface NewsFormProps {
  defaultValues?: Partial<NewsFormData>;
  newsId?: number;
}

export default function NewsForm({ defaultValues, newsId }: NewsFormProps) {
  const router = useRouter();
  const [form, setForm] = useState<NewsFormData>({
  title: '',
  slug: '',
  summary: '',
  cover_image: '',
  content: '',
  is_published: false,
    ...defaultValues,
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      if (newsId) {
        await updateNews(newsId, form);
      } else {
        await createNews(form);
      }
      router.push("/dashboard/news");
    } catch (err) {
      setError(err instanceof Error ? err.message : "保存失败，请重试");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl space-y-4">
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded text-red-700">
          {error}
        </div>
      )}
      <div>
        <label className="block text-sm font-medium mb-1">title *</label>
        <input type="text" name="title" value={form.title as string} required
          onChange={(e) => setForm({...form, title: e.target.value})}
          className="w-full border rounded px-3 py-2 text-sm" />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">slug *</label>
        <input type="text" name="slug" value={form.slug as string} required
          onChange={(e) => setForm({...form, slug: e.target.value})}
          className="w-full border rounded px-3 py-2 text-sm" />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">summary</label>
        <textarea name="summary" value={form.summary as string}
          onChange={(e) => setForm({...form, summary: e.target.value})}
          className="w-full border rounded px-3 py-2 text-sm" rows={4} />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">cover_image</label>
        <input type="text" name="cover_image" value={form.cover_image as string}
          onChange={(e) => setForm({...form, cover_image: e.target.value})}
          className="w-full border rounded px-3 py-2 text-sm" />
      </div>
      <div>
        <label className="block text-sm font-medium mb-1">content *</label>
        <textarea name="content" value={form.content as string} required
          onChange={(e) => setForm({...form, content: e.target.value})}
          className="w-full border rounded px-3 py-2 text-sm" rows={4} />
      </div>
      <label className="flex items-center gap-2">
        <input type="checkbox" name="is_published"
          checked={form.is_published as boolean}
          onChange={(e) => setForm({...form, is_published: e.target.checked})} />
        <span>is_published</span>
      </label>
      <div className="flex gap-3 pt-2">
        <button type="submit" disabled={submitting}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
          {submitting ? "保存中..." : "保存"}
        </button>
        <button type="button" onClick={() => router.back()}
          className="px-4 py-2 border rounded hover:bg-gray-50">
          取消
        </button>
      </div>
    </form>
  );
}
