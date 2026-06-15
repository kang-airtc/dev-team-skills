---
name: design-review
description: 读取设计稿截图，按多角色（UI、前端、产品、后端）视角进行设计评审，输出带优先级的评审报告
---

# Design Review - 多角色设计评审

读取设计稿截图（Pencil导出或用户上传），按团队成员的不同专业视角进行评审，输出结构化的评审报告。

## 触发场景

- 设计稿完成后，需要团队评审
- 想从多个专业角度发现设计问题
- 需要带优先级的修改清单
- 设计评审会上需要结构化讨论材料

## 目录结构

```
design-review/
├── SKILL.md
├── scripts/
│   └── design_review.py
└── assets/
    └── review-checklist.md
```

## 依赖

仅使用 Python 标准库，无需额外依赖。

## 使用方法

```bash
# 基础评审（默认所有角色）
python3 .opencode/skills/design-review/scripts/design_review.py \
  --input "login-page.png" \
  --output "review-report.md"

# 指定评审角色
python3 .opencode/skills/design-review/scripts/design_review.py \
  --input "login-page.png" \
  --roles "ui-designer,frontend-dev,product-manager" \
  --output "review-report.md"

# 从Pencil设计文件读取
python3 .opencode/skills/design-review/scripts/design_review.py \
  --pencil "design.pen" \
  --output "review-report.md"
```

参数：
- `--input, -i`：设计稿截图路径
- `--pencil, -p`：Pencil设计文件路径（与--input二选一）
- `--roles, -r`：评审角色列表，逗号分隔，默认全部
- `--output, -o`：输出报告路径，默认 `review-report.md`

## 评审角色

| 角色 | 关注点 | 检查项 |
|------|--------|--------|
| **UI Designer** | 视觉层面 | 色彩规范、字体层级、间距一致性、视觉层次 |
| **Frontend Dev** | 实现层面 | 组件复用性、响应式适配、交互复杂度、状态管理 |
| **Product Manager** | 业务层面 | 信息架构、用户流程、业务目标对齐、文案准确性 |
| **Backend Dev** | 数据层面 | 接口可行性、数据需求、权限设计、性能影响 |

## 输出格式

```markdown
# 设计评审报告：{设计名称}

**评审时间**: {date}
**评审角色**: {roles}

## UI Designer 评审意见

### [P1] 按钮对比度不足
- **位置**: 登录按钮
- **问题**: 当前背景色 #1890FF 在白色背景上对比度 3.2:1，低于 WCAG AA 标准 4.5:1
- **建议**: 加深至 #096DD9 或使用更深的蓝色

### [P2] 输入框缺少焦点状态
- **位置**: 邮箱/密码输入框
- **问题**: 聚焦时无视觉反馈
- **建议**: 添加边框颜色变化或阴影效果

## Frontend Dev 评审意见
...

## 汇总优先级

### P1（必须修改）
- [ ] 按钮对比度不足（UI Designer）
- [ ] ...

### P2（建议修改）
...

### P3（可选优化）
...
```

## 边界

- 本Skill输出的是**评审意见**，不直接修改设计稿
- 基于文本描述进行评审，不实际分析图像像素
- 角色定义从 `AGENTS.md` 和 `agent/*.md` 读取，如不存在则使用默认定义
- 优先级由脚本根据问题严重程度自动判定，可人工调整

## 与其他 Skill 的关系

```
design-pencil ──▶ design-review ──▶ design-ui-check
  设计稿         多角色评审        规范验证
```
