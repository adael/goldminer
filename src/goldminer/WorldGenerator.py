import random
from goldminer.WorldMap import Resource

class WorldGenerator:

    def __init__(self):
        self.rng = random.Random()
        self.world = None

    def generate(self, world, seed):
        self.rng.seed(seed)
        self.world = world
        # self.make_borders()
        self.create_mine()
        self.put_resources()
        self.put_trees()

    def make_borders(self):
        for y in range(self.world.height):
            self.make_wall(0, y)
            self.make_wall(self.world.width - 1, y)

        for x in range(self.world.width):
            self.make_wall(x, 0)
            self.make_wall(x, self.world.height - 1)

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
        tile = self.world.tile(x, y)
        tile.walkable = False
        tile.char = "#"
        tile.color = "white"

    def put_resources(self):
        for coord in self.random_tile_groups():
            x, y = coord
            tile = self.world.tile(x, y)
            if tile.walkable and not tile.resource:
                tile.resource = Resource()

    def put_trees(self):
        for coord in self.random_tile_groups(10, 10):
            x, y = coord
            tile = self.world.tile(x, y)
            if tile.walkable and not tile.resource:
                tile.resource = Resource(char="^", color="dark green")

    def random_tile_groups(self, max_groups=5, group_size=5):
        tile_coords = []
        for group in range(random.randint(0, max_groups)):
            x = random.randint(self.world.width)
            y = random.randint(self.world.height)
            for z in range(random.randint(0, group_size)):
                mx, my = self.random_orientation()
                tile_coords.append((x + mx, y + my))

        return tile_coords

    def random_orientation(self):
        r = self.rng.randint(1, 9)
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
