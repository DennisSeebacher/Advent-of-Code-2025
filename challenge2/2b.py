from enum import Enum
import os
print(os.getcwd())

file = './challenge2/input'
file = open(file)
content = file.read()

ranges = content.split(',')

sum = 0

for _range in ranges:
    start, end = int(_range.split('-')[0]),int(_range.split('-')[1])

    for id in range(start, end+1):
        x = str(id)
        y = len(x)
        
        #find repetitions

        for rep in range(1,y):
            #chop string
            chops = [x[n:n+rep] for n in range(0, len(x), rep)]
            #test if all chops are equal length

            if len(chops[0]) == len(chops[-1]):
                #print(chops)
                pass
            else:
                continue
            
            same = True
            same_count = 0

            #check sameness
            for w in range(1, len(chops)):
                if chops[w] == chops[0]:
                    same_count += 1
                else:
                    same = False
            if same:
                print(x, same, same_count, chops)
                sum += id
                break


print(sum)