# Front-end plan

Decided 2026-11-23.

## Decisions
| Question | Choice | Why |
|---|---|---|
| Page approach | Server-rendered Flask templates; JavaScript only on the battle screen | Sign-in, dashboard and account work without JavaScript and get CSRF protection from Flask-WTF; less code to test |
| Visual style | Retro pixel, my own version (castle courtyard arena) | Fits the fighters and Blender sprites; avoids copying another game's battle screen (no grass platforms, HP bars or "send out" lines) |
| Round pacing | Quick, about 2 seconds per round | Keeps a best-of-5 match around 30–60 seconds (audience A) |
| Result screen | Pop-up over the battle screen, "Play again" focused | One tap to the next match, like 2048's "Try again" |
| A/B nudge | Each new account is randomly assigned A or B and keeps it | Fair split; I can't influence who sees what |

## Screens
| Screen | Contents |
|---|---|
| Sign in / Sign up | Username, password, clear errors, link between the two |
| Battle | Rival top, player bottom, round score (first to 3), rule triangle always visible, three large fighter buttons |
| Result pop-up | Win/lose and round score; version B adds the star bar and "N stars to <next rank>!"; Play again (focused) and Dashboard |
| Dashboard | Stars to next rank first, then rank, wins/losses, streak, last 10 matches; empty state for new players |
| Account | Display name; password change (current, new, confirm) |
| Nav | Play · Dashboard · Account · Sign out |

## A round (about 2 s)
Pick → rival's pick revealed → short attack/hit animation → one text line ("Archer shoots Wizard — you win the round!").

## Accessibility and phone
- Keys 1/2/3 pick Knight/Archer/Wizard; Tab/Enter everywhere; visible focus.
- Round results announced through an `aria-live` text line.
- Animations shortened or off with `prefers-reduced-motion`.
- Battle fits at 375 px wide with no scrolling.

## Reused / replaced
Reused: Blender sprites, colors, parts of the CSS. Replaced: the single-page `app/static/index.html` and `app.js` (built around coins and gear).

## Mockup
Static HTML copies with design tokens: [docs/mockups/](mockups/README.md). Editable canvas (2026-11-23, made with Claude): https://claude.ai/artifact/XjZsT1Z8YhuFzfprf1GLrx — private until shared. Theme: castle courtyard at night, torch-gold accent, Press Start 2P headings with Pixelify Sans body text, pixelated Blender sprites. Not yet reviewed by a classmate.
