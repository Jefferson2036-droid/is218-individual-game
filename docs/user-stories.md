# Five user stories

Rewritten 2026-11-23 for the narrowed promise (no coins or gear). Each check has an observable result so a test or a classmate can confirm it.

**Unit of a saved result:** one finished best-of-5 **match**, not a round. Tied rounds are replayed, so a match always ends in a win or a loss; the dashboard therefore shows **wins and losses only** (no ties).

## 1. Join and leave safely
As a new player, I want to sign up, sign in and sign out, so that my climb is mine and stays private.
- Signing up with a new username and password starts me at Recruit with 0 stars.
- A duplicate username or a wrong password shows a clear error and does not sign me in.
- After signing out, opening the dashboard or calling the data API is refused.

## 2. Play a match
As a signed-in player, I want to play a best-of-5 Knight/Archer/Wizard match against the computer, so that I can try to climb.
- Each round shows both picks and the correct winner; the rule triangle is visible the whole match.
- The server decides every round from my validated pick and the computer's pick; a browser claiming "I won" is ignored.
- An invalid pick is rejected with a message; the match ends when one side reaches 3 round wins.
- The match is playable on a phone without scrolling and with the keyboard only.

## 3. Save the result and climb
As a player, I want each finished match saved with its rank change, so that every win moves me forward.
- A finished match saves win/loss, the round score, and rank and stars before and after.
- A win adds 1 star; a loss removes 1 star but never drops below the floor of my current rank; reaching the star target moves me up a rank.
- A match abandoned midway saves nothing and changes no stars.
- The saved result is still there after a refresh and after signing in again.

## 4. See my private dashboard
As a returning player, I want a dashboard of my progress, so that I know how close the next rank is.
- It shows stars to the next rank first, then rank, wins and losses, current win streak, and my last 10 matches newest first.
- A brand-new player sees a "play your first match" message instead of empty tables.
- Player B can never see or change player A's matches or account, even by changing an ID in a request.

## 5. Maintain my account
As a player, I want to change my display name and password, so that my account stays mine.
- A new display name shows on the dashboard; a blank or too-long name is rejected.
- Changing the password requires the current password; a wrong current password is rejected.
- After a password change the old password fails, my other sessions are signed out, and the new password works.
