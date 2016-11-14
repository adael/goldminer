import random

from bearlibterminal import terminal

from goldminer import game, draw
from goldminer.WorldGenerator import create_world
from goldminer.controls import SelectBox, SelectItem


class GameState:
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
        self.world = create_world()
        self.show_inventory = False

    def handle_input(self, action):
        if action.is_back:
            game.show_menu()
        elif action.is_lb:
            game.set_state(InventoryState(self.world.player.inventory))
        elif action.is_movement:
            (x, y) = action.movement
            self.world.player_move(x, y)

    def logic(self):
        pass

    def render(self):
        terminal.clear()
        draw.draw_game_layout()
        draw.draw_world(self.world)
        draw.draw_actor_stats(self.world.player)
        draw.draw_history(self.world.player.history)
        terminal.refresh()


class MenuState(GameState):
    def __init__(self):
        super().__init__()
        self.selected_index = 0
        self.lst = SelectBox(10, 13, [
            SelectItem("Continue", active=game.can_continue()),
            SelectItem("New Game"),
            SelectItem("Options"),
            SelectItem("Quit Game"),
        ])

    def handle_input(self, action):
        if action.is_back:
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
                game.end_game()

    def show(self):
        self.lst.get_item_by_label("Continue").active = game.can_continue()
        pass

    def logic(self):
        pass

    def render(self):
        draw.draw_menu_state(self)


class MenuOptionsState(GameState):
    def __init__(self):
        super().__init__()
        self.lst = SelectBox(30, 16, [
            SelectItem("Normal"),
            SelectItem("Big"),
            SelectItem("Bigger"),
        ])

    def handle_input(self, action):
        if action.is_back:
            game.show_menu()
        else:
            self.lst.handle_input(action)

    def show(self):
        pass

    def logic(self):
        pass

    def render(self):
        draw.draw_menu_option_state(self)


class InventoryState(GameState):
    def __init__(self, inventory):
        super().__init__()
        self.inventory = inventory

    def handle_input(self, action):
        if action.is_back:
            game.show_game()

    def logic(self):
        pass