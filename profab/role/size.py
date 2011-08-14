"""Plugin that allows the instance size to be chosen.
"""
from profab.role import Role


class Configure(Role):
    """Allows a specific size to be chosen.
    """
    def size(self):
        """Return the size that was specified.
        """
        return self.parameter
