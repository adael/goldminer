from bearlibterminal import terminal
from goldminer import texts


class Inventory:

    def __init__(self, owner, max_size=8):
        self.owner = owner
        self.max_size = max_size
        self.items = []

    def __iter__(self):
        return iter(self.items)

    def is_empty(self):
        return True if self.items else False

    def add(self, item, amount=1):
        if len(self.items) + amount < self.max_size:
            for _ in range(amount):
                self.items.append(item)
        else:
            self.owner.say(texts.no_more_space())

    def use(self, index, target):
        if index in self.items:
            self.items[index].apply(self.owner, target)

class InventoryItem:

    def __init__(self, char, color, description, effect=None):
        self.char = char
        self.color = color
        self.description = description
        self.effect = effect


class HealEffect:
    def __init__(self, amount=5):
        self.amount = amount

    def apply(self, source, target):
        target.hp.value += self.amount


class RestoreThirstEffect:
    def __init__(self, amount=5):
        self.amount = amount

    def apply(self, source, target):
        target.water.value += self.amount

