# 上传模块技术方案

> 来源 Skill：`dev-techspec`  
> 关联 Story：1.2 多图上传  
> 状态：已通过开发评审

## 1. 背景

后台表单需要上传产品封面与图集、新闻封面。AI 给出的草稿仅写了"调用 FastAPI UploadFile"，缺少大小校验、MIME 校验、命名策略与归档目录约定。

## 2. 目标

- 单图与图集统一接口规范
- MIME 白名单 + 大小上限双重校验
- 归档目录按 `YYYY/MM` 月分桶，避免单目录文件数爆炸
- 返回相对 URL，前端拼 `NEXT_PUBLIC_API_URL` 渲染

## 3. 方案对比

| 方案 | 优点 | 缺点 |
|---|---|---|
| A 本地文件系统 + docker volume | 简单、教学友好、零外部依赖 | 多副本部署难 |
| B 对象存储（OSS / S3） | 横向扩展容易 | 教学引入额外依赖 |
| C 二进制存数据库 | 备份容易 | 性能差、不推荐 |

**采纳：A**。教学示例聚焦工程化产物，部署形态保持单机。

## 4. 详细设计

### 4.1 接口

- POST /api/uploads —— 单图
- POST /api/uploads/multi —— 多图（前端循环调用单图接口聚合，本期不暴露独立后端入口）

### 4.2 约束

- MIME ∈ {image/jpeg, image/png, image/webp, image/gif}
- 体积 ≤ 5 MB（`settings.upload_max_bytes = 5242880`）

### 4.3 命名

`{token_hex(12)}.{ext}`，ext 由 MIME 映射而非信任前端 filename。

### 4.4 归档目录

```
uploads/
└── 2026/
    └── 04/
        ├── a3f1...e9.jpg
        └── 7c2b...d1.png
```

### 4.5 返回

```json
{"code": 0, "msg": "ok", "data": {"url": "/uploads/2026/04/a3f1...e9.jpg", "size": 124356, "mime": "image/jpeg"}}
```

## 5. 风险与对策

| 风险 | 影响 | 对策 |
|---|---|---|
| 上传目录被恶意填满 | 服务不可用 | 5 MB 上限 + `monitor-containers` 容量告警 |
| MIME 头伪造 | 上传可执行文件 | 不信任 `file.content_type`，必须走白名单映射 |
| 容器重建丢失文件 | 用户体验事故 | docker volume 挂载到宿主机 `./uploads` |

## 6. 里程碑

- D+0：接口骨架 + 单元测试
- D+1：后端 lint 修复（review-backend 已识别 5 处）
- D+2：前端组件集成
- D+3：自动化测试达标
