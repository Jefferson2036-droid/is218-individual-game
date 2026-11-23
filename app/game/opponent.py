"""The computer opponent using the Strategy pattern.

Opponents get better at reading the player at each rank:
- Rank 0 (Recruit): RandomStrategy (picks at random)
- Rank 1 (Squire): WinStayLoseShiftStrategy (sometimes expects win-stay, lose-shift)
- Rank 2 (Knight-Captain): PredictorStrategy (predicts from transitions in this match)
- Rank 3 (Champion): ChampionStrategy (uses player history across earlier matches + this match)

Rounds are dicts with at least "pick" (the player's fighter) and "result".
"""

import random
from abc import ABC, abstractmethod

from .rules import FIGHTERS, counter


def predict_wsls(last):
    """Win-stay, lose-shift guess for the player's next pick."""
    if not last:
        return None
    if last.get("result") == "win":
        return last["pick"]
    if last.get("result") == "lose":
        return counter(last["pick"])
    return None


def predict_transitions(rounds):
    """The pick that most often followed the player's latest pick."""
    if not rounds or len(rounds) < 2:
        return None
    last = rounds[-1]["pick"]
    counts = {f: 0 for f in FIGHTERS}
    seen = 0
    for current, following in zip(rounds, rounds[1:]):
        if current["pick"] == last:
            counts[following["pick"]] += 1
            seen += 1
    if not seen:
        return None
    return max(FIGHTERS, key=lambda f: counts[f])


class OpponentStrategy(ABC):
    """Base class for computer opponent strategies."""

    prediction_chance: float = 0.0

    @abstractmethod
    def predict(self, match_rounds, history=None) -> str | None:
        """Predict the player's next pick based on history."""
        raise NotImplementedError

    def choose(self, match_rounds=None, history=None, rng=None) -> tuple[str, str | None]:
        """Pick the computer's fighter.

        Returns (fighter, predicted) where `predicted` is the player pick the
        computer was anticipating, or None if it picked at random.
        """
        match_rounds = list(match_rounds or [])
        history = list(history or [])
        if rng is None:
            rng = random.Random()

        predicted = None
        if self.prediction_chance > 0 and rng.random() < self.prediction_chance:
            predicted = self.predict(match_rounds, history)

        if predicted:
            return counter(predicted), predicted

        return FIGHTERS[rng.randrange(len(FIGHTERS))], None


class RandomStrategy(OpponentStrategy):
    """Recruit: picks a fighter completely at random."""

    prediction_chance = 0.0

    def predict(self, match_rounds, history=None) -> str | None:
        return None


class WinStayLoseShiftStrategy(OpponentStrategy):
    """Squire: sometimes expects win-stay, lose-shift."""

    prediction_chance = 0.5

    def predict(self, match_rounds, history=None) -> str | None:
        last = match_rounds[-1] if match_rounds else None
        return predict_wsls(last)


class PredictorStrategy(OpponentStrategy):
    """Knight-Captain: predicts from transitions within the current match."""

    prediction_chance = 0.6

    def predict(self, match_rounds, history=None) -> str | None:
        last = match_rounds[-1] if match_rounds else None
        return predict_transitions(match_rounds) or predict_wsls(last)


class ChampionStrategy(OpponentStrategy):
    """Champion: uses transitions across earlier matches and the current match."""

    prediction_chance = 0.7

    def predict(self, match_rounds, history=None) -> str | None:
        last = match_rounds[-1] if match_rounds else None
        combined = list(history or []) + list(match_rounds or [])
        return predict_transitions(combined) or predict_wsls(last)


STRATEGIES: tuple[type[OpponentStrategy], ...] = (
    RandomStrategy,
    WinStayLoseShiftStrategy,
    PredictorStrategy,
    ChampionStrategy,
)


def get_strategy(rank: int) -> OpponentStrategy:
    """Return the opponent strategy instance for the given rank."""
    clamped_rank = max(0, min(rank, len(STRATEGIES) - 1))
    return STRATEGIES[clamped_rank]()


def choose(rank: int, match_rounds, history=None, rng=None) -> tuple[str, str | None]:
    """Compatibility wrapper dispatching to the rank's strategy."""
    return get_strategy(rank).choose(match_rounds, history, rng)
