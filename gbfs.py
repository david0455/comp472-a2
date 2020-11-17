import queue as Q
import numpy as np
import pandas as pd
import time

from puzzle_rules import check_goal, generate_children, h1


class GreedyBFS():

    def __init__(self):
        self.visited_state = []
        self.closed_list = []  # list of visited states
        self.open_list = []  # priority queue ordered by total cost

    def gbfs(self, init_puzzle):
        start = time.time()
        self.open_list.append([h1(init_puzzle), 0, init_puzzle, [0]])

        while len(self.open_list) > 0:
            self.open_list.sort(key=lambda x: x[0])
            h_cost, next_tile, current_puzzle, path = self.open_list.pop(0)

            if check_goal(current_puzzle):
                end = time.time()
                execution_time = end - start
                self.closed_list.append(current_puzzle)
                return print("Solution found in", execution_time, "sec", current_puzzle)

            children = generate_children(current_puzzle)

            if len(children.queue) > 0:
                for child in children.queue[:]:
                    child_cost, child_tile, child_state = children.get()
                    child_h = h1(child_state)

                    if not (child_state in (item for sublist in self.open_list for item in sublist)) and (child_state not in self.closed_list):
                        path.append(child_tile)
                        self.open_list.append([child_h, child_tile, child_state, path])

            self.closed_list.append(current_puzzle)
            temp_time = time.time()
            if (temp_time - start) > 60:
                print("No Solution")
                break
        
        return "No Solution"

def main():
    input_file = np.loadtxt("samplePuzzles.txt", delimiter=' ')

    first_puzzle = input_file[0].reshape(2,4)
    second_puzzle = input_file[1].reshape(2,4)
    third_puzzle = input_file[2].reshape(2,4)

    solve = GreedyBFS()
    solve.gbfs(first_puzzle.tolist())

    # TODO : loop through each line of file = puzzle

if __name__ == '__main__':
    main()
