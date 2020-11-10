import numpy as np

class Rules(object):

    def _init_(self):
        self.total_cost = 0

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

    def goal(self, current_state):
        goal_1 = np.array([1, 2, 3, 4, 5, 6, 7, 0])
        goal_2 = np.array([1, 3, 5, 7, 2, 4, 6, 0])

        if(np.array_equal(current_state, goal_1) or np.array_equal(current_state, goal_2)):
            exit()
