from goldminer.actor import Inventory


class WorldMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []
    
    def inside_map(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def tile(self, x, y):
        try:
            return self.tiles[x][y]
        except IndexError:
            print("Out of range: ", x, y)
            raise
    
    def set_tile(self, x, y, tile):
        self.tiles[x][y] = tile
    
    def is_walkable(self, x, y):
        return self.inside_map(x, y) and self.tile(x, y).is_walkable()


class Tile:
    def __init__(self, char="·", color="gray", walkable=True):
        self.char = char
        self.color = color
        self.walkable = walkable
        self.resource = None
        self.door = None
        self.chest = None
        self._in_sight = False
        self.explored = False
    
    @property
    def in_sight(self):
        return self._in_sight
    
    @in_sight.setter
    def in_sight(self, value: bool):
        if value:
            self.explored = value
        self._in_sight = value
    
    def is_walkable(self):
        if self.door and self.door.closed:
            return False
        
        if self.resource:
            return self.resource.walkable
        
        return self.walkable


class Door:
    def __init__(self, color="red", closed=True, leave=False):
        self.color = color
        self.closed = closed
        self.leave = leave
    
    def open(self):
        self.closed = False
    
    def close(self):
        self.closed = True


class Container:
    def __init__(self, color="red", capacity=8):
        self.char = "~"
        self.color = color
        self.inventory = Inventory(capacity)
