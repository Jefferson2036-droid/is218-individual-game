import pytest

from app.game.rules import BEATS, FIGHTERS, counter, resolve


def test_each_fighter_beats_exactly_one_and_loses_to_exactly_one():
    assert set(BEATS) == set(FIGHTERS)
    assert sorted(BEATS.values()) == sorted(FIGHTERS)
    for fighter in FIGHTERS:
        assert BEATS[fighter] != fighter


@pytest.mark.parametrize(
    "player, cpu, expected",
    [
        ("knight", "archer", "win"),    # Knight charges down Archer
        ("archer", "wizard", "win"),    # Archer shoots Wizard
        ("wizard", "knight", "win"),    # Wizard's magic beats Knight
        ("archer", "knight", "lose"),
        ("wizard", "archer", "lose"),
        ("knight", "wizard", "lose"),
        ("knight", "knight", "tie"),
        ("archer", "archer", "tie"),
        ("wizard", "wizard", "tie"),
    ],
)
def test_resolve(player, cpu, expected):
    assert resolve(player, cpu) == expected


def test_resolve_rejects_unknown_fighters():
    with pytest.raises(ValueError):
        resolve("rock", "knight")
    with pytest.raises(ValueError):
        resolve("knight", "paper")


def test_counter_is_the_fighter_that_wins():
    for fighter in FIGHTERS:
        assert resolve(counter(fighter), fighter) == "win"
