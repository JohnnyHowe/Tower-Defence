import pygame
from engine.display import Display
from event_handler import EventHandler
from engine.vector2 import Vector2
from engine.rect import Rect
from board import Board

from test_tower import TestTower


class Game:
    board = None

    def start(self):
        self.board = Board()
        self.board.set_cell(TestTower(Vector2(0, 0)), Vector2(0, 0))

    def run_frame(self):
        EventHandler.run()
        Display.surface.fill((255, 255, 255))
        self.board.show()

        pygame.display.update()


