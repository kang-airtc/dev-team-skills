# 前端代码规范

## 1. 组件命名

- 文件名：PascalCase（`UserCard.tsx`、`PostList.tsx`）
- 文件名必须与默认导出一致
- 一个文件一个组件，避免一个文件多个导出组件

## 2. API 调用统一封装

禁止直接调用 `fetch` 或 `axios`，必须经过 `src/lib/api.ts` 统一封装：

```typescript
// ❌ 错误
const res = await fetch('/api/posts');
const data = await res.json();

// ✅ 正确
import { api } from '@/lib/api';
const data = await api.get('/posts');
```

`api` 封装内部统一处理：base URL、token 注入、错误码映射、超时重试。

## 3. 错误码消费

后端响应是统一的 `{code, msg, data}` 三字段结构（详见后端 `error-codes.md`）。前端必须按错误码段做差异化处理：

```typescript
const result = await api.post('/login', { username, password });

if (result.code === 0) {
  // 成功路径
  return result.data;
}

if (result.code >= 1000 && result.code < 2000) {
  // 通用错误：网络/鉴权/参数类，统一弹 toast
  toast.error(result.msg);
} else if (result.code >= 2000 && result.code < 3000) {
  // 业务错误：根据具体码做差异化处理
  if (result.code === 2003) {
    redirectTo('/account-banned');
  } else {
    toast.error(result.msg);
  }
}
```

## 4. 样式规范

- 禁止行内 style（`<div style={{ ... }}>`）
- 统一用 Tailwind CSS 或 CSS Module
- 颜色、字号、间距必须用设计变量，禁止硬编码

## 5. import 顺序

```typescript
// 1. 第三方包
import React from 'react';
import { useRouter } from 'next/navigation';

// 2. 项目模块（绝对路径）
import { api } from '@/lib/api';
import { Button } from '@/components/Button';

// 3. 相对路径
import { formatDate } from './utils';
```

## 6. TypeScript

- 严格模式开启（`"strict": true`）
- 禁止 `any`，确实必要时加注释 `// @ts-expect-error 原因`
- 函数参数和返回值都要类型标注

## 7. 错误处理

- 异步操作必须 try/catch，不要让异常冒泡到全局
- 网络错误必须有用户可见的提示（toast / 错误页）
- 不要 `console.log` 错误，用 `console.error` 或上报系统
