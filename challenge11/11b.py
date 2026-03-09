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

    print("finding valid paths - step 1 - prep variables")

    # variants
    # svr - fft - dac - out
    # svr - dac - fft - out <<<---

    svr2dac = []
    dac2fft = []
    fft2out = []

    def traverse(outputobj, log, target, list):
        log.append(outputobj)
        
        if outputobj == target:
            list.append(log.copy())
            return

        for output in outputobj.outputs:
            traverse(output, log.copy(), target, list)

    def traverseStart(start, end, list):
        log = []
        log.append(start)
        for output in start.outputs:
            traverse(output, log.copy(), end, list)

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
        
    print("  " + str(svr))
    print("  " + str(dac))
    print("  " + str(fft))
    print("  " + str(out))

    time.sleep(2)

    print("finding valid paths - step 2a - find svr->dac")
    traverseStart(svr, fft, svr2dac)
    print(f"found {len(svr2dac)} paths")

    time.sleep(2)

    print("finding valid paths - step 2b - find dac->fft")
    traverseStart(fft, dac, dac2fft)
    print(f"found {len(dac2fft)} paths")

    time.sleep(2)

    print("finding valid paths - step 2c - find fft->out")
    traverseStart(dac, out, fft2out)
    print(f"found {len(fft2out)} paths")

    print(f"svr -> dac {len(svr2dac)}")
    print(f"dac -> fft {len(dac2fft)}")
    print(f"fft -> out {len(fft2out)}")

    return [svr2dac, dac2fft, fft2out]

def computeResult(paths):
    length = len(paths[0])
    length *= len(paths[1])
    length *= len(paths[2])
    print(f"In total, there are {len(paths[0])}{len(paths[1])}{len(paths[2])} = {formatNumber(length)} different paths via 'svr'->'dac'->'fft'->'out'.")

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
validpaths = findValidPaths(devices)

#compute the result
computeResult(validpaths)