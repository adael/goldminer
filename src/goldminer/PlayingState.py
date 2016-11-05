from goldminer import game
from goldminer.WorldMap import WorldMap
from bearlibterminal import terminal


class PlayingState:

    def __init__(self):
        self.world_map = WorldMap(game.MAP_WIDTH, game.MAP_HEIGHT)

    def handle_input(self, key):
        if key == terminal.TK_ESCAPE:
            game.show_menu()

    def logic(self):
        pass

    def render(self):
        terminal.clear()
        self.world_map.render()
        terminal.refresh()
