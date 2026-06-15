"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import NewsForm from "@/components/NewsForm";
import { getNewsById } from "@/services/news";

export default function EditNewsPage() {
  const { id } = useParams<{ id: string }>();
  const [defaultValues, setDefaultValues] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    getNewsById(Number(id)).then((res) => {
      setDefaultValues(res.data);
    });
  }, [id]);

  if (!defaultValues) return <p className="p-8 text-gray-500">加载中...</p>;

  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-6">编辑新闻</h1>
      <NewsForm defaultValues={defaultValues} newsId={Number(id)} />
    </div>
  );
}
