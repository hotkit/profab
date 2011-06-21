import socket

from profab import _Keys
from profab.tests.mockboto.image import MockImage


class Cnx(object):
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def get_all_key_pairs(self):
        return [_Keys(name=socket.gethostname())]


class  AuthnCnx(Cnx):
    pass


class ServerCnx(Cnx):
    def get_all_images(self, image):
        return [MockImage()]
