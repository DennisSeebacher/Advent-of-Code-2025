# ********************
# *    variables     *
# ********************

from classes import *

filename = './challenge11/input.txt'

# ********************
#      functions     *
# ********************

def formatNumber(number):
    if number == 1: return "one"
    if number == 2: return "two"
    if number == 3: return "three"
    if number == 4: return "four"
    if number == 5: return "five"
    if number == 6: return "six"
    if number == 7: return "seven"
    if number == 8: return "eight"
    if number == 9: return "nine"
    return str(number)

def readDeviceData(filename):

    print("reading device data")

    list = []
    data = open(filename, "r")

    for line in data:
        parts = line.split(':')
        name = parts[0].strip()
        outputs = parts[1].split()
        list.append(Device(name,outputs))
    
    return list

def findLooseEnds(devices):
    list = []
    for device in devices:
        if device.name == 'out':
            continue
        if device.outputs is None:
            list.append(device)
        if len(device.outputs) == 0:
            list.append(device)
    return list

def findLooseStarts(devices):
    list = []
    for device in devices:
        if device.name == 'svr':
            continue
        temp = []
        for dev2 in devices:
            if device in dev2.outputs:
                temp.append(dev2)
        if len(temp) == 0:
            list.append(device)
    return list

def findIsland(devices):
    circuit = []

    svr = None
    dac = None
    fft = None
    out = None

    flag = 0

    for device in devices:
        if flag >= 4:
            break
        if device.name == 'svr':
            svr = device
            flag += 1
            continue
        if device.name == 'dac':
            dac = device
            flag += 1
            continue
        if device.name == 'fft':
            fft = device
            flag += 1
            continue
        if device.name == 'out':
            out = device
            flag += 1
            continue
        
    queue = [svr]

    while len(queue) > 0:
        obj = queue.pop(0)

        if obj not in circuit:
            circuit.append(obj)
            for out in obj.outputs:
                queue.append(out)

    return circuit

def computeResultEnds(looseEnds):
    print(f"In total, there are {formatNumber(len(looseEnds))} loose ends.")

def computeResultStarts(looseStarts):
    print(f"In total, there are {formatNumber(len(looseStarts))} loose starts.")

def computeResultIslands(islands):
    print(f"In total, there are {formatNumber(len(islands))} devices in the svr circuit.")

# ********************
# *       main       *
# ********************

#read the data
devices = readDeviceData(filename)

devices.append(Device("out", []))
for device in devices:
    outs = []
    for output in device.outputs:
        dev = None
        for device2 in devices:
            if device2.name == output:
                dev = device2
                
        if dev is None:
            print(f"{output} not found!")
        else:
            outs.append(dev)
    device.outputs = outs

#find all paths from 'you' to 'out'
looseEnds = findLooseEnds(devices)
looseStarts = findLooseStarts(devices)
islands = findIsland(devices)

#compute the result
computeResultStarts(looseStarts)
computeResultEnds(looseEnds)
computeResultIslands(islands)

for island in islands:
    print(str(island))