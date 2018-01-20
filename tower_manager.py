from pygame import *
import mouse_extras
import global_functions as gfunc
import math

# Import towers
from towers import block, machine_gun, sniper, mortar, killing_floor, lightning

class Tower_Handler:

    def __init__(self):
        self.tower_names = ['block', 'killing_floor', 'machine_gun', 'sniper', 'mortar', 'lightning']
        self.usable_towers = []
        for tower in self.tower_names: self.usable_towers.append(eval(tower))

        self.towers = []
        self.blocks = []

    def move_external(self, dt):
        for tower in self.towers:

            try: tower.move_external(dt)
            except: pass

            try: tower.validate_external()
            except: pass

    def do_damage(self, enemies, window_scale):

        # Cycle through all the towers and to damage
        for tower in self.towers:
            enemies = tower.do_damage(enemies, window_scale)

        return enemies


    def show_towers(self, window, window_scale, dt):

        for tower in self.towers:
            tower.show(window, window_scale, 1)

        self.show_external(window, window_scale, dt)


    def reset(self):

        for tower in self.towers:
            tower.reset()

    info_font = font.SysFont('arial', 18)
    def show_desc(self, window, playing_grid):
        mouse_pos = list(mouse_extras.get_pos())

        # Is the mouse over the tower selection area?
        if mouse_pos[1] >= playing_grid[1] - 1:

            # Is it over an icon?
            if mouse_pos[0] < len(self.usable_towers):

                # Get info
                tower_module = self.usable_towers[mouse_pos[0]]
                name = tower_module.name
                desc = tower_module.info

                # Show Info
                if key.get_pressed()[K_LSHIFT]: text = desc
                else: text = name + ' $' + str(tower_module.Tower(None).cost)

                message = self.info_font.render(text, 0, (255, 255, 255))
                rect = message.get_rect()
                mouse_pos = mouse.get_pos()

                margin = 3
                border = 2

                rect1 = [mouse_pos[0], mouse_pos[1], rect.width + margin + border * 2, rect.height + margin + border * 2]
                rect2 = [mouse_pos[0] + border, mouse_pos[1] + border, rect.width + margin, rect.height + margin]

                draw.rect(window, (255, 255, 255), rect1)
                draw.rect(window, (100, 100, 100), rect2)

                window.blit(message, (mouse_pos[0] + margin, mouse_pos[1] + margin))

    def update_towers(self, window, window_scale, playing_grid, dt):

        for tower in self.towers:
            tower.update(window, window_scale, playing_grid, dt)


    def draw_selection_block(self, window, window_scale, playing_grid, tower_select_rows):
        # Draw selecetion block
        selection_rect = (0, window_scale * playing_grid[1], math.ceil(window_scale * playing_grid[0]), math.ceil(tower_select_rows * window_scale))
        draw.rect(window, (150, 150, 150), selection_rect)
        return selection_rect


    def clear_towers(self):
        self.towers = []
        self.blocks = []

    held_tower = None
    def tower_selection(self, window, window_scale, playing_grid, tower_select_rows, money, dt):
        k = key.get_pressed()

        def draw_rect(colour):
            pos = mouse_extras.get_pos()
            pos[0] *= window_scale
            pos[1] *= window_scale

            rect = Surface((window_scale, window_scale))
            rect.set_alpha(128)
            rect.fill(colour)
            window.blit(rect, pos)

        selection_rect = self.draw_selection_block(window, window_scale, playing_grid, tower_select_rows)

        # Show towers in selection part
        for tower_i in range(len(self.usable_towers)):
            tower = self.usable_towers[tower_i]

            # Change index to pos
            y = int(tower_i / playing_grid[0])
            x = tower_i - y * playing_grid[0]
            y += playing_grid[1]

            # Scale pos
            x *= window_scale
            y *= window_scale

            # Scale img
            img = transform.scale(tower.img, (int(window_scale), int(window_scale)))

            # Show
            window.blit(img, (x,y))

        # Delete tower
        if not self.held_tower or k[K_LSHIFT]:

            if mouse_extras.get_states()[2] == -1 or (mouse_extras.get_pressed()[2] and k[K_LSHIFT]):
                mouse_pos = mouse_extras.get_pos()

                # What tower(s) are the mouse over?
                highest = 0
                del_tower_index = None

                for tower_index in range(len(self.towers)):
                    tower = self.towers[tower_index]

                    # Is it in the right pos?
                    if tower.pos == mouse_pos:

                        # Is it above the others?
                        if tower.layer >= highest:

                            highest = tower.layer
                            del_tower_index = tower_index

                # Is there one to delete?
                if del_tower_index != None:
                    tower = self.towers[del_tower_index]

                    # Is it a block?
                    if self.towers[del_tower_index].id == 'block':
                        index = self.blocks.index(self.towers[del_tower_index])
                        self.blocks.pop(index)

                    self.towers.pop(del_tower_index)
                    money += tower.cost



        # Show placed towers
        for tower in self.towers:
            tower.show(window, window_scale, dt)

        # Show held tower
        if self.held_tower:
            scaled_pos = mouse_extras.get_pos()
            img = transform.scale(self.held_tower.img, (int(window_scale), int(window_scale)))

            scaled_pos[0] *= window_scale
            scaled_pos[1] *= window_scale

            def show_tower():
                window.blit(img, scaled_pos)

            # Can the tower be placed?
            # Is it in the playing area

            # Does the held tower need to be let go?
            if mouse_extras.get_states()[2] == -1 and not k[K_LSHIFT]:
                self.held_tower = None
                return money

            # Does it need to be placed?
            pos = mouse_extras.get_pos()
            if pos[1] < playing_grid[1]:

                # Check that the necessary base(s) are there
                towers_in_slot = []
                for tower in self.towers:
                    if tower.pos == pos:
                        towers_in_slot.append(tower)

                held_layer = self.held_tower.layer
                okay = True

                # Check that there are no towers in the same slot and layer
                for tower in towers_in_slot:
                    if tower.layer == held_layer:
                        okay = False

                # Is it on the lowest layer? (Is it a base)
                if held_layer == 0:
                    if len(towers_in_slot) != 0:
                        okay = False

                # Is it on 2nd layer (needs base)
                if held_layer == 1:
                    if len(towers_in_slot) != 1:
                        okay = False

                    # Is there something under it?
                    if len(towers_in_slot) >= 1:

                        # Is it not a block?
                        if towers_in_slot[0].id != 'block':
                            okay = False

                if okay:

                    if money >= self.held_tower.Tower(()).cost:
                        draw_rect((100, 255, 100))
                        show_tower()
                    else:
                        draw_rect((255, 100, 100))
                        show_tower()
                    # Does the held tower need to be placed?
                    if mouse_extras.get_states()[0] == -1 or (mouse_extras.get_pressed()[0] and k[K_LSHIFT]):

                        # Does the player have enough money
                        tower = self.held_tower.Tower(pos)
                        if money >= tower.cost:

                            # Place the tower
                            self.towers.append(tower)
                            money -= tower.cost

                            # Is it a block
                            if tower.id == 'block':
                                self.blocks.append(tower)

                        # Should the tower still be held on to?
                        if not key.get_pressed()[K_LSHIFT]:
                            self.held_tower = None

                else:
                    draw_rect((255, 100, 100))
                    show_tower()

            else:
                draw_rect((255, 100, 100))
                show_tower()

        # Does a tower need to be picked up?
        else:

            mouse_states = mouse_extras.get_states()
            if mouse_states[0] == -1:

                # Pick up tower
                pos = mouse_extras.get_pos()
                mouse_rect = [pos[0] * window_scale, pos[1] * window_scale, 0, 0]

                if gfunc.touching(mouse_rect, selection_rect):

                    pos = mouse_extras.get_pos()
                    pos[1] -= playing_grid[1]

                    index = pos[1] * playing_grid[0]
                    index += pos[0]

                    if index < len(self.usable_towers):
                        tower = self.usable_towers[index]
                        self.held_tower = tower

        return money

    def show_external(self, window, window_scale, dt, finish = False):

        for tower in self.towers:
            tower.show_external(window, window_scale, dt, finish = finish)
