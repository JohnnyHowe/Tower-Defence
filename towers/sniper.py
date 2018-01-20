from pygame import *
import global_functions as gfunc
import random
img = image.load('images//towers//sniper_icon.png')
layer = 1

name = 'Sniper'
info = 'Slow but very high damage weapon'

class Tower:

    def __init__(self, pos):

        self.pos = pos
        self.cost = 150

        self.id = 'sniper'
        self.damage = 15

        self.aiming = False

        self.layer = layer
        self.reset()

        self.base_img = image.load('images//towers//sniper_base.png')
        self.gun_img = image.load('images//towers//sniper_gun.png')

    def reset(self):
        self.aiming = False
        self.rot = 0
        self.recoil = 0
        self.shots = []
        self.points = [self.pos]
        self.max_time = 1
        self.last_time = random.random() * self.max_time
        self.projectiles = []

    def show_shot(self, window, window_scale, dt):
        for shot in self.shots:
            pos1 = int((shot[0][0]) * window_scale), int((shot[0][1]) * window_scale)
            pos2 = int((self.pos[0] + 0.5) * window_scale), int((self.pos[1] + 0.5) * window_scale)

            cv = min((200/0.2) * shot[1] + 55, 255)
            cv = 255 - cv
            draw.line(window, (cv, cv, cv), pos1, pos2, int(window_scale / 10))

            shot[1] -= dt
            if shot[1] <= 0:
                index = self.shots.index(shot)
                self.shots.pop(index)

    last_time = 0
    def shoot(self, dt, game_size, game_scale):

        self.last_time += dt
        if self.last_time >= self.max_time:

            if self.aiming:

                self.last_time -= self.max_time

                # Shoot
                self.recoil = game_scale * 0.1
                slope = gfunc.slope(self.rot)

                # Make a list of points that will receive damage
                pos = self.pos[0] + 0.5, self.pos[1] + 0.5
                points = [pos]
                accuracy = 0.1 # Lower is better

                while True:
                    last_pos = points[len(points) - 1]
                    next_pos = (round(last_pos[0] - slope[0], 5), round(last_pos[1] - slope[1], 5))
                    points.append(next_pos)

                    # Have we made it to the edge of the map?
                    if next_pos[0] < -1 or next_pos[0] > game_size[0] + 1 or next_pos[1] < -1 or next_pos[1] > game_size[1] + 1:
                        break

                self.shots.append([points[len(points) - 1], 0.2])
                for value in points: self.points.append(value)


    def do_damage(self, enemies, *args):

        # Aim
        self.aim(enemies)

        eindex = 1

        for enemy in enemies:
            enemy_pos = enemy.get_rect(1)
            if enemy_pos:

                for x, y in self.points:
                    rect1 = x, y, 0, 0

                    if gfunc.touching(rect1, enemy_pos):
                        enemy.health -= self.damage / eindex
                        eindex += 1
                        break

        self.points = [self.pos]

        # Do damage here
        return enemies

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

    def show_external(self, window, window_scale, dt, finish = False):
        self.show_shot(window, window_scale, dt)

    def update(self, window, window_scale, playing_grid, dt):
        self.show(window, window_scale, dt)
        self.shoot(dt, playing_grid, window_scale)

        self.recoil = max(0, self.recoil - dt * 20)

    def show(self, window, window_scale, dt):

        # Show base
        base_img = transform.scale(self.base_img, (int(window_scale), int(window_scale)))

        # Work out scaled pos
        pos = list(self.pos)
        pos[0] *= window_scale
        pos[1] *= window_scale

        # Show
        window.blit(base_img, pos)

        # Show gun
        center_pos = pos[0] + window_scale / 2, pos[1] + window_scale / 2

        gun_img = transform.scale(self.gun_img, (int(window_scale), int(window_scale)))
        gun_img = transform.rotate(gun_img, self.rot)

        rect = gun_img.get_rect()
        pos = [center_pos[0] - rect.width / 2, center_pos[1] - rect.height / 2]

        # Add recoil
        slope = gfunc.slope(self.rot)
        change = slope[0] * self.recoil, slope[1] * self.recoil

        pos[0] += change[0]
        pos[1] += change[1]

        window.blit(gun_img, pos)

