import random

from app.game.opponent import (
    STRATEGIES,
    ChampionStrategy,
    PredictorStrategy,
    RandomStrategy,
    WinStayLoseShiftStrategy,
    choose,
    get_strategy,
    predict_transitions,
    predict_wsls,
)
from app.game.rules import FIGHTERS, counter


class FixedRng:
    """Stands in for random.Random so computer picks are deterministic in tests."""

    def __init__(self, index=0, roll=0.99):
        self.index = index
        self.roll = roll

    def random(self):
        return self.roll

    def randrange(self, n):
        return self.index % n


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
    assert predict_transitions([r("archer"), r("knight")]) is None


def test_factory_maps_each_rank_to_the_right_strategy():
    assert isinstance(get_strategy(0), RandomStrategy)
    assert isinstance(get_strategy(1), WinStayLoseShiftStrategy)
    assert isinstance(get_strategy(2), PredictorStrategy)
    assert isinstance(get_strategy(3), ChampionStrategy)
    # Clamping
    assert isinstance(get_strategy(-1), RandomStrategy)
    assert isinstance(get_strategy(99), ChampionStrategy)


def test_random_strategy_never_predicts():
    strat = RandomStrategy()
    always_predict = FixedRng(index=1, roll=0.0)
    pick, predicted = strat.choose([r("knight", "win")], [], always_predict)
    assert predicted is None
    assert pick == "archer"


def test_wsls_strategy_counters_repeated_winning_pick():
    strat = WinStayLoseShiftStrategy()
    pick, predicted = strat.choose([r("knight", "win")], [], FixedRng(roll=0.0))
    assert predicted == "knight"
    assert pick == counter("knight") == "wizard"


def test_wsls_strategy_picks_randomly_when_roll_exceeds_chance():
    strat = WinStayLoseShiftStrategy()
    pick, predicted = strat.choose([r("knight", "win")], [], FixedRng(index=2, roll=0.99))
    assert (pick, predicted) == ("wizard", None)


def test_wsls_strategy_falls_back_on_first_round():
    strat = WinStayLoseShiftStrategy()
    pick, predicted = strat.choose([], [], FixedRng(index=0, roll=0.0))
    assert (pick, predicted) == ("knight", None)


def test_predictor_strategy_uses_habits_from_this_match():
    strat = PredictorStrategy()
    rounds = [r("archer"), r("knight"), r("archer"), r("knight"), r("archer")]
    pick, predicted = strat.choose(rounds, [], FixedRng(roll=0.0))
    assert predicted == "knight"
    assert pick == "wizard"


def test_predictor_strategy_ignores_earlier_matches():
    strat = PredictorStrategy()
    history = [r("wizard"), r("archer"), r("wizard"), r("archer")]
    pick, predicted = strat.choose([r("wizard", "tie")], history, FixedRng(index=1, roll=0.0))
    assert (pick, predicted) == ("archer", None)


def test_champion_strategy_uses_earlier_matches():
    strat = ChampionStrategy()
    history = [r("wizard"), r("archer"), r("wizard"), r("archer")]
    pick, predicted = strat.choose([r("wizard", "tie")], history, FixedRng(roll=0.0))
    assert predicted == "archer"
    assert pick == "knight"


def test_all_strategies_return_valid_picks():
    rng = random.Random(42)
    rounds = [r("knight", "win"), r("archer", "lose")]
    for strat_cls in STRATEGIES:
        strat = strat_cls()
        for _ in range(50):
            pick, pred = strat.choose(rounds, rounds, rng)
            assert pick in FIGHTERS
            assert pred is None or pred in FIGHTERS


def test_choose_compatibility_wrapper():
    pick, pred = choose(0, [], [], FixedRng(index=0))
    assert pick == "knight"
    assert pred is None
