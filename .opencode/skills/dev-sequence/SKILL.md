---
name: dev-sequence
description: 根据消息流描述生成时序图（draw.io 格式 .drawio 文件），用于接口调用流程、登录流程、支付链路等场景
---

# Dev Sequence - 时序图生成

读取一段"角色 → 消息"格式的描述，生成 `.drawio` 格式的时序图。

## 触发场景

- 设计接口调用流程（如 OAuth 登录、支付链路）需要可视化时序
- 排查跨服务调用的顺序问题，画出现状再讨论
- 写技术方案时附时序图，让 Reviewer 一眼看懂请求路径

## 目录结构

```
dev-sequence/
├── SKILL.md
├── scripts/
│   └── generate.py
└── references/
    └── sequence-syntax.md     # 输入语法说明
```

## 依赖

仅使用 Python 标准库。

## 使用方法

```bash
python3 .opencode/skills/dev-sequence/scripts/generate.py \
  --input login-flow.md \
  --output login-flow.drawio
```

参数：
- `--input, -i`：消息流描述文件
- `--output, -o`：输出 `.drawio` 路径

## 输入格式

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
- backend -> db: 查询用户
- db -> backend: 返回用户记录
- backend -> frontend: 返回 JWT token
- frontend -> user: 跳转首页
```

## 输出格式

draw.io 标准时序图：每个角色一个 lifeline，消息箭头按声明顺序自上而下排列，自动编号。

## 边界

- 不支持 `alt` / `loop` / `par` 等控制结构（draw.io 时序图本身支持，但本 Skill 当前版本不生成）
- 不支持自动布局微调，复杂时序图（消息 > 30 条）建议拆分
