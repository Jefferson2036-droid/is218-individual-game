from app.game.progression import (
    RANKS, TOP_RANK, Progress, apply_match_result, rank_name, stars_needed,
)


def test_a_win_gives_a_star_and_increments_streak():
    out = apply_match_result(Progress(), won=True)
    assert out.progress == Progress(rank=0, stars=1, streak=1)
    assert (out.stars_change, out.ranked_up, out.streak_bonus) == (1, False, False)


def test_a_loss_takes_a_star_and_resets_the_streak():
    out = apply_match_result(Progress(rank=1, stars=2, streak=2), won=False)
    assert out.progress == Progress(rank=1, stars=1, streak=0)
    assert out.stars_change == -1


def test_a_loss_never_drops_below_the_bottom_of_the_rank():
    out = apply_match_result(Progress(rank=2, stars=0, streak=0), won=False)
    assert out.progress == Progress(rank=2, stars=0, streak=0)
    assert out.stars_change == 0


def test_third_win_in_a_row_earns_a_bonus_star():
    out = apply_match_result(Progress(rank=1, stars=0, streak=2), won=True)
    assert out.streak_bonus
    assert out.stars_change == 2
    assert out.progress.stars == 2 and out.progress.streak == 3


def test_filling_the_stars_ranks_up():
    out = apply_match_result(Progress(rank=0, stars=2, streak=0), won=True)
    assert out.ranked_up
    assert out.progress == Progress(rank=1, stars=0, streak=1)


def test_three_straight_wins_from_a_new_account_reach_squire():
    # win 1: stars=1, streak=1
    # win 2: stars=2, streak=2
    # win 3: streak bonus gives +2 stars -> stars=4 -> ranks up to Squire (stars reset to 0)
    progress = Progress()
    for _ in range(2):
        progress = apply_match_result(progress, True).progress
    out = apply_match_result(progress, True)
    assert out.ranked_up and out.streak_bonus
    assert out.progress.rank == 1 and out.progress.stars == 0


def test_champion_keeps_collecting_stars_as_victory_points():
    progress = Progress(rank=TOP_RANK, stars=7, streak=0)
    out = apply_match_result(progress, True)
    assert not out.ranked_up
    assert out.progress.rank == TOP_RANK and out.progress.stars == 8


def test_rank_table():
    assert [name for name, _ in RANKS] == ["Recruit", "Squire", "Knight-Captain", "Champion"]
    assert rank_name(0) == "Recruit" and stars_needed(0) == 3
    assert rank_name(1) == "Squire" and stars_needed(1) == 4
    assert rank_name(2) == "Knight-Captain" and stars_needed(2) == 5
    assert stars_needed(TOP_RANK) is None
