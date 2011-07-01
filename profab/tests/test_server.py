from unittest2 import TestCase
import mock

from fabric.api import env
from fabric.state import connections

from profab.server import Server

from profab.tests.mockboto.connection import ServerCnx, AuthnCnx, regions


def _start_connection(*args, **kwargs):
    print env.host_string
    connections['ubuntu@%s:22' % env.host_string] = True
    return ''

class ServerLifecycle(TestCase):
    @mock.patch('profab.server.EC2Connection', ServerCnx)
    @mock.patch('profab.server.append', _start_connection)
    @mock.patch('profab.server.reboot', _start_connection)
    @mock.patch('profab.server.run', _start_connection)
    @mock.patch('profab.server.sudo', _start_connection)
    @mock.patch('time.sleep', lambda s: None)
    @mock.patch('os.mkdir', lambda p: None)
    def test_start_basic(self):
        server = Server.start('test')
        self.assertEquals(str(server),
            u"ec2-host (host) [default] {}")


    @mock.patch('profab.server.EC2Connection', ServerCnx)
    @mock.patch('profab.server.append', _start_connection)
    @mock.patch('profab.server.reboot', _start_connection)
    @mock.patch('profab.server.run', _start_connection)
    @mock.patch('profab.server.sudo', _start_connection)
    @mock.patch('time.sleep', lambda s: None)
    @mock.patch('os.mkdir', lambda p: None)
    def test_start_with_role(self):
        server = Server.start('test', 'postgres')
        self.assertEquals(str(server),
            u"ec2-host (host) [default] {}")


    @mock.patch('profab.server.EC2Connection', ServerCnx)
    @mock.patch('profab.server.append', _start_connection)
    @mock.patch('profab.server.reboot', _start_connection)
    @mock.patch('profab.server.run', _start_connection)
    @mock.patch('profab.server.sudo', _start_connection)
    @mock.patch('time.sleep', lambda s: None)
    @mock.patch('os.mkdir', lambda p: None)
    def test_connect_and_upgrade(self):
        server = Server.connect('test', 'ec2-host')
        server.dist_upgrade()


    @mock.patch('profab.server.EC2Connection', ServerCnx)
    @mock.patch('time.sleep', lambda s: None)
    @mock.patch('os.mkdir', lambda p: None)
    def test_connect_and_terminate(self):
        server = Server.connect('test', 'ec2-host')
        server.terminate()


    @mock.patch('profab.server.EC2Connection', ServerCnx)
    @mock.patch('profab.server.sudo', _start_connection)
    @mock.patch('os.mkdir', lambda p: None)
    def test_connect_and_add_role(self):
        server = Server.connect('test', 'ec2-host')
        server.add_role('postgres')


    @mock.patch('profab.role.munin.exists', lambda f: True)
    @mock.patch('profab.role.munin.put', _start_connection)
    @mock.patch('profab.role.munin.run', _start_connection)
    @mock.patch('profab.role.munin.sudo', _start_connection)
    @mock.patch('profab.server.EC2Connection', ServerCnx)
    @mock.patch('profab.server.sudo', _start_connection)
    @mock.patch('os.mkdir', lambda p: None)
    def test_connect_and_configure(self):
        server = Server.connect('test', 'ec2-host')
        server.add_role('munin')
        server.add_role('munin', 'monitor.example.com')


    @mock.patch('profab.server.EC2Connection', ServerCnx)
    @mock.patch('os.mkdir', lambda p: None)
    def test_try_connect_to_invalid_host(self):
        server = Server.connect('test', 'not-a-host')
        self.assertIs(server, None)

    @mock.patch('profab.server.EC2Connection', ServerCnx)
    @mock.patch('time.sleep', lambda s: None)
    @mock.patch('os.mkdir', lambda p: None)
    def test_server_role_not_found(self):
        server = Server.connect('test', 'ec2-host')
        with self.assertRaises(ImportError):
            server.add_role('not-a-role')


class ServerMeta(TestCase):
    @mock.patch('profab.server.EC2Connection', ServerCnx)
    @mock.patch('profab.server.regions', regions)
    @mock.patch('os.mkdir', lambda p: None)
    def test_get_servers(self):
        servers = Server.get_all('test')
