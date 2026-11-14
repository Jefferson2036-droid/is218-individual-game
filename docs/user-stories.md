# Five user stories

For the chosen concept (Pattern Reader). Draft; adjust if the concept or audience changes.

1. **Account.** As a new player, I want to create an account and log in, so that my matches are saved under my name.
   - Accept: registering with a valid email and password creates a user; a duplicate email is rejected with a clear message; a wrong password does not log in.
2. **Game.** As a logged-in player, I want to play a 20-round match of rock paper scissors against a computer that tries to predict me, so that I can test how predictable I am.
   - Accept: each round I pick one of three moves and see the computer's move and who won; the round counter and running score are visible; the match ends after round 20.
3. **Saved result.** As a player, I want my match saved when it ends, so that I do not lose it.
   - Accept: finishing a match stores one result (wins, losses, ties, predictability score, date) linked to my account; it is still there after I log out and back in; an unfinished match is not saved.
4. **Dashboard.** As a returning player, I want a dashboard of my past matches, so that I can see whether I am getting harder to predict.
   - Accept: the dashboard lists only my matches, newest first; it shows my overall win rate and my predictability score per match; with no matches yet it shows a prompt to play.
5. **Account update.** As a player, I want to change my display name and password, so that my account stays current.
   - Accept: a new display name appears on the dashboard; a new password works at next login and the old one does not; changing the password requires the current one.
