import math
from engine.vector2 import Vector2


def get_path(board):
    """ Using bfs, find the best path from x = -1, to x = board.w.
    Best path in form of array of node positions. """
    candidates = [Node(Vector2(-1, y), None, 0.0) for y in range(board.size.y)]  # candidate = (pos, cost)
    seen = [i.position for i in candidates]

    final_node = None

    while candidates and final_node is None:
        candidates.sort(key=lambda x: -x.cost)
        candidate = candidates.pop()
        print(candidate.position)

        # Is this candidate a destination?
        if candidate.position.x == 9:
            final_node = candidate

        # For each neighbour
        for node in get_neighbours(candidate, board):

            # Is the neighbour a valid spot? - Nothing there and not a current candidate
            if node.position not in seen:
                seen.append(node.position)

                # insert into list
                # TODO make less inneficient
                candidates.append(node)

    if final_node:
        # Backtrack from final node to get path
        current = final_node
        path = [current.position]
        while current.parent:
            path.append(current.parent.position)
            current = current.parent
    else:
        path = []

    return reversed(path)


def get_neighbours(node, board):
    """ Get the empty neighbouring cells. """
    neighbours = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if not (dx == 0 and dy == 0):   # Don't count the cell itself
                position = node.position + Vector2(dx, dy)
                if board.is_on_board(position):
                    if board.get_cell_contents(position) is None:
                        neighbours.append(Node(position, node, math.sqrt(abs(dx) + abs(dy))))
    return neighbours



class Node:

    position = None
    parent = None
    cost = None

    def __init__(self, position, parent, cost):
        self.position = position
        self.parent = parent
        self.cost = cost

    def __str__(self):
        return "Node({}, {})".format(self.position.x, self.position.y)

    def __repr__(self):
        return self.__str__()


