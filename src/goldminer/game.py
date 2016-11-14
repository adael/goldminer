import time

from bearlibterminal import terminal

from goldminer import settings
from goldminer.gamepad import GamePadAction
from goldminer.states import PlayingState, MenuState

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

# TODO: Make a smooth eventloop
# TODO: While the player is resting, the events must occurs at every second.
# TODO: While the player is awake, the events must occurs at every keystroke.
def process_input():

    if state.wait_for_input or terminal.has_input():
        key = terminal.read()
    else:
        key = None

    if key == terminal.TK_RESIZED:
        settings.update()
        return
    elif key == terminal.TK_CLOSE:
        end_game()
        return

    action = GamePadAction(key)
    state.handle_input(action)

    if not state.wait_for_input:
        time.sleep(1/60)


def game_loop():
    while running:
        state.logic()
        state.render()
        process_input()


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
        game_loop()

    finally:
        print("Closing...")
        terminal.close()

        # non blocking smaple:
        # sleep_time = 1.0 / 60
        # while running:
        #     if terminal.has_input():
        #         key = terminal.read()
        #         state.handle_input(key)
        #     state.logic()
        #     state.render()
        #
        #     time.sleep(sleep_time)
