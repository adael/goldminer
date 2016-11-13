from bearlibterminal import terminal


class SelectItem:
    def __init__(self, label, active=True):
        self.label = label
        self.active = active


class SelectBox:
    def __init__(self, x, y, items):
        self.x = x
        self.y = y
        self.w = None
        self.h = None
        self.items = items
        self.padding_left = 2
        self.item_focused_index = 0
        self.item_selected_index = None
        self.calculate_dimension()

    def is_selected(self):
        return self.item_selected_index is not None

    def item_selected(self):
        if self.item_selected_index is not None:
            item = self.items[self.item_selected_index]
            self.item_selected_index = None
            return item

    def item_focused(self):
        return self.items[self.item_focused_index]

    def up_item(self):
        if self.item_focused_index > 0:
            self.item_focused_index -= 1

    def down_item(self):
        if self.item_focused_index < len(self.items) - 1:
            self.item_focused_index += 1

    def select_focused_item(self):
        if self.item_focused().active:
            self.item_selected_index = self.item_focused_index

    def calculate_dimension(self):
        w = 3
        h = 3

        for item in self.items:
            w = max(len(item.label), w)

        for item in self.items:
            box = "[bbox={}]".format(w)
            h = max(terminal.measure(box + item.label), h)

        self.w = w + self.padding_left
        self.h = h

    def handle_input(self, key):
        if key in (terminal.TK_UP, terminal.TK_KP_8):
            self.up_item()
        elif key in (terminal.TK_DOWN, terminal.TK_KP_2):
            self.down_item()
        elif key in (terminal.TK_RETURN, terminal.TK_KP_ENTER):
            self.select_focused_item()

