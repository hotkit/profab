"""Handle EBS volumes.
"""

from profab import _logger


class Volume(object):
    """A single EBS volume.
    """
    def __init__(self, server, ec2_volume, device, attached=False):
        self.attached = attached
        self.device = device
        self.server = server
        self.volume = ec2_volume


    DEVICES = ['/dev/sd%s' % chr(97+c) for c in range(1, 26)] + \
        ['/dev/hd%s' % chr(97+c) for c in range(0, 26)]
    @classmethod
    def create(cls, server, size):
        """Create a new volume on the provided connection.
        """
        _logger.info("Creating volume size %dGB on %s",
            size, server.instance.placement)
        volumes = server.get_volumes()
        used = [v.device for v in volumes]
        devices = [d for d in cls.DEVICES if d not in used]
        _logger.info("Unused devices on this server are %s", devices)
        device = devices[0]
        volume = Volume(server, server.cnx.create_volume(
            size, server.instance.placement), device)
        _logger.info("Attaching volume %s to %s as %s",
            volume.volume, server.instance, device)
        volume.attached = volume.volume.attach(server.instance.id, device)
        return volume
