from classes import *
from svg_drawer import *

# ********************
# *     Switches     *
# ********************

TEST = False

# ********************
# *    Variables     *
# ********************

if TEST:
    print("TEST MODE")
    InputFilename = './challenge9/test'
    VisOutFilename = './challenge9/inverse/vis_test.svg'
else:
    print("INPUT MODE")
    InputFilename = './challenge9/input'
    VisOutFilename = './challenge9/inverse/vis_input.svg'


# left, top, right, bottom borders of the grid
borders = [0,0,-1,-1] 

# i know from a visualization that the perimeter will look like a circle with a nearly full cut through in the middle
# the following coordinates will define the upper and lower portion of the dataset
upper_boundary_start, upper_boundary_end = 0, 247
lower_boundary_start, lower_boundary_end = 249, 493

perimeter_boundaries = [(upper_boundary_start, upper_boundary_end),(lower_boundary_start, lower_boundary_end)]

# i can further reduce the workload by removing edges that are going in the wrong direction
# to do that i need to define 4 quarters, slicing at a 45° angle
# i get the left, upper, right, lower quarters
quarters = []
# eg if i am in the right quarter, i can remove all edges going to the right

# ********************
# *    Functions     *
# ********************

def read_data(FILENAME:str):
    '''reads the coordinates from the input file and returns a list of Coordinate objects'''

    if InputFilename is None or InputFilename.strip() == '':
        raise ValueError('InputFilename may not be None or empty')

    print(f"  reading data from {InputFilename}")

    coordinates = []
    file = open(FILENAME)
    for line in file.readlines():
        parts = line.split(',')
        c = Coordinate(int(parts[0]), int(parts[1]))
        coordinates.append(c)
    return coordinates

def set_borders(coordinates:list[Coordinate]):
    '''sets the borders of the grid based on the coordinates, and returns a list of the borders [MIN_X, MIN_Y, MAX_X, MAX_Y]'''
    
    if coordinates is None or len(coordinates) == 0:
        raise ValueError('coordinates may not be none or empty')

    print("  setting borders")

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

def process_perimeters(coordinates:list[Coordinate], boundaries:list[tuple:int]):
    '''creates the perimeter objects for each given boundary'''

    if coordinates is None or len(coordinates) == 0:
        raise ValueError('coordinates may not be None or empty')
    
    if boundaries is None or len(boundaries) == 0:
        raise ValueError('boundaries may not be None or empty')

    perimeters = []

    for boundary in boundaries:
        print(f"  creating perimter for range {boundary[0]} -> {boundary[1]}")
        perimeter = Perimeter()
        for index in range(boundary[0], boundary[1]):
            perimeter.coordinates.append(coordinates[index])
            perimeter.edges.append(Edge(coordinates[index], coordinates[index+1]))
        perimeter.edges.append(Edge(coordinates[boundary[1]], coordinates[boundary[0]]))
        perimeters.append(perimeter)

    return perimeters

# ********************
# *       Main       *
# ********************

coordinates = read_data(InputFilename)
borders = set_borders(coordinates)

perimeters = process_perimeters(coordinates, perimeter_boundaries)

draw_instructions = []
draw_instructions.append(DrawCoordinates(coordinates, 'red', 32, True))
draw_instructions.append(DrawEdges([Edge(Coordinate(0,0),Coordinate(100000,100000)), Edge(Coordinate(0,100000), Coordinate(100000,0))], 'red', 16))
for perimeter in perimeters:
    draw_instructions.append(DrawEdges(perimeter.edges, 'green', 16))
draw_svg(VisOutFilename, borders, draw_instructions)

print("DONE")