[Play Connect 4 Game](https://jakeh766.github.io/portfolio/assets/Connect4/build/web/index.html)

I developed a Connect 4 game using Python and implemented the minimax algorithm with alpha-beta pruning to maximize efficiency. The game has three different levels: Beginner, Intermediate, and Expert. Each level differs in the depth of moves the computer evaluates. For example, a depth of two means that the computer searches and evaluates each possible board state two moves ahead. Below is a table showing the search depth of each level:

| Level | Depth |
| --- | --- |
| Beginner | 2 |
| Intermediate | 4 |
| Expert | 6 |

There are four directions that a player can win in Connect 4: vertical, horizontal, positive-sloped diagonal, and negative-sloped diagonal. To evaluate a board position, the program segments the board into windows of length 4 (Each window contains 4 holes) in each direction. Then the Connect 4 AI follows a heuristic scoring approach for each window that has been fine-tuned by trial and error. Additionally, the number of pieces in the center column is also scored, as the center column provides the most branching options to get 4 in a row. The table below outlines the heuristic scoring approach:

| Condition | Score |
| --- | --- |
| Four in a row | + &infin; |
| Three in a row with one empty spot | + 5 |
| Two in a row with two empty spots | + 2 |
| Opponent has three in a row with one empty spot | - 4 |
| Opponent has two in a row with two empty spots | - 1 |
| Opponent has four in a row | - &infin; |
| Piece in center column | + 3 |
| Opponent piece in center column | - 2 |

The following GIF illustrates how the AI would evaluate this specific position for yellow.

![Scoring](/assets/Connect4/Connect4Scoring.gif)

The next GIF shows how the AI (yellow piece) would pick the optimal move after red starts the game by placing a piece in the center. 

![Minimax](/assets/Connect4/Connect4GIF.gif)

In the GIF, the circled boards are pruned, meaning there is no point in evaluating them because alpha is greater than beta.

Inspiration for this project came from Keith Galli's Youtube series: [Keith Galli's Youtube Series](https://www.youtube.com/playlist?list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV)

Additional resources for Minimax Algorithm:
- [Sebastian Lague's Youtube Video](https://www.youtube.com/watch?v=l-hh51ncgDI)
- [Wikipedia Page](https://en.wikipedia.org/wiki/Minimax)
