"""Ranks, stars, coins and streaks: what a finished match changes."""

from dataclasses import dataclass, field

from .items import items_unlocked_at

# (name, stars needed to rank up). The top rank has no target.
RANKS = (
    ("Recruit", 3),
    ("Squire", 4),
    ("Knight-Captain", 5),
    ("Champion", None),
)
TOP_RANK = len(RANKS) - 1

WIN_COINS = 10
RANKUP_COINS = 25
STREAK_BONUS_EVERY = 3  # every third win in a row earns a bonus star


def rank_name(rank: int) -> str:
    return RANKS[rank][0]


def stars_needed(rank: int):
    """Stars needed to leave `rank`, or None at the top rank."""
    return RANKS[rank][1]


@dataclass(frozen=True)
class Progress:
    rank: int = 0
    stars: int = 0
    coins: int = 0
    streak: int = 0


@dataclass(frozen=True)
class Outcome:
    progress: Progress          # the player's progress after the match
    stars_change: int           # stars won or lost by this match (before any rank-up reset)
    coins_earned: int
    ranked_up: bool = False
    streak_bonus: bool = False
    unlocked_item_ids: list = field(default_factory=list)


def apply_match_result(progress: Progress, won: bool) -> Outcome:
    rank, stars, coins, streak = progress.rank, progress.stars, progress.coins, progress.streak
    coins_earned = 0
    streak_bonus = False

    if won:
        streak += 1
        stars_change = 1
        coins_earned += WIN_COINS
        if streak % STREAK_BONUS_EVERY == 0:
            stars_change += 1
            streak_bonus = True
    else:
        streak = 0
        stars_change = -1 if stars > 0 else 0   # never drop below the bottom of the rank
    stars += stars_change

    ranked_up = False
    unlocked = []
    need = stars_needed(rank)
    if need is not None and stars >= need:
        rank += 1
        stars = 0
        coins_earned += RANKUP_COINS
        ranked_up = True
        unlocked = items_unlocked_at(rank)

    return Outcome(
        progress=Progress(rank=rank, stars=stars, coins=coins + coins_earned, streak=streak),
        stars_change=stars_change,
        coins_earned=coins_earned,
        ranked_up=ranked_up,
        streak_bonus=streak_bonus,
        unlocked_item_ids=unlocked,
    )
