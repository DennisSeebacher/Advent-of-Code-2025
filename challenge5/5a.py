from enum import Enum

file = './challenge5/input'
file = open(file)

# The Elves are trying to determine which of the available ingredient IDs are fresh.
# The database operates on ingredient IDs. 
# It consists of a list of fresh ingredient ID ranges, a blank line, and a list of available ingredient IDs. 
# How many of the available ingredient IDs are fresh?

fresh_ids = []
inventory = []
fresh_ids_count = 0
mode = 0

class idRange:
    def __init__(self, start, end):
        self.start = int(start.strip())
        self.end = int(end.strip())
    
    def test(self, value):
        v = int(value.strip())
        if (self.start <= v) and (v <= self.end):
            print(value)
            return True
        else:
            return False
        
    def __str__(self):
        return "["+str(self.start)+"/"+str(self.end)+"]"
    
    def __repr__(self):
        return "["+str(self.start)+"/"+str(self.end)+"]"
          

print('reading ids')
for line in file.readlines():
    if line.strip() == '':
        mode = 1 
        print('reading inventory')
        continue

    if mode == 0:
        start, end = line.strip().split('-')
        fresh_ids.append(idRange(start, end))

    if mode == 1:
        inventory.append(line.strip())

print('processing',)

for item in inventory:
    for f in fresh_ids:
        if f.test(item):
            fresh_ids_count += 1
            break

print("Es sind", fresh_ids_count, "frische Produkte vorhanden.")