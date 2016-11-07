from bearlibterminal import terminal
from goldminer import game, draw, settings
from goldminer.Rect import Rect


class InventoryState:
    def __init__(self, player):
        self.player = player

    def handle_input(self, key):
        if key in (terminal.TK_ESCAPE,):
            game.show_game()

    def logic(self):
        pass

    def render(self):
        terminal.color("azure")
        draw.window(settings.gui_rect, "Inventory window")
        terminal.refresh()

