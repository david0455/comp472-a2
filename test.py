import numpy as np
import pandas as pd
import queue as Q

# input_txt = pd.read_csv('samplePuzzles.txt', sep=' ', header=None)
input_txt = np.loadtxt('samplePuzzles.txt', delimiter=' ')
# input_txt is a 2d array
# where each row == 1 input_txt
print(input_txt)
print()
print(input_txt[0]) # row 1 == input_txt 1

print()
puzzle1 = input_txt[0].reshape(2, 4)
print(puzzle1)
print(puzzle1[0][-1])
print('shape = ', puzzle1.shape)
print('row = ', puzzle1.shape[0])
print('col = ', puzzle1.shape[1])

# # 2d array
# arr2d = np.array(
#     [
#         [1, 2, 3], 
#         [4, 5, 6], 
#         [7, 8, 0]   
#     ]
# )
# print(arr2d)
# print('dimension = ', arr2d.ndim)
# print('shape = ', arr2d.shape)
# print(arr2d[2][2]) # accessing Bot-Right value
# row, col = np.where(arr2d == 0)
# print(row)
# print(col)
# # print(arr2d[row][col])       BAD

# pq = Q.PriorityQueue()

# pq.put((1, 'up'))
# pq.put((2, 'wrap'))
# pq.put((1, 'down'))

# print(pq.queue) # prints content of PriorityQueue

# # iterates over PriorityQueue and print in ascending order of cost
# # if same cost, prints in alphabetical order
# while not pq.empty():
#     print(pq.get())

# print(pq.queue)


# A = np.eye(3)
# print(A)
# print()

# test = [[1, 2, 3, 4],
#         [0, 4, 5, 6],
#         [33, 9, 9, 69]]

# print(test)
# print(test[1][0])

# curr = (1, 0)
# temp = (0, 0)

# print('\nlength row = ', len(test))       # len(2d arr2day) == rows
# print('length col = ', len(test[0]), '\n')    # len(2d arr2day[0]) == column


# def swap(List, current_pos, next_pos):
#     curr_row = current_pos[0]
#     curr_col = current_pos[1]

#     temp_row = next_pos[0]
#     temp_col = next_pos[1]
#     temp_val = List[temp_row][temp_col]

#     List[temp_row][temp_col] = List[curr_row][curr_col]
#     List[curr_row][curr_col] = temp_val

# swap(test, (1, 0), (0, 0))
# print(test)

# test2 = [0, 1, 2, 3]
# print(test[-1][-1])

# arr2d = [0, 1]
# arr2d = [2, 3]
# row, col = arr2d
# print(row)
# print(col)