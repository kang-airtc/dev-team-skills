# review-backend 报告：feature/uploads → main

## P1（必须修）
- `views.py:18` —— MIME 仅信任前端字段，可绕过白名单
- `views.py:41` —— 无文件大小校验，可上传 GB 级文件耗尽磁盘

## P2（建议修）
- `views.py:50` —— 裸 except 吞掉所有异常，故障无法定位
- `views.py:51` —— 返回未走 ApiResponse 包装

## P3（可选）
- `views.py:8` —— 缺函数级 docstring

## 结论：3 P1 阻断合并；待修复后重新评审

## 修复后回归（commit 8a3f...e2 / 1c9e...4a）

- 3 P1 全部消除
- 2 P2 全部消除
- P3 docstring 已补
- 重跑 review-backend：0 P1 / 0 P2 / 0 P3 → 通过
