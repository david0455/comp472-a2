import queue as Q
import pandas as pd

class UniformCostSearch():

    def _init_(self):
        self.start_State = get_Start_State("file")
        self.visited_State = ()
        self.closed_State = []  # list of visited states
        self.open_State = Q.PriorityQueue()  # priority queue ordered by total cost

    def get_Start_State(self, puzzle_file):
        self.puzzle = pd.read_csv(puzzle_file, sep=" ", header=None)
        self.puzzle_list = []
        for i in range(self.puzzle.ndim+1):
            list.append(self.puzzle[i].reshape(2,4)) # reshape 1D array(s) to 2x4 (row x col) 2D array
        return self.puzzle_list

    def get_children(self):
        print("hello")
        # TODO: Create method to get children (all possible moves) of node zero

    def calc_cost(self):
        print("hello")
        # TODO: Calculate cost of move
        
    def ucs(self):
        if len(self.start_State) != 0:
            # iterate all the puzzles in filebe
            for i in len(self.start_State):          
                self.goal = True # placeholder
                self.open_State.put((cost, (currentState, moves))) #parent node

                while not self.open_State.empty():
                    self.visited_State = self.open_State.get() #pop first element in priority queue

                    if(self.goal is True):
                        return self.closed_State
                    
                    if currState not in self.closed_State:
                         self.closed_State.append(self.visited_State) #put visited state in closed state
                         possible_Moves = self.visited_State.get_children()
                         for route in possible_Moves:
                             self.open_State.put((cost, (currState, moves)))

                

                    
                    

