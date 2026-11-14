# Project record

One entry per working session. Link the issue, the change (commit or PR) and the check.
Never write that a check passed unless it was run; write "NOT RUN — reason".

## 2026-11-13 — Repository scaffold
**Changed:** Created the repo structure and Plan templates (README, docs/, research/, PR and issue templates).
**Checked:** Markdown links between files — NOT RUN. No automated checks exist yet.
**Next:** Fill in the two-concept comparison, choose the audience, confirm the stack against Canvas, write the experiment.

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
