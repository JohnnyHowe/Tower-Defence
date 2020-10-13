
class Projectile:

    board = None

    def __init__(self, board):
        self.board = board

    def show(self):
        """ Show the projectile. """
        print("Projectile has no show function")

    def update(self):
        """ Update the projectile. """
        print("Projectile has no update function")

    def is_valid(self):
        """ Is the projectile still valid?
        If False, projectile is removed. """
        print("Projectile has no is_valid function")
