outfilename = './challenge7/output-c.txt'
infilename = './challenge7/test.txt'
infile = open(infilename)

# Analyze your manifold diagram. How many times will the beam be split?
# start at S
# | move downward
# ^ splits a |

# count all occurences of | over a ^

print("reading manifold data...")
manifold_data = []
for line in infile.readlines():
    manifold_data.append(list(line))

print("processing...")
EMITTER = "S"
EMPTY = "."
SPLITTER = "^"
BEAM = "|"
rayIndices = []
splits = 0
for line in manifold_data:
    new_rayIndices = []
    for index in range(len(line)):
        if line[index] == EMITTER:
            new_rayIndices.append(index)
        if index in rayIndices:
            if line[index] == EMPTY:
                line[index] = BEAM
                new_rayIndices.append(index)
            elif line[index] == SPLITTER:
                splits += 1
                if line[index-1] == EMPTY:
                    line[index-1] = BEAM
                    new_rayIndices.append(index-1)
                if line[index+1] == EMPTY:
                    line[index+1] = BEAM
                    new_rayIndices.append(index+1)
    rayIndices = new_rayIndices



print("writing...")
with open(outfilename, "w") as o:
    for line in manifold_data:
        o.write(''.join(line))