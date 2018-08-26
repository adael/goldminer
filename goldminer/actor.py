import math
import random
from goldminer import texts
from goldminer.exceptions import TileBlockedException, OutOfBoundsException


class Actor:
    def __init__(self, name, char, color, x=None, y=None):
        self.world = None
        self.name = name
        self.char = char
        self.color = color
        self.x = x
        self.y = y
        self.orientation = None
        self.fighter = None
        self.inventory = None
        self.history = None

        self.resting = False

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, value):
        self.x, self.y = value

    def set_position(self, x, y):
        self.x, self.y = x, y

    def set_world(self, world):
        self.world = world

    def distance_to(self, other):
        return self.distance(other.x, other.y)

    def distance(self, x, y):
        return math.hypot(x - self.x, y - self.y)

    def move(self, x, y):
        self.move_position(x, y)
        self.waste()

    def move_position(self, x, y):
        self.x += x
        self.y += y

    def looking_position(self):
        (x, y) = self.x, self.y
        if self.orientation:
            (dx, dy) = self.orientation
            x += dx
            y += dy
        return x, y

    def heal(self, amount):
        if self.fighter:
            self.fighter.heal(amount)

    def damage(self, amount):
        if self.fighter:
            self.fighter.take_damage(amount)

    def waste(self, amount=1):
        if self.fighter:
            self.fighter.waste(amount)

    def restore(self, amount=1):
        if self.fighter:
            self.fighter.restore(amount)

    def can_attack(self, other):
        return self.fighter and other.fighter

    def attack(self, other):
        if self.can_attack(other):
            self.fighter.attack(other.figther)


    def drop_item(self, item):
        try:
            self.world.place_item(self.x, self.y, item)
            self.inventory.drop(item)
        except TileBlockedException:
            self.thinks("I cannot place anything here, it's blocked")
        except OutOfBoundsException:
            self.thinks("I cannot place anything here, it's in the outside world")

    def current_tile(self):
        return self.world.tile(self.x, self.y)
