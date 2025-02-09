# coding: UTF-8
from enum import IntEnum

class Direction(IntEnum):
    u'''移動方向を表す整数列挙型。'''
    LEFT = 0
    DOWN = 1
    RIGHT = 2
    UP = 3

    def reverse(d):
        if d == Direction.LEFT: return Direction.RIGHT
        elif d == Direction.DOWN: return Direction.UP
        elif d == Direction.RIGHT: return Direction.LEFT
        elif d == Direction.UP: return Direction.DOWN