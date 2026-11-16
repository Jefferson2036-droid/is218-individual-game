"""Turn database rows into the JSON the API returns."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from .game.items import ITEMS, get_item
from .game.progression import rank_name, stars_needed
from .game.rules import FIGHTERS, ROUNDS_TO_WIN
from .models import Loadout, Match, Unlock, User


def user_out(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "rank": user.rank,
        "rank_name": rank_name(user.rank),
        "stars": user.stars,
        "stars_needed": stars_needed(user.rank),
        "coins": user.coins,
        "streak": user.streak,
    }


def match_out(match: Match) -> dict:
    return {
        "id": match.id,
        "status": match.status,
        "you": match.you,
        "cpu": match.cpu,
        "rounds_to_win": ROUNDS_TO_WIN,
        "rounds": list(match.rounds or []),
        "rank_at_start": match.rank_at_start,
        "stars_change": match.stars_change,
        "coins_earned": match.coins_earned,
    }


def item_out(item_id: str) -> dict:
    item = get_item(item_id)
    return {"id": item["id"], "fighter": item["fighter"], "name": item["name"], "color": item["color"]}


def history_out(match: Match) -> dict:
    """A finished match, as a row of the dashboard's match history."""
    return {
        "id": match.id,
        "won": match.status == "won",
        "you": match.you,
        "cpu": match.cpu,
        "rank_name": rank_name(match.rank_at_start),
        "stars_change": match.stars_change,
        "coins_earned": match.coins_earned,
        "finished_at": match.finished_at.isoformat() if match.finished_at else None,
    }


def gear_out(db: Session, user: User) -> dict:
    """Every item with whether this player owns it and has it equipped, plus their loadout."""
    owned = set(db.scalars(select(Unlock.item_id).where(Unlock.user_id == user.id)).all())
    equipped = {row.fighter: row.item_id for row in db.scalars(select(Loadout).where(Loadout.user_id == user.id)).all()}
    items = []
    for item in ITEMS:
        items.append({
            "id": item["id"],
            "fighter": item["fighter"],
            "name": item["name"],
            "color": item["color"],
            "unlock_rank": item["unlock_rank"],
            "unlock_rank_name": rank_name(item["unlock_rank"]) if item["unlock_rank"] is not None else None,
            "price": item["price"],
            "owned": item["id"] in owned,
            "equipped": equipped.get(item["fighter"]) == item["id"],
        })
    return {"items": items, "loadout": {fighter: equipped.get(fighter) for fighter in FIGHTERS}}
