# Sources

Gathered 2026-11-13 with Claude, through web search. Summaries are in my own words.

| # | Source (title + link) | Date looked at | What I took from it | Used in |
|---|---|---|---|---|
| 1 | Gabriel Dance & Tom Jackson, "Rock-Paper-Scissors: You vs. the Computer", The New York Times (2010) — https://www.nytimes.com/interactive/science/rock-paper-scissors.html (found via encyclopedia.pub reference list and news coverage) | 2026-11-13 | The closest existing game to Concept B. The computer studies your moves and predicts your next throw; it has a "novice" mode that learns only from you and an "expert" mode built on past games. It narrates whether it predicted you correctly. Not opened directly — page may need a NYT login. | concepts.md, experiment.md |
| 2 | Kotaku, "Can you beat a computer at one of the world's oldest games" — https://kotaku.com/can-you-beat-a-computer-at-one-of-the-worlds-oldest-gam-5778598 | 2026-11-13 | A player's account of the NYT game: the novice computer first learned the rules, then started finding patterns in his play. Shows the "learning opponent" idea is understandable to ordinary players. | concepts.md |
| 3 | MIT Technology Review, "How to Win at Rock-Paper-Scissors" (2014) — https://www.technologyreview.com/2014/04/30/13423/how-to-win-at-rock-paper-scissors/ | 2026-11-13 | Reports a Zhejiang University study: 360 students in groups of six played 300 rounds each, paid per win. Players were not random. | concepts.md, experiment.md |
| 4 | Business Standard / PTI, "How to win at rock-paper-scissors discovered" — https://www.business-standard.com/article/pti-stories/how-to-win-at-rock-paper-scissors-discovered-114050500615_1.html | 2026-11-13 | Same study: winners tend to repeat their winning move; losers tend to switch to the next move in rock → paper → scissors order ("win-stay, lose-shift"). This is the simplest pattern my predictor can look for. | flow.md, experiment.md |
| 5 | Wang, Xu & Zhou, "Social Cycling and Conditional Responses in the Rock-Paper-Scissors Game", arXiv:1404.5199 — http://arxiv.org/abs/1404.5199 (cited by Cornell INFO 2040 blog and Phys.org) | 2026-11-13 | The original paper behind sources 3–4. Not read in full yet. | (to read) |
| 6 | Wolfram MathWorld, "Rock-Paper-Scissors-Lizard-Spock" — https://mathworld.wolfram.com/Rock-Paper-Scissors-Lizard-Spock.html | 2026-11-13 | Five-move version (Concept A): each move beats two others and loses to the other two. | concepts.md |
| 7 | "What Is Rock Paper Scissors Lizard Spock?" — https://crash-web.pages.dev/blog/rock-paper-scissors-lizard-spock/ | 2026-11-13 | Created by Sam Kass and Karen Bryla to reduce ties; 10 rules in total; ties drop to about 1 in 5. Supports Concept A's "fewer ties" claim and its "ten rules to remember" risk. | concepts.md |

| 8 | Wikipedia, "Sansukumi-ken" — https://en.wikipedia.com/wiki/Sansukumi-ken | 2026-11-13 | Japanese three-way hand games ("the three who are afraid of one another"). Rock paper scissors is one of the few still played; one scholar credits its success to how simple and easy to understand it is. Lesson: the three objects must have obvious rules. | concepts.md, game-design.md |
| 9 | Anime News Network, "Why Does Rock-Paper-Scissors Come Up In Anime So Much?" — https://www.animenewsnetwork.com/answerman/2017-11-22/.124355 | 2026-11-13 | The earliest variant had a slug beating a snake, which made little sense and is thought to be a mistranslation of "poisonous centipede". Example of what confusing rules look like. | concepts.md |
| 10 | Wikipedia, "Rock paper scissors" (kitsune-ken section) — https://Www.Wikipedia.org/wiki/Janken | 2026-11-13 | Kitsune-ken used characters (fox, village head, hunter) instead of objects. Precedent for a character-based theme like Knight, Archer, Wizard. | concepts.md |
| 11 | Campus.sg, "Rock paper scissors and ji gu pa are more than just games" — https://www.campus.sg/rock-paper-scissors-and-ji-gu-pa-are-more-than-just-games-campus-sg | 2026-11-13 | Modern "Bear, Hunter, Ninja" variant (hunter shoots bear, bear eats ninja, ninja beats hunter). Shows people enjoy re-themed versions with characters. | concepts.md |
| 12 | Defector, "What is the correct way to count off in rock paper scissors" — https://defector.com/what-is-the-correct-way-to-count-off-in-rock-paper-scissors | 2026-11-13 | Indonesian variant: elephant beats human, human beats ant, ant scares elephant. Another living themed variant. | concepts.md |

| 13 | Quaternius, "LowPoly RPG Characters" (OpenGameArt) — https://opengameart.org/content/lowpoly-rpg-characters | 2026-11-13 | Free animated low-poly wizard, warrior, rogue, monk and ranger, CC0 license. Planned source for the Wizard and Archer. | art-pipeline.md |
| 14 | Quaternius, "LowPoly Animated Knight" — https://quaternius.itch.io/lowpoly-animated-knight | 2026-11-13 | Free animated knight, CC0. Planned source for the Knight. | art-pipeline.md |
| 15 | Cinevva, "Free Medieval and Fantasy 3D Models" — https://app.cinevva.com/game-assets/free-medieval-3d-models | 2026-11-13 | Explains CC0 (public domain, no credit required) for Kenney, Quaternius, KayKit and others. | art-pipeline.md |
| 16 | three.js docs, "Loading 3D Models" — https://threejs.org/manual/en/loading-3d-models | 2026-11-13 | How to load a glTF model into a browser scene with GLTFLoader. For the real-time 3D stretch goal. | stack.md |

## What the evidence says about the two concepts
- **Re-theming the three objects has a long history** (sources 8–12), so Knight, Archer, Wizard is a known kind of variation, not a gimmick.
- **The risk is unclear rules** (sources 8–9). The design answers this by always showing the rule triangle.
- **The learning-opponent research (sources 1–5) is reused** to make higher ranks harder, which is how "gets harder as you win" is built.
- **Not answered by any source:** whether cosmetic unlocks are enough reason to keep playing. That is the creative experiment.
