# 前端代码审查报告

**审查文件**：`components/products/ProductEditPage.tsx`
**对照规范**：`references/frontend-standard.md`
**违规总数**：9 处（P1×5 / P2×2 / P3×2）

---

## 🔴 P1 必须修复（5 处）

### 1. 直接使用 `axios`，未经统一封装
**位置**：第 3、12、21 行

```tsx
// ❌ 违规
import axios from 'axios'
axios.get(`/api/products/${params.id}`)
axios.put(`/api/products/${params.id}`, data)
```

规范 §4：禁止直接调用 `axios`，必须通过 `services/` 层封装。

```tsx
// ✅ 修复
import { getProduct, updateProduct } from '@/services/products'

const product = await getProduct(Number(params.id))
await updateProduct(Number(params.id), formData)
```

---

### 2. Props 使用内联 `any` 类型
**位置**：第 7 行

```tsx
// ❌ 违规
export default function ProductEditPage({ params }: { params: any }) {
```

规范 §3：组件 Props 用 `interface` 单独定义，禁止 `any`。

```tsx
// ✅ 修复
interface Props {
  params: { id: string }
}
export default function ProductEditPage({ params }: Props) {
```

---

### 3. `as any` 强制类型转换
**位置**：第 31、32 行

```tsx
// ❌ 违规
value={(data as any)?.name || ''}
onChange={(e) => setData({ ...(data as any), name: e.target.value })}
```

规范 §3：禁止 `any`，`useState` 应声明明确类型。

```tsx
// ✅ 修复
const [product, setProduct] = useState<Product | null>(null)

value={product?.name || ''}
onChange={(e) => setProduct((prev) => prev ? { ...prev, name: e.target.value } : prev)}
```

---

### 4. 行内 `style` + 硬编码颜色值
**位置**：第 28、34 行

```tsx
// ❌ 违规
<div style={{ padding: '24px', background: '#f5f5f5' }}>
<button onClick={save} style={{ color: '#fff', background: '#333' }}>
```

规范 §6：禁止行内 `style`，颜色用设计 token，统一用 TailwindCSS。

```tsx
// ✅ 修复
<div className="p-6 bg-surface-alt">
<button onClick={handleSave} className="text-white bg-ink hover:bg-neutral-800">
```

---

### 5. 异步操作缺少 `try/catch`
**位置**：第 19–24 行

```tsx
// ❌ 违规
const save = async () => {
  setFlag(true)
  axios.put(`/api/products/${params.id}`, data).then(() => {
    alert('保存成功')
  })
  // 没有 .catch，保存失败时用户无任何提示
}
```

规范 §8：所有异步操作必须 `try/catch`，错误必须有用户可见的提示。

```tsx
// ✅ 修复
const handleSave = async () => {
  setIsSaving(true)
  try {
    await updateProduct(Number(params.id), formData)
    alert('保存成功')
  } catch (err) {
    console.error('保存失败', err)
    alert(err instanceof Error ? err.message : '保存失败')
  } finally {
    setIsSaving(false)
  }
}
```

---

## 🟡 P2 建议修复（2 处）

### 6. State 命名无语义
**位置**：第 8、9 行

```tsx
// ❌ 违规
const [data, setData] = useState(null)   // data 太宽泛
const [flag, setFlag] = useState(false)  // flag 完全无语义
```

规范 §2.5：普通 state 用业务名词，boolean state 加 `is` / `has` 前缀。

```tsx
// ✅ 修复
const [product, setProduct] = useState<Product | null>(null)
const [isSaving, setIsSaving] = useState(false)
```

---

### 7. 错误日志用 `console.log`
**位置**：第 15 行

```tsx
// ❌ 违规
console.log('加载失败', err)
```

规范 §8：错误日志必须用 `console.error`，且需要更新状态给用户提示。

```tsx
// ✅ 修复
console.error('加载产品失败', err)
setError(err instanceof Error ? err.message : '加载失败')
```

---

## 🟢 P3 小改进（2 处）

### 8. 事件处理函数缺少 `handle` 前缀
**位置**：第 19 行

```tsx
// ❌ 违规
const save = async () => { ... }
<button onClick={save}>

// ✅ 修复
const handleSave = async () => { ... }
<button onClick={handleSave}>
```

---

### 9. import 分组缺少空行
**位置**：第 3–5 行

```tsx
// ❌ 违规（三方包和项目模块之间没有空行）
import axios from 'axios'
import { useState, useEffect } from 'react'
import AdminShell from '@/components/admin/AdminShell'

// ✅ 修复（修完 axios 问题后，剩余 import 正确分组）
import { useState, useEffect } from 'react'

import AdminShell from '@/components/admin/AdminShell'
import { getProduct, updateProduct } from '@/services/products'
import type { Product } from '@/services/products'
```

---

## 汇总

| 级别 | 数量 | 主要问题 |
|------|------|----------|
| 🔴 P1 必须修复 | 5 | 直接用 axios、Props any、as any、行内 style、缺 try/catch |
| 🟡 P2 建议修复 | 2 | State 命名无语义、console.log |
| 🟢 P3 小改进 | 2 | 函数名缺 handle 前缀、import 分组 |

**结论**：P1 全部修复后方可提交。
