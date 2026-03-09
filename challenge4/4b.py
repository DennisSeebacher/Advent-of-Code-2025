from enum import Enum
import os

file = './challenge4/input'
file = open(file)

# How many rolls of paper can be accessed by a forklift?
# The forklifts can only access a roll of paper if there are fewer than four rolls of paper in the eight adjacent positions.

grid = []
"""grid [row] [column]"""

for line in file.readlines():
    row = []
    for char in line.strip():
        row.append(char)
    grid.append(row)

totalCount = 0

def checkForAccess(row, column):
    global grid
    Tile = grid[row][column]
    count = 0
    #print('Test', Tile, end=': ', flush=True)

    if Tile != "@":
        #print('skip')
        return False
    
    for i in range(row-1, row+2):
        for k in range(column-1, column+2):

            if i < 0:
                continue

            if k < 0:
                continue
            
            if i >= len(grid):
                continue

            if k >= len(grid[0]):
                continue            

            if i == row and k == column:
                continue

            #print(i,'/', k, sep='', end=' ')
            #print('(', grid[i][k], ')', end=', ', flush=True)
            if grid[i][k] == '@' or grid[i][k] == 'x':
                count += 1

    #print(count)
    if count < 4:
        grid[row][column] = 'x'
        return True
    else:
        return False

def cleanup():
    global grid
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if grid[row][column] == 'x':
                grid[row][column] = '.'


while True:
    count = 0
    for r in range(0,len(grid)):
        for c in range(0, len(grid[0])):
            if (checkForAccess(r,c)):
                count += 1
    print("Es können", count, "Boxen in diesem Durchgang erreicht werden.")
    if count == 0:
        break
    totalCount += count
    cleanup()

print("Es können insgesamt", totalCount, "Boxen erreicht werden.")