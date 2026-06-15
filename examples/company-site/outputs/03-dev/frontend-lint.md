# 前端规范扫描报告

> 来源 Skill：`review-frontend`（本地自查模式）  
> 输入：`frontend/components/` 与 `frontend/app/`  
> 规范：`references/frontend-standard.md`

## 总结：7 处违规（1 P1 / 4 P2 / 2 P3）

| 文件:行 | 级别 | 规则 | 说明 |
|---|---|---|---|
| `app/dashboard/products/new/page.tsx:42` | P1 | api-response-unwrap | 直接读 `data.id` 未走 `unwrapApi()`，未来响应格式变更会全站炸 |
| `components/admin/ImageUploader.tsx:18` | P2 | naming | `handleClick` 应为 `handleUpload`，语义更准 |
| `components/admin/GalleryUploader.tsx:55` | P2 | ts-strict | 隐式 `any`，回调参数缺类型 |
| `components/Footer.tsx:8` | P2 | tailwind-token | 颜色硬编码 `#666`，应用 token |
| `app/(public)/products/page.tsx:60` | P2 | error-code | 仅展示 `msg`，未根据 `code` 区分文案 |
| `components/ProductCard.tsx:14` | P3 | a11y | `<img>` 缺 `alt` |
| `app/(public)/news/[slug]/page.tsx:30` | P3 | seo | 缺 `<title>` meta |

## 修复指引

- 所有 `fetch` 响应统一走 `unwrapApi<T>(res)` 工具函数，封装在 `lib/api.ts`
- Tailwind 颜色统一在 `tailwind.config.ts` 的 `theme.extend.colors` 中声明 brand token
- 列表错误处理统一走 `ErrorBoundary` + `code -> 文案` 映射表
