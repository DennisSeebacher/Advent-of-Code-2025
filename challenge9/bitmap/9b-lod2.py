# ************************
# *      Reasoning       *
# ************************

# all previous attemps fail beceause the data size is too damn high
# the solution does not specify or need to be fully in code
# that could be done but for now the solution is as follows
# - generate a svg and look for the incision in the circle
# - make a note of the ids that are problematic
# - add this info to 9b-lod3.py and get the result

# ************************
# ***     switches     ***
# ************************


TEST = not True

# ************************
# ***     imports      ***
# ************************

import sys
import random

# ************************
# ***    variables     ***
# ************************

if TEST:
    InputFilename = './challenge9/test'
else:
    InputFilename = './challenge9/input'

MIN_X = -1
MAX_Y = -1
MIN_X = -1
MAX_Y = -1

# ************************
# ***     Classes      ***
# ************************

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
        
    def __hash__(self):
        return hash(f"{self.x}/{self.y}")

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
        self.Corners = set()
        #top left
        self.Corners.add( ( min(self.coordinateA.column, self.coordinateB.column) , min(self.coordinateA.row, self.coordinateB.row) ) )
        #top right
        self.Corners.add( ( min(self.coordinateA.column, self.coordinateB.column) , max(self.coordinateA.row, self.coordinateB.row) ) )
        #bottom left
        self.Corners.add( ( max(self.coordinateA.column, self.coordinateB.column) , min(self.coordinateA.row, self.coordinateB.row) ) )
        #bottom right
        self.Corners.add( ( max(self.coordinateA.column, self.coordinateB.column) , max(self.coordinateA.row, self.coordinateB.row) ) )
        Rectangle.idCounter += 1

    def GetBorder(self, corners = True):
        coords = []

        left = min(self.coordinateA.column, self.coordinateB.column)
        right = max(self.coordinateA.column, self.coordinateB.column)
        up = min(self.coordinateA.row, self.coordinateB.row)
        down = max(self.coordinateA.row, self.coordinateB.row)
        
        if corners: coords.append(Coordinate(left, up))

        for column in range(left+1, right):
            coords.append(Coordinate(column, up))
            coords.append(Coordinate(column, down))
        
        if corners: coords.append(Coordinate(right, up))
        
        for row in range(min(self.coordinateA.row, self.coordinateB.row)+1, max(self.coordinateA.row, self.coordinateB.row)):
            coords.append(Coordinate(left, row))
            coords.append(Coordinate(right, row))

        if corners: coords.append(Coordinate(left, down))
        if corners: coords.append(Coordinate(right, down))

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
        print(f"-> Creating Perimeter for {self.Width}*{self.Height} = {FormatBits(bits_needed)}.")
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

    def TestBorder(self, rectangle:Rectangle):
        for point in rectangle.GetBorder(corners = False):
            if self.GetPoint(point.x, point.y) == 1:
                return False
        return True

    def MarkOutline(self, coordinates:list):

        opCount = len(coordinates)
        divider = 10
        interval = opCount / divider

        for op in range(opCount):

            if opCount > 50 and op > 0 and op % interval == 0:
                print(f"      {op}/{opCount} = {(op/opCount)*100:.1f}%")

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

    def MarkOutside(self, coordinates:list):
        
        # use setpoint to connect each point in list with its follower, connect last point with first point, this is the fence that is in the grid
        # next, fill the grid beginning from 0,0, the area in the fence should not be filled
        # last redraw the fence, but this time subtract it
        # we have a bitmap now, 1 means outside, 0 means inside

        # Step 1: Draw the fence
        print("Drawing fence...")
        coords_copy = coordinates.copy()
        num_coords = len(coords_copy)
        
        for i in range(num_coords):
            if num_coords > 100 and i > 0 and i % 50 == 0:
                print(f"  Drawing: {i}/{num_coords}")
            
            a = coords_copy[i]
            b = coords_copy[(i + 1) % num_coords]  # Connect to next, wraparound to first
            
            startColumn = min(a.column, b.column)
            endColumn = max(a.column, b.column)
            startRow = min(a.row, b.row)
            endRow = max(a.row, b.row)
            
            for column in range(startColumn, endColumn + 1):
                for row in range(startRow, endRow + 1):
                    self.SetPoint(column, row)
        
        # Step 2: Flood fill from (0,0) to mark all outside areas
        print("Flood filling outside area from (0,0)...")
        self._flood_fill(0, 0)
        
        # Step 3: Clear the fence (subtract it)
        print("Clearing the fence...")
        for i in range(num_coords):
            if num_coords > 100 and i > 0 and i % 50 == 0:
                print(f"  Clearing: {i}/{num_coords}")
            
            a = coords_copy[i]
            b = coords_copy[(i + 1) % num_coords]
            
            startColumn = min(a.column, b.column)
            endColumn = max(a.column, b.column)
            startRow = min(a.row, b.row)
            endRow = max(a.row, b.row)
            
            for column in range(startColumn, endColumn + 1):
                for row in range(startRow, endRow + 1):
                    self.clear_bit(row, column)
        
        print("MarkOutside complete!")
    
    def _flood_fill(self, start_col: int, start_row: int):
        """Flood fill from a starting position using BFS"""
        from collections import deque
        
        queue = deque([(start_col, start_row)])
        visited = set()
        filled_count = 0
        total_cells = self.Width * self.Height
        
        while queue:
            col, row = queue.popleft()
            
            # Skip if already visited
            if (col, row) in visited:
                continue
            
            # Skip if out of bounds
            if col < 0 or col >= self.Width or row < 0 or row >= self.Height:
                continue
            
            # Skip if this cell is already marked (part of fence)
            if self.GetPoint(col, row) == 1:
                continue
            
            visited.add((col, row))
            self.SetPoint(col, row)
            filled_count += 1
            
            # Progress message every 100000 cells
            if filled_count % 100000 == 0:
                percentage = (filled_count / total_cells) * 100
                print(f"  {filled_count}/{total_cells}  ({percentage:.2f}%)")
            
            # Add neighbors to queue
            queue.append((col + 1, row))
            queue.append((col - 1, row))
            queue.append((col, row + 1))
            queue.append((col, row - 1))

    def __sizeof__(self):
        size = 0
        size += sys.getsizeof(self.Height)
        size += sys.getsizeof(self.Width)
        size += sys.getsizeof(self.grid)
        return size

# ************************
# ***     Methods      ***
# ************************

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

def GenerateRectangles(coordinates:list):
    rectangles = []

    l = len(coordinates)

    for i in range(l):

        if i > 0 and i % 50 == 0:
            print(f"{(i/l) * 100:.1f}%")

        for k in range(i,l):
            
            if i == k:
                continue
            
            #discard lines
            if coordinates[i].x == coordinates[k].x:
                continue
            if coordinates[i].y == coordinates[k].y:
                continue

            rectangles.append(Rectangle(coordinates[i], coordinates[k]))
    return rectangles

# ************************
# ***       Main       ***
# ************************

print("Reading coordinates")
coordinates, MIN, MAX = ReadData(InputFilename)
MIN_X = MIN[0]
MIN_Y = MIN[1]
MAX_X = MAX[0]
MAX_Y = MAX[1]

print(f"  Coordinates range from {MIN_X}/{MIN_Y} to {MAX_X}/{MAX_Y}")
if len(coordinates) < 15:
    for coord in coordinates:
        print(str(coord))

print("Generating Rectangles")
rectangles = GenerateRectangles(coordinates)

# ***** ROUGH PASS *****

print("Rough pass")

print("  Building perimeter...")
print("    Shrinking...")
perimeter_width = MAX_X
perimeter_height = MAX_Y
perimeter_divisor = 1

while perimeter_width > 40:
    perimeter_divisor += 1
    perimeter_width = MAX_X // perimeter_divisor
    perimeter_height = MAX_Y // perimeter_divisor
    print(f"    /{perimeter_divisor} => {int(perimeter_width)}*{int(perimeter_height)}")

scaled_perimeter = Perimeter(int(perimeter_width), int(perimeter_height))

scaled_coordinates = []

for c in coordinates:
    scaled_coordinates.append(Coordinate(c.x // perimeter_divisor, c.y // perimeter_divisor))

print("  Marking outline...")

scaled_perimeter.MarkOutline(scaled_coordinates)

scaled_perimeter.Draw()

# ***** Draw as SVG *****

svg_head = '<?xml version="1.0" encoding="UTF-8"?>' + "\n"
svg_head += '<svg xmlns="http://www.w3.org/2000/svg"' + "\n"
svg_head += 'version="1.1" baseProfile="full"' + "\n"
svg_head += f'width="1000px" height="1000px" viewBox="0 0 {MAX_X} {MAX_Y}"' + "\n"
svg_head += 'style="background: #fff;">' + "\n"
svg_head += " " + "\n"

svg_lines = ""
for i in range(-1, len(coordinates)-1):
    svg_lines += f'  <line x1="{coordinates[i].x}" y1="{coordinates[i].y}" x2="{coordinates[i+1].x}" y2="{coordinates[i+1].y}" style="stroke:black; stroke-width:8;" />' + "\n"

svg_circles = " \n"
for coordinate in coordinates:
    svg_circles += f'  <circle cx="{coordinate.x}" cy="{coordinate.y}" r ="256" style="stroke:black; stoke-width:8;" fill="white"/>' + "\n"

svg_ids = " \n"
for coordinate in coordinates:
    svg_ids += f'  <text x="{coordinate.x-16}" y="{coordinate.y+8}" fill="red" style="font-size:128;">{coordinate.id}</text>' + "\n"

svg_body = svg_lines + svg_circles + svg_ids + " \n"

svg_end = "</svg>"

svg_representation = svg_head + svg_body + svg_end

with open("./challenge9/input.svg", "w") as file:
    file.write(svg_representation)