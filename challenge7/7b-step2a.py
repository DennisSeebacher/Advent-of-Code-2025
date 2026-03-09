from definitions import *

manifolddefinitionfilename = './challenge7/manifold.txt'
quantumstatesfilename = './challenge7/quantum.txt'

infile = open(manifolddefinitionfilename)

print("reading manifold data...")
objects = []
for line in infile.readlines():
    objects.append(eval(line.strip()))

print("computing quantum states", end='', flush=True)

def getObjectbyId(id):
    for obj in objects:
        if id == obj.id:
            return obj
    return None

def widesearch(start):
    paths = []
    paths.append(start.id
                 )
    for childid in start.children:
        chobj = getObjectbyId(childid)
        if chobj is not None: 
            if isinstance(chobj, Splitter):
                paths.append(widesearch(chobj))
            elif isinstance(chobj, Output):
                paths.append([chobj.id])

    # für jedes child
    # verfolge pfad bis zum output
    # wenn am output, abwickeln und in paths speichern
    #print(".", end='', flush=True)
    return paths

startobj = getObjectbyId(1)
paths = widesearch(startobj)

with open(quantumstatesfilename, "w") as o:
    o.write(repr(paths))

print("done")