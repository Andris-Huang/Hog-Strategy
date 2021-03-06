# Hog

## Abstract
This project is an interactive game completed as a class project in \textit{CS 61A: Structure and Interpretation of Computer Programs} at UC Berkeley. This game is adapted from the traditional dice game, Hog, in which two players take turn to row dice, and the first player who gets 100 points win the game. The final version of the game requires the players need to follow the following four rules:
1. Sow Sad. If any of the dice outcomes is a 1, the current player's score for the turn is 1.
2. Piggy Points. A player who chooses to roll zero dice scores k+3 points, where k is the digit in the squared opponent’s score that has the lowest value.
3. More Boar. First, the points for the turn are added to the current player’s score. Then the current player takes another turn if the leftmost digit of the current player's score is smaller than the leftmost digit of the opponent's score and the second leftmost digit of the current player's score is smaller than the second leftmost digit of the opponent's score. If either score is only a singular digit, assume it has a 0 in front of it (e.g. 1 -> 01, 6 -> 06). You may not assume that the scores are under 100. The More Boar calculation should be done on the current player's score after the points from the current turn are added.
4. Time Trot. A turn involves a player rolling dice, and each turn is numbered, starting from 0. If a player chooses to roll a number of dice k on turn n, and n % 8 == k, then that player gets an extra turn immediately after the current turn. However, a player cannot get an extra turn as a consequence of Time Trot immediately after an extra turn, though they can get an extra turn as a consequence of More Boar. Furthermore, players will roll 8-sided dice on all extra turns (including those produced from More Boar).

Source: https://cs61a.org/proj/hog_contest/

## Final Strategy
The \textit{final_strategy} section of this project is an optional part, in which we are asked to come up with a best winning strategy. My strategy adapts the method of Monte Carlo Tree Search (MCTS), following these four steps: Selection, Expansion, Simulation, and Backpropagation. This method simulates all the possible children of the root (i.e. possible game states outcomes) and picks the best best child (next move) based on statistics modeled by the following equation:
```math
UCT(vi, v) = Q(vi)/N(vi) + c * sqrt(log(Nv)/N(vi))
```
where the c parameter used in this code is sqrt(2) = 1.4. 

## Acknowledgement:
Although I do not have any other collaborator, the theory behind MCTS is definitely beyond my current scope. The introduction to the algorithm and some instructions for implementation were found from int8.io, and I was also inspired by the MCTS on Tic Tac Toe, implemented by int8.

## Date
23 February, 2021
