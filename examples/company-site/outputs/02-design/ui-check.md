# UI 规范扫描报告

> 来源 Skill：`design-ui-check`  
> 输入：公开站现有页面（首页 / 产品列表 / 产品详情 / 新闻列表）  
> 规范：`references/ui-standard.md`

## 总体结论

12 处违规，其中 P1 = 3 / P2 = 6 / P3 = 3。需在开发阶段开工前修复 P1。

## 按维度

### 颜色

| 行号 | 级别 | 文件 | 问题 |
|---|---|---|---|
| 18 | P1 | `app/(public)/page.tsx` | 主按钮使用 `#3B82F6`，规范要求 `var(--brand-primary)` |
| 42 | P2 | `app/(public)/products/page.tsx` | 标签背景写死 `#F3F4F6`，应改 Tailwind token |

### 字体

| 行号 | 级别 | 文件 | 问题 |
|---|---|---|---|
| 25 | P1 | `app/(public)/news/[slug]/page.tsx` | 正文 `font-size: 14px`，规范要求正文最小 16px |
| 60 | P2 | `components/Footer.tsx` | 字重 400，规范要求次要信息 500 |

### 间距

| 行号 | 级别 | 文件 | 问题 |
|---|---|---|---|
| 12 | P1 | `app/(public)/products/[slug]/page.tsx` | 容器 padding 直接写 `px-7`，违反 4 的倍数约定 |
| 35 | P3 | `components/Hero.tsx` | section 间距 `mt-12`，建议 `mt-16` 与设计稿对齐 |

### 圆角

| 行号 | 级别 | 文件 | 问题 |
|---|---|---|---|
| 8  | P2 | `components/ProductCard.tsx` | 卡片 `rounded-md`，规范要求 `rounded-lg` |
| 14 | P2 | `components/admin/ImageUploader.tsx` | 上传按钮无圆角 |

## 整改建议

- 把 P1 三处违规列入开发阶段 Sprint 1 的子任务
- 提取 Tailwind preset 把品牌色、间距、圆角集中收口，避免硬编码
