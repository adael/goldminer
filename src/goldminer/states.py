import random

from goldminer import game, draw
from goldminer.controls import SelectBox, SelectItem
from goldminer.gamepad import GamePadAction
from goldminer.inventory import Inventory


class GameState:
    def __init__(self):
        self.wait_for_input = True

    def show(self):
        pass

    def hide(self):
        pass

    def logic(self):
        pass

    def render(self):
        pass

    def handle_input(self, action):
        pass


class PlayingState(GameState):
    def __init__(self):
        super().__init__()
        random.seed(1234)
        self.worlds = []
        self.show_inventory = False

    @property
    def world(self):
        return self.worlds[-1]

    def handle_input(self, action):
        if action.is_back:
            game.show_menu()
            return

        if not self.world.player.dead and not self.world.player.resting:
            if action.is_lb:
                game.set_state(InventoryState(self.world.player.inventory))
            elif action.is_movement:
                (x, y) = action.movement
                self.world.player_move(x, y)

    def logic(self):
        self.world.logic()
        self.wait_for_input = not self.world.player.resting

    def render(self):
        draw.draw_world(self.world)

    def enter_world(self, world):
        self.worlds.append(world)

    def leave_world(self):
        if self.worlds:
            self.worlds.pop()
            self.world.restore_player_position()


class MenuState(GameState):
    def __init__(self):
        super().__init__()
        self.selected_index = 0
        self.lst = SelectBox(10, 13, [
            SelectItem("Continue", active=game.can_continue()),
            SelectItem("New Game"),
            SelectItem("", active=False),
            SelectItem("Options"),
            SelectItem("Quit Game"),
        ])

    def handle_input(self, action: GamePadAction):
        if action.is_back:
            if game.can_continue():
                game.show_game()
            else:
                game.end_game()
        else:
            self.lst.handle_input(action)

        if self.lst.is_selected():
            item = self.lst.item_selected()
            if item.label == "Continue":
                game.load_previous_game()
                game.show_game()
            elif item.label == "New Game":
                game.start_new_game()
                game.show_game()
            elif item.label == "Options":
                game.set_state(MenuOptionsState())
            elif item.label == "Quit Game":
                if game.game_started():
                    game.save()
                game.end_game()

    def show(self):
        self.lst.items[0].active = game.can_continue()
        self.lst.items[1].active = not game.can_continue()

    def render(self):
        draw.draw_menu_state(self.lst)


class MenuOptionsState(GameState):
    def __init__(self):
        super().__init__()
        self.lst = SelectBox(30, 16, [
            SelectItem("Normal"),
            SelectItem("Big"),
            SelectItem("Bigger"),
        ])

    def handle_input(self, action: GamePadAction):
        if action.is_back:
            game.show_menu()
        else:
            self.lst.handle_input(action)

    def render(self):
        draw.draw_menu_option_state(self.lst)


class InventoryState(GameState):
    def __init__(self, inventory: Inventory):
        super().__init__()
        self.inventory = inventory

    def handle_input(self, action: GamePadAction):
        if action.is_back:
            game.show_game()

    def render(self):
        draw.draw_inventory_window(self.inventory)
