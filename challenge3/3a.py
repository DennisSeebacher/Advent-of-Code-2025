from enum import Enum
import os
print(os.getcwd())

file = './challenge3/input'
file = open(file)

class Bank:
    def __init__(self, bankDefinition):
        self.bankDefinition = bankDefinition
        self.maxJoltage = 0
        if len(self.bankDefinition) > 1:
            #find two largest digits from right to left
            #save indices as d1 and d2
            #loop twice
            # first time from i = n-1 to 0
            # second time from i = n to d1
            digits = []
            length = len(bankDefinition)
            candidate = length-2
            d1 = -1
            d2 = -1
            print(self.bankDefinition, end=' ', flush=True)
            #print("Loop 1:", end=' ', flush=True)
            for i in range(length-2, -1, -1):
                if self.bankDefinition[i] >= self.bankDefinition[candidate]:
                    candidate = int(i)
                #print(self.bankDefinition[candidate], end=' ', flush=True)
            d1 = candidate
            #print("Loop 2:", end=' ', flush=True)
            candidate = length-1
            for i in range(length-1, d1, -1):
                if self.bankDefinition[i] >= self.bankDefinition[candidate]:
                    candidate = int(i)
                #print(self.bankDefinition[candidate], end=' ', flush=True)
            d2 = candidate

            #print("|", d1, d2, self.bankDefinition[d1], self.bankDefinition[d2],"|", int(self.bankDefinition[d1])*10+int(self.bankDefinition[d2]))
            print("|", int(self.bankDefinition[d1])*10+int(self.bankDefinition[d2]))
            self.maxJoltage = int(self.bankDefinition[d1])*10+int(self.bankDefinition[d2])

banks = []
for line in file.readlines():
    banks.append(Bank(line.strip()))
    
#find the max joltage per bank, handled by class

#sum total joltage
sumJoltage = 0
for bank in banks:
    sumJoltage += bank.maxJoltage

print("Max Joltage is : ", sumJoltage)