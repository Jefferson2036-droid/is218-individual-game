"""Database tables."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(40))
    rank: Mapped[int] = mapped_column(Integer, default=0)
    stars: Mapped[int] = mapped_column(Integer, default=0)
    coins: Mapped[int] = mapped_column(Integer, default=0)
    streak: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class Match(Base):
    """A match. Finished matches (status "won" or "lost") are the saved results."""

    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(12), default="active", index=True)  # active | won | lost | abandoned
    you: Mapped[int] = mapped_column(Integer, default=0)   # rounds the player has won
    cpu: Mapped[int] = mapped_column(Integer, default=0)   # rounds the computer has won
    rounds: Mapped[list] = mapped_column(JSON, default=list)
    rank_at_start: Mapped[int] = mapped_column(Integer, default=0)
    stars_change: Mapped[int] = mapped_column(Integer, default=0)
    coins_earned: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class Unlock(Base):
    """Gear a player owns."""

    __tablename__ = "unlocks"
    __table_args__ = (UniqueConstraint("user_id", "item_id", name="uq_unlock_user_item"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    item_id: Mapped[str] = mapped_column(String(40))
    unlocked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class Loadout(Base):
    """The gear a player has equipped on each fighter (used by the armory, a later step)."""

    __tablename__ = "loadouts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    fighter: Mapped[str] = mapped_column(String(12), primary_key=True)
    item_id: Mapped[str] = mapped_column(String(40))
