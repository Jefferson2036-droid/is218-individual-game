---
title: Arena Climb · programming research
---

# Arena Climb: programming research

Research site for my IS218 creative project. It shows the question I started with, the sources I used, the choices I made and what is still unchecked.
**Code:** [github.com/Jefferson2036-droid/is218-individual-game](https://github.com/Jefferson2036-droid/is218-individual-game) ·
**My career research site:** [jefferson2036-droid.github.io/is218-portfolio](https://jefferson2036-droid.github.io/is218-portfolio/) ·
**Project record:** [docs/project-record.md](docs/project-record.md)

## 1. Question, audience and goal
- **Question:** what gives a player a reason to play rock paper scissors again, in a game short enough for a few minutes between classes?
- **Audience:** college students playing on their phones. Compared with a once-a-day “Wordle-style” player in [audience.md](docs/audience.md).
- **Bounded goal (Working Promise):** sign up → play a best-of-5 Knight/Archer/Wizard match against the computer → result saved → private dashboard → change display name and password. See [dream-promise.md](docs/dream-promise.md).

## 2. Sources
16 sources, each with the date I looked at it and what I took from it: [research/sources.md](research/sources.md).
The most important ones:

| Source | Date checked | What it gave me |
|---|---|---|
| MIT Technology Review and Business Standard reports on the Zhejiang University study (sources 3–4) | 2026-11-13 | Real players are not random: winners tend to repeat, losers tend to switch (“win-stay, lose-shift”). This is how the computer gets harder at higher ranks. |
| Sansukumi-ken and kitsune-ken history (sources 8–10) | 2026-11-13 | Re-themed versions with characters have a long history, and unclear rules hurt them. |
| IS218 game brief, “Use a supported authentication component” ([course repo](https://github.com/kaw393939/is218-studio)) | 2026-11-23 | Why I moved from my own password/token code to Flask-Login. |
| Quaternius CC0 models (sources 13–14) | 2026-11-13 | Free models for the three fighters, rendered in Blender. |

## 3. What the sources establish, what I infer, what I assume
- **Established:** people fall into win-stay/lose-shift patterns (sources 3–4); themed three-way games exist and confusing rules hurt them (sources 8–10).
- **My inference:** a computer that uses those patterns will feel harder at higher ranks; showing the rule triangle on screen prevents confusion.
- **Assumption still to check:** that the next rank alone (with coins and gear cut) is enough reason to play another match. This is the experiment below.

## 4. Alternatives and my choices
| Decision | Options compared | Choice and reason |
|---|---|---|
| Concept | Pattern Reader vs Arena Climb | Arena Climb: it gives a reason to keep playing. Coins and gear moved to the [backlog](docs/backlog.md) to keep scope small. [concepts.md](docs/concepts.md) |
| Audience | Quick competitor (2048-style) vs daily player (Wordle-style) | Quick competitor: fits the climb and can be tested with classmates. [audience.md](docs/audience.md) |
| Back end | Flask + Flask-Login vs FastAPI Users vs Django | Flask: supported auth, sessions I can revoke, matches the class example. [stack.md](docs/stack.md) |
| Code pattern | Strategy classes vs one if/else function | Strategy, to be compared in practice. [pattern-experiment.md](docs/pattern-experiment.md) |
| Front end | Server-rendered pages vs single-page app; retro pixel look | Server-rendered with JavaScript only on the battle screen. [frontend.md](docs/frontend.md), [screen mockups](docs/mockups/README.md) |

Full plan: [user stories](docs/user-stories.md) · [flow](docs/flow.md) · [architecture](docs/architecture.md) · [game design](docs/game-design.md) · [checks](docs/checks.md).

## 5. Next experiment and checks
| Check | Expected | Observed |
|---|---|---|
| A/B playtest: does “1 star to the next rank!” make classmates start another match? ([experiment.md](docs/experiment.md)) | Version B players play more matches | NOT RUN (planned for class, Nov 25) |
| First build's rules, opponent and match tests | All pass | 67 passed on my Mac, 2026-11-16 (FastAPI build) |
| Flask rebuild: two-user privacy, password change signs out other sessions | Pass | NOT RUN |
| Keyboard-only play and 375 px phone layout | Pass | NOT RUN |

## 6. How AI helped
I used Claude to search for sources, lay out options for each decision, draft documents and mockups, and write code. I made every choice listed above. I verified the course requirements myself in Canvas and the course repository. Two sources (1 and 5) were not opened directly and are marked that way. Every “observed” result above comes from a check that actually ran.
