file = './challenge9/input'
#file = './challenge9/test'

class Coordinate:

    idCounter = 0    

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = Coordinate.idCounter
        Coordinate.idCounter += 1

    def __str__(self):
        return f"({self.x}/{self.y})"

class Rectangle:

    idCounter = 0    

    def __init__(self, coordinateA, coordinateB):
        self.coordinateA = coordinateA
        self.coordinateB = coordinateB
        self.id = Rectangle.idCounter
        Rectangle.idCounter += 1

    def Area(self):
        side_a = abs(self.coordinateA.x - self.coordinateB.x) +1 
        side_b = abs(self.coordinateA.y - self.coordinateB.y) +1
        return side_a * side_b
    
    def __str__(self):
        return f"{self.id} (str({self.coordinateA})->str({self.coordinateB})) {self.Area()}"
    
coordinates = []
rectangles = []

file = open(file)

print("reading coordinates")

for line in file.readlines():
    parts = line.split(',')
    coordinates.append(Coordinate(int(parts[0]), int(parts[1])))

print("computering squares")

l = len(coordinates)

for i in range(l):

    if i > 0 and i % 50 == 0:
        print(f"{str(i/l * 100)}%")

    for k in range(l):
        
        if i == k:
            continue

        rectangles.append(Rectangle(coordinates[i], coordinates[k]))
        
print("order squares by size")

def rectangleAreaSorter(r):
    return r.Area()

rectangles.sort(key=rectangleAreaSorter, reverse=True)

print()

for rect in rectangles[0:10]:
    print(str(rect))

print()

print(f"largest square = {str(rectangles[0])}")