class Inventory:
    def __init__(self, owner, capacity=4):
        self.owner = owner
        self.capacity = capacity
        self.items = []

    def __iter__(self):
        return iter(self.items)

    @property
    def is_full(self):
        return len(self.items) >= self.capacity

    @property
    def is_empty(self):
        return False if self.items else True

    def add(self, item):
        self.items.append(item)

    def use(self, index, target):
        if index in self.items:
            self.items[index].apply(self.owner, target)


class Item:
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
