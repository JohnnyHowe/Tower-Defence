from pygame import *
import global_functions as gfunc
import mouse_extras, level_select

def run(window_size):

    init()
    display.set_caption('Tower Defence!')
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

    old_window = None

    while True:

        screen, window_size, window_scale = resize(screen, window_size)
        window = Surface(window_size)
        mouse_extras.update_buttons()
        mouse_extras.update_states()
        window.fill((150, 150, 150))

        # Show welcome message
        win_rect = window.get_rect()
        message = 'Generic Tower Defence Game!'
        margin = window_scale * 0.1

        test_rect = test_font.render(message, 0, (0,0,0)).get_rect()
        scale = min(win_rect.width / (test_rect.width + 2 * margin), win_rect.height / (test_rect.height + 2 * margin), win_rect.height / 200)

        new_font = font.SysFont('arial', int(scale * 100))
        message_surf = new_font.render(message, 0, (255, 255, 255))
        message_rect = message_surf.get_rect()

        # Center
        x = (window_size[0] - message_rect.width) / 2
        window.blit(message_surf, (x, margin))

        # draw.line(window, (0,0,0), (0,window_size[1] / 2),(window_size[0], window_size[1] /2))

        scale = 0.2
        x, y = window_size[0] / 2, window_size[1] * 0.75
        width, height = window_size[0] * scale, window_size[1] * scale

        k = key.get_pressed()
        if gfunc.text_button(window, window_size, (0,0), 'Start', (200, 200, 200), (x - width / 2, y - height / 2, width, height)) or k[K_RETURN]:
            old_window = level_select.run(window_size, window); offset2 = 0
            rect = old_window.get_rect()
            window_size = rect.width, rect.height

        screen.blit(window, (0, 0))
        display.update()
