# Two concepts compared

Both are variations of rock paper scissors against a computer opponent.
**Status: draft written with Claude on 2026-11-13. Jefferson to review and confirm the decision.**

| | Concept A: Five-Move Duel | Concept B: Pattern Reader |
|---|---|---|
| One-sentence pitch | Rock paper scissors with five moves instead of three, so ties are rarer and there is more to learn. | Classic three-move rock paper scissors against a computer that learns your habits and tries to predict you. |
| Who it is for | Players who know the classic game and want more variety | Players who like trying to outsmart an opponent |
| Core loop | Pick one of five moves → see who wins → next round, best of 7 | Pick one of three moves → see the computer's guess and the result → try to be less predictable, 20 rounds |
| Length of one session | About 1 minute | About 2 minutes |
| What gets saved as the "result" | Win/loss/tie count for the match, moves used | Win/loss/tie count, plus a "predictability" score (how often the computer guessed right) |
| What the dashboard shows | Match history, win rate, win rate per move | Match history, win rate, predictability over time, most-repeated habit |
| Similar games looked at | TODO: add to research/sources.md | TODO: add to research/sources.md |
| Riskiest or least certain part | Players have to memorize ten win rules; may feel like homework | The learning opponent may feel unfair, or be too easy to beat once understood |
| Fits the time available? | Yes: only the rules table changes | Yes, if the predictor stays simple (counting what the player did after their last move) |

## Decision
**Chosen concept (draft):** Concept B, Pattern Reader.

**Why:** The saved result and the dashboard are more interesting: predictability gives the player a number to improve that is not just win rate, which gives the dashboard a reason to exist. The rules need no explanation because everyone knows the three moves. The uncertain part (does a learning opponent feel fun?) doubles as the required creative experiment.

**What I am giving up by not choosing the other:** Concept A is simpler to build and has no risk of the opponent feeling unfair. Five moves could come back later as an optional mode.

**Evidence still needed:** look at two or three existing rock paper scissors games (including one with a learning opponent) and record them in research/sources.md. NOT DONE.
