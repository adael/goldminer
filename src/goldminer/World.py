import random

from goldminer import settings
from goldminer.Rect import Rect


class World:
    def __init__(self, worldmap, player):
        self.worldmap = worldmap
        self.actors = []
        self.player = player
        self.camera = Camera(Rect.from_rect(settings.map_rect), self.worldmap.width, self.worldmap.height)

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

    def player_move(self, x, y):
        if self.is_walkable(self.player.x + x, self.player.y + y):
            self.player.move(x, y)
            self.camera.update(self.player.x, self.player.y)

    def actor_heal(self, actor, amount):
        actor.heal(amount)

    def actor_say(self, actor, messages):
        if actor is self.player or actor.distance_to(self.player) < 10:
            self.player.listen(actor.name + " says: " + random.choice(messages))


class Camera:
    def __init__(self, rect, map_width, map_height):
        self.rect = rect
        self.map_width = map_width
        self.map_height = map_height

    def update(self, tx, ty):
        # coordinates so that the target is at the center of the screen
        x = int(tx - self.rect.w / 2)
        y = int(ty - self.rect.h / 2)

        # make sure the camera doesn't see outside the map
        x = max(0, min(self.map_width - self.rect.width, x))
        y = max(0, min(self.map_height - self.rect.height, y))

        self.rect.set_position(x, y)

    def map_to_camera(self, x, y):
        return x - self.rect.x, y - self.rect.y

    def camera_to_map(self, x, y):
        return x + self.rect.x, y + self.rect.y


class WorldMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []
        self.resources = []

    def tile(self, x, y):
        return self.tiles[x][y]

    def is_walkable(self, x, y):
        if 0 < x >= self.width or 0 < y >= self.height:
            return False

        return self.tile(x, y).is_walkable()


class Tile:
    def __init__(self, char="·", color="gray", walkable=True, ):
        self.char = char
        self.color = color
        self.walkable = walkable
        self.resource = None

    def is_walkable(self):
        if self.resource:
            return self.resource.walkable
        else:
            return self.walkable


class Resource:
    def __init__(self, char, color, quantity, walkable=False):
        self.char = char
        self.color = color
        self.quantity = quantity
        self.walkable = walkable
