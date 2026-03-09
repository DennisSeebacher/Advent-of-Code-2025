#FILENAME = './challenge9/test'
FILENAME = './challenge9/input'

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

def ReadData(FILENAME):
    coordinates = []
    MAX_X = 0
    MAX_Y = 0
    file = open(FILENAME)
    for line in file.readlines():
        parts = line.split(',')
        c = Coordinate(int(parts[0]), int(parts[1]))
        coordinates.append(c)
        if c.x > MAX_X: 
            MAX_X = c.x
        if c.y > MAX_Y: 
            MAX_Y = c.y
    return coordinates, MAX_X, MAX_Y

def ComputeringPerimeters(coordinates):
    perimeter = []

    # step 1 - mark perimeter

    opCount = len(coordinates)

    for op in range(opCount):

        if op > 0 and op % 50 == 0:
            print(f"{(op/opCount) * 100}%")

        a = coordinates.pop(0)
        b = coordinates[0]

        # coordinates von a speichern
        perimeter.append((a.x, a.y))

        # a -> b verbinden

        startX, endX = min(a.x, b.x), max(a.x, b.x)
        startY, endY = min(a.y, b.y), max(a.y, b.y)

        for x in range(startX, endX+1):
            for y in range(startY, endY+1):
                perimeter.append((x, y))
        #   coordinates der zwischenschritte speichern

        coordinates.append(a)

    # step 2 - fill perimeter
    # find all "cells" between two "neighbouring" coordinates on a row

    print("Filling Holes ...")

    for row in range(0, MAX_Y+1):

        #get all items from perimeter in this row
        thisPerimeterRow = []
        for item in perimeter:
            if item[1] == row:
                thisPerimeterRow.append(item)

        if row > 0 and row % 50 == 0:
            print(f"{(row/MAX_Y)*100}%")

        for cell in range(0, MAX_Y):
            # look for first perimeter item, save position
            if (cell, row) in thisPerimeterRow:
                start = cell
                # look for next perimeter item, save position
                end = None
                for lookout in range(cell, MAX_X+1):
                    if (lookout, row) in thisPerimeterRow:
                        end = lookout

                # if end is present, fill from start to end
                # else do nothing
                if end is not None:
                    for i in range(start, end):
                        if (i, row) not in perimeter:
                            perimeter.append((i, row))
            
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
            if coord not in perimeter:
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

def DrawDebugData():
    global valid_rectangles, coordinates, perimeter
    print()

    for rect in valid_rectangles[0:10]:
        print(str(rect))

    print()

    def AnyCoordWith(x,y):
        global coordinates
        for coord in coordinates:
                if coord.x == x and coord.y == y:
                    return True
        return False

    # █▓▒░·○


    for y in range(MAX_Y+2):
        for x in range(MAX_X+2):
            if AnyCoordWith(x,y):
                print('○', end='', flush=True)
            elif (x,y) in perimeter:
                print('·', end='', flush=True)
            else:
                print(' ', end='', flush=True)
        print()

    print()

print("reading coordinates")
coordinates, MAX_X, MAX_Y = ReadData(FILENAME)

print("computering perimeter")
perimeter = ComputeringPerimeters(coordinates)

print("computering rectangles")
rectangles = ComputingRectangles(coordinates)

print("removing rectangles out of perimeter")
valid_rectangles = TestPerimeter(rectangles, perimeter)

print("order rectangles by size")
valid_rectangles.sort(key=rectangleAreaSorter, reverse=True)

if MAX_X < 80:
    DrawDebugData()

print(f"largest rectangle = {str(valid_rectangles[0])}")