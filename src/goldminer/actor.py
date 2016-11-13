import math
import random

from goldminer import texts
from goldminer.Stat import Stat


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
        self.history = None

        self.deaf = False
        self.mute = False
        self.blind = False

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

    def waste(self, amount=1):
        if self.fighter:
            self.fighter.waste(amount)

    def can_attack(self, other):
        return self.fighter and other.fighter

    def attack(self, other):
        if self.fighter and other.fighter:
            self.fighter.attack(other.figther)

    def can_talk(self):
        return not self.mute

    def say(self, text):
        if self.can_talk():
            self.history.add_self(self, "say", text)
            self.world.actor_say(self, text)
        else:
            self.think(texts.im_muted)

    def think(self, text):
        self.history.add_self(self, "think", text)

    # senses
    def can_ear(self):
        return not self.deaf

    def can_see(self):
        return not self.blind

    def see(self, text):
        if self.can_see():
            self.history.add_self(self, "see", text)

    def ear(self, text):
        if self.can_ear():
            self.history.add_self(self, "hear", text)

    def listen(self, text):
        if self.can_ear():
            self.history.add_self(self, "listen", text)

    def feel(self, feeling):
        self.history.add_self(self, "feel", feeling)


class Fighter:
    def __init__(self, owner):
        self.owner = owner
        self.hp = Stat("HP:", 10)
        self.water = Stat("Water:", 10)
        self.food = Stat("Food:", 10)
        self.fatigue = Stat("Fatigue:", 10)
        self.dead = False
        self.damage = 1

        self.last_complain = random.randint(0, 25)

    def heal(self, amount):
        self.hp.value += amount
        if self.hp.value < 0:
            self.hp.value = 0

    def take_damage(self, amount):
        self.hp.value -= amount
        if self.hp.value <= 0:
            self.dead = True

    def waste(self, amount=1):
        self.fatigue.value -= amount / 100
        self.water.value -= amount / 1000
        self.food.value -= amount / 10000

        if self.fatigue.value < 4 and random.random() < .3:
            self.owner.feel(texts.im_tired)

        if self.water.value < 4 and random.random() < .3:
            self.owner.feel(texts.im_thirsty)

        if self.food.value < 2 and random.random() < .2:
            self.owner.feel(texts.im_hungry)

    def attack(self, other):
        if other.defense < self.damage:
            other.take_damage(self.damage)
        self.waste()
