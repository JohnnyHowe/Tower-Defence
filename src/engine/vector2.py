

class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __divmod__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __str__(self):
        return "Vec({}, {})".format(self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_pygame_tuple(self):
        return int(self.x), int(self.y)

    @staticmethod
    def component_mul(vec1, vec2):
        return Vector2(vec1.x * vec2.x, vec1.y * vec2.y)

    @staticmethod
    def one():
        return Vector2(1, 1)

    @staticmethod
    def left():
        return Vector2(-1, 0)

    @staticmethod
    def right():
        return Vector2(1, 0)

    @staticmethod
    def up():
        return Vector2(0, 1)

    @staticmethod
    def down():
        return Vector2(0, -1)
