# Planned checks: keyboard, phone, privacy, usage

Decided 2026-11-23. All checks below are **planned**; none has been run yet.

| Check | How | Passes if | Status |
|---|---|---|---|
| Keyboard | Play a full match and change the display name using only Tab, Enter and arrow keys | Every action is reachable and the focused control is always visible | NOT RUN |
| Phone layout | Play a match on a real phone; Playwright run at 375 px wide | No sideways scrolling; fighter buttons are large enough to tap; no scrolling during a match | NOT RUN |
| Private data | Passwords stored only as Werkzeug hashes; sessions revoked on password change; every query filtered by the signed-in user's id; a two-user test requests the other player's match; `.env` and local databases kept out of Git | Player B gets "not found" for player A's match; old sessions fail after a password change | NOT RUN |

## Usage measure
**Matches per session:** how many matches a player starts in one visit. This is the number the "almost there" experiment (experiment.md) tries to move.

## Analytics option
**Chosen: GoatCounter.** Free for non-commercial use, open source, no cookies and no personal data, so no cookie banner is needed. Pricing and terms to be re-checked on goatcounter.com before installing.

Compared with:
- Plausible: privacy-friendly but paid after a trial.
- Google Analytics: free, but uses cookies and needs a consent notice.

Not installed at this checkpoint (the Plan review only asks to name the option). Only page views and a "match started" event would be sent; never usernames or match data.
