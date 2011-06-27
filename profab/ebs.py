"""Handle EBS volumes.
"""


class Volume(object):
    """A single EBS volume.
    """

    @classmethod
    def create(cls, connection, size):
        """Create a new volume on the provided connection.
        """
        return "volume"
