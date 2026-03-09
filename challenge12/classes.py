class Area:

    exceeds = 0
    fits = 0
    todos = 0

    def __init__(self, width, height, presents):
        self.width = int(width)
        self.height = int(height)
        self.presents = []
        self.space = self.width * self.height
        for present in presents:
            self.presents.append(int(present))

    def __repr__(self):
        return f"{self.width}x{self.height}={self.space}: {str(self.presents)} "
    
    def __str__(self):
        return f"{self.width}x{self.height}={self.space}: {str(self.presents)}"
    
    def fitShapes(self, presents):

        print(f"area: {str(self)}")

        # count space needed
        # if it is too much set to false

        spaceneeded = 0

        for i in range(len(self.presents)):
            spaceneeded += self.presents[i] * presents[i].spaceNeeded

        if spaceneeded > self.space:
            print(f"Shape net space ({spaceneeded}) does not fit area space ({self.space}) any way")
            self.__setattr__("canFitShapes", False)
            Area.exceeds += 1
            return
        
        # see if the shapes fit without packing

        sumshapes = 0
        for present in self.presents:
            sumshapes += present
        sumspaces = (self.width//3) * (self.height//3)
        print(f"sum of shapes: {sumshapes}")
        print(f"available space: {sumspaces}")
        if sumspaces >= sumshapes:
            print("can fit easily")
            self.__setattr__("canFitShapes", True)
            Area.fits += 1
            return

        # TODO find an algorythm to fit the shapes into this area
        Area.todos += 1
        # find smallest possible way to arrange the tiles
        # then check if this solution is euqal or less than the width and height



        #if smallestCombination.Width <= self.width and smallestCombination.Height <= self.height:
            #canfitshapes = True

        print(" TODO ")

        self.__setattr__("canFitShapes", False)


class Shape:

    def __init__(self, num, data):
        self.num = num
        self.data = []
        self.spaceNeeded = 0
        for datum in data:
            self.data.append(datum.rstrip())
        for item in self.data:
            for subitem in item:
                if subitem == "#":
                    self.spaceNeeded += 1

    def __repr__(self):
        return f"{self.num} {str(len(self.data))}x{str(len(self.data[0]))}"
    
    def __str__(self):
        return f"{self.num} {str(len(self.data))}x{str(len(self.data[0]))}"
    
    def getVisual(self):
        s = ""

        for line in self.data:
            s += line
            s += "\n"
        
        return s