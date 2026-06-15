# Git Helper 输出示例

**用户输入**：帮我提交代码

---

**Agent**：好的，当前有以下改动文件：

```
modified:  components/products/ProductSearchBar.tsx
modified:  services/products.ts
modified:  app/(admin)/products/page.tsx
```

帮你生成了提交信息：

```
feat(products): 新增产品关键词搜索功能
```

确认提交，还是需要修改说明？

---

**用户**：加一句，搜索支持防抖

---

**Agent**：好的，更新为：

```
feat(products): 新增产品关键词搜索功能

搜索输入支持 300ms 防抖，避免频繁请求接口
```

已提交 ✅

---

**Agent**：要推送到远程吗？

---

**用户**：推一下

---

**Agent**：推送成功 ✅

当前分支 `feat/product-search` 已同步到远程。

