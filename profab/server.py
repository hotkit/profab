"""This module handles the connection to the virtual machines running on EC2.
"""
from socket import gaierror, getaddrinfo
import time

from fabric.api import settings, sudo, reboot, run
from fabric.contrib.files import append

from profab import Configuration, _logger
from profab.authentication import get_keyname, get_private_key_filename
from profab.connection import ec2_connect
from profab.ebs import Volume
from profab.ec2 import get_all_reservations


def _on_this_server(function):
    """Private decorator to wrap methods which require fabric configuration.
    """
    def wrapper(server, *args, **kwargs):
        """Wrapped method
        """
        keyfile = get_private_key_filename(server.config, server.cnx)
        with settings(host_string=server.eip or server.instance.dns_name,
                user='ubuntu', key_filename=keyfile, connection_attempts=10):
            function(server, *args, **kwargs)
    return wrapper


class Server(object):
    """Represents a server. Do not construct these instances directly,
    use one of the methods `start` or `connect`.
    """

    def __init__(self, config, reservation, instance):
        """The constructor is called by either `start` or `connect`.

        DO NOT CALL DIRECTLY.
        """
        self.config = config
        self.cnx = reservation.connection
        self.eip = None
        self.instance = instance
        self.reservation = reservation


    def __str__(self):
        return u"%s -- %s (%s) [%s] %s" % (
            self.instance.dns_name or self.reservation.id,
            self.instance.state, self.instance.key_name,
            ', '.join([g.name for g in self.instance.groups]),
            self.instance.tags)


    @classmethod
    def start(cls, client, *roles):
        """Start a server for the specified client with the given roles
        and connect the requested services.

        Roles are passed as either a name or a tuple (name, parameter).
        """
        config = Configuration(client)
        _logger.info("New server for %s on %s with roles %s",
            config.client, config.host, roles)
        roles = [('ami.lucid', None), ('bits', None)] + list(roles)
        role_adders = Server.get_role_adders(*roles)

        # Work out the correct region to use and connect to it
        region = config.region
        for role_adder in role_adders:
            region = role_adder.region() or region
        cnx = ec2_connect(config, region)

        # Work out the machine size to launch and set default run args
        run_args = {
                'key_name': get_keyname(config, cnx),
                'instance_type': 't1.micro',
            }
        for role_adder in role_adders:
            run_args['instance_type'] = role_adder.size() or \
                run_args['instance_type']

        # Calculate how many bits the AMI should be using
        bits = None
        for role_adder in role_adders:
            bits = role_adder.bits(run_args['instance_type']) or bits

        # Find the AMI to use
        ami = None
        for role_adder in role_adders:
            ami = role_adder.ami(region, bits, run_args['instance_type']) or ami

        # Work out the other run arguments we need
        for role_adder in role_adders:
            run_args = role_adder.run_kwargs(run_args)

        # Start the machine
        image = cnx.get_all_images(ami)[0]
        reservation = image.run(**run_args)
        _logger.debug("Have reservation %s for new server with instances %s",
            reservation, reservation.instances)

        # Now we can make the server instance and add the roles
        server = Server(config, reservation, reservation.instances[0])
        for role in role_adders:
            role.started(server)

        # Wait for it to start up
        while server.instance.state == 'pending':
            _logger.info("Waiting 10s for instance to start...")
            time.sleep(10)
            server.instance.update()
        _logger.info("Instance state now %s with name %s.",
            server.instance.state, server.instance.dns_name)

        # Upgrade it and configure it
        server.dist_upgrade()
        server.add_roles(role_adders)

        return server


    @classmethod
    def get_all(cls, client):
        """Connects to each region in turn and fetches all of the instances
        currently running."""
        servers = []
        config = Configuration(client)
        for reservation in get_all_reservations(config):
            for instance in reservation.instances:
                servers.append(Server(config, reservation, instance))
        return servers


    @classmethod
    def connect(cls, client, hostname):
        """Connect to a given server by the provided hostname.

        If a matching server cannot be found then return None.
        """
        servers = Server.get_all(client)
        try:
            ips = set([sockaddr[0]
                for (_, _, _, _, sockaddr) in getaddrinfo(hostname, 22)])
        except gaierror:
            ips = set()
        for server in servers:
            instance = server.instance
            _logger.info("instance %s...", instance.dns_name)
            if instance.ip_address in ips or \
                    server.reservation.id == hostname:
                _logger.info("Found %s", instance)
                return server
        return None


    @_on_this_server
    def reboot(self):
        """Reboot this server.
        """
        # The decorator requires this to be an instance method
        # pylint: disable=R0201
        reboot(120)


    def get_volumes(self):
        """Return all of the volumes attached to this server.
        """
        volumes = []
        all_volumes = self.cnx.get_all_volumes()
        for volume in all_volumes:
            if volume.attach_data.instance_id == self.instance.id:
                found = Volume(self, volume, volume.attach_data.device,
                    volume.attach_data.status == 'attached')
                _logger.info("Found volume %s on %s",
                    found.volume.id, found.device)
                volumes.append(found)
        return volumes


    @_on_this_server
    def install_packages(self, *packages):
        """Install the specified packages on the machine.
        """
        # The decorator requires this to be an instance method
        # pylint: disable=R0201
        if packages:
            package_names =  ' '.join(packages)
            _logger.info("Making sure the following packages are installed: %s",
                package_names)
            sudo('apt-get install -y %s' % package_names)


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
        self.install_packages('byobu', 'update-notifier-common',
            'python-software-properties')


    def add_role(self, name, parameter=None):
        """Add a single specific role to the server (with optional parameter).
        """
        adders = self.get_role_adders((name, parameter))
        self.add_roles(adders)


    @_on_this_server
    def add_roles(self, role_adders):
        """Adds a list of roles to the server.
        """
        for role_adder in role_adders:
            self.install_packages(*role_adder.packages)
            role_adder.configure(self)


    def stop(self):
        """Stop the server, but do not terminate it.
        """
        self.instance.stop()
        while self.instance.state != 'stopped':
            _logger.info("Wating 10s for instance to stop...")
            time.sleep(10)
            self.instance.update()
        _logger.info("Instance state now %s", self.instance.state)


    def restart(self):
        """Ask the server instance to restart from a stopped state.
        """
        self.instance.start()
        while self.instance.state != 'running':
            _logger.info("Wating 10s for instance to restart...")
            time.sleep(10)
            self.instance.update()
        _logger.info("Instance state now %s", self.instance.state)


    def terminate(self):
        """Terminate the server waiting for it to shut down.
        """
        self.instance.terminate()
        while self.instance.state != 'terminated':
            _logger.info("Wating 10s for instance to terminate...")
            time.sleep(10)
            self.instance.update()
        _logger.info("Instance state now %s", self.instance.state)


    @classmethod
    def get_role_adders(cls, *roles):
        """Convert the arguments into a list of commands or options and values.
        """
        role_adders = []
        for role_argument in roles:
            if type(role_argument) == tuple:
                role, parameter = role_argument
            else:
                role, parameter = role_argument, None
            import_names = ['AddRole', 'Configure']
            try:
                module = __import__(role, globals(), locals(), import_names)
            except ImportError:
                try:
                    module = __import__('profab.role.%s' % role, globals(),
                        locals(), import_names)
                except ImportError:
                    raise ImportError("Could not import %s or profab.role.%s" %
                        (role, role))
            if parameter:
                role_adders.append(module.Configure(parameter))
            else:
                role_adders.append(module.AddRole())
        return role_adders

