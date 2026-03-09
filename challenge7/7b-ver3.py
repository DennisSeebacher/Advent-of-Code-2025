outfilename = './challenge7/output-x.txt'
infilename = './challenge7/test.txt'
infile = open(infilename)

print("reading manifold data...")
manifold_data = []
for row in infile.readlines():
    manifold_data.append(list(row.strip()))

print("processing...")
EMITTER = "S"
EMPTY = "."
SPLITTER = "^"
BEAM = "|"

for row in range(len(manifold_data)):

    print(str(row).rjust(3), end='[', flush= True)

    processed = manifold_data[row]

    for col in range(len(processed)):
        if processed[col] == EMITTER:
            processed[col] = str(1)

        if row > 0:
            up = manifold_data[row-1][col]
            this = manifold_data[row][col]

            if up.isdigit() and this == EMPTY:
                manifold_data[row][col] = str(manifold_data[row-1][col])

            if up.isdigit() and this == SPLITTER:
                actual_value_left = manifold_data[row][col-1]
                actual_value_right = manifold_data[row][col+1]
                
                if actual_value_left.isdigit():
                    manifold_data[row][col-1] = str(int(actual_value_left) + int(manifold_data[row-1][col]))
                else:
                    manifold_data[row][col-1] = str(manifold_data[row-1][col])

                if actual_value_right.isdigit():
                    manifold_data[row][col+1] = str(int(actual_value_left) + int(manifold_data[row-1][col]))
                else:
                    manifold_data[row][col+1] = str(manifold_data[row-1][col])

        print(processed[col], end='', flush=True)
    
    print(']')
    
sum_last_line = 0

for item in manifold_data[-1]:
    if item.isdigit():
        sum_last_line += int(item)

print("writing...")
with open(outfilename, "w") as o:
    for row in manifold_data:
        o.write(''.join(row))
    o.write("\n\n")
    o.write(str(sum_last_line))

print(str(sum_last_line))