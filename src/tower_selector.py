from engine.vector2 import Vector2
from engine.ui_element import UIElement, ScaleModes


class TowerSelector(UIElement):

    current = None

    def show(self):
        # print(self._last_display_rect)
        self.show_area()
