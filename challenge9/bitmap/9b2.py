#read the data into coordinates
#build the rectangles from the coordinates
#build an array with the perimeter data
#accessing the perimeter data via perimeter[y][x] is faster

import sys


#FILENAME = './challenge9/test'
FILENAME = './challenge9/input'

OUTSIDE = False
PERIMETER = True
INSIDE = True

class Coordinate:

    idCounter = 0    

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = Coordinate.idCounter
        Coordinate.idCounter += 1

    def __str__(self):
        return f"({self.x}/{self.y})"
    
    def __repr__(self):
        return f"Coordinate({self.x},{self.y})"
    
    def __eq__(self, other):
        if type(other) != type(self):
            return False
        else: 
            return self.x == other.id and self.y == other.y
        
    def __lt__(self, other):
        if type(other) != type(self):
            raise TypeError()
        else:
            return self.x < other.x and self.y < other.y
        
    def __gt__(self, other):
        if type(other) != type(self):
            raise TypeError()
        else:
            return self.x > other.x and self.y > other.y

class Rectangle:

    idCounter = 0    

    def __init__(self, coordinateA, coordinateB):
        self.coordinateA = coordinateA
        self.coordinateB = coordinateB
        self.id = Rectangle.idCounter
        Rectangle.idCounter += 1

    def GetArea(self):
        side_a = abs(self.coordinateA.x - self.coordinateB.x) +1 
        side_b = abs(self.coordinateA.y - self.coordinateB.y) +1
        return side_a * side_b
    
    def GetCoordinates(self):
        listOfCoordinates = []
        
        for x in range(min(self.coordinateA.x, self.coordinateB.x), max(self.coordinateA.x, self.coordinateB.x)):
            for y in range(min(self.coordinateA.y, self.coordinateB.y), max(self.coordinateA.y, self.coordinateB.y)):
                listOfCoordinates.append((x,y))

        return listOfCoordinates
    
    def __str__(self):
        return f"{self.id} (str({self.coordinateA})->str({self.coordinateB})) {self.GetArea()}"

class Perimeter:
    def __init__(self, rows, columns):
        self.grid = []
        self.Width = columns + 3
        self.Height = rows + 2
        for row in range(self.Height):
            if rows > 1000 and row > 0 and row%100 == 0:
                print(f"{row}/{rows} = {row/rows*100:.2f}%")
            new_row = []
            for column in range(self.Width):
                new_row.append(OUTSIDE)
            self.grid.append(new_row)

    def SetPoint(self, column, row, value):
        self.grid[row][column] = value

    def GetPoint(self, column, row):
        return self.grid[row][column]
    
    def FillHoles(self):

        numrows = len(self.grid)
        numcolumns = len(self.grid[0])

        for row in range(0, numrows):

            if row > 0 and row % 10 == 0:
                print(f"{(row/numcolumns)*100}%")

            for cell in range(0, numcolumns):

                # look for first perimeter item, save position
                if self.IsPointInPerimeter(row, cell):
                    start = cell
                    # look for next perimeter item, save position
                    end = None
                    for lookout in range(start+1, numcolumns):
                        if self.IsPointInPerimeter(row, lookout):
                            end = lookout

                    # if end is present, fill from start to end
                    # else do nothing
                    if end is not None:
                        for i in range(start, end):
                            if self.GetPoint(i, row) == OUTSIDE:
                                self.SetPoint(i, row, INSIDE)

    def IsPointInPerimeter(self, row, column):
        return self.grid[row][column] != OUTSIDE
    
    def __sizeof__(self):
        size = 0
        size += sys.getsizeof(self.Height)
        size += sys.getsizeof(self.Width)
        size += sys.getsizeof(self.grid)
        size += sys.getsizeof(self.grid[0][0]) * self.Width * self.Height
        return size

def ReadData(FILENAME):
    coordinates = []
    MIN_X = 9999999999999999
    MIN_Y = 9999999999999999
    MAX_X = 0
    MAX_Y = 0
    file = open(FILENAME)
    for line in file.readlines():
        parts = line.split(',')
        c = Coordinate(int(parts[0]), int(parts[1]))
        coordinates.append(c)
        if c.x > MAX_X: 
            MAX_X = c.x
        if c.x < MIN_X:
            MIN_X = c.x
        if c.y > MAX_Y: 
            MAX_Y = c.y
        if c.y < MIN_Y:
            MIN_Y = c.y
    return coordinates, MIN_X, MAX_X, MIN_Y, MAX_Y

# Perimeter Berechnung hoffentlich verbessert
def ComputeringPerimeter(coordinates):
    perimeter = Perimeter(MAX_Y, MAX_X)

    # step 1 - mark perimeter

    opCount = len(coordinates)

    for op in range(opCount):

        print(f"{op}/{opCount} = {op/opCount}%")

        a = coordinates.pop(0)
        b = coordinates[0]

        # coordinates von a speichern
        perimeter.SetPoint(a.x, a.y, PERIMETER)

        # a -> b verbinden

        startX, endX = min(a.x, b.x), max(a.x, b.x)
        startY, endY = min(a.y, b.y), max(a.y, b.y)

        for x in range(startX, endX+1):
            for y in range(startY, endY+1):
                perimeter.SetPoint(x, y, PERIMETER)
        #   coordinates der zwischenschritte speichern

        coordinates.append(a)

    # step 2 - fill perimeter
    # find all "cells" between two "neighbouring" coordinates on a row

    print("Filling Holes ...")
    perimeter.FillHoles()

    return perimeter

def ComputingRectangles(coordinates):

    rectangles = []

    l = len(coordinates)

    for i in range(l):

        if i > 0 and i % 50 == 0:
            print(f"{str(i/l * 100)}%")

        for k in range(l):
            
            if i == k:
                continue

            rectangles.append(Rectangle(coordinates[i], coordinates[k]))
    return rectangles

def XIsInBoundsOfY(rect, perimeter):
        for coord in rect.GetCoordinates():
            if not perimeter.IsPointInPerimeter(coord[1], coord[0]):
                return False
        return True

def TestPerimeter(rectangles, perimeter):
    valid_rectangles = []

    # a box is out if perimeter if any part of it lies outside of the perimeter
    # for each point of a rectangle check if it is in perimeter

    for rectangle in rectangles:
        if XIsInBoundsOfY(rectangle, perimeter):
            valid_rectangles.append(rectangle)

    return valid_rectangles

def rectangleAreaSorter(r):
    return r.GetArea()

def PrintTop10Rectangles(rectangles):
    print("Top 10 Rectangles:")
    for rect in rectangles[0:10]:
        print("  " + str(rect))

def DrawPerimeter(perimeter):
    print("Perimeter Graph:")
    for y in range(MAX_Y+2):
        for x in range(MAX_X+3):
            point = perimeter.GetPoint(x,y)
            if point == PERIMETER:
                print('○', end='', flush=True)
            elif point == INSIDE:
                print('+', end='', flush=True)
            else:
                print('·', end='', flush=True)
        print()

def PrintDebugData(rectangles, perimeter):
    if MAX_X < 80:
        print("")
        print("*******************************************")
        print("Debugging Info Area:")
        PrintTop10Rectangles(rectangles)
        print("")
        DrawPerimeter(perimeter)
        print("*******************************************")
        print("")

print("reading coordinates")
coordinates, MIN_X, MAX_X, MIN_Y, MAX_Y = ReadData(FILENAME)

print(f"X [{MIN_X} -> {MAX_X}], Y [{MIN_Y} -> {MAX_Y}]")

print(f"Size of Grid = {MAX_X * MAX_Y}")

print(f"Size of {len(coordinates)} Coordinates = {sys.getsizeof(coordinates[0])*len(coordinates)} bytes")

p = Perimeter(256,256)
print(f"Size of a {p.Width}x{p.Height} Perimeter with {len(p.grid)*len(p.grid[0])} Items is {sys.getsizeof(p)} bytes")

print(f"Size of a single Datapoint in the grid is {sys.getsizeof(p.grid[0][0])} bytes")

sys.exit()

print("computering perimeter")
perimeter = ComputeringPerimeter(coordinates)

print("computering rectangles")
rectangles = ComputingRectangles(coordinates)

print("removing rectangles out of perimeter")
valid_rectangles = TestPerimeter(rectangles, perimeter)

print("order rectangles by size")
valid_rectangles.sort(key=rectangleAreaSorter, reverse=True)

print(f"largest rectangle = {str(valid_rectangles[0])}")

PrintDebugData(valid_rectangles, perimeter)    