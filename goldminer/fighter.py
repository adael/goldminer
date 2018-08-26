import random
from goldminer import texts
from goldminer.stat import Stat

class Fighter:
    def __init__(self, owner):
        self.owner = owner
        self.hp = Stat("Health:", 10)
        self.water = Stat("Hydration:", 10)
        self.food = Stat("Feeding:", 10)
        self.fatigue = Stat("Fatigue:", 10)
        self.damage = 1

        self.last_complain = random.randint(0, 25)

    def heal(self, amount):
        self.hp.value += amount
        if self.hp.value < 0:
            self.hp.value = 0

    def take_damage(self, amount):
        self.hp.value -= amount
        if self.hp.value <= 0:
            self.owner.dead = True

    def waste(self, amount=1):
        self.fatigue.value -= amount / 100
        self.water.value -= amount / 1000
        self.food.value -= amount / 10000

        if self.fatigue.value <= 0:
            self.owner.thinks(texts.im_losing_consciousness)
            self.owner.resting = True
            return

        if self.fatigue.value < 4:
            self.owner.thinks(texts.im_tired, 0.015)

        if self.water.value < 4:
            self.owner.thinks(texts.im_thirsty, 0.015)

        if self.food.value < 2:
            self.owner.thinks(texts.im_hungry, 0.005)

    def restore(self, amount=1):
        self.fatigue.value += amount / 10
        if self.fatigue.value > .25 and random.random() <= 0.01 + self.fatigue.value:
            self.owner.resting = False
            self.owner.thinks(texts.im_wake_up)

    def attack(self, other):
        if other.defense < self.damage:
            other.take_damage(self.damage)
        self.waste()


