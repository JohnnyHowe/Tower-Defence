import pygame
from engine.display import Display


class Tower:

    position = None
    board = None

    def __init__(self, position, board):
        self.position = position
        self.board = board

    def show(self):
        pygame.draw.rect(Display.surface, (0, 0, 255), self.board.get_cell_rect(self.position).get_pygame_tuple())

    def update(self):
        pass