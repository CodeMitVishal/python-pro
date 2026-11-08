"""add created_at to books

Revision ID: 0002
Revises: 0001

The models changed (Book got a created_at column), so the database must change
too, WITHOUT losing the rows that are already there.
"""
import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"        # runs after 0001
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("books") as batch:      # batch mode works on SQLite too
        batch.add_column(sa.Column("created_at", sa.DateTime,
                                   server_default=sa.func.now(), nullable=False))


def downgrade() -> None:
    with op.batch_alter_table("books") as batch:
        batch.drop_column("created_at")
