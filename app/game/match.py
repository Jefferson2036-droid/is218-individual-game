"""One best-of-5 match against the computer."""

from dataclasses import dataclass, field

from .opponent import get_strategy
from .rules import ROUNDS_TO_WIN, is_fighter, resolve


@dataclass
class MatchState:
    you: int = 0
    cpu: int = 0
    rounds: list = field(default_factory=list)

    @property
    def over(self) -> bool:
        return self.you >= ROUNDS_TO_WIN or self.cpu >= ROUNDS_TO_WIN

    @property
    def won(self) -> bool:
        return self.you >= ROUNDS_TO_WIN


def play_round(state: MatchState, pick: str, rank: int, history, rng) -> dict:
    """Play one round and update `state`. Returns the round that was played."""
    if not is_fighter(pick):
        raise ValueError("unknown fighter: %r" % (pick,))
    if state.over:
        raise ValueError("match is already over")
    strategy = get_strategy(rank)
    cpu_pick, predicted = strategy.choose(state.rounds, history, rng)
    result = resolve(pick, cpu_pick)
    played = {"pick": pick, "cpu": cpu_pick, "result": result, "predicted": predicted}
    state.rounds = state.rounds + [played]
    if result == "win":
        state.you += 1
    elif result == "lose":
        state.cpu += 1
    return played
