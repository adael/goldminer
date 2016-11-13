import random, math
from bearlibterminal import terminal
from goldminer import settings, draw, texts, History
from goldminer.Rect import Rect
from goldminer.Stat import Stat
from goldminer.Inventory import Inventory, RestoreThirstEffect, InventoryItem


class Actor:
    def __init__(self, name, char, color, x=None, y=None):
        self.world = None
        self.name = name
        self.char = char
        self.color = color
        self.x = x
        self.y = y
        self.fighter = None
        self.inventory = None

    def set_position(self, x, y):
        self.x, self.y = x, y

    def set_world(self, world):
        self.world = world

    def distance_to(self, other):
        return self.distance(other.x, other.y)

    def distance(self, x, y):
        return math.hypot(x - self.x, y - self.y)

    def move(self, x, y):
        self.x += x
        self.y += y
        self.waste()

    def heal(self, amount):
        if self.fighter:
            self.fighter.heal(amount)

    def damage(self, amount):
        if self.fighter:
            self.fighter.take_damage(amount)

    def waste(self):
        if self.fighter:
            self.fighter.waste()

    def attack(self, other):
        if self.fighter:
            self.fighter.attack(other)
            self.waste()


class Fighter:

    def __init__(self, owner):
        self.owner = owner
        self.hp = Stat("HP:", 10)
        self.water = Stat("Water:", 10, colors=["azure", "light azure"])
        self.food = Stat("Food:", 10)
        self.fatigue = Stat("Fatigue:", 10)
        self.dead = False
        self.damage = 1

        self.last_complain = random.randint(0, 25)

    def heal(self, amount):
        self.hp.value += amount

    def take_damage(self, amount):
        self.hp.value -= amount
        if self.hp.value <= 0:
            self.dead = True

    def waste(self):
        self.fatigue.value -= 0.01
        self.water.value -= .001
        self.food.value -= .0001

        if self.fatigue.value < 4 and random.random() < .3:
            self.owner.world.actor_say(self.owner, texts.im_tired)

        if self.water.value < 4 and random.random() < .3:
            self.owner.world.actor_say(self.owner, texts.im_thirsty)

        if self.food.value < 2 and random.random() < .2:
            self.owner.world.actor_say(self.owner, texts.im_hungry)

    def attack(self, other):
        if other.defense < self.damage:
            other.take_damage(self.damage)