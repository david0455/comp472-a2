import queue as Q
import numpy as np
import pandas as pd
import time
import re

from puzzle_rules import check_goal, generate_children, h1, h2


class GreedyBFS():

    def __init__(self):
        self.closed_list = []
        self.open_list = []

    def print_searchpath(self, index, heuristic, closed):
        filename = str(index) + '_gbfs-h' + str(heuristic) + '_search.txt'
        file = open(filename, 'a')

        for elem in closed:
            f, g, h, puzzle = elem
            strpuzzle = ' '.join(str(e) for e in puzzle)
            strpuzzle = re.sub(r"\[|\]|,", '', strpuzzle)
            file.write(str(f) + ' ' + str(g) + ' ' + str(h) + ' ' + strpuzzle + '\n')
        file.close()
    
    def print_solutionpath(self, index, heuristic, path, execution_time, solved):
        filename = str(index) + '_gbfs-h' + str(heuristic) + '_solution.txt'
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
            self.open_list.append([h1(init_puzzle), 0, init_puzzle, [[0, h1(init_puzzle), init_puzzle]]])
        elif heuristic == 2:
            self.open_list.append([h2(init_puzzle), 0, init_puzzle, [[0, h2(init_puzzle), init_puzzle]]])

        while len(self.open_list) > 0:
            self.open_list.sort(key=lambda x: x[0])
            h_cost, next_tile, current_puzzle, path = self.open_list.pop(0)
          
            if check_goal(current_puzzle):
                end = time.time()
                execution_time = end - start
                if heuristic == 1:
                    self.closed_list.append([0, 0, h1(current_puzzle), current_puzzle])
                elif heuristic == 2:
                    self.closed_list.append([0, 0, h2(current_puzzle), current_puzzle])

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
                        path.append([child_tile, child_h, child_state])
                        self.open_list.append([child_h, child_tile, child_state, path])

            if heuristic == 1:
                self.closed_list.append([0, 0, h1(current_puzzle), current_puzzle])
            elif heuristic == 2:
                self.closed_list.append([0, 0, h2(current_puzzle), current_puzzle])
            temp_time = time.time()
            if (temp_time - start) > 60:
                self.print_searchpath(index, heuristic, self.closed_list)
                self.print_solutionpath(index, heuristic, path, (temp_time - start), False)
                print("No solution found under 60s")
                break
        
        return "No Solution"

def get_Start_State(puzzle_file):
    input_file = np.loadtxt(puzzle_file, delimiter=' ')
    puzzle_list = []
    for i in range(input_file.ndim+1):
        puzzle_list.append(input_file[i].reshape(2,4).astype(int)) # reshape 1D array(s) to 2x4 (row x col) 2D array
    return puzzle_list

def main():
    initial_puzzles = get_Start_State("samplePuzzles.txt")

    solve = GreedyBFS()

    solve.gbfs(initial_puzzles[0].tolist(), 0, 1) # remove when done testing

    # GOOOD
    # for i in range(len(initial_puzzles)):
    #     for j in range(2):
    #         solve.gbfs(initial_puzzles[i].tolist(), i, j+1)

if __name__ == '__main__':
    main()
