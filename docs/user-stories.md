# Five user stories

1. **Account.** As a new player, I want to create an account and log in, so that my rank and unlocks are saved.
   - Accept: registering with a valid email and password creates a user at Recruit rank with 0 coins and the starter look; a duplicate email is rejected with a clear message; a wrong password does not log in.
2. **Game.** As a logged-in player, I want to play a best-of-5 match of Knight, Archer, Wizard against the computer, so that I can win and climb.
   - Accept: each round I pick one of three fighters and see the computer's pick and the round winner; the rule triangle is visible the whole match; the match ends when one side wins 3 rounds; my equipped gear is shown on my fighters.
3. **Saved result.** As a player, I want my match result saved with my rank change and reward, so that every win moves me forward.
   - Accept: finishing a match saves the outcome, rounds won/lost and coins earned; a win adds a star and a loss removes one (never below the current rank's floor); reaching the star target moves me up a rank and unlocks an item; leaving mid-match saves nothing.
4. **Dashboard.** As a returning player, I want a dashboard of my progress, so that I can see how close I am to the next rank and unlock.
   - Accept: the dashboard shows my rank, stars toward the next rank, coins, win rate, current streak, my last 10 matches newest first, and my gear collection; with no matches yet it shows a prompt to play.
5. **Account update.** As a player, I want to equip gear I have unlocked and change my profile details, so that my fighters and account look the way I want.
   - Accept: I can equip any unlocked item on its fighter and see it in my next match; I cannot equip locked items; I can buy an item if I have enough coins; I can change my display name; changing my password requires the current one.
