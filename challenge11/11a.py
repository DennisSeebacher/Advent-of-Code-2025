# ********************
# *     switches     *
# ********************

test = False

# ********************
# *    variables     *
# ********************

from classes import *

if test:
    filename = './challenge11/test.txt'
else:
    filename = './challenge11/input.txt'

# ********************
# *      sorts       *
# ********************

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
    list = []
    data = open(filename, "r")

    for line in data:
        parts = line.split(':')
        name = parts[0].strip()
        outputs = parts[1].split()

        list.append(Device(name,outputs))
    
    return list

def findPaths(devices):
    list = []

    def traverse(devicename, log):

        d = None
        for device in devices:
            if device.name == devicename:
                d = device
                break
        
        if d is None:
            return

        log.append(devicename)
        
        for output in device.outputs:

            if output == 'out':
                log.append('out')
                list.append(log.copy())
                #print(f">{str(log)}")
            else:
                traverse(output, log.copy())

    you = None

    for device in devices:
        if device.name == 'you':
            you = device
            break
        
    log = []
    log.append(device.name)

    for output in device.outputs:
        traverse(output, log.copy())

    # find device with the name 'you'
    # traverse each output until none left
    # if 'out' was found, save to list

    return list

def computeResult(paths):
    print(f"In total, there are {formatNumber(len(paths))} different paths leading from 'you' to 'out'.")

# ********************
# *       main       *
# ********************

#read the data
devices = readDeviceData(filename)

#print(f"showing {formatNumber(len(devices))} devices:")
# for i in range(0, len(devices)):
#     print(f"  {str(devices[i])}")

#find all paths from 'you' to 'out'
paths = findPaths(devices)

#compute the result
computeResult(paths)