# Two concepts compared

Both are rock paper scissors games against a computer opponent.

| | Concept A: Pattern Reader | Concept B: Arena Climb |
|---|---|---|
| One-sentence pitch | Classic rock paper scissors against a computer that learns your habits and scores how predictable you are. | Knight, Archer, Wizard: beat the computer to climb ranks, and unlock gear to customize your three fighters. |
| The three moves | Rock, paper, scissors | Knight, Archer, Wizard (Knight charges down Archer, Archer shoots Wizard, Wizard's magic beats Knight) |
| Who it is for | Players curious about how a computer predicts them | Competitive players who want a reason to keep playing |
| Core loop | Play 20 rounds → see your predictability score | Play a best-of-5 match → gain or lose rank stars → earn coins → unlock and equip gear |
| Why come back? | Try to lower your predictability score | Climb to the next rank, keep a win streak, unlock the next item |
| What gets saved as the "result" | Wins, losses, ties, predictability score | Match outcome, rounds won/lost, rank before/after, coins earned |
| What the dashboard shows | Match history and predictability over time | Current rank and progress, win rate, streak, match history, gear collection |
| How the "account update" step fits | Change name or password only | Change name or password **and** equip unlocked gear (a natural reason to visit) |
| Similar games looked at | NYT "You vs. the Computer" (sources 1–2) | Traditional themed variants: mushi-ken, kitsune-ken, Bear Hunter Ninja (sources 8–11); learning-opponent research reused for difficulty (sources 1–5) |
| Riskiest part | The opponent may feel unfair; little reason to replay | Rules for new objects are less obvious than rock paper scissors; cosmetic rewards may not be enough motivation |
| Fits the time available? | Yes | Yes, if gear is cosmetic only and the item list stays small (about 4 items per fighter) |

A third idea, **Five-Move Duel** (rock paper scissors lizard Spock), was dropped early: it cuts ties but makes players learn ten rules (sources 6–7).

## Decision
**Chosen concept:** Concept B, Arena Climb. First chosen 2026-11-13; re-confirmed and narrowed 2026-11-23.

**Why:** Rock paper scissors is a competitive game people use to settle things, and Pattern Reader gave players no reason to keep going. Arena Climb gives that reason: ranks to climb and a computer that gets harder as you win.

**Scope change (2026-11-23):** Coins and gear (buying, unlocking, equipping) are out of this term's promise and moved to the [backlog](backlog.md) for a future sprint. The rank climb stays. Reason: the required account → match → saved result → dashboard → account update journey has to work and be tested first; coins, a shop and gear would add a second system on top of it. Account update is now display name and password only, which is what the course requires.

**What I am giving up:** Pattern Reader's "how predictable am I?" idea, and (for now) gear as a reward. Part of Pattern Reader survives: the higher ranks use the same human-pattern research (win-stay, lose-shift) to make the computer harder.

**Known risk taken on:** Knight, Archer, Wizard rules are not as obvious as rock paper scissors. History shows confusing rules hurt these games (source 9: the mushi-ken slug). Response: the rule triangle is always shown on screen during a match.

**Open question:** Without gear, is the next rank enough reason to play another match? This becomes the creative experiment (see experiment.md).
