import mock
from socket import gaierror
from unittest2 import TestCase

from fabric.api import env

from profab.server import Server

from profab.tests.mockboto.connection import MockConnection, regions
from profab.tests.mockfabric.connections import start_connection


def _do_raise(t, a):
    raise t(a)


class ServerLifecycle(TestCase):
    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_start_basic(self):
        server = Server.start('test')
        self.assertEquals(str(server),
            u"ec2-host -- running (host) [default] {}")

    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.role.postgres.exists', lambda f: True)
    @mock.patch('profab.role.postgres.run', start_connection)
    @mock.patch('profab.role.postgres.sed', lambda *a, **kw: None)
    @mock.patch('profab.role.postgres.sudo', start_connection)
    @mock.patch('profab.role.smarthost.sudo', start_connection)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_start_with_roles(self):
        server = Server.start('test', 'postgres', 'smarthost')
        self.assertEquals(str(server),
            u"ec2-host -- running (host) [default] {}")

    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_start_with_ami(self):
        server = Server.start('test', ('ami', 'test-ami'))
        self.assertEqual(server.instance.image_id, 'test-ami')

    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_start_with_region(self):
        server = Server.start('test', ('region', 'bangkok'), ('ami', 'test-ami'))
        self.assertEqual(server.instance.region.name, 'bangkok')
        self.assertEqual(server.instance.image_id, 'test-ami')

    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_start_with_size(self):
        server = Server.start('test', ('size', 'c1.xlarge'))
        self.assertEqual(server.instance.instance_type, 'c1.xlarge')

    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.role.ami.ubuntu._fetch_html', lambda u:
        r'''
{ "aaData":
[
["us-east-1","precise","12.04 LTS","amd64","ebs","20161109","<a href=\"https://console.aws.amazon.com/ec2/home?region=us-east-1#launchAmi=ami-f8d4f9ef\">ami-f8d4f9ef</a>","aki-919dcaf8"],
["us-east-1","precise","12.04 LTS","i386","ebs","20161109","<a href=\"https://console.aws.amazon.com/ec2/home?region=us-east-1#launchAmi=ami-bddaf7aa\">ami-bddaf7aa</a>","aki-8f9dcae6"],
]
}
        ''')
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_start_customise_bits(self):
        server = Server.start('test', ('size', 't1.micro'), ('bits', '64'), ('ami.precise', None))
        self.assertEqual(server.instance.instance_type, 't1.micro')
        self.assertEqual(server.instance.image_id, 'ami-f8d4f9ef')

    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.ec2.regions', regions)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_connect_and_upgrade(self):
        server = Server.connect('test', 'ec2-host')
        server.dist_upgrade()

    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.ec2.regions', regions)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            _do_raise(gaierror, "IP not found"))
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_connect_to_reservation_name(self):
        server = Server.connect('test', 'r-reservation')
        self.assertEquals(server.reservation.id, 'r-reservation')

    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_security_group(self):
        server = Server.start('kirit', ('security_group', 'web'))
        self.assertItemsEqual([g.id for g in server.instance.groups], ['web'])

    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_security_groups(self):
        server = Server.start('kirit', ('security_group', 'web'), ('security_group', 'ssh'))
        self.assertItemsEqual([g.id for g in server.instance.groups], ['web', 'ssh'])


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.ec2.regions', regions)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('time.sleep', lambda s: None)
    def test_connect_and_stop(self):
        server = Server.connect('test', 'ec2-host')
        server.stop()


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.ec2.regions', regions)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            _do_raise(gaierror, "IP not found"))
    @mock.patch('time.sleep', lambda s: None)
    def test_connect_and_restart(self):
        server = Server.connect('test', 'r-reservation')
        server.restart()


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.ec2.regions', regions)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('time.sleep', lambda s: None)
    def test_connect_and_terminate(self):
        server = Server.connect('test', 'ec2-host')
        server.terminate()


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.ec2.regions', regions)
    @mock.patch('profab.role.postgres.exists', lambda f: True)
    @mock.patch('profab.role.postgres.run', lambda s: start_connection() or 'No rows')
    @mock.patch('profab.role.postgres.sed', lambda *a, **kw: None)
    @mock.patch('profab.role.postgres.sudo', lambda s, user=None: start_connection() or '0 rows')
    @mock.patch('profab.role.wsgi.exists', lambda f: True)
    @mock.patch('profab.role.wsgi.sudo', start_connection)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('profab.server.sudo', start_connection)
    def test_connect_and_add_role(self):
        server = Server.connect('test', 'ec2-host')
        server.add_role('postgres')
        server.add_role('wsgi')


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.ec2.regions', regions)
    @mock.patch('profab.role.munin.exists', lambda f: True)
    @mock.patch('profab.role.munin.put', start_connection)
    @mock.patch('profab.role.munin.run', start_connection)
    @mock.patch('profab.role.munin.sudo', start_connection)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('profab.server.sudo', start_connection)
    def test_connect_and_configure(self):
        server = Server.connect('test', 'ec2-host')
        server.add_role('munin', 'monitor.example.com')
        server.add_role('eip', '10.43.56.9')


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.ec2.regions', regions)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.5', p))])
    def test_try_connect_to_invalid_host(self):
        server = Server.connect('test', 'not-a-host')
        self.assertIs(server, None)

    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.ec2.regions', regions)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('time.sleep', lambda s: None)
    def test_server_role_not_found(self):
        server = Server.connect('test', 'ec2-host')
        with self.assertRaises(ImportError):
            server.add_role('not-a-role')

class ServerMeta(TestCase):
    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.ec2.regions', regions)
    def test_get_servers(self):
        servers = Server.get_all('test')
