import queue as Q
import pandas as pd
import numpy as np
import time
import copy

from puzzle_rules import Rules

class AStar():

    def __init__(self):
        self.start_state = []
        self.visited_state = []
        self.closed_state = []  # list of visited states
        self.open_state = []   # priority queue ordered by total cost

    # If the last tile of current puzzle state is not equal to zero, h(n) = 1
    def h0(self, current_puzzle_state):
        # current_puzzle_state[1][3] = Row 2 Col 4
        if(current_puzzle_state[1][3] == 0):
            self.h = 0
        else:
            self.h = 1
        return self.h
    
    # Checks if current_child state is in open_queue or closed list
    def is_in(self, elem, arr):
        deep_copy = copy.deepcopy(arr)
        state = list(deep_copy)
        inside = False
        for i in range(len(state)):
            for j in range(len(state)):
                if(elem == state[i][j]):
                    inside = True
        return inside
    
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

    def check_goal(self, puzzle):
        self.goal1 = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 0]])
        self.goal2 = np.array([[1, 3, 5, 7],
                  [2, 4, 6, 0]])
        current_state = np.array(puzzle)

        if (current_state == self.goal1).all() or (current_state == self.goal2).all():
            return True
        else:
            return False

    # Finds the coordinates of the 0 tile
    def find_zero(self, current_puzzle_state):
        for row in range(len(current_puzzle_state)):
            for col in range(len(current_puzzle_state[0])):
                if current_puzzle_state[row][col] == 0:
                    return row, col
    
    def getUp(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
        if row == 0:
            raise Exception('Illegal move -> cannot get UP')
        return current_puzzle_state[row-1][col]
    
    def moveUp(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        # If ZERO is at first row, then illegal
        if row == 0:
            raise Exception('Illegal move -> cannot move UP')
    
        self.new_state = self.swap(current_puzzle_state, [row, col], [row - 1, col])
    
        return self.new_state
    
    def getDown(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        if row ==  len(current_puzzle_state) - 1:
            raise Exception('Illegal move -> cannot get DOWN')
    
        return current_puzzle_state[row+1][col]
    
    def moveDown(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        # If ZERO is at last row, then illegal
        if row == len(current_puzzle_state) - 1:
            raise Exception('Illegal move -> cannot move DOWN')
    
        self.new_state = self.new_state = self.swap(
            current_puzzle_state, [row, col], [row + 1, col])
    
        return self.new_state
    
    def getLeft(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        if col == 0:
            raise Exception('Illegal move -> cannot get LEFT')
    
        return current_puzzle_state[row][col-1]
    
    def moveLeft(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        # If ZERO is at first column, then illegal
        if col == 0:
            raise Exception('Illegal move -> cannot move LEFT')
    
        self.new_state = self.swap(current_puzzle_state, [row, col], [row, col - 1])
    
        return self.new_state
    
    def getRight(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        if col == len(current_puzzle_state[0]) - 1:
            raise Exception('Illegal move -> cannot get RIGHT')
    
        return current_puzzle_state[row][col+1]
    
    def moveRight(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        # If ZERO is at last column, then illegal
        if col == len(current_puzzle_state[0]) - 1:
            raise Exception('Illegal move -> cannot move RIGHT')
    
        self.new_state = self.swap(current_puzzle_state, [row, col], [row, col + 1])
    
        return self.new_state
    
    def getWrap(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        if (row == 0 or row == len(current_puzzle_state) - 1) and col == 0:
            return current_puzzle_state[row][-1]
        elif (row == 0 or row == len(current_puzzle_state) - 1) and col == len(current_puzzle_state[0]) - 1:
            return current_puzzle_state[row][0]
        else:
            raise Exception('Illegal move -> cannot get WRAP')
    
    def moveWrap(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        if (row == 0 or row == len(current_puzzle_state) - 1) and col == 0:
            self.new_state = self.swap(current_puzzle_state, [row, col], [row, -1])
        elif (row == 0 or row == len(current_puzzle_state) - 1) and col == len(current_puzzle_state[0]) - 1:
            self.new_state = self.swap(current_puzzle_state, [row, col], [row, 0])
        else:
            raise Exception('Illegal move -> cannot move WRAP')
        return self.new_state
    
    def getDiagonal(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        # Top Left Corner
        if row == 0 and col == 0:
            return current_puzzle_state[row+1][col+1]
        # Top Right Corner
        elif row == 0 and col == len(current_puzzle_state[0]) - 1:
            return current_puzzle_state[row+1][col-1]
        # Bottom Left Corner
        elif row == len(current_puzzle_state) - 1 and col == 0:
            return current_puzzle_state[row-1][col+1]
        # Bottom Right Corner
        elif row == len(current_puzzle_state) - 1 and col == len(current_puzzle_state[0]) - 1:
            return current_puzzle_state[row-1][col-1]
        else:
            raise Exception('Illegal move -> cannot get DIAGONAL')
    
    def moveDiagonal(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        # Top Left Corner
        if row == 0 and col == 0:
            self.new_state = self.swap(current_puzzle_state, [row, col], [row + 1, col + 1])
        # Top Right Corner
        elif row == 0 and col == len(current_puzzle_state[0]) - 1:
            self.new_state = self.swap(current_puzzle_state, [row, col], [row + 1, col - 1])
        # Bottom Left Corner
        elif row == len(current_puzzle_state) - 1 and col == 0:
            self.new_state = self.swap(current_puzzle_state, [row, col], [row - 1, col + 1])
        # Bottom Right Corner
        elif row == len(current_puzzle_state) - 1 and col == len(current_puzzle_state[0]) - 1:
            self.new_state = self.swap(current_puzzle_state, [row, col], [row - 1, col - 1])
        else:
            raise Exception('Illegal move -> cannot move DIAGONAL')
        return self.new_state
    
    def getDiagWrap(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        # Top Left Corner
        if row == 0 and col == 0:
            return current_puzzle_state[-1][-1]
        # Top Right Corner
        elif row == 0 and col == len(current_puzzle_state[0]) - 1:
            return current_puzzle_state[-1][0]
        # Bottom Left Corner
        elif row == len(current_puzzle_state) - 1 and col == 0:
            return current_puzzle_state[0][-1]
        # Bottom Right Corner
        elif row == len(current_puzzle_state) - 1 and col == len(current_puzzle_state[0]) - 1:
            return current_puzzle_state[0][0]
        else:
            raise Exception('Illegal move -> cannot get DIAGONAL WRAP')
    
    def moveDiagWrap(self, current_puzzle_state):
        row, col = self.find_zero(current_puzzle_state)
    
        # Top Left Corner
        if row == 0 and col == 0:
            self.new_state = self.swap(current_puzzle_state, [row, col], [-1, -1])
        # Top Right Corner
        elif row == 0 and col == len(current_puzzle_state[0]) - 1:
            self.new_state = self.swap(current_puzzle_state, [row, col], [-1, 0])
        # Bottom Left Corner
        elif row == len(current_puzzle_state) - 1 and col == 0:
            self.new_state = self.swap(current_puzzle_state, [row, col], [0, -1])
        # Bottom Right Corner
        elif row == len(current_puzzle_state) - 1 and col == len(current_puzzle_state[0]) - 1:
            self.new_state = self.swap(current_puzzle_state, [row, col], [0, 0])
        else:
            raise Exception('Illegal move -> cannot move DIAGONAL WRAP')
        return self.new_state
    
    def swap(self, puzzle, current_pos, next_pos):
        copy_puzzle = copy.deepcopy(puzzle) # idk if good copy or not
        curr_row = current_pos[0]
        curr_col = current_pos[1]
    
        temp_row = next_pos[0]
        temp_col = next_pos[1]
        temp_val = copy_puzzle[temp_row][temp_col]
    
        # Set new position for ZERO
        copy_puzzle[temp_row][temp_col] = copy_puzzle[curr_row][curr_col]
        # Set old position to temp value
        copy_puzzle[curr_row][curr_col] = temp_val
        # return new puzzle state
        return copy_puzzle
    
    # Generates the available moves
    # Return a PriorityQueue with (cost, moved_tile, state_after the move 
    def generate_children(self, current_puzzle_state):
        children = Q.PriorityQueue()
        row, col = self.find_zero(current_puzzle_state)

        copy_puzzle = copy.deepcopy(current_puzzle_state) # idk if good copy or not
    
        if row != 0:
            children.put((1, self.getUp(current_puzzle_state), self.moveUp(copy_puzzle)))
        if row != len(current_puzzle_state) - 1:
            children.put((1, self.getDown(current_puzzle_state), self.moveDown(copy_puzzle)))
        if col != 0:
            children.put((1, self.getLeft(current_puzzle_state), self.moveLeft(copy_puzzle)))
        if col != len(current_puzzle_state[0]) - 1:
            children.put((1, self.getRight(current_puzzle_state), self.moveRight(copy_puzzle)))
    
        if ((row == 0 and col == 0)
        or (row == 0 and col == len(current_puzzle_state[0]) - 1)
        or (row == len(current_puzzle_state) - 1 and col == 0)
        or (row == len(current_puzzle_state) - 1 and col == len(current_puzzle_state[0]) - 1)):
            children.put((2, self.getWrap(current_puzzle_state), self.moveWrap(copy_puzzle)))
            children.put((3, self.getDiagonal(current_puzzle_state), self.moveDiagonal(copy_puzzle)))
            children.put((3, self.getDiagWrap(current_puzzle_state), self.moveDiagWrap(copy_puzzle)))
        return children

    def astar(self, initial_state):
        self.start = time.time()
        print("entered astar") 
        #self.open_state.append([self.h0(initial_state), 0, self.h0(initial_state), initial_state, list([0, self.h0(initial_state), initial_state])]) # initial-state: (f(n), g(n), h(n), curr _puzzle = Starting Puzzle, Path = [tile,cost, current_puzzle])  
        self.open_state.append([self.h0(initial_state), 0, self.h0(initial_state), initial_state]) # initial-state: (f(n), g(n), h(n), curr _puzzle = Starting Puzzle, Path = [tile,cost, current_puzzle])
        
        
        while len(self.open_state) > 0:
            print("entered first while loop")
            self.open_state.sort(key=lambda x: x[0])
            # self.curr_f, self.curr_g, self.curr_h, self.current_puzzle, self.path = self.open_state.pop(0) # pop lowest cost move from open queue
            self.curr_f, self.curr_g, self.curr_h, self.current_puzzle = self.open_state.pop(0) # pop lowest cost move from open queue

            if self.check_goal(self.current_puzzle): # Check if current puzzle state is goal state
                self.end = time.time()
                execution_time = self.end - self.start
                self.closed_state.append((self.current_puzzle))
                return print("Solution found in", execution_time, "sec")
            
            self.children = self.generate_children(self.current_puzzle) # generate possible successors from current puzzle state
            #print("\n children:", self.children.queue)
            if(len(self.children.queue) > 0 ):
                for self.child in self.children.queue[:]:
                    print("entered children loop")
                    self.child_path_cost, self.child_moved_tile, self.child_puzzle_state = self.children.get()

                    #print("\nchild:", self.child_path_cost, self.child_moved_tile, self.child_puzzle_state)
                    # Calculate each cost
                    child_h = self.h0(self.child_puzzle_state)
                    total_cost = self.get_path_cost(self.child_path_cost, self.curr_g) 
                    child_f = self.calc_f(total_cost, child_h)
                    
                    if (self.child_puzzle_state in (item for sublist in self.open_state for item in sublist)): # check if child is in open_state
                        if self.compare_Cost(child_f, self.child_puzzle_state, self.open_state):  # if child_f is lower than the cost inside open_state, replace it
                            print("entered compare cost open_state")
                            self.open_state = self.replace_Cost(child_f, self.child_puzzle_state, self.open_state)

                    elif (self.child_puzzle_state in (item for sublist in self.closed_state for item in sublist)): # check if child is in closed list
                        print("entered compare cost closed_state")
                        if self.compare_Cost(child_f, self.child_puzzle_state, self.open_state):  # if child_f is lower than the cost inside closed list, put it back to open_state
                            #self.path.append([self.child_moved_tile, child_f, self.child_puzzle_state])
                            #self.open_state.append([child_f, total_cost, child_h, self.child_puzzle_state, self.path])
                            self.open_state.append([child_f, total_cost, child_h, self.child_puzzle_state])

                    else:
                        #print("\n open_state before put", self.open_state)
                        #self.path.append([self.child_moved_tile, child_f, self.child_puzzle_state])
                        #self.open_state.append([child_f, total_cost, child_h, self.child_puzzle_state, self.path])
                        self.open_state.append([child_f, total_cost, child_h, self.child_puzzle_state])
                        #print("\n open_state after put", self.open_state)
            
            self.closed_state.append([self.curr_f, self.curr_g, self.curr_h, self.current_puzzle])
        
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
    solve.astar(initial_States[0].tolist())

if __name__ == '__main__':
    main()