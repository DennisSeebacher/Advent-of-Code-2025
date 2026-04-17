
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
        self.width = abs(self.coordinateA.column - self.coordinateB.column)
        self.height = abs(self.coordinateA.row - self.coordinateB.row)
        self.Area = self.width * self.height
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
    
    def TestIntersect(self, other: Rectangle):
        
        # self und other keine interaktion
        if self.coordinateB.x < other.coordinateA.x:
            return False
        
        if self.coordinateA.x > other.coordinateB.x:
            return False
        
        if self.coordinateA.y > other.coordinateB.y:
            return False
        
        if self.coordinateB.y < other.coordinateA.y:
            return False
        
        # self und other berühren
        if self.coordinateB.y == other.coordinateA.y:
            return False
        
        if self.coordinateA.y == other.coordinateB.y:
            return False
        
        if self.coordinateA.x == other.coordinateB.x:
            return False
        
        if self.coordinateB.x == other.coordinateA.x:
            return False

        # self und other überschneiden
        return True
