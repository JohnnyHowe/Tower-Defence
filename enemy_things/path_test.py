from pygame import *
import path_finder

game_grid = (6,6)
scale = 50

class Block:
    def __init__(self, pos):
        self.pos = pos

blocks = [Block((3,0))]

init()
window = display.set_mode((game_grid[0] * scale, game_grid[1] * scale))

path = path_finder.get_path(blocks, game_grid)

while True:
    for i in event.get():
        if i.type == QUIT: quit()
        if i.type == MOUSEBUTTONDOWN:
            m_pos = mouse.get_pos()
            x = int(m_pos[0] / scale)
            y = int(m_pos[1] / scale)
            blocks.append(Block((x,y)))
            path = path_finder.get_path(blocks, game_grid)
            
    window.fill((255,255,255))

    for block in blocks:
        draw.rect(window, (0,0,0), (block.pos[0] * scale, block.pos[1] * scale, scale, scale))

    for x,y in path:
        draw.circle(window, (100,100,0), (int(x * scale + scale / 2), int(y * scale + scale / 2)), 5)

    display.update()
