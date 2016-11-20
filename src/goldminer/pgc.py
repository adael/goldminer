import copy
import math
import random

from goldminer import settings, texts, colors, items
from goldminer.History import History
from goldminer.World import Resource, Tile, WorldMap, World, Door
from goldminer.actor import Actor, Fighter
from goldminer.geom import Rect, Direction
from goldminer.inventory import Inventory, Item

house_density = 18


def random_four_orientation(rng, x=0, y=0):
    r = math.radians(rng.randint(0, 4) * 90)
    return int(round(math.cos(r))) + x, int(round(math.sin(r))) + y


def random_eight_orientation(rng, x=0, y=0):
    r = math.radians(rng.randint(0, 4) * 45)
    return int(round(math.cos(r))) + x, int(round(math.sin(r))) + y


def area_is_clear(world_map, area):
    for x, y in area:
        if not world_map.is_walkable(x, y):
            return False
    return True


def find_empty_spaces(world_map, width, height, threshold=5):
    spaces = []
    for y in range(0, world_map.height, threshold):
        for x in range(0, world_map.width, threshold):
            rect = Rect(x, y, width, height)
            if area_is_clear(world_map, rect):
                spaces.append(rect.values)
            rect.swap_size()
            if area_is_clear(world_map, rect):
                spaces.append(rect.values)
    return spaces


def create_player():
    player = Actor("Player", "@", "orange", 2, 2)
    player.fighter = Fighter(player)
    player.inventory = Inventory(player)
    player.history = History()
    # player.waste(300)
    # player.damage(7)
    return player


def create_world():
    seed = 1234
    world_map = WorldMap(settings.default_world_width, settings.default_world_height)
    world_generator = WorldGenerator(world_map, seed)
    world_generator.generate_complete_world()
    player = create_player()
    world = World(world_map, player, seed)
    player.think(texts.im_back)
    return world


def create_house(seed, dox, doy):
    rng = random.Random(seed)

    width = rng.randint(7, 21)
    height = rng.randint(7, 17)

    dx, dy = 0, 0

    if dox != 0:
        dx = width - 1 if dox > 0 else 0
        dy = random.choice(range(1, height - 1))
    elif doy != 0:
        dx = random.choice(range(1, width - 1))
        dy = height - 1 if doy > 0 else 0

    house = WorldMap(width, height)
    gen = WorldGenerator(house, seed)
    gen.make_floor()
    gen.make_borders()
    house.tile(dx, dy).door = Door(closed=False, leave=True)

    return house, dx, dy


def degrees_to_cross_xy(degrees):
    r = math.radians(degrees % 90)
    return int(round(math.cos(r))), int(round(math.sin(r)))


def create_floor_tiles(width, height):
    return [[Tile(".", random.choice(settings.floor_colors)) for _ in range(height)] for _ in range(width)]


class WorldGenerator:
    def __init__(self, world_map, seed):
        self.rng = random.Random(seed)
        self.world_map = world_map

    def generate_complete_world(self):
        self.make_floor()
        self.make_borders()
        # self.create_house(Rect(10, 10, 3, 3), 1, 0)
        self.create_houses(house_density)
        #self.generate_street_side(10, 10, 4, Direction.down, Direction.right)
        #self.generate_street_side(16, 10, 4, Direction.down, Direction.left)
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
            area = Rect(x - 1, y - 1, 3, 3)
            if area_is_clear(self.world_map, area):
                dx, dy = random_four_orientation(self.rng)
                self.create_house(area, dx, dy)

    def create_house(self, area, dx, dy):
        self.make_walls(area)
        self.world_map.tile(area.x + dx + 1, area.y + + dy + 1).door = Door()

    def make_walls(self, locations):
        for x, y in locations:
            self.make_wall(x, y)

    def make_wall(self, x, y, color=None):
        if color is None:
            color = colors.slategray
        tile = self.world_map.tile(x, y)
        tile.walkable = False
        tile.char = "#"
        tile.color = color

    def put_resources(self):
        for x, y in self.random_tile_groups():
            tile = self.world_map.tile(x, y)
            if tile.walkable and not tile.resource:
                item = copy.copy(self.rng.choice(items.stones))
                tile.resource = Resource(item.char, item.color, random.randint(0, 10))
                tile.resource.drop = item

    def put_trees(self):
        for coord in self.random_tile_groups(10, 10):
            x, y = coord
            tile = self.world_map.tile(x, y)
            if tile.walkable and not tile.resource:
                tile.resource = Resource("^", "dark green", random.randint(3, 12))
                tile.resource.drop = copy.copy(items.wood_log)

    def random_tile_groups(self, max_groups=5, group_size=5):
        tile_coords = []
        for group in range(random.randint(0, max_groups)):
            x = random.randint(0, self.world_map.width)
            y = random.randint(0, self.world_map.height)
            if self.world_map.inside_map(x, y):
                tile_coords.append((x, y))
            for z in range(random.randint(0, group_size)):
                cx, cy = random_eight_orientation(self.rng, x, y)
                if self.world_map.inside_map(cx, cy):
                    tile_coords.append((cx, cy))

        return tile_coords

    def generate_street_side(self, x: int, y: int, num: int,
                             street_direction: Direction, doors_direction: Direction,
                             room_width=3, room_height=3, margin=1):

        if street_direction.is_vertical:
            area = Rect(x, y, room_width + margin, num * (room_height + margin))
        else:
            area = Rect(x, y, num * (room_width + margin), room_height + margin)

        spaces = find_empty_spaces(self.world_map, area.width, area.height)
        (x, y, w, h) = self.rng.choice(spaces)

        dx, dy = doors_direction.as_vector()

        if street_direction.is_vertical:
            for n in range(0, num):
                self.create_house(Rect(area.x, area.y + (n * (room_height + margin)), room_width, room_height), dx, dy)
        else:
            for n in range(0, num):
                self.create_house(Rect(area.x + (n * (room_width + margin)), area.y, room_width, room_height), dx, dy)
