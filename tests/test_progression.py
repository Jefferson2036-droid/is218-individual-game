from app.game.items import ITEMS, get_item, items_unlocked_at
from app.game.progression import (
    RANKS, RANKUP_COINS, TOP_RANK, WIN_COINS, Progress, apply_match_result, rank_name, stars_needed,
)
from app.game.rules import FIGHTERS


def test_a_win_gives_a_star_and_coins():
    out = apply_match_result(Progress(), won=True)
    assert out.progress == Progress(rank=0, stars=1, coins=WIN_COINS, streak=1)
    assert (out.stars_change, out.coins_earned, out.ranked_up, out.streak_bonus) == (1, WIN_COINS, False, False)
    assert out.unlocked_item_ids == []


def test_a_loss_takes_a_star_and_resets_the_streak():
    out = apply_match_result(Progress(rank=1, stars=2, coins=50, streak=2), won=False)
    assert out.progress == Progress(rank=1, stars=1, coins=50, streak=0)
    assert (out.stars_change, out.coins_earned) == (-1, 0)


def test_a_loss_never_drops_below_the_bottom_of_the_rank():
    out = apply_match_result(Progress(rank=2, stars=0, coins=5, streak=0), won=False)
    assert out.progress == Progress(rank=2, stars=0, coins=5, streak=0)
    assert out.stars_change == 0


def test_third_win_in_a_row_earns_a_bonus_star():
    out = apply_match_result(Progress(rank=1, stars=0, coins=0, streak=2), won=True)
    assert out.streak_bonus
    assert out.stars_change == 2
    assert out.progress.stars == 2 and out.progress.streak == 3


def test_filling_the_stars_ranks_up_and_unlocks_gear():
    out = apply_match_result(Progress(rank=0, stars=2, coins=20, streak=0), won=True)
    assert out.ranked_up
    assert out.progress == Progress(rank=1, stars=0, coins=20 + WIN_COINS + RANKUP_COINS, streak=1)
    assert out.unlocked_item_ids == ["gold-armor"]


def test_three_straight_wins_from_a_new_account_reach_squire():
    progress = Progress()
    for _ in range(2):
        progress = apply_match_result(progress, True).progress
    out = apply_match_result(progress, True)
    assert out.ranked_up and out.streak_bonus
    assert out.progress.rank == 1 and out.progress.stars == 0


def test_champion_keeps_collecting_stars_as_victory_points():
    progress = Progress(rank=TOP_RANK, stars=7, coins=0, streak=0)
    out = apply_match_result(progress, True)
    assert not out.ranked_up
    assert out.progress.rank == TOP_RANK and out.progress.stars == 8


def test_climbing_all_the_way_unlocks_one_item_per_rank():
    progress, unlocked = Progress(), []
    for _ in range(60):
        out = apply_match_result(progress, True)
        progress = out.progress
        unlocked += out.unlocked_item_ids
    assert progress.rank == TOP_RANK
    assert unlocked == ["gold-armor", "flame-bow", "storm-staff"]


def test_rank_table():
    assert [name for name, _ in RANKS] == ["Recruit", "Squire", "Knight-Captain", "Champion"]
    assert rank_name(0) == "Recruit" and stars_needed(0) == 3
    assert stars_needed(TOP_RANK) is None


def test_item_catalog_is_consistent():
    ids = [item["id"] for item in ITEMS]
    assert len(ids) == len(set(ids))
    for item in ITEMS:
        assert item["fighter"] in FIGHTERS
        # every item is earned exactly one way: by rank or by coins
        assert (item["unlock_rank"] is None) != (item["price"] is None)
    for rank in range(1, TOP_RANK + 1):
        assert len(items_unlocked_at(rank)) == 1
    assert items_unlocked_at(0) == []
    assert get_item("gold-armor")["fighter"] == "knight"
    assert get_item("nope") is None
