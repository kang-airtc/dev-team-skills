# review-frontend 报告：feature/uploads → main

## P1（必须修）
- `app/dashboard/products/new/page.tsx:42` —— 直接读 `data.id` 未走 `unwrapApi()`

## P2（建议修）
- `components/admin/ImageUploader.tsx:18` —— 命名 `handleClick` → `handleUpload`
- `components/admin/GalleryUploader.tsx:55` —— 回调参数缺类型，命中 `ts-strict`
- `components/admin/GalleryUploader.tsx:120` —— 错误处理仅 alert，未走 `<Toast>` 组件

## P3（可选）
- `components/admin/ImageUploader.tsx:64` —— `<img>` 缺 `alt`
- `components/admin/GalleryUploader.tsx:88` —— 缺加载骨架屏

## 结论：1 P1 阻断合并

## 修复后回归（commit 5f2a...d8）

- P1 已修复：所有响应统一 `unwrapApi<T>(res)`
- P2 已修复
- P3 已部分修复（alt 补全，骨架屏列入下一 Sprint）
- 重跑 review-frontend：0 P1 / 0 P2 / 1 P3 → 通过
