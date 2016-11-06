import random
from bearlibterminal import terminal
from goldminer.Rect import Rect

floor_colors = ["darkest green", "dark green", "dark gray"]

class WorldMap:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.rect = Rect(0, 0, w, h)
        self.viewport = Rect(0, 0, w, h)
        self.tiles = [[Tile() for _ in range(self.h)] for _ in range(self.w)]
        self.make_borders()
        self.create_mine()
        self.actors = []

    def make_borders(self):
        for y in range(self.h):
            self.make_wall(0, y)
            self.make_wall(self.w - 1, y)

        for x in range(self.w):
            self.make_wall(x, 0)
            self.make_wall(x, self.h - 1)

    def create_mine(self):
        self.make_wall(10, 10)
        self.make_walls([
            (10, 10), (11, 10), (12, 10),
            (10, 11), (12, 11)
        ])

    def make_walls(self, coords):
        for (x, y) in coords:
            self.make_wall(x, y)

    def make_wall(self, x, y):
        tile = self.tile(x, y)
        tile.walkable = False
        tile.char = "#"
        tile.color = "white"

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
        self.walkable = walkable
        self.color = color

    def render(self, x, y):
        terminal.color(self.color)
        terminal.put(x, y, self.char)
