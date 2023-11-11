import enum

class TileType(enum.Enum):
    Disconnected = 0
    Connected = 1
    Obstruction = 2
    Tower = 3