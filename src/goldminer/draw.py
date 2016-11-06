from bearlibterminal import terminal


def color_for_value(value, colors=None):
    if not colors:
        colors = ["dark red", "red", "orange", "yellow", "dark green", "green"]

    ncolors = len(colors) - 1
    percent = round(value * ncolors / 100, 0)
    index = int(min(ncolors, max(0, percent)))
    return colors[index]


def progress_label(x, y, label, value, max_value, color):
    label += " [color={}]{}[color=white]/{}".format(color, value, max_value)
    terminal.print_(x, y, label)


def progress(x, y, width, percent, color, bkcolor="dark gray"):
    fill_width = int(percent * width / 100)
    terminal.print_(x, y, "[bkcolor={}]".format(bkcolor) + (" " * width))
    terminal.print_(x, y, "[bkcolor={}]".format(color) + (" " * fill_width))


def rect(rect):
    box(rect.left, rect.top, rect.right, rect.bottom)


def box(x1, y1, x2, y2):
    for cx in range(x1, x2):
        terminal.put(cx, y1, 0x2550)
        terminal.put(cx, y2, 0x2550)

    for cy in range(y1, y2):
        terminal.put(x1, cy, 0x2551)
        terminal.put(x2, cy, 0x2551)

    terminal.put(x1, y1, 0x2554)
    terminal.put(x1, y2, 0x255A)
    terminal.put(x2, y2, 0x255D)
    terminal.put(x2, y1, 0x2557)

# U+2550	═	e2 95 90	&#9552;	═	BOX DRAWINGS DOUBLE HORIZONTAL
# U+2551	║	e2 95 91	&#9553;	║	BOX DRAWINGS DOUBLE VERTICAL
# U+2552	╒	e2 95 92	&#9554;	╒	BOX DRAWINGS DOWN SINGLE AND RIGHT DOUBLE
# U+2553	╓	e2 95 93	&#9555;	╓	BOX DRAWINGS DOWN DOUBLE AND RIGHT SINGLE
# U+2554	╔	e2 95 94	&#9556;	╔	BOX DRAWINGS DOUBLE DOWN AND RIGHT
# U+2555	╕	e2 95 95	&#9557;	╕	BOX DRAWINGS DOWN SINGLE AND LEFT DOUBLE
# U+2556	╖	e2 95 96	&#9558;	╖	BOX DRAWINGS DOWN DOUBLE AND LEFT SINGLE
# U+2557	╗	e2 95 97	&#9559;	╗	BOX DRAWINGS DOUBLE DOWN AND LEFT
# U+2558	╘	e2 95 98	&#9560;	╘	BOX DRAWINGS UP SINGLE AND RIGHT DOUBLE
# U+2559	╙	e2 95 99	&#9561;	╙	BOX DRAWINGS UP DOUBLE AND RIGHT SINGLE
# U+255A	╚	e2 95 9a	&#9562;	╚	BOX DRAWINGS DOUBLE UP AND RIGHT
# U+255B	╛	e2 95 9b	&#9563;	╛	BOX DRAWINGS UP SINGLE AND LEFT DOUBLE
# U+255C	╜	e2 95 9c	&#9564;	╜	BOX DRAWINGS UP DOUBLE AND LEFT SINGLE
# U+255D	╝	e2 95 9d	&#9565;	╝	BOX DRAWINGS DOUBLE UP AND LEFT
# U+255E	╞	e2 95 9e	&#9566;	╞	BOX DRAWINGS VERTICAL SINGLE AND RIGHT DOUBLE
# U+255F	╟	e2 95 9f	&#9567;	╟	BOX DRAWINGS VERTICAL DOUBLE AND RIGHT SINGLE
# U+2560	╠	e2 95 a0	&#9568;	╠	BOX DRAWINGS DOUBLE VERTICAL AND RIGHT
# U+2561	╡	e2 95 a1	&#9569;	╡	BOX DRAWINGS VERTICAL SINGLE AND LEFT DOUBLE
# U+2562	╢	e2 95 a2	&#9570;	╢	BOX DRAWINGS VERTICAL DOUBLE AND LEFT SINGLE
# U+2563	╣	e2 95 a3	&#9571;	╣	BOX DRAWINGS DOUBLE VERTICAL AND LEFT
# U+2564	╤	e2 95 a4	&#9572;	╤	BOX DRAWINGS DOWN SINGLE AND HORIZONTAL DOUBLE
# U+2565	╥	e2 95 a5	&#9573;	╥	BOX DRAWINGS DOWN DOUBLE AND HORIZONTAL SINGLE
# U+2566	╦	e2 95 a6	&#9574;	╦	BOX DRAWINGS DOUBLE DOWN AND HORIZONTAL
# U+2567	╧	e2 95 a7	&#9575;	╧	BOX DRAWINGS UP SINGLE AND HORIZONTAL DOUBLE
# U+2568	╨	e2 95 a8	&#9576;	╨	BOX DRAWINGS UP DOUBLE AND HORIZONTAL SINGLE
# U+2569	╩	e2 95 a9	&#9577;	╩	BOX DRAWINGS DOUBLE UP AND HORIZONTAL
# U+256A	╪	e2 95 aa	&#9578;	╪	BOX DRAWINGS VERTICAL SINGLE AND HORIZONTAL DOUBLE
# U+256B	╫	e2 95 ab	&#9579;	╫	BOX DRAWINGS VERTICAL DOUBLE AND HORIZONTAL SINGLE
# U+256C	╬	e2 95 ac	&#9580;	╬	BOX DRAWINGS DOUBLE VERTICAL AND HORIZONTAL
