import pygame
from engine.display import Display


class TestTower:

    def __init__(self, position):
        self.position = position

    def show(self, board):
        pygame.draw.rect(Display.surface, (0, 0, 255), board.get_cell_rect(self.position).get_pygame_tuple())
