from unittest2 import TestCase
import mock

from profab import _Configuration
from profab.ebs import Volume
from profab.server import Server

from profab.tests.mockboto.connection import MockConnection
from profab.tests.mockfabric.connections import start_connection


class TestVolumes(TestCase):
    @mock.patch('profab.server.EC2Connection', MockConnection)
    @mock.patch('profab.server.append', start_connection)
    @mock.patch('profab.server.reboot', start_connection)
    @mock.patch('profab.server.run', start_connection)
    @mock.patch('profab.server.sudo', start_connection)
    @mock.patch('time.sleep', lambda s: None)
    @mock.patch('os.mkdir', lambda p: None)
    def test_create(self):
        server = Server.start('test-volume')
        volume = Volume.create(server, 2)
        self.assertTrue(volume.attached)
