import queue as Q
import pandas as pd
import numpy as np
import time

from puzzle_rules import check_goal, generate_children, h0

class AStar():

    def __init__(self):
        self.closed_state = []
        self.open_state = []

    def compare_Cost(self, child_cost, child_state, pq):
        if len(pq) != 0:
            for cost in pq:
                if child_state == cost[3]: # get puzzle state in list
                    if child_cost < cost[0]: # get cost value in list
                        return True
                    else:
                        return False

    def replace_Cost(self, child_cost, child_state, pq):
        if len(pq) != 0:
            for cost in pq:
                if child_state == cost[3]: # get puzzle state in list
                    if child_cost < cost[0]: # get cost value in list
                        cost[0] = child_cost
        return pq

    # calculate total path cost
    def get_path_cost(self, new_cost, old_cost):
        total_cost = new_cost + old_cost
        return total_cost

    # Calculate f(n) = g(n) + h(n)
    def calc_f(self, path_cost, heuristic_cost):
        self.f = path_cost + heuristic_cost
        return self.f

    def astar(self, initial_state):
        start = time.time()
        # initial-state: (f(n), g(n), h(n), curr _puzzle = Starting Puzzle, Path = [tile,cost, current_puzzle])  
        self.open_state.append([h0(initial_state), 0, h0(initial_state), initial_state, list([0, h0(initial_state), initial_state])]) 
        while (len(self.open_state) > 0):

            self.open_state.sort(key=lambda x: x[0])
            self.curr_f, self.curr_g, self.curr_h, self.current_puzzle, self.path = self.open_state.pop(0) # pop lowest cost move from open queue

            # apply goal function
            if check_goal(self.current_puzzle): # Check if current puzzle state is goal state
                end = time.time()
                execution_time = end - start
                self.closed_state.append((self.current_puzzle))
                return print("Solution found in", execution_time, "sec", self.current_puzzle)
            
            self.children = generate_children(self.current_puzzle) # generate possible successors from current puzzle state

            if(len(self.children.queue) > 0 ):
                for self.child in self.children.queue[:]:

                    self.child_path_cost, self.child_moved_tile, self.child_puzzle_state = self.children.get()
                    # Calculate each cost
                    child_h = h0(self.child_puzzle_state)
                    total_cost = self.get_path_cost(self.child_path_cost, self.curr_g) 
                    child_f = self.calc_f(total_cost, child_h)
                    
                    if (self.child_puzzle_state in (item for sublist in self.open_state for item in sublist)): # check if child is in open_state
                        if self.compare_Cost(child_f, self.child_puzzle_state, self.open_state):  # if child_f is lower than the cost inside open_state, replace it
                            self.open_state = self.replace_Cost(child_f, self.child_puzzle_state, self.open_state)

                    elif (self.child_puzzle_state in (item for sublist in self.closed_state for item in sublist)): # check if child is in closed list
                        if self.compare_Cost(child_f, self.child_puzzle_state, self.open_state):  # if child_f is lower than the cost inside closed list, put it back to open_state
                            self.path.append([self.child_moved_tile, child_f, self.child_puzzle_state])
                            self.open_state.append([child_f, total_cost, child_h, self.child_puzzle_state, self.path])

                    else:
                        self.path.append([self.child_moved_tile, child_f, self.child_puzzle_state])
                        self.open_state.append([child_f, total_cost, child_h, self.child_puzzle_state, self.path])
            
            self.closed_state.append([self.curr_f, self.curr_g, self.curr_h, self.current_puzzle])
            temp_time = time.time()
            if (temp_time - start) > 60:
                print("One minute passed - No Solution")
                break
        
        return "No Solution"


def get_Start_State(puzzle_file):
    input_file = np.loadtxt(puzzle_file, delimiter=' ')
    puzzle_list = []
    for i in range(input_file.ndim+1):
        puzzle_list.append(input_file[i].reshape(2,4)) # reshape 1D array(s) to 2x4 (row x col) 2D array
    return puzzle_list


def main():
    initial_States = get_Start_State("samplePuzzles.txt")
    solve = AStar()
    for i in range(len(initial_States)):
        #solve.astar(initial_States[i].tolist())
        solve.astar(initial_States[0].tolist())


if __name__ == '__main__':
    main()