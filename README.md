# 8-Puzzle Solver

## Overview

This problem appeared as a project in the edX course ColumbiaX: CSMM.101x Artificial Intelligence (AI). In this assignment, an agent will be implemented to solve the 8-puzzle game.

An instance of the 8-puzzle game consists of a board holding 8 distinct movable tiles, plus an empty space. For any such board, the empty space may be legally swapped with any tile horizontally or vertically adjacent to it. In this assignment, the blank space is represented with the number 0.

Given an initial state of the board, the search problem is to find a sequence of moves that transitions this state to the goal state; that is, the configuration with all tiles arranged in ascending order 0,1,2,3,4,5,6,7,8.

The search space is the set of all possible states reachable from the initial state. The blank space may be swapped with a component in one of the four directions 'Up', 'Down', 'Left', 'Right', one move at a time. The cost of moving from one configuration of the board to another is the same and equal to one. Thus, the total cost of the path is equal to the number of moves made from the initial state to the goal state.

## Application

### Algorithms

You will need to implement the 8-puzzle search problem using the following three search algorithms:

- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- A* (A-star algorithm)

### Heuristics

For the A* (the informed search), we are going to use the following heuristics and compare between the number of nodes expanded and output paths, and to report which heuristic is more admissible:

1. **Manhattan Distance**:
   It is the sum of absolute values of differences in the goal’s x and y coordinates and the current cell’s x and y coordinates respectively,
   `h = abs(current cell:x - goal:x) + abs(current cell:y - goal:y)`

2. **Euclidean Distance**:
   It is the distance between the current cell and the goal cell using the distance formula
   `h = sqrt((current cell:x - goal:x)² + (current cell.y - goal:y)²)`

   
   ![BFS ](https://github.com/Mohamedragih1/8-puzzle_game/assets/93843532/2ccea681-1b60-4641-add7-96a5fce17030)


