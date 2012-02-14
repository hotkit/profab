from unittest2 import TestCase
import mock

from fabric.api import env

from profab.server import Server

from profab.tests.mockboto.connection import MockConnection, regions
from profab.tests.mockfabric.connections import start_connection


class TestRoles(TestCase):
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
    def test_munin(self):
        server = Server.connect('test', 'ec2-host')
        server.add_role('munin')
        server.add_role('munin', 'monitor.example.com')


    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.ec2.regions', regions)
    @mock.patch('profab.role.wsgi.exists', lambda f: True)
    @mock.patch('profab.role.wsgi.sudo', start_connection)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('profab.server.sudo', start_connection)
    def test_wsgi_with_default_site(self):
        server = Server.connect('test', 'ec2-host')
        server.add_role('wsgi')

    @mock.patch('os.mkdir', lambda p: None)
    @mock.patch('profab.connection.EC2Connection', MockConnection)
    @mock.patch('profab.ec2.regions', regions)
    @mock.patch('profab.role.wsgi.exists', lambda f: False)
    @mock.patch('profab.role.wsgi.sudo', start_connection)
    @mock.patch('profab.server.getaddrinfo', lambda h, p:
            [(0, 0, 0, '', ('10.56.32.4', p))])
    @mock.patch('profab.server.sudo', start_connection)
    def test_wsgi_without_www_data_homedir(self):
        server = Server.connect('test', 'ec2-host')
        server.add_role('wsgi')
