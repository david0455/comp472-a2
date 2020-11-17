import numpy as np
import re


file = open('random_puzzles.txt', 'w')

for i in range(50):
    test = np.arange(0, 8, 1)
    np.random.shuffle(test)
    string = str(test)
    string = re.sub(r"\[|\]", '', string)
    file.write(string + '\n')

file.close()