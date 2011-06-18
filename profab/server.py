import time
from boto.ec2.connection import EC2Connection

from profab import _Configuration, _logger


class Server(object):
    """Represents a server. Do not construct these instances directly,
    use one of the methods `start` or `connect`.
    """

    def __init__(self, config, cnx, instance):
        """The constructor is called by either `start` or `connect`.
        DO NOT CALL DIRECTLY.
        """
        self.config = config
        self.cnx = cnx
        self.instance = instance


    @classmethod
    def start(kls, client, *roles, **conections):
        """Start a server for the specified client with the given roles
        and connect the requested services.
        """
        config = _Configuration(client)
        _logger.info("New server for %s on %s with roles %s",
            config.client, config.host, roles)
        cnx = EC2Connection(config.keys.api, config.keys.secret)
        image = cnx.get_all_images('ami-245fac4d')[0]
        reservation = image.run(instance_type='t1.micro')
        _logger.debug("Have reservation %s for new server with instances %s",
            reservation, reservation.instances)
        server = Server(config, cnx, reservation.instances[0])
        while server.instance.state == 'pending':
            _logger.debug("Waiting 10s for instance to start...")
            time.sleep(10)
            server.instance.update()
        _logger.info("Instance state now %s with name %s",
            server.instance.state, server.instance.dns_name)


    @classmethod
    def connect(kls, client, hostname):
        """Connect to a given server by the provided hostname.

        If a matching server cannot be found then return None.
        """
        config = _Configuration(client)
        cnx = EC2Connection(config.keys.api, config.keys.secret)
        reservations = cnx.get_all_instances()
        _logger.debug("Found  %s", reservations)
        for reservation in reservations:
            instance = reservation.instances[0]
            if instance.dns_name == hostname:
                _logger.info("Found %s", instance)
                return Server(config, cnx, instance)
        return None
