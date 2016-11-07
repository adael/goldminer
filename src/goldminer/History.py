from bearlibterminal import terminal
from goldminer.Rect import Rect


class History:

    def __init__(self, rect):
        self.rect = rect
        self.rollback = 0
        self.messages = []

    def add(self, text):
        self.messages.append(text)

    def clear(self):
        self.messages.clear()

    def render(self):
        x, y = self.rect.x, self.rect.bottom
        index = len(self.messages) - 1
        color = "white"
        while index >= 0 and y >= self.rect.y:
            s = "[color={}][bbox={}]".format(color, self.rect.width) + self.messages[index]
            terminal.print_(x, y, s)
            y -= terminal.measure(s)
            index -= 1
            color = "dark gray"
