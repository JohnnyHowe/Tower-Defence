

class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "Vector({}, {})".format(self.x, self.y)

    @staticmethod
    def one():
        return Vector2(1, 1)
