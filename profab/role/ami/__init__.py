"""Plugins that allow the AMI to be chosen.
"""
from profab.role import Role


class Configure(Role):
    """Adds a Munin node to a server.
    """
    def ami(self, _region, _bits, _size):
        """Return the AMI that was passed in to the role.
        """
        return self.parameter


class ChooseAMI(Role):
    """Returns the correct AMI for a given Ubuntu version.
    """
    def ami(self, region, bits, size):
        """Return a suitable AMI.
        """
        # The AMIS member needs to be provided by the sub-class
        # pylint: disable = E1101
        disk = 'ebs' if size == 't1.micro' else 'instance'
        return self.AMIS[str(bits)][disk].get(region, None)

