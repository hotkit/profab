from profab import _Configuration


class Server(object):
    """Represents a server. Do not construct these instances directly,
    use one of the methods `start` or `connect`.
    """

    @classmethod
    def start(kls, client, *roles, **conections):
        """Start a server for the specified client with the given roles
        and connected the provided services.
        """
        config = _Configuration(client)


    @classmethod
    def connect(kls, hostname):
        """Connect to a given server by the provided hostname.
        """
        pass

