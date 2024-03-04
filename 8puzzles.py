import math 
from collections import deque
import queue
import heapq


path = []

class BoardState:
    def __init__(self, current_board:list, prev_state:'BoardState', prev_action):
        self.current_board = current_board
        self.zero_index = self.getZeroIndex()
        self.prev_state = prev_state
        self.prev_action = prev_action
        self.cost = 0

    def __lt__(self, other):
        return self.cost < other.cost

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

        # random.shuffle(available_actions)

        return available_actions
    
    def printState(self):
        for i in range(3):
            for j in range(3):
                print(self.current_board[i][j], end="\t")
            print()


    def manhattan(self):
        manhattan_dist = 0
        for i in range(3):
            for j in range(3):
                if (i*3 + j) != self.current_board[i][j]:
                    index1, index2 = findIndex(self.current_board, i*3 + j)
                    manhattan_dist += abs((i - index1))+ abs((j - index2))
        self.cost += manhattan_dist
        return manhattan_dist            


    def euclidean(self):
        euclidean_dist = 0
        for i in range(3):
            for j in range(3):
                if (i*3 + j) != self.current_board[i][j]:
                    index1, index2 = findIndex(self.current_board, i*3 + j)
                    euclidean_dist += math.sqrt(math.pow((i - index1), 2)+ math.pow((j - index2), 2))
        
        self.cost += euclidean_dist
                    
        return euclidean_dist            


    def isEqual(self, state):
        for i in range(3):
            for j in range(3):
                if self.current_board[i][j] != state.current_board[i][j]:
                    return False
        return True      

    def isIn(self,explored):
        for state in explored:
            if self.isEqual(state):
                return True
        return False    


def findIndex(board:'BoardState', target):

    for i, row in enumerate(board):
        for j, num in enumerate(row):
            if num == target:
                return ( i, j) 
    return (None, None)        


def inQueue(state:'BoardState',frontier:queue):
    temp = queue.Queue()
    while not frontier.empty():
        temp.put(frontier.get())
    while not temp.empty():
        my_state = temp.get()
        frontier.put(my_state)
        if state.isEqual(my_state):
            return True
    return False    



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
        # print(count)
        count += 1
        # print()
        state = frontier.pop()
        explored.add(state)
        # print()
        # state.printState()
        
        if finished(state):
            path.append(state)
            while state.prev_state != None:
                state = state.prev_state
                path.append(state)            
            return True
        
        actions = state.getAllAction()
       
        for action in actions:
            new_state = state.takeAction(action)
            if (( not new_state.isIn(explored)) and (not new_state.isIn(frontier))):
                frontier.append(new_state)
                # print()
                # print(action)
                # print()

    return False



def BFS(init_board):
    init_state = BoardState(init_board, None, None)
    frontier = queue.Queue()
    explored = set()
    frontier.put(init_state)
    count = 0
    while not frontier.empty():
        print(count)
        count += 1
        print()
        state = frontier.get()
        explored.add(state)
        print()
        state.printState()
        if finished(state):
            path.append(state)
            while state.prev_state != None:
                state = state.prev_state
                path.append(state)
            return True
        
        actions = state.getAllAction()
       
        for action in actions:
            new_state = state.takeAction(action)
            if ( not inQueue(new_state, frontier)) and ( not new_state.isIn(explored)):
                frontier.put(new_state)
                print()
                print(action)
                print()
                
    return False


def AStar(init_board):
    init_state = BoardState(init_board, None, None)
    frontier = []
    heapq.heapify(frontier)
    explored = set()
    heapq.heappush(frontier, init_state)
    count = 0
    while len(frontier) != 0:
        print(count)
        count += 1
        print()
        state = heapq.heappop(frontier)
        explored.add(state)
        print()
        state.printState()
        if finished(state):
            path.append(state)
            while state.prev_state != None:
                state = state.prev_state
                path.append(state)
            return True
        
        actions = state.getAllAction()
       
        for action in actions:
            new_state = state.takeAction(action)
            # new_state.manhattan()
            new_state.euclidean()
            if (( not new_state.isIn(explored)) and (not new_state.isIn(frontier))):
                heapq.heappush(frontier, new_state)
                print()
                print(action)
                print()
                
    return False



def main():
    
    # init_board = [
    #     [1, 0, 2],
    #     [3, 4, 5],
    #     [6, 7, 8]
    # ]
    
    init_board = [
        [1, 2, 5],
        [3, 4, 0],
        [6, 7, 8]
    ]
    
    init_state = BoardState(init_board, None, None)
    init_state.printState()
    print()
    # print("manhattan ",init_state.manhattan_cost)
    # print("euclidean",init_state.euclidean_cost)
    print(AStar(init_board))

    print("----------------------------------")
    path.reverse()
    for state in path:
        print()
        state.printState()
        print
    
if __name__ == "__main__":
    main()
        