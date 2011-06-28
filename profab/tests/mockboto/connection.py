import socket

from profab import _Keys
from profab.tests.mockboto.image import MockInstance, MockImage


class MockConnection(object):
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self._key = aws_access_key_id
        self._secret = aws_secret_access_key
        self._key_pairs = []
        self._key_pairs_created = []

    def attach_volume(self, volume_id, instance_id, device):
        print "Attaching", volume_id, instance_id, device
        return True

    def create_key_pair(self, host):
        self._key_pairs_created.append(host)
        key_pair = _Keys(name=host)
        key_pair.save = lambda f: None
        self._key_pairs.append(key_pair)
        return key_pair

    def create_volume(self, size, zone):
        return _Keys(id='volume:a')

    def get_all_key_pairs(self):
        return self._key_pairs

    def get_all_images(self, image):
        return [MockImage()]

    def get_all_instances(self):
        return [_Keys(instances=[MockInstance('running')])]

    def get_all_zones(self):
        return [_Keys()]


class Region(object):
    def connect(self, aws_access_key_id, aws_secret_access_key):
        return MockConnection(aws_access_key_id, aws_secret_access_key)


def regions(**kwargs):
    cnx = MockConnection(**kwargs)
    return [Region(), Region()]
