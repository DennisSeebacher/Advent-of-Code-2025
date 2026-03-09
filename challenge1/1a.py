from enum import Enum
import os
print(os.getcwd())

file = './challenge1/input'

file = open(file)
dial_position = 50
LEFT = "left"
RIGHT = "right"
direction = LEFT
zero_count = 0

def rotate(dir, steps):
    global dial_position

    for step in range(steps):
        if dir == LEFT:
            dial_position -= 1
        else:
            dial_position += 1

        if dial_position < 0:
            dial_position = 99
        
        if dial_position > 99:
            dial_position = 0


for line in file.readlines():
    if line[0] == "L":
        direction = LEFT
    else:
        direction = RIGHT

    steps = int(line[1:])

    rotate(direction, steps)

    # count zeros after rotation

    if dial_position == 0:
        zero_count += 1

    print(direction,dial_position)

print("The Password is", zero_count)