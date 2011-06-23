import socket

from profab import _Keys
from profab.tests.mockboto.image import MockInstance, MockImage


class Cnx(object):
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def get_all_key_pairs(self):
        return [_Keys(name=socket.gethostname())]


class  AuthnCnx(Cnx):
    def __init__(self, *args):
        super(AuthnCnx, self).__init__(*args)
        self.key_pairs = []
        self.key_pairs_created = []

    def get_all_key_pairs(self):
        if self.key_pairs:
            return self.key_pairs
        else:
            return super(AuthnCnx, self).get_all_key_pairs()
    
    def create_key_pair(self, host):
        self.key_pairs_created.append(host)
        key_pair = _Keys(name=host)
        key_pair.save = lambda f: None
        return key_pair


class ServerCnx(Cnx):
    def get_all_images(self, image):
        return [MockImage()]

    def get_all_instances(self):
        return [_Keys(instances=[MockInstance('running')])]
