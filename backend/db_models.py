from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserRow(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    habits: Mapped[list["HabitRow"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    completions: Mapped[list["CompletionRow"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class HabitRow(Base):
    __tablename__ = "habits"
    __table_args__ = (Index("ix_habits_user_created", "user_id", "created_at"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    color: Mapped[str] = mapped_column(String(7), nullable=False, default="#007AFF")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    user: Mapped[UserRow] = relationship(back_populates="habits")
    completions: Mapped[list["CompletionRow"]] = relationship(back_populates="habit", cascade="all, delete-orphan")


class CompletionRow(Base):
    __tablename__ = "completions"
    __table_args__ = (
        UniqueConstraint("user_id", "habit_id", "completion_date", name="uq_completion_user_habit_date"),
        Index("ix_completions_user_date", "user_id", "completion_date"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    habit_id: Mapped[str] = mapped_column(String(36), ForeignKey("habits.id", ondelete="CASCADE"), nullable=False, index=True)
    completion_date: Mapped[date] = mapped_column(Date, nullable=False)
    user: Mapped[UserRow] = relationship(back_populates="completions")
    habit: Mapped[HabitRow] = relationship(back_populates="completions")