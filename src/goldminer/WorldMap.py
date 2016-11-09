import random
from bearlibterminal import terminal
from goldminer.Rect import Rect


floor_colors = ["gray", "dark gray", "darker gray", "darkest gray", "darkest yellow", "darker yellow"]


def random_orientation():
    r = random.randint(1, 9)
    if r == 1:
        return -1, -1
    if r == 2:
        return 0, -1
    elif r == 3:
        return +1, -1
    elif r == 4:
        return -1, 0
    elif r == 5:
        return 0, 0
    elif r == 6:
        return +1, 0
    elif r == 7:
        return -1, -1
    elif r == 8:
        return 0, +1
    elif r == 9:
        return +1, +1


class WorldMap:
    def __init__(self, rect, history):
        self.history = history
        self.rect = rect
        self.viewport = rect
        self.tiles = [[Tile() for _ in range(self.rect.h)] for _ in range(self.rect.w)]
        # self.make_borders()
        self.create_mine()
        self.put_resources()
        self.put_trees()
        self.actors = []

    def make_borders(self):
        for y in range(self.rect.h):
            self.make_wall(0, y)
            self.make_wall(self.rect.w - 1, y)

        for x in range(self.rect.w):
            self.make_wall(x, 0)
            self.make_wall(x, self.rect.h - 1)

    def create_mine(self):
        self.make_wall(10, 10)
        self.make_walls([
            (10, 10), (11, 10), (12, 10),
            (10, 11), (12, 11)
        ])

    def make_walls(self, locations):
        for (x, y) in locations:
            self.make_wall(x, y)

    def make_wall(self, x, y):
        tile = self.tile(x, y)
        tile.walkable = False
        tile.char = "#"
        tile.color = "white"

    def put_resources(self):
        for coord in self.random_tile_groups():
            x, y = coord
            tile = self.tile(x, y)
            if tile.walkable and not tile.resource:
                tile.resource = Resource()

    def put_trees(self):
        for coord in self.random_tile_groups(10, 10):
            x, y = coord
            tile = self.tile(x, y)
            if tile.walkable and not tile.resource:
                tile.resource = Resource(char="^", color="dark green")

    def random_tile_groups(self, max_groups=5, group_size=5):
        tile_coords = []
        for group in range(random.randint(0, max_groups)):
            x = random.randint(1, self.rect.w - 1)
            y = random.randint(1, self.rect.h - 1)
            for z in range(random.randint(0, group_size)):
                mx, my = random_orientation()
                tile_coords.append((x + mx, y + my))

        return tile_coords

    def render(self):
        for y in range(self.viewport.y, self.viewport.h):
            for x in range(self.viewport.x, self.viewport.w):
                self.tile(x, y).render(x, y)

    def tile(self, x, y):
        return self.tiles[x][y]

    def add(self, actor):
        actor.set_world(self)
        self.actors.append(actor)

    def is_walkable(self, x, y):
        return self.rect.contains(x, y) and self.tile(x, y).walkable


class Tile:
    def __init__(self, char="·", walkable=True, color="gray"):
        if char == "·" and color == "gray":
            color = random.choice(floor_colors)

        self.char = char
        self._walkable = walkable
        self.color = color
        self.resource = None

    @property
    def walkable(self):
        if self.resource:
            return self.resource.walkable
        else:
            return self._walkable

    @walkable.setter
    def walkable(self, value):
        if not self.resource:
            self._walkable = value

    def render(self, x, y):
        if self.resource:
            self.resource.render(x, y)
        else:
            terminal.color(self.color)
            terminal.put(x, y, self.char)


class Resource:
    def __init__(self, char="*", walkable=False, color="yellow"):
        self.char = char
        self.walkable = walkable
        self.color = color
        self.quantity = random.randint(1, 500)

    def render(self, x, y):
        terminal.color(self.color)
        terminal.put(x, y, self.char)
