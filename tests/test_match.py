import random

import pytest

from app.game.match import MatchState, play_round
from tests.conftest import FixedRng


def test_first_to_three_wins_ends_the_match():
    state = MatchState()
    rng = FixedRng(index=0)                 # computer always sends Knight
    for expected in (1, 2, 3):
        played = play_round(state, "wizard", 0, [], rng)
        assert played == {"pick": "wizard", "cpu": "knight", "result": "win", "predicted": None}
        assert state.you == expected
    assert state.over and state.won
    assert len(state.rounds) == 3


def test_losing_three_rounds_loses_the_match():
    state = MatchState()
    for _ in range(3):
        play_round(state, "archer", 0, [], FixedRng(index=0))
    assert state.over and not state.won
    assert (state.you, state.cpu) == (0, 3)


def test_ties_are_recorded_but_do_not_score():
    state = MatchState()
    played = play_round(state, "knight", 0, [], FixedRng(index=0))
    assert played["result"] == "tie"
    assert (state.you, state.cpu) == (0, 0)
    assert len(state.rounds) == 1 and not state.over


def test_cannot_play_after_the_match_is_over():
    state = MatchState(you=3, cpu=1)
    with pytest.raises(ValueError):
        play_round(state, "knight", 0, [], FixedRng())


def test_rejects_unknown_fighter_without_changing_the_match():
    state = MatchState()
    with pytest.raises(ValueError):
        play_round(state, "dragon", 0, [], FixedRng())
    assert state.rounds == [] and (state.you, state.cpu) == (0, 0)


def test_every_match_ends_with_exactly_one_side_on_three():
    rng = random.Random(11)
    for i in range(400):
        state = MatchState()
        while not state.over:
            play_round(state, rng.choice(("knight", "archer", "wizard")), i % 4, [], rng)
        assert max(state.you, state.cpu) == 3 and min(state.you, state.cpu) < 3
        assert sum(r["result"] == "win" for r in state.rounds) == state.you
        assert sum(r["result"] == "lose" for r in state.rounds) == state.cpu
