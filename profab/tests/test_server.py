from unittest2 import TestCase
import mock

from fabric.api import env

from profab.server import Server

from profab.tests.mockboto.connection import MockConnection, regions
from profab.tests.mockfabric.connections import start_connection


class ServerLifecycle(TestCase):
    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.server.EC2Connection', MockConnection)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_start_basic(self):
        server = Server.start('test')
        self.assertEquals(str(server),
            u"ec2-host (host) [default] {}")


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.server.EC2Connection', MockConnection)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_start_with_role(self):
        server = Server.start('test', 'postgres')
        self.assertEquals(str(server),
            u"ec2-host (host) [default] {}")


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.server.EC2Connection', MockConnection)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    def test_connect_and_upgrade(self):
        server = Server.connect('test', 'ec2-host')
        server.dist_upgrade()


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.server.EC2Connection', MockConnection)
    @mock.patch('time.sleep', lambda s: None)
    def test_connect_and_terminate(self):
        server = Server.connect('test', 'ec2-host')
        server.terminate()


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.server.EC2Connection', MockConnection)
    @mock.patch('profab.server.sudo', start_connection)
    def test_connect_and_add_role(self):
        server = Server.connect('test', 'ec2-host')
        server.add_role('postgres')


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.role.munin.exists', lambda f: True)
    @mock.patch('profab.role.munin.put', start_connection)
    @mock.patch('profab.role.munin.run', start_connection)
    @mock.patch('profab.role.munin.sudo', start_connection)
    @mock.patch('profab.server.EC2Connection', MockConnection)
    @mock.patch('profab.server.sudo', start_connection)
    def test_connect_and_configure(self):
        server = Server.connect('test', 'ec2-host')
        server.add_role('munin')
        server.add_role('munin', 'monitor.example.com')


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.server.EC2Connection', MockConnection)
    def test_try_connect_to_invalid_host(self):
        server = Server.connect('test', 'not-a-host')
        self.assertIs(server, None)

    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.server.EC2Connection', MockConnection)
    @mock.patch('time.sleep', lambda s: None)
    def test_server_role_not_found(self):
        server = Server.connect('test', 'ec2-host')
        with self.assertRaises(ImportError):
            server.add_role('not-a-role')


class ServerMeta(TestCase):
    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.server.EC2Connection', MockConnection)
    @mock.patch('profab.server.regions', regions)
    def test_get_servers(self):
        servers = Server.get_all('test')
