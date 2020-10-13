
class _ProjectileManager:
    """ Class to manage projecticles """

    projectiles = None

    def __init__(self):
        self.projectiles = []

    def add_projectile(self, projectile):
        self.projectiles.append(projectile)

    def show_projectiles(self):
        for projectile in self.projectiles:
            projectile.show()

    def update(self):
        """ Remove all projectiles that aren't valid. """
        new_projectiles = []
        for projectile in self.projectiles:
            if projectile.is_valid():
                new_projectiles.append(projectile)
        self.projectiles = new_projectiles


ProjectileManager = _ProjectileManager()
