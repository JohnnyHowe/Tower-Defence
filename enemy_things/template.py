from pygame import *
import global_functions as gfunc
import math

class Enemy:

    def __init__(self, scale, speed, time_until_spawn):

        self.id = ''
        self.money = 0

        self.speed = speed
        self.scale = scale

        self.max_health = 10
        self.health = self.max_health

        self.dead = False
        self.path = []

        # Negative distance will be treated as the time left until the enemy will spawn
        self.dist = -time_until_spawn

        # Load image
        self.image = image.load('images\\enemies\\none.png')

    def update(self, window, window_scale, dt):
        self.move(dt)
        self.show(window, window_scale)
        self.update_death()


    def update_death(self):

        if self.health <= 0:
            self.dead = True


    def show_health(self, window, window_scale):

        height = max(1, 0.1 * window_scale)
        width = 0.8 * window_scale

        rect = self.get_rect(window_scale)

        if rect:
            health_per = max(0, self.health / self.max_health)

            x = rect[0] + rect[2] / 2 - width / 2
            y = max(0, rect[1] - window_scale * 0.1)

            draw.rect(window, (200, 100, 100), (x, y, width, height))

            if health_per > 0: draw.rect(window, (100, 200, 100), (x, y, width * health_per, height))


    # This will allow the init function to be called before the fight stage so all the images can be loaded in at the start
    def set(self, path):
        self.path = path

    # Enable the enemy to move
    def move(self, dt):
        self.dist += dt * self.speed

    # Change the distance integer to a position on the path
    def get_pos(self, dist = None):
        if not dist:
            if self.dist < len(self.path) - 3:
                if self.dist > 0: return gfunc.get_pos_on_path(self.path, self.dist)
                else: return None

        else: return gfunc.get_pos_on_path(self.path, dist)


    def get_rect(self, window_scale):
        pos = self.get_pos()
        if pos:return [pos[0] * window_scale, pos[1] * window_scale, window_scale, window_scale]
        else: return False

    # Show the enemy
    def show(self, window, window_scale):

        # Get blit pos and scale
        current_pos = self.get_pos()

        if current_pos:
            pos = list(current_pos)
            pos[0] *= window_scale
            pos[1] *= window_scale

            # Scale image to fit the correct amount of space
            img = transform.scale(self.image, (int(window_scale),) * 2)
            old_rect = img.get_rect()

            # Add the rotation
            next_dist = self.dist + 0.7
            next_pos = self.get_pos(dist = next_dist)

            angle = gfunc.get_rot(next_pos, current_pos) - 90
            img = transform.rotate(img, angle)

            # Add the sway
            rot = math.sin(self.dist * 4) * 5 # Sin because the curve resembles the wanted swaying motion
            img = transform.rotate(img, rot)

            rect = img.get_rect()
            change = (rect.width - old_rect.width) / 2, (rect.height - old_rect.height) / 2

            pos[0] -= change[0]
            pos[1] -= change[1]

            # Show
            window.blit(img, pos)
