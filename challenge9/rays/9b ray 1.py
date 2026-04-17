from enum import Enum
from time import time

# ********************
# *     Switches     *
# ********************

TEST = False

# ********************
# *    Variables     *
# ********************

# left, top, right, bottom borders of the grid
Borders = [0,0,-1,-1] 

# i know from a visualization that the perimeter will look like a circle with a nearly full cut through in the middle

# the following two coordinates define the rectangle that cuts the circle in two halves
problematic_rectangle_ids = [248,250]
problematic_rectangle = None

# i need to build the rectangles in two sets, one from 0 to 248 and one from 250 to the end
upper_rectangles_ids = [0,248]
upper_rectangles = None

lower_rectangles_ids = [250,494]
lower_rectangles = None

#for the validation i need to save to upper and lower part of the perimeter separately, so i can test the rectangles against the correct part of the perimeter
#added benefit, smaller number of edges to test against for each rectangle, which should speed up the validation process
upper_perimeter = None
upper_perimeter_bounds = [250,493]

lower_perimeter = None
lower_perimeter_bounds = [0,249]

InputFilename = None 
VisOutFilename = None

if TEST:
    InputFilename = './challenge9/test'
    VisOutFilename = './challenge9/rays/vis_test.svg'
else:
    InputFilename = './challenge9/input'
    VisOutFilename = './challenge9/rays/vis_input.svg'

# ********************
# *     Classes     *
# ********************

class Coordinate:

    idCounter = 0    

    def __init__(self, column, row):
        self.column = column
        self.x = self.column
        self.row = row
        self.y = self.row
        self.isOnPerimeter = False
        self.id = Coordinate.idCounter
        Coordinate.idCounter += 1

    def __str__(self):
        return f"Coordinate #{self.id} ({self.column},{self.row})"
    
    def __repr__(self):
        return f"#{self.id} ({self.column},{self.row})"
    
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

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Edge:
    def __init__(self, start:Coordinate, end:Coordinate):
        self.start = start
        self.end = end
        self.direction = None
        self.direction = self.determine_direction()
        #self.coordinates = self.get_all_coordinates()

    def determine_direction(self):
        if self.start.x == self.end.x:
            # vertical edge
            if self.start.y < self.end.y:
                # edge goes downwards
                return Direction.DOWN
            else:
                # edge goes upwards
                return Direction.UP
        else:
            # horizontal edge
            if self.start.x < self.end.x:
                # edge goes to the right
                return Direction.RIGHT
            else:
                # edge goes to the left
                return Direction.LEFT

    def get_all_coordinates(self):
        '''create all coordinates that are on the edge, and return them as a set'''
        # This is a simple implementation for a straight line edge
        coordinates = set()
        x, y = self.start.x, self.start.y
        dx = 1 if self.end.x > self.start.x else -1 if self.end.x < self.start.x else 0
        dy = 1 if self.end.y > self.start.y else -1 if self.end.y < self.start.y else 0

        while (x, y) != (self.end.x, self.end.y):
            coordinates.add(Coordinate(x, y))
            x += dx
            y += dy
        coordinates.add(Coordinate(self.end.x, self.end.y))
        return coordinates

    def __str__(self):
        return f"Edge {self.start.id} -> {self.end.id} : {self.direction}"
    
    def __repr__(self):
        return f"Edge {self.start.id} -> {self.end.id} : {self.direction}"

class Perimeter:
    def __init__(self):
        self.edges = []
        self.coordinates = []
    
    def Test(self, coordinate:Coordinate, verbose=False):
        '''checks if the coordinate is right of all edges that are intersected by a ray from the coordinate to all four cardinal directions'''

        global Borders

        if verbose:
            print(f' Testing {coordinate}:')

        if coordinate_is_on_perimeter(coordinate, self):
            if verbose:
                print(f'  {coordinate} is on the perimeter, it is inside')
            return True

        if verbose:
            print(f'  calculation of intersections with rays to the four cardinal directions..')

        intersections = set()

        # create the rays from the coordinate to the four cardinal directions
        ray_up = Edge(coordinate, Coordinate(coordinate.x, Borders[1]))
        ray_down = Edge(coordinate, Coordinate(coordinate.x, Borders[3]))
        ray_left = Edge(coordinate, Coordinate(Borders[0], coordinate.y))
        ray_right = Edge(coordinate, Coordinate(Borders[2], coordinate.y))

        # test the intersections of the rays with the edges of the perimeter, and add the intersected edges to the intersections list   
        # if the ray goes up, test only edges going left or right
        # if the ray goes down, test only edges going left or right
        # if the ray goes left, test only edges going up or down
        # if the ray goes right, test only edges going up or down

        for edge in self.edges:
            if edge.direction in [Direction.LEFT, Direction.RIGHT]:
                if do_edges_intersect(ray_up, edge):
                    intersections.add(edge)
                if do_edges_intersect(ray_down, edge):
                    intersections.add(edge)
            elif edge.direction in [Direction.UP, Direction.DOWN]:
                if do_edges_intersect(ray_left, edge):
                    intersections.add(edge) 
                if do_edges_intersect(ray_right, edge):
                    intersections.add(edge)

        # no intersections with the edges, so the coordinate is outside
        if len(intersections) == 0:
            if verbose:
                print(f'  {coordinate} has no intersections, it is outside')
            return False    
        else:
            # check each intersection, if the coordinate is right of all edges, then it is inside
            if verbose:
                print(f'  {coordinate} has {len(intersections)} intersections with edges, testing if it is right of all edges')

            result = True

            for edge in intersections:
                if verbose:
                    print(f'    testing if {coordinate} is right of {edge}')
                if not is_coordinate_right_of_edge(coordinate, edge):
                    if verbose:
                        print(f'      {coordinate} is not right of {edge}')
                    result = False

            if verbose:
                if result:
                    print(f'  {coordinate} is right of all edges, it is inside')
                else:                
                    print(f'  {coordinate} is not right of all edges, it is outside')

            return result

    def __str__(self):
        return f"Perimeter with {len(self.edges)} edges"
    
    def __repr__(self):
        return f"Perimeter with {len(self.edges)} edges"

class Rectangle:
    def __init__(self, top_left:Coordinate, bottom_right:Coordinate):
        self.A = top_left
        self.B = Coordinate(bottom_right.x, top_left.y)
        self.C = bottom_right
        self.D = Coordinate(top_left.x, bottom_right.y)
        self.Area = (self.C.x - self.A.x) * (self.C.y - self.A.y)
        self.width = self.C.x - self.A.x
        self.height = self.C.y - self.A.y

# ********************
# *    Functions     *
# ********************

def coordinate_is_on_perimeter(coordinate:Coordinate, perimeter:Perimeter):
    '''returns true if the coordinate is on the perimeter, false otherwise'''
    return coordinate in perimeter.coordinates

def is_coordinate_right_of_edge(coordinate:Coordinate, edge:Edge):
        '''returns true if the coordinate is right of the edge, false otherwise'''

        if edge.direction == Direction.RIGHT:
            return coordinate.y >= edge.start.y
        elif edge.direction == Direction.LEFT:
            return coordinate.y <= edge.start.y
        elif edge.direction == Direction.DOWN:
            return coordinate.x <= edge.start.x
        elif edge.direction == Direction.UP:
            return coordinate.x >= edge.start.x

def do_edges_intersect(edge1:Edge, edge2:Edge):
    '''returns true if the two edges intersect, false otherwise'''
    # if any of the points from edge1.get_all_coordinates() is in edge2.get_all_coordinates(), then the edges intersect
    
    # checking the all coordinates of both edges for intersection takes too long
    # faster should be to check the positions of the edges against each other, and determine if they intersect based on their directions and positions
    # there are four cases the edges can be positioned against each other:
    # one edge is horizontal, the other is vertical, and they intersect in one point
    ## a is left/right and b is up/down, and a's y coordinate is between b's start and end y coordinates, and b's x coordinate is between a's start and end x coordinates
    ## a is up/down and b is left/right, and a's x coordinate is between b's start and end x coordinates, and b's y coordinate is between a's start and end y coordinates
    # one edge is horizontal, the other is vertical, and they do not intersect
    # both edges have the same direction, and they intersect
    ## a and b are both left/right, and they are on the same y coordinate, and their x coordinates overlap
    ## a and b are both up/down, and they are on the same x coordinate, and their y coordinates overlap
    # both edges have the same direction, and they do not intersect

    if edge1.direction in [Direction.LEFT, Direction.RIGHT] and edge2.direction in [Direction.UP, Direction.DOWN]:
        if edge1.start.y >= min(edge2.start.y, edge2.end.y) and edge1.start.y <= max(edge2.start.y, edge2.end.y) and edge2.start.x >= min(edge1.start.x, edge1.end.x) and edge2.start.x <= max(edge1.start.x, edge1.end.x):
            return True
    elif edge1.direction in [Direction.UP, Direction.DOWN] and edge2.direction in [Direction.LEFT, Direction.RIGHT]:
        if edge1.start.x >= min(edge2.start.x, edge2.end.x) and edge1.start.x <= max(edge2.start.x, edge2.end.x) and edge2.start.y >= min(edge1.start.y, edge1.end.y) and edge2.start.y <= max(edge1.start.y, edge1.end.y):
            return True
    elif edge1.direction in [Direction.LEFT, Direction.RIGHT] and edge2.direction in [Direction.LEFT, Direction.RIGHT]:
        if edge1.start.y == edge2.start.y and max(edge1.start.x, edge1.end.x) >= min(edge2.start.x, edge2.end.x) and min(edge1.start.x, edge1.end.x) <= max(edge2.start.x, edge2.end.x):
            return True
    elif edge1.direction in [Direction.UP, Direction.DOWN] and edge2.direction in [Direction.UP, Direction.DOWN]:
        if edge1.start.x == edge2.start.x and max(edge1.start.y, edge1.end.y) >= min(edge2.start.y, edge2.end.y) and min(edge1.start.y, edge1.end.y) <= max(edge2.start.y, edge2.end.y):
            return True

    # for coord in edge1.coordinates:
    #     if coord in edge2.coordinates:
    #         return True
    return False

def read_data(FILENAME:str):
    '''reads the coordinates from the input file and returns a list of Coordinate objects'''

    coordinates = []
    file = open(FILENAME)
    for line in file.readlines():
        parts = line.split(',')
        c = Coordinate(int(parts[0]), int(parts[1]))
        coordinates.append(c)
    return coordinates

def set_borders(coordinates:list[Coordinate]):
    '''sets the borders of the grid based on the coordinates, and returns a list of the borders [MIN_X, MIN_Y, MAX_X, MAX_Y]'''
    
    MIN_X = 9999999999999999
    MIN_Y = 9999999999999999
    MAX_X = 0
    MAX_Y = 0

    for coord in coordinates:
        if coord.column > MAX_X:
            MAX_X = coord.column
        if coord.column < MIN_X:
            MIN_X = coord.column
        if coord.row > MAX_Y:
            MAX_Y = coord.row
        if coord.row < MIN_Y:
            MIN_Y = coord.row

    return [MIN_X, MIN_Y, MAX_X, MAX_Y]

def process_perimeter(coordinates:list[Coordinate], perimeter_bounds:list[Coordinate]):
    '''create a perimeter object and fill it with coordinates between the perimeter_bounds and then the edges'''

    print(f'creating perimeter between {perimeter_bounds}')

    PerimeterObject = Perimeter()

    #check if the given coordinates are of len 2 and in correct order
    if len(perimeter_bounds) != 2:
        raise ValueError("perimeter bounds must be a list of two coordinates")
    if perimeter_bounds[0] > perimeter_bounds[1]:
        raise ValueError("perimeter bounds must be in correct order, the first coordinate must have a smaller id than the second coordinate")

    # only add coordinates that are within the perimeter bounds to the perimeter object, and create edges between them in the order they appear in the coordinates list
    for coord in coordinates:
        if perimeter_bounds[0] <= coord.id <= perimeter_bounds[1]:
            coord.isOnPerimeter = True
            PerimeterObject.coordinates.append(coord)

    print(f'  creating edges')
    #create the edges between consecutive coordinates, closing the shape
    for i in range(-1, len(PerimeterObject.coordinates)-1):
        print(f"\r    {i} / {len(PerimeterObject.coordinates)}", end='        ', flush=True)
        PerimeterObject.edges.append(Edge(PerimeterObject.coordinates[i-1], PerimeterObject.coordinates[i]))
    print()
    return PerimeterObject

def draw_result(Filename:str, special_coordinates:list[Coordinate]=[]):
    '''draws the perimeter and the coordinates to an svg file, with the special coordinates highlighted in red'''
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

    if len(special_coordinates) > 0:
        svg_special_circles = " \n"
        for coordinate in special_coordinates:
            svg_special_circles += f'  <circle cx="{coordinate.x}" cy="{coordinate.y}" r ="{stroke_width*2}" fill="red"/>' + "\n"
        svg_special_circles += " \n"
        svg_body += svg_special_circles

    svg_end = "</svg>"

    svg_representation = svg_head + svg_body + svg_end

    with open(Filename, "w") as file:
        file.write(svg_representation)

def ascii_visualization():
    if len(coordinates) < 15:
        print()
        for row in range(0, Borders[3]+2):
            for column in range(0, Borders[2]+2):
                test_coordinate = Coordinate(column, row)
                if perimeter.Test(test_coordinate):
                    print('■', end="")
                else:
                    print('∙', end="")
            print()
        print()

def create_rectangles(coordinates:list[Coordinate], start_id:int, end_id:int):
    '''creates rectangles from the coordinates between the given ids, and returns a list of the rectangles'''
    # a rectangle is defined by two coordinates, the top left and the bottom right corner
    # to create rectangles from the coordinates, we can iterate through all pairs of coordinates, and create a rectangle from them if they are not on the same row or column

    #check if ids are in correct order
    if start_id > end_id:
        start_id, end_id = end_id, start_id 

    print(f'  creating rectangles between {start_id} and {end_id}')

    rectangles = []

    for i in range(start_id, end_id):
        for j in range(i+1, end_id+1):
            if coordinates[i].x != coordinates[j].x and coordinates[i].y != coordinates[j].y:
                top_left = Coordinate(min(coordinates[i].x, coordinates[j].x), min(coordinates[i].y, coordinates[j].y))
                bottom_right = Coordinate(max(coordinates[i].x, coordinates[j].x), max(coordinates[i].y, coordinates[j].y))
                rectangles.append(Rectangle(top_left, bottom_right))

    return rectangles

validity_counter = 0

def validate_rectangles(rectangles:list[Rectangle], perimeter:Perimeter):
    '''tests the rectangles for validity, and returns a list of the valid rectangles'''
    global validity_counter
    # Validity is defined as: the rectangle is completely inside the perimeter, which means that all four corners of the rectangle are inside the perimeter
    valid_rectangles = []
    for rectangle in rectangles:
        validity_counter += 1
        print(f'\r  tested {validity_counter} rectangles, found {len(valid_rectangles)} valid rectangles', end="", flush=True)

        if perimeter.Test(rectangle.A) and perimeter.Test(rectangle.B) and perimeter.Test(rectangle.C) and perimeter.Test(rectangle.D):
            valid_rectangles.append(rectangle)
        
    return valid_rectangles

def draw_perimeter(Filename:str, upper_perimeter:Perimeter, lower_perimeter:Perimeter):
    '''draws the perimeter to an svg file, with the upper perimeter in blue and the lower perimeter in green'''

    global Borders

    padding = 2
    stroke_width = 0.5

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

    svg_circles = " \n"
    for coordinate in upper_perimeter.coordinates:
        svg_circles += f'  <circle cx="{coordinate.x}" cy="{coordinate.y}" r ="{stroke_width}" fill="black"/>' + "\n"

    for coordinate in lower_perimeter.coordinates:
        svg_circles += f'  <circle cx="{coordinate.x}" cy="{coordinate.y}" r ="{stroke_width}" fill="black"/>' + "\n"

    svg_upper_lines = ""
    for edge in upper_perimeter.edges:
        svg_upper_lines += f'  <line x1="{edge.start.x}" y1="{edge.start.y}" x2="{edge.end.x}" y2="{edge.end.y}" style="stroke:blue; stroke-width:{stroke_width};" />' + "\n"

    svg_lower_lines = ""
    for edge in lower_perimeter.edges:  
        svg_lower_lines += f'  <line x1="{edge.start.x}" y1="{edge.start.y}" x2="{edge.end.x}" y2="{edge.end.y}" style="stroke:green; stroke-width:{stroke_width};" />' + "\n"
        
    svg_body = svg_upper_lines +" \n" + " \n" + svg_lower_lines + " \n"
    svg_body += svg_circles

    svg_end = "</svg>"

    svg_representation = svg_head + svg_body + svg_end

    with open(Filename, "w") as file:
        file.write(svg_representation)

def draw_rectangles(Filename:str, upper:list[Rectangle], lower:list[Rectangle]):
    '''draws a svg with the given rectangles'''

    global Borders

    padding = 2
    stroke_width = 0.5

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
    svg_upper = ""
    svg_lower = ""
    svg_end = "</svg>"

    for rect in upper:
        svg_upper += f'    <rect x="{rect.A.x}" y="{rect.A.y}" width="{rect.width}" height="{rect.height}" stroke="black" />' + "\n"

    for rect in lower:
        svg_lower += f'    <rect x="{rect.A.x}" y="{rect.A.y}" width="{rect.width}" height="{rect.height}" stroke="black" />' + "\n"

    svg_representation = svg_head + "\n" + svg_upper + "\n" + svg_lower + "\n" + svg_end

    with open(Filename, "w") as file:
        file.write(svg_representation)

# ********************
# *       Main       *
# ********************

if TEST:
    print("TEST MODE")
    test_coordinates = [Coordinate(9,3), Coordinate(3,6), Coordinate(0,0), Coordinate(2,5), Coordinate(2,4), Coordinate(2,3), Coordinate(4,3)]

else:
    print("INPUT MODE")
    test_coordinates = [Coordinate(0,0), Coordinate(2000,2000)]

coordinates = read_data(InputFilename)
Borders = set_borders(coordinates)

# print(f"coordinates range from {Borders[0]}/{Borders[1]} to {Borders[2]}/{Borders[3]}")
# if len(coordinates) < 15:
#     for coord in coordinates:
#         print(str(coord))
    
upper_perimeter = process_perimeter(coordinates, upper_perimeter_bounds)
lower_perimeter = process_perimeter(coordinates, lower_perimeter_bounds)

# for edge in upper_perimeter.edges:
#     print(str(edge) + " with coordinates: " + str(edge.coordinates))

# print("testing sample coordinates")
# for test_coordinate in test_coordinates:
#     perimeter.Test(test_coordinate)
# ascii_visualization()

print(f'creating rectangles from coordinates')
upper_rectangles = create_rectangles(coordinates, upper_rectangles_ids[0], upper_rectangles_ids[1])
lower_rectangles = create_rectangles(coordinates, lower_rectangles_ids[0], lower_rectangles_ids[1])

print(f'testing rectangles for validity')
upper_valid_rectangles = validate_rectangles(upper_rectangles, upper_perimeter)
lower_valid_rectangles = validate_rectangles(lower_rectangles, lower_perimeter)

print(f"found {len(lower_valid_rectangles) + len(upper_valid_rectangles)} valid rectangles")

print('ordering valid rectangles by area')                       
# #  find the largest rectangle
upper_valid_rectangles.sort(key=lambda r: r.Area, reverse=True)
lower_valid_rectangles.sort(key=lambda r: r.Area, reverse=True)
if len(upper_valid_rectangles) > 0 and len(lower_valid_rectangles) > 0:
    largest_rectangle = upper_valid_rectangles[0] if upper_valid_rectangles[0].Area > lower_valid_rectangles[0].Area else lower_valid_rectangles[0]
    print(f"largest rectangle: {largest_rectangle} with area {largest_rectangle.Area} and corners {largest_rectangle.A}, {largest_rectangle.B}, {largest_rectangle.C}, {largest_rectangle.D}")
elif len(upper_valid_rectangles) > 0:
        print(f"largest rectangle: {upper_valid_rectangles[0]} with area {upper_valid_rectangles[0].Area} and corners {upper_valid_rectangles[0].A}, {upper_valid_rectangles[0].B}, {upper_valid_rectangles[0].C}, {upper_valid_rectangles[0].D}")
elif len(lower_valid_rectangles) > 0:
    print(f"largest rectangle: {lower_valid_rectangles[0]} with area {lower_valid_rectangles[0].Area} and corners {lower_valid_rectangles[0].A}, {lower_valid_rectangles[0].B}, {lower_valid_rectangles[0].C}, {lower_valid_rectangles[0].D}")
else:
    print("No Result!")

#print(f"Drawing visualization to {VisOutFilename}")
#draw_result(VisOutFilename, special_coordinates=[largest_rectangle.A, largest_rectangle.B, largest_rectangle.C, largest_rectangle.D])
#draw_perimeter("perimeter.svg", upper_perimeter, lower_perimeter)
#draw_rectangles("rectangles.svg", upper_rectangles, lower_rectangles)