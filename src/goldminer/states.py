import random

from goldminer import game, draw, music
from goldminer.actor import Inventory
from goldminer.gamepad import GamePadAction
from goldminer.ui import SelectBox, SelectItem, Separator

class GameState:
    
    def __init__(self):
        self.automatic_mode = False
    
    def enter(self):
        pass
    
    def leave(self):
        pass
    
    def logic(self):
        pass
    
    def render(self):
        pass
    
    def handle_input(self, action):
        pass


class StateManager:
    def __init__(self):
        self.states = []
    
    @property
    def current_state(self):
        if self.states:
            return self.states[-1]
    
    def enter_state(self, state):
        self.states.append(state)
        state.enter()
    
    def leave_state(self):
        if len(self.states) > 1:
            state = self.states.pop()
            state.leave()
        else:
            raise Exception("It's the last state")
    
    def clear_states(self):
        self.states.clear()
    
    def replace_states(self, state):
        self.clear_states()
        self.enter_state(state)


class MenuState(GameState):
    def __init__(self):
        super().__init__()
        self.lst = SelectBox([
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
        
        self.check_selected_item()
    
    def enter(self):
        music.play()
        self.lst.items[0].active = game.can_continue()
        # self.lst.items[1].active = not game.can_continue()
    
    def leave(self):
        music.stop()
    
    def render(self):
        draw.draw_menu_state(self.lst)
    
    def check_selected_item(self):
        if self.lst.is_selected():
            item = self.lst.item_selected()
            if item.label == "Continue":
                game.load_previous_game()
                game.show_game()
            elif item.label == "New Game":
                game.start_new_game()
                game.show_game()
            elif item.label == "Options":
                game.enter_state(MenuOptionsState())
            elif item.label == "Quit Game":
                if game.game_started():
                    game.save()
                game.end_game()


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
                game.enter_state(InventoryState(self.world.player.inventory))
            elif action.is_movement:
                (x, y) = action.movement
                self.world.player_move(x, y)
    
    def logic(self):
        self.world.logic()
        self.automatic_mode = self.world.player.resting
    
    def render(self):
        draw.draw_world(self.world)
    
    def enter_world(self, world):
        self.worlds.append(world)
    
    def leave_world(self):
        if self.worlds:
            self.worlds.pop()
            self.world.restore_player_position()


class MenuOptionsState(GameState):
    def __init__(self):
        super().__init__()
        self.lst = SelectBox([
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
        self.selected_index = 0
    
    @property
    def selected_item(self):
        if self.inventory.has(self.selected_index):
            return self.inventory.get(self.selected_index)
    
    def handle_input(self, action: GamePadAction):
        if action.is_back:
            game.show_game()
        elif action.is_up:
            self.up()
        elif action.is_down:
            self.down()
        elif action.is_a:
            item = self.selected_item
            if item:
                game.enter_state(ViewItemState(self.inventory, self.selected_item))
        elif action.is_b:
            pass
    
    def up(self):
        if self.selected_index > 0:
            self.selected_index -= 1
    
    def down(self):
        if self.selected_index < len(self.inventory.items) - 1:
            self.selected_index += 1
    
    def render(self):
        draw.draw_inventory_window(self.inventory, self.selected_index)


class ViewItemState(GameState):

    def __init__(self, inventory, item):
        super().__init__()
        self.inventory = inventory
        self.item = item
        self.selected_action = None
        self.lst = SelectBox([
            SelectItem("Examine"),
            SelectItem("Study"),
            SelectItem("Drop"),
            Separator(),
            SelectItem("Build", active=False),
            SelectItem("Use", active=False),
            SelectItem("Eat", active=False),
            SelectItem("Deconstruct", active=False),
            SelectItem("Throw", active=False),
        ])

    def enter(self):
        self.selected_action = None
        pass
    
    def handle_input(self, action: GamePadAction):
        if action.is_back:
            game.leave_state()
        else:
            self.lst.handle_input(action)
    
    def logic(self):
        self.check_selected_item()
    
    def render(self):
        draw.draw_view_item_window(self.lst, self.item)
    
    def check_selected_item(self):
        if self.lst.is_selected():
            item = self.lst.item_selected()
            if item.label == "Examine":
                pass
            elif item.label == "Study":
                pass
            elif item.label == "Drop":
                self.inventory.drop(self.item)
                game.leave_state()
