# Project record

One entry per working session. Link the issue, the change (commit or PR) and the check.
Never write that a check passed unless it was run; write "NOT RUN — reason".

## 2026-11-23 — Plan re-done, scope narrowed, stack changed to Flask
**Changed:** Re-did the Plan one decision at a time. Kept Arena Climb but cut coins, gear and the armory to a new backlog. Compared two audiences (A: 2048-style quick competitor, B1: Wordle-style daily player) and chose A. Wrote Dream / Working Promise; chose the "almost there" A/B nudge as the creative experiment and Strategy vs if/else as the pattern experiment. Changed the stack to Flask + Flask-Login because the first build's hand-made scrypt/JWT auth did not meet the "supported authentication component" rule. Rewrote the five stories (a saved result is one match; dashboard shows wins and losses only), flow and architecture (in-progress match in the database, rounds table). Planned keyboard, phone and privacy checks; chose GoatCounter and matches-per-session. Options laid out with Claude; I made each choice.
**Checked:** Plan docs only; no code changed. Partner review — NOT RUN. Playtest — NOT RUN. GoatCounter and Plausible pricing — NOT CHECKED on their sites.
Front end planned (server-rendered pages, retro pixel castle-courtyard look, quick rounds, result pop-up, random A/B per account) and five phone screens mocked up as static HTML in docs/mockups/. Added AGENTS.md for the Flask rebuild with a coding agent.
**Next:** Publish the research site; partner review in class Nov 25 with the A/B playtest; rebuild on Flask.

## 2026-11-13 — Repository scaffold
**Changed:** Created the repo structure and Plan templates (README, docs/, research/, PR and issue templates).
**Checked:** Markdown links between files — NOT RUN. No automated checks exist yet.
**Next:** Fill in the two-concept comparison, choose the audience, confirm the stack against Canvas, write the experiment.

## 2026-11-16 — Pages: the game is playable in the browser
**Changed:** Added the game's pages (`app/static/`): sign in and register, the battle screen now driven by the API, dashboard, armory and account settings. The API serves them at `/`. Docker image now includes the pages and the fighter images; added `.dockerignore`. The Friday prototype in `prototype/` is unchanged and kept for reference. Written with Claude.
**Checked:** Before this change, on my Mac: Docker Compose started the API and PostgreSQL, and a browser check against it registered an account, played and saved a match, and confirmed log-out (dashboard and armory endpoints were not in that build yet). For the pages: a headless-Chrome run of the whole flow (bad login, register, win three matches, rank up, equip unlocked gear, lose a match, dashboard, buy and equip in the armory, rename, change password, log out, old password refused, new password accepted, reload keeps the session) passed with no script errors — but against a stand-in server built on the real `app/game` code, not the real API. Display name `<b>Jeff</b>` shows as text. 47 pure-logic tests pass in Claude's workspace. Full `pytest` on my Mac (expected 86) and the pages against the real API in Docker — NOT RUN yet.
**Next:** `pytest`, rebuild Docker, play at http://localhost:8000; then a Playwright test in the repo, GitHub Actions, restyle the battle screen as my own design.

## 2026-11-16 — Back end: dashboard, account update, armory
**Changed:** Added API endpoints for the dashboard (progress, stats, last 10 matches, gear), account update (display name, password) and armory (buy with coins, equip, unequip). With the earlier work, all five flow steps now exist in the API; none has a web page yet. Written with Claude.
**Checked:** 47 pure-logic tests still pass in Claude's workspace. The 17 new API tests (`tests/test_api_dashboard.py`) and the reorganized earlier API tests — NOT RUN yet on a machine with FastAPI installed. Expected total: 84.
**Next:** Run `pytest` on my Mac; then build the pages (login, battle screen wired to the API, dashboard, armory) and a Playwright test of the whole flow.

## 2026-11-16 — Back end: accounts, match logic, saved results
**Changed:** Started the build. Added `app/` (FastAPI): game rules, computer opponent, match and progression as plain Python in `app/game/`; accounts (register, log in, log out, /api/me); match API where the server decides every round and saves the result, stars, coins, rank-ups and unlocks when a match ends. Added Dockerfile, docker-compose.yml (API + PostgreSQL), requirements and tests. Architecture and stack docs updated to match what was built. Written with Claude.
**Checked:** `pytest`: 47 tests passed for rules, opponent, match, progression, password hashing and tokens (run in Claude's workspace, Python 3.13). Then on my Mac (Python 3.12, fresh `.venv`): `pytest` — 67 passed, 1 warning (a Starlette deprecation notice about the httpx test client; no failures), including all 20 API test cases. `docker compose up --build` — NOT RUN yet (Docker Desktop was not running).
**Next:** Start Docker Desktop and run `docker compose up --build`; then dashboard, account update and armory; then connect the battle screen.

## 2026-11-13 — Retro battle-screen look
**Changed:** Restyled the prototype as a retro handheld battle screen (my request): fighters on platforms, HP bars for rounds, typewriter text box, four-option command menu, pixelated Blender sprites, simple attack/hit/knockout animations. Game rules unchanged. Kept our own art and names; no material from other games. Built with Claude.
**Checked:** Headless Chrome: no script errors; full matches played through the text flow; rank-up unlock screen with the Gold Armor sprite; equipped gear shows in battle; 500 simulated matches across all ranks; desktop and phone layouts checked from screenshots. Playtest with classmates — NOT RUN.
**Next:** Playtest; refine gear tint so faces and hair keep their colors.

## 2026-11-13 — First Blender renders
**Changed:** Ran art/blender/make_sprites.py in Blender 5.3 (from Blender's Python console, run by Claude). It produced 9 sprites in art/renders: Knight, Archer and Wizard, each in starter look plus two gear variants.
**Checked:** All 9 PNGs are 512×512 with transparent backgrounds; reviewed on a contact sheet: textured, idle pose, fully in frame, gear tints visible. Prototype loads the images (emoji fallback when they are missing).
**Known issue:** The gear tint colors the whole model, including faces and hair. Next pass: tint only armor/cloth materials or texture regions.
**Next:** Playtest with classmates; refine gear look.

## 2026-11-13 — Models added, Blender render attempted
**Changed:** Downloaded Quaternius "LowPoly RPG Characters" (CC0) and added Warrior (as Knight), Ranger (as Archer) and Wizard as FBX with textures to art/models, with license and source table. Updated make_sprites.py: attaches textures by material name, uses the Idle pose, 3/4 camera angle, can run inside Blender's window. Prototype now shows art/renders images when they exist and falls back to emoji. Done with Claude.
**Checked:** Prototype in headless Chrome: no script errors, emoji fallback works when renders are missing. Render run in Blender 5.3 — NOT RUN to completion (screen became unavailable mid-attempt).
**Next:** Run the render command in Terminal; review the images; push.

## 2026-11-13 — Art decision: Blender
**Changed:** Decided to use Blender for the fighters' art, with free CC0 Quaternius models and a Python script (`art/blender/make_sprites.py`) that renders every fighter + gear variant as a PNG. 2D sprites first; real-time 3D with Three.js is a stretch goal. Added docs/art-pipeline.md, art/models/README.md, stack and source updates. Pros/cons discussed and script written with Claude.
**Checked:** Script passes a Python syntax check. Rendering in Blender — NOT RUN (Blender not installed, models not downloaded).
**Next:** Install Blender; download the Quaternius knight and RPG character packs into art/models; run the script and fix camera framing; record model sources in art/models/README.md.

## 2026-11-13 — Playtest prototype
**Changed:** Added `prototype/index.html`, a single-page clickable prototype for the creative experiment (fighters, best-of-5 matches, four ranks with a smarter computer at each, coins, unlocks, armory, playtest counter). Built with Claude.
**Checked:** Opened in headless Chrome: no console errors; rule logic checked (Wizard beats Knight, Knight beats Archer, Archer beats Wizard); win-stay/lose-shift and habit predictions checked on sample inputs; 800 simulated matches across all four ranks ran without errors; rank-up, equip, buy and mobile layout checked from screenshots. Playtest with classmates — NOT RUN.
**Next:** Playtest with 3–5 classmates and record results in experiment.md.

## 2026-11-13 — Concept decided: Arena Climb (Knight, Archer, Wizard)
**Changed:** Replaced the Pattern Reader draft with my own direction: rock paper scissors needs a reason to keep playing, so the game is now a rank climb against a computer that gets harder as you win, with cosmetic gear unlocks. I chose the audience (college students), the difficulty approach (gets harder as you win) and the theme (Knight, Archer, Wizard). Rewrote concepts, audience, flow, user stories, architecture and experiment; added game-design.md; added 12 sources. Drafting and source search done with Claude.
**Checked:** Sources were found through web search; source 1 (NYT game) and source 5 (arXiv paper) not opened directly — NOT RUN. Experiment — NOT RUN. Stack not yet checked against Canvas — NOT RUN.
**Next:** Run the paper/clickable playtest with 3–5 classmates; check Canvas for a required stack; open one GitHub issue per Plan item and link them here.

## 2026-11-13 — Plan drafts for the rock paper scissors concept
**Changed:** Drafted the two-concept comparison (Five-Move Duel vs Pattern Reader), audience, flow, five user stories, stack table and experiment plan. Drafts were written with Claude and still need my review.
**Checked:** Repository published to GitHub and local `main` tracks `origin/main` (checked with `git status`). Links between docs — NOT RUN. Experiment — NOT RUN. No sources collected yet.
**Next:** Confirm the concept decision and audience; look at 2–3 existing rock paper scissors games and record them in research/sources.md; confirm the stack against Canvas; open one issue per Plan item and link them here.

<!-- Copy for each new session:
## YYYY-MM-DD — Title
**Changed:** what changed (#issue, commit/PR link)
**Checked:** which check, with link — or NOT RUN — reason
**Next:** next step (#issue)
-->
