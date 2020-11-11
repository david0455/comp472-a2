import numpy as np

A = np.eye(3)
print(A)
print()

test = [[1, 2, 3, 4],
        [0, 4, 5, 6],
        [33, 9, 9, 69]]

print(test)
print(test[1][0])

curr = (1, 0)
temp = (0, 0)

print('\nlength row = ', len(test))       # len(2d array) == rows
print('length col = ', len(test[0]), '\n')    # len(2d array[0]) == column


def swap(List, current_pos, next_pos):
    curr_row = current_pos[0]
    curr_col = current_pos[1]

    temp_row = next_pos[0]
    temp_col = next_pos[1]
    temp_val = List[temp_row][temp_col]

    List[temp_row][temp_col] = List[curr_row][curr_col]
    List[curr_row][curr_col] = temp_val

swap(test, (1, 0), (0, 0))
print(test)

test2 = [0, 1, 2, 3]
print(test[-1][-1])

arr = [0, 1]
arr = [2, 3]
row, col = arr
print(row)
print(col)