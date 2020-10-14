"""Module for handling UI elements.

Contains UIElement, a parent class for UI elements. This class holds the heavy lifting for
scaling and positioning UI elements as well as some debugging features like showing borders.
Contains SizeModes and PositionModes, these act similar to an Enum and tell your UI element
how to scale and position itself.

    Typical usage:

    class SomeElement(UIElement):
        ...

    foo = SomeElement(anchor_point=Vector2(...), size=Vector2(...),
                      anchor_mode=Vector2(...), size_mode=Vector2(...))

    while x:    # game loop
        ...
        foo.show()
        ...
"""
# pylint: disable=import-error
from enum import Enum

import pygame

from engine.display import Display
from engine.vector2 import Vector2
from engine.rect import Rect


class SizeModes(Enum):
    """Contains resizing/scaling options for the UIElement.

    Attributes:
        absolute: treat the size component as pixels, no scaling.
        relative: multiply the size component by the corresponding window size component.
    """
    absolute = 0
    relative = 1


class PositionModes(Enum):
    """Contains positioning options for the UIElement.

    The positioning of the UIElement is done on the PyGame window.
    This means the top left is (0, 0).

    Attributes:
        absolute: treat the size component as pixels, no scaling.
        relative: multiply the size component by the corresponding window size component.
    """
    absolute = 0    # Take position as pixels
    relative = 1    # Multiply position by window size


class UIElement:
    """Parent for UIElements. Contains the nasty positioning and scaling work.

    Attributes:
        anchor_point: position Vector2. How this scales is defined by anchor_mode.
        anchor_mode: Vector2 on how to treat anchor_point. See PositionModes.
        size: size Vector2. How this scales is defined by size_mode.
        size_mode: Vector2 on how to treat size. See SizeModes.
        offset: Vector2 on how much to offset center of element from anchor_point
        offset_mode: Vector2 on how to treat offset. See PositionModes
    """
    # pylint: disable=too-few-public-methods

    anchor_point = None
    anchor_mode = None
    offset = None

    size = None
    size_mode = None
    offset_mode = None

    _last_display_rect = None   # rect in pixels that the element took up last time it was shown

    def __init__(self, anchor_point, size, offset=Vector2(0, 0),
                 anchor_mode=Vector2(PositionModes.relative, PositionModes.relative),
                 size_mode=Vector2(SizeModes.relative, SizeModes.relative),
                 offset_mode=Vector2(PositionModes.relative, PositionModes.relative)):
        """Initializes the UIElement with the given parameters.
        See class doc for attribute definitions.
        If no anchor_mode or size_mode is given, they are assumed to be relative.
        """
        self.anchor_point = anchor_point
        self.anchor_mode = anchor_mode

        self.size = size
        self.size_mode = size_mode

        self.offset = offset
        self.offset_mode = offset_mode

    def show_area(self, color=(0, 0, 216)):
        """Show the area the element takes up as a solid color rectangle."""
        rect = Rect()
        rect.set_position(self.get_scaled_position())
        rect.set_size(self.get_scaled_size())
        self._last_display_rect = rect
        pygame.draw.rect(Display.surface, color, self._last_display_rect.get_pygame_tuple())

    def show_anchor(self, color=(0, 0, 128), radius=5):
        """Show a dot at the anchor point of the element"""
        pygame.draw.circle(Display.surface, color,
                           self.get_scaled_anchor_position().get_pygame_tuple(),
                           radius)

    def get_scaled_position(self):
        """Get the position center position of the element the display (in pixels)."""
        return self.get_scaled_anchor_position() - self.get_scaled_offset()

    def get_scaled_offset(self):
        """Get the offset scaled up."""
        return Vector2(
            UIElement.__scaled_pos_comp(self.offset.x, self.offset_mode.x, Display.size.x),
            UIElement.__scaled_pos_comp(self.offset.y, self.offset_mode.y, Display.size.y))

    def get_scaled_anchor_position(self):
        """Get the position of the anchor point on the display (in pixels)."""
        return Vector2(
            UIElement.__scaled_pos_comp(self.anchor_point.x, self.anchor_mode.x, Display.size.x),
            UIElement.__scaled_pos_comp(self.anchor_point.y, self.anchor_mode.y, Display.size.y))

    def get_scaled_size(self):
        """Get the size of the element on the display (in pixels)."""
        return Vector2(
            UIElement.__scaled_size_comp(self.size.x, self.size_mode.x, Display.size.x),
            UIElement.__scaled_size_comp(self.size.y, self.size_mode.y, Display.size.y))

    @staticmethod
    def __scaled_pos_comp(component, mode, display_size_component):
        """Get the position component scaled in accordance with mode."""
        if mode == PositionModes.relative:
            return component * display_size_component
        return component

    @staticmethod
    def __scaled_size_comp(component, mode, display_size_component):
        """Get the size component scaled in accordance with mode."""
        if mode == SizeModes.relative:
            return component * display_size_component
        return component
