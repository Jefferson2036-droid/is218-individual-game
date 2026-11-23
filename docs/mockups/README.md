# Arena Climb – screen mockups

Static HTML mockups of the five phone screens (390 × 844), made 2026-11-23 with Claude from the decisions in [../frontend.md](../frontend.md). Open any file in a browser. They are a **visual reference for the build, not production code**: no Flask, no JavaScript, sample data only.

| File | Screen | Story |
|---|---|---|
| [sign-in.html](sign-in.html) | Sign in (sign-up uses the same layout) | 1 |
| [battle.html](battle.html) | Battle, mid-match (round 3: your Archer beats the rival's Wizard) | 2 |
| [result.html](result.html) | Result pop-up over the battle, **version B** (nudge). Version A drops the star block | 2, 3, experiment |
| [dashboard.html](dashboard.html) | Dashboard with sample matches; the new-player empty state is in a `<template>` at the bottom | 4 |
| [account.html](account.html) | Display name and password change, with an example error | 5 |

Editable design canvas (private until shared): https://claude.ai/artifact/XjZsT1Z8YhuFzfprf1GLrx

## Design tokens
| Token | Value | Use |
|---|---|---|
| Ground | `#16182A` | Page background |
| Panel | `#262A40`, border `#3B4163` | Cards, buttons, inputs |
| Text | `#F4EBD0`; muted `#C9C2AC` | Body text |
| Accent (torch gold) | `#F2B84B`, shadow `#9C6B17` | Primary buttons, stars, active nav, focus ring |
| Player | `#7FB3E8` | Your card, wins |
| Rival | `#E8835A` | Rival card, losses, errors |
| Wall / floor | `#2B2F45` / `#3A3A4F` with 2 px grid lines | Battle arena |
| Heading font | Press Start 2P (Google Fonts) | Titles, labels, buttons |
| Body font | Pixelify Sans (Google Fonts) | Everything else, 16 px minimum |
| Sprites | `img/*-px.png`: Blender renders cut to 96 px tall, hard alpha, shown with `image-rendering: pixelated` at 1.5× or 2× | Fighters; rival flipped with `scaleX(-1)` |
| Pixel shadow | `4px 4px 0` hard drop shadow, no border radius | Buttons and cards |

## Rules the build must keep
- Round wins are three squares per side. No HP bars, grass platforms or "send out" lines (keeps the look our own).
- The rules line "Knight beats Archer beats Wizard beats Knight" is always visible during a match.
- Fighter buttons are at least 44 px tall and show their key (1/2/3); the focused control gets a gold outline.
- The round text line is an `aria-live="polite"` region.
- On the result pop-up, "Play again" has focus when it opens.
- The dashboard leads with stars to the next rank.
