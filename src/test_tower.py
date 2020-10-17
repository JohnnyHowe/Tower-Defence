import pygame
import time

from engine.vector2 import Vector2
from engine.display import Display
from engine.event_handler import EventHandler

from projectile import Projectile
from tower import Tower
from projectile_manager import ProjectileManager


class TestTower(Tower):

    name = "Test Tower"
    icon_path = "images/TestTower.png"

    def __init__(self, position, board):
        super().__init__(position, board)
        # EventHandler.add_listener(pygame.MOUSEBUTTONUP, lambda x: self.shoot())

    def shoot(self):
        end = Vector2(0, 0)
        ProjectileManager.add_projectile(TestProjectile(self.position, end, self.board))


class TestProjectile(Projectile):

    start_time = None
    time_to_live = 1
    start = None
    end = None

    def __init__(self, start, end, board):
        super().__init__(board)
        self.start = start
        self.end = end
        self.start_time = time.time()

    def is_valid(self):
        return time.time() < self.start_time + self.time_to_live

    def update(self):
        pass

    def show(self):
        start = self.board.get_cell_center(self.start).get_pygame_tuple()
        end = self.board.get_cell_center(self.end).get_pygame_tuple()
        pygame.draw.line(Display.surface, (255, 255, 255), start, end, int(self.board.get_cell_size() * 0.2))
