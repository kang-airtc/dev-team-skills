# 前端代码规范

> 适用范围：Next.js（App Router） + TypeScript + TailwindCSS 项目

---

## 1. 文件与目录组织

```
frontend/
├── app/                      # Next.js App Router 路由
│   ├── (admin)/              # 路由组（括号，不影响 URL）
│   │   ├── dashboard/        # 路由段
│   │   │   └── products/
│   │   │       ├── page.tsx  # 列表页
│   │   │       ├── [id]/     # 动态路由（已有资源）
│   │   │       │   └── page.tsx
│   │   │       └── new/      # 新建页
│   │   │           └── page.tsx
│   │   └── layout.tsx        # 路由组布局
│   └── (public)/
│       └── layout.tsx
├── components/               # 共享 UI 组件
│   └── admin/                # 按功能分子目录
├── services/                 # API 服务层（按资源分文件）
├── utils/                    # 纯工具函数
└── styles/                   # 全局样式
```

规则：
- `app/` 下只放路由文件（page.tsx / layout.tsx / loading.tsx / error.tsx）
- 业务 UI 必须提取到 `components/`，不在 page.tsx 里直接写大段 JSX
- 所有 API 调用必须在 `services/` 里，page.tsx / 组件里不出现 httpGet/httpPost

---

## 2. 命名规范

### 2.1 组件命名

- 文件名 **PascalCase**：`UserCard.tsx`、`ProductForm.tsx`
- 文件名必须与默认导出函数名一致
- 一个文件一个主组件；辅助小组件可以在同文件末尾定义但不导出

### 2.2 页面命名（Next.js App Router 约定）

| 文件名 | 作用 |
|--------|------|
| `page.tsx` | 路由页面（唯一） |
| `layout.tsx` | 路由布局（可嵌套） |
| `loading.tsx` | 加载占位 |
| `error.tsx` | 错误边界 |
| `not-found.tsx` | 404 处理 |
| `[slug]/page.tsx` | 动态路由（字符串标识，如文章 slug） |
| `[id]/page.tsx` | 动态路由（数字 ID） |
| `(group)/` | 路由组，括号内名称不影响 URL |

### 2.3 函数命名

| 场景 | 前缀 / 规则 | 示例 |
|------|-------------|------|
| 事件处理 | `handle` 前缀 | `handleSubmit`、`handleDelete` |
| 异步数据获取 | `fetch` / `get` / `load` | `fetchAll`、`getProduct` |
| 删除操作 | `remove` / `delete` | `removeItem`、`deleteProduct` |
| 格式化工具 | 动词 + 名词 | `formatDate`、`toAbsoluteUrl` |
| 判断函数 | `is` / `has` / `can` | `isAdmin`、`hasPermission` |

### 2.4 Hooks 命名

- 自定义 Hook 必须以 **`use`** 开头：`useAuth`、`useProducts`、`useModal`
- Hook 不允许定义在普通函数里，必须是独立的 `function useXxx()` 或 `const useXxx = () =>`

### 2.5 State 命名

- 普通状态：直接用名词：`items`、`loading`、`error`
- boolean 状态：`is` / `has` 前缀：`isLoading`、`isOpen`、`hasError`
- `useState` 解构命名：`[name, setName]`，保持对称

```typescript
// ✅ 正确
const [items, setItems] = useState<Product[]>([])
const [isLoading, setIsLoading] = useState(true)
const [isOpen, setIsOpen] = useState(false)

// ❌ 错误
const [data, setData] = useState([])   // data 太宽泛
const [flag, setFlag] = useState(false) // flag 无语义
```

### 2.6 VO / Model / Type 命名

| 场景 | 后缀约定 | 示例 |
|------|----------|------|
| 接口/响应体（VO） | 直接用业务名，无需加 VO | `Product`、`NewsArticle`、`User` |
| 创建/更新输入体 | `Input` 后缀 | `ProductInput`、`CreateUserInput` |
| 查询参数 | `Params` 后缀 | `ProductListParams`、`NewsQueryParams` |
| 列表响应 | `ListResult` 后缀 | `ProductListResult`、`NewsListResult` |
| 统一 API 响应 | `ApiResponse<T>` | `ApiResponse<Product>` |
| 枚举值 | `PascalCase` | `UserRole`、`OrderStatus` |

```typescript
// ✅ 正确
export interface Product { id: number; name: string }
export interface ProductInput { name: string; price?: number }
export interface ProductListParams { category_id?: number; limit?: number }
export interface ProductListResult { items: Product[]; total: number }

// ❌ 错误
export interface ProductVO { ... }     // 不用 VO 后缀
export interface IProduct { ... }      // 不用 I 前缀
export type ProductDTO = { ... }       // 不用 DTO
```

---

## 3. TypeScript 规范

- 严格模式开启（`tsconfig.json` 中 `"strict": true`）
- **禁止 `any`**，确实必要时加注释 `// @ts-expect-error 原因`
- 函数参数和返回值都要类型标注
- 组件 Props 用 `interface Props` 或 `interface XxxProps` 定义，不用内联对象字面量

```typescript
// ✅ 正确
interface Props {
  product: Product
  variant?: 'default' | 'feature'
}
export default function ProductCard({ product, variant = 'default' }: Props) { ... }

// ❌ 错误
export default function ProductCard({ product }: { product: any }) { ... }
```

---

## 4. API 调用规范

- **禁止**直接调用 `fetch` 或 `axios`
- 必须通过 `utils/request.ts` 导出的工具函数：`httpGet` / `httpPost` / `httpPut` / `httpDelete` / `httpPatch`
- 服务函数统一放在 `services/` 目录，按资源分文件（`products.ts`、`news.ts`、`auth.ts`）
- 服务函数名用「动词 + 名词」：`listProducts`、`getProduct`、`createProduct`、`updateProduct`、`deleteProduct`

```typescript
// ✅ 正确（services/products.ts）
import { httpGet, httpPost } from '@/utils/request'
export const listProducts = (params?: ProductListParams) =>
  httpGet<ProductListResult>('/products', params)

// ❌ 错误（组件或页面里直接调用）
const res = await fetch('/api/products')
const data = await axios.get('/products')
```

---

## 5. 错误码消费

后端响应统一结构：`{ code: number, msg: string, data: T | null }`

| code 范围 | 含义 | 前端处理 |
|-----------|------|----------|
| `0` | 成功 | 取 `data` 继续处理 |
| `1000–1999` | 通用/系统错误（鉴权、参数、网络） | 统一弹 toast 提示 `msg` |
| `2000–2999` | 业务错误 | 按具体码做差异化处理 |
| `1104 / 1105` | Token 过期/无效 | 清 localStorage，跳转 `/login` |

---

## 6. 样式规范（TailwindCSS）

- **禁止**行内 style：`<div style={{ color: 'red' }}>` ❌
- 统一使用 TailwindCSS 工具类
- 颜色、字号、间距必须用设计 token 变量，禁止硬编码：
  - 文字颜色：`text-ink`、`text-ink-muted`
  - 背景：`bg-surface-alt`
  - 边框：`border-line`
  - 不写 `text-[#333]`、`bg-[#f5f5f5]`
- 仅在 TailwindCSS 无法满足时才使用 CSS Module，两者不混用
- 动画/过渡统一用 `transition-*`、`duration-*`、`ease-*` 工具类

---

## 7. import 顺序

```typescript
// 1. 第三方包
import React, { useState, useEffect } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'

// 2. 项目模块（绝对路径，@/ 别名）
import AdminShell from '@/components/admin/AdminShell'
import { httpGet } from '@/utils/request'

// 3. 当前模块的相对路径
import { formatDate } from './utils'
import styles from './page.module.css'
```

每组之间空一行，组内不空行。

---

## 8. 错误处理

- 所有异步操作必须 `try/catch`，不让异常冒泡到全局
- **禁止** `console.log` 记录错误，用 `console.error` 或统一上报
- 用户可见的错误必须有提示（toast / alert / 错误页）
- 删除/破坏性操作必须有二次确认（`confirm` 或 Modal）

---

## 9. 代码组织

- **page.tsx** 只负责布局组织，复杂业务逻辑提取为自定义 Hook 或独立组件
- `'use client'` 只在真正需要客户端交互（事件、useState、useEffect）时添加
- Server Component 和 Client Component 分离清晰，尽量让叶子节点才是 Client Component
- 单个组件不超过 200 行，超出就考虑拆分
