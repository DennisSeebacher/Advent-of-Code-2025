class Connection:

    id_counter = 0

    def __init__(self, a, b, distance):
        self.id = Connection.id_counter
        Connection.id_counter += 1
        self.a = a
        self.b = b
        self.distance = distance

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Connection #{self.id:<5} {self.a.id:>8} -> {self.b.id:<8} => {self.distance:8}"

class Circuit:

    id_counter = 0

    def __init__(self):
        self.id = Circuit.id_counter
        Circuit.id_counter += 1
        self.members = []

    def getSize(self):
        return len(self.members)
    
    def addMember(self, candidate):
        if candidate not in self.members:
            self.members.append(candidate)

    def moveMembersFrom(self, circuit):
        '''
        moves the members from the given circuit into this circuit
        '''

        for member in circuit.members:
            self.members.append(member)
        circuit.members.clear()

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        if  len(self.members) < 5:
            return f"Circuit #{self.id:<5} -> {self.getSize():8} {str(self.members)}"
        else:
            return f"Circuit #{self.id:<5} -> {self.getSize():8} Junctionboxes"

class Junctionbox:

    idcounter = 0

    def __init__(self, x, y, z):
        self.id = Junctionbox.idcounter
        Junctionbox.idcounter += 1
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Junctionbox #{self.id} ({self.x}/{self.y}/{self.z})"