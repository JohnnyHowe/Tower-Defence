import math
from engine.vector2 import Vector2


class Node:

    position = None
    parent = None
    cost = None

    def __init__(self, position, parent, cost):
        self.position = position
        self.parent = parent
        self.cost = cost

    def __eq__(self, other):
        return self.position == other.position

    def __str__(self):
        return "Node(({}, {}), {})".format(self.position.x, self.position.y, self.cost)

    def __repr__(self):
        return self.__str__()


class _PathFinder:

    board = None
    candidates = None
    visited = None
    destination_x = None
    final_node = None

    def find_path(self, board):
        self._setup(board)

        while self.candidates and self.final_node is None:
            self._process_next()

        return self._get_path_backtrack()

    def _setup(self, board):
        """ Set the board, candidates, visited and destination. """
        self.board = board
        self.candidates = [Node(Vector2(-1, y), None, 0.0) for y in range(board.size.y)]  # candidate = (pos, cost)
        self.visited = [i.position for i in self.candidates]
        self.destination_x = self.board.size.x - 1
        self.final_node = None

    def _process_next(self):
        """ Pop the next candidate from self.candidates.
        If candidate is at destination, set final node, otherwise add neighbours to candidates if appropriate. """
        self.candidates.sort(key=lambda x: -x.cost)
        candidate = self.candidates.pop()

        if candidate.position.x == self.destination_x:
            self.final_node = candidate
            return

        for neighbour in self._get_neighbours(candidate):
            if neighbour.position not in self.visited:
                self.candidates.append(neighbour)

        self.visited.append(candidate.position)

    def _get_neighbours(self, node):
        """ Get the empty neighbouring cells. """
        neighbours = []
        # for dx in range(-1, 2):
        #     for dy in range(-1, 2):
        #         if not (dx == 0 and dy == 0):   # Don't count the cell itself
        #             position = node.position + Vector2(dx, dy)
        #             if self.board.is_on_board(position):
        #                 if self.board.get_cell_contents(position) is None:
        #                     neighbours.append(Node(position, node, math.sqrt(abs(dx) + abs(dy))))
        for change in [Vector2(-1, 0), Vector2(1, 0), Vector2(0, 1), Vector2(0, -1)]:
            position = node.position + change
            if self.board.is_on_board(position):
                if self.board.get_cell_contents(position) is None:
                    neighbours.append(Node(position, node, node.cost + 1))
        return neighbours

    def _get_path_backtrack(self):
        """ Backtrack from the final_node to create the full path. is returned """
        path = []
        current = self.final_node
        while current:
            path.append(current.position)
            current = current.parent
        return list(reversed(path))


PathFinder = _PathFinder()
