from enum import Enum

class Coordinate:

    idCounter = 0    

    def __init__(self, column, row):
        self.column = column
        self.row = row
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
        self.center = Coordinate((start.column + end.column) / 2, (start.row + end.row) / 2)
        self.direction = None
        self.direction = self.determine_direction()

    def determine_direction(self):
        if self.start.column == self.end.column:
            # vertical edge
            if self.start.row < self.end.row:
                # edge goes downwards
                return Direction.DOWN
            else:
                # edge goes upwards
                return Direction.UP
        else:
            # horizontal edge
            if self.start.column < self.end.column:
                # edge goes to the right
                return Direction.RIGHT
            else:
                # edge goes to the left
                return Direction.LEFT

    def __str__(self):
        return f"Edge {self.start.id} -> {self.end.id} : {self.direction}"
    
    def __repr__(self):
        return f"Edge {self.start.id} -> {self.end.id} : {self.direction}"

class Perimeter:
    def __init__(self):
        self.edges = []
        self.coordinates = []
    
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
