from bearlibterminal import terminal
from goldminer import settings, draw, text, History
from goldminer.Rect import Rect
from goldminer.Stat import Stat
from goldminer.Inventory import Inventory, WaterEffect, InventoryItem


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.world = None
        self.hp = Stat("HP:", 10)
        self.water = Stat("Water:", 10, colors=["azure", "light azure"])
        self.food = Stat("Food:", 10)

        potion = InventoryItem("!", "azure",
                               "A portable water skin, for approximately 30 ounces of water", WaterEffect(5))

        self.inventory = Inventory(self, 20)
        self.inventory.add(potion, 2)
        self.dead = False

    def set_world(self, world):
        self.world = world

    def move_up(self):
        if self.world.is_walkable(self.x, self.y - 1):
            self.y -= 1
            self.waste()

    def move_down(self):
        if self.world.is_walkable(self.x, self.y + 1):
            self.y += 1
            self.waste()

    def move_left(self):
        if self.world.is_walkable(self.x - 1, self.y):
            self.x -= 1
            self.waste()

    def move_right(self):
        if self.world.is_walkable(self.x + 1, self.y):
            self.x += 1
            self.waste()

    def waste(self):
        self.water.value -= .01
        self.food.value -= .0001

        if self.water.value < 4:
            self.say(text.im_thirsty())

    def render(self):
        terminal.color('orange')
        terminal.put(self.x, self.y, '@')

    def heal(self, amount):
        self.hp.value += amount

    def damage(self, amount):
        self.hp.value -= amount
        if self.hp.value <= 0:
            self.dead = True

    def say(self, text):
        self.world.history.add("Player says: " + text)


class PlayerGui:
    def __init__(self, player):
        self.player = player
        self.rect = settings.gui_rect

    def render(self):
        terminal.color('azure')

        draw.rect(self.rect)

        x = self.rect.left + 2
        y = self.rect.top + 2
        width = self.rect.width - 3

        self.player.hp.render_gui(x, y, width)

        y += 3
        self.player.water.render_gui(x, y, width)

        y += 3
        self.player.food.render_gui(x, y, width)

        y += 4
        terminal.color("#AA6939")
        terminal.print_(x, y, "Inventory:")
        draw.double_line(x, y + 1, width)
        self.player.inventory.render(x, y + 2, width)
