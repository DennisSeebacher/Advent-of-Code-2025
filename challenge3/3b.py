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

        #process maxJoltage
        
        #remove leading small values until a plateu or down is found
       
        start = 0

        for n in range(len(self.bankDefinition)-1):
        
            n0 = int(self.bankDefinition[n+0])
            n1 = int(self.bankDefinition[n+1])

            if n0 == n1:
                #plateu, keep going
                pass
            if n0 < n1:
                #upward, keep going
                pass
            if n0 > n1:
                #downward, stop
                start = n
                #print(n , self.bankDefinition[n:])
                break

        print(self.bankDefinition)
        print(self.bankDefinition[start:])

        self.bankDefinition = self.bankDefinition[start:]

        #build an index for the digits from 9 to 1
        index = [[] for i in range(9)]
        
        #fill by going from 9 to 1 and saving indices
        for i in range(9,0,-1):
            for k in range(len(self.bankDefinition)):
                if int(self.bankDefinition[k]) == i:
                    index[i-1].append(k)

        #print(index)
        
        #from 1 to 9 remove until only x elements are left

        count = 0
        for i in index:
            count += len(i)
        
        #remove from left to right
        while count > 12:
            for i in range(10):
                if len(index[i]) > 0:
                    index[i].pop(0)
                    break
            count = 0
            for i in index:
                count += len(i)

        #print(index)

        #rebuild a string from the index
        count = 0
        for i in index:
            count += len(i)
        string = ""
        while count > 0:
            smallest_index = 999999999
            #search for smallest item from index
            for i in range(9):
                for item in index[i]:
                    if int(item) < smallest_index:
                        smallest_index = int(item)

            for i in range(9):
                if smallest_index in index[i]:
                    index[i].remove(smallest_index)
                    string += str(i+1)
                    break

            count = 0
            for i in index:
                count += len(i)

        print(int(string))
        self.maxJoltage = int(string)

        
banks = []
for line in file.readlines():
    banks.append(Bank(line.strip()))
    
#find the max joltage per bank, handled by class

#sum total joltage
sumJoltage = 0
for bank in banks:
    sumJoltage += bank.maxJoltage

print("Max Joltage is : ", sumJoltage)