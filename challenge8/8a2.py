import math

# *****************************************************************************
# variables
# *****************************************************************************

prune_distances_count = 300
#only save the max 200 shortest connections

filename = './challenge8/test.txt'
filename = './challenge8/input.txt'
connect_count = 20
connect_count = 1000
take_from_clusters = 3

# *****************************************************************************
# classes
# *****************************************************************************

class Connection:

    def __init__(self, TargetId, dist):
        self.Id = TargetId
        self.Distance = dist

    def __str__(self):
        return f"Connection({str(self.Id).rjust(3)} = {str(self.Distance).rjust(24)})"

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
        self.Distances = []
        self.Connections = []
        self.ClusterId = None

    def listConnections(self):
        s = ""
        for link in self.Connections:
            if isinstance(link, Junctionbox):
                s += "#" + str(link.Id) + ","
            else:
                s += str(link) + ","
        return s

    def getShortestDistance(self):
        if len(self.Distances) > 0:
            return self.Distances[0]
        return None
    
    def __distSorter(d):
        return d.Distance

    def sort_and_prune(self):
        global prune_distances_count
        self.Distances.sort(key = Junctionbox.__distSorter)
        if len(self.Distances) > prune_distances_count:
            self.Distances = self.Distances[0:prune_distances_count]

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return f"Junctionbox #{self.Id}, {self.X}/{self.Y}/{self.Z}, {str(self.ClusterId)}, [{self.listConnections()[:-1]}]"

# *****************************************************************************
# functions
# *****************************************************************************

def readData(filename):
    print(f"reading data from {filename}")
    junctions = []
    file = open(filename)
    for line in file.readlines():
        x,y,z = line.strip().split(',')
        junctions.append(Junctionbox(int(x),int(y),int(z)))

    return junctions

def distSort(d):
    return d.Distance

def processJunctionboxValues(junctions):
    print("processing distances")

    sum_junctions = len(junctions)

    for i in range(sum_junctions):

        if i > 0 and i % 10  == 0: 
            print(f"{str((i/sum_junctions)*100)}%")

        for k in range(i+1, sum_junctions):
            A = junctions[i]
            B = junctions[k]

            x = math.pow(A.X-B.X,2)
            y = math.pow(A.Y-B.Y,2)
            z = math.pow(A.Z-B.Z,2)
            distAB = x+y+z
        
            A.Distances.append(Connection(junctions[k].Id, distAB))

        junctions[i].Distances.sort(key = distSort)

    junctions.sort(key = junctionDistanceSort)

# *****************************************************************************
# void
# *****************************************************************************

def junctionDistanceSort(j):
    x = j.getLongestDistance()
    if x is None:
        return -1
    else:
        return x.Distance

# *****************************************************************************
# main
# *****************************************************************************



print("connecting junctions")

counter = 0

for counter in range(connect_count):

    A = junctions.pop(0)
    B = A.Distances.pop(0)

    A.Connections.append(B.Id)

    # take the junction with the lowest distance. pop(0) its distance
    # connect the two items

    print(f"{counter}/{connect_count} - Connect {A.Id} with {B.Id}")

    junctions.append(A)

    for junction in junctions:
        junction.sort_and_prune()
    junctions.sort(key = junctionDistanceSort)

def junctionIdSort(j):
    return j.Id

junctions.sort(key= junctionIdSort)

print()
for item in junctions:
    print(str(item))
print()

print("translating to references")

def findreference(id):
    global junctions

    for item in junctions:
        if item.Id == id:
            return item

    return None

for junction in junctions:
    cons = junction.Connections
    temp = []
    for id in cons:
        x = findreference(id)
        if x is not None:
            temp.append(x)
    junction.Connections = temp

print("computing clusters")
newClusterId = 0
def propagateClusterId(junction, id):
    if junction.ClusterId is None:
        junction.ClusterId = id
        for sibling in junction.Connections:
            propagateClusterId(sibling, id)
    elif junction.ClusterId > id:
        junction.ClusterId = id
        for sibling in junction.Connections:
            propagateClusterId(sibling, id)

for junction in junctions:
    if junction.ClusterId is None:
        propagateClusterId(junction, newClusterId)
        newClusterId += 1

print("collecting clusters")

class Cluster:
    def __init__(self, number):
        self.Number = number
        self.Junctions = []

    def listContents(self):
        s = ""

        for x in self.Junctions:
            s += str(x.Id)
            s += ', '

        return s[0:-2]

    def __str__(self):
        if self.Junctions is None:
            return f"{self.Number} (0)-[]"
        else:
            return f"{self.Number} ({self.length()})-[{self.listContents()}]"

    def add(self, junction):
        if junction in self.Junctions:
            pass
        else:
            self.Junctions.append(junction)

    def length(self):
        return len(self.Junctions)

clusters = []

for item in junctions:
    
    found = False

    for cluster in clusters:
        
        if cluster.Number == item.ClusterId:
        # find cluster with number == item.ClusterId
            cluster.add(item)
            found = True
            break
    
    if not found:
        newCluster = Cluster(item.ClusterId)
        newCluster.add(item)
        clusters.append(newCluster)

def clusterSort(a):
    return len(a.Junctions)

clusters.sort(key = clusterSort, reverse=True) # sort clusters by count

for cluster in clusters[0:min(3, len(clusters))]:
    print(str(cluster))

# *****************************************************************************
# main
# *****************************************************************************

junctions = readData(filename)

processJunctionboxValues(junctions)

print("computering cable length ... >> ", end='', flush=True)

length = len(clusters[0].Junctions)
length *= len(clusters[1].Junctions)
length *= len(clusters[2].Junctions)

print(str(length), end='', flush=True)
print(" <<")

