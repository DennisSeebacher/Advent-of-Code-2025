# ********************
# *     switches     *
# ********************

test = not True

# ********************
# *    variables     *
# ********************

import math
import re
from classes import *

if test:
    filename = './challenge12/test.txt'
else:
    filename = './challenge12/input.txt'

# ********************
#      functions     *
# ********************

def formatNumber(number):
    if number == 1: return "one"
    if number == 2: return "two"
    if number == 3: return "three"
    if number == 4: return "four"
    if number == 5: return "five"
    if number == 6: return "six"
    if number == 7: return "seven"
    if number == 8: return "eight"
    if number == 9: return "nine"
    return str(number)

def readData(filename):

    SHAPE = "Shape"
    AREA = "Area"
    
    shapes = []
    areas = []

    data = open(filename, "r")

    mode = None

    shapenum = None
    shapedata = []

    for line in data:
        if re.match("^[0-9]+:", line):
            mode = SHAPE
            shapenum = re.search("^[0-9]+", line).group(0)
            continue
    
        if re.match("^[0-9]+x[0-9]+:", line):
            mode = AREA
            parts = line.split(":")
            sizedef = parts[0].split('x')
            presents = parts[1].split()
            areas.append(Area(sizedef[0], sizedef[1], presents))
            continue

        if line.strip() == "":
            if mode == SHAPE:
                shapes.append(Shape(shapenum, shapedata.copy()))
                shapedata.clear()
            mode = None

        if mode == SHAPE:
            shapedata.append(line)

    return shapes, areas

def computeResult(areas):

    validAreas = []

    for area in areas:
        if area.canFitShapes:
            validAreas.append(area)

    print(f"In total, there are {formatNumber(len(validAreas))} different areas that fit alll of the presents.")
    #for area in validAreas:
        #print(f"  {str(area)}")

    print("Stats:")
    print(f"Space exceeded: {Area.exceeds}")
    print(f"Space fit:      {Area.fits}")
    print(f"Todos:          {Area.todos}")

# ********************
# *       main       *
# ********************

#read the data
shapes, areas = readData(filename)

# print(f"showing {formatNumber(len(shapes))} shapes:")
# for i in range(0, len(shapes)):
#     print(f"{str(shapes[i])}")
#     print(shapes[i].getVisual())
# print()

# print(f"showing {formatNumber(len(areas))} areas:")
# for i in range(0, len(areas)):
#     print(f"{str(areas[i])}")
# print()

print("fitting shapes")
for area in areas:
    area.fitShapes(shapes)
    print()
print()

computeResult(areas)

print()