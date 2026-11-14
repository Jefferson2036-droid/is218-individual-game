# Required flow: account → game → saved result → dashboard → account update

For the chosen concept (Pattern Reader). One match = 20 rounds against the computer.

| Step | What the user does | What the system does | Data touched |
|---|---|---|---|
| 1. Account | Registers or logs in | Validates input, hashes password, issues a session/token | `users` |
| 2. Game | Plays a 20-round match, choosing rock, paper or scissors each round | Predicts the player's next move from their earlier moves, plays the counter, shows each round's result | (kept in the browser until the match ends) |
| 3. Saved result | Finishes the match | Stores wins, losses, ties and predictability score for that user | `results` |
| 4. Dashboard | Opens the dashboard | Reads that user's results; shows match history, win rate and predictability over time | `results` |
| 5. Account update | Changes display name or password | Validates and saves the change | `users` |

**Predictability score:** the percentage of rounds in a match where the computer's prediction of the player's move was correct.
