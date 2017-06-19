"""Allow the volume to be set.
"""
from profab.role import Role
from boto.ec2.blockdevicemapping import BlockDeviceMapping, BlockDeviceType


class Configure(Role):
    """Used to determine the volume that a machine is launched in.
    """
    def volume(self):
        """Return the BlockDeviceMapping that was passed in to the role.
        """

        dev_sda1 = BlockDeviceType()
        dev_sda1.size = self.parameter
        bdm = BlockDeviceMapping()
        bdm['/dev/sda1'] = dev_sda1

        return bdm
