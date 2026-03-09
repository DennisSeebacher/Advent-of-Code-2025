#read the data into coordinates
#build the rectangles from the coordinates
#build an array with the perimeter data
#accessing the perimeter data via perimeter[row][column] is faster
#using a bitarray because a grid exploded the ram
#bitarray works good
#next problem, speed of perimetertest
# maybe inverting the test works
# also i'll try a few random spots from the rectangle border, not all of them

import sys
import random

samples = 50

InputFilename = './challenge9/input'
InputFilename = './challenge9/test'

CollisionFilename = "./challenge9/collision.bin"

MIN_X = -1
MAX_Y = -1
MIN_X = -1
MAX_Y = -1

def FormatBits(size: int):
    if size < 2048:
        return f"{size:.0f} bits"
    else:
        return FormatBytes(size/8)

def FormatBytes(size:int):
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

    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.id = Coordinate.idCounter
        Coordinate.idCounter += 1

    def __str__(self):
        return f"({self.column}/{self.row})"
    
    def __repr__(self):
        return f"({self.column},{self.row})"
    
    def __eq__(self, other):
        if type(other) != type(self):
            return False
        else: 
            return self.column == other.column and self.row == other.row
        
    def __lt__(self, other):
        if type(other) != type(self):
            raise TypeError()
        else:
            return self.column < other.column and self.row < other.row
        
    def __gt__(self, other):
        if type(other) != type(self):
            raise TypeError()
        else:
            return self.column > other.column and self.row > other.row

class Rectangle:

    idCounter = 0    

    def __init__(self, coordinateA, coordinateB):
        self.coordinateA = None
        self.coordinateB = None
        if coordinateA < coordinateB:
            self.coordinateA = coordinateA
            self.coordinateB = coordinateB
        else:
            self.coordinateA = coordinateB
            self.coordinateB = coordinateA

        self.id = Rectangle.idCounter
        side_a = abs(self.coordinateA.column - self.coordinateB.column) +1 
        side_b = abs(self.coordinateA.row - self.coordinateB.row) +1
        self.Area = side_a * side_b
        self.Corners = []
        self.Corners.append( ( min(self.coordinateA.column, self.coordinateB.column) , min(self.coordinateA.row, self.coordinateB.row) ) )
        self.Corners.append( ( max(self.coordinateA.column, self.coordinateB.column) , max(self.coordinateA.row, self.coordinateB.row) ) )
        Rectangle.idCounter += 1

    def GetBorder(self):
        coords = []

        left = min(self.coordinateA.column, self.coordinateB.column)
        right = max(self.coordinateA.column, self.coordinateB.column)
        up = min(self.coordinateA.row, self.coordinateB.row)
        down = max(self.coordinateA.row, self.coordinateB.row)
        
        coords.append(Coordinate(left, up))

        for column in range(left+1, right):
            coords.append(Coordinate(column, up))
            coords.append(Coordinate(column, down))
        
        coords.append(Coordinate(right, up))
        
        for row in range(min(self.coordinateA.row, self.coordinateB.row)+1, max(self.coordinateA.row, self.coordinateB.row)):
            coords.append(Coordinate(left, row))
            coords.append(Coordinate(right, row))

        coords.append(Coordinate(left, down))
        coords.append(Coordinate(right, down))

        return coords
    
    def __str__(self):
        return f"id: {self.id:8} | a->b: ({str(self.coordinateA):14}-> {str(self.coordinateB):14}) | area: {self.Area:8}"

class Perimeter:

    def __init__(self, columns, rows):
        self.Width = columns + 3 + 2
        self.Height = rows + 2
        bits_needed = (self.Width) * (self.Height)
        bytes_aligned = ((bits_needed + 7) // 8)
        print(f"Creating Perimeter for {FormatBits(bits_needed)} ({FormatBits(bytes_aligned*8)}).")
        self.grid = bytearray(bytes_aligned)
        
    @staticmethod
    def _index(width: int, row: int, column: int):
        return row * width + column

    def SetPoint(self, column:int, row:int):
        idx = self._index(self.Width, row, column)
        self.grid[idx >> 3] |= 1 << (idx & 7)

    def GetPoint(self, column:int, row:int):
        idx = self._index(self.Width, row, column)
        return (self.grid[idx >> 3] >> (idx & 7)) & 1

    def clear_bit(self, row: int, column: int):
        idx = self._index(self.Width, row, column)
        self.grid[idx >> 3] &= ~(1 << (idx & 7))
    
    def MarkOutline(self, coordinates:list):

        opCount = len(coordinates)

        for op in range(opCount):

            if opCount > 100 and op > 0 and op%50 == 0:
                print(f"{op}/{opCount} = {(op/opCount)*100:.1f}%")

            a = coordinates.pop(0)
            b = coordinates[0]

            # coordinates von a speichern
            self.SetPoint(a.column, a.row)

            # a -> b verbinden
            startColumn, endColumn = min(a.column, b.column), max(a.column, b.column)
            startRow, endRow = min(a.row, b.row), max(a.row, b.row)

            for column in range(startColumn, endColumn+1):
                for row in range(startRow, endRow+1):
                    self.SetPoint(column, row)
            #   coordinates der zwischenschritte speichern

            coordinates.append(a)

    def Test(self, rectangle:Rectangle):
        for coord in rectangle.GetBorder():
            if self.GetPoint(coord.column, coord.row) == 1:
                return False
        return True
    
    def Test2(self, rectangle:Rectangle):

        #TODO hier weitermachen, alle werden rausgekegelt, warum?

        points = rectangle.GetBorder()

        random.shuffle(points)

        for coord in points[0:min(50,len(points))]:
            value = self.GetPoint(coord.column, coord.row)
            if value == 0:
                return False
        return True
    
    def __sizeof__(self):
        size = 0
        size += sys.getsizeof(self.Height)
        size += sys.getsizeof(self.Width)
        size += sys.getsizeof(self.grid)
        return size

def ReadData(FILENAME:str):
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
        if c.column > MAX_X: 
            MAX_X = c.column
        if c.column < MIN_X:
            MIN_X = c.column
        if c.row > MAX_Y: 
            MAX_Y = c.row
        if c.row < MIN_Y:
            MIN_Y = c.row
    return coordinates, (MIN_X, MIN_Y), (MAX_X, MAX_Y)

def ComputeringPerimeter(coordinates:list):
    perimeter = Perimeter(MAX_X, MAX_Y)
    print("Mark Outline ...")
    perimeter.MarkOutline(coordinates)
    return perimeter

def ComputingRectangles(coordinates:list):

    rectangles = []

    l = len(coordinates)

    for i in range(l):

        if i > 0 and i % 50 == 0:
            print(f"{(i/l) * 100:.1f}%")

        for k in range(i,l):
            
            if i == k:
                continue

            rectangles.append(Rectangle(coordinates[i], coordinates[k]))
    return rectangles

def TestPerimeter(rectangles:list, perimeter:Perimeter):
    valid_rectangles = []

    counter = 0
    count = len(rectangles)

    for rectangle in rectangles:
        #print(f"Testing {str(rectangle)} : ", end=' ', flush=True)
        counter += 1
        print(f"{counter} / {count} = {(counter/count)*100:.2f}%" , end=' ')

        if perimeter.Test2(rectangle):
            valid_rectangles.append(rectangle)
            print(f"+")
        else:
            print(f"-")

    return valid_rectangles

def rectangleAreaSorter(r:Rectangle):
    return r.Area

def PrintTopRectangles(rectangles:list, count:int):
    count = min(len(rectangles), count)
    print(f"Top {str(count)} Rectangles:")
    for rect in rectangles[0:count]:
        print(f"  {str(rect)}")

def DrawPerimeter(perimeter:Perimeter):
    print("Perimeter Graph:")
    for row in range(perimeter.Height):
        for column in range(perimeter.Width):
            point = perimeter.GetPoint(column,row)
            if point == 1:
                print('○', end='', flush=True)
            else:
                print('·', end='', flush=True)
        print()

def PrintRectanglesDebug(rectangles:list, count:int):
    print("")
    print("Debugging Rectangle:")
    PrintTopRectangles(rectangles, count)
    instanceSize = sys.getsizeof(rectangles[0])
    rectanglesSize = sys.getsizeof(rectangles)
    print(f"Size of a Rectangle instance: {FormatBytes(instanceSize)}")
    print(f"Size of rectangles + {len(rectangles)} instances: {FormatBytes(rectanglesSize)} + {FormatBytes(instanceSize * len(rectangles))} = {FormatBytes(rectanglesSize+instanceSize * len(rectangles))}")
    print("")

def PrintRectangle(rect:Rectangle, perimeter: Perimeter):
    if MAX_X < 80:

        # ▓▒░█

        print("")
        border = rect.GetBorder()
        for row in range(0,perimeter.Height):
            for col in range(0, perimeter.Width):
                if Coordinate(col,row) in border:
                    print("█", end='')
                else:
                    if perimeter.GetPoint(col,row) == 1:
                        print("░", end='')
                    else:
                        print("·", end='')
            print()

def PrintPerimeterDebug(perimeter:Perimeter):
    print("")
    print("Debugging Perimeter:")
    if perimeter.Width < 80:
        DrawPerimeter(perimeter)
    print(f"Size of the Perimeter ({perimeter.Width}x{perimeter.Height}) instance: {FormatBytes(sys.getsizeof(perimeter))}")
    print("")

print("reading coordinates")
coordinates, MIN, MAX = ReadData(InputFilename)
MIN_X = MIN[0]
MIN_Y = MIN[1]
MAX_X = MAX[0]
MAX_Y = MAX[1]

print("computering perimeter")
perimeter = ComputeringPerimeter(coordinates)

PrintPerimeterDebug(perimeter)

# print("saving map")
# with open(CollisionFilename, "wb") as f:
#   f.write(perimeter.grid)

# sys.exit()

print("computering rectangles")
rectangles = ComputingRectangles(coordinates)

print("order rectangles by size")
rectangles.sort(key=rectangleAreaSorter, reverse=True)

print()
if MAX_X < 80:
    for i in range(len(rectangles)):
        print(str(rectangles[i]))
        print(str(rectangles[i].GetBorder()))
        PrintRectangle(rectangles[i], perimeter)
print()

print("removing rectangles out of perimeter")
valid_rectangles = TestPerimeter(rectangles, perimeter)

print("order rectangles by size")
valid_rectangles.sort(key=rectangleAreaSorter, reverse=True)

PrintRectanglesDebug(valid_rectangles,100)

print("")
print("")
print(f"largest rectangle = {str(valid_rectangles[0])}")
print("")
print("")