from bearlibterminal import terminal

from goldminer import settings
from goldminer.states import PlayingState, MenuState
from goldminer.gamepad import GamePadAction


running = True
state = None
states = {}


def can_continue():
    return 'game' in states


def set_state(new_state):
    global state
    state = new_state
    state.show()


def show_menu():
    if 'menu' not in states:
        states['menu'] = MenuState()
    set_state(states['menu'])


def show_game():
    if 'game' not in states:
        states['game'] = PlayingState()
    set_state(states['game'])


def load_previous_game():
    pass


def start_new_game():
    states['game'] = PlayingState()


def end_game():
    global running
    running = False


def start():
    try:
        title = "Gold Miner"
        size = "{}x{}".format(settings.initial_screen_width, settings.initial_screen_height)
        minimun_size = size

        font = "res/proggy/ProggySquare.ttf"
        font_size = 12
        # cell_size = "7x11"
        cell_size = "auto"

        resizeable = "true" if settings.resizeable else "false"
        full_screen = "true" if settings.full_screen else "false"

        terminal.open()
        terminal.set("window.size={}".format(size))
        terminal.set("window.minimun-size={}".format(minimun_size))
        terminal.set("window.resizeable={}".format(resizeable))
        terminal.set("window.fullscreen={}".format(full_screen))
        terminal.set("window.cellsize={}".format(cell_size))
        terminal.set("window.title='{}'".format(title))
        terminal.set("font: {}, size={}".format(font, font_size))
        terminal.set("input: filter=[keyboard],alt-functions=false")

        settings.update()

        show_menu()
        while running:
            state.logic()
            state.render()
            key = terminal.read()

            if key == terminal.TK_RESIZED:
                settings.update()
            elif key == terminal.TK_CLOSE:
                end_game()
                break

            action = GamePadAction(key)
            state.handle_input(action)

    finally:
        print("Closing...")
        terminal.close()
