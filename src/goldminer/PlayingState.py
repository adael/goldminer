from bearlibterminal import terminal
from goldminer import game
from goldminer.WorldMap import WorldMap
from goldminer.Player import Player, PlayerGui


class PlayingState:
    def __init__(self):
        self.world = WorldMap(game.MAP_WIDTH, game.MAP_HEIGHT)
        self.player = Player(25, 25)
        self.world.add(self.player)
        self.player_gui = PlayerGui(self.player)

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
        elif key in (terminal.TK_KP_PLUS, ):
            self.player.heal(1)
        elif key in (terminal.TK_KP_MINUS, ):
            self.player.heal(-1)

    def logic(self):
        pass

    def render(self):
        terminal.clear()
        self.world.render()
        self.player.render()
        self.player_gui.render()
        terminal.refresh()
