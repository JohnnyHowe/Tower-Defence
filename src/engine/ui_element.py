"""Module for handling UI elements.

Contains UIElement, a parent class for UI elements. This class holds the heavy lifting for
scaling and positioning UI elements as well as some debugging features like showing borders.
Contains ScaleModes, these act similar to an Enum and tell your UI element
how to scale and position itself.

    TODO update this

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


class ScaleModes(Enum):
    """Contains resizing/scaling options for the UIElement.

    Attributes:
        absolute: treat the size component as pixels, no scaling.
        relative: multiply the size component by the corresponding window size component.
    """
    absolute = 0
    relative = 1


# class PositionModes(Enum):
#     """Contains positioning options for the UIElement.
#
#     The positioning of the UIElement is done on the PyGame window.
#     This means the top left is (0, 0).
#
#     Attributes:
#         absolute: treat the size component as pixels, no scaling.
#         relative: multiply the size component by the corresponding window size component.
#     """
#     absolute = 0    # Take position as pixels
#     relative = 1    # Multiply position by window size


class UIElement:
    """Parent for UIElements. Contains the nasty positioning and scaling work.

    Attributes:
        rect: where and how big the element is. how this is interpreted defined by scale_mode.
            The position of the rect is treated as an anchor point
        scale_mode: how to treat the rect. eg, relative, absolute positioning? See ScaleModes
        offset: Rect on how much to offset the rect.
        offset_mode: Rect on how to treat offset. See ScaleModes
        parent: the parent object of the element. Allows the element to be scaled/positioned
            relative to the parent.
    """
    # pylint: disable=too-few-public-methods

    rect = None
    scale_mode = None

    offset = None
    offset_mode = None

    parent = None
    inherit = Rect(True, True, True, True)

    _last_display_rect = None  # rect in pixels that the element took up last time it was shown

    def __init__(self, rect,
                 scale_mode=Rect(ScaleModes.absolute, ScaleModes.absolute,
                                 ScaleModes.absolute, ScaleModes.absolute),
                 offset=Rect(),
                 offset_mode=Rect(ScaleModes.relative, ScaleModes.relative,
                                  ScaleModes.relative, ScaleModes.relative),
                 ):
        """Initializes the UIElement with the given parameters.
        See class doc for attribute definitions.
        If no anchor_mode or size_mode is given, they are assumed to be relative.
        """
        self.rect = rect
        self.scale_mode = scale_mode

        self.offset = offset
        self.offset_mode = offset_mode

        self.init()

    def init(self):
        """ Called by __init__ so you don't need to copy all the parameters again.
        Override this to add things to __init__. """

    # ==================================================
    # Display-ers
    # ==================================================

    def show_area(self, color=(0, 0, 216)):
        """Show the area the element takes up as a solid color rectangle."""
        self._last_display_rect = self.get_final_rect()
        pygame.draw.rect(Display.surface, color, self._last_display_rect.get_pygame_tuple())

    def show_anchor(self, color=(0, 0, 128), radius=5):
        """Show a dot at the anchor point of the element"""
        offset = self.get_scaled_offset().get_position() + self.get_scaled_rect().get_position()
        pygame.draw.circle(Display.surface, color,
                           offset.get_pygame_tuple(),
                           radius)

    def show_center(self, color=(0, 0, 0), radius=5):
        """Show a dot at the center point of the element"""
        pygame.draw.circle(Display.surface, color,
                           self.get_scaled_rect().get_position().get_pygame_tuple(),
                           radius)

    def show_offset(self, color=(0, 0, 128), width=5):
        """ Show a line between the anchor and center point. """
        center = self.get_scaled_rect().get_position()
        offset = self.get_scaled_offset().get_position() + center
        pygame.draw.line(Display.surface, color,
                         center.get_pygame_tuple(),
                         offset.get_pygame_tuple(),
                         width)

    # ==================================================
    # Display helpers
    # ==================================================

    def get_final_rect(self):
        """Get the position center position of the element the display (in pixels)."""
        return self.get_scaled_rect() + self.get_scaled_offset() + self.get_parent_offset()

    def get_parent_offset(self):
        """How much does the parent offset the final rect?"""
        rect = Rect()
        if self.parent:
            parent_rect = self.parent.get_final_rect()
            if self.inherit.x:
                rect.x = parent_rect.x
            if self.inherit.y:
                rect.y = parent_rect.y
            if self.inherit.w:
                rect.w = parent_rect.w
            if self.inherit.h:
                rect.h = parent_rect.h
        return rect

    def get_scaled_rect(self):
        """ Scale up the rect according to scale_mode. """
        return Rect(
            UIElement.__scaled_component(self.rect.x, self.scale_mode.x, Display.size.x),
            UIElement.__scaled_component(self.rect.y, self.scale_mode.y, Display.size.y),
            UIElement.__scaled_component(self.rect.w, self.scale_mode.w, Display.size.x),
            UIElement.__scaled_component(self.rect.h, self.scale_mode.h, Display.size.y)
        )

    def get_scaled_offset(self):
        """Get the offset rect scaled up."""
        return Rect(
            UIElement.__scaled_component(self.offset.x, self.offset_mode.x, Display.size.x),
            UIElement.__scaled_component(self.offset.y, self.offset_mode.y, Display.size.y),
            UIElement.__scaled_component(self.offset.w, self.offset_mode.x, Display.size.x),
            UIElement.__scaled_component(self.offset.h, self.offset_mode.y, Display.size.y),
        )

    @staticmethod
    def __scaled_component(component, mode, display_size_component):
        """Get the component scaled in accordance with mode."""
        if mode == ScaleModes.relative:
            return component * display_size_component
        return component

