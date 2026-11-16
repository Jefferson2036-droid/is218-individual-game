# Project record

One entry per working session. Link the issue, the change (commit or PR) and the check.
Never write that a check passed unless it was run; write "NOT RUN — reason".

## 2026-11-13 — Repository scaffold
**Changed:** Created the repo structure and Plan templates (README, docs/, research/, PR and issue templates).
**Checked:** Markdown links between files — NOT RUN. No automated checks exist yet.
**Next:** Fill in the two-concept comparison, choose the audience, confirm the stack against Canvas, write the experiment.

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
