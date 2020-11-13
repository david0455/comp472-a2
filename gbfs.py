import queue as Q
import pandas as pd


class GreedyBFS():

    def __init__(self):
        self.start_state = []
        self.visited_state = []
        self.closed_state = []  # list of visited states
        self.open_state = Q.PriorityQueue()  # priority queue ordered by total cost

    def get_start_state(self, puzzle_file):
        self.puzzle = pd.read_csv(puzzle_file, sep=" ", header=None)
        self.puzzle_list = []
        for i in range(self.puzzle.ndim+1):
            self.puzzle_list.append(self.puzzle[i].reshape(2,4)) # reshape 1D array(s) to 2x4 (row x col) 2D array
        return self.puzzle_list

    def generate_children(self):
        print()
        # TODO

    def gbfs(self):
        self.open_state.put((cost, state))

        while not self.open_state.empty():
            print()
