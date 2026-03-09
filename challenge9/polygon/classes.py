import sys
from formatter import *

class Coordinate:
    def __init__(self, col:int, row:int):
        self.Column = col
        self.Row = row
        self.X = col
        self.Y = row
    
    def __str__(self):
        return f"({self.Column}/{self.Row})"
    
    def __repr__(self):
        return f"Coordinate({self.Column},{self.Row})"
    
    def __eq__(self, other):
        if type(other) != type(self):
            return False
        else: 
            return self.Column == other.Column and self.Row == other.Row
        
    def __lt__(self, other):
        if type(other) != type(self):
            raise TypeError()
        else:
            return self.Column < other.Column and self.Row < other.Row
        
    def __gt__(self, other):
        if type(other) != type(self):
            raise TypeError()
        else:
            return self.Column > other.Column and self.Row > other.Row

class Line:
    def __init__(self, a:Coordinate, b:Coordinate):
        self.A = a
        self.B = b
        self.Ignore = False
        self.Coordinates = []
        if self.A.X == self.B.X:
            for y in range(self.A.Y, self.B.Y):
                c = Coordinate(self.A.X, y)
                if not c in self.Coordinates:
                    self.Coordinates.append(c)
        else:
            for x in range(self.A.X, self.B.X):
                c = Coordinate(x, self.A.Y)
                if not c in self.Coordinates:
                    self.Coordinates.append(c)

    def __str__(self):
        return f"{str(self.A)}/{str(self.B)}"
        
    def __repr__(self):
        return f"Line({str(self.A)},{str(self.B)})"

class Rectangle:

    idCounter = 0

    def __init__(self, A:Coordinate, B:Coordinate):
        self.id = Rectangle.idCounter
        Rectangle.idCounter += 1
        
        self.A = None
        self.B = None
        if A < B:
            self.A = A
            self.B = B
        else:
            self.A = B
            self.B = A

        side_a = abs(self.A.Column - self.B.Column) +1 
        side_b = abs(self.A.Row - self.B.Row) +1
        self.Area = side_a * side_b
        
        self.Border = []
        start_y = min(A.Y, B.Y)
        start_x = min(A.X, B.X)
        end_y = max(A.Y, B.Y)
        end_x = max(A.X, B.X)
        for y in range(start_y, end_y+1):
            for x in range(start_x, end_x+1):
                self.Border.append(Coordinate(x, y))
            

    def __str__(self):
        return f"id: {self.id:8} | a->b: ({str(self.A):14}-> {str(self.B):14}) | area: {self.Area:8}"

    def __repr__(self):
        return f"Rectangle({str(self.A)},{str(self.B)})"
    
    def Debug(self):
        print("****************")
        print(f"Debug Output for Rectangle #{self.id}")
        print(f"A: {str(self.A)}")
        print(f"B: {str(self.B)}")
        print(f"Area: {self.Area}")
        print(f"Border: {str(self.Border)}")
        print("****************")
    
class Polygon:
    def __init__(self, coordinates: list):

        if coordinates is not None and not isinstance(coordinates, list):
            raise Exception(f"parameter coordinates must be None or a list of Coordinate! ({isinstance(coordinates)})")

        self.Coordinates = coordinates if coordinates is not None else []
        self.Outline = []
        self.OutlinePoints = []

    def __str__(self):
        return f"Polygon"
        
    def __repr__(self):
        return f"Polygon()"

    def ComputeOutline(self):
        if self.Coordinates is None:
            raise Exception(f"Coordinates must be a list of Coordinate! ({isinstance(self.Coordinates)})")
        if len(self.Coordinates) < 3: 
            raise Exception(f"Number of Coordinates is too low! ({len(self.Coordinates)}/3)")
        
        opCount = len(self.Coordinates)
        divider = 10
        interval = opCount / divider

        print(f"{opCount} steps")

        for op in range(opCount):

            if opCount > 50 and op > 0 and op % interval == 0:
                print(f"{op}/{opCount} = {(op/opCount)*100:.1f}%")

            a = self.Coordinates.pop(0)
            b = self.Coordinates[0]

            self.Outline.append(Line(a,b))

            startColumn, endColumn = min(a.Column, b.Column), max(a.Column, b.Column)
            startRow, endRow = min(a.Row, b.Row), max(a.Row, b.Row)

            for column in range(startColumn, endColumn+1):
                for row in range(startRow, endRow+1):
                    c = Coordinate(column, row)
                    if not c in self.OutlinePoints:
                        self.OutlinePoints.append(c)

            # coordinates von a zurückspeichern
            self.Coordinates.append(a)

    def Debug(self):
        print("****************")
        print(f"Debug Output for Polygon")
        print(f"len(Coordinates): {len(str(self.Coordinates))}")
        print(f"len(Outline): {len(str(self.Outline))}")
        print(f"Size: {FormatBits(self.__sizeof__() + sys.getsizeof(self.Outline) + sys.getsizeof(self.Coordinates))}")
        print(f"Lines: {str(self.Outline)}")
        print("****************")

    def CoordinateColumnSorter(c:Coordinate):
        return c.Column

    def Includes(self, rect:Rectangle):

        print(f"Testing {str(rect)}")

        # ▓▒█·

        if rect.id == 25:
            pass


        for y in range(12):
            for x in range(12):
                c = Coordinate(x,y)
                pointIsInBorder = c in rect.Border
                pointIsInRectangle = c in self.OutlinePoints
                if pointIsInBorder and pointIsInRectangle:
                    print('█', end='')
                elif pointIsInRectangle:
                    print('▒', end='')
                elif pointIsInBorder:
                    print('▓', end='')
                else:
                    print('·', end='')
            print()

        for borderPoint in rect.Border:
            
            intersections = []
            
            for column in range(0, borderPoint.Column+1):
                c = Coordinate(column, borderPoint.Y)
                if c in self.OutlinePoints:
                    if not c in intersections:
                        intersections.append(c)

            intersections.sort(key=self.CoordinateColumnSorter)

            opcount = len(intersections)

            for op in range(opcount):
                n = intersections.pop(0)
                # combine elelement [n] with [n+1] if they are adjecent
                #TODO hier weitermachen

            if len(intersections) % 2 == 0:
                print(f"({str(borderPoint)}) is OOB ({len(intersections)})")
                return False
        
        print("OK")
        return True
