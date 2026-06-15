# company-site / frontend

Next.js 13 App Router + Tailwind + TypeScript。**公开站与后台共用一个工程**，通过路由组分隔。

## 启动

```bash
npm install
npm run dev   # http://localhost:3000
```

## 目录

```
frontend/
├── app/
│   ├── layout.tsx                # 根布局（仅 html + body）
│   ├── (public)/                 # 公开站路由组：套 Navbar + Footer
│   │   ├── layout.tsx
│   │   ├── page.tsx              # /
│   │   ├── about/page.tsx
│   │   ├── products/page.tsx + [slug]/page.tsx
│   │   ├── news/page.tsx + [slug]/page.tsx
│   │   └── contact/page.tsx
│   └── (admin)/                  # 后台路由组：无公开站布局
│       ├── login/page.tsx        # /login
│       ├── register/page.tsx     # /register
│       └── dashboard/page.tsx    # /dashboard
├── components/                   # Navbar / Footer（公开站用）
├── services/
│   ├── auth.ts                   # login / register / getCurrentUser / logout
│   └── api.ts                    # 业务接口占位（products / news / messages）
├── utils/request.ts              # axios 拦截器 + 401 自动刷新（与参考项目一致）
├── styles/globals.css
├── config.ts                     # API_BASE
├── tailwind.config.js
└── tsconfig.json
```
