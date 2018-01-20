from pygame import *
img = None #image.load('images//towers')
layer = 0

name = 'name'
info = 'description'

class Tower:

    def __init__(self, pos):

        self.pos = pos
        self.cost = 50

        self.id = None

        self.layer = layer
        self.projectiles = []

    def reset(self):
        pass

    def do_damage(self, enemies, *args):
        # Do damage here
        return enemies

    def show_external(self, finish = False, *args):
        pass

    def update(self, window, window_scale, playing_grid, dt):
        self.show(window, window_scale, dt)


    def show(self, window, window_scale, dt):

        # Scale image
        t_img = transform.scale(img, (int(window_scale), int(window_scale)))

        # Work out scaled pos
        pos = list(self.pos)
        pos[0] *= window_scale
        pos[1] *= window_scale

        # Show
        window.blit(t_img, pos)
