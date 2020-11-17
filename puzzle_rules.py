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
def h0(current_puzzle_state):
    # current_puzzle_state[1][3] = Row 2 Col 4
    if(current_puzzle_state[1][3] == 0):
        h = 0
    else:
        h = 1
    return h


# Count the number of tiles out of place compared to goal
def h1(puzzle):
    h1_val1 = 0 # goal 1
    h1_val2 = 0 # goal 2
    goal1 = np.array([[1, 2, 3, 4],[5, 6, 7, 0]])
    goal2 = np.array([[1, 3, 5, 7], [2, 4, 6, 0]])
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] != goal1[row][col]:
                h1_val1 += 1
            if puzzle[row][col] != goal2[row][col]:
                h1_val2 += 1
    return h1_val1 if h1_val1 < h1_val2 else h1_val2


# Finds the coordinates of the 0 tile
def find_zero(current_puzzle_state):
    for row in range(len(current_puzzle_state)):
        for col in range(len(current_puzzle_state[0])):
            if current_puzzle_state[row][col] == 0:
                return row, col


def getUp(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)
    if row == 0:
        raise Exception('Illegal move -> cannot get UP')
    return current_puzzle_state[row-1][col]


def moveUp(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

    # If ZERO is at first row, then illegal
    if row == 0:
        raise Exception('Illegal move -> cannot move UP')

    new_state = swap(current_puzzle_state, [row, col], [row - 1, col])

    return new_state


def getDown(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

    if row ==  len(current_puzzle_state) - 1:
        raise Exception('Illegal move -> cannot get DOWN')

    return current_puzzle_state[row+1][col]


def moveDown(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

    # If ZERO is at last row, then illegal
    if row == len(current_puzzle_state) - 1:
        raise Exception('Illegal move -> cannot move DOWN')

    new_state = new_state = swap(current_puzzle_state, [row, col], [row + 1, col])

    return new_state


def getLeft(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

    if col == 0:
        raise Exception('Illegal move -> cannot get LEFT')

    return current_puzzle_state[row][col-1]


def moveLeft(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

    # If ZERO is at first column, then illegal
    if col == 0:
        raise Exception('Illegal move -> cannot move LEFT')

    new_state = swap(current_puzzle_state, [row, col], [row, col - 1])

    return new_state


def getRight(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

    if col == len(current_puzzle_state[0]) - 1:
        raise Exception('Illegal move -> cannot get RIGHT')

    return current_puzzle_state[row][col+1]


def moveRight(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

    # If ZERO is at last column, then illegal
    if col == len(current_puzzle_state[0]) - 1:
        raise Exception('Illegal move -> cannot move RIGHT')

    new_state = swap(current_puzzle_state, [row, col], [row, col + 1])

    return new_state


def getWrap(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

    if (row == 0 or row == len(current_puzzle_state) - 1) and col == 0:
        return current_puzzle_state[row][-1]
    elif (row == 0 or row == len(current_puzzle_state) - 1) and col == len(current_puzzle_state[0]) - 1:
        return current_puzzle_state[row][0]
    else:
        raise Exception('Illegal move -> cannot get WRAP')


def moveWrap(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

    if (row == 0 or row == len(current_puzzle_state) - 1) and col == 0:
        new_state = swap(current_puzzle_state, [row, col], [row, -1])
    elif (row == 0 or row == len(current_puzzle_state) - 1) and col == len(current_puzzle_state[0]) - 1:
        new_state = swap(current_puzzle_state, [row, col], [row, 0])
    else:
        raise Exception('Illegal move -> cannot move WRAP')
    return new_state


def getDiagonal(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

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


def moveDiagonal(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

    # Top Left Corner
    if row == 0 and col == 0:
        new_state = swap(current_puzzle_state, [row, col], [row + 1, col + 1])
    # Top Right Corner
    elif row == 0 and col == len(current_puzzle_state[0]) - 1:
        new_state = swap(current_puzzle_state, [row, col], [row + 1, col - 1])
    # Bottom Left Corner
    elif row == len(current_puzzle_state) - 1 and col == 0:
        new_state = swap(current_puzzle_state, [row, col], [row - 1, col + 1])
    # Bottom Right Corner
    elif row == len(current_puzzle_state) - 1 and col == len(current_puzzle_state[0]) - 1:
        new_state = swap(current_puzzle_state, [row, col], [row - 1, col - 1])
    else:
        raise Exception('Illegal move -> cannot move DIAGONAL')
    return new_state


def getDiagWrap(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

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


def moveDiagWrap(current_puzzle_state):
    row, col = find_zero(current_puzzle_state)

    # Top Left Corner
    if row == 0 and col == 0:
        new_state = swap(current_puzzle_state, [row, col], [-1, -1])
    # Top Right Corner
    elif row == 0 and col == len(current_puzzle_state[0]) - 1:
        new_state = swap(current_puzzle_state, [row, col], [-1, 0])
    # Bottom Left Corner
    elif row == len(current_puzzle_state) - 1 and col == 0:
        new_state = swap(current_puzzle_state, [row, col], [0, -1])
    # Bottom Right Corner
    elif row == len(current_puzzle_state) - 1 and col == len(current_puzzle_state[0]) - 1:
        new_state = swap(current_puzzle_state, [row, col], [0, 0])
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
def generate_children(current_puzzle_state):
    children = Q.PriorityQueue()
    row, col = find_zero(current_puzzle_state)

    copy_puzzle = copy.deepcopy(current_puzzle_state) # idk if good copy or not

    if row != 0:
        children.put((1, getUp(current_puzzle_state), moveUp(copy_puzzle)))
    if row != len(current_puzzle_state) - 1:
        children.put((1, getDown(current_puzzle_state), moveDown(copy_puzzle)))
    if col != 0:
        children.put((1, getLeft(current_puzzle_state), moveLeft(copy_puzzle)))
    if col != len(current_puzzle_state[0]) - 1:
        children.put((1, getRight(current_puzzle_state), moveRight(copy_puzzle)))

    if ((row == 0 and col == 0)
    or (row == 0 and col == len(current_puzzle_state[0]) - 1)
    or (row == len(current_puzzle_state) - 1 and col == 0)
    or (row == len(current_puzzle_state) - 1 and col == len(current_puzzle_state[0]) - 1)):
        children.put((2, getWrap(current_puzzle_state), moveWrap(copy_puzzle)))
        children.put((3, getDiagonal(current_puzzle_state), moveDiagonal(copy_puzzle)))
        children.put((3, getDiagWrap(current_puzzle_state), moveDiagWrap(copy_puzzle)))
    return children