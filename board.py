import pygame
from engine.vector2 import Vector2
from engine.rect import Rect
from engine.display import Display


class Board:
    size = None
    items = None

    def __init__(self, size=Vector2(10, 7)):
        self.size = size
        self.initialize_board()

    def initialize_board(self):
        """ Set the items list to a 2D list of size filled with None.
        x columns, y rows """
        self.items = []
        for y in range(self.size.y):
            self.items.append([None, ] * self.size.x)

    def show(self):
        """ Show the board
        background, grid, towers. """
        self.show_background()
        self.show_grid()
        self.show_towers()

    def show_towers(self):
        """ Loop through all the items and show the towers. """
        for row in self.items:
            for item in row:
                if item:
                    item.show(self)

    def show_grid(self, color=(0, 0, 0), line_width=1):
        """ Show grid lines over the board. """
        cell_size = self.get_cell_size()
        board_rect = self.get_board_rect()
        offset = board_rect.get_top_left()
        for x in range(self.size.x + 1):
            pygame.draw.line(Display.surface, color,
                             (x * cell_size + offset.x, offset.y),
                             (x * cell_size + offset.x, board_rect.h + offset.y),
                             line_width)
        for y in range(self.size.y + 1):
            pygame.draw.line(Display.surface, color,
                             (offset.x, y * cell_size + offset.y),
                             (offset.x + board_rect.w, y * cell_size + offset.y),
                             line_width)

    def show_background(self, color=(200, 200, 200)):
        """ Show a solid color backdrop for the board """
        board_rect = self.get_board_rect()
        pygame.draw.rect(Display.surface, color, board_rect.get_pygame_tuple())

    def get_board_rect(self):
        """ Get the rect of the board in pixels. """
        cell_size = self.get_cell_size()
        window_center = Vector2(Display.size.x / 2, Display.size.y / 2)
        return Rect(window_center.x, window_center.y, self.size.x * cell_size, self.size.y * cell_size)

    def get_cell_top_left(self, cell):
        """ Get the top left position of the cell in pixels. """
        cell_size = self.get_cell_size()
        board_rect = self.get_board_rect()
        return board_rect.get_top_left() + cell * cell_size

    def get_cell_center(self, cell):
        """ Get the center position of the cell in pixels. """
        return self.get_cell_top_left(cell) + Vector2.one() * self.get_cell_size() * 0.5

    def get_cell_size(self):
        """ Get the board cell size in pixels. """
        return min(Display.size.x / self.size.x, Display.size.y / self.size.y)

    def get_cell_rect(self, position):
        """ Get the rect of the cell in pixels. """
        cell_pos = self.get_cell_center(position)
        cell_size = self.get_cell_size()
        return Rect(cell_pos.x, cell_pos.y, cell_size, cell_size)

    def set_cell_contents(self, obj, position):
        """ Set the item in cell. """
        self.items[position.y][position.x] = obj

    def get_cell_contents(self, position):
        """ What's there? """
        return self.items[position.y][position.x]

