# 后端规范扫描报告

> 来源 Skill：`review-backend`（本地自查模式，开发阶段）  
> 输入：`outputs/bad-samples/uploads_views_bad.py`  
> 评审阶段会针对 PR diff 再跑一次正式扫描

| 行号 | 级别 | 规则 | 说明 |
|------|------|------|------|
| 30 | P1 | mime-allowlist | MIME 仅信任前端字段，缺白名单校验 |
| 39 | P1 | file-handle-leak | open() 未走上下文管理器，异常时句柄泄漏 |
| 52 | P1 | size-limit | 缺少文件大小上限校验，可被 DoS |
| 54 | P2 | response-format | 返回未走 ApiResponse 包装，违反 {code,msg,data} 约定 |
| 55 | P2 | bare-except | 裸 except 吞掉所有异常，无法定位故障 |

## 总结：5 处违规（3 P1 / 2 P2），不通过

## 修复指引

| 违规 | 修复要点 |
|---|---|
| mime-allowlist | 加 `_MIME_TO_EXT` 字典作为白名单 |
| file-handle-leak | 改 `pathlib.Path.write_bytes()` 或 `with open()` |
| size-limit | 启动配置 `settings.upload_max_bytes`，校验前置 |
| response-format | 路由函数 `response_model=ApiResponse[dict]` |
| bare-except | 业务异常走 `HTTPException`，避免裸 except |

## 回归校验

修复后需重新运行：

```bash
opencode run review-backend \
    --target backend/server/web/api/uploads/views.py \
    --output outputs/03-dev/backend-lint.md
```

期望结果：0 P1 / 0 P2，通过。
