"""Handle EBS volumes.
"""

from profab import _logger
import time


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
        device = cls.get_volume(server.get_volumes())
        _loger.info("Used device %s on this server", device)
        volume = cls(server, server.cnx.create_volume(
            size, server.instance.placement), device)
        cls.attach_volume(server.insatance.id, volume, device)
        return volume


    @classmethod
    def creat_from_snapshot(cls, server, snapshot):
        """Create a new volume from snapshot.
        """
        _logger.info("Creating volume from snapshot id %s",
            snapshot.id)
        device = cls.get_device(server.get_volumes())
        _loger.info("Used device %s on this server", device)
        volume = cls(server, snapshot.create_volume(
            server.instance.placement), device)
        _logger.info("Used volume %s size %dGB",
            volume.volume.id, volume.volume.size)
        cls.attach_volume(server.instance.id, volume, device)
        return volume


    @classmethod
    def get_device(cls, volumes)
        used = [v.device for v in volumes]
        devices = [d for d in cls.DEVICES if d not in used]
        _logger.info("Unused devices on this server are %s", devices)
        return devices[0]


    @classmethod
    def attach_volume(cls, server, volume, device)
        #Wait for create volume
        while volume.volume.status == 'creating':
            _logger.info("Waiting 10s for volume to create...")
            time.sleep(10)
            volume.volume.update()
        _logger.info("Volume state now %s with name %s",
            volume.volume.volume_state(), volume.volume)
        _logger.info("Attaching volume %s to %s as %s",
            volume.volume.id, server, device)
        volume.attached = volume.volume.attach(server, device)
