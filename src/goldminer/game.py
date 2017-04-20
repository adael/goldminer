import time

from bearlibterminal import terminal

from goldminer import settings, filesave
from goldminer.gamepad import GamePadAction
from goldminer.pgc import create_world
from goldminer.states import PlayingState, MenuState, StateManager

running = True
FPS = 30
manager = StateManager()
running_states = {}


def can_continue():
    return game_started() or filesave.can_load()


def game_started():
    return 'game' in running_states


def enter_state(new_state):
    manager.enter_state(new_state)


def leave_state():
    manager.leave_state()


def get_game_state() -> PlayingState:
    if 'game' not in running_states:
        start_new_game()
    return running_states['game']


def start_new_game():
    state = PlayingState()
    state.enter_world(create_world())
    running_states['game'] = state


def get_menu_state() -> MenuState:
    if 'menu' not in running_states:
        running_states['menu'] = MenuState()
    return running_states['menu']


def show_menu():
    manager.replace_states(get_menu_state())


def show_game():
    manager.replace_states(get_game_state())


def load_previous_game():
    if not game_started():
        load()


def load():
    get_game_state().worlds = filesave.load_world()


def save():
    filesave.save_world(get_game_state().worlds)


def end_game():
    manager.clear_states()


def convert_to_action(key):
            
    if key == terminal.TK_RESIZED:
        settings.update()
    elif key == terminal.TK_CLOSE:
        end_game()

    return GamePadAction(key)


def game_loop():
    while manager.current_state:
        if manager.current_state.automatic_mode:
            automatic_loop()
        else:
            manager.current_state.logic()
            manager.current_state.render()
            manager.current_state.handle_input(convert_to_action(terminal.read()))


def automatic_loop():
    ticks = 0
    while manager.current_state and manager.current_state.automatic_mode:
        if ticks % FPS == 0:
            manager.current_state.logic()
            manager.current_state.render()
            ticks = 0

        if terminal.has_input():
            key = terminal.read()
            manager.current_state.handle_input(convert_to_action(key))

        time.sleep(1 / FPS)
        ticks += 1


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
