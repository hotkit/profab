from unittest2 import TestCase
import mock

from profab import _Configuration
from profab.ebs import Volume

from profab.tests.mockboto.connection import MockConnection


class TestVolumes(TestCase):
    @mock.patch('profab.server.EC2Connection', MockConnection)
    def test_create(self):
        config = _Configuration('kirit')
        connection = MockConnection(config.keys.api, config.keys.secret)
        volume = Volume.create(connection, connection.get_all_zones()[0], 2)
