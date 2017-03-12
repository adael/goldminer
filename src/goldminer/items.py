from goldminer import colors


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
