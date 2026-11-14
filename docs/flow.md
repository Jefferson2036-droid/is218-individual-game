# Required flow: account → game → saved result → dashboard → account update

| Step | What the user does | What the system does | Data touched |
|---|---|---|---|
| 1. Account | Registers or logs in | Validates input, hashes password, issues a session/token | `users` |
| 2. Game | Plays one round | Runs the game in the browser | (none until the round ends) |
| 3. Saved result | Finishes the round | Stores the result for that user | `results` |
| 4. Dashboard | Opens the dashboard | Reads that user's results and shows history/stats | `results` |
| 5. Account update | Changes display name, password or preferences | Validates and saves the change | `users` |

TODO: replace "one round" and "result" with what they mean for the chosen concept
(for example score, time, ending reached).
