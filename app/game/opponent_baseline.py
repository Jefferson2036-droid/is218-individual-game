"""The computer opponent. It gets better at reading the player at each rank.

Rank 0 (Recruit): random.
Rank 1 (Squire): sometimes expects "win-stay, lose-shift" (repeat a winning
    pick; after a loss, switch to the fighter that just beat you).
Rank 2 (Knight-Captain): sometimes predicts from what the player usually
    picks after their previous pick, within this match.
Rank 3 (Champion): the same, using the player's earlier matches too.

Rounds are dicts with at least "pick" (the player's fighter) and "result".
`rng` is a random.Random (or anything with random() and randrange()).
"""

from .rules import FIGHTERS, counter

# How often each rank tries to predict instead of picking at random.
PREDICTION_CHANCE = (0.0, 0.5, 0.6, 0.7)


def predict_wsls(last):
    """Win-stay, lose-shift guess for the player's next pick."""
    if not last:
        return None
    if last["result"] == "win":
        return last["pick"]
    if last["result"] == "lose":
        return counter(last["pick"])
    return None


def predict_transitions(rounds):
    """The pick that most often followed the player's latest pick."""
    if len(rounds) < 2:
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


def choose(rank: int, match_rounds, history, rng):
    """Pick the computer's fighter.

    Returns (fighter, predicted) where `predicted` is the player pick the
    computer was expecting, or None if it picked at random.
    """
    rank = max(0, min(rank, len(PREDICTION_CHANCE) - 1))
    chance = PREDICTION_CHANCE[rank]
    predicted = None
    if chance > 0 and rng.random() < chance:
        last = match_rounds[-1] if match_rounds else None
        if rank == 1:
            predicted = predict_wsls(last)
        elif rank == 2:
            predicted = predict_transitions(match_rounds) or predict_wsls(last)
        else:
            predicted = predict_transitions(list(history) + list(match_rounds)) or predict_wsls(last)
    if predicted:
        return counter(predicted), predicted
    return FIGHTERS[rng.randrange(len(FIGHTERS))], None
