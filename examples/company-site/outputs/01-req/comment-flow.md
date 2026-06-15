# 评论提交流程

> 来源 Skill：`req-flowchart`  
> 范围：访客发评论 → 后台审核 → 公开站可见

```mermaid
flowchart TD
    A[访客打开产品/新闻详情页] --> B[填写昵称/邮箱/内容]
    B --> C{前端校验}
    C -- 失败 --> B
    C -- 通过 --> D[POST /api/comments]
    D --> E{后端校验}
    E -- 字段非法 --> F[返回 code=1004]
    E -- 通过 --> G[写入 comments 表 is_visible=false]
    G --> H[返回 code=0 + 提示"待审核"]
    H --> I[访客看到"评论已提交"]

    subgraph 后台审核
        J[admin 进入 /dashboard/comments] --> K{逐条查看}
        K -- 合规 --> L[点击"显示"]
        K -- 不合规 --> M[点击"删除"]
        L --> N[is_visible=true]
        M --> O[软删除 deleted_at]
    end

    N --> P[公开站详情页评论区出现新评论]
```

## 关键节点

| 节点 | 责任方 | 异常处理 |
|---|---|---|
| 前端校验 | frontend | 内容空 / >1000 字 → 即时提示 |
| 后端校验 | backend | 字段缺失 → code=1004 |
| 落库 | backend DAO | `is_visible=false` 默认 |
| 审核 | admin | 软删除保留追溯 |
