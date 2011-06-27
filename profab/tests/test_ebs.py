from unittest2 import TestCase

from boto.ec2.connection import EC2Connection

from profab import _Configuration
from profab.ebs import Volume


class TestVolumes(TestCase):
    def test_create(self):
        config = _Configuration('kirit')
        connection = EC2Connection(config.keys.api, config.keys.secret)
        volume = Volume.create(connection)
