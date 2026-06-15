---
name: design-discuss
description: 针对设计方案的多选项决策，模拟多角色讨论并输出结构化决策记录
---

# Design Discuss - 设计决策讨论

针对设计方案中的争议点（如A方案 vs B方案），模拟拉上产品经理、UI设计师、前端开发等多角色进行结构化讨论，输出包含利弊分析和最终决策的记录文档。

## 触发场景

- 设计方案有多个可行选项，需要团队决策
- 设计评审会上出现分歧，需要记录决策过程
- 需要多角色视角评估设计选项
- 希望保留决策历史，便于后续追溯

## 目录结构

```
design-discuss/
├── SKILL.md
├── scripts/
│   └── design_discuss.py
└── assets/
    └── role-templates.md
```

## 依赖

仅使用 Python 标准库，无需额外依赖。

## 使用方法

```bash
# 交互式讨论
python3 .opencode/skills/design-discuss/scripts/design_discuss.py

# 命令行方式
python3 .opencode/skills/design-discuss/scripts/design_discuss.py \
  --topic "登录页应该用弹窗还是独立页面" \
  --options "弹窗,独立页面" \
  --roles "product-manager,ui-designer,frontend-dev" \
  --output "decision.md"
```

参数：
- `--topic, -t`：讨论主题
- `--options, -o`：选项列表，逗号分隔
- `--roles, -r`：参与角色，逗号分隔
- `--output`：输出决策记录路径，默认 `decision.md`

## 参与角色

默认角色（从 AGENTS.md 读取，不存在则使用内置定义）：

| 角色 | 视角 | 关注点 |
|------|------|--------|
| **Product Manager** | 业务与用户 | 用户体验、业务目标、转化路径 |
| **UI Designer** | 视觉与交互 | 视觉一致性、空间利用、设计规范 |
| **Frontend Dev** | 实现与维护 | 实现成本、组件复用、性能影响 |
| **Backend Dev** | 数据与接口 | 接口设计、数据流、权限控制 |

## 输出格式

```markdown
# 设计决策记录：登录页形式

**决策时间**: 2024-01-15
**参与角色**: Product Manager, UI Designer, Frontend Dev

## 议题

登录页应该用弹窗还是独立页面？

## 选项分析

### 选项 A：弹窗

**Product Manager**
- 👍 优点：用户不离开当前页面，流失率低
- 👍 优点：登录后可以无缝继续操作
- 👎 缺点：在移动端体验差，屏幕空间有限
- 👎 缺点：不利于SEO优化
- **倾向**: 不推荐

**UI Designer**
- 👍 优点：可以复用现有弹窗组件
- 👎 缺点：表单字段多时空间拥挤
- 👎 缺点：难以展示品牌元素和辅助信息
- **倾向**: 不推荐

**Frontend Dev**
- 👍 优点：无需新路由，实现简单
- 👍 优点：状态管理更简单
- 👎 缺点：弹窗层级管理复杂（z-index）
- **倾向**: 推荐

### 选项 B：独立页面

**Product Manager**
- 👍 优点：移动端体验好，有充足空间
- 👍 优点：可以做SEO优化
- 👍 优点：可以展示品牌信息和辅助功能
- 👎 缺点：用户可能流失
- **倾向**: 推荐

**UI Designer**
- 👍 优点：设计空间大，可以充分表达品牌
- 👍 优点：可以放置更多辅助信息和链接
- 👍 优点：符合用户认知（登录=新页面）
- **倾向**: 推荐

**Frontend Dev**
- 👎 缺点：需要新路由和页面组件
- 👎 缺点：登录后需要处理返回逻辑
- **倾向**: 不推荐

## 决策结果

**采用方案**: 独立页面

**决策理由**:
1. 3个角色中有2个（PM、UI）明确推荐独立页面
2. 用户体验因素（移动端适配、品牌展示）权重更高
3. Frontend Dev 的顾虑可通过路由设计和组件复用解决

**异议记录**:
- Frontend Dev：建议评估路由改造成本，使用现有 Layout 组件减少工作量

## 后续行动

- [ ] Frontend Dev 评估路由改造成本（2天）
- [ ] UI Designer 设计独立页面初稿（3天）
- [ ] Product Manager 确定登录后的返回策略

## 备注

（此处记录其他相关信息）
```

## 边界

- 本Skill模拟的是**结构化讨论流程**，不是真实的团队会议
- 各角色的观点基于内置模板生成，需要人工审核和补充
- 最终决策需要团队实际讨论确认，不建议完全依赖自动输出
- 适合用于会前准备和会后记录，不适合替代实际讨论

## 与其他 Skill 的关系

```
design-review ──▶ design-discuss
  发现问题       决策讨论
```
