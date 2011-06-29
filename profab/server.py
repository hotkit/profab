"""This module handles the connection to the virtual machines running on EC2.
"""
import time

from fabric.api import settings, sudo, reboot, run
from fabric.contrib.files import append
from fabric.state import connections
from boto.ec2 import regions
from boto.ec2.connection import EC2Connection

from profab import _Configuration, _logger
from profab.authentication import get_keyname, get_private_key_filename


def _on_this_server(function):
    """Private decorator to wrap methods which require fabric configuration.
    """
    def wrapper(server, *args, **kwargs):
        """Wrapped method
        """
        keyfile = get_private_key_filename(server.config, server.cnx)
        with settings(host_string=server.instance.dns_name, user='ubuntu',
                key_filename=keyfile):
            function(server, *args, **kwargs)
    return wrapper


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


    def __str__(self):
        return u"%s (%s) [%s] %s" % (
            self.instance.dns_name, self.instance.key_name,
            ', '.join([g.groupName for g in self.instance.groups]),
            self.instance.tags)


    @classmethod
    def start(cls, client, *roles):
        """Start a server for the specified client with the given roles
        and connect the requested services.
        """
        config = _Configuration(client)
        _logger.info("New server for %s on %s with roles %s",
            config.client, config.host, roles)
        cnx = EC2Connection(config.keys.api, config.keys.secret)
        image = cnx.get_all_images('ami-2cc83145')[0]
        reservation = image.run(instance_type='t1.micro',
            key_name=get_keyname(config, cnx),
            security_groups=['default'])
        _logger.debug("Have reservation %s for new server with instances %s",
            reservation, reservation.instances)
        server = Server(config, cnx, reservation.instances[0])
        while server.instance.state == 'pending':
            _logger.info("Waiting 10s for instance to start...")
            time.sleep(10)
            server.instance.update()
        _logger.info("Instance state now %s with name %s."
            " Waiting 30s for machine to boot.", server.instance.state,
            server.instance.dns_name)
        time.sleep(30)
        server.dist_upgrade()
        return server


    @classmethod
    def get_all(cls, client):
        """Connects to each region in turn and fetches all of the instances
        currently running."""
        servers = []
        config = _Configuration(client)
        region_list = regions(aws_access_key_id=config.keys.api,
            aws_secret_access_key=config.keys.secret)
        for region in region_list:
            _logger.info("Searching %s", region)
            cnx = region.connect(aws_access_key_id=config.keys.api,
                aws_secret_access_key=config.keys.secret)
            for reservation in cnx.get_all_instances():
                _logger.info("Found %s", reservation)
                for instance in reservation.instances:
                    servers.append(Server(config, cnx, instance))
        return servers


    @classmethod
    def connect(cls, client, hostname):
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


    @_on_this_server
    def reboot(self):
        """Reboot this server.
        """
        reboot(30)
        del connections[self.instance.dns_name]


    @_on_this_server
    def install_packages(self, *packages):
        """Install the specified packages on the machine.
        """
        # The decorator requires this to be an instance method
        # pylint: disable=R0201
        package_names =  ' '.join(packages)
        _logger.info("Making sure the following packages are installed: %s",
            package_names)
        sudo('apt-get install %s' % package_names)


    @_on_this_server
    def dist_upgrade(self):
        """Perform a dist-upgrade and make sure the base packages are installed.
        """
        _logger.info("First ensure all keys are on server")
        key_file = '~/.ssh/authorized_keys'
        authorized_keys = run('cat %s' % key_file)
        for key in self.config.ssh.ubuntu:
            if key.split()[2] not in authorized_keys:
                append(key_file, key)
        _logger.info("Starting dist-upgrade sequence for %s", self.instance)
        sudo('apt-get update')
        sudo('apt-get dist-upgrade -y')
        self.reboot()
        self.install_packages('byobu', 'update-notifier-common')


    def terminate(self):
        """Terminate the server waiting for it to shut down.
        """
        self.instance.terminate()
        while self.instance.state != 'terminated':
            _logger.info("Wating 10s for instance to stop...")
            time.sleep(10)
            self.instance.update()
        _logger.info("Instance state now %s", self.instance.state)

