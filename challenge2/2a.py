from enum import Enum
import os
print(os.getcwd())

file = './challenge2/input'
file = open(file)
content = file.read()

ids = content.split(',')

sum = 0

for id in ids:
    start, end = int(id.split('-')[0]),int(id.split('-')[1])

    for i in range(start, end+1):
        x = str(i)
        y = len(x)
        if y % 2 == 0:
            # split in half
            u = x[0:y//2]
            v = x[y//2:]

            # check for sameness
            #print(i,u,v, u == v)
            if u == v:
                sum += i

print(sum)