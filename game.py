import pygame
from engine.display import Display
from engine.event_handler import EventHandler
from engine.vector2 import Vector2
from board import Board

from test_tower import TestTower


class Game:
    board = None
    mouse_cell = None   # What cell is the mouse over?

    def start(self):
        self.board = Board()
        EventHandler.add_listener(pygame.MOUSEMOTION, self.mouse_motion_listener)
        EventHandler.add_listener(pygame.MOUSEBUTTONUP, self.mouse_up_listener)

    def run_frame(self):
        EventHandler.run()

        Display.surface.fill((255, 255, 255))
        self.board.show_background()
        self.show_mouse_over_cell()
        self.board.show_towers()

        pygame.display.update()

    def show_mouse_over_cell(self, color=(255, 255, 0)):
        """ Highlight the mouse_cell if it exists. """
        if self.mouse_cell:
            pygame.draw.rect(Display.surface, color, self.board.get_cell_rect(self.mouse_cell).get_pygame_tuple())

    def mouse_motion_listener(self, event):
        """ When there's a mouse motion event, set the mouse cell. """
        mouse_pos = Vector2(event.pos[0], event.pos[1])
        mouse_pos -= self.board.get_board_rect().get_top_left()
        mouse_pos /= self.board.get_cell_size()
        if 0 < mouse_pos.x < self.board.size.x and 0 < mouse_pos.y < self.board.size.y:
            self.mouse_cell = Vector2(int(mouse_pos.x), int(mouse_pos.y))
        else:
            self.mouse_cell = None

    def mouse_up_listener(self, event):
        """ When mouse 1 (left) is released, try make a tower.
        When mouse 3 (right) is released, try remove a tower. """
        if event.button == 1:
            self.try_make_tower("HOES", self.mouse_cell)
        elif event.button == 3:
            self.sell_cell(self.mouse_cell)

    def sell_cell(self, cell):
        """ Clears the cell. Refunding the player the towers refund amount. """
        # Refund player
        self.board.set_cell_contents(None, cell)

    def try_make_tower(self, tower, position):
        """ Try to make a tower at the position.
        Checks:
          - position (anything there? on board?)
          - is the tower valid (not None?)
        """
        # Is this a valid position? (Anything there already?)
        # Can the player afford this?
        # Do it
        self.board.set_cell_contents(TestTower(position), position)

