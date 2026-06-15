---
name: design-ui-check
description: 检查设计稿是否符合设计系统规范，包括颜色、字体、间距、圆角等
---

# Design UI Check - UI 规范检查

对比设计稿与设计系统规范，自动检查颜色、字体、间距、圆角等是否符合规范要求。

## 触发场景

- 设计稿完成后，需要验证是否符合设计系统
- 设计评审时快速发现规范偏差
- 多设计师协作时保持设计一致性
- 设计系统更新后检查存量设计

## 目录结构

```
design-ui-check/
├── SKILL.md
├── scripts/
│   └── ui_check.py
└── assets/
    └── default-design-system.md
```

## 依赖

仅使用 Python 标准库，无需额外依赖。

## 使用方法

```bash
# 使用默认设计系统规范检查
python3 .opencode/skills/design-ui-check/scripts/ui_check.py \
  --input "design.pen" \
  --output "ui-check-report.md"

# 使用自定义设计系统
python3 .opencode/skills/design-ui-check/scripts/ui_check.py \
  --input "design.pen" \
  --design-system "my-design-system.md" \
  --output "ui-check-report.md"
```

参数：
- `--input, -i`：设计稿文件路径（Pencil文件或描述文件）
- `--design-system, -s`：设计系统规范文件路径（可选）
- `--output, -o`：输出报告路径，默认 `ui-check-report.md`

## 检查项

| 检查维度 | 检查内容 | 严重程度 |
|---------|---------|---------|
| **颜色** | 是否使用设计系统定义的颜色值 | P1 |
| **字体大小** | 是否按标准阶梯使用（12/14/16/20/24/32） | P1 |
| **行高** | 是否在 1.5-1.8 倍范围内 | P2 |
| **间距** | 是否为 4px/8px 的倍数 | P2 |
| **圆角** | 是否使用标准圆角值（0/4/8/16） | P3 |
| **阴影** | 是否使用标准阴影层级 | P3 |

## 设计系统规范格式

默认从 `assets/default-design-system.md` 读取，或用户自定义：

```markdown
# 设计系统规范

## 颜色
- primary: #1890FF
- success: #52C41A
- warning: #FAAD14
- error: #F5222D
- text-primary: #262626
- text-secondary: #595959
- text-hint: #8C8C8C
- border: #D9D9D9
- background: #F5F5F5

## 字体大小
- xs: 12px
- sm: 14px
- base: 16px
- lg: 20px
- xl: 24px
- 2xl: 32px

## 间距
- unit: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px

## 圆角
- none: 0
- sm: 4px
- md: 8px
- lg: 16px
```

## 输出格式

```markdown
# UI 规范检查报告

## 检查概览
- **设计稿**: login-page.pen
- **设计系统**: default-design-system.md
- **检查项**: 6 项
- **通过**: 4 项
- **警告**: 1 项
- **错误**: 1 项

## 详细结果

### ❌ 颜色规范（1 个问题）

| 元素 | 使用值 | 规范值 | 建议 |
|------|--------|--------|------|
| 登录按钮 | #007AFF | #1890FF (primary) | 更换为主色 |

### ✅ 字体大小（通过）

### ⚠️ 间距规范（1 个警告）

| 元素 | 当前间距 | 规范 | 建议 |
|------|----------|------|------|
| 标题与输入框 | 20px | 应为 4px 倍数 | 调整为 20px → 24px |
```

## 边界

- 当前版本支持解析Pencil JSON格式和文本描述
- 颜色检查为精确匹配，不支持近似色判断
- 复杂布局（grid、flex）的间距检查可能不准确
- 仅检查数值规范，不检查设计可用性

## 与其他 Skill 的关系

```
design-pencil ──▶ design-ui-check ──▶ design-review
  生成设计稿       规范检查           多角色评审
```
