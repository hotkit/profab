"""Plugin that allows the bits for the operating system to be set.
"""
from profab.role import Role


class AddRole(Role):
    """Automatically determine the number of bits to use from
    AMI size type. This role is added automatically.
    """
    def bits(self, size):
        """Return the number of bits to use by default.
        """
        if size in ['t1.micro', 'c1.medium', 'm1.small']:
            return '32'
        else:
            return '64'


class Configure(Role):
    """Allows the number of bits to run at to be chosen.
    """
    def bits(self, size):
        """Return the number of bits specified.
        """
        return self.parameter
