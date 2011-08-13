"""Plugins that allow the AMI to be chosen.
"""
from profab.role import Role


class Configure(Role):
    """Adds a Munin node to a server.
    """
    def ami(self, _region):
        """Return the AMI that was passed in to the role.
        """
        return self.parameter
