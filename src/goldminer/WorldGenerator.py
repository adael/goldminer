import math
import random

from goldminer import settings, texts
from goldminer.History import History
from goldminer.World import Resource, Tile, WorldMap, World, Door
from goldminer.actor import Actor, Fighter
from goldminer.inventory import Inventory


def create_player():
    player = Actor("Player", "@", "orange", 2, 2)
    player.fighter = Fighter(player)
    player.inventory = Inventory(player)
    player.history = History()
    player.waste(600)
    player.damage(7)
    return player


def create_world():
    seed = 1234
    world_map = WorldMap(settings.default_world_width, settings.default_world_height)
    world_generator = WorldGenerator()
    world_generator.generate(world_map, seed)
    player = create_player()
    world = World(world_map, player)
    player.think(texts.im_back)
    return world


def create_floor_tiles(width, height):
    return [[Tile(".", random.choice(settings.floor_colors)) for _ in range(height)] for _ in range(width)]


class WorldGenerator:
    def __init__(self):
        self.rng = random.Random()
        self.world_map = None

    def generate(self, world_map, seed):
        self.rng.seed(seed)
        self.world_map = world_map
        self.make_floor()
        self.make_borders()
        self.create_houses(5)
        self.put_resources()
        self.put_trees()

    def random_position(self):
        return self.rng.randint(0, self.world_map.width), self.rng.randint(0, self.world_map.height)

    def make_floor(self):
        self.world_map.tiles = create_floor_tiles(self.world_map.width, self.world_map.height)

    def make_borders(self):
        for y in range(self.world_map.height):
            self.make_wall(0, y)
            self.make_wall(self.world_map.width - 1, y)

        for x in range(self.world_map.width):
            self.make_wall(x, 0)
            self.make_wall(x, self.world_map.height - 1)

    def create_houses(self, amount):
        for _ in range(amount):
            x, y = self.random_position()
            self.create_house(x, y)

    def create_house(self, x, y):
        coords = [
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y), (x, y), (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
        ]

        dx, dy = self.random_four_orientation(x, y)

        for px, py in coords:
            if not self.world_map.is_walkable(px, py):
                return

        for px, py in coords:
            self.make_wall(px, py)

        self.world_map.tile(dx, dy).door = Door()

    def make_walls(self, locations):
        for (x, y) in locations:
            self.make_wall(x, y)

    def make_wall(self, x, y, color="white"):
        tile = self.world_map.tile(x, y)
        tile.walkable = False
        tile.char = "#"
        tile.color = color

    def put_resources(self):
        for x, y in self.random_tile_groups():
            tile = self.world_map.tile(x, y)
            if tile.walkable and not tile.resource:
                tile.resource = Resource("*", "yellow", random.randint(0, 10))

    def put_trees(self):
        for coord in self.random_tile_groups(10, 10):
            x, y = coord
            tile = self.world_map.tile(x, y)
            if tile.walkable and not tile.resource:
                tile.resource = Resource("^", "dark green", random.randint(3, 12))

    def random_tile_groups(self, max_groups=5, group_size=5):
        tile_coords = []
        for group in range(random.randint(0, max_groups)):
            x = random.randint(0, self.world_map.width)
            y = random.randint(0, self.world_map.height)
            if self.world_map.inside_map(x, y):
                tile_coords.append((x, y))
            for z in range(random.randint(0, group_size)):
                cx, cy = self.random_eight_orientation(x, y)
                if self.world_map.inside_map(cx, cy):
                    tile_coords.append((cx, cy))

        return tile_coords

    def validate_coords(self, coords):
        for x, y in coords:
            if not self.world_map.is_walkable(x, y):
                return False
        return True

    def random_four_orientation(self, x=0, y=0):
        r = math.radians(self.rng.randint(0, 4) * 90)
        return int(round(math.cos(r))) + x, int(round(math.sin(r))) + y

    def random_eight_orientation(self, x=0, y=0):
        r = math.radians(self.rng.randint(0, 4) * 45)
        return int(round(math.cos(r))) + x, int(round(math.sin(r))) + y
