

class _Configuration(object):
    """Fetch a client configuration.
    """

    def __init__(self, client):
        """Load the configuration for the specified client.
        """
        # Set up the default configuration
        self.host = 'ec2'
        self.keys = _Keys(api = 'test-api-key',
            secret = 'test-api-secret')


class _Keys(object):
    """Used for storage of keys.
    """

    def __init__(self, **kwargs):
        """Load the specified key values.
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
