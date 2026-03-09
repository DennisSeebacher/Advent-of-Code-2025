import os
import sys
import random
import threading
import time

CollisionFilename = "./challenge9/collision.bin"
CollisionMetadataFilename = "./challenge9/collision.meta"

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
        self.x = self.column
        self.row = row
        self.y = self.row
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
                      
    def GenerateHalfSizeImage(self):
        print("generating compressed bitmap ...")

        if self.Height < 5000:
            return __GenerateHalfSizeImage(0,self.Height, p2)

        num_threads = 8
        threads = []
        ranges = []
        range_count = self.Height // num_threads

        print(f"compressing ({num_threads} Threads) ({self.Height/num_threads} rows per thread) (Prepare for Takeoff!) ...")
        
        p2 = Perimeter(self.Width//2 ,self.Height//2)

        def __GenerateHalfSizeImage(start_row, end_row, r_id):

            for row in range(start_row, end_row , 2):

                if row > 0 and row % 500 == 0:
                    print(f"#{r_id:8} -> {row-start_row}/{end_row-start_row} = {((row-start_row)/(end_row-start_row))*100:.1f}%")

                for col in range(0, self.Width, 2):
                    if self.GetPoint(col, row) == 1:
                        p2.SetPoint(col//2, row//2)
                        continue
                    if self.GetPoint(col+1, row) == 1:
                        p2.SetPoint(col//2, row//2)
                        continue
                    if row + 1 < self.Height:
                        if self.GetPoint(col, row+1) == 1:
                            p2.SetPoint(col//2, row//2)
                            continue
                        if self.GetPoint(col+1, row+1) == 1:
                            p2.SetPoint(col//2, row//2)
                            continue

        

        for c in range(num_threads):
            ranges.append((0+c*range_count, range_count+c*range_count, c))
        if ranges[-1][1] < self.Height:
            ranges.append((ranges[-1][1]+1,self.Height, num_threads))

        for r in ranges:
            t = threading.Thread(target=__GenerateHalfSizeImage, args=(r))
            threads.append(t)

        ranges.clear()
        
        for t in threads:
            t.start()

        for t in threads:
            t.join()

        threads.clear()

        print("All threads finished")
        
        return p2

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

        print(f"{opCount} steps")

        for op in range(opCount):

            #if opCount > 50 and op > 0 and op % interval == 0:
            print(f"{op}/{opCount} = {(op/opCount)*100:.1f}%")

            a = coordinates.pop(0)
            b = coordinates[0]
            c = coordinates[1]

            # left or right curve?
            # orient=(x2​−x1​)(y3​−y1​)−(y2​−y1​)(x3​−x1​)
            # left when orient < 0
            # right wenn orient > 0
            # straight wenn orient == 0

            orient=(b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x)

            fill = False

            if orient > 0:
                # right
                fill = True
                pass
            elif orient < 0:
                # left
                pass
            else:
                # straight
                pass

            if fill:
                startColumn, endColumn = min(a.column, c.column), max(a.column, c.column)
                startRow, endRow = min(a.row, c.row), max(a.row, c.row)

                for column in range(startColumn, endColumn+1):
                    for row in range(startRow, endRow+1):
                        self.SetPoint(column, row)
            else:
                # a -> b verbinden
                startColumn, endColumn = min(a.column, b.column), max(a.column, b.column)
                startRow, endRow = min(a.row, b.row), max(a.row, b.row)

                for column in range(startColumn, endColumn+1):
                    for row in range(startRow, endRow+1):
                        self.SetPoint(column, row)

            # coordinates von a speichern
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

def ReadPerimeterData():
    file = open(CollisionFilename, 'rb')
    meta = open(CollisionMetadataFilename)
    meta = meta.readline().split('*')
    width = int(meta[0])
    heigth = int(meta[1])

    perimeter = Perimeter(width, heigth)
    perimeter.Height -= 2

    perimeter.grid = file.read()

    return perimeter
 
def PrintPerimeterDebug(perimeter:Perimeter):
    print("Debugging Perimeter:")
    print(f"Size of the Perimeter ({perimeter.Width}x{perimeter.Height}) instance: {FormatBytes(sys.getsizeof(perimeter))}")
    if perimeter.Width <= 100:
        perimeter.Draw()
    else:
        print("generating smaller resolution image ...")
        p2 = perimeter.GenerateHalfSizeImage()
        while p2.Width > 100:
            p2 = p2.GenerateHalfSizeImage()
        p2.Draw()

print("reading collision map")
perimeter = ReadPerimeterData()
PrintPerimeterDebug(perimeter)
print("done")