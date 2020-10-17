import pygame
from engine.vector2 import Vector2
from engine.rect import Rect
from engine.display import Display
from engine.event_handler import EventHandler
from engine.ui_element import UIElement


class Board(UIElement):

    # Board logic
    size = None
    items = None

    # GUI
    mouse_cell = None

    def init(self, size=Vector2(12, 8)):
        # Board logic
        self.size = size
        self.initialize_board()

        # GUI
        EventHandler.add_listener(pygame.MOUSEMOTION, self.mouse_motion_listener)

    def initialize_board(self):
        """Set the items list to a 2D list of size filled with None.
        x columns, y rows"""
        self.items = []
        for y in range(self.size.y):
            self.items.append([None, ] * self.size.x)

    def set_cell_contents(self, obj, position):
        """Set the item in cell."""
        self.items[position.y][position.x] = obj

    def get_cell_contents(self, position):
        """What's there?"""
        return self.items[position.y][position.x]

    def is_on_board(self, cell):
        """Is the cell a valid cell?
        is it on the board?"""
        return 0 <= cell.x < self.size.x and 0 <= cell.y < self.size.y

    # ==================================================
    # GUI interaction
    # ==================================================

    def mouse_motion_listener(self, event):
        """When there's a mouse motion event, set the mouse cell.
        If the mouse isn't over a cell, set to None."""
        board_rect = self.get_scaled_board_rect()
        mouse_pos = Vector2(event.pos[0], event.pos[1])
        mouse_pos -= board_rect.get_top_left()
        mouse_pos /= (board_rect.w / self.size.x)
        if 0 < mouse_pos.x < self.size.x and 0 < mouse_pos.y < self.size.y:
            self.mouse_cell = Vector2(int(mouse_pos.x), int(mouse_pos.y))
        else:
            self.mouse_cell = None

    # ==================================================
    # Display-ers
    # ==================================================

    def show(self):
        """Show the board. Including the background and towers/tiles"""
        self.show_background()
        self.show_mouse_over_cell()
        self.show_grid(color=(150, 150, 150))
        # self.show_towers()

    def show_towers(self):
        """Loop through all the items and show the towers."""
        for row in self.items:
            for item in row:
                if item:
                    item.show()

    def show_grid(self, color=(0, 0, 0), line_width=1):
        """Show grid lines over the board."""
        rect = self.get_scaled_board_rect()
        offset = rect.get_top_left()
        cell_size = rect.w / self.size.x
        for x in range(self.size.x + 1):
            pygame.draw.line(Display.surface, color,
                             (x * cell_size + offset.x, offset.y),
                             (x * cell_size + offset.x, rect.h + offset.y),
                             line_width)
        for y in range(self.size.y + 1):
            pygame.draw.line(Display.surface, color,
                             (offset.x, y * cell_size + offset.y),
                             (offset.x + rect.w, y * cell_size + offset.y),
                             line_width)

    def show_background(self, color=(200, 200, 200)):
        """Show a solid color backdrop for the board"""
        pygame.draw.rect(Display.surface, color, self.get_scaled_board_rect().get_pygame_tuple())

    def show_mouse_over_cell(self, color=(255, 255, 0)):
        """Highlight the mouse_over cell (if it exists)."""
        if self.mouse_cell:
            pygame.draw.rect(Display.surface,
                             color,
                             self.get_cell_rect(self.mouse_cell,
                                                self.get_final_rect()).get_pygame_tuple())

    # ==================================================
    # Display helpers
    # ==================================================

    def get_scaled_board_rect(self):
        """What is the rect of the board in pixels? - Where will it be shown?
        Returns a sub-rect of (UIElement.)rect. Maximises the board while keeping the aspect
        ratio."""
        max_rect = self.get_final_rect()
        scale = min(max_rect.w / self.size.x, max_rect.h / self.size.y)
        return Rect(max_rect.x, max_rect.y, scale * self.size.x, scale * self.size.y)

    def get_cell_center(self, cell):
        """Get the center position of the cell in pixels."""
        display_rect = self.get_scaled_board_rect()
        cell_size = display_rect.w / self.size.x
        cell_offset = (cell + Vector2.one() / 2) * cell_size
        return display_rect.get_top_left() + cell_offset

    def get_cell_size(self):
        """Get the board cell size in pixels."""
        rect = self.get_scaled_board_rect()
        return min(rect.x / self.size.x, rect.y / self.size.y) * 2

    def get_cell_rect(self, position, display_rect):
        """Get the rect of the cell in pixels."""
        cell_pos = self.get_cell_center(position)
        cell_size = self.get_cell_size()
        return Rect(cell_pos.x, cell_pos.y, cell_size, cell_size)


