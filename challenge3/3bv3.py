#solved via tip from reddit :/

from enum import Enum
import os
print(os.getcwd())

file = './challenge3/input'
file = open(file)

def indicesToDigits(indices, source):
    retVal = ""
    for index in indices:
        retVal += str(source[index])
    return retVal

class Bank:
    def __init__(self, bankDefinition):
        self.bankDefinition = bankDefinition
        self.maxJoltage = 0
        self.maxJoltageBatteryCount = 12
        
        #process maxJoltage
        #start by collecting the last 12 indices
        indices = []
        for n in range(len(self.bankDefinition)-self.maxJoltageBatteryCount+1,len(self.bankDefinition)+1):
            indices.append(n-1)

        #print(self.bankDefinition)
        #print('  ',indicesToDigits(indices, self.bankDefinition))

        #beginning with the first index
        #take the index 
        for index_num in range(len(indices)):
            index = indices[index_num]
            resultingIndex = index
            value = self.bankDefinition[index]
            #print(value, end=' : ', flush=True)
            iValue = -1
            #move it left to the biggest value not used by another index
            for i in range(index)[::-1]:
                iValue = self.bankDefinition[i]
                if i >= index:
                    #print('x', end='', flush=True)
                    iValue = self.bankDefinition[i+1]
                    break
                elif index_num >= 1 and i <= indices[index_num-1]:
                    #print('x', end='', flush=True)
                    iValue = self.bankDefinition[i+1]
                    break
                elif iValue >= value:
                    #print('u', end='', flush=True)
                    resultingIndex = i
                    value = self.bankDefinition[resultingIndex]
                else:
                    #print('<', end='', flush=True)
                    pass
            #print(' ',iValue, sep='', end='', flush=True)
            
            #print(' :' , index, "=>", resultingIndex)
            indices[index_num] = resultingIndex

        self.maxJoltage = int(indicesToDigits(indices, self.bankDefinition))
        #print(self.maxJoltage)

        #print("-----------------")
        
banks = []
for line in file.readlines():
    banks.append(Bank(line.strip()))
    
#find the max joltage per bank, handled by class

#sum total joltage
print('Summiere:')
sumJoltage = 0
for bank in banks:
    print(bank.maxJoltage)
    sumJoltage += bank.maxJoltage

print("Max Joltage is : ", sumJoltage)