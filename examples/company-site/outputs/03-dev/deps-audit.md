# 依赖审计

> 来源 Skill：`dev-deps-audit`  
> 输入：`backend/requirements.txt` + `frontend/package.json`  
> 工具：pip-audit + npm audit

## 后端

| 包 | 当前版本 | 漏洞 | 严重度 | 修复版本 |
|---|---|---|---|---|
| `python-jose[cryptography]` | 3.3.0 | CVE-2024-33663 算法混淆 | High | 升级到 3.4.0 |
| `python-multipart` | 0.0.6 | CVE-2024-24762 ReDoS | Medium | 升级到 0.0.7 |
| `aiohttp` | 3.9.1 | 信息泄漏 | Low | 升级到 3.9.5 |

## 前端

| 包 | 当前版本 | 漏洞 | 严重度 | 修复版本 |
|---|---|---|---|---|
| `next` | 13.5.4 | CVE-2024-34351 SSRF | High | 升级到 13.5.6 |
| `axios` | 1.6.0 | CVE-2023-45857 CSRF | Medium | 升级到 1.6.5 |

## 处理建议

- High 漏洞 5 个工作日内处理完毕
- Medium 漏洞下个 Sprint 处理
- Low 漏洞跟踪即可，无需紧急升级

## 复审

修复完成后重新运行：

```bash
opencode run dev-deps-audit \
    --project dev-team-skills/examples/company-site \
    --output  outputs/03-dev/deps-audit.md
```
