import queue as Q
import pandas as pd
import numpy as np

from puzzle_rules import Rules

class UniformCostSearch():

    def __init__(self):
        self.start_State = []
        self.visited_state = []
        self.closed_state = []  # list of visited states
        self.open_state = Q.PriorityQueue()  # priority queue ordered by total cost

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

    def printPath(self):
        print("hello")
    
    # initial_state = self.get_Start_State("file")
    def ucs(self, initial_state):
        print("entered ucs")
        if len(initial_state) > 0:
            print("entered first if\n")

            print(initial_state)
            rl = Rules(initial_state)
            if rl.checkGoal(): #if initial state is equal to goal, end ucs
                return print("Already at goal state") 

            self.open_state.put([0, 0, None, initial_state ,[0,0]])  # initial-state: (Path-Cost=0, moved_tile=0, move, curr _puzzle = Starting Puzzle, Path = [0,0])     

            while not self.open_state.empty():
                print("\nentered while loop")
                self.cost, self.moved_tile, self.move, self.visited_state, self.path = self.open_state.get() #pop first element with lowest cost in priority queue

                # apply goal function
                if rl.checkGoal():
                    self.closed_state.append(self.visited_state) #put the last visited node in closed list
                    self.path.append((self.moved_tile, self.cost))
                    return print(self.path, self.cost) #return solution path
                
                
                self.closed_state.append(self.visited_state) #put visited state in closed state
                self.possible_Moves = rl.generate_moves()
                print('OPEN STATE = ', self.open_state.queue)
                print('\nCLOSED STATE = ', self.closed_state)
                print('\npossible moves = ', self.possible_Moves.queue)
                while not self.possible_Moves.empty():
                    self.child_cost, self.child_moved_tile, self.next_move, self.parent_state = self.possible_Moves.get()
                    self.child_state = self.action_move(self.next_move, rl)
                    print("\nChild:", self.child_state)
                    if (not all(item in self.child_state for item in self.closed_state)) and (not all(item in self.child_state for item in self.open_state.queue)):  # check if the child is in closed list or open priority queue
                        self.path.append(self.moved_tile, self.cost)
                        self.open_state.put([self.child_cost, self.child_moved_tile, self.next_move, self.child_state, self.path])
                        print('\npossMove IF OPEN STATE = ', self.open_state.queue)
                    elif self.open_state: # if the child in priority queue has higher PATH-COST than this child, replace it
                        if self.compare_Cost(self.child_cost, self.child_state, self.open_state): 
                            self.open_state = self.replace_Cost(self.child_cost, self.child_state, self.open_state)
                        print('\npossMove ELSE OPEN STATE = ', self.open_state.queue)

        return print("No Solution")

def get_Start_State(puzzle_file):
    input_file = np.loadtxt(puzzle_file, delimiter=' ')
    puzzle_list = []
    for i in range(input_file.ndim+1):
        puzzle_list.append(input_file[i].reshape(2,4)) # reshape 1D array(s) to 2x4 (row x col) 2D array
    return puzzle_list

def main():
    input_file = np.loadtxt("samplePuzzles.txt", delimiter=' ')

    first_puzzle = input_file[0].reshape(2,4)
    second_puzzle = input_file[1].reshape(2,4)
    third_puzzle = input_file[2].reshape(2,4)

    solve = UniformCostSearch()
    solve.ucs(first_puzzle)

if __name__ == '__main__':
    main()