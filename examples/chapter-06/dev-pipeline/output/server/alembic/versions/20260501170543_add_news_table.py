"""add_news_table

Revision ID: 4c06173fd308
Revises:
Create Date: 2026-05-01 17:05:43
"""

import sqlalchemy as sa
from alembic import op


revision = "4c06173fd308"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "news",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=True),
        sa.Column("cover_image", sa.String(length=500), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("author", sa.String(length=100), nullable=True),
        sa.Column("is_published", sa.Boolean(), nullable=False, default=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_news_title", "news", ["title"])
    op.create_index("ix_news_slug", "news", ["slug"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_news_slug", table_name="news")
    op.drop_index("ix_news_title", table_name="news")
    op.drop_table("news")
