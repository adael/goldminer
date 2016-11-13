import random
from enum import Enum

from bearlibterminal import terminal
from goldminer import game, settings, draw, texts
from goldminer.History import History
from goldminer.InventoryState import InventoryState
from goldminer.WorldGenerator import WorldGenerator
from goldminer.World import World, WorldMap
from goldminer.actor import Actor, Fighter
from goldminer.inventory import Inventory
from goldminer.gamepad import Gamepad, key_to_action


def create_player():
    player = Actor("Player", "@", "orange", 25, 25)
    player.fighter = Fighter(player)
    player.inventory = Inventory(player)
    player.history = History()
    return player


def create_world():
    seed = 1234
    worldmap = WorldMap(settings.default_world_width, settings.default_world_height)
    wgen = WorldGenerator()
    wgen.generate(worldmap, seed)
    player = create_player()
    world = World(worldmap, player)
    player.think(texts.im_back)
    return world


def movement_action_to_coords(action):
    if action == Gamepad.up:
        return 0, -1
    elif action == Gamepad.down:
        return 0, 1
    elif action == Gamepad.left:
        return -1, 0
    elif action == Gamepad.right:
        return 1, 0


class PlayingState:
    def __init__(self):
        random.seed(1234)
        self.world = create_world()
        self.show_inventory = False

    def handle_input(self, key):
        action = key_to_action(key)

        if not action:
            return False

        return self.handle_action(action) or self.handle_movement_action(action)

    def handle_action(self, action):
        if action == Gamepad.back:
            game.show_menu()
        elif action == Gamepad.lb:
            game.set_state(InventoryState(self.world.player.inventory))
        else:
            return False
        return True

    def handle_movement_action(self, action):
        r = movement_action_to_coords(action)
        if r is None:
            return False

        (x, y) = r
        self.world.actor_move(self.world.player, x, y)
        return True

    def move_player(self, x, y):
        self.world.player.move(x, y)

    def logic(self):
        pass

    def render(self):
        terminal.clear()
        draw.draw_game_layout()
        draw.draw_world(self.world)
        draw.draw_actor_stats(self.world.player)
        draw.draw_history(self.world.player.history)
        terminal.refresh()
