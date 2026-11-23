# Required flow: account → match → saved result → dashboard → account update

Updated 2026-11-23 for the Flask stack and narrowed promise.

| Step | What the player does | What the server does | Data touched |
|---|---|---|---|
| 1. Account | Signs up, signs in or signs out | Validates input, hashes the password with Werkzeug, creates or ends a server-side login session (Flask-Login) | `users`, `login_sessions` |
| 2. Match | Plays best-of-5, picking Knight, Archer or Wizard each round | Validates the pick, gets the computer's pick from the rank's strategy, decides the round, keeps the match in progress | `matches` (in progress) |
| 3. Saved result | Finishes the match | Marks the match finished; saves win/loss, round score, rank and stars before/after; updates the player's stars and rank | `matches`, `users` |
| 4. Dashboard | Opens the dashboard | Shows only this player's progress, totals, streak and last 10 matches; empty state if none | `matches`, `users` (read) |
| 5. Account update | Changes display name or password | Validates; for a password change checks the current password, re-hashes, and revokes other login sessions | `users`, `login_sessions` |

An abandoned match is never marked finished, so it is not counted and changes no stars.
