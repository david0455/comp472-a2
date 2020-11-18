import queue as Q
import pandas as pd
import numpy as np
import time
import re

from puzzle_rules import check_goal, generate_children, h0, h1, h2

class AStar():

    def __init__(self):
        self.closed_state = []
        self.open_state = []


    def print_searchpath(self, index, heuristic, closed):
        filename = ".//3_astar_output//" + str(index) + '_astar-h' + str(heuristic) + '_search.txt'
        file = open(filename, 'a')

        for elem in closed:
            f, g, h, puzzle = elem
            strpuzzle = ' '.join(str(e) for e in puzzle)
            strpuzzle = re.sub(r"\[|\]|,", '', strpuzzle)
            file.write(str(f) + ' ' + str(g) + ' ' + str(h) + ' ' + strpuzzle + '\n')
        file.close()
    

    def print_solutionpath(self, index, heuristic, path, execution_time, solved):
        filename = ".//3_astar_output//" + str(index) + '_astar-h' + str(heuristic) + '_solution.txt'
        file = open(filename, 'a')
        total_cost = 0
        for elem in path:
            tile, cost, puzzle = elem
            total_cost += cost
            strpuzzle = ' '.join(str(e) for e in puzzle)
            strpuzzle = re.sub(r"\[|\]|,", '', strpuzzle)
            file.write(str(tile) + ' ' + str(cost) + ' ' + strpuzzle + '\n')
        if solved:
            file.write(str(total_cost) + ' ' + str(execution_time) + '\n')
        else:
            file.write("no solution" + '\n')
        file.close()


    def compare_Cost(self, child_cost, child_state, pq):
        if len(pq) != 0:
            for cost in pq:
                if child_state == cost[3]: # get puzzle state in list
                    if child_cost < cost[0]: # get cost value in list
                        return True
                    else:
                        return False

    def replace_Cost(self, child_f, total_cost, child_h, child_state, pq):
        if len(pq) != 0:
            for cost in pq:
                if child_state == cost[3]: # get puzzle state in list
                    if child_f < cost[0]: # get cost value in list
                        cost[0] = child_f
                        cost[1] = total_cost
                        cost[2] = child_h
        return pq

    # calculate total path cost
    def get_path_cost(self, new_cost, old_cost):
        total_cost = new_cost + old_cost
        return total_cost

    # Calculate f(n) = g(n) + h(n)
    def calc_f(self, path_cost, heuristic_cost):
        self.f = path_cost + heuristic_cost
        return self.f

    def astar(self, initial_state, index, heuristic):
        start = time.time()
        # initial-state: (f(n), g(n), h(n), curr _puzzle = Starting Puzzle, Path = [tile,cost, current_puzzle])
        if heuristic == 1:
            self.open_state.append([h1(initial_state), 0, h1(initial_state), initial_state, [[0, 0, initial_state]]]) 
        elif heuristic == 2:
            self.open_state.append([h2(initial_state), 0, h2(initial_state), initial_state, [[0, 0, initial_state]]]) 
        
        while (len(self.open_state) > 0):

            self.open_state.sort(key=lambda x: x[0])
            self.curr_f, self.curr_g, self.curr_h, self.current_puzzle, self.path = self.open_state.pop(0) # pop lowest cost move from open queue

            # apply goal function
            if check_goal(self.current_puzzle): # Check if current puzzle state is goal state
                end = time.time()
                execution_time = end - start
                self.closed_state.append([self.curr_f, self.curr_g, self.curr_h, self.current_puzzle])
                self.print_solutionpath(index, heuristic, self.path, execution_time, True)
                self.print_searchpath(index, heuristic, self.closed_state)
                return print("Solution found in", execution_time, "sec", self.current_puzzle)
            
            self.children = generate_children(self.current_puzzle) # generate possible successors from current puzzle state

            if(len(self.children.queue) > 0 ):
                for self.child in self.children.queue[:]:

                    self.child_path_cost, self.child_moved_tile, self.child_puzzle_state = self.children.get()
                    # Calculate each cost
                    if heuristic == 1:
                        child_h = h1(self.child_puzzle_state)
                    elif heuristic == 2:
                        child_h = h2(self.child_puzzle_state)
                    total_cost = self.get_path_cost(self.child_path_cost, self.curr_g) 
                    child_f = self.calc_f(total_cost, child_h)
                    
                    if (self.child_puzzle_state in (item for sublist in self.open_state for item in sublist)): # check if child is in open_state
                        if self.compare_Cost(child_f, self.child_puzzle_state, self.open_state):  # if child_f is lower than the cost inside open_state, replace it
                            self.open_state = self.replace_Cost(child_f, total_cost, child_h, self.child_puzzle_state, self.open_state)

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
                self.print_solutionpath(index, heuristic, self.path, (temp_time - start), False)
                self.print_searchpath(index, heuristic, self.closed_state)
                print("No solution found under 60s")
                break
        
        return "No Solution"


def get_Start_State(puzzle_file):
    input_file = np.loadtxt(puzzle_file, delimiter=' ')
    puzzle_list = []
    for i in range(input_file.shape[0]):
        puzzle_list.append(input_file[i].reshape(2,4).astype(int)) # reshape 1D array(s) to 2x4 (row x col) 2D array
    return puzzle_list


def main():
    initial_states = get_Start_State("samplePuzzles.txt")
    
    for i in range(len(initial_states)):
        for j in range(2):
            solve = AStar()
            solve.astar(initial_states[i].tolist(), i, j+1)

if __name__ == '__main__':
    main()