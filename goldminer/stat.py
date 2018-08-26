class Stat:
    def __init__(self, label, value, max_value=None):
        if max_value is None:
            max_value = value

        self.label = label
        self._value = value
        self.max_value = max_value

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
