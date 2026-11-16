# IS218 Individual Creative Game: Arena Climb (working title)

Knight, Archer, Wizard: a rock paper scissors game where you climb ranks against a computer that gets harder as you win, and winning unlocks gear to customize your three fighters.
Repository: https://github.com/Jefferson2036-droid/is218-individual-game

**Phase: Build.** The back end (accounts and matches) is in `app/`; the playable screen is still the prototype and is not connected to it yet.

**Try the prototype:** open `prototype/index.html` in a browser (double-click it). No install needed.

## Run it

**With Docker (API + PostgreSQL):**
```
docker compose up --build
```
Then open http://localhost:8000/docs to try the API.

**Run the tests (no Docker needed):**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

## What is built so far
| Flow step | Status |
|---|---|
| Account (register, log in, log out) | API built: `app/routers/auth.py` |
| Game (best-of-5 match, server decides every round) | API built: `app/routers/matches.py`, rules in `app/game/` |
| Saved result (stars, coins, rank-ups, unlocks) | Saved when a match ends |
| Dashboard (progress, stats, last 10 matches, gear) | API built: `app/routers/dashboard.py`; no page yet |
| Account update (display name, password, buy and equip gear) | API built: `app/routers/account.py`, `app/routers/armory.py`; no page yet |
| Battle screen connected to the API | Not built (prototype only) |

Required product flow: **account → game → saved result → dashboard → account update**

| Plan item | File | Status |
|---|---|---|
| Two concepts compared | [docs/concepts.md](docs/concepts.md) | Decided: Arena Climb |
| Audience chosen | [docs/audience.md](docs/audience.md) | Chosen; playtest evidence still needed |
| Game design (rules, ranks, rewards) | [docs/game-design.md](docs/game-design.md) | Draft |
| Art pipeline (Blender) | [docs/art-pipeline.md](docs/art-pipeline.md) | First 9 sprites rendered |
| Flow specified | [docs/flow.md](docs/flow.md) | Draft |
| Stack named | [docs/stack.md](docs/stack.md) | Proposed, not confirmed against Canvas |
| Five user stories | [docs/user-stories.md](docs/user-stories.md) | Draft |
| Architecture sketch | [docs/architecture.md](docs/architecture.md) | Draft |
| One uncertain creative experiment | [docs/experiment.md](docs/experiment.md) | Prototype built ([prototype/index.html](prototype/index.html)); playtest NOT RUN |
| Sources | [research/sources.md](research/sources.md) | 12 sources |
| Project record | [docs/project-record.md](docs/project-record.md) | Ongoing |

Instructor example (research/planning only, not a required engine):
https://github.com/kaw393939/is218-individual-game

Follow the Canvas assignment for full scope and rubric.
