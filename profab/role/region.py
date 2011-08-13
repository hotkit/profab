"""Allow the region to be set.
"""
from profab.role import Role


class Configure(Role):
    """Used to determine the region that a machine is launched in.
    """
    def region(self):
        """Return the region that was passed in to the role.
        """
        return self.parameter
