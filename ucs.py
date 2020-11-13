import queue as Q
import pandas as pd
import numpy as np

from puzzle_rules import Rules

class UniformCostSearch():

    def __init__(self):
        self.start_State = []
        self.visited_State = ()
        self.closed_State = []  # list of visited states
        self.open_State = Q.PriorityQueue()  # priority queue ordered by total cost

    def get_PQ_Content(self, pq):
        self.content = []
        while not pq.empty():
            self.content.append(pq.get())
        
        return self.content

    def compare_Cost(self, child_cost, child_state, pq):
        self.content = self.get_PQ_Content(pq) # put priority queue content in list

        if len(self.content) != 0:
            for cost in self.content:
                if child_state == cost[2]: # get puzzle state in list
                    if child_cost < cost[0]: # get cost value in list
                        return True
                    else:
                        return False

    def replace_Cost(self, child_cost, child_state, pq):
        self.content = self.get_PQ_Content(pq) # put priority queue content in list
        self.new_pq = Q.PriorityQueue()
        if len(self.content) != 0:
            for cost in self.content:
                if child_state == cost[2]: # get puzzle state in list
                    if child_cost < cost[0]: # get cost value in list
                        cost[0] = child_cost
                        self.new_pq.put(cost)
                else:
                    self.new_pq.put(cost)
        return self.new_pq


    def printPath(self):
        print("hello")
    
    # initial_State = self.get_Start_State("file")
    def ucs(self, initial_State):
        print("entered ucs")
        if len(initial_State) > 0:
            print("entered first if")
            # iterate all the puzzles in file
            for i in range(len(initial_State)):
                print(initial_State[i])
                rl = Rules(initial_State[i])
                if rl.checkGoal(): #if initial state is equal to goal, end ucs
                    return print("Already at goal state") 

                self.open_State.put([0, 0, initial_State[i], [0,0]])  # initial-state: (Path-Cost=0, moved_tile=0, curr _puzzle = Starting Puzzle, Path = [0,0])     

                while not self.open_State.empty():
                    print("entered while loop")
                    self.cost, self.moved_tile, self.visited_State, self.path = self.open_State.get() #pop first element with lowest cost in priority queue

                    # apply goal function
                    if rl.checkGoal():
                        self.closed_State.append(self.visited_State) #put the last visited node in closed list
                        self.path.append((self.moved_tile, self.cost))
                        return print(self.path) #return solution path
                    
                    if self.visited_State not in self.closed_State:
                         self.closed_State.append(self.visited_State) #put visited state in closed state
                         self.possible_Moves = rl.generate_moves()
                         while not self.possible_Moves.empty():
                            self.child_cost, self.child_moved_tile, self.child_State = self.possible_Moves.get()
                            if (self.child_State not in self.closed_State) and not self.open_State:  # check if the child is in closed list or open priority queue
                                self.path.append(self.moved_tile, self.cost)
                                self.open_State.put([self.child_cost, self.child_moved_tile, self.child_State, self.path])
                            elif self.open_State: # if the child in priority queue has higher PATH-COST than this child, replace it
                                if self.compare_Cost(self.child_cost, self.child_State, self.open_State): 
                                    self.open_State = self.replace_Cost(self.child_cost, self.child_State, self.open_State)


        return None

def get_Start_State(puzzle_file):
    input_file = np.loadtxt(puzzle_file, delimiter=' ')
    puzzle_list = []
    for i in range(input_file.ndim+1):
        puzzle_list.append(input_file[i].reshape(2,4)) # reshape 1D array(s) to 2x4 (row x col) 2D array
    return puzzle_list

def main():
    initial_States = get_Start_State("samplePuzzles.txt")
    solve = UniformCostSearch()
    solve.ucs(initial_States)

if __name__ == '__main__':
    main()