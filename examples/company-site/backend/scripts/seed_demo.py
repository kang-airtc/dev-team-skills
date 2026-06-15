"""Seed demo data: categories, products, news, comments.

运行：
    cd backend
    source venv/bin/activate
    python -m scripts.seed_demo

特点：
- 幂等：按 slug 找；存在则更新，不存在则创建
- 评论：会先清空 demo 标记的评论，再插入
- 图片：来自 Unsplash 公共图床（高质量、商用友好）
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from server.models.category_model import Category
from server.models.comment_model import Comment
from server.models.news_model import News
from server.models.product_model import Product
from server.models.user_model import User
from server.settings import settings
from server.utils.jwt import get_password_hash


# ---------------------------------------------------------------------------
# 数据
# ---------------------------------------------------------------------------

# 用 Unsplash 自动尺寸参数：?auto=format&fit=crop&w=1600&q=80
def _img(photo_id: str, w: int = 1600) -> str:
    return f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w={w}&q=80"


CATEGORIES: List[Dict[str, Any]] = [
    {"name": "手机", "slug": "phone", "description": "随身的旗舰，握在手里的极致。", "sort_order": 1},
    {"name": "平板", "slug": "tablet", "description": "随时随地，轻盈的创作空间。", "sort_order": 2},
    {"name": "笔记本", "slug": "laptop", "description": "为创意而生的桌面级算力。", "sort_order": 3},
    {"name": "配件", "slug": "accessory", "description": "为生活补全最后一块拼图。", "sort_order": 4},
]


# 旧版本可能写入过的 slug，下次执行时清理掉，避免历史数据残留
LEGACY_PRODUCT_SLUGS = [
    "aurora-16-pro", "aurora-16", "aurora-tab-pro-13", "aurora-tab-air",
    "aurora-book-pro-15", "aurora-book-air-13", "aurora-pods-pro", "aurora-watch",
]
LEGACY_NEWS_SLUGS = [
    "aurora-16-pro-launch", "tab-pro-tandem-oled",
    "ces-recap-2026", "ces-recap",
    "sustainability-2026", "sustainability",
    "developer-conference-invite",
]


PRODUCTS: List[Dict[str, Any]] = [
    {
        "slug": "phone-pro-16",
        "name": "某某手机 Pro 16",
        "category_slug": "phone",
        "tagline": "PRO. 重新定义。",
        "summary": "钛合金中框，6.7 英寸超视网膜屏，A 级影像系统。",
        "description": (
            "某某手机 Pro 16 拥有航空级钛合金中框与双面纳米陶瓷玻璃，\n"
            "6.7 英寸 LTPO 超视网膜屏支持 1–120Hz 自适应刷新。\n"
            "全新 A18 Pro 仿生芯片，CPU 性能提升 25%，GPU 性能提升 40%。\n"
            "三摄系统加入潜望长焦，5x 光学变焦覆盖更多创作场景。"
        ),
        "cover_image": _img("photo-1592750475338-74b7b21085ab"),
        "gallery": [
            _img("photo-1511707171634-5f897ff02aa9"),
            _img("photo-1574944985070-8f3ebc6b79d2"),
            _img("photo-1605236453806-6ff36851218e"),
        ],
        "specs": {
            "屏幕": "6.7 英寸 LTPO Super Retina XDR · 120Hz",
            "芯片": "A18 Pro 仿生",
            "影像": "4800 万主摄 + 1200 万超广角 + 1200 万 5x 长焦",
            "存储": "256GB / 512GB / 1TB",
            "电池": "4422 mAh，支持 27W 有线 / 25W MagSafe",
            "材质": "5 级钛金属中框 · 双面纳米陶瓷玻璃",
            "重量": "199 g",
        },
        "price": 8999,
        "is_featured": True,
        "is_published": True,
        "sort_order": 1,
    },
    {
        "slug": "phone-16",
        "name": "某某手机 16",
        "category_slug": "phone",
        "tagline": "鲜活每一天。",
        "summary": "活力配色，双摄系统，整日续航。",
        "description": (
            "某某手机 16 带来五种活力配色与亲肤手感的航空铝中框，\n"
            "6.1 英寸超视网膜屏，配备全新主摄 + 超广角双摄系统。\n"
            "A18 仿生芯片让游戏、剪辑、AI 应用全面流畅。"
        ),
        "cover_image": _img("photo-1567581935884-3349723552ca"),
        "gallery": [_img("photo-1556656793-08538906a9f8")],
        "specs": {
            "屏幕": "6.1 英寸 Super Retina XDR",
            "芯片": "A18 仿生",
            "影像": "4800 万主摄 + 1200 万超广角",
            "存储": "128GB / 256GB / 512GB",
            "电池": "3561 mAh",
            "重量": "171 g",
        },
        "price": 5999,
        "is_featured": True,
        "is_published": True,
        "sort_order": 2,
    },
    {
        "slug": "tab-pro-13",
        "name": "某某平板 Pro 13",
        "category_slug": "tablet",
        "tagline": "屏幕之外，皆为可能。",
        "summary": "13 英寸超视网膜 XDR 屏，M4 同源算力，桌面级专业体验。",
        "description": (
            "某某平板 Pro 13 配备双层串联 OLED 显示屏，\n"
            "支持 P3 广色域与 1600 尼特持续亮度。\n"
            "搭载与笔记本同源的 M 系列芯片，足以胜任 4K 视频剪辑、3D 建模。\n"
            "搭配磁吸触控键盘与触控笔，工作与创作随时切换。"
        ),
        "cover_image": _img("photo-1561154464-82e9adf32764"),
        "gallery": [_img("photo-1544244015-0df4b3ffc6b0"), _img("photo-1542751110-97427bbecf20")],
        "specs": {
            "屏幕": "13 英寸 Tandem OLED · ProMotion 120Hz",
            "芯片": "M-Series Pro",
            "存储": "256GB / 512GB / 1TB / 2TB",
            "接口": "USB-C 雷雳 4",
            "重量": "579 g",
        },
        "price": 8499,
        "is_featured": True,
        "is_published": True,
        "sort_order": 3,
    },
    {
        "slug": "tab-air",
        "name": "某某平板",
        "category_slug": "tablet",
        "tagline": "轻盈。强大。",
        "summary": "轻于 460g 的 11 英寸液态视网膜屏，性能与便携并存。",
        "description": (
            "某某平板 拥有 11 英寸 / 13 英寸两种尺寸可选，\n"
            "一体成型铝合金机身，重量轻至 460g，是出行与学习的理想伴侣。"
        ),
        "cover_image": _img("photo-1623126908029-58cb08a2b272"),
        "gallery": [],
        "specs": {
            "屏幕": "11 / 13 英寸液态视网膜屏",
            "芯片": "M-Series",
            "重量": "460 g",
        },
        "price": 4799,
        "is_featured": False,
        "is_published": True,
        "sort_order": 4,
    },
    {
        "slug": "book-pro-15",
        "name": "某某笔记本 Pro 15",
        "category_slug": "laptop",
        "tagline": "为创意造的桌面级笔电。",
        "summary": "M-Series Pro 芯片，120Hz 视网膜显示屏，整日不插电。",
        "description": (
            "某某笔记本 Pro 15 配备 15.3 英寸 Liquid Retina XDR 屏幕，\n"
            "搭载 M-Series Pro 芯片与高带宽统一内存。\n"
            "电池续航最长可达 22 小时，全天创作无忧。"
        ),
        "cover_image": _img("photo-1517336714731-489689fd1ca8"),
        "gallery": [_img("photo-1496181133206-80ce9b88a853"), _img("photo-1611186871348-b1ce696e52c9")],
        "specs": {
            "屏幕": "15.3 英寸 Liquid Retina XDR · 120Hz",
            "芯片": "M-Series Pro · 12 核 CPU / 18 核 GPU",
            "内存": "18GB / 36GB / 48GB 统一内存",
            "存储": "512GB / 1TB / 2TB / 4TB",
            "续航": "最长 22 小时视频播放",
            "接口": "雷雳 4 × 3 / HDMI / SD / MagSafe 3",
        },
        "price": 14999,
        "is_featured": True,
        "is_published": True,
        "sort_order": 5,
    },
    {
        "slug": "book-air-13",
        "name": "某某笔记本 13",
        "category_slug": "laptop",
        "tagline": "薄至极致，强至非凡。",
        "summary": "13.6 英寸液态视网膜屏，轻薄机身，全天候续航。",
        "description": (
            "某某笔记本 13 仅厚 11.3mm，重 1.24kg，\n"
            "配备 13.6 英寸液态视网膜屏与 M-Series 芯片，\n"
            "无风扇设计带来全天安静运行。"
        ),
        "cover_image": _img("photo-1541807084-5c52b6b3adef"),
        "gallery": [],
        "specs": {
            "屏幕": "13.6 英寸液态视网膜屏",
            "芯片": "M-Series · 8 核 CPU / 10 核 GPU",
            "重量": "1.24 kg",
            "续航": "最长 18 小时",
        },
        "price": 8999,
        "is_featured": False,
        "is_published": True,
        "sort_order": 6,
    },
    {
        "slug": "pods-pro",
        "name": "某某耳机 Pro",
        "category_slug": "accessory",
        "tagline": "听见，更被听见。",
        "summary": "自适应主动降噪，自适应音频，更精准的空间音频。",
        "description": (
            "某某耳机 Pro 全新升级 H2 芯片，\n"
            "自适应音频根据环境实时切换降噪与通透模式。\n"
            "充电盒支持 USB-C 与无线充电，最长 30 小时续航。"
        ),
        "cover_image": _img("photo-1606220588913-b3aacb4d2f46"),
        "gallery": [_img("photo-1572569511254-d8f925fe2cbb")],
        "specs": {
            "芯片": "H2",
            "降噪": "自适应主动降噪",
            "续航": "单次 6 小时 / 总续航 30 小时",
            "充电": "USB-C / MagSafe 无线充电",
        },
        "price": 1899,
        "is_featured": True,
        "is_published": True,
        "sort_order": 7,
    },
    {
        "slug": "watch",
        "name": "某某手表",
        "category_slug": "accessory",
        "tagline": "腕上的健康专家。",
        "summary": "全天血氧、心率监测，全新 Always-On 视网膜屏。",
        "description": (
            "某某手表 拥有更纤薄的边框与更亮的 Always-On 视网膜屏，\n"
            "配备全新双核 S10 芯片，配合精准健康传感器，\n"
            "全天监测心率、血氧与睡眠质量。"
        ),
        "cover_image": _img("photo-1546435770-a3e426bf472b"),
        "gallery": [_img("photo-1579586337278-3befd40fd17a")],
        "specs": {
            "屏幕": "Always-On Retina LTPO OLED",
            "芯片": "S10 双核",
            "防水": "50 米",
            "续航": "最长 36 小时",
        },
        "price": 2999,
        "is_featured": False,
        "is_published": True,
        "sort_order": 8,
    },
]


NEWS: List[Dict[str, Any]] = [
    {
        "slug": "phone-pro-16-launch",
        "title": "某某手机 Pro 16 发布：钛金属，重新定义 Pro",
        "summary": "全新一代旗舰，更轻、更强、更环保的钛金属机身正式登场。",
        "cover_image": _img("photo-1605236453806-6ff36851218e"),
        "author": "编辑部",
        "is_published": True,
        "days_ago": 2,
        "content": (
            "今天，我们正式发布某某手机 Pro 16。\n\n"
            "这是我们史上最坚固、也最轻盈的 Pro 系列。\n"
            "采用 5 级钛金属中框，重量降至 199 克。\n\n"
            "全新 A18 Pro 仿生芯片性能提升 25%，\n"
            "三摄系统加入潜望长焦，光学变焦达到 5 倍。\n\n"
            "某某手机 Pro 16 将于本周五开启预订，下周二正式发售。"
        ),
    },
    {
        "slug": "tab-pro-tandem-oled",
        "title": "某某平板 Pro 13：双层串联 OLED 屏幕带来什么？",
        "summary": "在屏幕显示技术上，我们做了一次跨代级别的升级。",
        "cover_image": _img("photo-1542751110-97427bbecf20"),
        "author": "硬件团队",
        "is_published": True,
        "days_ago": 7,
        "content": (
            "屏幕，是一块平板的灵魂。\n\n"
            "某某平板 Pro 13 首次采用双层串联 OLED 显示技术，\n"
            "通过将两层 OLED 像素堆叠，亮度与寿命同时翻倍。\n\n"
            "持续亮度 1000 尼特、HDR 峰值 1600 尼特，\n"
            "在阳光下也能清晰阅读、精准调色。"
        ),
    },
    {
        "slug": "conference-recap",
        "title": "某某大会现场：我们带去了什么？",
        "summary": "回顾本次展会现场的亮点产品与互动体验。",
        "cover_image": _img("photo-1531973576160-7125cd663d86"),
        "author": "市场团队",
        "is_published": True,
        "days_ago": 18,
        "content": (
            "本次某某大会，我们以「Calm Technology」为主题，\n"
            "搭建了一座 600 平方米的体验空间。\n\n"
            "现场展示了全系新品、跨设备协同演示，以及与开发者的合作项目。\n\n"
            "感谢每一位到场的朋友。"
        ),
    },
    {
        "slug": "developer-conference-invite",
        "title": "某某开发者大会 2026 邀请函",
        "summary": "面向全球开发者的年度盛会，6 月线上 + 线下同步举行。",
        "cover_image": _img("photo-1515378791036-0648a3ef77b2"),
        "author": "开发者关系",
        "is_published": True,
        "days_ago": 45,
        "content": (
            "今年的开发者大会将聚焦三大主题：\n"
            "1. 端侧智能与隐私保护\n"
            "2. 跨设备应用框架\n"
            "3. 新一代图形与游戏 API\n\n"
            "欢迎报名。"
        ),
    },
]


# 评论：(target_slug_or_news_slug, target_type, nickname, content, days_ago)
COMMENTS: List[Dict[str, Any]] = [
    # 产品评论
    {"target_slug": "phone-pro-16", "type": "product", "nickname": "Lina", "content": "钛金属真的轻太多了，握感很舒服。", "days_ago": 1},
    {"target_slug": "phone-pro-16", "type": "product", "nickname": "数码玩家", "content": "5x 长焦演唱会拍偶像稳了！", "days_ago": 0},
    {"target_slug": "phone-pro-16", "type": "product", "nickname": "Echo", "content": "屏幕色彩比上一代准了一档，剪片直出。", "days_ago": 0},
    {"target_slug": "tab-pro-13", "type": "product", "nickname": "设计师 Yang", "content": "OLED 调色真的爽，外接屏都省了。", "days_ago": 3},
    {"target_slug": "tab-pro-13", "type": "product", "nickname": "Mei", "content": "终于等到 13 寸版本，看 PDF 太合适。", "days_ago": 2},
    {"target_slug": "book-pro-15", "type": "product", "nickname": "前端老司机", "content": "M Pro 跑 docker 完全没压力，续航惊人。", "days_ago": 5},
    {"target_slug": "pods-pro", "type": "product", "nickname": "Tom", "content": "通勤降噪非常干净，地铁里能完全沉浸。", "days_ago": 4},
    # 新闻评论
    {"target_slug": "phone-pro-16-launch", "type": "news", "nickname": "Anna", "content": "已下单，期待发售日！", "days_ago": 1},
    {"target_slug": "phone-pro-16-launch", "type": "news", "nickname": "Hugo", "content": "希望国行价格友好一点 🙏", "days_ago": 1},
    {"target_slug": "tab-pro-tandem-oled", "type": "news", "nickname": "屏幕控", "content": "技术细节写得很清楚，赞！", "days_ago": 6},
    {"target_slug": "developer-conference-invite", "type": "news", "nickname": "indie dev", "content": "求线下名额！", "days_ago": 30},
]


# ---------------------------------------------------------------------------
# 执行
# ---------------------------------------------------------------------------

DEMO_NICKNAMES = {c["nickname"] for c in COMMENTS}


async def upsert_category(session: AsyncSession, data: Dict[str, Any]) -> Category:
    result = await session.execute(select(Category).where(Category.slug == data["slug"]))
    obj = result.scalar_one_or_none()
    if obj:
        for k, v in data.items():
            setattr(obj, k, v)
    else:
        obj = Category(**data)
        session.add(obj)
    await session.flush()
    return obj


async def upsert_product(session: AsyncSession, data: Dict[str, Any], category_id: int) -> Product:
    payload = {
        "name": data["name"],
        "slug": data["slug"],
        "category_id": category_id,
        "tagline": data.get("tagline"),
        "summary": data.get("summary"),
        "description": data.get("description"),
        "cover_image": data.get("cover_image"),
        "gallery": json.dumps(data.get("gallery", []), ensure_ascii=False),
        "specs": json.dumps(data.get("specs", {}), ensure_ascii=False),
        "price": data.get("price"),
        "is_featured": data.get("is_featured", False),
        "is_published": data.get("is_published", True),
        "sort_order": data.get("sort_order", 0),
    }
    result = await session.execute(select(Product).where(Product.slug == data["slug"]))
    obj = result.scalar_one_or_none()
    if obj:
        for k, v in payload.items():
            setattr(obj, k, v)
    else:
        obj = Product(**payload)
        session.add(obj)
    await session.flush()
    return obj


async def upsert_news(session: AsyncSession, data: Dict[str, Any]) -> News:
    published_at = datetime.now(timezone.utc) - timedelta(days=int(data.get("days_ago", 0)))
    payload = {
        "title": data["title"],
        "slug": data["slug"],
        "summary": data.get("summary"),
        "cover_image": data.get("cover_image"),
        "content": data["content"],
        "author": data.get("author"),
        "is_published": data.get("is_published", True),
        "published_at": published_at,
    }
    result = await session.execute(select(News).where(News.slug == data["slug"]))
    obj = result.scalar_one_or_none()
    if obj:
        for k, v in payload.items():
            setattr(obj, k, v)
    else:
        obj = News(**payload)
        session.add(obj)
    await session.flush()
    return obj


async def reset_demo_comments(session: AsyncSession) -> None:
    """删除已存在的 demo 评论（按昵称匹配）。"""
    if not DEMO_NICKNAMES:
        return
    await session.execute(delete(Comment).where(Comment.nickname.in_(DEMO_NICKNAMES)))


async def cleanup_legacy(session: AsyncSession) -> None:
    """删除上一版 demo 写入但本次不再使用的产品 / 新闻（含其评论）。"""
    if LEGACY_PRODUCT_SLUGS:
        old_products = (
            await session.execute(
                select(Product).where(Product.slug.in_(LEGACY_PRODUCT_SLUGS))
            )
        ).scalars().all()
        if old_products:
            ids = [p.id for p in old_products]
            await session.execute(
                delete(Comment).where(
                    Comment.target_type == "product", Comment.target_id.in_(ids)
                )
            )
            for p in old_products:
                await session.delete(p)
            print(f"[seed] cleanup legacy products: {len(old_products)}")

    if LEGACY_NEWS_SLUGS:
        old_news = (
            await session.execute(
                select(News).where(News.slug.in_(LEGACY_NEWS_SLUGS))
            )
        ).scalars().all()
        # 仅删除真正在 legacy 列表里、且当前不再使用的（current 也用相同 slug 时跳过）
        current_news_slugs = {n["slug"] for n in NEWS}
        purge = [n for n in old_news if n.slug not in current_news_slugs]
        if purge:
            ids = [n.id for n in purge]
            await session.execute(
                delete(Comment).where(
                    Comment.target_type == "news", Comment.target_id.in_(ids)
                )
            )
            for n in purge:
                await session.delete(n)
            print(f"[seed] cleanup legacy news:     {len(purge)}")


DEMO_ADMIN = {
    "username": "admin",
    "email": "admin@example.com",
    "password": "admin123",
    "full_name": "示例管理员",
}


async def upsert_admin(session: AsyncSession) -> None:
    """确保有一个 admin/admin123 的超级管理员。"""
    result = await session.execute(
        select(User).where(User.username == DEMO_ADMIN["username"])
    )
    user = result.scalar_one_or_none()
    if user is None:
        session.add(
            User(
                username=DEMO_ADMIN["username"],
                email=DEMO_ADMIN["email"],
                hashed_password=get_password_hash(DEMO_ADMIN["password"]),
                full_name=DEMO_ADMIN["full_name"],
                is_active=True,
                is_superuser=True,
            )
        )
        print(f"[seed] admin user:    created ({DEMO_ADMIN['username']}/{DEMO_ADMIN['password']})")
    else:
        # 已存在则只重置密码 + 确保 superuser，方便忘了密码时重跑
        user.hashed_password = get_password_hash(DEMO_ADMIN["password"])
        user.is_superuser = True
        user.is_active = True
        user.email = DEMO_ADMIN["email"]
        print(f"[seed] admin user:    reset ({DEMO_ADMIN['username']}/{DEMO_ADMIN['password']})")


async def seed() -> None:
    engine = create_async_engine(str(settings.db_url), echo=False)
    Session = async_sessionmaker(engine, expire_on_commit=False)

    async with Session() as session:
        # admin 账号（幂等）
        await upsert_admin(session)

        # cleanup legacy aurora-* 数据
        await cleanup_legacy(session)

        # categories
        cat_map: Dict[str, int] = {}
        for c in CATEGORIES:
            obj = await upsert_category(session, c)
            cat_map[obj.slug] = obj.id
        print(f"[seed] categories: {len(cat_map)}")

        # products
        product_map: Dict[str, int] = {}
        for p in PRODUCTS:
            cat_id = cat_map.get(p["category_slug"])
            obj = await upsert_product(session, p, cat_id)
            product_map[obj.slug] = obj.id
        print(f"[seed] products:   {len(product_map)}")

        # news
        news_map: Dict[str, int] = {}
        for n in NEWS:
            obj = await upsert_news(session, n)
            news_map[obj.slug] = obj.id
        print(f"[seed] news:       {len(news_map)}")

        # comments：清空 demo 再插入
        await reset_demo_comments(session)
        comment_count = 0
        for c in COMMENTS:
            target_id = (
                product_map.get(c["target_slug"])
                if c["type"] == "product"
                else news_map.get(c["target_slug"])
            )
            if target_id is None:
                continue
            created_at = datetime.now(timezone.utc) - timedelta(days=int(c.get("days_ago", 0)))
            session.add(
                Comment(
                    target_type=c["type"],
                    target_id=target_id,
                    nickname=c["nickname"],
                    content=c["content"],
                    is_approved=True,
                    created_at=created_at,
                )
            )
            comment_count += 1
        print(f"[seed] comments:   {comment_count}")

        await session.commit()

    await engine.dispose()
    print("[seed] ✅ Done.")


if __name__ == "__main__":
    asyncio.run(seed())
