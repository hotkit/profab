"""Handle EBS volumes.
"""


class Volume(object):
    """A single EBS volume.
    """
    def __init__(self, ec2_volume):
        self.volume = ec2_volume


    @classmethod
    def create(cls, connection, zone, size):
        """Create a new volume on the provided connection.
        """
        return Volume(connection.create_volume(size, zone))
