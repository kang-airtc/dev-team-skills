# 时序图输入格式

`dev-sequence` 接受一个 Markdown 文件作为输入，包含两个固定章节：`## 角色` 和 `## 消息`。

## 完整示例

```markdown
# 用户登录时序

## 角色
- user: 用户
- frontend: 前端
- backend: 后端
- db: 数据库

## 消息
- user -> frontend: 输入账号密码
- frontend -> backend: POST /api/login
- backend -> db: SELECT user
- db -> backend: 返回用户记录
- backend -> frontend: 返回 JWT token
- frontend -> user: 跳转首页
```

## 语法约定

- **角色 id**：英文/数字/连字符组合，作为消息中的引用
- **角色 label**：冒号后的中文描述，可省（省略时用 id）
- **消息箭头**：必须用 ASCII 的 `->`
- **消息内容**：箭头后冒号 `:` 紧跟，内容会作为箭头标签

## 输出

- 角色：顶部一排矩形，按声明顺序从左到右排列
- 每个角色下方：一条灰色虚线（lifeline），向下延伸到时序结束
- 每条消息：一个水平箭头，从源 lifeline 指向目标 lifeline，标签居中
- 消息按声明顺序自上而下排列，间距 40px

## 边界

- 不支持 `alt` / `loop` / `par` 等控制结构（draw.io 时序图本身支持，本 Skill 当前不生成）
- 不支持自调用（`backend -> backend`）——可以画但视觉上是一根 0 长度箭头，建议拆分成两条
- 复杂时序（消息 > 30）建议拆分多张图后分别生成
