import queue as Q
import numpy as np
import pandas as pd
import time
import re

from rules_scaled import check_goal, generate_children, h1, h2


class GreedyBFS():

    def __init__(self):
        self.closed_list = []
        self.open_list = []
        self.path = []

    def search_visited_state(self, puzzle): 
        for i in range(len(self.closed_list)):
                if(puzzle == self.closed_list[i][3]):
                    curr_f, curr_g, curr_h, current_puzzle, tile, parent_puzzle = self.closed_list[i]
                    return tile, curr_h, current_puzzle, parent_puzzle 
    
    def backtrack(self, puzzle):   
        parent = puzzle 
        if parent == None: # Stopping point
            return self.path
        else:
            tile, cost, current_puzzle, parent_puzzle  = self.search_visited_state(puzzle)
            self.path.append([tile, cost, current_puzzle])
            return self.backtrack(parent_puzzle)

    def print_searchpath(self, index, heuristic, closed):
        filename = ".//4_gbfs_scaled_output//" + str(index) + '_gbfs-h' + str(heuristic) + '_search.txt'
        file = open(filename, 'a')

        for elem in closed:
            f, g, h, puzzle, tile, parent_puzzle = elem
            strpuzzle = ' '.join(str(e) for e in puzzle)
            strpuzzle = re.sub(r"\[|\]|,", '', strpuzzle)
            file.write(str(f) + ' ' + str(g) + ' ' + str(h) + ' ' + strpuzzle + '\n')
        file.close()
    
    def print_solutionpath(self, index, heuristic, path, execution_time, solved):
        filename = ".//4_gbfs_scaled_output//" + str(index) + '_gbfs-h' + str(heuristic) + '_solution.txt'
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

    def gbfs(self, init_puzzle, index, heuristic):      
        start = time.time()
        if heuristic == 1:
            # [heuristic, current puzzle, tile, parent puzzle]
            self.open_list.append([h1(init_puzzle), 0, init_puzzle, None])
        elif heuristic == 2:
            self.open_list.append([h2(init_puzzle), 0, init_puzzle, None])

        while len(self.open_list) > 0:
            self.open_list.sort(key=lambda x: x[0])
            h_cost, next_tile, current_puzzle, parent_puzzle = self.open_list.pop(0)
          
            if check_goal(current_puzzle):
                end = time.time()
                execution_time = end - start
                if heuristic == 1:
                    self.closed_list.append([0, 0, h1(current_puzzle), current_puzzle, next_tile, parent_puzzle])
                elif heuristic == 2:
                    self.closed_list.append([0, 0, h2(current_puzzle), current_puzzle, next_tile, parent_puzzle])

                path = self.backtrack(current_puzzle)
                path.reverse()
                self.print_solutionpath(index, heuristic, path, execution_time, True)
                self.print_searchpath(index, heuristic, self.closed_list)
                
                return print("Solution found in", execution_time, "sec", current_puzzle)

            children = generate_children(current_puzzle)

            if len(children.queue) > 0:
                for child in children.queue[:]:
                    child_cost, child_tile, child_state = children.get()
                    if heuristic == 1:
                        child_h = h1(child_state)
                    elif heuristic == 2:
                        child_h = h2(child_state)

                    if not (child_state in (item for sublist in self.open_list for item in sublist)) and not (child_state in (item for sublist in self.closed_list for item in sublist)):
                        self.open_list.append([child_h, child_tile, child_state, current_puzzle])

            if heuristic == 1:
                self.closed_list.append([0, 0, h1(current_puzzle), current_puzzle, next_tile, parent_puzzle])
            elif heuristic == 2:
                self.closed_list.append([0, 0, h2(current_puzzle), current_puzzle, next_tile, parent_puzzle])
        
        return "No Solution"

def get_start_state(puzzle_file):
    input_file = np.loadtxt(puzzle_file, delimiter=' ')
    puzzle_list = []
    for i in range(input_file.shape[0]):
        puzzle_list.append(input_file[i].reshape(3,4).astype(int)) # reshape 1D array(s) to 3x4 (row x col) 2D array
    return puzzle_list

def main():
    # initial_puzzles = get_start_state("scaled_random_puzzles.txt")

    # for i in range(len(initial_puzzles)):
    #     for j in range(2):
    #         solve = GreedyBFS()
    #         solve.gbfs(initial_puzzles[i].tolist(), i, j+1)

    np3x4 = np.loadtxt('scaled_3x4.txt', delimiter=' ')
    puzzle3x4 = []
    puzzle3x4.append(np3x4[0].reshape(3,4).astype(int))
    solve3x4 = GreedyBFS()
    solve3x4.gbfs(puzzle3x4[0].tolist(), 0, 1) # h1
    solve3x4.gbfs(puzzle3x4[0].tolist(), 0, 2) # h2

    np4x4 = np.loadtxt('scaled_4x4.txt', delimiter=' ')
    puzzle4x4 = []
    puzzle4x4.append(np4x4[0].reshape(4,4).astype(int))
    solve4x4 = GreedyBFS()
    solve4x4.gbfs(puzzle4x4[0].tolist(), 0, 1) # h1
    solve4x4.gbfs(puzzle4x4[0].tolist(), 0, 2) # h2

    puzzle5x4 = np.loadtxt('scaled_5x4.txt', delimiter=' ')
    puzzle5x4 = []
    puzzle5x4.append(np5x4[0].reshape(5,4).astype(int))
    solve5x4 = GreedyBFS()
    solve5x4.gbfs(puzzle5x4[0].tolist(), 0, 1) # h1
    solve5x4.gbfs(puzzle5x4[0].tolist(), 0, 2) # h2
       

if __name__ == '__main__':
    main()
