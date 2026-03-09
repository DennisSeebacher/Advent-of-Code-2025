import itertools

def FormatList(list):
    s = ""
    for item in list:
        s += item
    return s

class Permutation:
    def __init__(self, indicator, instructions):
        self.indicator = indicator
        self.instructions = instructions
        self.instructions.sort()
    
    def __switch(self, indicator, button):
        for instruction in button:
            if indicator[instruction] == '.':
                indicator[instruction] = '#'
            else:
                indicator[instruction] = '.'
        return indicator
    
    def compute(self):
        for instruction in self.instructions:
            self.indicator = self.__switch(self.indicator, instruction)
        self.depth = len(self.instructions)

    def __str__(self):
        return f"{str(self.indicator)} {str(self.instructions)}"
    
    def __repr__(self):
        return self.__str__()

class Machine():
    def __init__(self):
        self.indicatorGoal = None
        self.buttons = []
        self.joltageRequirement = []

    def __isMatch(self, indicator, indicatorGoal):
        if len(indicator) != len(indicatorGoal): 
            return False
        
        for i in range(len(indicator)):
            if indicator[i] != indicatorGoal[i]:
                return False

        return True

    def processPermutations(self):
        print(f"creating permutations for [{FormatList(self.indicatorGoal)}]")
        permutations = []
        startIndicator = []
        for i in range(len(self.indicatorGoal)):
            startIndicator.append('.')

        for i in range(1, len(self.buttons)+1):
            els = [list(x) for x in itertools.combinations(self.buttons, i)]
            
            for element in els:
                permutations.append(Permutation(startIndicator,element))
        
        print(f"{len(permutations)} permutations created")
        print(f"computing permutations")
        for p in permutations:
            p.compute()

        for item in permutations:
            print(str(item))

        print(f"filter permutations")
        valid_permutations = []

        for p in permutations:
            if self.__isMatch(p.indicator, self.indicatorGoal):
                valid_permutations.append(p)

        print(f"sort permutations")
        valid_permutations.sort(key = lambda x : x.depth)

    def getShortestPermutation(self):
        if hasattr(self, "valid_permutations") and len(self.valid_permutations) > 0:
            return self.valid_permutations[0]
        else: 
            return None

    def __str__(self):
        return f"{str(self.indicatorGoal):32} --- {str(self.buttons):96} --- {self.joltageRequirement}"
    
    def __repr__(self):
        return f"{str(self.indicatorGoal):32} --- {str(self.buttons):96} --- {self.joltageRequirement}"