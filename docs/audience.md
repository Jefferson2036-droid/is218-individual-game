# Audience

Two audience/presentation approaches compared, then one chosen. Both are hypotheses to check with real players, not facts about every student.

| | A: Quick competitor (chosen) | B1: Daily ritual player |
|---|---|---|
| Who | College students filling a few minutes between classes | Students who play one short game a day as a habit |
| Reference game | 2048: simple rules, short runs, "one more try" | Wordle: one puzzle a day, a streak, a shareable result |
| How often they play | As many matches as they want, in short bursts | One ranked run per day |
| Device | Phone first, laptop works | Phone first |
| What the battle screen emphasizes | Fast best-of-5 match, rank bar, how close the next rank is | The single daily run and its result |
| What the dashboard leads with | Current rank and progress, win rate, streak, recent matches | Daily streak and calendar, shareable result |
| What gets saved | Every match: result, rounds won/lost, rank before/after | One run per day: result and streak |
| Why come back | The next rank is always close | Don't break the streak |
| Risk | Rank alone may not be enough reward once gear is out of scope | One run a day may feel too little; hard to see "play again" behavior in a playtest |

## Decision
**Chosen audience:** A, the quick competitor. Decided 2026-11-23.

**Why:** It fits the rank climb I chose for Arena Climb: like 2048, the loop is short and the next goal is always close. It can also be tested this week: classmates can play several matches on their phones and I can watch whether they choose to play again. With B1's one run per day, a playtest can't show that.

**What I am giving up:** B1's daily streak and shareable result. The daily streak is kept in the [backlog](backlog.md) as a possible future feature.

**Design rules that follow from this choice:**
- The battle screen must work on a phone, one-handed, with no scrolling during a match.
- One match should take about one minute.
- The dashboard shows how close the next rank is first.

**Who this game is not for:** players wanting a long story, real-time play against other people, or a once-a-day ritual.

**Evidence still needed:** watch 3–5 classmates play on their phones and record whether they choose another match (see experiment.md). NOT RUN.
