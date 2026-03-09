# ********************
# *     switches     *
# ********************

test = not True

# ********************
# *    variables     *
# ********************

import math
from classes import *

num_of_clusters_to_multiply = 3

if test:
    filename = './challenge8/test.txt'
    connection_target = 10
else:
    filename = './challenge8/input.txt'
    connection_target = 1000

# ********************
# *      sorts       *
# ********************

def circuitSizeSort(circuit):
    return circuit.getSize()

def connectionDistanceSort(connection):
    return connection.distance

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

def readJunctions(filename):

    print(f"reading data from {filename}")

    junctions = []
    file = open(filename)
    for line in file.readlines():
        x,y,z = line.strip().split(',')
        junctions.append(Junctionbox(int(x),int(y),int(z)))

    print(f"read {formatNumber(len(junctions))} entries")
    return junctions

def computeConnections(junctions):

    print("computing connections")

    opcount = len(junctions)
    connections = []

    for j1 in range(len(junctions)):

        if opcount > 100 and j1 > 0 and j1 % 100 == 0:
            print(f"{j1}/{opcount}")

        for j2 in range(j1+1, len(junctions)):
                       
            a = junctions[j1]
            b = junctions[j2]

            dist_a_b = 0
            x = math.pow(a.x-b.x,2)
            y = math.pow(a.y-b.y,2)
            z = math.pow(a.z-b.z,2)
            dist_a_b = x+y+z

            c = Connection(a, b, dist_a_b)

            connections.append(c)
    connections.sort(key=connectionDistanceSort)
    
    print(f"computed {formatNumber(len(connections))} connections")
    return connections

def connectCircuitsUntilAllConnected(connections, junctions):

    print("connecting circuits")

    def findCircuit(junction, circuits):
        for cir in circuits:
            if junction in cir.members:
                return cir
        return None

    circuits = []
    orphans = [] 

    for box in junctions:
        orphans.append(box.id)

    action_count = 0
    connections_count = 0
    while len(orphans) > 0 and len(connections) > 0:
    #while connections_count < connection_target and len(connections) > 0:

        print(f"> action #{action_count}")

        action_count += 1
        con = connections.pop(0)

        #find circuits containing both A and/or B

        cir_a = findCircuit(con.a, circuits)
        cir_b = findCircuit(con.b, circuits)
        
        if cir_a is None and cir_b is None:
            # both a and b are not connected to anything yet
            # create a new circuit containing a and b
            cir = Circuit()
            cir.addMember(con.a)
            cir.addMember(con.b)
            circuits.append(cir)
            connections_count += 1
            print(f">> created circuit {cir.id} with junction {con.a.id} and junction {con.b.id}")
            orphans.remove(con.a.id)
            orphans.remove(con.b.id)
        
        elif cir_a is not None and cir_b is None:
            # a is connected but b is not connected
            # add b to a's circuit
            cir_a.addMember(con.b)
            connections_count += 1
            print(f">> added junction {con.b.id} to circuit {cir_a.id}")
            orphans.remove(con.b.id)
        
        elif cir_a is None and cir_b is not None:
            # a is not connected but b is connected
            # add a to b's circuit
            cir_b.addMember(con.a)
            connections_count += 1
            print(f">> added junction {con.a.id} to circuit {cir_b.id}")
            orphans.remove(con.a.id)
                        
        elif cir_a is not None and cir_b is not None:
            # bot a and b are connected

            if cir_a.id == cir_b.id:
                # a and b are already in the same circuit
                # "do nothing"
                pass
                print(f">> pass")
                print(f">> junction {con.a.id} and {con.b.id} are already in circuit {cir_a.id}")
        
            else:
                # a and b are in different circuits
                # create a new circuit containing all members of ca and cb
                cir = Circuit()
                cir.moveMembersFrom(cir_a)
                cir.moveMembersFrom(cir_b)
                circuits.remove(cir_a)
                circuits.remove(cir_b)
                circuits.append(cir)
                connections_count += 1
                print(f">> combined circuits {cir_a.id} and {cir_b.id}")

        print(f">> {connections_count} connections established")
        print(f">> {len(circuits)} circuits established")
        print()

        if len(orphans) <= 0:
            print()
            print(f">{action_count} actions, {connections_count} connections established")
            print(f">{str(con)}")
            print()
            return con

    return circuits

def computeResult(connection):

    print("computing results")

    xx = connection.a.x * connection.b.x

    print(f">> result of a.x * b.x ({connection.a.x} * {connection.b.x}) of the last connection  = {xx} <<")

# ********************
# *       main       *
# ********************

#read the data and transform into junctions
junctions = readJunctions(filename)

# print(f"showing {formatNumber(len(junctions))} junctions:")
# for i in range(0, len(junctions)):
#     print(f"#{str(junctions[i])}")

#compute the connections for each junction
connections = computeConnections(junctions)

#compute the connection of each junction returning the pair that lead to one singular circuit
lastPair = connectCircuitsUntilAllConnected(connections, junctions)

#compute the result
computeResult(lastPair)