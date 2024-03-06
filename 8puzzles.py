import math 
from collections import deque
import queue
import heapq
import tkinter as tk
from tkinter import ttk
import time


path = []
cost = 0

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




class MyGUI():
    def __init__(self, root, board_state:'BoradState'):
        self.root = root
        self.board_state = board_state
        self.setGui()

    def setGui(self):
        self.root.geometry("800x550")
        self.root.title("8 Puzzle")
        self.root.configure(bg="#CCFFFF")
        self.label = tk.Label(self.root, text="8 Puzzle", font=('Goudy Stout', 30), foreground="#0571B0",
                              background="#CCFFFF")
        self.label.pack(padx=10)
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="#404040")
        self.canvas.pack(pady=20, padx=20)

        self.search_label = tk.Label(self.root, text="Search Algorithm:", font=('Arial', 12), bg="#CCFFFF")
        self.search_label.pack(pady=5)
        self.search_var = tk.StringVar()
        self.search_combobox = ttk.Combobox(self.root, textvariable=self.search_var,
                                                      values=["DFS", "BFS", "A* manhattan", "A* euclidean"], state="readonly",font=('Arial', 11))
        self.search_combobox.current(0)
        self.search_combobox.pack(pady=5)

        self.button = tk.Button(self.root, text="Search", bg="#009292", anchor="center", width=20, font=('Arial', 13))
        self.button.pack(pady=20, padx=20)
        self.display_matrix(self.board_state)
        self.button.bind("<Button-1>", lambda event: self.runSearch())

    def runSearch(self):
        search_algorithm = self.search_var.get()

        if search_algorithm == "DFS":
            goal = DFS(self.board_state)
            self.display_matrix(goal.current_board)
            printStatistics()
        elif search_algorithm == "BFS":
            goal = BFS(self.board_state)
            self.display_matrix(goal.current_board)
            printStatistics()
        elif search_algorithm == "A* manhattan":
            goal = AStar(self.board_state, 0) 
            self.display_matrix(goal.current_board) 
            printStatistics()
        else:
            goal = AStar(self.board_state, 1) 
            self.display_matrix(goal.current_board) 
            printStatistics()




    def display_matrix(self, matrix):
        cell_width = 100
        cell_height = 100
        for i in range(3):
            for j in range(3):
                x0 = j * cell_width
                y0 = i * cell_height
                x1 = x0 + cell_width
                y1 = y0 + cell_height
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                if matrix[i][j] != 0:
                    self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(matrix[i][j]), font=('Arial', 13))






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
    global start_time
    start_time= time.time()
    init_state = BoardState(init_board, None, None)
    frontier = deque()
    explored = set()
    frontier.append(init_state)

    while not isEmpty(frontier):
        count += 1
        state = frontier.pop()
        explored.add(state)
        # state.printState()
        
        if finished(state):
            path.append(state)
            while state.prev_state != None:
                state = state.prev_state
                path.append(state)    
            global end_time
            end_time= time.time()          
            return path[0]
        
        actions = state.getAllAction()
       
        for action in actions:
            new_state = state.takeAction(action)
            if (( not new_state.isIn(explored)) and (not new_state.isIn(frontier))):
                frontier.append(new_state)
                # print()
                # print(action)
                # print()

    return None



def BFS(init_board):
    global start_time
    start_time= time.time()
    init_state = BoardState(init_board, None, None)
    frontier = queue.Queue()
    explored = set()
    frontier.put(init_state)
    count = 0
    while not frontier.empty():
        count += 1
        print()
        state = frontier.get()
        explored.add(state)
        # state.printState()
        if finished(state):
            path.append(state)
            while state.prev_state != None:
                state = state.prev_state
                path.append(state)
            global end_time
            end_time= time.time()       
            return path[0]
        
        actions = state.getAllAction()
       
        for action in actions:
            new_state = state.takeAction(action)
            if ( not inQueue(new_state, frontier)) and ( not new_state.isIn(explored)):
                frontier.put(new_state)
                # print()
                # print(action)
                # print()
                
    return None


def AStar(init_board, flag):
    global start_time
    start_time= time.time()
    init_state = BoardState(init_board, None, None)
    frontier = []
    heapq.heapify(frontier)
    explored = set()
    heapq.heappush(frontier, init_state)
    count = 0
    while len(frontier) != 0:
        count += 1
        state = heapq.heappop(frontier)
        explored.add(state)
        # state.printState()
        if finished(state):
            path.append(state)
            while state.prev_state != None:
                state = state.prev_state
                path.append(state)
            global end_time
            end_time= time.time()     
            return path[0]
        
        actions = state.getAllAction()
       
        for action in actions:
            new_state = state.takeAction(action)
            if flag == 1:
                new_state.manhattan()
            elif flag == 0:    
                new_state.euclidean()
            if (( not new_state.isIn(explored)) and (not new_state.isIn(frontier))):
                heapq.heappush(frontier, new_state)
                # print()
                # print(action)
                # print()
                
    return None



def printStatistics():
    total_time = end_time - start_time
    print("path:\n")
    path.reverse()
    for state in path:
        print()
        state.printState()
        print()
    print(f"cost equals: {cost}")   
    print(f"time equals: {total_time}")  



def main():
    
    init_board = [
        [1, 2, 5],
        [3, 4, 0],
        [6, 7, 8]
    ]
  
    root = tk.Tk()
    gui = MyGUI(root, init_board)
    root.mainloop()
    
if __name__ == "__main__":
    main()
