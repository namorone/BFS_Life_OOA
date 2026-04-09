"""auth user fields and item owner

Revision ID: e8f4a1c2b3d4
Revises: 659231255fd0
Create Date: 2026-04-01

"""

import sqlalchemy as sa

from alembic import op

revision = "e8f4a1c2b3d4"
down_revision = "659231255fd0"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(sa.text("DELETE FROM warranties"))
    op.execute(sa.text("DELETE FROM items"))
    op.execute(sa.text("DELETE FROM users"))

    op.add_column(
        "users",
        sa.Column("full_name", sa.String(length=255), nullable=False),
    )
    op.add_column(
        "users",
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
    )

    op.add_column("items", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_index(op.f("ix_items_user_id"), "items", ["user_id"], unique=False)
    op.create_foreign_key(
        "fk_items_user_id_users",
        "items",
        "users",
        ["user_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint("fk_items_user_id_users", "items", type_="foreignkey")
    op.drop_index(op.f("ix_items_user_id"), table_name="items")
    op.drop_column("items", "user_id")

    op.drop_column("users", "hashed_password")
    op.drop_column("users", "full_name")
