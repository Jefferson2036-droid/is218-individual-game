# Game design: Arena Climb

## The three fighters
| Fighter | Beats | Because |
|---|---|---|
| Knight | Archer | The Knight charges down the Archer before they can shoot again. |
| Archer | Wizard | The Archer shoots the Wizard before the spell is cast. |
| Wizard | Knight | Magic goes straight through armor. |

Same fighter on both sides is a tie, and the round is replayed. The triangle above is shown on screen during every match, because these rules are less familiar than rock paper scissors.

## A match
- Best of 5 rounds against the computer (first to 3 round wins).
- Each round: the player picks a fighter, the computer's pick is revealed, the winner is shown with a short animation.

## Ranks (the climb)
| Rank | Stars to rank up | How the computer plays |
|---|---|---|
| Recruit | 3 | Picks at random. |
| Squire | 4 | Sometimes uses the "win-stay, lose-shift" pattern real players fall into (sources 3–4): it expects you to repeat a winning fighter, or to switch after a loss. |
| Knight-Captain | 5 | Predicts your next pick from what you usually play after your previous pick in this match. |
| Champion | — (top rank) | Uses your history across all your matches, plus the patterns above. |

- Win a match: +1 star. Lose a match: −1 star (you cannot drop below the start of your current rank).
- Three wins in a row: bonus star.
- The computer at every rank keeps some randomness, so it can always be beaten.

## Rewards
For this term the reward is the climb itself: stars, rank-ups and a visible "next rank" bar. Coins, gear and the armory were cut on 2026-11-23 and moved to the [backlog](backlog.md).

## Art and screen style
Fighters are rendered from Blender (see docs/art-pipeline.md). Gear variants (tinted models) are backlog only.

The match screen uses a **retro handheld battle-screen style** (inspired by classic turn-based handheld RPGs, but with our own art, names and layout; no characters, logos or screens from other games):
- Rival's fighter on a grass platform top right, yours bottom left, each with an info panel and an HP bar (3 HP = the 3 round wins needed).
- A text box at the bottom tells the round as it happens ("You send out KNIGHT!", "The rival sends out WIZARD!", "WIZARD's magic blasts KNIGHT!").
- A three-option command menu: Knight, Archer, Wizard.
- Fighters are the Blender renders shrunk and enlarged to look like pixel art.
- Short animations: send-out slide, attack lunge, hit flash, knockout drop.

## Open design questions
- Whether losing stars feels too punishing for a casual audience.
