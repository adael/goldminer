from bearlibterminal import terminal
from goldminer.Rect import Rect

initial_screen_width = 120
initial_screen_height = 50

default_world_width = 512
default_world_height = 512

gui_width = 40
status_height = 10
screen_rect = Rect()
map_rect = Rect()
gui_rect = Rect()
status_rect = Rect()

hp_colors = ["darkest red", "darker red", "dark red", "red", "orange", "dark green", "green"]
water_colors = ["dark azure", "azure", "light azure"]
food_colors = ["darkest amber", "darker amber", "dark amber", "amber"]


def update():
    screen_rect.set_position(0, 0)
    screen_rect.set_size(terminal.state(terminal.TK_WIDTH),
                         terminal.state(terminal.TK_HEIGHT))

    map_rect.set_position(0, 0)
    map_rect.set_size(screen_rect.w - gui_width, screen_rect.h - status_height)

    gui_rect.set_position(map_rect.right, 0)
    gui_rect.set_size(gui_width, map_rect.height)

    status_rect.set_position(0, map_rect.bottom)
    status_rect.set_size(screen_rect.width, status_height)

    print("Screen: {}".format(screen_rect))
    print("Map: {}".format(map_rect))
    print("Gui: {}".format(gui_rect))
    print("Status: {}".format(status_rect))