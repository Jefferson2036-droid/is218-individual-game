import random

from app.game.opponent import choose, predict_transitions, predict_wsls
from app.game.rules import FIGHTERS, counter
from tests.conftest import FixedRng


def r(pick, result="win"):
    return {"pick": pick, "result": result}


def test_wsls_expects_a_winner_to_repeat():
    assert predict_wsls(r("knight", "win")) == "knight"


def test_wsls_expects_a_loser_to_switch_to_what_beat_them():
    assert predict_wsls(r("knight", "lose")) == "wizard"


def test_wsls_has_no_guess_after_a_tie_or_with_no_rounds():
    assert predict_wsls(r("knight", "tie")) is None
    assert predict_wsls(None) is None


def test_transitions_finds_the_usual_follow_up():
    rounds = [r("knight"), r("wizard"), r("knight"), r("wizard"), r("knight")]
    assert predict_transitions(rounds) == "wizard"


def test_transitions_needs_evidence():
    assert predict_transitions([]) is None
    assert predict_transitions([r("knight")]) is None
    assert predict_transitions([r("archer"), r("knight")]) is None  # knight never seen before


def test_recruit_never_predicts():
    always_predict = FixedRng(index=1, roll=0.0)
    pick, predicted = choose(0, [r("knight", "win")], [], always_predict)
    assert predicted is None
    assert pick == "archer"


def test_squire_counters_a_repeated_winning_pick():
    pick, predicted = choose(1, [r("knight", "win")], [], FixedRng(roll=0.0))
    assert predicted == "knight"
    assert pick == counter("knight") == "wizard"


def test_squire_picks_randomly_when_the_roll_says_so():
    pick, predicted = choose(1, [r("knight", "win")], [], FixedRng(index=2, roll=0.99))
    assert (pick, predicted) == ("wizard", None)


def test_squire_falls_back_to_random_on_the_first_round():
    pick, predicted = choose(1, [], [], FixedRng(index=0, roll=0.0))
    assert (pick, predicted) == ("knight", None)


def test_captain_uses_habits_from_this_match():
    rounds = [r("archer"), r("knight"), r("archer"), r("knight"), r("archer")]
    pick, predicted = choose(2, rounds, [], FixedRng(roll=0.0))
    assert predicted == "knight"
    assert pick == "wizard"


def test_champion_uses_earlier_matches():
    history = [r("wizard"), r("archer"), r("wizard"), r("archer")]
    pick, predicted = choose(3, [r("wizard", "tie")], history, FixedRng(roll=0.0))
    assert predicted == "archer"
    assert pick == "knight"


def test_captain_ignores_earlier_matches():
    history = [r("wizard"), r("archer"), r("wizard"), r("archer")]
    pick, predicted = choose(2, [r("wizard", "tie")], history, FixedRng(index=1, roll=0.0))
    assert (pick, predicted) == ("archer", None)


def test_always_returns_a_real_fighter_and_out_of_range_ranks_are_clamped():
    rng = random.Random(7)
    rounds = []
    for i in range(300):
        pick, predicted = choose(i % 6 - 1, rounds, rounds, rng)
        assert pick in FIGHTERS
        assert predicted is None or predicted in FIGHTERS
        rounds = rounds + [r(FIGHTERS[i % 3], ("win", "lose", "tie")[i % 3])]


def test_a_predictable_player_loses_more_at_higher_ranks():
    """Someone who always repeats a winning pick and shifts after a loss should do worse against Squire than Recruit."""
    from app.game.rules import resolve

    def win_rate(rank, seed):
        rng = random.Random(seed)
        rounds, wins, played = [], 0, 0
        for _ in range(3000):
            guess = predict_wsls(rounds[-1]) if rounds else None
            player = guess or "knight"                     # the player really does follow the pattern
            cpu, _ = choose(rank, rounds, [], rng)
            result = resolve(player, cpu)
            rounds = (rounds + [{"pick": player, "result": result}])[-30:]
            if result != "tie":
                played += 1
                wins += result == "win"
        return wins / played

    assert win_rate(0, 1) > 0.45
    assert win_rate(1, 1) < 0.35
