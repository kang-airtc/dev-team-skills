# my-agent-cli spec

## 目标

向 AI 提问，并在本地记录历史，方便回溯。

## 命令

| 命令 | 行为 |
|------|------|
| `ask <question>` | 向 AI 提问，打印回答，写入历史 |
| `history` | 打印历史列表（序号 + 时间戳 + 问题） |
| `clear` | 清空历史，打印确认信息 |

## 决策记录

| 决策点 | 结论 | 原因 |
|--------|------|------|
| history 存储位置 | `~/.my-agent-cli/history.json` | 跨项目共享，不污染代码目录 |
| 最大条数 | 20 条，超出删最旧 | 避免文件无限增长 |
| AI 响应 | mock：`Echo: <question>` | 先跑通流程，API 集成后续再加 |
| 退出码 | 0=成功, 1=用法错误 | 方便脚本调用判断 |
| `--json` 输出 | 不支持 | YAGNI |

## 不在 scope 内

- 真实 AI API 调用
- 配置文件（`~/.my-agent-cli/config.yaml`）
- 多用户 / 多 session
- 搜索历史
