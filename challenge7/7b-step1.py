from definitions import *

infilename = './challenge7/test.txt'
manifolddefinitionfilename = './challenge7/manifold.txt'
infile = open(infilename)

print("reading manifold data...")
manifold_data = []
for line in infile.readlines():
    manifold_data.append(list(line))

# *** build quantum tachyon manifold data structure ***
# from top to bottom
# left to right
# look for splitters and emitters
# give each object an id

print("building quantum tachyon manifold data structure...")

objectIndex = 0
objects = []
for line in range(len(manifold_data)):
    for index in range(len(manifold_data[0])):
        if manifold_data[line][index] == SPLITTER:
            objects.append(Splitter(objectIndex, line, index))
            objectIndex += 1
        if manifold_data[line][index] == EMITTER:
            objects.append(Emitter(objectIndex, line, index))
            objectIndex += 1

# *** connect items ***
# begin again from bottom right
# take next splitter

# Looking Directions
#   7 0 1
#    \|/
#   6-x-2
#    /|\
#   5 4 3
def lookforitems(item, direction, firstoccurenceonly = False):
    global objects

    retVal = None

    row_start = item.row + 1
    row_end = len(manifold_data)+1
    col = item.column

    match direction:
        case 0: pass
        case 4: pass

        case 1: col += 1
        case 3: col += 1

        case 5: col -= 1
        case 7: col -= 1

    for row in range(row_start, row_end):
        for obj in objects:
            if isinstance(obj, Output):
                continue
            if obj.row == row and obj.column == col:
                if retVal is None:
                    retVal = []
                retVal.append(obj)

    if firstoccurenceonly and retVal is not None and len(retVal) > 0:
        return retVal[0]
    else:
        return retVal

def findoutput(col):
    for i in objects:
        if isinstance(i, Output):
            if i.column == col:
                return i
    return None

for item in objects:

    itembelow = None
    itembelowleft = None
    itembelowright = None

    if isinstance(item, Emitter):

        itembelow = lookforitems(item, LOOK_DOWN, True)
        item.children.append(itembelow.id)
        itembelow.powered = True

    if isinstance(item, Splitter) and item.powered:

        itembelowleft = lookforitems(item, LOOK_DOWN_LEFT, True)
        itembelowright = lookforitems(item, LOOK_DOWN_RIGHT, True)

        if itembelowleft is None:
            x = findoutput(item.column - 1)
            if x is None:
                objects.append(Output(objectIndex, item.column-1))
                item.children.append(objectIndex)
                objectIndex += 1
            else:
                item.children.append(x.id)

        else:
            item.children.append(itembelowleft.id)
            itembelowleft.powered = True

        if itembelowright is None:
            x = findoutput(item.column + 1)
            if x is None:
                objects.append(Output(objectIndex, item.column+1))
                item.children.append(objectIndex)
                objectIndex += 1
            else:
                item.children.append(x.id)
        else:
            item.children.append(itembelowright.id)
            itembelowright.powered = True

print("removing orphaned objects...")
to_remove = [item for item in objects if getattr(item, "powered", True) is False]
for item in to_remove:
    print(item.id, end=' ', flush=True)
    manifold_data[item.row][item.column] = "."
    objects.remove(item)
print()

print("writing manifold data...")

with open(manifolddefinitionfilename, "w") as o:
    for item in objects:
        o.write(repr(item))
        o.write("\n")

print("done")