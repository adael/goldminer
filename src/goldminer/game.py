from bearlibterminal import terminal

from goldminer import settings
from goldminer.MenuState import MenuState
from goldminer.PlayingState import PlayingState

running = True
state = None
states = {}


def can_continue():
    return 'game' in states


def set_state(new_state):
    global state
    state = new_state


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
        font = "res/proggy/ProggySquare.ttf"
        #font = "res/DejaVuSansMono.ttf"
        font_size = 12

        terminal.open()
        terminal.set("window: size={};".format(size) +
                     "window.title='{}';".format(title) +
                     "font: {}, size={};".format(font, font_size) +
                     "input: filter=[keyboard],alt-functions=false;")

        # terminal.set("0xE000: res/img/tree.png, size=12x12, align=center")

        settings.update()

        show_menu()
        while running:
            state.logic()
            state.render()
            key = terminal.read()
            state.handle_input(key)

    finally:
        print("Closing...")
        terminal.close()
