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

        self.goal_1 = [[1, 2, 3, 4],
                  [5, 6, 7, 0]]

        self.goal_2 = [[1, 3, 5, 7],
                  [2, 4, 6, 0]]

    def getPuzzle(self):
        return self.puzzle
    
    def getTotalCost(self):
        return self.total_cost

    # TODO: np.where() could be better?
    # Finds the coordinates of the 0 tile
    def find(self):
        for row in range(self.puzzle.shape[0]):
            for col in range(self.puzzle.shape[1]):
                if self.puzzle[row][col] == 0:
                    return row, col

    def swap(self, puzzle, current_pos, next_pos):
        curr_row = current_pos[0]
        curr_col = current_pos[1]

        temp_row = next_pos[0]
        temp_col = next_pos[1]
        temp_val = puzzle[temp_row][temp_col]

        # Set new position for ZERO
        puzzle[temp_row][temp_col] = puzzle[curr_row][curr_col]
        # Set old position to temp value
        puzzle[curr_row][curr_col] = temp_val
        # Set current position of ZERO
        self.zero_pos = [temp_row, temp_col]

    def temp_swap(self, puzzle, current_pos, next_pos):
        temp_puzzle = list(puzzle)
        curr_row = current_pos[0]
        curr_col = current_pos[1]

        temp_row = next_pos[0]
        temp_col = next_pos[1]
        temp_val = temp_puzzle[temp_row][temp_col]

        # Set new position for ZERO
        temp_puzzle[temp_row][temp_col] = temp_puzzle[curr_row][curr_col]
        # Set old position to temp value
        temp_puzzle[curr_row][curr_col] = temp_val
        # Set current position of ZERO
        temp_zero = [temp_row, temp_col]
        return temp_puzzle, temp_zero

    # Count the number of tiles out of place compared to goal
    def h1(self, puzzle):

        h1_val = 0
        for row in range(puzzle.shape[0]):
            for col in range(puzzle.shape[1]):
                if puzzle[row][col] != self.goal_1[row][col] or puzzle[row][col] != self.goal_2[row][col]:
                    h1_val += 1
        return h1_val

    def h2(self):
        print()


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

        # If ZERO is at first row, then illegal
        if row == 0:
            raise Exception('Illegal move -> cannot move UP')

        self.swap(self.puzzle, [row, col], [row - 1, col])
        self.total_cost += 1

    def temp_moveUp(self, puzzle):
        row, col = self.zero_pos

        # If ZERO is at first row, then illegal
        if row == 0:
            raise Exception('Illegal move -> cannot move UP')

        return self.temp_swap(puzzle, [row, col], [row - 1, col])

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

    def temp_moveDown(self, puzzle):
        row, col = self.zero_pos

        # If ZERO is at last row, then illegal
        if row == puzzle.shape[0] - 1:
            raise Exception('Illegal move -> cannot move DOWN')

        return self.temp_swap(puzzle, [row, col], [row + 1, col])
    
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

    def temp_moveLeft(self, puzzle):
        row, col = self.zero_pos

        if col == 0:
            raise Exception('Illegal move -> cannot move LEFT')

        return self.temp_swap(puzzle, [row, col], [row, col - 1])
    
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

    def temp_moveRight(self, puzzle):
        row, col = self.zero_pos

        if col == 0:
            raise Exception('Illegal move -> cannot move RIGHT')

        return self.temp_swap(puzzle, [row, col], [row, col + 1])
    
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

    def temp_moveWrap(self, puzzle):
        row, col = self.zero_pos

        if (row == 0 or row == puzzle.shape[0] - 1) and col == 0:
            return self.temp_swap(puzzle, [row, col], [row, -1])
        elif (row == 0 or row == puzzle.shape[0] - 1) and col == puzzle.shape[1] - 1:
            return self.temp_swap(puzzle, [row, col], [row, 0])
        else:
            raise Exception('Illegal move -> cannot move WRAP')
    
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
    
    def temp_moveDiagonal(self, puzzle):
        row, col = self.zero_pos

        # Top Left Corner
        if row == 0 and col == 0:
            return self.temp_swap(puzzle, [row, col], [row + 1, col + 1])
        # Top Right Corner
        elif row == 0 and col == puzzle.shape[1] - 1:
            return self.temp_swap(puzzle, [row, col], [row + 1, col - 1])
        # Bottom Left Corner
        elif row == puzzle.shape[0] - 1 and col == 0:
            return self.temp_swap(puzzle, [row, col], [row - 1, col + 1])
        # Bottom Right Corner
        elif row == puzzle.shape[0] - 1 and col == puzzle.shape[1] - 1:
            return self.temp_swap(puzzle, [row, col], [row - 1, col - 1])
        else:
            raise Exception('Illegal move -> cannot move DIAGONAL')
    
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
    
    def temp_moveDiagWrap(self, puzzle):
        row, col = self.zero_pos

        # Top Left Corner
        if row == 0 and col == 0:
            return self.temp_swap(puzzle, [row, col], [-1, -1])
        # Top Right Corner
        elif row == 0 and col == puzzle.shape[1] - 1:
            return self.temp_swap(puzzle, [row, col], [-1, 0])
        # Bottom Left Corner
        elif row == puzzle.shape[0] - 1 and col == 0:
            return self.temp_swap(puzzle, [row, col], [0, -1])
        # Bottom Right Corner
        elif row == puzzle.shape[0] - 1 and col == puzzle.shape[1] - 1:
            return self.temp_swap(puzzle, [row, col], [0, 0])
        else:
            raise Exception('Illegal move -> cannot move DIAGONAL WRAP')
    
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
    # Return a PriorityQueue with (cost, nextValue, nextMove, moveDirection)
    def generate_moves(self):
        row, col = self.zero_pos
        pq = Q.PriorityQueue()

        if row != 0:
            pq.put((1, self.getUp(), 'up', self.puzzle))
        if row != self.puzzle.shape[0] - 1 :
            pq.put((1, self.getDown(), 'down', self.puzzle))
        if col != 0:
            pq.put((1, self.getLeft(), 'left', self.puzzle))
        if col != self.puzzle.shape[1] - 1:
            pq.put((1, self.getRight(), 'right', self.puzzle))

        if ((row == 0 and col == 0)
        or (row == 0 and col == self.puzzle.shape[1] - 1)
        or (row == self.puzzle.shape[0] - 1 and col == 0)
        or (row == self.puzzle.shape[0] - 1 and col == self.puzzle.shape[1] - 1)):
            pq.put((2, self.getWrap(), 'wrap'))
            pq.put((3, self.getDiagonal(), 'diagonal', self.puzzle))
            pq.put((3, self.getDiagWrap(), 'diagwrap', self.puzzle))
        
        return pq

    # Generate children with heuristic 1
    def genMove_h1(self):
        row, col = self.zero_pos
        copy_puzzle = list(self.puzzle)
        pq = Q.PriorityQueue()

        if row != 0:
            testpuzzle, tempzero = self.temp_moveUp(copy_puzzle)
            pq.put((self.h1(testpuzzle), self.getUp(), 'up', testpuzzle))
            
        if row != self.puzzle.shape[0] - 1 :
            testpuzzle, tempzero = self.temp_moveDown(copy_puzzle)
            pq.put((self.h1(testpuzzle), self.getDown(), 'down', testpuzzle))

        if col != 0:
            testpuzzle, tempzero = self.temp_moveLeft(copy_puzzle)
            pq.put((self.h1(testpuzzle), self.getLeft(), 'left', testpuzzle))

        if col != self.puzzle.shape[1] - 1:
            testpuzzle, tempzero = self.temp_moveRight(copy_puzzle)
            pq.put((self.h1(testpuzzle), self.getRight(), 'right', testpuzzle))

        if ((row == 0 and col == 0)
        or (row == 0 and col == self.puzzle.shape[1] - 1)
        or (row == self.puzzle.shape[0] - 1 and col == 0)
        or (row == self.puzzle.shape[0] - 1 and col == self.puzzle.shape[1] - 1)):
            testpuzzle, tempzero = self.temp_moveWrap(copy_puzzle)
            pq.put((self.h1(testpuzzle), self.getWrap(), 'wrap', testpuzzle))

            testpuzzle, tempzero = self.temp_moveDiagonal(copy_puzzle)
            pq.put((self.h1(testpuzzle), self.getDiagonal(), 'diagonal', self.puzzle))

            testpuzzle, tempzero = self.temp_moveDiagWrap(copy_puzzle)
            pq.put((self.h1(testpuzzle), self.getDiagWrap(), 'diagwrap', self.puzzle))
        
        return pq

    # TODO: NOT DONE / CORRECT
    def checkGoal(self):
        if (self.puzzle == self.goal_1).all() or (self.puzzle == self.goal_2).all():
            return True
        return False
