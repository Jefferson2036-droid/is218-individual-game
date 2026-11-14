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

## Rewards (cosmetic only)
- Every match win earns coins; ranking up gives a bigger coin bonus and unlocks one item.
- Coins buy gear in the armory. Gear changes how a fighter looks, never whether it wins.

| Fighter | Starter look | Example unlocks |
|---|---|---|
| Knight | Plain steel armor | Gold armor, dragon shield, black knight set |
| Archer | Green cloak | Shadow cloak, flame bow, elven set |
| Wizard | Blue robe | Storm staff, purple spell color, archmage set |

Plan for about 4 items per fighter at launch (12 total).

## Open design questions
- Exact coin amounts and item prices (set during playtesting).
- Whether losing stars feels too punishing for a casual audience.
