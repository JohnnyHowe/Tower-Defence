from pygame import *
from enemy_things import path_finder
import global_functions as gfunc
import time

# Import enemies
from enemy_things import walker, sprinter

class Enemy_Handler:

    def __init__(self):
        self.enemies = []
        self.added_money = 0

    def update_enemies(self, window, window_scale, playing_grid, dt, money):

        finished = False
        extra_money = 0

        temp = []
        for enemy in self.enemies:

            # Update
            enemy.update(window, window_scale, dt)

            # Is it still valid?
            pos = enemy.get_pos()

            if pos:
                if not enemy.dead:
                    if pos[0] < playing_grid[0]:
                        temp.append(enemy)
                    else:
                        finished = True

                else: # Dead
                    extra_money += enemy.money


            else:
                temp.append(enemy)

        money += extra_money
        self.added_money += extra_money

        for enemy in self.enemies:
            enemy.show_health(window, window_scale)

        self.enemies = temp
        return finished, money


    def set_enemy_path(self):

        # Update the path
        for enemy in self.enemies:
            enemy.path = self.path


    def load_enemies(self, enemies):

        # Store the objects
        self.enemies = []
        last_time = 0

        for enemy in enemies:
            name, scale, speed, amount, init_t, mid_t = enemy

            last_time += init_t

            for index in range(amount):

                last_time += mid_t
                string = name + '.Enemy(scale, speed, last_time)'
                self.enemies.append(eval(string))

    blocks = []     # Keep track of the blocks on the grid to avoid updating the path when it doesn't need to
    path = None

    def update_path(self, window, window_scale, grid_size, blocks, dt):
        self.get_path(blocks, grid_size)

        if self.path:
            self.show_path(window, window_scale, dt)

    lines = None
    old_path = None

    def show_path(self, window, window_scale, dt):

        # Has the path changed?
        if self.path != self.old_path:

            # Update old path
            self.old_path = self.path

            # reset the lines

            # Partial reset
            if self.old_path and self.lines:

                for index in range(len(self.old_path)):
                    if self.old_path[index] != self.path[index]:
                        break

                lines = self.lines[:index - 1]

                for next_i in range(len(self.path) - len(lines)):
                    last = lines[len(lines) - 1]
                    lines.append(last + 1)

                self.lines = lines

            # Complete reset
            else:
                self.lines = []
                for dist in range(len(self.path) - 1):
                    self.lines.append(dist + 0.5)


        reset = False

        # Show the lines
        for dist_index in range(len(self.lines)):

            dist = self.lines[dist_index]
            self.lines[dist_index] += dt * 2

            # Work out positions
            front_dist = dist
            back_dist = dist - 0.5

            if front_dist > 0:

                pos = gfunc.get_pos_on_path(self.path, front_dist)
                back_pos = gfunc.get_pos_on_path(self.path, back_dist)

                # If everything is on the path
                if pos and back_pos:

                    pos = list(pos)
                    back_pos = list(back_pos)

                    # Center points
                    pos[0] += 0.5
                    pos[1] += 0.5

                    back_pos[0] += 0.5
                    back_pos[1] += 0.5

                    # Scale pos
                    pos[0] *= window_scale
                    pos[1] *= window_scale

                    back_pos[0] *= window_scale
                    back_pos[1] *= window_scale

                    # Show
                    draw.line(window, (255, 100, 30), pos, back_pos, max(1, int(window_scale * 0.15)))

                else:
                    reset = True

        if reset:

            for dist_index in range(len(self.lines)):
                self.lines[dist_index] -= 1


    def get_path(self, blocks, grid_size):

        if blocks != self.blocks or self.path == None:
            self.blocks = list(blocks)

            # Update path
            self.path = path_finder.get_path(blocks, grid_size)
