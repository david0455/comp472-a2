import numpy as np
import re


#file = open('scaled_4x4.txt', 'w')

test = np.arange(0, 16, 1)
np.random.shuffle(test)
string = str(test)
string = re.sub(r"\[|\]", '', string)
string = re.sub(' +', ' ', string)
string = string.lstrip()
file.write(string + '\n')

# for i in range(50):
#     test = np.arange(0, 12, 1)
#     np.random.shuffle(test)
#     string = str(test)
#     string = re.sub(r"\[|\]", '', string)
#     string = re.sub(' +', ' ', string)
#     string = string.lstrip()
#     file.write(string + '\n')

#file.close()