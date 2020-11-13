import numpy as np
import queue as Q

class Rules(object):

    def __init__(self, puzzle):
        self.total_cost = 0
        
        # self.input_txt = np.loadtxt('samplePuzzles.txt', delimiter=' ')
        # # TODO: self.puzzle
        # # TODO: this only takes first line of text file
        # # TODO: need to assign each line as a puzzle
        # self.puzzle = self.input_txt[0].reshape(2, 4)
        self.puzzle = puzzle
        self.zero_pos = self.find()

        self.openq = []
        self.closedq = []

    def getTotalCost(self):
        return self.total_cost

    # TODO: np.where() could be better?
    # Finds the coordinates of the 0 tile
    def find(self):
        for row in range(self.puzzle.shape[0]):
            for col in range(self.puzzle.shape[1]):
                if self.puzzle[row][col] == 0:
                    return row, col

    def swap(self, List, current_pos, next_pos):
        curr_row = current_pos[0]
        curr_col = current_pos[1]

        temp_row = next_pos[0]
        temp_col = next_pos[1]
        temp_val = List[temp_row][temp_col]

        # Set new position for ZERO
        List[temp_row][temp_col] = List[curr_row][curr_col]
        # Set old position to temp value
        List[curr_row][curr_col] = temp_val
        # Set current position of ZERO
        self.zero_pos = [temp_row, temp_col]

    ##################################################################
    ##################################################################
    #######     total row == self.puzzle.shape[0] - 1     for 0 ~ n-1
    #######                  len(self.puzzle) - 1
    #######     total col == self.puzzle.shape[1] - 1  for 0 ~ n-1
    #######                  len(self.puzzle[0]) - 1
    ##################################################################
    ##################################################################

    def getUp(self):
        row, col = self.zero_pos

        if row == 0:
            raise Exception('Illegal move -> cannot get UP')

        return self.puzzle[row-1][col]
    
    def moveUp(self):
        row, col = self.zero_pos

        # TODO: Probably will have dimension of puzzle at start so use that instead of length
        # If ZERO is at first row, then illegal
        if row == 0:
            raise Exception('Illegal move -> cannot move UP')

        self.swap(self.puzzle, [row, col], [row - 1, col])
        self.total_cost += 1

    def getDown(self):
        row, col = self.zero_pos

        if row == self.puzzle.shape[0] - 1:
            raise Exception('Illegal move -> cannot get DOWN')

        return self.puzzle[row+1][col]

    def moveDown(self):
        row, col = self.zero_pos

        # If ZERO is at last row, then illegal
        if row == self.puzzle.shape[0] - 1:
            raise Exception('Illegal move -> cannot move DOWN')

        self.swap(self.puzzle, [row, col], [row + 1, col])
        self.total_cost += 1

    def getLeft(self):
        row, col = self.zero_pos

        if col == 0:
            raise Exception('Illegal move -> cannot get LEFT')

        return self.puzzle[row][col-1]
    
    def moveLeft(self):
        row, col = self.zero_pos

        # If ZERO is at first column, then illegal
        if col == 0:
            raise Exception('Illegal move -> cannot move LEFT')

        self.swap(self.puzzle, [row, col], [row, col - 1])
        self.total_cost += 1

    def getRight(self):
        row, col = self.zero_pos

        if col == self.puzzle.shape[1] - 1:
            raise Exception('Illegal move -> cannot get RIGHT')

        return self.puzzle[row][col+1]
    
    def moveRight(self):
        row, col = self.zero_pos

        # If ZERO is at last column, then illegal
        if col == self.puzzle.shape[1] - 1:
            raise Exception('Illegal move -> cannot move RIGHT')

        self.swap(self.puzzle, [row, col], [row, col + 1])
        self.total_cost += 1

    def getWrap(self):
        row, col = self.zero_pos

        if (row == 0 or row == self.puzzle.shape[0] - 1) and col == 0:
            return self.puzzle[row][-1]
        elif (row == 0 or row == self.puzzle.shape[0] - 1) and col == self.puzzle.shape[1] - 1:
            return self.puzzle[row][0]
        else:
            raise Exception('Illegal move -> cannot get WRAP')
    
    def moveWrap(self):
        row, col = self.zero_pos

        if (row == 0 or row == self.puzzle.shape[0] - 1) and col == 0:
            self.swap(self.puzzle, [row, col], [row, -1])
        elif (row == 0 or row == self.puzzle.shape[0] - 1) and col == self.puzzle.shape[1] - 1:
            self.swap(self.puzzle, [row, col], [row, 0])
        else:
            raise Exception('Illegal move -> cannot move WRAP')
        self.total_cost += 2

    def getDiagonal(self):
        row, col = self.zero_pos

        # Top Left Corner
        if row == 0 and col == 0:
            return self.puzzle[row+1][col+1]
        # Top Right Corner
        elif row == 0 and col == self.puzzle.shape[1] - 1:
            return self.puzzle[row+1][col-1]
        # Bottom Left Corner
        elif row == self.puzzle.shape[0] - 1 and col == 0:
            return self.puzzle[row-1][col+1]
        # Bottom Right Corner
        elif row == self.puzzle.shape[0] - 1 and col == self.puzzle.shape[1] - 1:
            return self.puzzle[row-1][col-1]
        else:
            raise Exception('Illegal move -> cannot get DIAGONAL')
    
    def moveDiagonal(self):
        row, col = self.zero_pos

        # Top Left Corner
        if row == 0 and col == 0:
            self.swap(self.puzzle, [row, col], [row + 1, col + 1])
        # Top Right Corner
        elif row == 0 and col == self.puzzle.shape[1] - 1:
            self.swap(self.puzzle, [row, col], [row + 1, col - 1])
        # Bottom Left Corner
        elif row == self.puzzle.shape[0] - 1 and col == 0:
            self.swap(self.puzzle, [row, col], [row - 1, col + 1])
        # Bottom Right Corner
        elif row == self.puzzle.shape[0] - 1 and col == self.puzzle.shape[1] - 1:
            self.swap(self.puzzle, [row, col], [row - 1, col - 1])
        else:
            raise Exception('Illegal move -> cannot move DIAGONAL')
        self.total_cost += 3

    def getDiagWrap(self):
        row, col = self.zero_pos

        # Top Left Corner
        if row == 0 and col == 0:
            return self.puzzle[-1][-1]
        # Top Right Corner
        elif row == 0 and col == self.puzzle.shape[1] - 1:
            return self.puzzle[-1][0]
        # Bottom Left Corner
        elif row == self.puzzle.shape[0] - 1 and col == 0:
            return self.puzzle[0][-1]
        # Bottom Right Corner
        elif row == self.puzzle.shape[0] - 1 and col == self.puzzle.shape[1] - 1:
            return self.puzzle[0][0]
        else:
            raise Exception('Illegal move -> cannot get DIAGONAL WRAP')
    
    def moveDiagWrap(self):
        row, col = self.zero_pos

        # Top Left Corner
        if row == 0 and col == 0:
            self.swap(self.puzzle, [row, col], [-1, -1])
        # Top Right Corner
        elif row == 0 and col == self.puzzle.shape[1] - 1:
            self.swap(self.puzzle, [row, col], [-1, 0])
        # Bottom Left Corner
        elif row == self.puzzle.shape[0] - 1 and col == 0:
            self.swap(self.puzzle, [row, col], [0, -1])
        # Bottom Right Corner
        elif row == self.puzzle.shape[0] - 1 and col == self.puzzle.shape[1] - 1:
            self.swap(self.puzzle, [row, col], [0, 0])
        else:
            raise Exception('Illegal move -> cannot move DIAGONAL WRAP')
        self.total_cost += 3

    # Generates the available moves
    # Return a PriorityQueue with (cost, moveDirection)
    def generate_moves(self):
        row, col = self.zero_pos
        pq = Q.PriorityQueue()

        if row != 0:
            pq.put((1, self.getUp(), self.puzzle))
        if row != self.puzzle.shape[0] - 1 :
            pq.put((1, self.getDown(), self.puzzle))
        if col != 0:
            pq.put((1, self.getLeft(), self.puzzle))
        if col != self.puzzle.shape[1] - 1:
            pq.put((1, self.getRight(), self.puzzle))

        if ((row == 0 and col == 0)
        or (row == 0 and col == self.puzzle.shape[1] - 1)
        or (row == self.puzzle.shape[0] - 1 and col == 0)
        or (row == self.puzzle.shape[0] - 1 and col == self.puzzle.shape[1] - 1)):
            pq.put((2, self.getWrap(), self.puzzle))
            pq.put((3, self.getDiagonal(), self.puzzle))
            pq.put((3, self.getDiagWrap(), self.puzzle))
        
        return pq

    # TODO: NOT DONE / CORRECT
    def checkGoal(self):
        goal_1 = [[1, 2, 3, 4],
                  [5, 6, 7, 0]]

        goal_2 = [[1, 3, 5, 7],
                  [2, 4, 6, 0]]

        if (self.puzzle == goal_1).all() or (self.puzzle == goal_2).all():
            return True
        return False
