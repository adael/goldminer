from bearlibterminal import terminal
from goldminer import game
from goldminer import draw
from goldminer.Rect import Rect


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.world = None
        self.hp = Stat("HP:", 10)
        self.water = Stat("Water:", 10, colors=["azure", "light azure"])
        self.food = Stat("Food:", 10)
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

    def render(self):
        terminal.color('orange')
        terminal.put(self.x, self.y, '@')

    def heal(self, amount):
        self.hp.value += amount

    def damage(self, amount):
        self.hp.value -= amount
        if self.hp.value <= 0:
            self.dead = True


class PlayerGui:
    def __init__(self, player):
        self.player = player
        self.rect = Rect.from_points(game.MAP_WIDTH + 1, 0, game.SCREEN_WIDTH - 1, game.MAP_HEIGHT - 1)

    def render(self):
        terminal.color('azure')
        draw.rect(self.rect)

        x = self.rect.left + 2
        y = self.rect.top + 1
        width = self.rect.width - 3

        self.player.hp.render_gui(x, y, width)
        self.player.water.render_gui(x, y + 3, width)
        self.player.food.render_gui(x, y + 6, width)


class Stat:
    def __init__(self, label, value, max_value=None, colors=None):
        if max_value is None:
            max_value = value

        self.label = label
        self._value = value
        self.max_value = max_value
        self.colors = colors
        self.bkcolor = "dark gray"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = min(self.max_value, max(0, value))

    @property
    def percent(self):
        return int(round(self._value * 100 / self.max_value, 0))

    @property
    def size_for(self, width):
        return int(self.percent * width / 100)

    def render_gui(self, x, y, width):
        color = draw.color_for_value(self.percent, self.colors)
        draw.progress_label(x, y, self.label, int(round(self._value, 0)), self.max_value, color)
        draw.progress(x, y + 1, width, self.percent, color, self.bkcolor)
