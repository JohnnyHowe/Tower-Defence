from pygame import *
import global_functions as gfunc
import random

img = image.load('images\\towers\\machine_gun_icon.png')
layer = 1

name = 'Machine Gun'
info = 'Fast firing, low damage gun'

bullet_img = image.load('images\\towers\\bullet.png')

class Bullet:

    def __init__(self, pos, slope, speed = 35):
        self.pos = list(pos)
        self.slope = slope
        self.angle = self.get_angle()
        self.speed = speed
        self.damage = 0.3

        self.id = 'machine_gun'

        self.height = 0.3 # Multiplied by the window scale

    def update(self, window, window_scale, dt):
        self.move(dt)

    def move(self, dt):
        self.pos[0] += dt * self.speed * self.slope[0]
        self.pos[1] += dt * self.speed * self.slope[1]


    def get_angle(self):
        p1 = self.pos
        p2 = self.pos[0] + self.slope[0], self.pos[1] + self.slope[1]
        return gfunc.get_rot(p1, p2)


    def on_screen(self, window_scale, game_grid):

        rect = self.get_rect(window_scale)
        scaled_grid = (0, 0) + gfunc.tuple_mult(game_grid, window_scale)

        if gfunc.touching(rect, scaled_grid):
            return True
        return False


    def get_rect(self, window_scale):
        img_rect = bullet_img.get_rect()
        scale = self.height * window_scale / min(img_rect.width, img_rect.height)

        width = img_rect.width * scale
        height = img_rect.height * scale

        img = transform.scale(bullet_img, (int(width), int(height)))
        img = transform.rotate(img, self.angle)

        rect_obj = img.get_rect()
        rect_list = [self.pos[0] * window_scale - rect_obj.width / 2, self.pos[1] * window_scale - rect_obj.height / 2, rect_obj.width, rect_obj.height]

        return rect_list


    def show(self, window, window_scale, dt):
        img_rect = bullet_img.get_rect()
        scale = self.height * window_scale / min(img_rect.width, img_rect.height)

        width = img_rect.width * scale
        height = img_rect.height * scale

        img = transform.scale(bullet_img, (int(width), int(height)))
        img = transform.rotate(img, self.angle)

        rect = self.get_rect(window_scale)

        pos = rect[:2]
        window.blit(img, pos)


class Tower:

    def __init__(self, pos):

        self.layer = layer

        self.pos = pos
        self.cost = 30

        self.id = 'name'
        self.info = 'description'

        self.base_img = image.load('images\\towers\\machine_gun_base.png')
        self.barrel_img = image.load('images\\towers\\machine_gun_barrel.png')

        self.rot = None
        self.projectiles = []

        self.aiming = False
        self.reset()

        self.time = 1
        self.last_shot = random.random() * self.time


    def move_external(self, dt):
        for bullet in self.projectiles:
            bullet.move(dt)

    def shoot(self, dt):

        self.last_shot += dt * 10

        if self.last_shot >= self.time:
            self.last_shot -= self.time

            if self.rot and self.aiming:

                pos = list(self.pos)
                pos[0] += 0.5
                pos[1] += 0.5

                self.projectiles.append(Bullet(pos, gfunc.slope(self.rot - 180)))
                self.recoil = 0.5


    def update_bullets(self, window, window_scale, game_grid, dt):

        temp = []
        for bullet in self.projectiles:
            bullet.update(window, window_scale, dt)

            if bullet.on_screen(window_scale, game_grid):
                temp.append(bullet)

        self.projectiles = list(temp)


    def reset(self):
        self.projectiles = []
        self.rot = 0
        self.recoil = 0


    def do_damage(self, enemies, window_scale):
        self.aim(enemies)

        for enemy in enemies:
            enemy_rect = enemy.get_rect(window_scale)

            if enemy_rect:

                for bullet in self.projectiles:
                    bullet_rect = bullet.get_rect(window_scale)

                    if gfunc.touching(bullet_rect, enemy_rect):

                        enemy.health -= bullet.damage
                        bullet_index = self.projectiles.index(bullet)
                        self.projectiles.pop(bullet_index)


        return enemies


    def update(self, window, window_scale, playing_grid, dt):
        self.shoot(dt)
        self.update_bullets(window, window_scale, playing_grid, dt)
        self.show(window, window_scale)
        self.recoil = max(0, self.recoil - dt * 5)

    def aim(self, enemies):
        if len(enemies) > 0:

            # Aim at first
            enemy = enemies[0]
            pos = enemy.get_pos()

            if pos:

                pos[0] += 0.5
                pos[1] += 0.5

                this_pos = list(self.pos)
                this_pos[0] += 0.5
                this_pos[1] += 0.5

                self.rot = gfunc.get_rot(pos, this_pos)
                self.aiming = True
                return
        self.aiming = False

    def show_external(self, window, window_scale, dt, finish = False, *args):
        for bullet in self.projectiles:
            bullet.show(window, window_scale, dt)

    def show(self, window, window_scale, *args):

        # Scale images
        base = transform.scale(self.base_img, (int(window_scale), int(window_scale)))
        barrel = transform.scale(self.barrel_img, (int(window_scale), int(window_scale)))

        # Rotate barrel
        if self.rot: barrel = transform.rotate(barrel, self.rot)

        # Get correct position after rotation
        rect = barrel.get_rect()
        offset = (window_scale - rect.width) / 2, (window_scale - rect.height) / 2

        # Work out scaled pos
        pos = list(self.pos)
        pos[0] *= window_scale
        pos[1] *= window_scale

        # Add recoil
        scale = 0.2 * self.recoil
        slope = gfunc.slope(self.rot)
        xc = slope[0] * scale * window_scale
        yc = slope[1] * scale * window_scale

        # Show
        window.blit(base, pos)
        window.blit(barrel, (pos[0] + offset[0] + xc, pos[1] + offset[1] + yc))
