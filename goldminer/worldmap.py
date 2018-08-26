from goldminer import colors
from goldminer.inventory import Inventory
from goldminer.exceptions import OutOfBoundsException, TileBlockedException


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
            raise OutOfBoundsException("Out of range: {0}, {1}".format(x, y))

    def set_tile(self, x, y, tile):
        self.tiles[x][y] = tile

    def is_walkable(self, x, y):
        return self.inside_map(x, y) and self.tile(x, y).is_walkable()


class Tile:
    def __init__(self, char="·", color="gray", walkable=True):
        self._char = char
        self._color = color
        self.walkable = walkable
        self.resource = None
        self.door = None
        self.chest = None
        self.item = None
        self._in_sight = False
        self.explored = False

    @property
    def blocked(self):
        return bool(not self.walkable or self.resource or self.door or self.chest or self.item)

    @property
    def color(self):
        if self.resource:
            return self.resource.color
        elif self.door:
            return self.door.color
        elif self.chest:
            return self.chest.color
        elif self.item:
            return self.item.color
        else:
            return self._color

    @property
    def char(self):
        if self.resource:
            return self.resource.char
        elif self.door:
            return self.door.char
        elif self.chest:
            return self.chest.char
        elif self.item:
            return self.item.char
        else:
            return self._char

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

    def place_item(self, item):
        if self.blocked:
            raise TileBlockedException
        self.item = item

    def modify(self, char, color):
        self._char = char
        self._color = color


class Door:
    def __init__(self, color=colors.doors, closed=True, leave=False):
        self.color = color
        self.closed = closed
        self.leave = leave

    @property
    def char(self):
        return "+" if self.closed else "/"

    @property
    def opened(self):
        return not self.closed

    def open(self):
        self.closed = False

    def close(self):
        self.closed = True


class Container:
    def __init__(self, description, capacity, char="~", color=colors.chests):
        self.char = char
        self.color = color
        self.inventory = Inventory(capacity)
        self.description = description

    def is_empty(self):
        return self.inventory.is_empty()
