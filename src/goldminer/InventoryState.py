from bearlibterminal import terminal

from goldminer import game, draw, settings


class InventoryState:

    def __init__(self, inventory):
        self.inventory = inventory

    def handle_input(self, key):
        if key in (terminal.TK_ESCAPE,):
            game.show_game()

    def logic(self):
        pass

    def render(self):
        draw.draw_inventory_state(self)

    def render_items(self):
        line_x = settings.gui_rect.x + 1
        line_y = settings.gui_rect.y + 3
        line_w = settings.gui_rect.width - 3
        item_w = 2

        for item in self.inventory:
            text_x = line_x + 4
            text_y = line_y + 1

            label = "[bbox={}][color=white]{}[/color]".format(line_w, item.description)
            cy = terminal.measure(label)

            draw.corners(line_x, line_y, line_x + item_w, line_y + item_w)
            terminal.put(line_x + 1, line_y + 1, item.char)
            terminal.print_(text_x, text_y, label)
            line_y += max(3, cy + 1)
