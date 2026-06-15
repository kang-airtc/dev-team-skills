# 测试素材 / Sample Assets

随书示例图片，全部来自 [Unsplash](https://unsplash.com)（CC0 / Unsplash License，可商用 + 免署名）。
仅用于本地测试图片上传功能、验证产品 / 新闻封面与图集渲染。

## 目录

```
sample-assets/
├── products/      # 8 个产品的封面与图集
└── news/          # 5 条新闻的封面
```

## 使用方法

1. 启动后端（已挂载 `/api/uploads`）与前端
2. 登录后台 `/dashboard`
3. 进入「产品 → 编辑某产品」，在「封面图」点 **上传图片**，从 `products/` 选对应文件
4. 在「图集」点 **添加图片** 可多选
5. 新闻同理，从 `news/` 选

## 文件映射

### 产品 `products/`

| Slug | 文件 | 用途 |
| --- | --- | --- |
| `phone-pro-16` | `phone-pro-16-cover.jpg` | 封面 |
| | `phone-pro-16-1.jpg` ~ `-3.jpg` | 图集 |
| `phone-16` | `phone-16-cover.jpg` | 封面 |
| | `phone-16-1.jpg` | 图集 |
| `tab-pro-13` | `tab-pro-13-cover.jpg` | 封面 |
| | `tab-pro-13-1.jpg` ~ `-2.jpg` | 图集 |
| `tab-air` | `tab-air-cover.jpg` | 封面 |
| `book-pro-15` | `book-pro-15-cover.jpg` | 封面 |
| | `book-pro-15-1.jpg` ~ `-2.jpg` | 图集 |
| `book-air-13` | `book-air-13-cover.jpg` | 封面 |
| `pods-pro` | `pods-pro-cover.jpg` | 封面 |
| | `pods-pro-1.jpg` | 图集 |
| `watch` | `watch-cover.jpg` | 封面 |
| | `watch-1.jpg` | 图集 |

### 新闻 `news/`

| Slug | 文件 |
| --- | --- |
| `phone-pro-16-launch` | `phone-pro-16-launch.jpg` |
| `tab-pro-tandem-oled` | `tab-pro-tandem-oled.jpg` |
| `ces-recap-2026` | `ces-recap-2026.jpg` |
| `sustainability-2026` | `sustainability-2026.jpg` |
| `developer-conference-invite` | `developer-conference-invite.jpg` |

## 重新下载

如果文件丢失，运行根目录的 `download.sh` 即可重新拉取所有素材：

```bash
bash sample-assets/download.sh
```
