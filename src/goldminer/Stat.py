from goldminer import draw


class Stat:
    def __init__(self, label, value, max_value=None, colors=None):
        if max_value is None:
            max_value = value

        self.label = label
        self._value = value
        self.max_value = max_value
        self.colors = colors
        self.bkcolor = "dark gray"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = min(self.max_value, max(0, value))

    @property
    def percent(self):
        return int(round(self._value * 100 / self.max_value, 0))

    @property
    def size_for(self, width):
        return int(self.percent * width / 100)

    def render_gui(self, x, y, width):
        color = draw.color_for_value(self.percent, self.colors)
        draw.progress_label(x, y, self.label, int(round(self._value, 0)), self.max_value, color)
        draw.progress(x, y + 1, width, self.percent, color, self.bkcolor)
