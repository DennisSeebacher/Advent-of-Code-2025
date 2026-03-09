#read the data into coordinates
#build the rectangles from the coordinates
#build an array with the perimeter data
#accessing the perimeter data via perimeter[row][column] is faster
#using a bitarray because a grid exploded the ram
#bitarray works good
#next problem, speed of perimetertest
# maybe inverting the test works
# also i'll try a few random spots from the rectangle border, not all of them

import os
import sys
import random
import threading
import time

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
        self.Width = columns
        self.Height = rows + 2
        self.Width = ((self.Width + 7) // 8) * 8
        bits_needed = self.Width * self.Height
        bytes_aligned = ((bits_needed + 7) // 8)
        print(f"Creating Perimeter for {self.Width}*{self.Height} = {FormatBits(bits_needed)}.")
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
    
    def Draw(self):
        print(f"Perimeter Graph ({self.Width}*{self.Height})")
        for row in range(self.Height):
            for column in range(self.Width):
                point = self.GetPoint(column,row)
                if point == 1:
                    print('○', end='', flush=True)
                else:
                    print('·', end='', flush=True)
            print()

    def MarkOutline(self, coordinates:list):

        opCount = len(coordinates)
        divider = 10
        interval = opCount / divider

        for op in range(opCount):

            if opCount > 100 and op > 0 and op % interval == 0:
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

    def FillThreaded(self, num_threads):
        print(f"Filling Holes ({num_threads} Threads) ({self.Height/num_threads} rows per thread) (Prepare for Takeoff!) ...")

        def fill_threadlet(r_start, r_end, r_id):
            #print(f"#{r_id:8} -> Filling")

            for row in range(r_start, r_end):
                inside = False
                col = 0
                if row > 0 and row % 500 == 0:
                    print(f"#{r_id:8} -> {row-r_start}/{r_end-r_start} = {((row-r_start)/(r_end-r_start))*100:.1f}%")
                
                while col < self.Width:

                    #prev = self.GetPoint(col-1, row) if col > 0 else 0
                    curr = self.GetPoint(col, row)
                    next = self.GetPoint(col+1, row) if col <= self.Width else 0
                    abovenext = self.GetPoint(col+1, row-1) if row > 0 else 0
                    above = self.GetPoint(col, row-1) if row > 0 else 0
                    #below = self.GetPoint(col, row+1) if row < self.Height else 0

                    if curr == 1 and next == 0 and above == 1 and abovenext == 1:
                        inside = True

                    elif curr == 1 and above == 1 and abovenext == 0:
                        inside = False

                    if curr == 0 and inside:
                        print(f"#{r_id:8} -> Set 1 @ {col}, {row}")
                        self.SetPoint(col, row)

                    col += 1

            print(f"#{r_id:8} -> finished")

        threads = []
        range_count = self.Height // num_threads

        ranges = []
        for c in range(num_threads):
            ranges.append((0+c*range_count, range_count+c*range_count, c))
        if ranges[-1][1] < self.Height:
            ranges.append((ranges[-1][1]+1,self.Height, num_threads))

        for r in ranges:
            t = threading.Thread(target=fill_threadlet, args=(r))
            threads.append(t)

        ranges.clear()

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        threads.clear()

        print("All threads finished")

        for r in ranges:
            print(f"#{r[0]:8} -> {FormatBytes(sys.getsizeof(r[1]))}")

        if self.Width < 80:
            for r in ranges:
                r[1].Draw()

    def Fill(self):

        print("Filling Holes...")
        for row in range(self.Height):

            if row > 0 and row % 50 == 0:
                print(f"{row}/{self.Height} = {(row/self.Height)*100:.1f}%")

            col = 0
            while col < self.Width:
            #for col in range(self.Width):
                if self.GetPoint(col, row) == 1:
                    end = None
                    for col2 in range(col + 1, self.Width):
                        if self.GetPoint(col2, row) == 1:
                            end = col2
                            break
                    if end is not None:
                        for i in range(col + 1 , end):
                            self.SetPoint(i, row)
                        col = end
                        continue
                col += 1
     
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
    print("Debugging Perimeter:")
    if perimeter.Width < 80:
        perimeter.Draw()
    print(f"Size of the Perimeter ({perimeter.Width}x{perimeter.Height}) instance: {FormatBytes(sys.getsizeof(perimeter))}")

print("reading coordinates")
coordinates, MIN, MAX = ReadData(InputFilename)
MIN_X = MIN[0]
MIN_Y = MIN[1]
MAX_X = MAX[0]
MAX_Y = MAX[1]

print(f"Coordinates range from {MIN_X}/{MIN_Y} to {MAX_X}/{MAX_Y}")
if len(coordinates) < 15:
    for coord in coordinates:
        print(str(coord))

print("computering perimeter")
perimeter = ComputeringPerimeter(coordinates)
PrintPerimeterDebug(perimeter)

#num_threads = 4
#if perimeter.Height > 1024:
num_threads = min(perimeter.Height//8,os.cpu_count())
perimeter.FillThreaded(num_threads)
#else:
    #perimeter.Fill()

PrintPerimeterDebug(perimeter)

print("saving map")
with open(CollisionFilename, "wb") as f:
  f.write(perimeter.grid)