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
        self.openArr = [] # use this to compare instead of PQ

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
        rl = Rules(init_puzzle)
        if rl.checkGoal(): #if initial state is equal to goal, end ucs
            return print("Already at goal state") 

        copy_puzzle = list(init_puzzle)
        self.open_list.put([0, 0, None, copy_puzzle]) # TODO: dafuq u do with this path

        i = 0
        while not self.open_list.empty():
            print('========================\ni = ', i)
            i += 1
            print('\n\n')
            if rl.checkGoal(): #if initial state is equal to goal, end ucs
                return print("Already at goal state")

            temp_open = self.open_list.get()
            heuristic_child = temp_open[0]
            self.openarr = list(self.open_list.queue) # copying PQ to List

            self.visited_state = temp_open[3]
            self.closed_list.append(self.visited_state)
            print('\nclosed = ', self.closed_list)
            print('open = ', self.open_list.queue)
            print('visited = ', self.visited_state)

            if i > 0:
                current_state = self.action_move(temp_open[2], rl)
                print('\ncurrent state = ', current_state)

            generated_children = rl.genMove_h1() # [self.h1(testpuzzle), self.getLeft(), 'left', testpuzzle]
            print('\ngen children = ', generated_children)

            for item in generated_children:
                print('\n----------child ', item)
                print('child[3] = ', item[3])
                print('closed ', self.closed_list)
                print('openArr ', self.openArr)
                print()
                heuristic, nextTile, nextMove, nextChild = item

                if self.open_list.empty() or item not in self.openArr:
                    if not self.is_in(item[3], self.closed_list):
                        print('\nINSIDE IF===================')
                        print('PUTTING INSIDE OPEN LIST\n')
                        self.open_list.put([heuristic, nextTile, nextMove, nextChild])
                        self.openArr.append([heuristic, nextTile, nextMove, nextChild])
                else:
                    print('\nELSE!!!!!!!!!!!!!!')
             
            



def main():
    input_file = np.loadtxt("samplePuzzles.txt", delimiter=' ')

    first_puzzle = input_file[0].reshape(2,4)
    second_puzzle = input_file[1].reshape(2,4)
    third_puzzle = input_file[2].reshape(2,4)

    solve = GreedyBFS()
    solve.gbfs(first_puzzle)

if __name__ == '__main__':
    main()
