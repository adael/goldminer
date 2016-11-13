from bearlibterminal import terminal
from enum import Enum


class Gamepad(Enum):
    select = 1
    back = 2
    up = 3
    down = 4
    left = 5
    right = 6
    a = 10
    b = 11
    x = 12
    z = 13
    lb = 14
    rb = 15


def key_to_action(key):
    if key in (terminal.TK_UP, terminal.TK_KP_8):
        return Gamepad.up
    elif key in (terminal.TK_DOWN, terminal.TK_KP_2):
        return Gamepad.down
    elif key in (terminal.TK_LEFT, terminal.TK_KP_4):
        return Gamepad.left
    elif key in (terminal.TK_RIGHT, terminal.TK_KP_6):
        return Gamepad.right
    elif key in (terminal.TK_A, terminal.TK_SPACE):
        return Gamepad.a
    elif key in (terminal.TK_B, ):
        return Gamepad.b
    elif key in (terminal.TK_Z, ):
        return Gamepad.z
    elif key in (terminal.TK_X, ):
        return Gamepad.x
    elif key in (terminal.TK_I, ):
        return Gamepad.lb
    elif key in (terminal.TK_G, terminal.TK_P):
        return Gamepad.rb
    elif key in (terminal.TK_ENTER, terminal.TK_KP_ENTER):
        return Gamepad.select
    elif key in (terminal.TK_ESCAPE,):
        return Gamepad.back
