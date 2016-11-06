from bearlibterminal import terminal
from goldminer.MenuState import MenuState
from goldminer.PlayingState import PlayingState

# size of window
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 50

# size of map
MAP_WIDTH = 80
MAP_HEIGHT = 43

running = True
state = None
states = {}


def can_continue():
    return 'game' in states


def show_menu():
    global state
    state = MenuState()


def show_game():
    global state
    if 'game' not in states:
        states['game'] = PlayingState()
    state = states['game']


def load_previous_game():
    pass


def start_new_game():
    states['game'] = PlayingState()


def end_game():
    global running
    running = False


def start():
    try:
        terminal.open()
        terminal.set("window: size=120x50; window.title='Gold Miners';" +
                     "font: res/proggy/ProggySquare.ttf, size=12;" +
                     "input: filter=[keyboard],alt-functions=false;")

        show_menu()
        while running:
            state.logic()
            state.render()
            key = terminal.read()
            state.handle_input(key)

    finally:
        print("Closing...")
        terminal.close()
