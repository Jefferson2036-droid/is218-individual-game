"""Dashboard: the player's progress, stats, match history and gear."""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..deps import get_current_user, get_db
from ..models import Match, User
from ..views import gear_out, history_out, user_out

router = APIRouter(prefix="/api", tags=["dashboard"])

RECENT_MATCHES = 10


def _count(db: Session, user_id: int, status: str) -> int:
    return db.scalar(select(func.count()).select_from(Match).where(Match.user_id == user_id, Match.status == status)) or 0


@router.get("/dashboard")
def dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    wins = _count(db, user.id, "won")
    losses = _count(db, user.id, "lost")
    played = wins + losses
    recent = db.scalars(
        select(Match)
        .where(Match.user_id == user.id, Match.status.in_(("won", "lost")))
        .order_by(Match.id.desc())
        .limit(RECENT_MATCHES)
    ).all()
    return {
        "user": user_out(user),
        "stats": {
            "matches_played": played,
            "wins": wins,
            "losses": losses,
            "win_rate": round(wins / played, 3) if played else None,
            "streak": user.streak,
        },
        "recent_matches": [history_out(match) for match in recent],
        "gear": gear_out(db, user),
    }
