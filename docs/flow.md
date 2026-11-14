# Required flow: account → game → saved result → dashboard → account update

| Step | What the user does | What the system does | Data touched |
|---|---|---|---|
| 1. Account | Registers or logs in | Validates input, hashes the password, starts a session. New players start at Recruit with the starter look. | `users` |
| 2. Game | Plays a best-of-5 match, picking Knight, Archer or Wizard each round | Computer picks using its rank's strategy; each round's winner is shown; equipped gear is displayed on the fighters | `loadouts` (read) |
| 3. Saved result | Finishes the match | Saves the outcome, updates stars and rank, adds coins, unlocks an item on rank-up | `results`, `users`, `unlocks` |
| 4. Dashboard | Opens the dashboard | Shows rank and progress to the next rank, win rate, current streak, match history and gear collection | `results`, `users`, `unlocks` |
| 5. Account update | Equips unlocked gear, buys gear with coins, or changes display name or password | Validates and saves the change; new gear appears in the next match | `loadouts`, `unlocks`, `users` |

An unfinished match (player leaves mid-match) is not saved and does not change stars.
