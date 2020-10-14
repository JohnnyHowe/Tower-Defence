import pygame
from engine.vector2 import Vector2


class _Display:

    surface = None
    size = None

    def __init__(self):
        self.resize(Vector2(600, 400))

    def resize(self, new_size):
        self.size = new_size
        self.surface = pygame.display.set_mode((new_size.x, new_size.y), pygame.RESIZABLE)


Display = _Display()
