import pygame
from display import Display
from eventHandler import EventHandler
from game import Game


class Scenes:
    game = Game()


class Main:
    """ State machine for the game. """

    current = None

    def __init__(self):
        self.change_scene(Scenes.game)

    def change_scene(self, new_scene):
        self.current = new_scene
        self.current.start()

    def run_frame(self):
        self.current.run_frame()

    def run(self):
        while True:
            self.run_frame()


if __name__ == "__main__":
    Main().run()
