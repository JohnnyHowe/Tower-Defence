import math
from engine.vector2 import Vector2


class PathFinder:

    def get_path(self, board):
        """ Using bfs, find the best path from x = -1, to x = board.w.
        Best path in form of array of node positions. """
        # candidates = [(Vector2(-1, y), 0) for y in range(board.size.y)]  # candidate = (pos, cost)
        # desintations = [Vector2(board.size.x, y) for y in range(board.size.y)]
        #
        # final_node = None
        #
        # while candidates and final_node is None:
        #     candidate, cost = candidates.pop()
        #
        #     # Is this candidate a destination?
        #     if candidate in desintations:
        #         final_node = candidate
        #
        #     # For each neighbour
        #     for dx in range(-1, 2):
        #         for dy in range(-1, 2):
        #             if dx == 1 and dy == 1:
        #                 continue
        #
        #             # Is the neighbour a valid spot? - Nothing there and not a current candidate
        #             position = candidate + Vector2(dx, dy)
        #             if board.get_cell_contents(position) is None and NOT A CURRENT CANDIDATE:
        #                 new_cost = cost + math.sqrt(dx + dy)
        #                 # insert into list
        #
        #
        # # Backtrack from final node to get path

