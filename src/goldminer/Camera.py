from goldminer.Rect import Rect


class Camera:
    def __init__(self, width, height, map_width=None, map_height=None,
                 offset_x=0, offset_y=0):

        if map_width is None:
            map_width = width

        if map_height is None:
            map_height = height

        self.rect = Rect(0, 0, width, height)
        self.map_width = map_width
        self.map_height = map_height
        self.offset_x = offset_x
        self.offset_y = offset_y

    def update(self, tx, ty):
        # coordinates so that the target is at the center of the screen
        x = int(tx - self.rect.w / 2)
        y = int(ty - self.rect.h / 2)

        # make sure the camera doesn't see outside the map
        x = max(0, min(self.map_width - self.rect.width + 1, x))
        y = max(0, min(self.map_height - self.rect.height + 1, y))

        self.rect.set_position(x, y)

    def map_to_camera(self, x, y):
        x += self.offset_x
        y += self.offset_y
        return x - self.rect.x, y - self.rect.y

    def camera_to_map(self, x, y):
        x -= self.offset_x
        y -= self.offset_y
        return x + self.rect.x, y + self.rect.y
