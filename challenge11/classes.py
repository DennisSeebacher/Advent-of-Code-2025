class Device:

    idcounter = 0

    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs.copy()
        self.id = Device.idcounter
        Device.idcounter += 1

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"
