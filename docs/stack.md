# Stack

**Status: in use.** The back end is built with FastAPI, SQLAlchemy, PostgreSQL (SQLite for tests and Docker-free runs), pytest and Docker Compose. Still not checked against Canvas for a required stack.

Installed on my Mac as of 2026-11-13: git 2.55.0, Python 3.12.14, VS Code. Node.js and Docker Desktop were installed the same evening; `docker --version` and `node --version` output not recorded here yet.

| Layer | Proposed choice | Why | Alternative considered |
|---|---|---|---|
| Game front end | Plain HTML, CSS and JavaScript | Three fighter buttons, a scoreboard and simple win animations do not need a game engine | Phaser, if animations grow |
| Dashboard / account pages | HTML pages served by the API, with a little JavaScript | Keeps one codebase | A separate React app |
| API | FastAPI (Python) | Matches the Python + pytest work earlier in IS218 | Express (Node) |
| Database | PostgreSQL + SQLAlchemy | Users and results are relational | SQLite for local development |
| Auth | scrypt password hashes (Python standard library) + JWT in an HttpOnly cookie or Bearer header | No extra hashing package to install | bcrypt / argon2 |
| Tests | pytest (API), Playwright (the five-step flow) | | |
| CI | GitHub Actions | Gives linkable check runs for the project record | |
| Containers | Docker Compose (API + database) | Same setup on any machine | Run both directly |
| Art | Blender + Python (`bpy`) scripts, free CC0 Quaternius models | Scripted gear variants; regenerable; see docs/art-pipeline.md | Emoji / colored cards (prototype look) |
| In-game 3D (stretch) | Three.js with glTF models | Same models, real-time 3D in the browser | Stay with rendered 2D sprites |
