"""Module for handling rectangle info. Contains Rect class.

See Rect (that's all this contains)
"""
# pylint: disable=import-error
from engine.vector2 import Vector2


class Rect:
    """Rect representation.

    class stores each component as an attribute, rather than position and size.
    Position of rect (x and y attributes) describe the center of the rect.

    Attributes:
        x: x ordinate of center of rect.
        y: y ordinate of center of rect.
        w: width of rect
        h: height of rect
    """

    # pylint: disable=invalid-name
    # pylint: disable=missing-function-docstring

    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def set_position(self, center_vector):
        self.x = center_vector.x
        self.y = center_vector.y

    def set_size(self, size_vector):
        self.w = size_vector.x
        self.h = size_vector.y

    def get_position(self):
        return Vector2(self.x, self.y)

    def get_size(self):
        return Vector2(self.w, self.h)

    def get_top_left(self):
        return Vector2(self.x - self.w / 2, self.y - self.h / 2)

    def get_top_right(self):
        return Vector2(self.x + self.w / 2, self.y - self.h / 2)

    def get_bottom_left(self):
        return Vector2(self.x - self.w / 2, self.y + self.h / 2)

    def get_bottom_right(self):
        return Vector2(self.x + self.w / 2, self.y + self.h / 2)

    def get_left(self):
        return self.x - self.w / 2

    def get_right(self):
        return self.x + self.w / 2

    def get_bottom(self):
        return self.y - self.h / 2

    def get_top(self):
        return self.y + self.h / 2

    def is_touching(self, vector):
        """ Is the vector touching the rect?

        Considered touching if.
            rect left <= vector x <= rect right and
            rect top <= vector y <= rect bottom (Coordinate system has y inverted)
        """
        return self.get_left() <= vector.x <= self.get_right() and \
            self.get_bottom() <= vector.y <= self.get_top()

    def get_copy(self):
        return Rect(self.x, self.y, self.w, self.h)

    def __mul__(self, other):
        return Rect(self.x * other, self.y * other, self.w * other, self.h * other)

    def __sub__(self, other):
        return Rect(self.x - other.x, self.y - other.y, self.w - other.w, self.h - other.h)

    def __add__(self, other):
        return Rect(self.x + other.x, self.y + other.y, self.w + other.w, self.h + other.h)

    def __str__(self):
        return "Rect({}, {}, {}, {})".format(self.x, self.y, self.w, self.h)

    def get_pygame_tuple(self):
        return int(self.x - self.w / 2), int(self.y - self.h / 2), int(self.w), int(self.h)
