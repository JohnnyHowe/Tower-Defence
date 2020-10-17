"""Contains the Button class

    Typical usage:

    button = Button(...)
    button.add_mouse_up_listener(lambda : print("Clicked!"))

    while game_loop:
        ...
        button.show()
        ...
"""
# pylint: disable=import-error
import pygame

from engine.ui_element import UIElement, ScaleModes
from engine.vector2 import Vector2
from engine.event_handler import EventHandler


class Button(UIElement):
    """Button object. UIElement able to show solid rect and detect being clicked.

    Button uses listeners for click detection.
    To call a function foo on button press,

        button = Button(...)
        button.add_mouse_up_listener(foo)

    To be built upon - just a working placeholder
    """
    mouse_over = False  # is the mouse over the button?
    mouse_down = False  # is the mouse pressing the button right now?

    mouse_up_listeners = None
    mouse_down_listeners = None

    idle_color = (100, 100, 100)
    hovered_color = (150, 150, 150)
    pressed_color = (170, 255, 170)

    def init(self):
        # pylint: disable=no-member
        EventHandler.add_listener(pygame.MOUSEMOTION, self.on_mouse_move)
        EventHandler.add_listener(pygame.MOUSEBUTTONDOWN, self.on_mouse_down)
        EventHandler.add_listener(pygame.MOUSEBUTTONUP, self.on_mouse_up)

        self.mouse_up_listeners = []
        self.mouse_down_listeners = []

    def on_mouse_move(self, event):
        """Listener for the mouse move event.

        On the event, check whether the mouse is over the button.
        If the mouse is over the button, set the mouse_over attribute to True, else False
        If mouse_over is set to false, also set mouse_down to False
        """
        mouse_pos = Vector2(event.pos[0], event.pos[1])
        if self._last_display_rect:  # When app first opened, this may not exist
            self.mouse_over = self._last_display_rect.is_touching(mouse_pos)
            if not self.mouse_over:
                self.mouse_down = False

    def on_mouse_down(self, event):
        """Listener for the mouse down event.

        If the mouse_over attribute is True,
            the mouse down listeners are called and mouse_down attribute is set to True
        """
        if self.mouse_over:
            self.mouse_down = True
            for listener in self.mouse_down_listeners:
                listener(event)

    def on_mouse_up(self, event):
        """Listener for the mouse up event.

        if mouse_down, call mouse_up listeners
        set mouse_down to False
        """
        if self.mouse_down:
            for listener in self.mouse_up_listeners:
                listener(event)
        self.mouse_down = False

    def add_mouse_up_listener(self, listener):
        """Call listener whenever the button is pressed."""
        self.mouse_up_listeners.append(listener)

    def show(self):
        """Show the button - currently just the area rect.
        Color depends on whether mouse is over button and whether the mouse is down.
        """
        if self.mouse_down:
            color = self.pressed_color
        elif self.mouse_over:
            color = self.hovered_color
        else:
            color = self.idle_color
        self.show_area(color)
