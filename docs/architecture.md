# Architecture sketch

Updated 2026-11-23 for the Flask stack.

```
Phone/laptop browser (HTML + CSS + JS)
        │  forms + small JSON calls, session cookie
        ▼
Flask web layer  ── auth/      sign up, sign in, sign out, account update (Flask-Login)
                 ── play/      start match, submit pick → round result
                 ── dashboard/ this player's progress only
        │  calls plain Python (no Flask inside)
        ▼
Game core (app/game/)  rules · opponent strategies (Strategy pattern) · match · ranks/stars
        │
        ▼
Database (PostgreSQL; SQLite in tests)
   users           id, username, password_hash, display_name, rank, stars, auth_version
   login_sessions  id, user_id, auth_version, expires_at
   matches         id, user_id, status (in_progress/finished), result, score, rank/stars before & after
   rounds          match_id, n, player_pick, computer_pick, outcome
```

## Rules
- The browser only sends a pick. The server validates it, gets the computer's pick, decides the round and owns the match state.
- Every data query is filtered by the signed-in user's id, so one player cannot read or change another's records.
- The game core has no web code, so rules, strategies and rank math are unit-tested without a server.

## Decisions (2026-11-23)
- **In-progress match lives in a database row**, not the session cookie: a refresh does not lose it, and an abandoned match stays `in_progress` and is never counted.
- **A `rounds` table stores every pick.** It is the data the higher-rank opponents read (Squire: last round; Knight-Captain: this match; Champion: all past matches). Without it, Champion could only use the current match.
- **Password change** bumps `users.auth_version`; any login session with an older version is rejected, which signs out other devices.

Note: the opponent "learning" is not machine learning. The strategies count patterns in the `rounds` data (for example, what the player picks after a win) and play against the most likely pick, with some randomness kept at every rank.
