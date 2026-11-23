# Stack

**Status: decided 2026-11-23.** Replaces the FastAPI stack from 2026-11-16.

## Why the stack changed
The course brief says to use a supported authentication component rather than inventing password hashing or session tokens. The first build hashed passwords with Python's built-in scrypt and issued its own JWT tokens, which is invented auth. Hand-made JWTs also make it hard to meet the rule that old sessions stop working after a password change, because a token stays valid until it expires.

## Back-end options compared
| | Flask + Flask-Login (chosen) | FastAPI + FastAPI Users | Django |
|---|---|---|---|
| Authentication | Flask-Login sessions; Werkzeug password hashing | Library handles register, login, hashing | All built in |
| Revoke sessions after password change | Server-side session records checked on every request; the instructor's full-game example shows the pattern | Possible with its database strategy | Built in |
| What gets rewritten | API/web layer only; `app/game/` rules, opponent and match logic move over unchanged | Auth and account routes | Most of the app |
| Risk | Switching framework mid-project | Library described as in maintenance mode (to verify on its repository) | Most to learn in two weeks |

**Why Flask:** it is the setup the instructor's reference game uses, its session model makes "log out everywhere after a password change" easy to explain and test, and my game logic carries over as plain Python.

**Giving up:** FastAPI's automatic `/docs` API page and the code already written for the FastAPI routes (kept in git history).

## Chosen stack
| Layer | Choice | Why |
|---|---|---|
| Web app | Flask | Small, matches the class example |
| Auth | Flask-Login + Werkzeug password hashing; server-side login-session table | Supported components; sessions can be revoked |
| Forms / CSRF | Flask-WTF | CSRF protection on sign-in and account forms |
| Game logic | Plain Python in `app/game/` (rules, opponent strategies, match, progression) | Testable without the web layer |
| Front end | HTML templates + plain CSS and JavaScript | Three fighter buttons and a result screen need no engine |
| Database | PostgreSQL in Docker Compose; SQLite for tests and Docker-free runs | Users and matches are relational |
| Tests | pytest (unit, integration with the Flask test client), Playwright (browser journey) | Each layer checked separately |
| CI | GitHub Actions | Linkable check runs for the project record |
| Containers | Docker Compose (web + database) | Same setup on any machine; credentials in `.env`, not the image |
| Art | Blender renders of Quaternius CC0 models, starter look per fighter | Already rendered |

Moved to the backlog: Three.js real-time 3D fighters.

## Installed on my Mac
git 2.55.0, Python 3.12.14, VS Code (2026-11-13). Docker Desktop and Node.js installed; versions not recorded yet. NOT CHECKED.
