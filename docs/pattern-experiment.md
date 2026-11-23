# Code pattern experiment: Strategy for the computer opponent

Chosen 2026-11-23.

- **Problem:** each rank's computer plays differently (Recruit: random; Squire: win-stay/lose-shift; Knight-Captain: predicts from this match; Champion: uses all your past matches). See game-design.md.
- **Simple design (baseline):** one `computer_move(rank, history)` function with an if/else per rank (preserved in `app/game/opponent_baseline.py`).
- **Pattern design:** a Strategy class per behavior (`RandomStrategy`, `WinStayLoseShiftStrategy`, `PredictorStrategy`, `ChampionStrategy`) sharing one `choose(...)` method; the match asks a small factory `get_strategy(rank)` for the strategy that fits the player's rank (implemented in `app/game/opponent.py`).
- **Compare on:** how easy each is to test on its own, how much changes when a new rank or behavior is added, and how easy each is to read and explain.
- **Expected:** Strategy is easier to test and extend; the if/else version is shorter while there are only four ranks.

## Result

- **Lines of code:**
  - Procedural baseline (`app/game/opponent_baseline.py`): 66 lines.
  - Strategy pattern implementation (`app/game/opponent.py`): 132 lines.
  - The baseline is roughly half the lines of code because all dispatch logic and branching are collapsed into a single tuple index and an `if/elif/else` cascade.
- **How tests changed:**
  - Under the procedural baseline, testing a single rank's prediction required calling the monolithic `choose(rank, match_rounds, history, rng)` with dummy arguments for parameters that the rank didn't even use (e.g., passing match rounds and history to Recruit).
  - Under the Strategy pattern, each strategy class (`RandomStrategy`, `WinStayLoseShiftStrategy`, `PredictorStrategy`, `ChampionStrategy`) is instantiated and unit-tested in isolation directly (`strategy.choose(...)`).
  - The factory `get_strategy(rank)` is verified independently, confirming rank mapping and bounds clamping without re-testing the core AI algorithms.
- **What was easier / harder:**
  - *Easier:* Adding a new difficulty level or tuning an existing AI behavior (e.g. tweaking `PredictorStrategy` heuristics) touches only that specific class, without any risk of breaking Recruit or Champion logic. Unit tests are cleaner and easier to reason about.
  - *Harder:* The Strategy pattern requires more boilerplate classes (`OpponentStrategy` ABC, 4 subclasses, and a factory function) and increases code size from 66 lines to 132 lines. For a small game with only four ranks, the overhead is visible, but the architectural clarity and modular testability are significantly improved.
