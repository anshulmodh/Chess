# Chess Application

Disclaimer -> This progam was initially created as my final term project for 15-112 Fundamentals of Computer Science at Carnegie Mellon University during the Summer of 2017. This program is a work in progress and is constantly being updated

Chess is a game that allows the player to play the classical game of chess either with another player or against an AI. There are three modes on the start screen: 2-player mode, AI-mode, the help menu, and the custom game mode. All modes have timers that are automatically activated for the respective player and pause when in the pause screen. The pause screen can be accessed by pressing 'p' at any moment, or by clicking the pause button in the upper right-hand corner. In the pause screen, you can choose to resume playing or to go back to the start menu, reseting your game. If you are playing against the AI, you can choose difficulty level between easy, medium, or hard. You can exit the pause menu by pressing 'p' again or hitting the escape key. The game will moniter a player's dead pieces in the margin of the screen. In the custom game setting, you can change the size of the board and the number of pieces in play. Drag and drop pieces from the table below onto the board. You can trash pieces to the side. The number of rows and columns can be changed using the text boxes to the top as long as 3 < n < 20 for screen size purposes. Then, click the start button at the top left and select whether you want to play your custom game against another player or against the AI.

# Pre-Requisites 
1. Python 3
2. Pygame

You can install pygame using pip by running the command:
```
$ pip install pygame
```

# Gameplay Features
1. Automatic Timers
2. Castling
3. Pawn Promotion
4. En Passant
5. Move Validation
6. Check Validation
7. Checkmate Validation

# AI Features
1. MiniMax Algorithm
2. Alpa-Beta Pruning
3. Heuristic Evaluation(In-Development)
4. 3 difficulty levels -> Easy - predicts up to 3 moves ahead, Medium - 7 moves, Hard - 15 moves

# How to Run
Clone the source locally:

`$ git clone https://github.com/anshulmodh/Chess.git`

Run the Main.py file:

`Python Main.py`
