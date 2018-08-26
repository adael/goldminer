class SelectItem:
    def __init__(self, label, active=True):
        self.label = label
        self.active = active


class Separator:
    def __init__(self):
        self.label = ""
        self.active = False


class SelectBox:
    def __init__(self, items):
        self.items = items
        self.item_focused_index = 0
        if 0 in self.items and not self.items[0].active:
            self.item_focused_index = self.next_active_index()
        self.item_selected_index = None

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
        index = self.prev_active_index()
        if index is not None:
            self.item_focused_index = index

    def down_item(self):
        index = self.next_active_index()
        if index is not None:
            self.item_focused_index = index

    def prev_active_index(self):
        for index in range(self.item_focused_index - 1, -1, -1):
            if self.items[index].active:
                return index

    def next_active_index(self):
        for index in range(self.item_focused_index + 1, len(self.items)):
            if self.items[index].active:
                return index

    def select_focused_item(self):
        if self.item_focused().active:
            self.item_selected_index = self.item_focused_index

    def handle_input(self, action):
        if action.is_up:
            self.up_item()
        elif action.is_down:
            self.down_item()
        elif action.is_a or action.is_select:
            self.select_focused_item()
