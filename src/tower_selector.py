import pygame

from engine.display import Display
from engine.ui_element import UIElement, ScaleModes
from engine.rect import Rect
from engine.vector2 import Vector2
from engine.button import Button
from engine.ui_element import ScaleModes


class TowerSelector(UIElement):
    """Tower selector bar.

    Shows all towers horizontally along the rect given. See tower_selector.Icon."""

    current = None
    towers = None
    icons = None

    def __init__(self,
                 towers,
                 rect,
                 scale_mode=Rect(ScaleModes.absolute, ScaleModes.absolute,
                                 ScaleModes.absolute, ScaleModes.absolute),
                 offset=Rect(),
                 offset_mode=Rect(ScaleModes.relative, ScaleModes.relative,
                                  ScaleModes.relative, ScaleModes.relative)):
        super().__init__(rect, scale_mode, offset, offset_mode)
        self.towers = towers
        self.load_icons()

    def load_icons(self):
        """load up the icons list. For each tower in self.towers, create an icon."""
        icons = []
        icon_size = self.rect.h
        for i, tower_class in enumerate(self.towers):
            icon = Icon(tower_class,
                        rect=Rect(icon_size * (i + 0.5),
                                  0,
                                  icon_size,
                                  icon_size),
                        scale_mode=Rect(ScaleModes.absolute,
                                        ScaleModes.absolute,
                                        ScaleModes.absolute,
                                        ScaleModes.absolute),
                        )
            icon.parent = self
            icon.inherit = Rect(False, True, False, False)

            icons.append(icon)
        self.icons = icons

    def show(self):
        self.show_area()
        self.show_towers()

    def show_towers(self):
        for icon in self.icons:
            icon.show()


class Icon(Button):
    """Object to represent the icons on the tower selector."""

    tower_class = None
    image = None

    def __init__(self,
                 tower_class,
                 rect,
                 scale_mode=Rect(ScaleModes.absolute, ScaleModes.absolute,
                                 ScaleModes.absolute, ScaleModes.absolute),
                 offset=Rect(),
                 offset_mode=Rect(ScaleModes.relative, ScaleModes.relative,
                                  ScaleModes.relative, ScaleModes.relative),
                 ):
        super().__init__(rect, scale_mode, offset, offset_mode)
        self.tower_class = tower_class
        self.image = pygame.image.load(tower_class.icon_path)

    # def show(self, rect):
    #     image = pygame.transform.scale(self.image, rect.get_size().get_pygame_tuple())
    #     Display.surface.blit(image, rect.get_top_left().get_pygame_tuple())
