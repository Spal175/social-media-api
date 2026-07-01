"""Create posts table

Revision ID: 907f9f2ed833
Revises: 
Create Date: 2026-06-30 20:06:15.940221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '907f9f2ed833'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # Users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "createdat",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()")
        )
    )

    # Posts table
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column(
            "published",
            sa.Boolean(),
            nullable=True,
            server_default="True"
        ),
        sa.Column(
            "createdat",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()")
        ),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
            ondelete="CASCADE"
        )
    )

    # Votes table
    op.create_table(
        "votes",
        sa.Column("posts_id", sa.Integer(), nullable=False),
        sa.Column("users_id", sa.Integer(), nullable=False),

        sa.ForeignKeyConstraint(
            ["posts_id"],
            ["posts.id"],
            ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["users_id"],
            ["users.id"],
            ondelete="CASCADE"
        ),

        sa.PrimaryKeyConstraint("posts_id", "users_id")
    )


def downgrade():
    op.drop_table("votes")
    op.drop_table("posts")
    op.drop_table("users")
