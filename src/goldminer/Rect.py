class Rect:

    @staticmethod
    def from_points(x1, y1, x2, y2):
        return Rect(x1, y1, x2 - x1, y2 - y1)

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

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

    def expanded_by(self, n):
        """Return a rectangle with extended borders.

        Create a new rectangle that is wider and taller than the
        immediate one. All sides are extended by "n" points.
        """
        self.x -= n
        self.y -= n
        self.w += n
        self.h += n

    def __str__(self):
        return "<Rect (%s,%s)-(%s,%s)>" % (self.left, self.top, self.right, self.bottom)
