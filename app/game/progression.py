"""Ranks, stars, streaks and progression: what a finished match changes."""

from dataclasses import dataclass

# (name, stars needed to rank up). The top rank has no target.
RANKS = (
    ("Recruit", 3),
    ("Squire", 4),
    ("Knight-Captain", 5),
    ("Champion", None),
)
TOP_RANK = len(RANKS) - 1
STREAK_BONUS_EVERY = 3  # every third win in a row earns a bonus star


def rank_name(rank: int) -> str:
    rank = max(0, min(rank, TOP_RANK))
    return RANKS[rank][0]


def stars_needed(rank: int):
    """Stars needed to leave `rank`, or None at the top rank."""
    rank = max(0, min(rank, TOP_RANK))
    return RANKS[rank][1]


@dataclass(frozen=True)
class Progress:
    rank: int = 0
    stars: int = 0
    streak: int = 0


@dataclass(frozen=True)
class Outcome:
    progress: Progress  # player's progress after the match
    stars_change: int   # net stars won or lost by this match (before rank-up reset)
    ranked_up: bool = False
    streak_bonus: bool = False


def apply_match_result(progress: Progress, won: bool) -> Outcome:
    rank, stars, streak = progress.rank, progress.stars, progress.streak
    streak_bonus = False

    if won:
        streak += 1
        stars_change = 1
        if streak % STREAK_BONUS_EVERY == 0:
            stars_change += 1
            streak_bonus = True
    else:
        streak = 0
        stars_change = -1 if stars > 0 else 0  # never drop below floor (0) of current rank
    stars += stars_change

    ranked_up = False
    need = stars_needed(rank)
    if need is not None and stars >= need:
        rank += 1
        stars = 0
        ranked_up = True

    return Outcome(
        progress=Progress(rank=rank, stars=stars, streak=streak),
        stars_change=stars_change,
        ranked_up=ranked_up,
        streak_bonus=streak_bonus,
    )
