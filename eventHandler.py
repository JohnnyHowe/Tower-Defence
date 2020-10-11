import pygame
from display import Display
from vector2 import Vector2


class _Handler:

    def __init__(self):
        pass

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
