---
name: design-pencil
description: 通过 Pencil MCP 连接 Pencil.dev，用自然语言描述界面需求，在画布上生成低保真设计稿（.pen 文件）
---

# Design Pencil - AI 原生设计稿生成

借助 Pencil.dev 的 MCP 接口，用自然语言描述设计需求，直接在 Pencil 画布上生成低保真原型。设计稿以 `.pen` 格式保存（JSON 结构，天然支持 git 管理）。

## 触发场景

- 需要快速制作线框图或低保真原型
- 设计评审前快速产出概念稿
- 设计冲刺中快速制作故事板

## 前提条件

1. Pencil.dev（VS Code 扩展）已安装并在 VS Code 中处于运行状态
2. `~/.config/opencode/opencode.json` 中 `pencil` MCP 条目 `enabled: true`
3. 已在 Pencil 中打开目标 `.pen` 文件（或准备新建）

## 调用方式

直接用自然语言描述设计需求：

```
/design-pencil 为公司站点的联系留言页设计低保真线框图，包含姓名、联系方式、留言内容三个输入字段和提交按钮
```

## 执行步骤

### 步骤 0：建立设计系统（新项目时可选）

**何时需要**：新项目尚无 design token 时，在画页面前先建立设计系统。已有 token 和组件库则跳过此步骤。

**第一步：写入 design token**

用 `set_variables` 把颜色、字号、间距等核心数值写入 `.pen` 文件的变量表：

```
set_variables({
  variables: {
    "primary-600": { "type": "color", "value": "#4F46E5" },
    "neutral-100": { "type": "color", "value": "#F5F5F5" },
    "neutral-900": { "type": "color", "value": "#171717" },
    "font-size-base": { "type": "number", "value": 16 },
    "spacing-4": { "type": "number", "value": 4 },
    "radius-base": { "type": "number", "value": 8 }
  }
})
```

token 写入后，后续所有组件和页面通过变量名引用（如 `$primary-600`），不硬编码色值。

**第二步：生成组件库**

用 `batch_design`（`reusable: true`）创建可复用组件：

```
batch_design({
  operations: "
    btn=I('canvas', { type: 'frame', name: 'primary-button', reusable: true, ... })
    input=I('canvas', { type: 'frame', name: 'input-text', reusable: true, ... })
  "
})
```

组件用 `reusable: true` 标记，之后用 `ref` 类型实例化，实例可通过 `descendants` 覆盖部分属性。

**完成后**：后续步骤直接引用变量（`$primary-600`）和组件（`ref` 类型），不再重复写数值。

### 步骤 1：检查编辑器状态

```
get_editor_state({ include_schema: true })
```

- 确认 Pencil 已连接、当前打开了目标 `.pen` 文件
- `include_schema: true` 在**首次调用时必须传**，让 AI 理解 .pen 文件结构
- 如需打开特定文件：`open_document({ filePath: "/绝对路径/design.pen" })`

### 步骤 2：获取设计规范（可选但推荐）

```
get_guidelines()                               # 列出所有可用规范
get_guidelines({ category: "xxx", name: "yyy" })  # 加载特定规范
```

Designer agent 不会自动继承规范，若后续要 spawn_agents，需在每个 agent 的 prompt 里显式带上规范名称。

### 步骤 3：生成设计

**方案 A — 简单设计（单页/局部）**，直接调用 `batch_design`：

```
batch_design({
  operations: "..."   // AI 根据需求自行生成操作序列
})
```

`batch_design` 支持的操作类型：`insert`、`copy`、`update`、`replace`、`move`、`delete`、`image`。
每次调用**最多 25 条操作**，超出则拆成多次调用（先做整体结构，再填充内容）。

**方案 B — 复杂设计（多屏/多区块）**，用 `spawn_agents` 并行拆分任务：

先用 `batch_design` 创建各区块的占位 frame，再分配给 agent 并行工作：

```
spawn_agents({
  config: [
    { prompt: "设计顶部导航栏，风格简洁商务，参考 Mobile App 规范", nodeIds: ["frame-header"] },
    { prompt: "设计留言表单区域：姓名、联系方式、留言内容字段 + 提交按钮，参考 Mobile App 规范", nodeIds: ["frame-form"] }
  ]
})
```

> Designer agent 会自动读取文档中的 design variables，**prompt 中不需要写颜色值、间距数值或变量名**，只描述视觉意图即可。

### 步骤 4：验证并修正

```
get_screenshot({ nodeId: "目标-frame-id" })
```

分析截图确认布局正确。若有偏差，重新调用 `batch_design` 修正，循环直到满意。

### 步骤 5：输出报告

调用脚本记录本次生成结果：

```bash
python3 .opencode/skills/design-pencil/scripts/record_output.py \
  --file "design-output/company-site-design.pen" \
  --pages "留言页" \
  --notes "低保真，待评审"
```

## 注意事项

- `.pen` 文件**只能通过 Pencil MCP 工具访问**，禁止用 `Read` / `Grep` 直接读取
- `batch_design` 失败时会返回验证错误列表，根据提示修正后重新调用
- `spawn_agents` 总是少创建一个 agent（当前 session 自己完成最后一项任务）
- 如果画布空间不足，先调用 `find_empty_space_on_canvas` 找可用区域

## 输出产物

| 产物 | 说明 |
|------|------|
| `design-output/xxx.pen` | Pencil 自动保存的设计文件（git 友好） |
| `design-output/xxx-design.md` | 本次生成的摘要报告 |

## 与其他 Skill 的关系

```
design-pencil ──▶ design-review
  生成设计稿      多角色评审
```
