import numpy as np
import pandas as pd
import queue as Q


##################################################################
##################################################################
#######     array of arrays
#######     array of arrays
#######     array of arrays
#######     array of arrays
##################################################################
##################################################################

# numbersList = []

# listofNumbers = [1,2,3]
# secondListofNumbers = [4,5,6]

# numbersList.append(listofNumbers)
# numbersList.append(secondListofNumbers)

# for number in numbersList:
#     print(number)

# print(numbersList[0])

#######
arrOfarr = []

##################################################################
##################################################################
#######     Priority Queue
#######     Priority Queue
#######     Priority Queue
#######     Priority Queue
##################################################################
##################################################################

# pq = Q.PriorityQueue()
# arr1 = [1, 2, 3]
# arr2 = [2, 1, 3]
# arr3 = [2, 3, 1]

# # (cost, move, state_arr, uID)
# pq.put((1, 'up', arr1, 0))
# pq.put((2, 'wrap', arr2, 1))
# pq.put((1, 'down', arr3, 2))

# print('queue = ', pq.queue) # prints content of PriorityQueue
# print()
# # iterates over PriorityQueue and print in ascending order of cost
# # if same cost, prints in alphabetical order
# while not pq.empty():
#    # print('pq.get() = ', pq.get())
#     arrOfarr.append(pq.get())

# print('queue = ', pq.queue)
# print('array of array = ', arrOfarr)
# print(arrOfarr[0])
# print()

# def findUID(List, uID):
#     for tup in List:
#         print(tup[2])
#     if (uID == np.where(List == uID)):
#         print(uID)
# findUID(arrOfarr, 2)

##################################################################
##################################################################
#######     load text file with numpy
#######     load text file with numpy
#######     load text file with numpy
#######     load text file with numpy
##################################################################
##################################################################

# # input_txt = pd.read_csv('samplePuzzles.txt', sep=' ', header=None)
# input_txt = np.loadtxt('samplePuzzles.txt', delimiter=' ')
# # input_txt is a 2d array
# # where each row == 1 input_txt
# print(input_txt)
# print()
# print(input_txt[0]) # row 1 == input_txt 1
# print('ndim = ', input_txt.ndim)


# print()
# puzzle1 = input_txt[0].reshape(2, 4)
# print(puzzle1)
# print(puzzle1[0][-1])
# print('shape = ', puzzle1.shape)
# print('row = ', puzzle1.shape[0])
# print('col = ', puzzle1.shape[1])

##################################################################
##################################################################
#######     numpy 2d array
#######     numpy 2d array
#######     numpy 2d array
#######     numpy 2d array
##################################################################
##################################################################

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


##################################################################
##################################################################
#######     testing swap and array manipulation
#######     testing swap and array manipulation
#######     testing swap and array manipulation
#######     testing swap and array manipulation
##################################################################
##################################################################

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


q = Q.PriorityQueue()
q.put((12, 3, [[1, 2, 3, 4], [5, 6, 7, 8]], [0,0]))
q.put((2, 3,  [[9, 11, 11, 12], [13, 14, 15, 16]], [0, 0, 1, 3]))
q.put((5, 4,  [[17, 18, 19, 20], [21, 22, 23, 24]], [0, 0, 1, 3, 4, 6]))


p = Q.PriorityQueue()

print(q.queue)

closed = [[[1, 2, 3, 4], [5, 6, 7, 8]] , [[9, 10, 11, 12], [13, 14, 15, 16]], [[17, 18, 19, 20], [21, 22, 23, 24]]]

print(closed)


# if closed.count(child_state) > 0: 
#     print(True)
# else:
#     print(False)

# if q.queue.count(child_state) > 0: 
#     print(True)
# else:
#     print(False)

    
# print(p.queue.count(child_state))    

# if not(closed.count(child_state) > 0) and not(q.queue.count(child_state) > 0): 
#     print(True)
# else:
#     print(False)

print()
print()

closeed_state = [[3, 0, 1, 4], [2, 6, 5, 7]]
open_state = Q.PriorityQueue()
child = [[3, 1, 0, 4], [2, 6, 5, 7]]

asd = [3, 1, 0, 4, 2, 6, 5, 7]
testchild = np.array(asd).reshape(2,4)

if (closeed_state != child):
    print('\nnot euql\n')
else:
    print('\nequal\n')

print('open ', open_state.queue)
print('testchild = ', testchild)
print(type(testchild))

if not(closeed_state.count(testchild.tolist()) > 0) and not(open_state.queue.count(testchild.tolist()) > 0): 
    print(True)
else:
    print(False)