import queue as Q
import numpy as np
import copy


def check_goal(puzzle):
    goal1 = np.array([[1, 2, 3, 4],[5, 6, 7, 0]])
    goal2 = np.array([[1, 3, 5, 7], [2, 4, 6, 0]])
    current_state = np.array(puzzle)

    if (current_state == goal1).all() or (current_state == goal2).all():
        return True
    else:
        return False


# If the last tile of current puzzle state is not equal to zero, h(n) = 1
def h0(puzzle):
    # puzzle[1][3] = Row 2 Col 4
    if(puzzle[1][3] == 0):
        h = 0
    else:
        h = 1
    return h


# Count the number of tiles out of place compared to goal
def h1(puzzle):
    h1_g1 = 0 # goal 1
    h1_g2 = 0 # goal 2
    goal1 = np.array([[1, 2, 3, 4],[5, 6, 7, 0]])
    goal2 = np.array([[1, 3, 5, 7], [2, 4, 6, 0]])
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] != goal1[row][col]:
                h1_g1 += 1
            if puzzle[row][col] != goal2[row][col]:
                h1_g2 += 1

    if h1_g1 < h1_g2:
        return h1_g1
    else:
        return h1_g2


# Count the number of steps of each tile to reach goal position
def h2(puzzle):
    h2_g1 = 0  
    h2_g2 = 0
    goal1 = np.array([[1, 2, 3, 4],[5, 6, 7, 0]])
    goal2 = np.array([[1, 3, 5, 7], [2, 4, 6, 0]])

    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            current_tile = puzzle[row][col]
            goal_tile1 = find_tile(goal1, current_tile)
            goal_tile2 = find_tile(goal2, current_tile)

            h2_g1 += abs((goal_tile1[0] - row) + (goal_tile1[1] - col))
            h2_g2 += abs((goal_tile2[0] - row) + (goal_tile2[1] - col))
            
    if h2_g1 < h2_g2:
        return h2_g1
    else:
        return h2_g2


# Finds the coordinates of the 0 tile
def find_tile(puzzle, tileNumber):
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] == tileNumber:
                return row, col


def getUp(puzzle):
    row, col = find_tile(puzzle, 0)
    if row == 0:
        raise Exception('Illegal move -> cannot get UP')
    return puzzle[row-1][col]


def moveUp(puzzle):
    row, col = find_tile(puzzle, 0)

    # If ZERO is at first row, then illegal
    if row == 0:
        raise Exception('Illegal move -> cannot move UP')

    new_state = swap(puzzle, [row, col], [row - 1, col])

    return new_state


def getDown(puzzle):
    row, col = find_tile(puzzle, 0)

    if row ==  len(puzzle) - 1:
        raise Exception('Illegal move -> cannot get DOWN')

    return puzzle[row+1][col]


def moveDown(puzzle):
    row, col = find_tile(puzzle, 0)

    # If ZERO is at last row, then illegal
    if row == len(puzzle) - 1:
        raise Exception('Illegal move -> cannot move DOWN')

    new_state = new_state = swap(puzzle, [row, col], [row + 1, col])

    return new_state


def getLeft(puzzle):
    row, col = find_tile(puzzle, 0)

    if col == 0:
        raise Exception('Illegal move -> cannot get LEFT')

    return puzzle[row][col-1]


def moveLeft(puzzle):
    row, col = find_tile(puzzle, 0)

    # If ZERO is at first column, then illegal
    if col == 0:
        raise Exception('Illegal move -> cannot move LEFT')

    new_state = swap(puzzle, [row, col], [row, col - 1])

    return new_state


def getRight(puzzle):
    row, col = find_tile(puzzle, 0)

    if col == len(puzzle[0]) - 1:
        raise Exception('Illegal move -> cannot get RIGHT')

    return puzzle[row][col+1]


def moveRight(puzzle):
    row, col = find_tile(puzzle, 0)

    # If ZERO is at last column, then illegal
    if col == len(puzzle[0]) - 1:
        raise Exception('Illegal move -> cannot move RIGHT')

    new_state = swap(puzzle, [row, col], [row, col + 1])

    return new_state


def getRowWrap(puzzle):
    row, col = find_tile(puzzle, 0)

    if (row == 0 or row == len(puzzle) - 1) and col == 0:
        return puzzle[row][-1]
    elif (row == 0 or row == len(puzzle) - 1) and col == len(puzzle[0]) - 1:
        return puzzle[row][0]
    else:
        raise Exception('Illegal move -> cannot get ROW WRAP')


def moveRowWrap(puzzle):
    row, col = find_tile(puzzle, 0)

    if (row == 0 or row == len(puzzle) - 1) and col == 0:
        new_state = swap(puzzle, [row, col], [row, -1])
    elif (row == 0 or row == len(puzzle) - 1) and col == len(puzzle[0]) - 1:
        new_state = swap(puzzle, [row, col], [row, 0])
    else:
        raise Exception('Illegal move -> cannot move ROW WRAP')
    return new_state


def getColWrap(puzzle):
    row, col = find_tile(puzzle, 0)

    if row == 0 and (col == 0 or col == len(puzzle[0]) - 1):
        return puzzle[-1][col]
    elif row == len(puzzle) - 1 and (col == 0 or col == len(puzzle[0]) - 1):
        return puzzle[0][col]
    else:
        raise Exception('Illegal move -> cannot get COL WRAP')


def moveColWrap(puzzle):
    row, col = find_tile(puzzle, 0)

    if row == 0 and (col == 0 or col == len(puzzle[0]) - 1):
        new_state = swap(puzzle, [row, col], [-1, col])
    elif row == len(puzzle) - 1 and (col == 0 or col == len(puzzle[0]) - 1):
        new_state = swap(puzzle, [row, col], [0, col])
    else:
        raise Exception('Illegal move -> cannot move COL WRAP')


def getDiagonal(puzzle):
    row, col = find_tile(puzzle, 0)

    # Top Left Corner
    if row == 0 and col == 0:
        return puzzle[row+1][col+1]
    # Top Right Corner
    elif row == 0 and col == len(puzzle[0]) - 1:
        return puzzle[row+1][col-1]
    # Bottom Left Corner
    elif row == len(puzzle) - 1 and col == 0:
        return puzzle[row-1][col+1]
    # Bottom Right Corner
    elif row == len(puzzle) - 1 and col == len(puzzle[0]) - 1:
        return puzzle[row-1][col-1]
    else:
        raise Exception('Illegal move -> cannot get DIAGONAL')


def moveDiagonal(puzzle):
    row, col = find_tile(puzzle, 0)

    # Top Left Corner
    if row == 0 and col == 0:
        new_state = swap(puzzle, [row, col], [row + 1, col + 1])
    # Top Right Corner
    elif row == 0 and col == len(puzzle[0]) - 1:
        new_state = swap(puzzle, [row, col], [row + 1, col - 1])
    # Bottom Left Corner
    elif row == len(puzzle) - 1 and col == 0:
        new_state = swap(puzzle, [row, col], [row - 1, col + 1])
    # Bottom Right Corner
    elif row == len(puzzle) - 1 and col == len(puzzle[0]) - 1:
        new_state = swap(puzzle, [row, col], [row - 1, col - 1])
    else:
        raise Exception('Illegal move -> cannot move DIAGONAL')
    return new_state


def getDiagWrap(puzzle):
    row, col = find_tile(puzzle, 0)

    # Top Left Corner
    if row == 0 and col == 0:
        return puzzle[-1][-1]
    # Top Right Corner
    elif row == 0 and col == len(puzzle[0]) - 1:
        return puzzle[-1][0]
    # Bottom Left Corner
    elif row == len(puzzle) - 1 and col == 0:
        return puzzle[0][-1]
    # Bottom Right Corner
    elif row == len(puzzle) - 1 and col == len(puzzle[0]) - 1:
        return puzzle[0][0]
    else:
        raise Exception('Illegal move -> cannot get DIAGONAL WRAP')


def moveDiagWrap(puzzle):
    row, col = find_tile(puzzle, 0)

    # Top Left Corner
    if row == 0 and col == 0:
        new_state = swap(puzzle, [row, col], [-1, -1])
    # Top Right Corner
    elif row == 0 and col == len(puzzle[0]) - 1:
        new_state = swap(puzzle, [row, col], [-1, 0])
    # Bottom Left Corner
    elif row == len(puzzle) - 1 and col == 0:
        new_state = swap(puzzle, [row, col], [0, -1])
    # Bottom Right Corner
    elif row == len(puzzle) - 1 and col == len(puzzle[0]) - 1:
        new_state = swap(puzzle, [row, col], [0, 0])
    else:
        raise Exception('Illegal move -> cannot move DIAGONAL WRAP')
    return new_state


def swap(puzzle, current_pos, next_pos):
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
def generate_children(puzzle):
    children = Q.PriorityQueue()
    row, col = find_tile(puzzle, 0)

    copy_puzzle = copy.deepcopy(puzzle) # idk if good copy or not

    if row != 0:
        children.put((1, getUp(puzzle), moveUp(copy_puzzle)))
    if row != len(puzzle) - 1:
        children.put((1, getDown(puzzle), moveDown(copy_puzzle)))
    if col != 0:
        children.put((1, getLeft(puzzle), moveLeft(copy_puzzle)))
    if col != len(puzzle[0]) - 1:
        children.put((1, getRight(puzzle), moveRight(copy_puzzle)))

    if ((row == 0 and col == 0)
    or (row == 0 and col == len(puzzle[0]) - 1)
    or (row == len(puzzle) - 1 and col == 0)
    or (row == len(puzzle) - 1 and col == len(puzzle[0]) - 1)):
        children.put((2, getRowWrap(puzzle), moveRowWrap(copy_puzzle)))
        if len(puzzle) > 2: # if more than 2 rows in puzzle, then colwrap enabled
            children.put((2, getColWrap(puzzle), moveColWrap(copy_puzzle)))
        children.put((3, getDiagonal(puzzle), moveDiagonal(copy_puzzle)))
        children.put((3, getDiagWrap(puzzle), moveDiagWrap(copy_puzzle)))
    return children