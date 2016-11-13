import random
from bearlibterminal import terminal
from goldminer import game, settings, draw
from goldminer.History import History
from goldminer.InventoryState import InventoryState
from goldminer.Rect import Rect
from goldminer.WorldMap import WorldMap
from goldminer.Actor import Actor, Fighter
from goldminer.Inventory import Inventory


def create_player():
    player = Actor("Player", "@", "orange", 25, 25)
    player.fighter = Fighter(player)
    player.inventory = Inventory(player)
    return player


def create_world():
    history = History()
    player = create_player()
    world = WorldMap(512, 512, player, history)
    player.say("Hello, I'm back!")
    return world


def handle_movement(key):
    if key in (terminal.TK_UP, terminal.TK_KP_8):
        return 0, -1
    elif key in (terminal.TK_DOWN, terminal.TK_KP_2):
        return 0, 1
    elif key in (terminal.TK_LEFT, terminal.TK_KP_4):
        return -1, 0
    elif key in (terminal.TK_RIGHT, terminal.TK_KP_6):
        return 1, 0


class PlayingState:
    def __init__(self):
        random.seed(1234)
        self.world = create_world()

        self.show_inventory = False

    def handle_input(self, key):
        if not self.handle_command(key):
            (x, y) = handle_movement(key)
            if x is not None:
                self.world.actor_move(self.world.player, x, y)

    def handle_command(self, key):
        if key == terminal.TK_ESCAPE:
            game.show_menu()
        elif key in (terminal.TK_I,):
            game.set_state(InventoryState(self.world.player.inventory))
        elif key in (terminal.TK_KP_PLUS,):
            self.world.player.heal(1)
        elif key in (terminal.TK_KP_MINUS,):
            self.world.player.heal(-1)
        elif key in (terminal.TK_S,):
            self.world.player.say("What do you want?")
        else:
            return False
        return True

    def move_player(self, x, y):
        self.world.player.move(x, y)

    def logic(self):
        pass

    def render(self):
        terminal.clear()
        draw.playing_layout()
        terminal.color("white")
        draw.draw_world(self.world)
        draw.render_actor_stats(self.world.player)
        self.world.history.rendher()
        terminal.refresh()
