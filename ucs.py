import queue as Q
import pandas as pd
import numpy as np

from puzzle_rules import *

class UniformCostSearch():

    # get_Start_State is useless
    # just use np.loadtxt('file', delimiter=' ')
    # like i did in puzzle_rules or just use it from there, but need to separate each line/puzzle
    # you do it

    def _init_(self):
        self.start_State = self.get_Start_State("file")
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
        
    def ucs(self, start_State):
        if len(self.start_State) > 0:

            # iterate all the puzzles in file
            for i in range(len(self.start_State)):      
                self.goal = True # placeholder
                if self.start_State[i] == self.goal: #if initial state is equal to goal, end ucs
                    return "Already at goal state" 

              # self.open_State.put(cost, moved_tile, curr_puzzle, path) # parent node, priority queue 
                self.open_State.put(0, 0, self.start_State[i], [0,0])  # initial-state: (Path-Cost=0, moved_tile=0, curr _puzzle = Starting Puzzle, Path = [0,0])     

                while not self.open_State.empty():
                    self.visited_State = self.open_State.get() #pop first element with lowest cost in priority queue

                    # apply goal function
                    if(self.goal is True):
                        self.closed_State.append(self.visited_State) #put the last visited node in closed list
                        return self.closed_State, self.open_State #return solution path
                    
                    if self.visited_State not in self.closed_State:
                         self.closed_State.append(self.visited_State) #put visited state in closed state
                         possible_Moves = self.visited_State.get_children()
                         for route in possible_Moves:
                            if (route not in self.closed_State) and not self.open_State:  # check if the child is in closed list or open priority queue
                                self.open_State.put(route)
                            elif self.open_State: # if the child in priority queue has higher PATH-COST than this child, replace it
                                if route.cost < self.open_State.cost: # TODO: find a way to get cost from priority queues
                                    self.open_State.get(index)
                                    self.open_State.put(route)

                
        return None
                    
                    

