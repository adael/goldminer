import time

from bearlibterminal import terminal

from goldminer import settings, filesave
from goldminer.gamepad import GamePadAction
from goldminer.pgc import create_world
from goldminer.states import PlayingState, MenuState

running = True
state = None
states = {}
FPS = 30


def can_continue():
    return game_started() or filesave.can_load()


def game_started():
    return 'game' in states


def set_state(new_state):
    global state
    state = new_state
    state.show()


def get_game_state() -> PlayingState:
    if 'game' not in states:
        start_new_game()
    return states['game']


def get_menu_state():
    if 'menu' not in states:
        states['menu'] = MenuState()
    return states['menu']


def show_menu():
    set_state(get_menu_state())


def show_game():
    set_state(get_game_state())


def load_previous_game():
    if not game_started():
        load()


def load():
    get_game_state().worlds = filesave.load_world()


def save():
    filesave.save_world(get_game_state().worlds)


def start_new_game():
    states['game'] = PlayingState()
    states['game'].enter_world(create_world())


def end_game():
    global running
    running = False


def handle_event(key):
    if key == terminal.TK_RESIZED:
        settings.update()
        return
    elif key == terminal.TK_CLOSE:
        end_game()
        return

    action = GamePadAction(key)
    state.handle_input(action)


def automatic_loop():
    ticks = 0
    while not state.wait_for_input:
        if ticks % FPS == 0:
            state.logic()
            state.render()
            ticks = 0

        if terminal.has_input():
            key = terminal.read()
            handle_event(key)

        time.sleep(1 / FPS)
        ticks += 1


def logic():
    state.logic()


def render():
    state.render()


def game_loop():
    while running:
        if state.wait_for_input:
            state.logic()
            state.render()
            handle_event(terminal.read())
        else:
            automatic_loop()


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
