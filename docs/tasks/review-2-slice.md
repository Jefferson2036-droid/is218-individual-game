# Task: Review 2 — First Working Slice (Arena Climb)

Read `AGENTS.md` first; its rules apply. This file says exactly what to build **now**. Anything not listed here waits for Review 3.

## Goal (from Canvas)
A player can **sign up / sign in → play one correct best-of-5 match → see the saved result and reopen it later → sign out**, with real tests and one design-pattern experiment.

## Work on a branch
1. Create a GitHub issue "Review 2: first working slice" and a branch `review-2-slice`.
2. Commit in small steps with clear messages. Open a pull request that closes the issue when done.

## Build steps
1. **Replace the FastAPI layer with Flask.** Remove `app/main.py`, `app/routers/`, `app/security.py`, `app/deps.py`, `app/schemas.py`, `app/views.py`, `app/static/` and the FastAPI-only tests. Keep `app/game/` (plain Python) and the Blender renders in `art/renders/`.
2. **Narrow the game core to the plan:** remove coins and items (`app/game/items.py`, coin fields in `progression.py`). Keep ranks, stars, floor rule and win streak as in `docs/game-design.md`.
3. **Strategy pattern experiment:** turn `app/game/opponent.py` into one class per behavior (`RandomStrategy`, `WinStayLoseShiftStrategy`, `PredictorStrategy`, `ChampionStrategy`) with `choose(history)`, plus a small factory by rank. Keep the old single-function version as `opponent_baseline.py` so both can be compared. Write the actual comparison (lines of code, how tests changed, what was easier/harder) in `docs/pattern-experiment.md` under "Result".
4. **Flask app** (`app/__init__.py` with `create_app(config)`): Flask-SQLAlchemy models `User`, `LoginSession`, `Match`, `Round` as in `docs/architecture.md`; config from environment (`.env`, never committed); SQLite by default, PostgreSQL via `DATABASE_URL`.
5. **Accounts:** sign up, sign in, sign out with Flask-Login, Werkzeug password hashing and Flask-WTF CSRF. Duplicate username and wrong password show clear errors. Each new account is randomly assigned experiment version `A` or `B` and keeps it.
6. **Play:** `POST /play/start` creates an in-progress match; `POST /play/<match_id>/pick` accepts only `{"pick": "knight"|"archer"|"wizard"}`, decides the round on the server, stores a `Round`, and finishes the match at 3 round wins (updating stars/rank). Any other input → 400 with a helpful message. Another user's match → 404.
7. **Saved result you can reopen:** `GET /results` lists the signed-in player's finished matches (newest first); `GET /results/<match_id>` shows one. A full dashboard and account maintenance are Review 3 — **not now**.
8. **Pages:** sign in / sign up, battle screen and result pop-up, matching `docs/mockups/` (colors, fonts, layout) and the animation rules in `AGENTS.md`. Version B shows the "N stars to <next rank>!" nudge; version A does not.

## Tests (predict expected results from the docs, not from the code)
- **Unit:** all 9 matchups; star/rank math including the floor rule; each strategy returns a valid pick; factory maps each rank to the right strategy.
- **Integration (Flask test client + SQLite):** sign up; duplicate username rejected; wrong password rejected; full match plays and is saved; saved result reopens after signing out and back in; abandoned match is not counted; a client-sent "result" field is ignored; another user cannot open my match (404); after sign-out, `/results` redirects to sign in.
- **Browser (Playwright, Chromium, 375 px wide):** sign up → play a match with keys 1/2/3 → see the result → open `/results` → sign out.
- Add `.github/workflows/tests.yml` that runs all tests on every push and pull request (Python 3.12, `pip install -r requirements-dev.txt`, `playwright install --with-deps chromium`, `pytest`). Do not touch `.github/workflows/jekyll-gh-pages.yml`.

## Definition of done
- [ ] All tests pass locally and in GitHub Actions; link the green run.
- [ ] `README.md` "Run it" section updated for Flask (venv, `flask --app app run`, tests).
- [ ] `docs/pattern-experiment.md` has a real "Result" section.
- [ ] `docs/project-record.md` has a new entry: Changed / Checked (with the actual test output summary and run link) / Next. Anything not run says NOT RUN.
- [ ] Pull request merged into `main`; issue closed.

## Out of scope for this slice
Dashboard, account maintenance (display name, password change), Docker changes, analytics, anything in `docs/backlog.md`.
