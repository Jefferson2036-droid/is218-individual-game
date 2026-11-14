# Stack

**Status: proposed, not confirmed.** Check the Canvas assignment for any required stack before committing to this.

| Layer | Proposed choice | Why | Alternative considered |
|---|---|---|---|
| Game front end | HTML canvas + JavaScript (or Phaser) | Runs in the browser, no install | |
| Dashboard / account pages | Server-rendered HTML or a small JS front end | | |
| API | FastAPI (Python) | Matches the Python + pytest work earlier in IS218 | |
| Database | PostgreSQL + SQLAlchemy | Users and results are relational | SQLite for local development |
| Auth | Hashed passwords + JWT or session cookie | | |
| Tests | pytest (API), Playwright (flow) | | |
| CI | GitHub Actions | Gives linkable check runs for the project record | |
| Containers | Docker Compose | | |
