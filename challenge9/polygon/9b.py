# ********************************************************************************************
# imports
# ********************************************************************************************

import sys
from classes import *
from formatter import *

# ********************************************************************************************
# variables
# ********************************************************************************************

filename = "./challenge9/input"
filename = "./challenge9/test" 

# ********************************************************************************************
# function definitions
# ********************************************************************************************

def readData(filename):
    data = []

    with open(filename, 'r') as file:
        for line in file.readlines():
            parts = line.split(',')
            c = Coordinate(int(parts[0]), int(parts[1]))
            data.append(c)

    return data

def computeRectangles(coordinates):
    rectangles = []

    l = len(coordinates)

    for i in range(l):

        if i > 0 and i % 50 == 0:
            print(f"    {(i/l) * 100:.1f}%")

        for k in range(i,l):
            
            if i == k:
                continue

            rectangles.append(Rectangle(coordinates[i], coordinates[k]))

    return rectangles

def computePolygon(coordinates):
    return Polygon(coordinates)

def computeValidity(rectangles, polygon):
    validRectangles = []

    for rectangle in rectangles:
        if polygon.Includes(rectangle):
            validRectangles.append(rectangle)

    return validRectangles

# ********************************************************************************************
# sorting functions
# ********************************************************************************************

def rectangleSizeSort(rectangle):
    return rectangle.Area

# ********************************************************************************************
# debugging functions
# ********************************************************************************************

def DebugList(entries, displayCountMax = 20):
    print(f"showing {min(displayCountMax, len(entries))} entries:")
    for entry in entries[:min(displayCountMax, len(entries))]:
        #if hasattr(entry, "Debug"):
            #entry.Debug()
        #else:
        print(f"    {str(entry)}")

# ********************************************************************************************
# main loop starts here
# ********************************************************************************************

# read data
print(f"reading data from '{filename}'")
coordinates = readData(filename)
print(f"read {len(coordinates)} entries")

# compute values
print("computing rectangles")
rectangles = computeRectangles(coordinates)
print(f"computed {len(rectangles)} rectangles")

print("building polygon")
polygon = computePolygon(coordinates)
polygon.ComputeOutline()

print("testing rectangle validity")
validRectangles = computeValidity(rectangles, polygon)

print("sorting lists")
rectangles.sort(key=rectangleSizeSort, reverse=True)
validRectangles.sort(key=rectangleSizeSort, reverse=True)

DebugList(coordinates)
polygon.Debug()
DebugList(rectangles)
DebugList(validRectangles,20)

# present results
print(f"Results for {filename}:")
if len(rectangles) > 0:
    print(f"Largest rectangle is {str(rectangles[0])}")
if len(validRectangles) > 0:
    print(f"Largest rectangle inside of polygon is {str(validRectangles[0])}")