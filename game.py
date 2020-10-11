import pygame
from display import Display
from eventHandler import EventHandler
from vector2 import Vector2
from rect import Rect


class Game:
    board = None

    def start(self):
        self.board = Board()

    def run_frame(self):
        EventHandler.run()
        Display.surface.fill((255, 255, 255))
        self.board.show()

        pygame.display.update()


class Board:
    size = None
    items = None

    def __init__(self, size=Vector2(10, 7)):
        self.size = size
        self.initialize_board()

    def initialize_board(self):
        items = []
        for y in range(self.size.y):
            items.append([None, ] * self.size.x)

    def show(self):
        self.show_background()
        self.show_grid()

    def show_grid(self):
        cell_size = self.get_cell_size()
        board_rect = self.get_board_rect()
        offset = board_rect.get_top_left()
        for x in range(self.size.x + 1):
            pygame.draw.line(Display.surface, (0, 0, 0),
                             (x * cell_size + offset.x, offset.y),
                             (x * cell_size + offset.x, board_rect.h + offset.y))
        for y in range(self.size.y + 1):
            pygame.draw.line(Display.surface, (0, 0, 0),
                             (offset.x, y * cell_size + offset.y),
                             (offset.x + board_rect.w, y * cell_size + offset.y))

    def show_background(self):
        board_rect = self.get_board_rect()
        pygame.draw.rect(Display.surface, (200, 200, 200), board_rect.get_pygame_tuple())

    def get_board_rect(self):
        cell_size = self.get_cell_size()
        window_center = Vector2(Display.size.x / 2, Display.size.y / 2)
        return Rect(window_center.x, window_center.y, self.size.x * cell_size, self.size.y * cell_size)

    def get_cell_position(self, cell):
        cell_size = self.get_cell_size()
        board_rect = self.get_board_rect()
        return board_rect.get_top_left() + cell * cell_size

    def get_cell_size(self):
        return min(Display.size.x / self.size.x, Display.size.y / self.size.y)
