"""models."""
import pkgutil
from pathlib import Path


def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="server.models.",
    )
    for module in modules:
        __import__(module.name)


from server.models.user_model import User
from server.models.category_model import Category
from server.models.product_model import Product
from server.models.news_model import News
from server.models.comment_model import Comment

__all__ = [
    "User",
    "Category",
    "Product",
    "News",
    "Comment",
    "load_all_models",
]
