import queue as Q
import numpy as np
import pandas as pd
import time
from rules_gbfs import check_goal, generate_children

class GreedyBFS():

    def __init__(self):
        self.visited_state = []
        self.closed_list = []  # list of visited states
        self.open_list = []  # priority queue ordered by total cost

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

    # Merge pq2 into pq1
    def mergePQ(self, pq1, arr):
        for item in arr:
            pq1.put(item)
        return pq1

    def is_in(self, child, arr):
        copyArr = list(arr)
        inside = False
        for i in range(len(copyArr)):
            if np.array_equal(child, arr[i]):
                inside = True
        return inside

    def gbfs(self, init_puzzle):
        start = time.time()
        self.open_list.append([0, 0, init_puzzle, [0]])

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
                    child_hcost, child_tile, child_state = children.get()

                    if not (child_state in (item for sublist in self.open_list for item in sublist)) and (child_state not in self.closed_list):
                        path.append(child_tile)
                        self.open_list.append([child_hcost, child_tile, child_state, path])

            self.closed_list.append(current_puzzle)


    # def gbfs(self, init_puzzle):
    #     start = time.time()
    #     rl = Rules(init_puzzle)
    #     if rl.checkGoal(): #if initial state is equal to goal, end ucs
    #         return print("Already at goal state") 

    #     copy_puzzle = list(init_puzzle)
    #     # TODO: path needs to be chanegd, now is [h=0, tile=0, puzzle]
    #     self.open_list.append([0, 0, None, copy_puzzle, [0, 0]])

    #     while len(self.open_list) > 0:
    #         self.open_list.sort(key=lambda x: x[0])
    #         h_cost, next_tile, next_move, current_puzzle, path = self.open_list.pop(0)

    #         if rl.checkGoal(): #if initial state is equal to goal, end ucs
    #             end = time.time()
    #             execution_time = end - start
    #             self.closed_list.append((rl.getPuzzle()))
    #             return print("Solution found in", execution_time, "sec", rl.getPuzzle())

    #         print('open list = ', self.open_list)
    #         print('\nheuristic  = ', h_cost)
    #         print('next move = ', next_move)
    #         print('current state = ', rl.getPuzzle())

    #         self.visited_state.append(current_puzzle)
    #         self.closed_list.append(current_puzzle)
    #         children = rl.genMove_h1()
            
    #         print('children = ', children.queue)
            
            
    #         print('asdasd\n')

    #         if len(children.queue) > 0:
    #             for child in children.queue[:]:
    #                 child_hcost, child_tile, child_move, child_state = children.get()

    #                 if not (child_state in (item for sublist in self.open_list for item in sublist)) and (child_state not in self.closed_list):
    #                     path.append(child_tile)
    #                     self.open_list.append([child_hcost, child_tile, child_move, child_state, path])
    #         self.action_move(next_move, rl)
    #     print('\nout of while???')

def main():
    input_file = np.loadtxt("samplePuzzles.txt", delimiter=' ')

    first_puzzle = input_file[0].reshape(2,4)
    second_puzzle = input_file[1].reshape(2,4)
    third_puzzle = input_file[2].reshape(2,4)

    solve = GreedyBFS()
    solve.gbfs(first_puzzle.tolist())

if __name__ == '__main__':
    main()
