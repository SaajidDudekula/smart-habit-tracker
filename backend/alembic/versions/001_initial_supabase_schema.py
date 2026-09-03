"""Create users, habits, and completions tables.

Revision ID: 001_supabase
Revises:
"""

from alembic import op
import sqlalchemy as sa


revision = "001_supabase"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=60), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "habits",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("color", sa.String(length=7), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_habits_user_created", "habits", ["user_id", "created_at"], unique=False)
    op.create_table(
        "completions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("habit_id", sa.String(length=36), nullable=False),
        sa.Column("completion_date", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(["habit_id"], ["habits.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "habit_id", "completion_date", name="uq_completion_user_habit_date"),
    )
    op.create_index("ix_completions_habit_id", "completions", ["habit_id"], unique=False)
    op.create_index("ix_completions_user_date", "completions", ["user_id", "completion_date"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_completions_user_date", table_name="completions")
    op.drop_index("ix_completions_habit_id", table_name="completions")
    op.drop_table("completions")
    op.drop_index("ix_habits_user_created", table_name="habits")
    op.drop_table("habits")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")