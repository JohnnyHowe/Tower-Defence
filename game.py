import pygame
from engine.display import Display
from event_handler import EventHandler
from engine.vector2 import Vector2
from engine.rect import Rect
from board import Board

from test_tower import TestTower


class Game:
    board = None
    mouse_cell = None   # What cell is the mouse over?

    def start(self):
        self.board = Board()
        # self.board.set_cell(TestTower(Vector2(0, 0)), Vector2(0, 0))
        EventHandler.add_listener(pygame.MOUSEMOTION, self.mouse_motion_listener)

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
