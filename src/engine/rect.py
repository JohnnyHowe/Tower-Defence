from engine.vector2 import Vector2


class Rect:
    """ Rect object
    x and y ordinates are of the center. """

    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def set_center(self, center_vector):
        self.x = center_vector.x
        self.y = center_vector.y

    def set_size(self, size_vector):
        self.w = size_vector.x
        self.h = size_vector.y

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
        return int(self.x - self.w / 2), int(self.y - self.h / 2), int(self.w), int(self.h)
