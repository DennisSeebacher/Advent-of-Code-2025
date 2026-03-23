USE_TEST_DATA = True

if USE_TEST_DATA:
    FILENAME = './challenge9/test'
else:
    FILENAME = './challenge9/input'

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
            return self.x == other.x and self.y == other.y
        
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
        
    def __hash__(self):
        return hash(f"{self.x}/{self.y}")

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
    
    def GetCorners(self):
        corners = set()

        corners.add(self.coordinateA)
        corners.add(self.coordinateB)
        corners.add(Coordinate(self.coordinateA.x, self.coordinateB.y))
        corners.add(Coordinate(self.coordinateB.x, self.coordinateA.y))

        return corners

    def GetCoordinates(self):
        setOfCoordinates = set()
        
        for x in range(min(self.coordinateA.x, self.coordinateB.x), max(self.coordinateA.x, self.coordinateB.x) +1):
            for y in range(min(self.coordinateA.y, self.coordinateB.y), max(self.coordinateA.y, self.coordinateB.y) +1):
                setOfCoordinates.add((x,y))

        return setOfCoordinates
    
    def __str__(self):
        return f"#{self.id} {self.coordinateA}->{self.coordinateB} {self.GetArea()}²"

def ReadData(FILENAME):
    coordinates = []
    MAX_X = 0
    MAX_Y = 0
    file = open(FILENAME)
    for line in file.readlines():
        parts = line.split(',')
        c = Coordinate(int(parts[0]), int(parts[1]))
        coordinates.append(c)
        if c.x > MAX_X: 
            MAX_X = c.x
        if c.y > MAX_Y: 
            MAX_Y = c.y
    return coordinates, MAX_X, MAX_Y

def ComputeringPerimeter(coordinates):

    perimeter = set()

    # step 1 - mark perimeter

    opCount = len(coordinates)

    for op in range(opCount):

        if op > 0 and op % 50 == 0:
            print(f"{(op/opCount) * 100}%")

        a = coordinates.pop(0)
        b = coordinates[0]

        # coordinates von a speichern
        perimeter.add((a.x, a.y))

        # a -> b verbinden

        startX, endX = min(a.x, b.x), max(a.x, b.x)
        startY, endY = min(a.y, b.y), max(a.y, b.y)

        for x in range(startX, endX+1):
            for y in range(startY, endY+1):
                perimeter.add((x, y))
        #   coordinates der zwischenschritte speichern

        coordinates.append(a)



    return perimeter

def ComputingRectangles(coordinates):

    rectangles = []

    l = len(coordinates)

    for i in range(l):

        if i > 0 and i % 50 == 0:
            print(f"{str(i/l * 100)}%")

        for k in range(l):
            
            if i == k:
                continue

            rectangles.append(Rectangle(coordinates[i], coordinates[k]))
    return rectangles

def TestPerimeter(rectangles, perimeter):
    valid_rectangles = []

    for rectangle in rectangles:
        rectangle_coords = rectangle.GetCoordinates()
        
        # Check if all rectangle coordinates are inside perimeter using odd-even algorithm
        all_inside = True
        for x, y in rectangle_coords:
            # Cast a ray to the right and count intersections with perimeter points
            intersection_count = 0
            for px, py in perimeter:
                # Check if perimeter point is on the same horizontal line and to the right
                if py == y and px > x:
                    intersection_count += 1
            
            print(f"{x}/{y} -> {intersection_count}")

            # If odd number of intersections, point is inside
            if intersection_count % 2 == 0:
                all_inside = False
                break
        
        if all_inside:
            valid_rectangles.append(rectangle)

    return valid_rectangles

def rectangleAreaSorter(r):
    return r.GetArea()

def DrawDebugData():
    global valid_rectangles, coordinates, perimeter
    print()

    print("Valid Rectangles:")
    for item in valid_rectangles:
        print(f"  {item}")

    def AnyCoordWith(x,y):
        global coordinates
        for coord in coordinates:
                if coord.x == x and coord.y == y:
                    return True
        return False

    for y in range(MAX_Y+2):
        for x in range(MAX_X+2):
            if AnyCoordWith(x,y):
                print('○', end='', flush=True)
            elif (x,y) in perimeter:
                print('·', end='', flush=True)
            else:
                print(' ', end='', flush=True)
        print()

    print()

print("reading coordinates")
coordinates, MAX_X, MAX_Y = ReadData(FILENAME)

print("computering perimeter")
perimeter = ComputeringPerimeter(coordinates)

print("computering rectangles")
rectangles = ComputingRectangles(coordinates)

print("removing rectangles out of perimeter")
valid_rectangles = TestPerimeter(rectangles, perimeter)

print("order rectangles by size")
valid_rectangles.sort(key=rectangleAreaSorter, reverse=True)

if MAX_X < 80:
    DrawDebugData()

if len(valid_rectangles) > 0:
    print(f"largest rectangle = {str(valid_rectangles[0])}")