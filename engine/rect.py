from engine.vector2 import Vector2


class Rect:
    """ Rect object
    x and y ordinates are of the center. """

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_center(self):
        return Vector2(self.x, self.y)

    def get_top_left(self):
        return Vector2(self.x - self.w / 2, self.y - self.h / 2)

    def __mul__(self, other):
        return Rect(self.x * other, self.y * other, self.w * other, self.h * other)

    def __sub__(self, other):
        return Rect(self.x - other.x, self.y - other.y, self.w - other.w, self.h - other.h)

    def __add__(self, other):
        return Rect(self.x + other.x, self.y + other.y, self.w + other.w, self.h + other.h)

    def __str__(self):
        return "Rect({}, {}, {}, {})".format(self.x, self.y, self.w, self.h)

    def get_pygame_tuple(self):
        return self.x - self.w / 2, self.y - self.h / 2, self.w, self.h
