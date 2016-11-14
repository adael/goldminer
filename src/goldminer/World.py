import random

from goldminer import settings
from goldminer.Camera import Camera


class World:
    def __init__(self, world_map, player):
        self.world_map = world_map
        self.actors = []
        self.player = player

        self.camera = Camera(
            width=settings.map_rect.w,
            height=settings.map_rect.h,
            map_width=self.world_map.width,
            map_height=self.world_map.height,
            offset_x=settings.map_rect.x,
            offset_y=settings.map_rect.y
        )
        self.camera.update(self.player.x, self.player.y)

    def inside_map(self, x, y):
        return self.world_map.inside_map(x, y)

    def tile(self, x, y):
        return self.world_map.tile(x, y)

    def set_tile(self, x, y, tile):
        self.world_map.set_tile(x, y, tile)

    def add(self, actor):
        actor.set_world(self)
        self.actors.append(actor)
        return actor

    def is_walkable(self, x, y):
        return self.world_map.is_walkable(x, y)

    def actor_move(self, actor, x, y):
        if self.is_walkable(actor.x + x, actor.y + y):
            actor.move(x, y)

    def player_move(self, x, y):
        if self.is_walkable(self.player.x + x, self.player.y + y):
            self.player.move(x, y)
            self.camera.update(self.player.x, self.player.y)

    def actor_heal(self, actor, amount):
        actor.heal(amount)

    def actor_say(self, actor, messages):
        if actor is self.player or actor.distance_to(self.player) < 10:
            self.player.listen(actor.name + " says: " + random.choice(messages))


class WorldMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []
        self.resources = []

    def inside_map(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def tile(self, x, y):
        return self.tiles[x][y]

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

    def is_walkable(self):
        if self.door and self.door.closed:
            return False

        if self.resource:
            return self.resource.walkable

        return self.walkable


class Resource:
    def __init__(self, char, color, quantity, walkable=False):
        self.char = char
        self.color = color
        self.quantity = quantity
        self.walkable = walkable


class Door:
    def __init__(self, char="+", color="red"):
        self.char = char
        self.color = color
        self.closed = True

    def open(self):
        self.char = "/"
        self.closed = False

    def close(self):
        self.char = "+"
        self.closed = True
