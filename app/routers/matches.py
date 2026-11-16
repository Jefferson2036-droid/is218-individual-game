"""Matches. The server picks for the computer and decides every round,
so a player cannot fake wins from the browser."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..deps import get_current_user, get_db, get_rng
from ..game.match import MatchState, play_round
from ..game.progression import TOP_RANK, Progress, apply_match_result, rank_name
from ..models import Match, Unlock, User, now_utc
from ..schemas import PickIn
from ..views import item_out, match_out, user_out

router = APIRouter(prefix="/api/matches", tags=["matches"])

HISTORY_MATCHES = 20  # how many past matches the Champion-rank computer remembers


def _history(db: Session, user_id: int) -> list:
    """Rounds (oldest first, ties left out) from the player's recent finished matches."""
    recent = db.scalars(
        select(Match)
        .where(Match.user_id == user_id, Match.status.in_(("won", "lost")))
        .order_by(Match.id.desc())
        .limit(HISTORY_MATCHES)
    ).all()
    rounds = []
    for match in reversed(recent):
        rounds.extend(r for r in (match.rounds or []) if r.get("result") != "tie")
    return rounds


def _own_match(db: Session, match_id: int, user: User, lock: bool = False) -> Match:
    query = select(Match).where(Match.id == match_id, Match.user_id == user.id)
    if lock:
        query = query.with_for_update()
    match = db.scalar(query)
    if match is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Match not found")
    return match


@router.post("", status_code=status.HTTP_201_CREATED)
def start_match(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # A match the player walked away from is not saved as a result and changes nothing.
    unfinished = db.scalars(select(Match).where(Match.user_id == user.id, Match.status == "active")).all()
    for old in unfinished:
        old.status = "abandoned"
        old.finished_at = now_utc()
    match = Match(user_id=user.id, rank_at_start=user.rank, rounds=[])
    db.add(match)
    db.commit()
    db.refresh(match)
    return {"match": match_out(match)}


@router.get("/{match_id}")
def get_match(match_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"match": match_out(_own_match(db, match_id, user))}


@router.post("/{match_id}/rounds")
def play(
    match_id: int,
    data: PickIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    rng=Depends(get_rng),
):
    match = _own_match(db, match_id, user, lock=True)
    if match.status != "active":
        raise HTTPException(status.HTTP_409_CONFLICT, "This match is already finished")

    state = MatchState(you=match.you, cpu=match.cpu, rounds=list(match.rounds or []))
    history = _history(db, user.id) if match.rank_at_start >= TOP_RANK else []
    played = play_round(state, data.pick, match.rank_at_start, history, rng)
    match.you, match.cpu, match.rounds = state.you, state.cpu, state.rounds

    outcome_json = None
    if state.over:
        outcome = apply_match_result(
            Progress(rank=user.rank, stars=user.stars, coins=user.coins, streak=user.streak), state.won
        )
        new = outcome.progress
        user.rank, user.stars, user.coins, user.streak = new.rank, new.stars, new.coins, new.streak
        match.status = "won" if state.won else "lost"
        match.finished_at = now_utc()
        match.stars_change = outcome.stars_change
        match.coins_earned = outcome.coins_earned

        owned = set(db.scalars(select(Unlock.item_id).where(Unlock.user_id == user.id)).all())
        for item_id in outcome.unlocked_item_ids:
            if item_id not in owned:
                db.add(Unlock(user_id=user.id, item_id=item_id))

        outcome_json = {
            "won": state.won,
            "stars_change": outcome.stars_change,
            "coins_earned": outcome.coins_earned,
            "streak_bonus": outcome.streak_bonus,
            "ranked_up": outcome.ranked_up,
            "new_rank_name": rank_name(new.rank) if outcome.ranked_up else None,
            "unlocked_items": [item_out(i) for i in outcome.unlocked_item_ids],
        }

    db.commit()
    return {"round": played, "match": match_out(match), "outcome": outcome_json, "user": user_out(user)}
