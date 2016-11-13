from bearlibterminal import terminal

from goldminer import draw
from goldminer import game
from goldminer.controls import SelectBox, SelectItem


class MenuState:
    def __init__(self):
        self.selected_index = 0
        self.lst = SelectBox(10, 13, [
            SelectItem("Continue", active=game.can_continue()),
            SelectItem("New Game"),
            SelectItem("Options"),
            SelectItem("Quit Game"),
        ])

    def handle_input(self, key):
        if key == terminal.TK_ESCAPE:
            game.end_game()
        else:
            self.lst.handle_input(key)

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

    def logic(self):
        pass

    def render(self):
        draw.draw_menu_state(self)


class MenuOptionsState:
    def __init__(self):
        self.lst = SelectBox(30, 16, [
            SelectItem("Normal"),
            SelectItem("Big"),
            SelectItem("Bigger"),
        ])

    def handle_input(self, key):
        if key == terminal.TK_ESCAPE:
            game.show_menu()
        else:
            self.lst.handle_input(key)

    def logic(self):
        pass

    def render(self):
        draw.draw_menu_option_state(self)
