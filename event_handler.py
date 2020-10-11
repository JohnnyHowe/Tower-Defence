import pygame
from engine.display import Display
from engine.vector2 import Vector2


class _Handler:
    """ Should this be static?
    Maybe even just a bunch of functions? """

    def run(self):
        events = pygame.event.get()
        for event in events:

            # Quit button
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.VIDEORESIZE:
                Display.resize(Vector2(event.w, event.h))

        return events


EventHandler = _Handler()
