from pygame import *
img = image.load('images//towers//killing_floor.png')
layer = 0
import global_functions as gfunc

name = 'Killing Floor'
info = 'Does damage to one enemy standing on this'

class Tower:

    def __init__(self, pos):

        self.pos = pos
        self.cost = 30

        self.id = 'killingfloor'
        self.damage = 0.001

        self.layer = layer
        self.projectiles = []

    def reset(self):
        pass

    def do_damage(self, enemies, dt, *args):

        # Do damage here
        for enemy in enemies:

            pos = enemy.get_pos()
            if pos:

                rect1 = pos[0] + 0.5, pos[1] + 0.5, 0, 0
                rect2 = self.pos[0], self.pos[1], 1, 1

                if gfunc.touching(rect1, rect2):
                    enemy.health -= self.damage * dt

                    return enemies
        return enemies

    def update(self, window, window_scale, playing_grid, dt):
        self.show(window, window_scale, dt)

    def show_external(self, finish = False, *args):
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
