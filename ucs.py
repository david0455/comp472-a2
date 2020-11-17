import queue as Q
import pandas as pd
import numpy as np
import time
import re

from puzzle_rules import check_goal, generate_children, h0

class UniformCostSearch():


    def __init__(self):
        self.closed_state = []  # list of visited states
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


    def print_searchpath(self, index, closed):
        filename = ".//1_ucs_output//" + str(index) + '_ucs_search.txt'
        file = open(filename, 'a')

        for elem in closed:
            f, g, h, puzzle = elem
            strpuzzle = ' '.join(str(e) for e in puzzle)
            strpuzzle = re.sub(r"\[|\]|,", '', strpuzzle)
            file.write(str(f) + ' ' + str(g) + ' ' + str(h) + ' ' + strpuzzle + '\n')
        file.close()
    
    def print_solutionpath(self, index, path, execution_time, solved):
        filename = ".//1_ucs_output//" + str(index) + '_ucs_solution.txt'
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

    
    def ucs(self, initial_state, index):
            start = time.time()
            
            # initial-state: (f(n), g(n), h(n), curr _puzzle = Starting Puzzle, Path = [tile,cost, current_puzzle])  
            self.open_state.append([0, 0, 0, initial_state, [[0, 0, initial_state]]]) 

            while len(self.open_state) > 0:
                
                self.open_state.sort(key=lambda x: x[0])
                self.curr_f, self.curr_g, self.curr_h, self.current_puzzle, self.path = self.open_state.pop(0) # pop lowest cost move from open queue

                # apply goal function
                if check_goal(self.current_puzzle):
                    end = time.time()
                    execution_time = end - start
                    self.closed_state.append([0, self.curr_g , 0, self.current_puzzle])

                    self.print_solutionpath(index, self.path, execution_time, True)
                    self.print_searchpath(index, self.closed_state)
                    return print("Solution found in", execution_time, "sec", self.current_puzzle)
                
                # generate possible successors from current puzzle state
                possible_moves = generate_children(self.current_puzzle) 

                if(len(possible_moves.queue) > 0 ):
                    for self.child in possible_moves.queue[:]:
                        child_path_cost, child_moved_tile, child_puzzle_state = possible_moves.get()
                        
                        # Calculate each cost
                        total_cost = self.get_path_cost(child_path_cost, self.curr_g) 

                        if not (child_puzzle_state in (item for sublist in self.open_state for item in sublist)) and not (child_puzzle_state in (item for sublist in self.closed_state for item in sublist)):  # check if the child is in closed list or open priority queue
                            self.path.append([child_moved_tile, total_cost, child_puzzle_state])
                            self.open_state.append([0, total_cost, 0, child_puzzle_state, self.path])

                        elif (child_puzzle_state in (item for sublist in self.open_state for item in sublist)): # if the child in priority queue has higher PATH-COST than this child, replace it
                            if self.compare_Cost(total_cost, child_puzzle_state, self.open_state): 
                                self.open_state = self.replace_Cost(total_cost, child_puzzle_state, self.open_state)
                
                self.closed_state.append([0, self.curr_g , 0, self.current_puzzle])
                temp_time = time.time()
                if (temp_time - start) > 60:
                    print('No solution found under 60s')
                    self.print_solutionpath(index, self.path, (temp_time - start), False)
                    self.print_searchpath(index, self.closed_state)                    
                    break
            return print("No Solution")


def get_Start_State(puzzle_file):
    input_file = np.loadtxt(puzzle_file, delimiter=' ')
    puzzle_list = []
    for i in range(input_file.ndim+1):
        puzzle_list.append(input_file[i].reshape(2,4).astype(int)) # reshape 1D array(s) to 2x4 (row x col) 2D array
    return puzzle_list


def main():
    initial_states = get_Start_State("samplePuzzles.txt")
    solve = UniformCostSearch()
    solve.ucs(initial_states[0].tolist(), 1)
    
    # for i in range(len(initial_states)):
    #     for j in range(2):
    #         solve.astar(initial_states[i].tolist(), i, j+1)


if __name__ == '__main__':
    main()