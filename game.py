from pygame import *
import pickle, math, mouse_extras, enemy_manager, random
import global_functions as gfunc
import time as Time

def run(level, max_levels, window_size, old_window, y_change = -1):

    import tower_manager

    # Set up
    main_window = display.set_mode(window_size, RESIZABLE)
    clock = time.Clock()

    # Get level info
    level_info = pickle.load(open('levels', 'rb'))[level]
    money = level_info['start_money']


    # Scale window correctly
    message_height = 1
    game_grid = level_info['grid_size']
    scale = min(window_size[0] / game_grid[0], window_size[1] / (game_grid[1] + message_height))
    game_size = scale * game_grid[0], scale * game_grid[1]
    game_window = Surface(game_size)

    # Make message surface
    message_surf = Surface((game_size[0], math.ceil(scale)))

    # Start up handlers
    tower_handler = tower_manager.Tower_Handler()
    enemy_handler = enemy_manager.Enemy_Handler()

    # Fancy hitbox things
    def show_dev_things():

        if key.get_pressed()[K_F2]:

            # Show fps
            gfunc.show_fps(game_window)

            # Enemies
            for enemy in enemy_handler.enemies:

                try:
                    rect = enemy.get_rect(game_scale)

                    if rect:
                        draw.rect(game_window, (255, 100, 100), rect, 2)
                except:
                    pass

            # Towers
            for tower in tower_handler.towers:
                draw.rect(game_window, (100, 255, 100), (tower.pos[0] * game_scale, tower.pos[1] * game_scale, game_scale, game_scale), 2)

                # Projectiles
                for obj in tower.projectiles:
                    draw.rect(game_window, (100, 100, 255), obj.get_rect(game_scale), 2)



    # Work out tower selection size
    num = len(tower_handler.usable_towers)
    rows = math.ceil(num / game_grid[0])
    playing_grid = list(game_grid)
    playing_grid[1] += rows
    tower_select_rows = rows

    # Make background functions (just for ease later)
    def show_background_image(background): game_window.blit(background, (0,0))
    def show_background_colour(background): game_window.fill(background)

    def resize(window_size, window, game_window, game_size):

        # Size and offset the game correctly
        new = gfunc.event_loop()
        scale = min(window_size[0] / playing_grid[0], window_size[1] / (playing_grid[1] + message_height))
        game_size = playing_grid[0] * scale, playing_grid[1] * scale
        game_window = Surface(game_size)
        offset = (window_size[0] - game_size[0]) / 2, math.ceil((window_size[1] - game_size[1] + scale) / 2)

        if new: clock.tick()

        if new: window_size = new; window = display.set_mode(window_size, RESIZABLE)
        return offset, window, window_size, game_window, game_size, scale

    def pause(window_size):
        escape = gfunc.get_key_states()[K_ESCAPE]
        if escape:

            surf_size = game_size[1] + message_height * game_scale
            surf = Surface((game_size[0], surf_size))

            surf.blit(game_window, (0, math.ceil(game_scale)))
            surf.blit(message_surf, (0, 0))

            window_size, value = gfunc.pause(surf, window_size, offset, (0, 0))
            clock.tick()

            if value == 'quit':
                window.fill((30, 30, 30))
                window.blit(game_window, (offset[0], offset[1]))
                window.blit(message_surf, (offset[0], offset[1] - game_scale))
                return 'quit', Surface(window_size)

            return 'done', window_size

    # Set background functions
    if type(level_info['background']) == tuple: show_background = show_background_colour; background = level_info['background']
    else: show_background = show_background_image; background = image.load(level_info['background'])

    state = 1

    # Path message
    red_value = 255
    last_red_change = -1

    # Game loop (loop through the stages)
    while True:
        paused = 0
        dead = False

        if state == 0:
            money -= enemy_handler.added_money
            enemy_handler.added_money = 0
            state = 1

        for enemies in level_info['enemies']:
            if dead: break

            enemy_len = 0
            for enemy in enemies:
                enemy_len += enemy[3]

            enemy_handler.load_enemies(enemies)

            complete = False
            while not complete:
                if dead: break

                # Set up loop (game)
                while True:

                    # Must be at start
                    offset, main_window, window_size, game_window, game_size, game_scale = resize(window_size, main_window, game_window, game_size)
                    window = Surface(window_size)
                    mouse_extras.update(game_scale, playing_grid, offset)
                    message_surf = Surface((game_size[0], math.ceil(game_scale)))
                    gfunc.update_keys(key)

                    # Does the game need to progress to the next stage?
                    k = key.get_pressed()
                    if k[K_RETURN] and enemy_handler.path: break

                    # Does the game grid need to be cleared?
                    if k[K_c]: tower_handler.clear_towers(); money = level_info['start_money']

                    # Clear window(s)
                    show_background(background)
                    message_surf.fill((150, 150, 150))

                    # Do important things
                    dt = clock.tick() / 1000

                    # Update towers
                    money = tower_handler.tower_selection(game_window, game_scale, game_grid, tower_select_rows, money, dt)
                    tower_handler.show_external(game_window, game_scale, dt, finish = True)
                    tower_handler.move_external(dt)

                    # Update path
                    enemy_handler.update_path(game_window, game_scale, game_grid, tower_handler.blocks, dt)

                    # Show message
                    if enemy_handler.path:
                        gfunc.show_message('Build stage!', message_surf, size = game_scale * 0.5, pos = ('mid', 'top'))
                        gfunc.show_message('Press enter to start the wave!', message_surf, size = game_scale * 0.3, pos = ('mid', 'low'), colour = (90, 90, 90))

                        colour = (70, 70, 70)
                        gfunc.show_message('Money: ' + str(money), message_surf, colour = colour, border = 0.3, pos = 'right', size = 0.4 * game_scale)
                        gfunc.show_message('Incoming Enemies: ' + str(enemy_len), message_surf, colour = colour, border = 0.3, pos = 'left', size = 0.4 * game_scale)

                    else:
                        gfunc.show_message('It must be possible for the enemies to get through!', message_surf, colour = (red_value, 50, 0), border = 0.3)

                        # Make the error message change colour for a cool animation
                        red_value += last_red_change * dt * 500
                        red_value = max(min(255, red_value), 150)
                        if red_value >= 255 or red_value <= 150: last_red_change = -last_red_change

                    # Pause button
                    val = pause(window_size)

                    if val:
                        if val[0] == 'done':
                            y_change = 0
                            window_size = val[1]
                            offset, main_window, window_size, game_window, game_size, game_scale = resize(window_size, main_window, game_window, game_size)
                            continue
                        else: return val

                    # Must be at end
                    window.fill((30, 30, 30))
                    show_dev_things()
                    window.blit(game_window, offset)
                    window.blit(message_surf, (offset[0], offset[1] - game_scale))

                    if y_change != 0.0:
                        surf = transform.scale(old_window, window_size)
                        main_window.blit(surf, (0,0))

                    main_window.blit(window, (0, y_change * window_size[1]))
                    tower_handler.show_desc(main_window, playing_grid)
                    display.update()

                    y_change -= y_change * 5 * dt
                    if y_change > -0.0001: y_change = 0

                enemy_handler.set_enemy_path()
                y_change = 0

                # --------------------------------------------
                # Fight!
                # --------------------------------------------

                restart = False
                tower_handler.reset()

                offset, window, window_size, game_window, game_size, game_scale = resize(window_size, main_window, game_window, game_size)

                while not restart:

                    # Must be at start
                    offset, window, window_size, game_window, game_size, game_scale = resize(window_size, window, game_window, game_size)
                    mouse_extras.update(game_scale, playing_grid, offset)
                    message_surf = Surface((game_size[0], math.ceil(game_scale)))

                     # Clear/set up window(s)
                    show_background(background)
                    message_surf.fill((150, 150, 150))

                    # Do we want to restart the game?
                    if key.get_pressed()[K_r] and False:
                        enemy_handler.load_enemies(enemies)
                        money -= enemy_handler.added_money
                        enemy_handler.added_money = 0
                        restart = True
                        break

                    tower_handler.draw_selection_block(game_window, game_scale, game_grid, tower_select_rows)

                    # Do important things
                    dt = clock.tick() / 1000

                    # Update towers
                    tower_handler.update_towers(game_window, game_scale, game_grid, dt)

                    # Update enemies
                    fin, money = enemy_handler.update_enemies(game_window, game_scale, game_grid, dt, money)

                    if fin:
                        state = 0
                        dead = True
                        break

                    if enemy_handler.enemies == []:
                        complete = True
                        break

                    tower_handler.show_external(game_window, game_scale, dt)

                    # Do the damage
                    enemy_handler.enemies = tower_handler.do_damage(enemy_handler.enemies, game_scale)

                    # Message board
                    gfunc.show_message('Enemies left: ' + str(len(enemy_handler.enemies)), message_surf, pos = 'left', size = game_scale * 0.4, border = 1)
                    gfunc.show_message('Money: ' + str(money), message_surf, colour = (70, 70, 70), border = 0.3, pos = 'right', size = 0.4 * game_scale)

                    # Fancy
                    show_dev_things()

                    # Must be at end
                    window.fill((30, 30, 30))
                    window.blit(game_window, offset)
                    window.blit(message_surf, (offset[0], offset[1] - game_scale))

                    # Pause button
                    gfunc.update_keys(key)
                    val = pause(window_size)

                    if val:
                        if val[0] == 'done':
                            y_change = 0
                            window_size = val[1]
                            offset, main_window, window_size, game_window, game_size, game_scale = resize(window_size, main_window, game_window, game_size)
                            continue
                        else: return val

                    display.update()

        # ----------------------------
        # Final screen
        # ----------------------------

        global current_confetti
        current_confetti = []

        # Update user progress
        if not restart:
            if state == 1:

                user_data = pickle.load(open('user_data', 'rb'))
                user_data['level'] += 1

                # Save file
                file = open('user_data', 'wb')
                pickle.dump(user_data, file)
                file.close()

        window_y = window_size[1]
        while not restart:

            # Must be at start
            offset, window, window_size, game_window, game_size, game_scale = resize(window_size, window, game_window, game_size)
            mouse_extras.update(game_scale, playing_grid, offset)
            message_surf = Surface((game_size[0], math.ceil(game_scale)))

             # Clear/set up window(s)
            show_background(background)
            message_surf.fill((150, 150, 150))

            # Do we want to restart the game?
            if key.get_pressed()[K_r]:
                enemy_handler.load_enemies(enemies)
                restart = True
                break

            # Show tower selection thing
            tower_handler.draw_selection_block(game_window, game_scale, game_grid, tower_select_rows)

            # Do important things
            dt = clock.tick() / 1000

            # Show towers
            tower_handler.show_towers(game_window, game_scale, dt)

            # Update enemies
            enemy_handler.update_enemies(game_window, game_scale, game_grid, dt, money)

            # Show death window
            if state == 0:
                value = death_window(game_window, game_size, offset, (0, window_y))

                if value:

                    rect = window.get_rect()
                    surf = Surface((rect.width, rect.height))

                    surf.fill((30, 30, 30))
                    surf.blit(game_window, offset)
                    surf.blit(message_surf, (offset[0], offset[1] - game_scale))

                    if value == 'restart': break
                    if value == 'next': return level + 1, surf
                    if value == 'menu': return 'menu', surf

            elif state == 1:

                next = level < max_levels
                value = win_window(game_window, game_size, offset, (0, window_y), dt, next)

                if value:

                    rect = window.get_rect()
                    surf = Surface((rect.width, rect.height))

                    surf.fill((30, 30, 30))
                    surf.blit(game_window, offset)
                    surf.blit(message_surf, (offset[0], offset[1] - game_scale))

                    if value == 'restart': break
                    if value == 'next': return level + 1, surf
                    if value == 'menu': return 'menu', surf


            # Move death window
            max_height = -game_scale * tower_select_rows / 2
            window_y -= dt * max((window_y - max_height) * 10, 1)

            window_y = max(window_y, max_height)

            # Message board
            gfunc.show_message('Enemies left: ' + str(len(enemy_handler.enemies)), message_surf, pos = 'left', size = game_scale * 0.4, border = 1)
            gfunc.show_message('Money: ' + str(money), message_surf, colour = (70, 70, 70), border = 0.3, pos = 'right', size = 0.4 * game_scale)

            # Must be at end
            window.fill((30, 30, 30))
            show_dev_things()
            window.blit(game_window, offset)
            window.blit(message_surf, (offset[0], offset[1] - game_scale))

            display.update()

        money = level_info['start_money']
        enemy_handler.added_money = 0
        tower_handler.clear_towers()


base_font = font.SysFont('arial', 100)
def death_window(window, window_size, window_offset, offset):

    background_colour = (120, 120, 120)
    text_colour = (255, 255, 255)

    scale = min(window_size)
    margin_x = scale / 8
    margin_y = scale / 15

    width = scale / 16 * 16
    height = scale / 16 * 9

    window_rect = [(window_size[0] - width) / 2 + offset[0], (window_size[1] - height) / 2 + offset[1], width, height]
    draw.rect(window, background_colour, window_rect)

    # Show header and get scale etc
    header = "Not So Good Job"

    max_width = width - margin_x * 2
    max_height = height - margin_y * 2

    test = base_font.render(header, 0, (0, 0, 0))
    test_rect = test.get_rect()

    width_scale = max_width / test_rect.width
    height_scale = max_height / test_rect.height

    scale = min(width_scale, height_scale)

    new_font = font.SysFont('arial', int(100 * scale))
    header_message = new_font.render(header, 0, text_colour)

    window.blit(header_message, (window_rect[0] + margin_x, window_rect[1] + margin_y))


    # Buttons
    width = 10000 * scale
    # restart = gfunc.text_button(window, window_size, window_offset, 'Restart', text_colour + (200,), (window_rect[0] + (window_rect[2] - width) / 2, window_rect[1] + window_rect[3] * 0.6, width, height))

    # Height ratios
    heights = [1, 1]
    max_height = 200 * scale
    margin = 0.0001

    # draw.rect(window, (100, 100, 255), (window_rect[0], window_rect[1] + window_rect[3] - max_height, window_rect[2], max_height))

    # Make ratio add to 1
    scale = 1 / (sum(heights) + margin * len(heights))

    for index in range(len(heights)):
        heights[index] = heights[index] * scale * max_height

    # Just makes it easy to loop through
    buttons = [('Restart', 'restart'), ('Menu', 'menu')]

    y_height = 0
    for index in range(len(buttons)):
        name, func = buttons[index]

        height = heights[index]

        y = window_rect[1] + window_rect[3] * 0.4 + y_height + height# * 0.5
        y_height += height

        g_value = 220
        if gfunc.text_button(window, window_size, window_offset, name, (g_value, g_value, g_value), (window_rect[0] + window_rect[2] / 2, y, width, height), alignment = 'center'): return func


current_confetti = []
last_time = 0
def win_window(window, window_size, window_offset, offset, dt, next):

    # Confetti

    # Make more
    global last_time

    while last_time > 1:
        scale = random.random()
        size = max(scale * 0.1, 0.045)

        while True:
            # Make colour look good
            colour = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            vibrance = abs(colour[0] - colour[1]) + abs(colour[1] - colour[2]) + abs(colour[2] - colour[0])

            # Only continue if colour is a good colour
            if vibrance > 200:
                break

        current_confetti.append([[random.random(), -1, size * 0.3, size], (1 + scale * 8) / 7, colour])
        last_time -= 1

    last_time += dt * 150

    # Show all
    width = min(window_size) / 100

    for rect, speed, colour in current_confetti:
        rect = rect[0] * window_size[0], rect[1] * window_size[1], rect[2] * window_size[0], rect[3] * window_size[1]
        draw.rect(window, colour, rect)

    # Move all
    for index in range(len(current_confetti)):
        current_confetti[index][0][1] += dt * current_confetti[index][1]

    # Delete if not on screen
    for confetti in current_confetti:
        if confetti[0][1] > 1:
            index = current_confetti.index(confetti)
            current_confetti.pop(index)


    background_colour = (120, 120, 120)
    text_colour = (255, 255, 255)

    scale = min(window_size)
    margin_x = scale / 8
    margin_y = scale / 15

    width = scale / 16 * 16
    height = scale / 16 * 9

    window_rect = [(window_size[0] - width) / 2 + offset[0], (window_size[1] - height) / 2 + offset[1], width, height]
    draw.rect(window, background_colour, window_rect)


    # Show header and get scale etc
    header = "Good Job!"

    max_width = width - margin_x * 2
    max_height = height - margin_y * 2

    test = base_font.render(header, 0, (0, 0, 0))
    test_rect = test.get_rect()

    width_scale = max_width / test_rect.width
    height_scale = max_height / test_rect.height

    scale = min(width_scale, height_scale)

    new_font = font.SysFont('arial', int(100 * scale))
    header_message = new_font.render(header, 0, text_colour)

    window.blit(header_message, (window_rect[0] + margin_x, window_rect[1] + margin_y))

    # Buttons
    width = 175 * scale
    # restart = gfunc.text_button(window, window_size, window_offset, 'Restart', text_colour + (200,), (window_rect[0] + (window_rect[2] - width) / 2, window_rect[1] + window_rect[3] * 0.6, width, height))

    # Height ratios
    max_height = scale * 100
    margin = 0.0

    # draw.rect(window, (100, 100, 255), (window_rect[0], window_rect[1] + window_rect[3] - max_height, window_rect[2], max_height))

    # Just makes it easy to loop through
    if next: buttons = [('Next level', 'next'), ('Restart', 'restart'), ('Menu', 'menu')]; heights = [0.1, 0.1, 0.1]
    else: buttons = [('Menu', 'menu'), ('Restart', 'restart')]; heights = [2, 2]

    # Make ratio add to 1
    scale = 1 / (sum(heights) + margin * len(heights))

    for index in range(len(heights)):
        heights[index] = heights[index] * scale * max_height

    for index in range(len(buttons)):
        name, func = buttons[index]

        height = heights[index]

        y_height = (index / len(buttons) * min(window_size)) * 0.2
        y = window_rect[1] + window_rect[3] * 0.6 + y_height

        g_value = 220
        scale = 1.5
        if gfunc.text_button(window, window_size, window_offset, name, (g_value, g_value, g_value), (window_rect[0] + window_rect[2] / 2, y, width * scale, height * scale), alignment = 'center'):
            return func


