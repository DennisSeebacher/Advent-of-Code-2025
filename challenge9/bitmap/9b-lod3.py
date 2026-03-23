# ************************
# *      Reasoning       *
# ************************

from classes import *

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
MAX_X = 0
MAX_Y = 0

# ************************
# ***     Methods      ***
# ************************

def ReadData(FILENAME:str):
    global MAX_X, MAX_Y
    coordinates = []
    
    file = open(FILENAME)
    for line in file.readlines():
        parts = line.split(',')
        c = Coordinate(int(parts[0]), int(parts[1]))
        coordinates.append(c)
        if c.column > MAX_X: 
            MAX_X = c.column
        if c.row > MAX_Y: 
            MAX_Y = c.row
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
if rect_count-len(rectangles) == 0:
    raise ValueError("this should not be zero")
rect_count = len(rectangles)

print("Largest Rectangle:")
print(rectangles[0])

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

svg_body += "\n" + f"<rect x=\"{rectangles[0].coordinateA.x}\" y=\"{rectangles[0].coordinateA.y}\" width=\"{rectangles[0].width}\" height=\"{rectangles[0].height}\" style=\"fill:rgb(255,192,192);stroke-width:12;stroke:blue\"></rect>"  + "\n"

svg_end = "</svg>"

svg_representation = svg_head + svg_body + svg_end

with open("./challenge9/result.svg", "w") as file:
    file.write(svg_representation)