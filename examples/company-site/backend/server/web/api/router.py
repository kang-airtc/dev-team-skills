# server/web/api/router.py

from fastapi.routing import APIRouter

from server.web.api import categories, comments, news, products, uploads, users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
