# ************************
# *      Reasoning       *
# ************************

# - get the info from 9b-lod2.py and get the result

# ************************
# ***     switches     ***
# ************************

problematic_rectangle = [248,250]
THRESHOLD = 200000

# ************************
# ***    variables     ***
# ************************

InputFilename = './challenge9/input'

# ************************
# ***     Classes      ***
# ************************

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
    
    def TestIntersect(self, other):
        # HIER WEITERMACHEN
        # darf sich berühren
        # darf nicht überschneiden
        return False

# ************************
# ***     Methods      ***
# ************************

def ReadData(FILENAME:str):
    coordinates = []
    
    file = open(FILENAME)
    for line in file.readlines():
        parts = line.split(',')
        c = Coordinate(int(parts[0]), int(parts[1]))
        coordinates.append(c)
    return coordinates

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

def RectAreaSort(r):
    return r.Area

def rectMinSizeFilter(r):
    global THRESHOLD

    if r.coordinateA.x == r.coordinateB.x:
        return False
    
    if r.coordinateA.y == r.coordinateB.y:
        return False
    
    if r.Area > THRESHOLD:
        return True
    else:
        return False

def rectIntersectFilter(r):
    global problematic_rectangle
    if r.TestIntersect(problematic_rectangle):
        return False
    else:
        return True

# ************************
# ***       Main       ***
# ************************

print("Reading coordinates")
coordinates = ReadData(InputFilename)

print("Generating Rectangles")
a = list(filter(lambda x:x.id == problematic_rectangle[0], coordinates))[0]
b = list(filter(lambda x:x.id == problematic_rectangle[1], coordinates))[0]
problematic_rectangle = Rectangle(a, b)
rectangles = GenerateRectangles(coordinates)
rect_count = len(rectangles)

print("Sorting Rectangles")
rectangles.sort(key = RectAreaSort, reverse=True)

print("Pruning small Rectangles")
rectangles = list(filter(rectMinSizeFilter, rectangles))
print(f"removed {rect_count-len(rectangles)}")
rect_count = len(rectangles)

print("Pruning intersecting Rectangles")
rectangles = list(filter(rectIntersectFilter, rectangles))
print(f"removed {rect_count-len(rectangles)}")
rect_count = len(rectangles)

print("Largest Rectangle:")
print(rectangles[0])