class Tower:
    def __init__(self, radius, coords):
        self.x, self.y = coords
        self.radius = radius
        self.connections = set()

    def connect(self, tower):
        self.connections.add(tower)
        