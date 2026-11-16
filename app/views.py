"""Turn database rows into the JSON the API returns."""

from .game.items import get_item
from .game.progression import rank_name, stars_needed
from .game.rules import ROUNDS_TO_WIN
from .models import Match, User


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
