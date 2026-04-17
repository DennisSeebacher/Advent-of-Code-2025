from enum import Enum

# ********************
# *     Switches     *
# ********************

TEST = True

# ********************
# *    Variables     *
# ********************

# left, top, right, bottom borders of the grid
Borders = [0,0,-1,-1] 

InputFilename = None 
VisOutFilename = None

if TEST:
    InputFilename = './challenge9/test'
    VisOutFilename = './challenge9/abstract/vis_test.svg'
else:
    InputFilename = './challenge9/input'
    VisOutFilename = './challenge9/abstract/vis_input.svg'

# ********************
# *     Classes     *
# ********************

class region_type(Enum):
    '''enumeration for the type of region, either inside or outside'''
    INSIDE = "inside"
    OUTSIDE = "outside"

class Region:
    def __init__(self, type:region_type, start:int, end:int):
        self.type = type
        self.start = start
        self.end = end

    def is_inside(self, pos:int) -> bool:
        '''check if a position is inside this region'''
        return self.start <= pos < self.end and self.type == region_type.INSIDE

class Row:
    '''a row of the grid, which can have multiple regions of inside and outside'''
    def __init__(self, row_number:int):
        '''initialize the row with an empty list of regions'''
        self.row_number = row_number
        self.regions = []

    def add_region(self, region:Region):
        '''add an existing region to the row'''
        self.regions.append(region)

    def create_region(self, type:region_type, start:int, end:int):
        '''create and add a region to the row'''
        self.regions.append(Region(type, start, end))
    
    def sort_regions(self):
        '''sort the regions by their start position'''
        self.regions.sort(key=lambda x: x.start)

    def is_inside(self, pos:int) -> bool:
        '''check if a position is inside any of the regions'''
        for region in self.regions:
            if region.is_inside(pos):
                return region.type == region_type.INSIDE
        return False

class Perimeter:
    '''a perimeter of the grid, which can have multiple rows'''
    def __init__(self):
        '''initialize the perimeter with an empty list of rows'''
        self.rows = []

    def add_row(self, row:Row):
        '''add an existing row to the perimeter'''
        self.rows.append(row)
    
    def create_row(self, row_number:int):
        '''create and add a row to the perimeter'''
        self.rows.append(Row(row_number))

    def sort_rows(self):
        '''sort the rows by their row number'''
        self.rows.sort(key=lambda x: x.row_number)

    def has_row(self, row_number:int) -> bool:
        '''check if the perimeter has a row with the given row number'''
        for row in self.rows:
            if row.row_number == row_number:
                return True
        return False

    def get_row(self, row_number:int) -> Row:
        '''get the row with the given row number'''
        for row in self.rows:
            if row.row_number == row_number:
                return row
        raise ValueError(f"Row {row_number} not found in perimeter")

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

# ********************
# *    Functions     *
# ********************

def ReadData(FILENAME:str):
    global Borders
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
    Borders = [MIN_X, MIN_Y, MAX_X, MAX_Y]
    return coordinates

def processPerimeter(coordinates:list[Coordinate]):
    perimeter = Perimeter()
    for coordinate in coordinates:
        if perimeter.has_row(coordinate.row):
            perimeter.get_row(coordinate.row)

def draw(Filename:str):
    global Borders, coordinates, rectangles
    padding = 2
    stroke_width = 0.25

    if Borders[2] > 4000:
        padding = 8
        stroke_width = 4
    
    if Borders[2] > 40000:
        padding = 16
        stroke_width = 16

    svg_head = '<?xml version="1.0" encoding="UTF-8"?>' + "\n"
    svg_head += '<svg xmlns="http://www.w3.org/2000/svg"' + "\n"
    svg_head += 'version="1.1" baseProfile="full"' + "\n"
    svg_head += f'width="1000px" height="1000px" viewBox="{Borders[0]-padding} {Borders[1]-padding} {Borders[2]+padding} {Borders[3]+padding}"' + "\n"
    svg_head += 'style="background: #eee;">' + "\n"
    svg_head += " " + "\n"
    svg_head += f'  <rect x="{Borders[0]}" y="{Borders[1]}" width="{Borders[2] - Borders[0]}" height="{Borders[3] - Borders[1]}" fill="white" />' + "\n"
    svg_head += " " + "\n"

    svg_lines = ""
    for i in range(-1, len(coordinates)-1):
        svg_lines += f'  <line x1="{coordinates[i].x}" y1="{coordinates[i].y}" x2="{coordinates[i+1].x}" y2="{coordinates[i+1].y}" style="stroke:black; stroke-width:{stroke_width};" />' + "\n"

    svg_circles = " \n"
    for coordinate in coordinates:
        svg_circles += f'  <circle cx="{coordinate.x}" cy="{coordinate.y}" r ="{stroke_width}" fill="black"/>' + "\n"

    svg_ids = " \n"
    for coordinate in coordinates:
        svg_ids += f'  <text x="{coordinate.x}" y="{coordinate.y}" fill="red" style="font-size:{stroke_width*stroke_width};">{coordinate.id}</text>' + "\n"

    svg_body = svg_lines + svg_circles + svg_ids + " \n"

    svg_end = "</svg>"

    svg_representation = svg_head + svg_body + svg_end

    with open(Filename, "w") as file:
        file.write(svg_representation)

# ********************
# *       Main       *
# ********************

print("reading coordinates")
coordinates = ReadData(InputFilename)

print(f"coordinates range from {Borders[0]}/{Borders[1]} to {Borders[2]}/{Borders[3]}")
if len(coordinates) < 15:
    for coord in coordinates:
        print(str(coord))

print("processing perimeter")
perimeter = processPerimeter(coordinates)

print(f"Drawing visualization to {VisOutFilename}")
draw(VisOutFilename)