"""Knight / Archer / Wizard rules."""

FIGHTERS = ("knight", "archer", "wizard")

# Each fighter beats exactly one other.
BEATS = {"knight": "archer", "archer": "wizard", "wizard": "knight"}

ROUNDS_TO_WIN = 3  # best of 5


def is_fighter(name) -> bool:
    return name in FIGHTERS


def counter(fighter: str) -> str:
    """The fighter that beats `fighter`."""
    return next(f for f in FIGHTERS if BEATS[f] == fighter)


def resolve(player: str, cpu: str) -> str:
    """Result of one round from the player's side: "win", "lose" or "tie"."""
    if not is_fighter(player) or not is_fighter(cpu):
        raise ValueError("unknown fighter")
    if player == cpu:
        return "tie"
    return "win" if BEATS[player] == cpu else "lose"
