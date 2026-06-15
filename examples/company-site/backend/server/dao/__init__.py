"""DAO layer."""
from server.dao.user_dao import UserDAO
from server.dao.category_dao import CategoryDAO
from server.dao.product_dao import ProductDAO
from server.dao.news_dao import NewsDAO
from server.dao.comment_dao import CommentDAO

__all__ = ["UserDAO", "CategoryDAO", "ProductDAO", "NewsDAO", "CommentDAO"]
