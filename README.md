# IS218 Individual Creative Game: Arena Climb (working title)

Knight, Archer, Wizard: a rock paper scissors game where you climb ranks against a computer that gets harder as you win.
Repository: https://github.com/Jefferson2036-droid/is218-individual-game

**Phase: Plan (re-done 2026-11-23), then rebuild on Flask.**

**Try the prototype:** open `prototype/index.html` in a browser (double-click it). No install needed.

## Run it

**With Docker (API + PostgreSQL):**
```
docker compose up --build
```
Then open **http://localhost:8000** to play. The API's own test page is at http://localhost:8000/docs.

**Run the tests (no Docker needed):**
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
```

## Plan (re-done 2026-11-23)
Required product flow: **account → match → saved result → dashboard → account update**

| Plan item | File | Status |
|---|---|---|
| Two concepts compared | [docs/concepts.md](docs/concepts.md) | Arena Climb, narrowed (no coins/gear) |
| Two audiences compared | [docs/audience.md](docs/audience.md) | A: quick competitor (2048-style) over B1: daily ritual (Wordle-style) |
| Dream / Working Promise / Experiment | [docs/dream-promise.md](docs/dream-promise.md) | Decided |
| Creative experiment | [docs/experiment.md](docs/experiment.md) | "Almost there" A/B nudge; NOT RUN |
| Code pattern experiment | [docs/pattern-experiment.md](docs/pattern-experiment.md) | Strategy vs if/else; NOT RUN |
| Stack | [docs/stack.md](docs/stack.md) | Flask + Flask-Login, PostgreSQL |
| Five user stories | [docs/user-stories.md](docs/user-stories.md) | Rewritten with checks |
| Flow | [docs/flow.md](docs/flow.md) | Updated |
| Architecture sketch | [docs/architecture.md](docs/architecture.md) | Updated (rounds table) |
| Keyboard, phone, privacy, analytics | [docs/checks.md](docs/checks.md) | Planned; GoatCounter |
| Game design | [docs/game-design.md](docs/game-design.md) | Updated |
| Front end + mockups | [docs/frontend.md](docs/frontend.md), [docs/mockups/](docs/mockups/README.md) | Decided; 5 screens mocked up |
| Instructions for coding agents | [AGENTS.md](AGENTS.md) | For the Flask rebuild |
| Backlog | [docs/backlog.md](docs/backlog.md) | Coins, gear, armory, daily run, 3D |
| Sources | [research/sources.md](research/sources.md) | 12 sources |
| Project record | [docs/project-record.md](docs/project-record.md) | Ongoing |

## Build status
The first build (2026-11-16) used FastAPI with hand-made auth and included coins, gear and an armory. It is being rebuilt on Flask to match this plan; the game rules, opponent and match logic in `app/game/` carry over.

Instructor example (research/planning only, not a required engine):
https://github.com/kaw393939/is218-individual-game

Follow the Canvas assignment for full scope and rubric.
