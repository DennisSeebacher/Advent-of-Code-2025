#read the data into coordinates
#build the rectangles from the coordinates
#build an array with the perimeter data
#accessing the perimeter data via perimeter[y][x] is faster
#using a bitarray because a grid exploded the ram
#using the even-odd rule for determining if a point is inside the perimeter
# choose a point
# if it is on the perimeter
#   it is inside
# else
#   determine nearest orthogonal edge
#   count the perimeter crossings
#       odd is inside
#       even is outside

import sys
import time

FILENAME = './challenge9/test'
FILENAME = './challenge9/input'

def FormatBytes(size):
    if size < 1024:
        return f"{size:.0f} B"
    
    size /= 1024
    if size < 1024:
        return f"{size:.1f} kB"
    
    size /= 1024
    if size < 1024:
        return f"{size:.1f} mB"
    
    size /= 1024
    if size < 1024:
        return f"{size:.1f} gB"
    
    size /= 1024
    return f"{size:.2f} tB"

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
    
    def GetBorder(self):
        coords = []

        left = min(self.coordinateA.x, self.coordinateB.x)
        right = max(self.coordinateA.x, self.coordinateB.x)
        up = min(self.coordinateA.y, self.coordinateB.y)
        down = max(self.coordinateA.y, self.coordinateB.y)

        for column in range(left, right):
            coords.append(Coordinate(up, column))
            coords.append(Coordinate(down, column))
        
        for row in range(min(self.coordinateA.y, self.coordinateB.y), max(self.coordinateA.y, self.coordinateB.y)):
            coords.append(Coordinate(row, left))
            coords.append(Coordinate(row, right))

        return coords
    
    def __str__(self):
        return f"id: {self.id:5} | a->b: ({str(self.coordinateA):6}->{str(self.coordinateB):6}) | area: {self.GetArea():8}"

class Perimeter:

    def __init__(self, rows, columns):
        self.Width = columns + 3
        self.Height = rows + 2
        bits = self.Width * self.Height
        self.grid = bytearray((bits + 7) // 8)
        
    @staticmethod
    def _index(width: int, row: int, column: int) -> int:
        return row * width + column

    def set_bit(self, row: int, column: int):
        idx = self._index(self.Width, row, column)
        self.grid[idx >> 3] |= 1 << (idx & 7)

    def get_bit(self, row: int, column: int) -> int:
        idx = self._index(self.Width, row, column)
        return (self.grid[idx >> 3] >> (idx & 7)) & 1

    def clear_bit(self, row: int, column: int):
        idx = self._index(self.Width, row, column)
        self.grid[idx >> 3] &= ~(1 << (idx & 7))

    def SetPoint(self, column, row):
        self.set_bit(row, column)

    def GetPoint(self, column, row):
        return self.get_bit(row, column)
    
    def MarkOutline(self, coordinates):

        opCount = len(coordinates)

        for op in range(opCount):

            if opCount > 100 and op > 0 and op%50 == 0:
                print(f"{op}/{opCount} = {(op/opCount)*100:.1f}%")

            a = coordinates.pop(0)
            b = coordinates[0]

            # coordinates von a speichern
            self.SetPoint(a.x, a.y)

            # a -> b verbinden

            startX, endX = min(a.x, b.x), max(a.x, b.x)
            startY, endY = min(a.y, b.y), max(a.y, b.y)

            for x in range(startX, endX+1):
                for y in range(startY, endY+1):
                    self.SetPoint(x, y)
            #   coordinates der zwischenschritte speichern

            coordinates.append(a)

    def Test(self, rectangle):
        for coord in rectangle.GetBorder():
            if self.GetPoint(coord.x, coord.y) == 1:
                return False
        return True
    
    def __sizeof__(self):
        size = 0
        size += sys.getsizeof(self.Height)
        size += sys.getsizeof(self.Width)
        size += sys.getsizeof(self.grid)
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

def ComputeringPerimeter(coordinates):
    perimeter = Perimeter(MAX_Y, MAX_X)
    print("Mark Outline ...")
    perimeter.MarkOutline(coordinates)
    return perimeter

def ComputingRectangles(coordinates):

    rectangles = []

    l = len(coordinates)

    for i in range(l):

        if i > 0 and i % 50 == 0:
            print(f"{(i/l) * 100:.1f}%")

        for k in range(l):
            
            if i == k:
                continue

            rectangles.append(Rectangle(coordinates[i], coordinates[k]))
    return rectangles

def TestPerimeter(rectangles, perimeter):
    valid_rectangles = []

    counter = 0
    count = len(rectangles)

    for rectangle in rectangles:
        #print(f"Testing {str(rectangle)} : ", end=' ', flush=True)
        counter += 1
        print(f"{counter} / {count} = {(counter/count)*100:.2f}%")

        if perimeter.Test(rectangle):
            valid_rectangles.append(rectangle)
            #print(f"= Accepted")
        #else:
            #print(f"= Dropped")

    return valid_rectangles

def rectangleAreaSorter(r):
    return r.GetArea()

def PrintTopRectangles(rectangles, count):
    print(f"Top {str(count)} Rectangles:")
    for rect in rectangles[0:count]:
        print(f"  {str(rect)}")

def DrawPerimeter(perimeter):
    print("Perimeter Graph:")
    for y in range(MAX_Y+2):
        for x in range(MAX_X+3):
            point = perimeter.GetPoint(x,y)
            if point == 1:
                print('○', end='', flush=True)
            else:
                print('·', end='', flush=True)
        print()

def PrintRectanglesDebug(rectangles, count):
    print("")
    print("Debugging Rectangle:")
    PrintTopRectangles(rectangles, count)
    instanceSize = sys.getsizeof(rectangles[0])
    rectanglesSize = sys.getsizeof(rectangles)
    print(f"Size of a Rectangle instance: {FormatBytes(instanceSize)}")
    print(f"Size of rectangles + {len(rectangles)} instances: {FormatBytes(rectanglesSize)} + {FormatBytes(instanceSize * len(rectangles))} = {FormatBytes(rectanglesSize+instanceSize * len(rectangles))}")
    print("")
    print(str(rectangles[0].GetBorder()))
 
def PrintPerimeterDebug(perimeter):
    print("")
    print("Debugging Perimeter:")
    if MAX_X < 80:
        DrawPerimeter(perimeter)
    print(f"Size of the Perimeter instance: {FormatBytes(sys.getsizeof(perimeter))}")
    print("")

print("reading coordinates")
coordinates, MIN_X, MAX_X, MIN_Y, MAX_Y = ReadData(FILENAME)

print("computering perimeter")
perimeter = ComputeringPerimeter(coordinates)

PrintPerimeterDebug(perimeter)

print("computering rectangles")
rectangles = ComputingRectangles(coordinates)

print("order rectangles by size")
rectangles.sort(key=rectangleAreaSorter, reverse=True)

#PrintRectanglesDebug(rectangles, 20) 

print("removing rectangles out of perimeter")
valid_rectangles = TestPerimeter(rectangles, perimeter)

print("order rectangles by size")
valid_rectangles.sort(key=rectangleAreaSorter, reverse=True)

PrintRectanglesDebug(valid_rectangles,20)

print("")
print("")
print(f"largest rectangle = {str(valid_rectangles[0])}")
print("")
print("")