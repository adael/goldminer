from bearlibterminal import terminal

from goldminer import settings, texts, colors
from goldminer.History import History
from goldminer.inventory import Inventory


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


color_stack = []

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


def push_colors():
    color_stack.append((terminal.state(terminal.TK_COLOR), terminal.state(terminal.TK_BKCOLOR)))


def pop_colors():
    (fg, bg) = color_stack.pop()
    terminal.color(fg)
    terminal.bkcolor(bg)


def color_for_value(value, colors=None):
    if not colors:
        colors = ["dark red", "red", "orange", "yellow", "dark green", "green"]

    ncolors = len(colors) - 1
    percent = round(value * ncolors / 100, 0)
    index = int(min(ncolors, max(0, percent)))
    return colors[index]


def draw_double_line(x, y, width):
    draw_line(x, y, width, "[U+2550]")


def draw_line(x, y, width, code="[U+2500]"):
    terminal.print_(x, y, code * width)


def draw_progress_label(x, y, label, value, max_value, color):
    label += " [color={}]{}[color=white]/{}".format(color, value, max_value)
    terminal.print_(x, y, label)


def draw_progress(x, y, width, percent, color, bkcolor="dark gray"):
    fill_width = int(percent * width / 100)
    terminal.print_(x, y, "[bkcolor={}]".format(bkcolor) + (" " * width))
    terminal.print_(x, y, "[bkcolor={}]".format(color) + (" " * fill_width))


def draw_rect(rect_, border=double_border):
    draw_box(rect_.left, rect_.top, rect_.right - 1, rect_.bottom - 1, border)


def draw_box(x1, y1, x2, y2, border=double_border):
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


def draw_corners(x1, y1, x2, y2, border=single_border):
    terminal.put(x1, y1, border.topLeft)
    terminal.put(x2, y1, border.topRight)
    terminal.put(x2, y2, border.bottomRight)
    terminal.put(x1, y2, border.bottomLeft)


def draw_window(rect_, caption, color="white", bkcolor="black"):
    push_colors()
    terminal.color(color)
    terminal.bkcolor(bkcolor)
    terminal.clear_area(rect_.x, rect_.y, rect_.width, rect_.height)
    draw_line(rect_.x + 1, rect_.y + 2, rect_.width - 2, "[U+2594]")
    draw_rect(rect_)
    terminal.print_(rect_.center_x, rect_.y + 1, "[align=center]" + caption)
    pop_colors()


def draw_select_box(control):
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
    terminal.color(colors.beige)
    draw_rect(settings.screen_rect)
    draw_rect(settings.map_window_rect)
    draw_rect(settings.gui_rect)
    draw_rect(settings.status_rect)


def draw_world(world):
    terminal.clear()
    draw_game_layout()
    draw_world_map(world.camera, world.world_map)
    draw_world_actors(world.camera, world.actors)
    draw_world_player(world.camera, world.player)
    draw_actor_stats(world.player)
    draw_history(world.player.history)
    world.player.history.trim()
    terminal.refresh()


def draw_world_map(camera, world_map):
    for x, y in settings.map_rect:
        px, py = camera.camera_to_map(x, y)
        if world_map.inside_map(px, py):
            draw_tile(world_map.tile(px, py), x, y)


def draw_world_actors(camera, actors):
    for actor in actors:
        x, y = camera.map_to_camera(actor.x, actor.y)
        draw_actor(actor, x, y)


def draw_world_player(camera, player):
    x, y = camera.map_to_camera(player.x, player.y)
    draw_player(player, x, y)


def draw_tile(tile, x, y):
    if tile.door:
        draw_door(tile.door, x, y)
    elif tile.resource:
        draw_resource(tile.resource, x, y)
    else:
        draw_entity(tile, x, y)


def draw_door(door, x, y):
    char = "+" if door.closed else "/"
    terminal.color(door.color)
    terminal.put(x, y, char)


def draw_resource(resource, x, y):
    draw_entity(resource, x, y)


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

    draw_rect(r)

    x = r.left + 2
    y = r.top + 2
    width = r.width - 4

    draw_gui_stat(actor.fighter.hp, x, y, width, settings.hp_colors)

    y += 3
    draw_gui_stat(actor.fighter.water, x, y, width, settings.water_colors)

    y += 3
    draw_gui_stat(actor.fighter.food, x, y, width, settings.food_colors)

    y += 3
    draw_gui_stat(actor.fighter.fatigue, x, y, width, colors.get_bright_range(colors.brown))

    y += 3
    terminal.print_(x, y, "Position: {}x{}".format(actor.x, actor.y))

    y += 4
    terminal.color("#AA6939")
    terminal.print_(x, y, "Inventory:")
    draw_double_line(x, y + 1, width)
    draw_ingame_inventory_items(actor.inventory, x, y + 3, width)


def draw_gui_stat(stat, x, y, width, colors, bkcolor="dark gray"):
    color = color_for_value(stat.percent, colors)
    draw_progress_label(x, y, stat.label, int(round(stat.value, 0)), stat.max_value, color)
    draw_progress(x, y + 1, width, stat.percent, color, bkcolor)


def draw_ingame_inventory_items(inventory: Inventory, x: int, y: int, width: int):
    """

    :type inventory: Inventory
    """
    items = ["[color={}]{} [/color]".format(item.color, item.char) for item in inventory.items]
    s = "".join(items)
    str_items = s + ("[color=#404040]· [/color]" * (inventory.capacity - len(items)))

    terminal.print_(x, y, "[bbox={}]".format(width) + str_items)


def draw_history(history: History):
    """

    :type history: History
    """
    r = settings.status_rect
    x, y = r.x + 1, r.bottom - 2
    color = "white"
    for msgtime, msg in reversed(history.messages):
        if y <= r.y:
            return
        s = "{} [color={}][bbox={}]{}".format(msgtime.strftime("%H:%M:%S"), color, r.width, msg)
        terminal.print_(x, y, s)
        y -= terminal.measure(s)
        color = "dark gray"


# MenuState
def draw_menu_state(lst):
    terminal.clear()
    caption = ".*{Gold Miner}*."
    terminal.color("yellow")
    terminal.print_(10, 10, caption)
    draw_double_line(10, 11, len(caption))
    draw_select_box(lst)
    terminal.refresh()


def draw_menu_option_state(lst):
    terminal.clear_area(30, 14, 60, 30)
    terminal.color("yellow")
    terminal.print_(30, 14, "Screen size")
    draw_double_line(30, 15, len("Screen size"))
    draw_select_box(lst)
    terminal.refresh()


def draw_inventory_window(inventory: Inventory, selected_index):
    draw_window(settings.gui_rect, "Inventory window", colors.darkslategray, colors.night)

    if inventory.is_empty:
        inner_width = settings.gui_rect.width - 2
        terminal.print_(settings.gui_rect.x + 1, settings.gui_rect.y + 3,
                        "[bbox={}][color=teal]{}[/color]".format(inner_width, texts.inventory_is_empty))
    else:
        draw_inventory_state_items(inventory.items, selected_index)

    terminal.refresh()


# Inventory state
def draw_inventory_state_items(items, selected_index):
    line_x = settings.gui_rect.x + 1
    line_y = settings.gui_rect.y + 3
    line_w = settings.gui_rect.width - 3
    item_w = 2
    item_h = 3

    index = 0
    for item in items:
        text_x = line_x + 4
        text_y = line_y + 1
        bkcolor = colors.darkslategray if index == selected_index else colors.night
        label = "[bbox={}][color=white]{}[/color]".format(line_w, item.description)
        cy = terminal.measure(label)

        # draw icon
        terminal.bkcolor(colors.night)
        terminal.color("white")
        draw_corners(line_x, line_y, line_x + item_w, line_y + item_w)
        terminal.color(item.color)
        terminal.put(line_x + 1, line_y + 1, item.char)

        # draw highlight
        terminal.bkcolor(bkcolor)
        terminal.clear_area(text_x, line_y, line_w - 4, item_h)

        # draw text
        terminal.print_(text_x, text_y, label)

        # restore background color
        terminal.bkcolor("black")

        # calculations
        line_y += max(3, cy + 1)
        index += 1

