# Git Helper 输出示例

**用户输入**：帮我提交代码

---

**Agent**：好的，当前有以下改动文件：

```
modified:  components/products/ProductEditPage.tsx
modified:  server/web/api/comments/views.py
```

帮你生成了提交信息：

```
fix(product): 修复产品编辑页前后端代码规范问题
```

确认提交，还是需要修改说明？

---

**用户**：加一句，前端消除 any、后端换 ApiResponse

---

**Agent**：好的，更新为：

```
fix(product): 修复产品编辑页前后端代码规范问题

前端：消除 any 类型、改用 services 封装、加 try/catch
后端：统一 ApiResponse 响应格式、修复计数查询性能问题
```

已提交 ✅

---

**Agent**：要推送到远程吗？

---

**用户**：推一下，然后帮我写个 PR 描述

---

**Agent**：推送成功 ✅

当前分支 `feat/product-management` 已同步到远程。

PR 描述草稿：

```
## 变更内容
- 前端 ProductEditPage：消除 any 类型，改用 services 层封装 API 调用，
  修复异步操作缺少 try/catch 的问题
- 后端 comments/views：统一响应格式为 ApiResponse，业务错误改用 error code，
  修复全量拉取计数的性能问题，移除 print 调试

## 测试
- 前端：ProductEditPage 手动验证编辑、保存、加载失败三个路径
- 后端：评论接口单元测试通过，计数接口 EXPLAIN 验证走索引

## 不包含
- P2、P3 小项留到下次统一处理
```
