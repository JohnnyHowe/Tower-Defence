from pygame import *
import mouse_extras, pickle, math, game
import global_functions as gfunc


def run(window_size, old_window):

    scroll = 0

    offset = [0, window_size[1]]

    init()
    screen = display.set_mode(window_size, RESIZABLE)
    test_font = font.SysFont('arial', 100)
    clock = time.Clock()

    def resize(window, window_size):
        new = gfunc.event_loop()

        if new:
            window = display.set_mode(new, RESIZABLE)
            scale = min(new)
            return window, new, scale
        else:
            return window, window_size, min(window_size)


    def level_button(number, window, window_size, window_scale, pos, valid, show = True):
        height = window_scale * 0.15

        if valid:
            if gfunc.text_button(window, window_size, (0,0), str(number), (255, 255, 255), (pos[0], pos[1], height, height), alignment = 'center'):
                return True
        else:
            gfunc.text_button(window, window_size, (0,0), str(number), (150, 150, 150), (pos[0], pos[1], height, height), alignment = 'center')


    level_info = pickle.load(open('levels', 'rb'))
    levels = len(level_info)
    max_columns = 5

    # User data
    user_data = pickle.load(open('user_data', 'rb'))

    while True:

        screen, window_size, window_scale = resize(screen, window_size)
        window = Surface(window_size)
        window.fill((130, 130, 130))
        dt = clock.tick() / 1000

        x_dist = window_size[0] / (min(max_columns, levels) + 1)
        rows = math.ceil(levels / max_columns)

        if rows > 0: y_dist = window_size[1] / (rows + 1)
        else: y_dist = 0

        y_dist = max(y_dist, window_scale * 0.2)

        # Scroll
        mouse_pos = mouse.get_pos()
        s = 200
        if mouse_pos[1] >= window_size[1] * 0.8:
            scroll += s * dt
        if mouse_pos[1] <= window_size[1] * 0.2:
            scroll -= s * dt

        max_s = 0.15 * window_scale + y_dist * (rows - 5)
        scroll = max(0, scroll)
        scroll = min(max_s, scroll)

        if rows < 5:
            scroll = 0

        offset[1] -= dt * offset[1] * 5
        offset[1] = max(0, offset[1])

        # So it does stop
        if offset[1] < 1:
            offset[1] = 0

        mouse_extras.update_buttons()
        mouse_extras.update_states()

        screen.blit(transform.scale(old_window, window_size), (0,0))
        # draw.rect(screen, (120, 120, 120), (0, offset[1] - 10, window_size[0], window_size[1]))

        k = key.get_pressed()
        button_pressed = None
        ret = None

        for level_num in range(levels):

            y = int(level_num / max_columns)
            x = level_num - y * max_columns

            x += 1
            y += 1

            x *= x_dist

            if y_dist == 0:
                y += window_size[1] / 2
            else:
                y *= y_dist

            y -= scroll
            level_num += 1

            valid = user_data['level'] + 1 >= level_num

            if level_button(level_num, window, window_size, window_scale, (x, y), valid):
                button_pressed = level_num

        if button_pressed:
            val, surf = game.run(button_pressed, levels, window_size, window)
            user_data = pickle.load(open('user_data', 'rb'))

            rect = surf.get_rect(); window_size = rect.width, rect.height
            screen = display.set_mode(window_size, RESIZABLE)

            if type(val) == int: game.run(val, levels, window_size, surf)
            user_data = pickle.load(open('user_data', 'rb'))
            continue

        while True:
            if type(ret) == int:
                ret, new_window = game.run(button_pressed + 1, levels, window_size, new_window)
                user_data = pickle.load(open('user_data', 'rb'))
                rect = new_window.get_rect(); window_size = rect.width, rect.height
            else: break

        if k[K_ESCAPE]:
            return screen

        if k[K_F2]:
            gfunc.show_fps(window)

        screen.blit(window, offset)

        display.update()
