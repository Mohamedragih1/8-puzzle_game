from collections import deque
import random

class BoardState:
    def __init__(self, current_board:list, prev_state:'BoardState', prev_action):
        self.current_board = current_board
        self.zero_index = self.getZeroIndex()
        self.prev_state = prev_state
        self.prev_action = prev_action

    def getZeroIndex(self):
        for i in range(3):
            for j in range(3):
                if self.current_board[i][j] == 0:
                    return (i,j)
        
    def checkAction(self, action):
        if action == 'U' and self.zero_index[0] == 0:
            return False
        elif action == 'D' and self.zero_index[0] == 2:
            return False
        elif action == 'L' and self.zero_index[1] == 0:
            return False
        elif action == 'R' and self.zero_index[1] == 2:
            return False
        else:
            return True
    

    def takeAction(self, action): 
        if not self.checkAction(action):
            return None

        new_board = [row[:] for row in self.current_board]
        
        zero_row, zero_col = self.zero_index

        if action == 'U':
            new_board[zero_row][zero_col], new_board[zero_row - 1][zero_col] = new_board[zero_row - 1][zero_col], 0
        elif action == 'D':
            new_board[zero_row][zero_col], new_board[zero_row + 1][zero_col] = new_board[zero_row + 1][zero_col], 0
        elif action == 'L':
            new_board[zero_row][zero_col], new_board[zero_row][zero_col - 1] = new_board[zero_row][zero_col - 1], 0
        elif action == 'R':
            new_board[zero_row][zero_col], new_board[zero_row][zero_col + 1] = new_board[zero_row][zero_col + 1], 0
                    
        new_state = BoardState(new_board, self, action)

        return new_state

    
    def getAllAction(self):
        available_actions = []
        for i in ['U', 'D', 'L', 'R']:
            if self.checkAction(i) == True:
                available_actions.append(i)

        random.shuffle(available_actions)

        return available_actions
    
    def printState(self):
        for i in range(3):
            for j in range(3):
                print(self.current_board[i][j], end="\t")
            print()
    

def finished(state:BoardState):        
    for i in range(3):
        for j in range(3):
            if (i*3 + j) != state.current_board[i][j]:
                return False
    
    return True

def isEmpty(stack):
    if not stack:
        return True
    else:
        return False


def DFS(init_board):
    init_state = BoardState(init_board, None, None)
    frontier = deque()
    explored = set()
    frontier.append(init_state)
    count = 0
    while not isEmpty(frontier):
        print()
        print(count)
        count += 1
        print()
        state = frontier.pop()
        explored.add(state)
        print()
        state.printState()
        
        if finished(state):
            return True
        
        actions = state.getAllAction()
        print()
        print(actions)
        print()
        for action in actions:
            new_state = state.takeAction(action)
            if (new_state not in frontier) and (new_state not in explored):
                frontier.append(new_state)
                
    return False


def main():
    
    init_board = [
        [1, 0, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]
    
    init_state = BoardState(init_board, None, None)
    init_state.printState()
    print()
    
   
    print(DFS(init_board))
    
if __name__ == "__main__":
    main()
        