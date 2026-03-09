from enum import Enum

file = './challenge5/input'
file = open(file)

# The Elves are trying to determine which of the available ingredient IDs are fresh.
# The database operates on ingredient IDs. 
# It consists of a list of fresh ingredient ID ranges, a blank line, and a list of available ingredient IDs. 
# How many of the available ingredient IDs are fresh?

fresh_ids = []
fresh_ids_count = 0
ids = []

class idRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def test(self, value):
        v = int(value.strip())
        if (self.start <= v) and (v <= self.end):
            print(value)
            return True
        else:
            return False
        
    def count(self):
        return self.end + 1 - self.start
                
    def __str__(self):
        return "["+str(self.start)+"/"+str(self.end)+'->'+str(self.count())+"]"
    
    def __repr__(self):
        return "["+str(self.start)+"/"+str(self.end)+'->'+str(self.count())+"]"
    
print('reading ids')
for line in file.readlines():
    if line.strip() == '':
        break

    start, end = line.strip().split('-')
    fresh_ids.append(idRange(int(start), int(end.strip())))

print('ordering')
def sortfunction(e):
    return e.start

fresh_ids.sort(key=sortfunction)

for id in fresh_ids:
    print(id)

print('collapsing')
print('--------')
#print(fresh_ids)
keepCollapsing = True
while keepCollapsing:
    keepCollapsing = False
    items = []
    temp = []
    collapsed = 0
    merged = 0

    while len(fresh_ids) > 0:

        if len(fresh_ids) > 0:
            while len(items) < 2 and len(fresh_ids) > 0:
                items.append(fresh_ids.pop(0))
        else:
            while len(items) > 0:
                temp.append(items.pop(0))
            break

        if len(items) == 2:

            if items[0].start == items[1].start and items[0].end == items[1].end:
                temp.append(idRange(items[0].start, items[1].end))
                #print('merge', items[0], 'with', items[1], '->', temp[-1])
                keepCollapsing = True
                items.pop(0)
                items.pop(0)
                merged+=1

            elif items[0].end >= items[1].start:
                temp.append(idRange(min(items[0].start, items[1].start), max(items[0].end, items[1].end)))
                #print('cllps', items[0], 'with', items[1], '->', temp[-1])
                keepCollapsing = True
                items.pop(0)
                items.pop(0)
                collapsed+=1

            else:
                temp.append(items.pop(0))

        elif len(items) == 1:
            temp.append(items.pop())

    if len(items) > 0:
            temp.append(items.pop(0))
    print("M:",merged, " C:", collapsed, "T:", len(temp))
    
    if keepCollapsing:
        fresh_ids = temp
    else:
        fresh_ids = temp
        break

print('--------')

for id in fresh_ids:
    print(id)

print('summieren')

sum = 0
for id in fresh_ids:
    sum += id.count()

print("Es sind", sum, "frische Produkte vorhanden.")