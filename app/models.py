"""SQLAlchemy database models for Arena Climb."""

from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(40), nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)
    stars = db.Column(db.Integer, default=0, nullable=False)
    streak = db.Column(db.Integer, default=0, nullable=False)
    auth_version = db.Column(db.Integer, default=1, nullable=False)
    experiment_version = db.Column(db.String(1), default="A", nullable=False)  # 'A' or 'B'
    created_at = db.Column(db.DateTime(timezone=True), default=now_utc, nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class LoginSession(db.Model):
    __tablename__ = "login_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    auth_version = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=now_utc, nullable=False)


class Match(db.Model):
    __tablename__ = "matches"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = db.Column(db.String(16), default="in_progress", nullable=False, index=True)  # in_progress | won | lost
    you = db.Column(db.Integer, default=0, nullable=False)
    cpu = db.Column(db.Integer, default=0, nullable=False)
    rank_at_start = db.Column(db.Integer, default=0, nullable=False)
    stars_at_start = db.Column(db.Integer, default=0, nullable=False)
    rank_after = db.Column(db.Integer, nullable=True)
    stars_after = db.Column(db.Integer, nullable=True)
    stars_change = db.Column(db.Integer, default=0, nullable=False)
    started_at = db.Column(db.DateTime(timezone=True), default=now_utc, nullable=False)
    finished_at = db.Column(db.DateTime(timezone=True), nullable=True)

    rounds = db.relationship("Round", backref="match", cascade="all, delete-orphan", order_by="Round.n")


class Round(db.Model):
    __tablename__ = "rounds"

    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    n = db.Column(db.Integer, nullable=False)
    player_pick = db.Column(db.String(12), nullable=False)
    cpu_pick = db.Column(db.String(12), nullable=False)
    outcome = db.Column(db.String(8), nullable=False)  # win | lose | tie
    predicted = db.Column(db.String(12), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=now_utc, nullable=False)
