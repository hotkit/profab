"""Plugins that allow the AMI to be chosen.
"""
from profab.role import Role


class Configure(Role):
    """Allows the AMI to be specified at the command line.
    """
    def ami(self, _region, _bits, _size):
        """Return the AMI that was passed in to the role.
        """
        return self.parameter
