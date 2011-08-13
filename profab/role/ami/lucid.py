"""Plugins that allow the AMI to be chosen.
"""
from profab.role import Role


class AddRole(Role):
    """Returns the right Lucid AMI name.
    """
    def ami(self):
        """Return the AMI that was passed in to the role.
        """
        return 'ami-2cc83145'
