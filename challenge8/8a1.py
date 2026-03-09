# does take an eternity
#8a2 fixes the time to compute the distances by writing them into each junction

import math

# file = './challenge8/test.txt'
# connect_count = 10
# take_from_clusters = 3

file = './challenge8/input.txt'
connect_count = 1000
take_from_clusters = 3

file = open(file)

print("reading data")

junctions = []

class Junctionbox:

    __idcounter = 0

    def __init__(self,x,y,z, id = None):
        if id is None:
            self.Id = Junctionbox.__idcounter
            Junctionbox.__idcounter += 1
        else:
            self.Id = id
        self.X = x
        self.Y = y
        self.Z = z
        self.distances = []
        self.connections = []
        self.ClusterId = None

    def listConnections(self):
        s = ""
        for link in self.connections:
            s += str(link.Id) + ","
        return s

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return f"Junctionbox #{self.Id}, {self.X}/{self.Y}/{self.Z}, {str(self.ClusterId)}, [{self.listConnections()[:-1]}]"

for line in file.readlines():
    x,y,z = line.strip().split(',')
    junctions.append(Junctionbox(int(x),int(y),int(z)))

print("processing distances")

class DistanceAB:

    def __init__(self, id_a, id_b, dist):

        if id_a < id_b:
            self.IdA = id_a
            self.IdB = id_b
        else:
            self.IdA = id_b
            self.IdB = id_a
        self.Distance = dist

    def __str__(self):
        return f"DistanceAB({str(self.IdA).rjust(3)},{str(self.IdB).rjust(3)},{str(self.Distance).rjust(24)})"

distances = []

sum_junctions = len(junctions)
for i in range(sum_junctions):

    if i > 0 and i % 5  == 0: 
        print(f"{str((i/sum_junctions)*100)}%")

    for k in range(sum_junctions):

        if i == k:
            #ignore self connection
            continue

        A = junctions[i]
        B = junctions[k]

        # ignore if this combinations exists already

        skip = False

        for combination in distances: #this is the shit that slow everything down
            if combination.IdA == A.Id and combination.IdB == B.Id:
                skip = True
            if combination.IdA == B.Id and combination.IdB == A.Id:
                skip = True

        if skip:
            continue

        x = math.pow(A.X-B.X,2)
        y = math.pow(A.Y-B.Y,2)
        z = math.pow(A.Z-B.Z,2)
        distAB = math.sqrt(x+y+z)
    
        distances.append(DistanceAB(junctions[i].Id, junctions[k].Id, distAB))

def distSorter(d):
    return d.Distance

distances.sort(key = distSorter)

print()
for link in distances:
    print(str(link))
print()

print(f"connecting junctions")

counter = 0

def finditeminlist(list, id):
    for item in list:
        if item.Id == id:
            return item
    return None

while counter < connect_count:
    item = distances.pop(0)
    
    itema = finditeminlist(junctions, item.IdA)
    itemb = finditeminlist(junctions, item.IdB)

    itema.connections.append(itemb)
    itemb.connections.append(itema)

    counter += 1

print("searching clusters")

class Cluster:
    def __init__(self, id, amount, startitem):
        self.Id = id
        self.Amount = amount
        self.StartItem = startitem

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Cluster({self.Id},{self.Amount})"

clusters = []

#sortiere die junctions in cluster ein
#gib jeder junction und allen daran hängenden die gleiche nummer
#speichere die clusternummer und anzahl junctions in clusters
#erhöhe die nummer um 1
#nimm die nächste junction ohne cluster nummer und wiederhole

def updateConnectedJunctions(junct, id):
    for cj in junct.connections:
        if cj.ClusterId is None:
            cj.ClusterId = id
            updateConnectedJunctions(cj, id)


cluster_id = 0
for junction in junctions:

    if junction.ClusterId is None:
        junction.ClusterId = cluster_id
        updateConnectedJunctions(junction, cluster_id)
        cluster_id += 1
    else:
        pass

for junction in junctions:
    foundCluster = False
    for cluster in clusters:
        if cluster.Id == junction.ClusterId:
            cluster.Amount += 1
            foundCluster = True
            break
    if not foundCluster:
        clusters.append(Cluster(junction.ClusterId, 1, junction.Id))
    
def clusterSort(n):
    return n.Amount

clusters.sort(key = clusterSort, reverse=True)

print()
for item in junctions:
    print(str(item))
print()
for cluster in clusters: 
    print(cluster)
print()

print(f"compiling result")
length = 1

for i in range(take_from_clusters):
    length *= clusters[i].Amount

print(f"Die benötigte Kabellänge ist {str(length)} !")