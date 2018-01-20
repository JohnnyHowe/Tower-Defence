'''
This code was stolen from the machine_gun file and had minor edits
Don't stress, I stole it from myself - Johnny
'''

from pygame import *
import global_functions as gfunc
import math, time, random

img = image.load('images\\towers\\mortar_icon.png')
layer = 1

name = 'Mortar'
info = 'Shoots explosive projectiles'

bullet_img = image.load('images\\towers\\bomb.png')

class Bullet:

    def __init__(self, pos, rot, destination, speed = 12):
        self.pos = list(pos)
        self.speed = speed
        self.dest = destination

        self.dist = math.sqrt((pos[0] - destination[0]) ** 2 + (pos[1] - destination[1]) ** 2)
        self.dist2 = 0 # Distance travelled

        self.slope = gfunc.slope(rot)

        self.angle = self.get_angle()
        self.id = 'bomb'

        self.height = 0.3 # Multiplied by the window scale

    def update(self, window, window_scale, dt):
        self.move(dt)

    def move(self, dt):
        self.pos[0] -= dt * self.speed * self.slope[0]
        self.pos[1] -= dt * self.speed * self.slope[1]
        dist = math.sqrt((dt * self.speed * self.slope[0]) ** 2 + (dt * self.speed * self.slope[1]) ** 2)
        self.dist2 += dist


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
        scale = (self.height * window_scale) / min(img_rect.width, img_rect.height)

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

        percent_done = self.dist2 / self.dist

        x = (1 - abs(percent_done - 0.5)) * 0.5
        x += 1

        extra_size = x

        if extra_size > 0.05:
            img = transform.scale(bullet_img, (int(width * extra_size), int(height * extra_size)))
            img = transform.rotate(img, self.angle)

        rect = self.get_rect(window_scale)

        pos = rect[:2]
        window.blit(img, pos)


class Tower:

    def __init__(self, pos):

        self.layer = layer

        self.pos = pos
        self.cost = 75

        self.id = 'name'
        self.info = 'description'

        self.base_img = image.load('images\\towers\\mortar_base.png')
        self.barrel_img = image.load('images\\towers\\mortar_gun.png')

        self.rot = None
        self.projectiles = []
        self.aiming = False

        self.damage = 15
        self.ex_range = 3

        self.time = 1
        self.reset()

        self.images = [
            image.load('images//misc//explosion//1.png'),
            image.load('images//misc//explosion//2.png'),
            image.load('images//misc//explosion//3.png'),
            image.load('images//misc//explosion//4.png'),
            image.load('images//misc//explosion//5.png'),
            image.load('images//misc//explosion//6.png'),
        ]

    def validate_external(self):
        bullets = []
        for bullet in self.projectiles:
            if bullet.dist2 < bullet.dist:
                bullets.append(bullet)
        self.projectiles = bullets

    def shoot(self, dt):
        time = self.time

        self.last_shot += dt

        if self.last_shot >= time:
            self.last_shot -= time

            if self.rot and self.aiming:

                pos = list(self.pos)
                pos[0] += 0.5
                pos[1] += 0.5

                self.projectiles.append(Bullet(pos, self.rot, self.aiming))
                self.recoil = 1.5


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
        self.explosions = []
        self.last_shot = random.random() * self.time
        self.recoil = 0


    def do_damage(self, enemies, window_scale):

        self.aim(enemies)

        for bullet in self.projectiles:
            b_index = self.projectiles.index(bullet)

            # Has the bullet reached its destination?
            if bullet.dist2 >= bullet.dist:

                # Make an explosion
                pos = bullet.pos
                self.explosions.append([pos, 1, random.randint(0, 4) * 90])

                # Remove bomb
                self.projectiles.pop(b_index)

                # Do damage
                for enemy in enemies:

                    epos = enemy.get_pos()
                    if epos:

                        dist = math.sqrt((pos[0] - epos[0]) ** 2 + (pos[1] - epos[1]) ** 2)
                        if dist <= self.ex_range:
                            # Do damage

                            dist_per = 1 - (dist / self.ex_range)

                            damage = dist_per * self.damage
                            enemy.health -= damage

        return enemies


    def update(self, window, window_scale, playing_grid, dt):
        self.shoot(dt)
        self.update_bullets(window, window_scale, playing_grid, dt)
        self.show(window, window_scale, dt)

        self.recoil = max(0, self.recoil - dt * 10)


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
                self.aiming = pos
                return
        self.aiming = False


    def show(self, window, window_scale, dt, *args):

        # Scale images
        base = transform.scale(self.base_img, (int(window_scale), int(window_scale)))
        barrel = transform.scale(self.barrel_img, (int(window_scale), int(window_scale)))

        # Rotate barrel
        if self.rot: barrel = transform.rotate(barrel, self.rot)

        # Get correct position after rotation
        rect = barrel.get_rect()
        offset = (window_scale - rect.width) / 2, (window_scale - rect.height) / 2

        pos = list(self.pos)

        # Add recoil
        scale = 0.2 * self.recoil
        slope = gfunc.slope(self.rot)
        xc = slope[0] * scale * window_scale
        yc = slope[1] * scale * window_scale

        # Work out scaled pos
        pos[0] *= window_scale
        pos[1] *= window_scale

        # Show
        window.blit(base, pos)
        window.blit(barrel, (pos[0] + offset[0] + xc, pos[1] + offset[1] + yc))

    def move_external(self, dt):
        for bullet in self.projectiles:
            bullet.move(dt)

    def show_external(self, window, window_scale, dt, finish = False, *args):
        time_between = 1 / len(self.images)

        for bullet in self.projectiles:
            bullet.show(window, window_scale, dt)

        # Show explosions
        for explosion in self.explosions:
            index = self.explosions.index(explosion)

            img_index = int(explosion[1] * (len(self.images) - 1))
            img = self.images[img_index]

            size = window_scale * 2
            img = transform.scale(img, (int(size), int(size)))
            img = transform.rotate(img, explosion[2])

            pos = int(explosion[0][0] * window_scale), int(explosion[0][1] * window_scale)
            window.blit(img, (pos[0] - size / 2, pos[1] - size / 2))

            self.explosions[index][1] -= dt * 5
            if self.explosions[index][1] < 0: self.explosions.pop(index)
