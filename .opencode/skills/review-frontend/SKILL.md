---
name: review-frontend
description: 检查前端新增代码是否符合团队规范——命名约定、TypeScript、API 封装、错误码消费、TailwindCSS 样式、import 顺序、代码组织等
---

# Review Frontend - 前端代码审查

读取当前 Git 差异（`git diff`）或指定的前端目录，对照 `references/frontend-standard.md` 中的项目规范，逐条核查新增代码，输出分级违规清单和修复建议。

**只扫 diff 的加号行，不追究历史存量问题。**

---

## 触发场景

用自然语言说即可，例如：

- 帮我检查一下前端代码
- 我刚写完产品列表功能，review 一下
- 提交前帮我跑个前端审查
- 看看这些改动有没有不符合规范的地方

---

## 目录结构

```
review-frontend/
├── SKILL.md
└── references/
    └── frontend-standard.md     # 项目前端规范（命名、样式、API、TypeScript 等）
```

---

## 依赖

无外部依赖。读取 `git diff` 输出或目录文件，AI 直接分析。

---

## 使用方法

### 方式一：检查当前 staged/unstaged 改动（推荐）

```
帮我 review 一下前端改动
```

Agent 会自动执行 `git diff HEAD`，只分析新增的 `.tsx` / `.ts` 文件。

### 方式二：检查某个具体文件或目录

```
review 一下 components/admin/ProductForm.tsx
帮我看看 services/ 目录的写法对不对
```

### 方式三：命令行扫描模式

```bash
git diff HEAD -- '*.tsx' '*.ts' | grep '^+' \
  | python3 .opencode/skills/review-frontend/scripts/lint.py
```

---

## 检查项

按照 `references/frontend-standard.md` 逐条核查，分以下九个维度：

### 1. 文件与目录组织

- `app/` 下只放路由文件（`page.tsx` / `layout.tsx` / `loading.tsx` / `error.tsx`）
- 业务 UI 组件必须放在 `components/`，不在 `page.tsx` 里写大段 JSX
- API 调用逻辑必须在 `services/` 里，不在组件/页面里直接调 `httpGet` / `httpPost`

### 2. 命名规范

**组件：**
- 文件名 PascalCase，与默认导出函数名一致（`ProductCard.tsx` → `export default function ProductCard`）
- 一个文件一个主组件

**页面（Next.js App Router）：**
- 路由页面必须用 `page.tsx`
- 动态路由用 `[id]` 或 `[slug]`，路由组用括号 `(admin)`

**函数：**
- 事件处理函数：`handle` 前缀（`handleSubmit`、`handleDelete`）
- 异步获取：`fetch` / `get` / `load` 前缀（`fetchAll`、`getProduct`）
- 判断函数：`is` / `has` / `can` 前缀

**Hooks：**
- 自定义 Hook 必须以 `use` 开头（`useAuth`、`useProducts`）
- 不允许把 Hook 逻辑写在普通函数里

**State：**
- boolean state：`is` / `has` 前缀（`isLoading`、`isOpen`、`hasError`）
- `useState` 解构：`[name, setName]` 对称命名，避免 `data`、`flag` 等无语义名

**VO / Model / Type：**

| 场景 | 约定 | 示例 |
|------|------|------|
| 接口/响应体 | 直接用业务名，不加 VO/DTO/I 前缀 | `Product`、`NewsArticle` |
| 创建/更新输入 | `Input` 后缀 | `ProductInput` |
| 查询参数 | `Params` 后缀 | `ProductListParams` |
| 列表响应 | `ListResult` 后缀 | `ProductListResult` |
| 枚举 | PascalCase | `UserRole`、`OrderStatus` |

### 3. TypeScript 规范

- `tsconfig.json` 中 `"strict": true`
- 禁止 `any`，必要时加 `// @ts-expect-error 原因`
- 函数参数和返回值必须有类型标注
- 组件 Props 用 `interface Props` 或 `interface XxxProps`，不用内联 `{ foo: string }` 传参

### 4. API 调用规范

- 禁止直接调用 `fetch` 或 `axios`
- 必须通过 `utils/request.ts` 的封装函数：`httpGet` / `httpPost` / `httpPut` / `httpDelete` / `httpPatch`
- 服务函数放在 `services/`，函数名用「动词 + 名词」：`listProducts`、`createProduct`

### 5. 错误码消费

- 后端响应统一 `{ code, msg, data }`
- `code === 0`：成功，取 `data`
- `1000–1999`：通用错误，弹 toast 提示 `msg`
- `2000–2999`：业务错误，按具体码差异化处理
- `1104 / 1105`：Token 过期，清 localStorage，跳转 `/login`

### 6. 样式规范（TailwindCSS）

- 禁止行内 `style`（`<div style={{ ... }}>`）
- 统一用 TailwindCSS 工具类
- 颜色/字号/间距用设计 token：`text-ink`、`text-ink-muted`、`bg-surface-alt`、`border-line`，不硬编码颜色值
- 只在 Tailwind 无法满足时才用 CSS Module，两者不混用

### 7. import 顺序

```
第三方包（react、next）
↓ 空行
项目绝对路径（@/components、@/utils）
↓ 空行
相对路径（./utils、../types）
```

### 8. 错误处理

- 异步操作必须 `try/catch`，不让异常冒泡
- 禁止 `console.log` 记录错误，用 `console.error`
- 用户可见错误必须有提示（toast / alert / 错误页）
- 删除等破坏性操作需二次确认

### 9. 代码组织

- `page.tsx` 只做布局，复杂逻辑提取为自定义 Hook 或独立组件
- `'use client'` 只在需要事件/useState/useEffect 时加
- Server Component 和 Client Component 明确分离
- 单个组件不超过 200 行

---

## 输出格式

```markdown
# 前端代码审查报告

**扫描范围**：git diff HEAD（新增行）
**违规总数**：N 处

## 🔴 P1 必须修复

- `components/admin/ProductForm.tsx:58`
  直接调用 `axios.post('/products', data)`，必须改用 `httpPost`
  ```ts
  // 修复
  import { httpPost } from '@/utils/request'
  await httpPost<Product>('/products', data)
  ```

## 🟡 P2 建议修复

- `app/(admin)/dashboard/products/page.tsx:12`
  State 命名 `const [data, setData]` 语义不清，建议改为 `[items, setItems]`

## 🟢 P3 小改进

- `services/news.ts:3`
  import 顺序有误：`@/utils/request` 应在第三方包之后、相对路径之前
```

---

## 边界

- 只检查 `.tsx` 和 `.ts` 文件，不处理 `.css` / `.json` / 配置文件
- 只看 diff 加号行，不追究历史代码
- 不替代 ESLint，ESLint 能查的不重复报
- 规范文档在 `references/frontend-standard.md`，修改规范后即时生效
