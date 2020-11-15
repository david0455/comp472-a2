import queue as Q
import numpy as np
import pandas as pd
from puzzle_rules import Rules


class GreedyBFS():

    def __init__(self):
        self.start_state = []
        self.visited_state = []
        self.closed_list = []  # list of visited states
        self.open_list = Q.PriorityQueue()  # priority queue ordered by total cost

    def get_start_state(self, puzzle_file):
        self.puzzle = pd.read_csv(puzzle_file, sep=" ", header=None)
        self.puzzle_list = []
        for i in range(self.puzzle.ndim+1):
            self.puzzle_list.append(self.puzzle[i].reshape(2,4)) # reshape 1D array(s) to 2x4 (row x col) 2D array
        return self.puzzle_list

    def generate_children(self):
        print()
        # TODO

    def action_move(self, move, rl):
        if move == "up":
            rl.moveUp()
        elif move == "down":
            rl.moveDown()
        elif move == "right":
            rl.moveRight()
        elif move == "left":
            rl.moveLeft()
        elif move == "diagonal":
            rl.moveDiagonal()
        elif move == "diagwrap":
            rl.moveDiagWrap()
        elif move == "wrap":
            rl.moveWrap()
        
        return rl.getPuzzle()

    def gbfs(self, init_puzzle):
        rl = Rules(init_puzzle)
        if rl.checkGoal(): #if initial state is equal to goal, end ucs
            return print("Already at goal state") 

        copy_puzzle = list(init_puzzle)
        self.open_list.put([0, 0, None, copy_puzzle, [0,0]]) # TODO: dafuq u do with this path

        while not self.open_list.empty():
            self.cost, self.moved_tile, self.move, self.visited_state, self.path = self.open_list.get()
            self.closed_list.append(self.visited_state)

            if rl.checkGoal(): #if initial state is equal to goal, end ucs
                return print("Already at goal state") 
            else:
                self.open_list.put(rl.genMove_h1()) #(self.h1(testpuzzle), self.getLeft(), 'left', testpuzzle)
                # something with visited state
                temp_h, temp_tile, temp_move, temp_puzzle = self.open_list.get()
                current_puzzle = self.action_move(temp_move, rl)





def main():
    input_file = np.loadtxt("samplePuzzles.txt", delimiter=' ')

    first_puzzle = input_file[0].reshape(2,4)
    second_puzzle = input_file[1].reshape(2,4)
    third_puzzle = input_file[2].reshape(2,4)

    solve = GreedyBFS()
    solve.gbfs(first_puzzle)

if __name__ == '__main__':
    main()
