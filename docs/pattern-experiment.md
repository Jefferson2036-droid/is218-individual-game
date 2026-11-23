# Code pattern experiment: Strategy for the computer opponent

Chosen 2026-11-23.

- **Problem:** each rank's computer plays differently (Recruit: random; Squire: win-stay/lose-shift; Knight-Captain: predicts from this match; Champion: uses all your past matches). See game-design.md.
- **Simple design (baseline):** one `computer_move(rank, history)` function with an if/else per rank.
- **Pattern design:** a Strategy class per behavior (`RandomStrategy`, `WinStayLoseShiftStrategy`, `PredictorStrategy`, `ChampionStrategy`) sharing one `choose(history)` method; the match asks a small factory for the strategy that fits the player's rank.
- **Compare on:** how easy each is to test on its own, how much changes when a new rank or behavior is added, and how easy each is to read and explain.
- **Expected:** Strategy is easier to test and extend; the if/else version is shorter while there are only four ranks.
- **Result:** NOT RUN.
