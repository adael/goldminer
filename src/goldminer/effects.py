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
