---
name: git-helper
description: Git 日常助手——帮你提交代码、生成提交信息、管理分支、检查提交规范、起草 PR 描述
---

# Git Helper - Git 日常助手

理解你的自然语言意图，执行 Git 操作或给出建议：生成规范的 commit message、检查分支命名、起草 PR 描述、梳理提交历史。

**不替代 review-frontend / review-backend，不做代码质量检查。**

---

## 触发场景

用自然语言说即可，例如：

**提交代码**
- 帮我提交代码
- 帮我写一下提交信息
- 提交了，加了个搜索功能

**推送代码**
- 帮我推送到远程
- push 一下
- 同步到远端

**合并分支**
- 把 feat/product-search 合并到 main
- 合并代码
- 合一下

**分支切换**
- 切到 main 分支
- 切换到开发分支
- 我要去改个 bug，先切到 fix 分支

**暂存与恢复**
- 暂存一下当前代码，我要切分支
- 把暂存恢复回来
- 看一下暂存列表

**新建 / 删除分支**
- 帮我新建一个 feat/order-export 分支
- 创建一个 fix 分支
- 删除 feat/old-feature 分支

**撤销提交**
- 撤销上次提交
- 回退到上个版本

**检查分支规范**
- 看看这个分支名规不规范
- 检查一下分支命名

**起草 PR 描述**
- 我要发 PR，帮我写个描述
- 帮我整理一下这次的改动

**查看提交历史**
- 帮我看看最近几次提交
- 最近改了什么

---

## 目录结构

```
git-helper/
└── SKILL.md
```

---

## 依赖

无外部依赖。调用 `git` 命令读取仓库状态，AI 直接生成内容。

---

## 使用方法

### 场景一：生成 commit message

```
帮我写提交信息
```

Agent 执行 `git diff --staged`，根据改动内容自动生成符合 Conventional Commits 规范的提交信息，供你确认后执行 `git commit`。

### 场景二：提交代码

```
帮我提交代码，我加了一个产品搜索功能
```

Agent 生成提交信息，确认后执行：

```bash
git add .
git commit -m "feat(products): 新增产品关键词搜索功能"
```

### 场景三：推送代码

```
帮我推送到远程
推送一下
```

Agent 执行 `git branch --show-current` 确认当前分支，然后执行：

```bash
git push origin feat/product-search
```

若远程不存在该分支，提示加 `-u` 参数建立跟踪。

### 场景四：合并分支

```
把 feat/product-search 合并到 main
合并代码
```

Agent 自动流程：
1. 确认源分支和目标分支
2. 切换到目标分支，拉取最新代码（`git pull`）
3. 执行 `git merge`
4. 若有冲突，列出冲突文件并引导解决

### 场景五：分支切换

```
切到 main 分支
切换到开发分支
```

Agent 先检查是否有未提交改动：
- 有改动 → 询问：暂存（stash）/ 先提交 / 放弃修改
- 无改动 → 直接执行 `git checkout <branch>`

### 场景六：暂存与恢复

```
暂存一下当前代码，我要去改个 bug
把暂存恢复回来
```

Agent 支持：`stash save` / `stash list` / `stash pop` / `stash drop`

### 场景七：新建 / 删除分支

```
帮我新建一个 feat/order-export 分支
删除 feat/old-feature 分支
```

新建时自动校验命名规范，不合规则先给建议再执行。删除前确认是否已合并。

### 场景八：检查分支规范

```
帮我看看现在的分支名规不规范
```

Agent 执行 `git branch --show-current`，对照规范给出判断和建议。

### 场景九：起草 PR 描述

```
我要发 PR，帮我写个描述
```

Agent 执行 `git log main..HEAD --oneline` 梳理改动，生成 PR 标题 + 描述草稿。

### 场景十：查看提交历史

```
帮我看看最近几次提交
```

Agent 执行 `git log --oneline -10`，用可读格式展示提交摘要。

### 场景十一：撤销提交

```
撤销上次提交
回退到上个版本
```

Agent 区分两种场景：
- 只撤销提交保留改动：`git reset --soft HEAD~1`
- 完全回退丢弃改动：`git reset --hard HEAD~1`（执行前二次确认）

---

## 规范说明

### Commit Message 规范（Conventional Commits）

```
<type>(<scope>): <subject>

[body - 可选]
[footer - 可选]
```

**type 对照表：**

| type | 场景 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `refactor` | 重构（不改行为） |
| `style` | 格式调整（不影响逻辑） |
| `docs` | 文档更新 |
| `test` | 测试相关 |
| `chore` | 构建/依赖/工具配置 |
| `perf` | 性能优化 |
| `revert` | 回滚提交 |

**subject 规则：**
- 动词开头，中文或英文均可，但一次提交只用一种语言
- 不超过 72 个字符
- 末尾不加句号

**示例：**
```
feat(auth): 新增手机号验证码登录
fix(products): 修复搜索结果为空时的空指针异常
refactor(order): 拆分 OrderService，提取支付逻辑到 PaymentService
```

### 分支命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 功能分支 | `feat/描述` | `feat/product-search` |
| 修复分支 | `fix/描述` | `fix/login-token-expired` |
| 重构分支 | `refactor/描述` | `refactor/order-service` |
| 发布分支 | `release/版本号` | `release/v1.2.0` |
| 热修复 | `hotfix/描述` | `hotfix/payment-crash` |

**禁止：** `dev`、`test`、`my-branch`、`temp`、`ksj-0502` 等无语义名称。

### PR 描述模板

```markdown
## 改动说明

简述本次 PR 做了什么、为什么这样做。

## 改动内容

- 新增 / 修改 / 删除了哪些功能
- 涉及哪些文件或模块

## 测试说明

如何验证这次改动正确？

## 注意事项（可选）

部署依赖、数据库迁移、配置变更等需要特别说明的事项。
```

---

## 输出格式

根据场景输出不同内容：

**生成 commit message 时：**

```markdown
## 建议的提交信息

```
feat(products): 新增产品关键词搜索功能

- 支持按名称、描述模糊搜索
- 搜索结果按相关度排序
- 空关键词时展示全部产品
```

确认后执行：
```bash
git add .
git commit -m "feat(products): 新增产品关键词搜索功能"
```
```

**检查分支名时：**

```markdown
## 分支检查结果

当前分支：`ksj-search-0502`

❌ 不规范：使用了个人名称缩写 + 日期，无法从名称判断改动类型和内容。

✅ 建议改为：`feat/product-search`

重命名命令：
```bash
git branch -m ksj-search-0502 feat/product-search
```
```

**起草 PR 描述时：**

```markdown
## PR 描述草稿

**标题**：feat(products): 新增产品搜索与筛选功能

---

## 改动说明

为满足运营人员快速查找产品的需求，新增关键词搜索和分类筛选功能。

## 改动内容

- 新增 `ProductSearchBar` 组件，支持关键词实时搜索
- 新增 `listProductsFiltered` 服务函数，对接后端搜索接口
- 修改产品列表页，集成搜索栏和筛选面板
- 新增 `Product` 类型的 `category` 字段

## 测试说明

1. 打开产品列表页，在搜索框输入关键词，验证列表实时更新
2. 切换分类筛选，验证结果正确过滤
3. 搜索框留空，验证展示全部产品

## 注意事项

后端需同步部署，搜索接口 `GET /api/products?q=&category=` 已在 staging 验证。
```

---

## 边界

- `git reset --hard` 等破坏性操作执行前必须二次确认
- `git push --force` 不执行，只告知命令让用户手动操作
- 不做代码质量检查，那是 `review-frontend` / `review-backend` 的工作
