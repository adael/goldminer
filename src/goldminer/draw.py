from bearlibterminal import terminal


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


def window(rect_, caption):
    terminal.clear_area(rect_.x, rect_.y, rect_.width, rect_.height)
    line(rect_.x + 1, rect_.y + 2, rect_.width - 2, "[U+2594]")
    rect(rect_)
    terminal.print_(rect_.center_x, rect_.y + 1, "[align=center]" + caption)
