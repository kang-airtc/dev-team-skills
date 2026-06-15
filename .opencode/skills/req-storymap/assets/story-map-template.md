# 用户故事地图模板

# 用户故事地图

**项目**: {{project_name}}
**生成时间**: {{date}}
**说明**: 横向为用户旅程阶段，纵向为功能优先级，每一列为一个可发布的版本

---

## Markdown 表格版

| 活动 | 任务 | {{release_1}} | {{release_2}} | {{release_3}} |
|------|------|---------------|---------------|---------------|
{{rows}}

---

## Mermaid 用户旅程图

```mermaid
journey
    title {{journey_title}}
{{mermaid_sections}}
```

---

## 版本说明

### {{release_1}}
（MVP - 最小可用版本）
{{release_1_desc}}

### {{release_2}}
{{release_2_desc}}

### {{release_3}}
{{release_3_desc}}

---

## 功能缺口分析

（以下活动在当前 Backlog 中缺少 Story，需补充）
{{gaps}}
