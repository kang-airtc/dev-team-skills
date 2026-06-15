# base-dir-view 调用意图

对应书稿 3.3.6 节，三种调用方式：

## 显式调用

```
/base-dir-view ./examples/company-site 4
```

## 自然语言调用（点名 Skill）

```
请使用 base-dir-view 帮我看一下 examples/company-site 的目录结构，深度限制 4 层
```

## 隐式触发

```
帮我看看 examples/company-site 整体结构大概是什么样的
```

## 等价命令行

```bash
.opencode/skills/base-dir-view/scripts/view.sh ./examples/company-site 4
```
