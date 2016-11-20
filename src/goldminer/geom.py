import enum


class Rect:
    @classmethod
    def from_points(cls, x1, y1, x2, y2):
        return cls(x1, y1, x2 - x1, y2 - y1)

    @classmethod
    def from_rect(cls, other):
        return cls(other.x, other.y, other.w, other.h)

    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __iter__(self):
        for y in range(self.y, self.y + self.h):
            for x in range(self.x, self.x + self.w):
                yield x, y

    def __str__(self):
        return "<Rect {},{} {}x{}>".format(self.left, self.top, self.width, self.height)

    def set(self, x, y, w, h):
        self.set_position(x, y)
        self.set_size(w, h)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_size(self, w, h):
        self.w = w
        self.h = h

    def swap_size(self):
        tmp = self.w
        self.w = self.h
        self.h = tmp

    @property
    def position(self):
        return self.x, self.y

    @property
    def size(self):
        return self.w, self.h

    @property
    def width(self):
        return self.w

    @property
    def height(self):
        return self.h

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.w

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.h

    @property
    def center_x(self):
        return self.x + int(self.w / 2)

    @property
    def center_y(self):
        return self.y + int(self.h / 2)

    @property
    def values(self):
        return self.x, self.y, self.w, self.h

    def contains(self, x, y):
        return (self.x <= x <= self.right and
                self.y <= y <= self.bottom)

    def overlaps(self, other):
        return (self.right > other.left and self.left < other.right and
                self.top < other.bottom and self.bottom > other.top)

    def top_left(self):
        return self.left, self.top

    def bottom_right(self):
        return self.right, self.bottom

    def expand_by(self, n: int):
        """
        Expands the rectangle by "n" points
        :param n: int
        """
        self.x -= n
        self.y -= n
        self.w += n
        self.h += n


def orientation(from_x, from_y, to_x, to_y):
    return from_x - to_x, from_y - to_y


class Direction(enum.IntEnum):
    left = 180
    up = 90
    right = 0
    down = 270

    @property
    def is_horizontal(self):
        return self in (Direction.left, Direction.right)

    @property
    def is_vertical(self):
        return self in (Direction.down, Direction.up)

    def as_vector(self):
        return {
            Direction.left: (-1, 0),
            Direction.up: (0, -1),
            Direction.right: (1, 0),
            Direction.down: (0, 1),
        }.get(self)
