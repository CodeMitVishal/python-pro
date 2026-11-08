"""create authors and books

Revision ID: 0001
Revises:
"""
import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None          # the first migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column("country", sa.String(2), nullable=True),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("price", sa.Float, nullable=False),
        sa.Column("author_id", sa.Integer, sa.ForeignKey("authors.id"), nullable=False),
    )


def downgrade() -> None:      # every migration can be undone
    op.drop_table("books")
    op.drop_table("authors")
