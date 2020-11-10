import numpy as np

class Rules(object):

    def _init_(self):
        self.total_cost = 0
        self.puzzle = []
        self.openq = []
        self.closedq = []

    def horizontal(self, empty_pos):
        cost_horizontal = 1
        self.total_cost += cost_horizontal

    def vertical(self):
        cost_vertical = 1
        self.total_cost += cost_vertical
    
    def wrap(self):
        cost_wrap = 2
        self.total_cost += cost_wrap

    def diagonal(self):
        cost_diagonal = 3
        self.total_cost += cost_diagonal

    # Finds the coordinates of the 0 tile
    def find(self):
        for row in range(4):
            for col in range(2):
                if self.puzzle[row][col] == 0:
                    return row, col

    # Defines the available moves
    def available_moves(self):
        row, col = self.find()
        
        # For 2x4 puzzles only
        # if in a corner
        if row == 0 and col == 0:
            moves = {
                'down': 1,      # [1][0]
                'right': 1,     # [0][1] 
                'wrap': 2,      # [0][3]
                'diag': 3,      # [1][1]
                'diag_wrap': 3  # [1][3]    
            }
        elif row == 0 and col == 3:
            moves = {
                'down': 1,      # [1][3]
                'left': 1,      # [0][2]
                'wrap': 2,      # [0][0]
                'diag': 3,      # [1][2]
                'diag_wrap': 3  # [1][0]
            }
        elif row == 1 and col == 0:
            moves = {
                'up': 1,        # [0][0]
                'right': 1,     # [1][1]
                'wrap': 2,      # [1][3]
                'diag': 3,      # [0][1]
                'diag_wrap': 3  # [0][3]    
            }
        elif row == 1 and col == 3:
            moves = {
                'up': 1,        # [0][3]
                'left': 1,      # [1][2]
                'wrap': 2,      # [1][0]
                'diag': 3,      # [0][2]
                'diag_wrap': 3  # [0][0]    
            }
        # else if anywhere on first row except corners
        elif row == 0:
            moves = {
                'down': 1,      
                'left': 1,      
                'right': 1      
            }
        # else if anywhere on second row except corners
        elif row == 1:
            moves = {
                'up': 1,
                'left': 1,
                'right': 1
            }
        
        return moves


    def goal(self, current_state):
        goal_1 = [[1, 2, 3, 4],
                  [5, 6, 7, 0]]
        
        goal_2 = [[1, 3, 5, 7], 
                  [2, 4, 6, 0]]

        if (current_state == goal_1 or current_state == goal_2):
            return 'Solved state = ' + current_state


asd = [[1, 2, 3, 4],
       [5, 6, 7, 0]]

print('asd = ', asd)


print(asd[0][0])
print(asd[0][3])

print(asd[1][0])
print(asd[1][3])
