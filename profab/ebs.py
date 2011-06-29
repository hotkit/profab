"""Handle EBS volumes.
"""

from profab import _logger


class Volume(object):
    """A single EBS volume.
    """
    def __init__(self, server, ec2_volume, device):
        self.attached = False
        self.device = device
        self.server = server
        self.volume = ec2_volume


    @classmethod
    def create(cls, server, size, device="/dev/sdx"):
        """Create a new volume on the provided connection.
        """
        _logger.info("Creating volume size %dGB on %s",
            size, server.instance.placement)
        volume = Volume(server, server.cnx.create_volume(
            size, server.instance.placement), device)
        _logger.info("Attaching volume %s to %s as %s",
            volume.volume, server.instance, device)
        volume.attached = volume.volume.attach(server.instance.id, device)
        return volume
