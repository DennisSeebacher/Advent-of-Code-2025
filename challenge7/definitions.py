EMITTER = "S"
EMPTY = "."
SPLITTER = "^"
BEAM = "|"
LEFT = 0
RIGHT = 1
LOOK_UP_LEFT = 7
LOOK_UP = 0
LOOK_UP_RIGHT = 1
LOOK_DOWN_LEFT = 5
LOOK_DOWN = 4
LOOK_DOWN_RIGHT = 3

class Splitter:
    def __init__(self, id, row, column, children = None, powered = False):
        self.children = [] if children is None else children
        self.id = id
        self.row = row
        self.column = column
        self.path = None
        self.powered = powered
        self.path_count = 0

    def __repr__(self):
        return f"Splitter({self.id}, {self.row}, {self.column}, {self.children}, {self.powered})"
    
    def __str__(self):
        return 'Splitter { id:' + str(self.id) + ', coords: ' + str(self.row) + '/' + str(self.column) + ', children: '+ ','.join(map(str, self.children)) + ' }' 

class Emitter:
    def __init__(self, id, row, column, children = None):
        self.children = [] if children is None else children
        self.id = id
        self.row = row
        self.column = column
        self.path_count = 0

    def __repr__(self):
        return f"Emitter({self.id}, {self.row}, {self.column}, {self.children})"
    
    def __str__(self):
        return 'Emitter { id:' + str(self.id) + ', coords: ' + str(self.row) + '/' + str(self.column) + ', children: '+ ','.join(map(str, self.children)) + ' }' 

class Output:
    def __init__(self, id, column):
        self.id = id
        self.column = column
        self.path = None
        self.path_count = 0

    def __repr__(self):
        return f"Output({self.id}, {self.column})"
    
    def __str__(self):
        return 'Output { id:' + str(self.id) + ', coords: ' + str(self.column) + ' }' 