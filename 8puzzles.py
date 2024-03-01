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
       
        # Check if valid move    
        if self.checkAction(action) == False:
            return None
        
        new_board = self.current_board.copy()
        
        if action == 'U':
            new_board[self.zero_index[0]][self.zero_index[1]], new_board[self.zero_index[0] - 1][self.zero_index[1]]  = new_board[self.zero_index[0] - 1][self.zero_index[1]], new_board[self.zero_index[0]][self.zero_index[1]] 
        elif action == 'D':
            new_board[self.zero_index[0]][self.zero_index[1]], new_board[self.zero_index[0] + 1][self.zero_index[1]]  = new_board[self.zero_index[0] + 1][self.zero_index[1]], new_board[self.zero_index[0]][self.zero_index[1]] 
        elif action == 'L':
            new_board[self.zero_index[0]][self.zero_index[1]], new_board[self.zero_index[0]][self.zero_index[1] - 1]  = new_board[self.zero_index[0]][self.zero_index[1] - 1], new_board[self.zero_index[0]][self.zero_index[1]] 
        elif action == 'R':
            new_board[self.zero_index[0]][self.zero_index[1]], new_board[self.zero_index[0]][self.zero_index[1] + 1]  = new_board[self.zero_index[0]][self.zero_index[1] + 1], new_board[self.zero_index[0]][self.zero_index[1]] 
                
        new_state = BoardState(new_board, self, action)

        return new_state
    
    def getAllAction(self):
        available_actions = []
        for i in ['U', 'D', 'L', 'R']:
            if self.checkAction(i) == True:
                available_actions.append(i)
        
        return i
    
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
    
        
def main():
    
    init_board = [
        [4, 1, 2],
        [3, 0, 5],
        [6, 7, 8]
    ]
    
    init_state = BoardState(init_board, None, None)
    init_state.printState()
    print()
    state2 = init_state.takeAction('D')
    state2.printState()
    
    
if __name__ == "__main__":
    main()
        