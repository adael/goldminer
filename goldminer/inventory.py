class Inventory:
    def __init__(self, owner, capacity=40):
        self.owner = owner
        self.capacity = capacity
        self.items = []

    def __iter__(self):
        return iter(self.items)

    def is_full(self):
        return len(self.items) >= self.capacity

    def is_empty(self):
        return len(self.items) == 0

    def count(self):
        return len(self.items)

    def has(self, index):
        return len(self.items) > index

    def get(self, index):
        return self.items[index]

    def add(self, item):
        self.items.append(item)

    def drop(self, item):
        self.items.remove(item)

