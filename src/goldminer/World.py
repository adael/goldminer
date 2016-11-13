import random
from bearlibterminal import terminal
from goldminer import settings
from goldminer.Rect import Rect

floor_colors = ["gray", "dark gray", "darker gray", "darkest gray", "darkest yellow", "darker yellow"]


def create_tiles(width, height):
    return [[Tile() for _ in range(height)] for _ in range(width)]


class World:
    def __init__(self, worldmap, player):
        self.worldmap = worldmap
        self.actors = []
        self.player = player
        self.viewport = settings.map_rect

    def position_to_viewport(self, x, y):
        return x - self.viewport.x, y - self.viewport.y

    def position_from_viewport(self, x, y):
        return x + self.viewport.x, y + self.viewport.y

    def tile(self, x, y):
        return self.worldmap.tile(x, y)

    def add(self, actor):
        actor.set_world(self)
        self.actors.append(actor)
        return actor

    def is_walkable(self, x, y):
        return self.worldmap.is_walkable(x, y)

    def actor_move(self, actor, x, y):
        if self.is_walkable(actor.x + x, actor.y + y):
            actor.move(x, y)

    def actor_heal(self, actor, amount):
        actor.heal(amount)

    def actor_say(self, actor, messages):
        if actor is self.player or actor.distance_to(self.player) < 10:
            self.player.listen(actor.name + " says: " + random.choice(messages))



class WorldMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = create_tiles(width, height)

    def tile(self, x, y):
        return self.tiles[x][y]

    def is_walkable(self, x, y):
        return 0 > x < self.width and 0 > y < self.height and self.tile(x, y).walkable


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


class Resource:
    def __init__(self, char="*", walkable=False, color="yellow"):
        self.char = char
        self.walkable = walkable
        self.color = color
        self.quantity = random.randint(1, 500)
