# Stack

**Status: proposed, not confirmed.** Check the Canvas assignment for any required stack before committing to this.

Installed on my Mac as of 2026-11-13: git 2.55.0, Python 3.12.14, VS Code. Node.js and Docker Desktop were installed the same evening; `docker --version` and `node --version` output not recorded here yet.

| Layer | Proposed choice | Why | Alternative considered |
|---|---|---|---|
| Game front end | Plain HTML, CSS and JavaScript | Three buttons and a scoreboard do not need a game engine | Phaser |
| Dashboard / account pages | HTML pages served by the API, with a little JavaScript | Keeps one codebase | A separate React app |
| API | FastAPI (Python) | Matches the Python + pytest work earlier in IS218 | Express (Node) |
| Database | PostgreSQL + SQLAlchemy | Users and results are relational | SQLite for local development |
| Auth | Hashed passwords + JWT or session cookie | | |
| Tests | pytest (API), Playwright (the five-step flow) | | |
| CI | GitHub Actions | Gives linkable check runs for the project record | |
| Containers | Docker Compose (API + database) | Same setup on any machine | Run both directly |
