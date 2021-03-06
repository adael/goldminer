from goldminer import colors


class Resource:
    """
    Represents a recollectable resource like food, wood, ores, etc.
    Attributes:
        char (str):
        color (str):
        item (Item): the item that you get when the resource is gathered
        quantity (int): number of items you can gather before it depletes
        hardness (int): the force that needs to be applied to gather the resource. It affects to energy wasted
        health (int): number of hits to get a drop
        max_health (int): the reference value for restore health
        walkable (bool): if the resource can be walked through
        restore_penalty (int): each time an item is gathered from the resource, it'll cost more to get the next.
    """

    def __init__(self, char, color, item=None, quantity=1, hardness=1, health=100, walkable=False):
        self.char = char
        self.color = color
        self.quantity = quantity
        self.walkable = walkable
        self.health = health
        self.max_health = self.health
        self.hardness = hardness
        self.item = item
        self.restore_penalty = 2

    @property
    def depleted(self):
        return self.quantity <= 0

    def restore_health(self):
        self.max_health += self.restore_penalty
        self.health = self.max_health


class Material:
    def __init__(self, name, color):
        self.name = name
        self.color = color


class Item:
    def __init__(self, char, color, description, effect=None):
        self.char = char
        self.color = color
        self.description = description
        self.effect = effect


stone_flint = Item("*", "gray", "A flint stone")
stone_chert = Item("*", colors.steelblue, "A gray chert rock")
stone_jasper = Item("*", colors.darksalmon, "A red jasper rock")
stone_chalcedony = Item("*", colors.skyblue, "A sky-blue chalcedony rock")
stone_quartz = Item("*", colors.beige, "A solid quartz rock")
stone_obsidian = Item("*", colors.night, "A obsidian rock")
stones = [stone_flint, stone_chert, stone_jasper, stone_chalcedony, stone_quartz, stone_obsidian]

wood_log = Item("w", colors.woody_brown, "A wood log")

# Resource(item.char, item.color, item=item, quantity=random.randint(0, 10))
