# base-summarize 调用意图

对应书稿 3.2.3 节，三种调用方式：

## 显式调用

```
/base-summarize 帮我看看 examples/company-site/backend 目录大致在干嘛
```

## 自然语言调用（点名 Skill）

```
请使用 base-summarize 帮我读一下 examples/company-site/backend，梳理一下这是什么项目
```

## 隐式触发

```
我刚 clone 了一个新仓库，先帮我看一眼大致是什么项目
```

> 第三种写法依赖 description 的精度：`description` 里包含“陌生的代码目录”，所以 Agent 会自动激活 base-summarize。
