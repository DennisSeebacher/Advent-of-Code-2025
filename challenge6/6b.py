file = './challenge6/input'
file = open(file)

# help with math homework
# find the grad total

grand_total = 0
tasks = []

class Problem:
    def __init__(self):
        self.parts = []

    def total(self):
        sum = 0
        if self.parts[-1] == '*':
            sum += 1

        if self.parts[-1] == '+':
            for i in self.parts[0:-1]:
                sum += int(i)
        else:
            for i in self.parts[0:-1]:
                sum *= int(i)

        print(self.parts, '=>', sum)

        return sum

    def __str__(self):
        return 'P[' + self.parts + ']'
    
    def __repr__(self):
        return 'P[' + self.parts + ']'

class Task:
    def __init__(self):
        self.lines = []

    def splitTaskIntoProblems(self):
        problems = []
        p = Problem()
        linelength = len(self.lines[0])
        rows = len(self.lines)
        # todo read items from right to left until index = 0
        for column in range(linelength)[::-1]:
            digit = ""
            operator = ""
            for row in range(rows):
                char = self.lines[row][column]
                if char in "*+":
                    operator = char
                else:
                    digit += char
            
            if digit.strip() is not "":
                p.parts.append(digit)
            if operator is not "":
                p.parts.append(operator)
                problems.append(p)
                p = Problem()
        
        return problems

    def total(self):
        sum = 0

        self.problems = self.splitTaskIntoProblems()
       
        for problem in self.problems:
            sum += problem.total()

        return sum
    
print("reading tasks")

t = Task()
for line in file.readlines():
    if line.strip() == '':
        tasks.append(t)
        t = Task()
    else:
        t.lines.append(line.replace("\n", ""))
tasks.append(t)

print("processing")

for task in tasks:
    grand_total += task.total()

print("Die Gesamtlösungsmenge der", str(len(tasks)) ,"Aufgaben ist", grand_total)
