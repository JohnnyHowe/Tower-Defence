from pygame import *
import time


def update_states():

    global states, old_state

    try:
        new_state = mouse.get_pressed()

        for state_i in range(len(states)):
            states[state_i] = new_state[state_i] - old_state[state_i]

        old_state = new_state

    except:

        states = [0,0,0]
        old_state = [0,0,0]



def update_buttons():
    global buttons
    buttons = mouse.get_pressed()

def update(window_scale, game_grid, offset):
    update_states()
    update_pos(window_scale, game_grid, offset)
    update_buttons()

def get_pressed():
    global buttons
    return(list(buttons))

def get_states():
    global states
    return list(states)

def update_pos(window_scale, game_grid, offset):
    pos = list(mouse.get_pos())
    pos[0] /= window_scale
    pos[1] /= window_scale

    pos[0] -= offset[0] / window_scale
    pos[1] -= offset[1] / window_scale

    pos[0] = int(pos[0])
    pos[1] = int(pos[1])

    pos[0] = max(min(pos[0], game_grid[0] - 1), 0)
    pos[1] = max(min(pos[1], game_grid[1] - 1), 0)

    global rounded_pos
    rounded_pos = list(pos)

def get_pos():
    global rounded_pos
    return list(rounded_pos)