import random
from bearlibterminal import terminal
from goldminer import game, settings, draw
from goldminer.History import History
from goldminer.InventoryState import InventoryState
from goldminer.Rect import Rect
from goldminer.WorldMap import WorldMap
from goldminer.Player import Player, PlayerGui


class PlayingState:
    def __init__(self):
        self.history = History(settings.status_rect)
        r = settings.map_rect
        random.seed(1234)
        self.world = WorldMap(Rect(r.x + 1, r.y + 1, r.width - 2, r.height - 2), self.history)
        self.player = Player(25, 25)
        self.world.add(self.player)
        self.player_gui = PlayerGui(self.player)
        self.player.say("Hello, I'm back!")
        self.show_inventory = False

    def handle_input(self, key):
        if key == terminal.TK_ESCAPE:
            game.show_menu()
        elif key in (terminal.TK_UP, terminal.TK_KP_8):
            self.player.move_up()
        elif key in (terminal.TK_DOWN, terminal.TK_KP_2):
            self.player.move_down()
        elif key in (terminal.TK_LEFT, terminal.TK_KP_4):
            self.player.move_left()
        elif key in (terminal.TK_RIGHT, terminal.TK_KP_6):
            self.player.move_right()
        elif key in (terminal.TK_KP_PLUS,):
            self.player.heal(1)
        elif key in (terminal.TK_KP_MINUS,):
            self.player.heal(-1)
        elif key in (terminal.TK_S,):
            self.player.say("What do you want?")
        elif key in (terminal.TK_I,):
            game.set_state(InventoryState(self.player))

    def logic(self):
        pass

    def render(self):
        terminal.clear()
        terminal.color("azure")
        draw.rect(settings.screen_rect)
        draw.rect(settings.map_rect)
        draw.rect(settings.gui_rect)
        draw.rect(settings.status_rect)
        terminal.color("white")
        self.world.render()
        self.player.render()
        self.player_gui.render()
        self.history.render()
        terminal.refresh()
