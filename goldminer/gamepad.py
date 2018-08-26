from enum import Enum
from bearlibterminal import terminal


def key_to_action(key):
    if key in (terminal.TK_UP, terminal.TK_KP_8):
        return GamePad.up
    elif key in (terminal.TK_DOWN, terminal.TK_KP_2):
        return GamePad.down
    elif key in (terminal.TK_LEFT, terminal.TK_KP_4):
        return GamePad.left
    elif key in (terminal.TK_RIGHT, terminal.TK_KP_6):
        return GamePad.right
    elif key == terminal.TK_A:
        return GamePad.a
    elif key in (terminal.TK_S,):
        return GamePad.b
    elif key in (terminal.TK_D,):
        return GamePad.c
    elif key in (terminal.TK_Z,):
        return GamePad.d
    elif key in (terminal.TK_X,):
        return GamePad.lb
    elif key in (terminal.TK_C,):
        return GamePad.rb
    elif key in (terminal.TK_ENTER, terminal.TK_KP_ENTER):
        return GamePad.select
    elif key in (terminal.TK_ESCAPE,):
        return GamePad.back


class GamePad(Enum):
    select = 1
    back = 2
    up = 3
    down = 4
    left = 5
    right = 6
    a = 10
    b = 11
    c = 12
    d = 13
    lb = 14
    rb = 15


class GamePadAction:
    def __init__(self, key):
        self.key = key
        self.action = key_to_action(key)
        self.is_select = self.action == GamePad.select
        self.is_back = self.action == GamePad.back
        self.is_up = self.action == GamePad.up
        self.is_down = self.action == GamePad.down
        self.is_left = self.action == GamePad.left
        self.is_right = self.action == GamePad.right
        self.is_a = self.action == GamePad.a
        self.is_b = self.action == GamePad.b
        self.is_c = self.action == GamePad.c
        self.is_d = self.action == GamePad.d
        self.is_lb = self.action == GamePad.lb
        self.is_rb = self.action == GamePad.rb
        self.is_movement = self.action in (GamePad.up, GamePad.down, GamePad.left, GamePad.right)

    @property
    def movement(self):
        if self.is_up:
            return 0, -1
        elif self.is_down:
            return 0, 1
        elif self.is_left:
            return -1, 0
        elif self.is_right:
            return 1, 0
