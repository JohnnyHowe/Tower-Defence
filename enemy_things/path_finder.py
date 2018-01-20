'''
-1: obstacle
None: empty
0: start
>1: dist from start
'''

def get_path(blocks, grid_size):

    grid_size = list(grid_size)
    grid_size[0] += 1

    grid = [[None for y in range(grid_size[1])] for x in range(grid_size[0])]

    candidates = []

    for block in blocks:
        grid[block.pos[0]][block.pos[1]] = -1

    for y in range(grid_size[1]):
        if grid[0][y] == None:
            grid[0][y] = 0        
            candidates.append((0, y, 0))

    #candidates = [(0,0,0)]
    #grid[0][0] = 0

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while True:

        if len(candidates) == 0:
            return False

        current = candidates.pop(0)

        for opt in directions:
            new_pos = opt[0] + current[0], opt[1] + current[1]
            
            # is it in a valid spot?
            
            # is it on the grid
            if new_pos[0] >= 0 and new_pos[0] <= grid_size[0] - 1:
                if new_pos[1] >= 0 and new_pos[1] <= grid_size[1] - 1:
                    
                    # is the spot empty?
                    if grid[new_pos[0]][new_pos[1]] == None:
                        candidates.append(new_pos + (current[2] + 1,))
                        
                        grid[new_pos[0]][new_pos[1]] = current[2] + 1

            
        if len(candidates) == 0:
            return False

        stop = False
        for y in range(grid_size[1]):
            if grid[grid_size[0] - 1][y]:
                stop = True
                break
        if stop: break

    # backtrack to find path

    # Find end pos with lowest value
    end_x = grid_size[0] - 1

    lowest = None
    pos = None
    
    for y in range(grid_size[1]):
        value = grid[end_x][y]

        if type(value) == int:

            if not type(lowest) == int:
                lowest = value
                pos = (end_x, y)

            elif value < lowest:
                lowest = value
                pos = (end_x, y)
    
    positions = [pos]
    moves = grid[pos[0]][pos[1]]

    for move in range(moves):
        last_pos = positions[len(positions) - 1]
        number = moves - move

        for opt in directions:
            new_pos = opt[0] + last_pos[0], opt[1] + last_pos[1]

            # Check new pos
            if new_pos[0] >= 0 and new_pos[0] <= grid_size[0] - 1:
                if new_pos[1] >= 0 and new_pos[1] <= grid_size[1] - 1:
            
                    if grid[new_pos[0]][new_pos[1]] == number - 1:
                        positions.append(new_pos)
                        break

    last_pos = positions[len(positions) - 1]
    new = list(last_pos); new[0] -= 1
    positions.append(new)

    positions.reverse()
    
   # Adding more points onto the end so the enemies don't stop
    for extra_pos in range(5):
        last = list(positions[len(positions) - 1])
        pos = last[0] + 1, last[1]
        positions.append(pos)

    return positions
