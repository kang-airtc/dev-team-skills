"use client";

import NewsForm from "@/components/NewsForm";

export default function NewNewsPage() {
  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-6">新增新闻</h1>
      <NewsForm />
    </div>
  );
}
