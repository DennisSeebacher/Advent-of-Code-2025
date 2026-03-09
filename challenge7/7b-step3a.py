from definitions import *

quantumstatesfilename = './challenge7/quantum.txt'
outputfilename = './challenge7/output.txt'

infile = open(quantumstatesfilename)

print("reading quantum states data...")
quantumpaths = []
for line in infile.readlines():
    quantumpaths = eval(line.strip())

listofquantumpaths = []

def breakapart(list, indent = 0, route = ''):
    global listofquantumpaths

    # 0 is actual element id
    # 1..n are children lists

    #print('>'*indent, list[0],sep='')
    route += str(list[0])
    #print(route)
    indent += 1

    if len(list) > 1:
        for sublist in list[1:]:
            breakapart(sublist, indent, route)
    else:
        listofquantumpaths.append(route)


breakapart(quantumpaths)

with open(outputfilename, "w") as o:
    for path in listofquantumpaths:
        o.write(path)
        o.write("\n")
    o.write(str("\nEs gibt insgesamt " + str(len(listofquantumpaths)) + " Quantenpfade."))

# get a count
print("Es gibt insgesamt", len(listofquantumpaths), "Quantenpfade.")