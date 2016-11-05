from goldminer import game
from bearlibterminal import terminal
from goldminer.controls import SelectBox, SelectItem


class MenuState:

    def __init__(self):
        self.selected_index = 0
        self.lst = SelectBox(10, 13, [
            SelectItem("Continue", active=game.can_continue()),
            SelectItem("New Game"),
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
                game.load_previus_game()
                game.show_game()
            elif item.label == "New Game":
                game.start_new_game()
                game.show_game()
            elif item.label == "Quit Game":
                game.end_game()

    def logic(self):
        pass

    def render(self):
        terminal.clear()

        terminal.color("yellow")
        terminal.print_(10, 10, ".*{Gold Miners}*.")
        terminal.print_(10, 11, "=================")

        self.lst.render()
        terminal.refresh()
