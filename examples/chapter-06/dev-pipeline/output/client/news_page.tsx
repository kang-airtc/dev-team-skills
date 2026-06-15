"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { listNews } from "@/services/news";
import { Container } from "@/components/Container";
import type { NewsItem } from "@/services/news";

export default function NewsPage() {
  const [items, setItems] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listNews({ limit: 10, offset: 0 })
      .then((res) => {
        setItems(res.data.items);
      })
      .catch((err) => {
        setError(err?.message ?? "加载失败");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <Container>
      <h1 className="text-3xl font-bold mb-8">公司新闻</h1>

      {/* loading 骨架屏 */}
      {loading && (
        <div className="space-y-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="h-32 bg-gray-100 rounded-lg animate-pulse" />
          ))}
        </div>
      )}

      {/* 错误状态 */}
      {error && (
        <p className="text-red-500 text-center py-8">{error}</p>
      )}

      {/* 空状态 */}
      {!loading && !error && items.length === 0 && (
        <p className="text-gray-500 text-center py-16">暂无新闻</p>
      )}

      {/* 列表 */}
      {!loading && !error && items.length > 0 && (
        <div className="space-y-6">
          {items.map((item) => (
            <Link key={item.id} href={`/news/${item.slug}`} className="block">
          {/* TODO: 卡片内容 */}
        </Link>
          ))}
        </div>
      )}
    </Container>
  );
}
