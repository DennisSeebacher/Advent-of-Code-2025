# ********************
# *     switches     *
# ********************

test = True

# ********************
# *    variables     *
# ********************

import math
from classes import *

if test:
    filename = './challenge10/test.txt'
else:
    filename = './challenge10/input.txt'

# ********************
# *      sorts       *
# ********************

# ********************
#      functions     *
# ********************

def formatNumber(number):
    if number == 1: return "one"
    if number == 2: return "two"
    if number == 3: return "three"
    if number == 4: return "four"
    if number == 5: return "five"
    if number == 6: return "six"
    if number == 7: return "seven"
    if number == 8: return "eight"
    if number == 9: return "nine"
    return str(number)

def readMachineData(filename):

    print(f"reading machine data from {filename}")

    machines = []
    file = open(filename)
    for line in file.readlines():
        m = Machine()

        parts = line.split()

        for part in parts:
            if part.startswith("["):
                m.indicatorGoal = list(part.replace("[","").replace("]",""))

            if part.startswith("("):
                m.buttons.append(part.replace("(","").replace(")","").split(","))
                for i in range(len(m.buttons)):
                    for k in range(len(m.buttons[i])):
                        m.buttons[i][k] = int(m.buttons[i][k])

            if part.startswith("{"):
                m.joltageRequirement = part.replace("{","").replace("}","").split(",")

        machines.append(m)
        
    print(f"read {formatNumber(len(machines))} machines")
    return machines

def computeCombinations(machines):

    print("computing combinations")

    for i in range(len(machines)):

        if len(machines) > 100 and i > 0 and i % 10 == 0:
              print(f"{i}/{len(machines)}")

        machines[i].processPermutations()

def computeResult(machines):

    print("computing results")

    sum = 0

    for machine in machines:
        if machine.getShortestPermutation() is not None:
            sum += machine.getShortestPermutation()
        else: 
            print(f"X -> {str(machine)}")

    print(f">> to configure all machines you need to do {formatNumber(sum)} button presses <<")

# ********************
# *       main       *
# ********************

#read the data
machines = readMachineData(filename)

print(f"showing {formatNumber(len(machines))} machines:")
for i in range(0, len(machines)):
    print(f"  {str(machines[i])}")

#compute the combinations for each machine
computeCombinations(machines)

#compute the result
computeResult(machines)