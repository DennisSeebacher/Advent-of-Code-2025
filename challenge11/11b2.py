# ********************
# *     switches     *
# ********************

test = not True

# ********************
# *    variables     *
# ********************

import time
from classes import *

if test:
    filename = './challenge11/test3.txt'
else:
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

def findValidPaths(devices):

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

    print(str(svr))
    print(str(dac))
    print(str(fft))
    print(str(out))

    countAttribute = "count"
    setattr(svr, countAttribute, 1)

    circuit = []
    queue = [svr]

    while len(queue) > 0:
        obj = queue.pop(0)
    
        if obj not in circuit:
            if obj == svr:
                print(f">>>>>>> {obj.name} svr")
            elif obj == dac:
                print(f">>>>>>> {obj.name} dac")
            elif obj == fft:
                print(f">>>>>>> {obj.name} fft")
            elif obj == out: 
                print(f">>>>>>> {obj.name} out")
            else:
                #print(f"process {obj.name}")
                pass
            circuit.append(obj)
            for output in obj.outputs:

                if hasattr(output, countAttribute):
                    output.count += obj.count
                    #print(f"+ {obj.count} to {output.name} => {output.count}")
                else:
                    setattr(output, countAttribute, obj.count)
                    #print(f"-> {obj.count} to {output.name}")

                queue.append(output)
            if len(obj.outputs) == 0 and obj is not out:
                print(f"! No outs for {obj.name}")

def computeResult(devices):
    out = None
    for device in devices:
        if device.name == 'out':
            out = device
            break

    print(f"In total, there are {formatNumber(out.count)} different paths via 'svr'->'dac'->'fft'->'out'.")

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
findValidPaths(devices)

#compute the result
computeResult(devices)