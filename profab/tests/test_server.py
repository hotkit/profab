from unittest2 import TestCase
import mock

from profab.tests.mockboto.connection import ServerCnx, AuthnCnx

from profab.server import Server


class ServerLifecycle(TestCase):
    @mock.patch('profab.authentication.EC2Connection', AuthnCnx)
    @mock.patch('profab.server.EC2Connection', ServerCnx)
    def test_start_basic(self):
        server = Server.start('test')
