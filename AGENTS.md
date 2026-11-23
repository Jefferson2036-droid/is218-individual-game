# AGENTS.md — instructions for coding agents

Arena Climb is an IS218 creative project: a Knight / Archer / Wizard rock-paper-scissors game where the player climbs ranks against a computer that gets harder as they win. Read the plan before writing code; the owner (Jefferson) makes the decisions.

## Current task
Work on **`docs/tasks/review-2-slice.md`** — it lists exactly what to build now and what to leave for later.

## Read first
1. `docs/dream-promise.md` – the Working Promise (what must work)
2. `docs/user-stories.md` – five stories with acceptance checks (the definition of done)
3. `docs/stack.md`, `docs/architecture.md`, `docs/flow.md` – how it is built
4. `docs/game-design.md` – rules, ranks, stars, opponent behavior per rank
5. `docs/frontend.md` and `docs/mockups/` – screens, design tokens, accessibility rules
6. `docs/experiment.md`, `docs/pattern-experiment.md`, `docs/checks.md`
7. `docs/backlog.md` – **do not build anything listed there**

## Hard rules
- Stack: Flask, Flask-Login, Flask-WTF (CSRF), Werkzeug password hashing, SQLAlchemy, PostgreSQL via Docker Compose, SQLite in tests. Do not write custom password hashing or token code.
- Server-rendered Jinja templates; JavaScript only on the battle screen.
- The browser sends only a pick. The server validates it, chooses the computer's pick and decides every round. Never trust a client-sent result.
- A saved result is one finished best-of-5 match. Abandoned matches are never counted. Matches always end in a win or a loss.
- Every query for private data is filtered by the signed-in user's id. A password change bumps `auth_version` and revokes other sessions.
- Out of scope: coins, gear, armory, daily runs, multiplayer, Three.js.
- Keep `app/game/` free of Flask imports so its rules can be unit-tested alone. Opponents use the Strategy pattern (one class per behavior).
- Each new account is randomly assigned experiment version A or B and keeps it; only version B shows the "N stars to <next rank>!" nudge.
- Keep secrets in `.env` (never committed); keep `.venv`, caches and local databases out of Git.

## Animation (required, but quick)
A round must stay about 2 seconds, so animations are short and snappy. Use CSS keyframes and the Web Animations API; no animation library needed.
- **Round sequence (~2 s total):** your fighter does a send-out slide (200 ms) → the rival's pick flips in (200 ms) → the winner does an attack lunge toward the loser (250 ms) → the loser flashes white twice and shakes (300 ms) → the round-win square fills with a small pop (scale 0.6 → 1, 150 ms) → the text line types out quickly (about 20 ms per character, skippable).
- **Match end:** the loser drops and fades (knockout, 400 ms); the result pop-up scales from 0.95 to 1 with a fade (200 ms). In version B the earned star fills with a short pulse, then the "1 star to …" line slides up.
- **Rank up:** a brief full-width gold banner sweeps across (600 ms) with the new rank name; no confetti loops.
- **Buttons:** fighter buttons press down 2 px on click/keypress and show the gold focus ring; the chosen fighter's button stays highlighted until the round resolves.
- **Pixel feel:** use `steps()` timing for sprite movement so it looks pixel-stepped; keep `image-rendering: pixelated`.
- **Dashboard:** the star bar fills from left to right on load (400 ms); recent matches fade in with a 40 ms stagger.
- **Rules:** animate only `transform` and `opacity`; never block input for longer than the round sequence; Enter/1/2/3 can skip the text typing.
- **Reduced motion:** with `prefers-reduced-motion`, skip lunges, shakes and sweeps; show results instantly with a 150 ms fade. Round results are still announced through the `aria-live` line.

## Tests
- Predict expected results from the rules in the docs, not from the code. Do not weaken or delete assertions to make tests pass.
- Unit tests: rules (all 9 matchups), stars and rank math, each opponent strategy.
- Integration tests (Flask test client + SQLite): sign up / sign in / sign out, duplicate and wrong-password errors, a full match saved, abandoned match not saved, two-user isolation, display-name validation, password change revoking old sessions.
- Browser test (Playwright): the whole journey at 375 px wide, plus keyboard-only play.
- GitHub Actions runs all of the above on every push.

## Record
After each working session add an entry to `docs/project-record.md` (Changed / Checked / Next). Write NOT RUN for any check that was not actually run. Note that the work was AI-assisted.
