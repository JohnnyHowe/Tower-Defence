from pygame import *
img = image.load('images//towers//killing_floor.png')
layer = 0
import global_functions as gfunc

name = 'Insta-kill'
info = 'Press k to kill'

class Tower:

    def __init__(self, pos):

        self.pos = pos
        self.cost = 30

        self.id = 'insta'
        self.damage = 0.001

        self.layer = layer
        self.projectiles = []

    def reset(self):
        pass

    def do_damage(self, enemies, dt, *args):
        if key.get_pressed()[K_k]: return []
        return enemies

    def update(self, window, window_scale, playing_grid, dt):
        self.show(window, window_scale, dt)

    def show_external(self, *args):
        pass

    def show(self, window, window_scale, dt):

        # Scale image
        t_img = transform.scale(img, (int(window_scale), int(window_scale)))

        # Work out scaled pos
        pos = list(self.pos)
        pos[0] *= window_scale
        pos[1] *= window_scale

        # Show
        window.blit(t_img, pos)
