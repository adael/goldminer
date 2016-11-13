from bearlibterminal import terminal

from goldminer import settings, texts


class Border:
    def __init__(self, top, bottom, left, right, topLeft, topRight, bottomLeft, bottomRight):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


double_border = Border(
    top=0x2550,
    bottom=0x2550,
    left=0x2551,
    right=0x2551,
    topLeft=0x2554,
    topRight=0x2557,
    bottomLeft=0x255A,
    bottomRight=0x255D
)

single_border = Border(
    top=0x2500,
    bottom=0x2500,
    left=0x2502,
    right=0x2502,
    topLeft=0x250C,
    topRight=0x2510,
    bottomLeft=0x2514,
    bottomRight=0x2518
)


def color_for_value(value, colors=None):
    if not colors:
        colors = ["dark red", "red", "orange", "yellow", "dark green", "green"]

    ncolors = len(colors) - 1
    percent = round(value * ncolors / 100, 0)
    index = int(min(ncolors, max(0, percent)))
    return colors[index]


def double_line(x, y, width):
    line(x, y, width, "[U+2550]")


def line(x, y, width, code="[U+2500]"):
    terminal.print_(x, y, code * width)


def progress_label(x, y, label, value, max_value, color):
    label += " [color={}]{}[color=white]/{}".format(color, value, max_value)
    terminal.print_(x, y, label)


def progress(x, y, width, percent, color, bkcolor="dark gray"):
    fill_width = int(percent * width / 100)
    terminal.print_(x, y, "[bkcolor={}]".format(bkcolor) + (" " * width))
    terminal.print_(x, y, "[bkcolor={}]".format(color) + (" " * fill_width))


def rect(rect_, border=double_border):
    box(rect_.left, rect_.top, rect_.right - 1, rect_.bottom - 1, border)


def box(x1, y1, x2, y2, border=double_border):
    for cx in range(x1, x2):
        terminal.put(cx, y1, border.top)
        terminal.put(cx, y2, border.bottom)

    for cy in range(y1, y2):
        terminal.put(x1, cy, border.left)
        terminal.put(x2, cy, border.right)

    terminal.put(x1, y1, border.topLeft)
    terminal.put(x2, y1, border.topRight)
    terminal.put(x2, y2, border.bottomRight)
    terminal.put(x1, y2, border.bottomLeft)


def corners(x1, y1, x2, y2, border=single_border):
    terminal.put(x1, y1, border.topLeft)
    terminal.put(x2, y1, border.topRight)
    terminal.put(x2, y2, border.bottomRight)
    terminal.put(x1, y2, border.bottomLeft)


def window(rect_, caption):
    terminal.clear_area(rect_.x, rect_.y, rect_.width, rect_.height)
    line(rect_.x + 1, rect_.y + 2, rect_.width - 2, "[U+2594]")
    rect(rect_)
    terminal.print_(rect_.center_x, rect_.y + 1, "[align=center]" + caption)


def draw_selectbox(control):
    terminal.clear_area(control.x, control.y, control.w, control.h)
    index = 0
    y = 0
    for item in control.items:

        color = "white"
        if item.active and control.item_focused_index == index:
            color = "yellow"
        elif not item.active:
            color = "gray"

        box = "[bbox={}]".format(control.w - control.padding_left)
        height = terminal.measure(box + item.label)
        terminal.color(color)
        terminal.print_(control.x + 2, control.y + y, box + item.label)
        if index == control.item_focused_index:
            terminal.print_(control.x, control.y + y, "[color=lightblue]>")

        y += height
        index += 1


# PlayingState

def draw_game_layout():
    terminal.color("azure")
    rect(settings.screen_rect)
    rect(settings.map_rect)
    rect(settings.gui_rect)
    rect(settings.status_rect)


def draw_world(world):
    for x, y in settings.map_rect:
        px, py = world.camera.camera_to_map(x, y)
        draw_tile(world.tile(px, py), x, y)

    for actor in world.actors:
        x, y = world.camera.map_to_camera(actor.x, actor.y)
        draw_actor(actor, x, y)

    x, y = world.camera.map_to_camera(world.player.x, world.player.y)
    draw_player(world.player, x, y)


def draw_tile(tile, x, y):
    if tile.resource:
        draw_entity(tile.resource, x, y)
    else:
        draw_entity(tile, x, y)


def draw_actor(actor, x, y):
    draw_entity(actor, x, y)


def draw_player(player, x, y):
    draw_entity(player, x, y)


def draw_entity(entity, x, y):
    terminal.color(entity.color)
    terminal.put(x, y, entity.char)


def draw_actor_stats(actor):
    r = settings.gui_rect
    terminal.color('azure')

    rect(r)

    x = r.left + 2
    y = r.top + 2
    width = r.width - 4

    draw_gui_stat(actor.fighter.hp, x, y, width, settings.hp_colors)

    y += 3
    draw_gui_stat(actor.fighter.water, x, y, width, settings.water_colors)

    y += 3
    draw_gui_stat(actor.fighter.food, x, y, width, settings.food_colors)

    y += 4
    terminal.color("#AA6939")
    terminal.print_(x, y, "Inventory:")
    double_line(x, y + 1, width)
    draw_ingame_inventory_items(actor.inventory, x, y + 3, width)


def draw_gui_stat(stat, x, y, width, colors, bkcolor="dark gray"):
    color = color_for_value(stat.percent, colors)
    progress_label(x, y, stat.label, int(round(stat.value, 0)), stat.max_value, color)
    progress(x, y + 1, width, stat.percent, color, bkcolor)


def draw_ingame_inventory_items(inventory, x, y, width):
    items = ["[color={}]{}[/color]".format(item.color, item.char) for item in inventory.items]
    s = "".join(items)
    str_items = s + ("[color=white][U+0095] [/color]" * (inventory.max_size - len(items)))

    terminal.print_(x, y, "[bbox={}]".format(width) + str_items)


def draw_history(history):
    r = settings.status_rect
    x, y = r.x, r.bottom
    index = len(history.messages) - 1
    color = "white"
    while index >= 0 and y >= r.y:
        s = "[color={}][bbox={}]{}".format(color, r.width, history.messages[index])
        terminal.print_(x, y, s)
        y -= terminal.measure(s)
        index -= 1
        color = "dark gray"


# MenuState
def draw_menu_state(state):
    terminal.clear()
    caption = ".*{Gold Miner}*."
    terminal.color("yellow")
    terminal.print_(10, 10, caption)
    double_line(10, 11, len(caption))
    draw_selectbox(state.lst)
    terminal.refresh()


def draw_menu_option_state(state):
    terminal.clear_area(30, 14, 60, 30)
    terminal.color("yellow")
    terminal.print_(30, 14, "Screen size")
    double_line(30, 15, len("Screen size"))
    draw_selectbox(state.lst)
    terminal.refresh()


def draw_inventory_state(state):
    terminal.color("azure")
    window(settings.gui_rect, "Inventory window")

    if state.inventory.is_empty():
        inner_width = settings.gui_rect.width - 2
        terminal.print_(settings.gui_rect.x + 1, settings.gui_rect.y + 3,
                        "[bbox={}][color=teal]{}[/color]".format(inner_width, texts.inventory_is_empty()))
    else:
        state.render_items()

    terminal.refresh()
